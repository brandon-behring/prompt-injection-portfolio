"""C1 treated-arm runner: held-table carrier-LODO + synthetic table corpus (criteria.md).

Control = the ratified carrier-LODO artifacts as-committed
(``../attack-type-lodo/results/seed=*/carrier_lodo_table/``) — NEVER re-run here.
Treated = byte-identical fold construction (same ``build_examples`` frame per seed,
same ``make_fold`` carve — the Rev-2 in-distribution val lives inside ``make_fold``
for carrier folds) with ONE change: the leakage-gated synthetic table corpus
(``corpus_gated.parquet``) is appended to the **inner train** AFTER the val carve,
so val/test are byte-identical to control and the corpus rows can never leak into
either (they also carry ``source=synthetic_*`` + ``role=train`` for audit).

Per (seed, rung) writes ``C1_results_treated/seed={s}/carrier_lodo_table/
{rung}.predictions.parquet`` + ``{rung}.metrics.json`` (with ``val_roc_auc``) —
the exact layout ``falsify_carrier_lodo.load_carrier_fold`` and ``c1_verdict``
consume.

Rungs: ``tfidf``/``frozen`` local ($0). ``lora`` is accepted for the post-RunPod
merge path but is WRITE-GATED behind a separate present-first paid go
(criteria.md; do not run it locally).

Run::

    uv run python experiments/carrier-table-training/run_c1.py \
        [--seeds 0 1 2] [--rungs tfidf frozen] [--corpus corpus_gated.parquet]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from pathlib import Path

import numpy as np
import pandas as pd

_HERE = Path(__file__).resolve().parent
_LODO_DIR = _HERE.parent / "attack-type-lodo"
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
for _p in (_LODO_DIR, _OOD_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import detectors  # noqa: E402
import folds  # noqa: E402
import harness  # noqa: E402
import metrics  # noqa: E402
from bipia_carrier import build_examples  # noqa: E402  # type: ignore[import-not-found]
from eval_toolkit.artifacts import write_json_strict  # noqa: E402

FOLD_NAME = "carrier_lodo_table"
RESULTS_DIR = _HERE / "C1_results_treated"
# Match the control run's frame construction exactly (results/MANIFEST.yml config).
CONTEXTS_PER_ATTACK = 12
DEFAULT_SEEDS: tuple[int, ...] = (0, 1, 2)


def augment_train(fold_train: pd.DataFrame, corpus: pd.DataFrame) -> pd.DataFrame:
    """Append the gated corpus to the inner train (post-carve; the ONLY treated-arm change).

    Validates the corpus is train-only synthetic rows and projects it onto the
    fold's columns (corpus extras like ``context_sha256``/``format`` are dropped).

    Raises
    ------
    ValueError
        If the corpus contains non-train roles, non-synthetic sources, or lacks
        both classes (a single-class augmentation is a config error).
    """
    if set(corpus["role"].unique()) != {"train"}:
        raise ValueError(f"corpus roles must be exactly {{'train'}}: {set(corpus['role'])}")
    bad_src = set(corpus["source"].unique()) - {"synthetic_clean", "synthetic_inject"}
    if bad_src:
        raise ValueError(f"corpus has non-synthetic sources: {bad_src}")
    if set(corpus["label"].unique()) != {0, 1}:
        raise ValueError("corpus must contain both classes")
    projected = corpus.loc[:, [c for c in fold_train.columns if c in corpus.columns]]
    missing = set(fold_train.columns) - set(projected.columns)
    if missing:
        raise ValueError(f"corpus lacks fold columns: {sorted(missing)}")
    return pd.concat([fold_train, projected], ignore_index=True)


def run_treated_one(
    frame: pd.DataFrame,
    corpus: pd.DataFrame,
    rung: str,
    *,
    seed: int,
    n_bootstrap: int,
) -> tuple[dict[str, object], pd.DataFrame]:
    """One treated (seed, rung): control-identical fold, augmented inner train.

    Mirrors ``harness.run_one`` (val_roc_auc, headline, over-defense FPRs) with the
    augmentation inserted between the carve and the fit.
    """
    fold = folds.make_fold(frame, FOLD_NAME, seed=seed)
    train = augment_train(fold.train, corpus)
    detector = detectors.make_detector(rung, seed=seed)
    recipe = detector.fit(
        train["text"].tolist(),
        train["label"].tolist(),
        fold.val["text"].tolist(),
        fold.val["label"].tolist(),
    )
    test_scores = np.asarray(detector.predict_proba(fold.test["text"].tolist()), dtype=float)
    val_scores = np.asarray(detector.predict_proba(fold.val["text"].tolist()), dtype=float)

    val_auprc = float(recipe["val_pr_auc"])  # type: ignore[arg-type]
    headline = metrics.compute_fold_metrics(
        fold.test["label"].tolist(), test_scores, n_bootstrap=n_bootstrap, seed=seed
    )
    val_roc_auc = metrics.roc_auc_point(fold.val["label"].tolist(), val_scores)
    thr = harness._val_threshold(fold.val, val_scores, fpr=harness._BENIGN_FPR_TARGET)
    clean_context_fpr = metrics.benign_fpr(
        test_scores[fold.test["label"].to_numpy() == 0], threshold=thr
    )
    ni_texts = harness._load_notinject()
    notinject_fpr = (
        metrics.benign_fpr(
            np.asarray(detector.predict_proba(list(ni_texts)), dtype=float), threshold=thr
        )
        if ni_texts
        else None
    )

    record: dict[str, object] = {
        "arm": "treated",
        "rung": rung,
        "fold": FOLD_NAME,
        "seed": seed,
        "val_auprc": val_auprc,
        "val_roc_auc": val_roc_auc,
        "recipe": recipe,
        "headline": headline,
        "clean_context_fpr": clean_context_fpr,
        "notinject_fpr": notinject_fpr,
        "benign_threshold": None if thr == float("inf") else thr,
        "n_notinject": len(ni_texts),
        "test_types": list(fold.test_types),
        "n_train": int(len(train)),
        "n_train_control": int(len(fold.train)),
        "n_corpus_rows": int(len(corpus)),
        "n_val": int(len(fold.val)),
        "n_test": int(len(fold.test)),
    }
    predictions = fold.test.loc[:, [c for c in harness._PRED_COLUMNS if c != "y_score"]].copy()
    predictions["y_score"] = test_scores
    return record, predictions


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="C1 treated-arm cheap-rung sweep (held-table fold).")
    ap.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    ap.add_argument(
        "--rungs",
        nargs="+",
        default=["tfidf", "frozen"],
        choices=["tfidf", "frozen", "lora"],
        help="lora is write-gated behind a separate present-first paid go (criteria.md).",
    )
    ap.add_argument("--corpus", type=Path, default=_HERE / "corpus_gated.parquet")
    ap.add_argument("--n-bootstrap", type=int, default=1000)
    ap.add_argument("--out", type=Path, default=RESULTS_DIR)
    args = ap.parse_args(argv)

    gate_report = _HERE / "leakage_gate.json"
    if not gate_report.exists():
        print("run_c1: leakage_gate.json missing — run leakage_gate.py first", file=sys.stderr)
        return 1
    corpus = pd.read_parquet(args.corpus)
    corpus_sha = hashlib.sha256(args.corpus.read_bytes()).hexdigest()
    print(
        f"[c1] corpus rows={len(corpus)} "
        f"(pos={int((corpus['label'] == 1).sum())} neg={int((corpus['label'] == 0).sum())})",
        flush=True,
    )

    for seed in args.seeds:
        frame = build_examples(
            root=harness.BIPIA_ROOT, contexts_per_attack=CONTEXTS_PER_ATTACK, seed=seed
        ).frame
        fold_dir = args.out / f"seed={seed}" / FOLD_NAME
        fold_dir.mkdir(parents=True, exist_ok=True)
        for rung in args.rungs:
            record, predictions = run_treated_one(
                frame, corpus, rung, seed=seed, n_bootstrap=args.n_bootstrap
            )
            record["corpus_sha256"] = corpus_sha
            predictions.to_parquet(fold_dir / f"{rung}.predictions.parquet", index=False)
            write_json_strict(record, fold_dir / f"{rung}.metrics.json")
            print(
                f"[seed={seed} {rung}] val_roc={record['val_roc_auc']:.4f} "
                f"test_roc={metrics.roc_auc_point(predictions['label'].tolist(), predictions['y_score'].to_numpy()):.4f} "
                f"n_train={record['n_train']} (+{record['n_corpus_rows']} corpus)",
                flush=True,
            )

    manifest = {
        "experiment": "carrier-table-training (C1 treated arm)",
        "fold": FOLD_NAME,
        "seeds": list(args.seeds),
        "rungs": list(args.rungs),
        "contexts_per_attack": CONTEXTS_PER_ATTACK,
        "n_bootstrap": args.n_bootstrap,
        "corpus_sha256": corpus_sha,
        "control_tree": "../attack-type-lodo/results (as-committed; never re-run)",
    }
    (args.out / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", "utf-8")
    print(f"[c1] wrote manifest under {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
