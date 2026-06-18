"""B2.4 orchestrator — Arm-A direct→indirect cross-family cheap-rung directional read.

Runs the **single** Arm-A fold (one direct-train pool → one *pooled* cross-family test over the 4
two-class slices BIPIA / InjecAgent / JBB / XSTest) at the local/free rungs (tfidf + frozen
ModernBERT-base) × ≥3 seeds, for two pools (criteria Rev 3 + decision 5):

* **capped** (primary)  — the capped-balanced direct pool (tfidf + frozen);
* **uncapped** (robust) — the uncapped natural-mix dominance check (**tfidf only**; embedding ≈1.1M
  texts on the local GPU is impractical — frozen-uncapped deferred + LOGGED).

It then computes, **reusing the Arm-B verdict machinery unchanged** (``falsify_dialect_lodo``):

* the **pooled gate** ``Gx = val_roc − test_roc`` with the label-stratified cluster bootstrap CI +
  presence-of-transfer ``perm_p`` (``directional_table([arm_a_pooled])``) — clusters span slices,
  slice-prefixed for global uniqueness (criteria §Statistics line 170);
* a **descriptive per-slice** ROC table (the §v lead result; no per-slice CI — Rev 2 §b fixes the
  gate to the single pooled Gx, no multiplicity);
* the descriptive **injection-only** (BIPIA+InjecAgent) sub-aggregate (§v, non-gating);
* the **over-defense FPR** column on NotInject at a **val-fixed** low-FPR threshold (mirrors M1
  ``harness._val_threshold`` / ADR-027; ``recall_at_fpr`` → ``metrics.benign_fpr``);
* the **E8** off-the-shelf detector reference column (``e8_reference``).

It does **NOT** run lora, compute a verdict, or commit (the SURVIVES/FALSIFIED/SMALL-THROUGHOUT
verdict is lora-gated at B3). Persists per-(pool,rung,seed) predictions + metrics under
``B2_4_results/`` plus a compact ``summary.json``.

Run (full sweep; smoke is ``--smoke``)::

    uv run python experiments/cross-family-transfer/run_b2_4.py --pool capped --rungs tfidf frozen
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from eval_toolkit.artifacts import write_json_strict
from eval_toolkit.thresholds import recall_at_fpr

_HERE = Path(__file__).resolve().parent
_ATTACK_LODO_DIR = _HERE.parent / "attack-type-lodo"
for _p in (_HERE, _ATTACK_LODO_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import assemble_arm_a as aa  # noqa: E402
import detectors  # noqa: E402  # attack-type-lodo detectors
import e8_reference  # noqa: E402
import falsify_dialect_lodo as fdl  # noqa: E402
import folds_dialect as fd  # noqa: E402
import metrics  # noqa: E402
from run_b2_3 import _CachedFrozenEmbedder  # noqa: E402  # reuse the cached frozen embedder

RESULTS_DIR = _HERE / "B2_4_results"
DEFAULT_SEEDS: tuple[int, ...] = (0, 1, 2)
FOLD_NAME = "arm_a_pooled"
BENIGN_FPR_TARGET = 0.01  # val-fixed over-defense FPR (mirrors M1 _BENIGN_FPR_TARGET; <2% per §v)


def _build_fold(*, cap: int | None, seed: int) -> fd.Fold:
    """Build the single Arm-A ``arm_a_pooled`` fold (in-distribution val carve from train)."""
    manifest = fd._load_leakage_manifest()  # noqa: SLF001 — the §vi clean-manifest (decision 9)
    train = aa.assemble_arm_a_train(cap=cap, seed=seed, clean_manifest=manifest)
    test = aa.assemble_arm_a_test(seed=seed)
    inner, val = fd.carve_val_from_train(
        train, seed=seed, min_types_for_typeholdout=10**9, val_frac=0.2
    )
    fold = fd.Fold(FOLD_NAME, inner, val, test, test_types=())
    fold.train.attrs["realized"] = train.attrs.get("realized", {})
    return fold


def _fit_tfidf(fold: fd.Fold, *, seed: int) -> dict[str, Any]:
    """Fit tfidf; return scores + a score_fn (for NotInject) + val_roc + recipe."""
    det = detectors.make_detector("tfidf", seed=seed)
    recipe = det.fit(
        fold.train["text"].tolist(),
        fold.train["label"].tolist(),
        fold.val["text"].tolist(),
        fold.val["label"].tolist(),
    )

    def score_fn(texts: Sequence[str]) -> np.ndarray:
        return np.asarray(det.predict_proba(list(texts)), dtype=float)

    val_scores = score_fn(fold.val["text"].tolist())
    return {
        "test_scores": score_fn(fold.test["text"].tolist()),
        "val_scores": val_scores,
        "val_roc": metrics.roc_auc_point(fold.val["label"].tolist(), val_scores),
        "score_fn": score_fn,
        "recipe": recipe,
    }


def _fit_frozen(fold: fd.Fold, embedder: _CachedFrozenEmbedder, *, seed: int) -> dict[str, Any]:
    """Fit the frozen rung (cached embeddings + LR head, C selected on val PR-AUC); same returns."""
    from sklearn.linear_model import LogisticRegression

    x_tr = embedder.embed(fold.train["text"].tolist())
    x_val = embedder.embed(fold.val["text"].tolist())
    best: tuple[float, float, LogisticRegression] | None = None
    for c in (0.1, 1.0, 10.0):
        clf = LogisticRegression(C=c, class_weight="balanced", max_iter=2000, random_state=seed)
        clf.fit(x_tr, fold.train["label"].tolist())
        score = detectors._val_pr_auc(  # noqa: SLF001 — reuse the model-selection metric
            fold.val["label"].tolist(), clf.predict_proba(x_val)[:, 1]
        )
        if best is None or score > best[0]:
            best = (score, c, clf)
    assert best is not None
    clf = best[2]

    def score_fn(texts: Sequence[str]) -> np.ndarray:
        return np.asarray(clf.predict_proba(embedder.embed(list(texts)))[:, 1], dtype=float)

    val_scores = score_fn(fold.val["text"].tolist())
    return {
        "test_scores": score_fn(fold.test["text"].tolist()),
        "val_scores": val_scores,
        "val_roc": metrics.roc_auc_point(fold.val["label"].tolist(), val_scores),
        "score_fn": score_fn,
        "recipe": {"C": best[1], "val_pr_auc": best[0]},
    }


def _over_defense(
    fold: fd.Fold, fit: dict[str, Any], notinject: pd.DataFrame, *, fpr: float = BENIGN_FPR_TARGET
) -> dict[str, Any]:
    """Over-defense FPR on NotInject at a val-fixed low-FPR threshold (mirrors M1 / ADR-027 §5)."""
    res = recall_at_fpr(
        np.asarray(fold.val["label"].to_numpy()), np.asarray(fit["val_scores"]), fpr
    )
    thr = float(res.threshold)
    ni_scores = fit["score_fn"](notinject["text"].tolist())
    return {
        "target_fpr": fpr,
        "val_threshold": None if thr == float("inf") else thr,
        "over_defense_fpr": metrics.benign_fpr(ni_scores, threshold=thr),
        "n_notinject": int(len(notinject)),
    }


def run_pool(
    *,
    pool: str,
    seeds: Sequence[int],
    rungs: Sequence[str],
    out_dir: Path,
    embedder: _CachedFrozenEmbedder | None,
    notinject: pd.DataFrame,
) -> dict[str, Any]:
    """Run one Arm-A pool: persist per-(rung,seed) preds+metrics; return the over-defense column."""
    cap = aa.CAP if pool == "capped" else None
    out_dir.mkdir(parents=True, exist_ok=True)
    over_defense: dict[str, list[dict[str, Any]]] = {r: [] for r in rungs}
    realized: dict[str, Any] = {}
    for seed in seeds:
        fold = _build_fold(cap=cap, seed=seed)
        realized = fold.train.attrs.get("realized", realized)
        fold_dir = out_dir / f"seed={seed}" / FOLD_NAME
        fold_dir.mkdir(parents=True, exist_ok=True)
        for rung in rungs:
            if rung == "tfidf":
                fit = _fit_tfidf(fold, seed=seed)
            elif rung == "frozen":
                assert embedder is not None
                fit = _fit_frozen(fold, embedder, seed=seed)
            else:
                raise ValueError(f"B2.4 is cheap-rung only; got rung {rung!r}")

            preds = fold.test.loc[:, ["cluster_id", "label", "slice"]].copy()
            preds["y_score"] = fit["test_scores"]
            preds.to_parquet(fold_dir / f"{rung}.predictions.parquet", index=False)
            test_roc = metrics.roc_auc_point(fold.test["label"].tolist(), fit["test_scores"])
            record = {
                "rung": rung,
                "pool": pool,
                "fold": FOLD_NAME,
                "seed": seed,
                "val_roc_auc": fit["val_roc"],
                "test_roc_auc": test_roc,
                "recipe": fit["recipe"],
                "n_train": int(len(fold.train)),
                "n_val": int(len(fold.val)),
                "n_test": int(len(fold.test)),
            }
            write_json_strict(record, fold_dir / f"{rung}.metrics.json")
            over_defense[rung].append({"seed": seed, **_over_defense(fold, fit, notinject)})
            print(
                f"[{pool} seed={seed} {rung}] val_roc={fit['val_roc']:.3f} test_roc={test_roc:.3f} "
                f"Gx={fit['val_roc'] - test_roc:+.3f} n_train={len(fold.train)}"
            )
    return {"over_defense": over_defense, "realized": realized}


def _per_slice_table(out_dir: Path, rungs: Sequence[str], seeds: Sequence[int]) -> dict[str, Any]:
    """Descriptive per-slice ROC table (§v lead result; mean over seeds, no per-slice CI)."""
    table: dict[str, Any] = {}
    for rung in rungs:
        per_slice: dict[str, list[float]] = {}
        for seed in seeds:
            p = out_dir / f"seed={seed}" / FOLD_NAME / f"{rung}.predictions.parquet"
            df = pd.read_parquet(p)
            for sl, sub in df.groupby("slice"):
                if set(sub["label"].unique()) == {0, 1}:
                    per_slice.setdefault(str(sl), []).append(
                        metrics.roc_auc_point(sub["label"].tolist(), sub["y_score"].to_numpy())
                    )
        table[rung] = {sl: float(np.mean(v)) for sl, v in per_slice.items()}
    return table


def _injection_only(out_dir: Path, rungs: Sequence[str], seeds: Sequence[int]) -> dict[str, float]:
    """Descriptive injection-only (BIPIA+InjecAgent) pooled ROC per rung (§v non-gating)."""
    out: dict[str, float] = {}
    for rung in rungs:
        rocs = []
        for seed in seeds:
            df = pd.read_parquet(
                out_dir / f"seed={seed}" / FOLD_NAME / f"{rung}.predictions.parquet"
            )
            sub = df[df["slice"].isin(("BIPIA", "InjecAgent"))]
            rocs.append(metrics.roc_auc_point(sub["label"].tolist(), sub["y_score"].to_numpy()))
        out[rung] = float(np.mean(rocs))
    return out


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: smoke or full B2.4 Arm-A cheap-rung sweep → pooled gate + per-slice + over-defense."""
    p = argparse.ArgumentParser(
        description="B2.4 Arm-A direct→indirect cheap-rung directional read."
    )
    p.add_argument("--pool", choices=["capped", "uncapped"], default="capped")
    p.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    p.add_argument("--rungs", nargs="+", default=["tfidf", "frozen"], choices=["tfidf", "frozen"])
    p.add_argument("--out", type=Path, default=RESULTS_DIR)
    p.add_argument("--n-boot", type=int, default=fdl._N_BOOT)
    p.add_argument("--n-perm", type=int, default=fdl._N_PERM)
    p.add_argument("--frozen-batch-size", type=int, default=16)
    p.add_argument("--skip-e8", action="store_true")
    p.add_argument("--smoke", action="store_true", help="tfidf × 1 seed × capped, skip E8")
    args = p.parse_args(argv)

    if args.smoke:
        args.seeds, args.rungs, args.pool, args.skip_e8 = [0], ["tfidf"], "capped", True
    if args.pool == "uncapped" and "frozen" in args.rungs:
        print("[note] uncapped: frozen deferred (≈1.1M texts impractical on GPU) — tfidf only")
        args.rungs = [r for r in args.rungs if r != "frozen"]

    out_dir = args.out / args.pool
    embedder = (
        _CachedFrozenEmbedder(batch_size=args.frozen_batch_size) if "frozen" in args.rungs else None
    )
    notinject = aa.load_notinject_overdefense()

    pool_res = run_pool(
        pool=args.pool,
        seeds=args.seeds,
        rungs=args.rungs,
        out_dir=out_dir,
        embedder=embedder,
        notinject=notinject,
    )

    gate = fdl.directional_table(
        out_dir, [FOLD_NAME], rungs=args.rungs, n_boot=args.n_boot, n_perm=args.n_perm
    )
    summary: dict[str, Any] = {
        "study": "cross-family-transfer B2.4 (Arm-A direct→indirect cheap-rung read)",
        "criteria": "experiments/cross-family-transfer/criteria.md (Rev 3 + 4)",
        "note": (
            "Cheap rungs only — NO verdict (SURVIVES/FALSIFIED/SMALL-THROUGHOUT lora-gated at B3). "
            "Gate = pooled Gx over the 4 two-class slices; lead = the per-slice table (Rev 2 §b: a "
            "single pooled Gx, no multiplicity)."
        ),
        "pool": args.pool,
        "seeds": list(args.seeds),
        "rungs": list(args.rungs),
        "realized_train": pool_res["realized"],
        "pooled_gate": gate,
        "per_slice_table": _per_slice_table(out_dir, args.rungs, args.seeds),
        "injection_only_subagg": _injection_only(out_dir, args.rungs, args.seeds),
        "over_defense_fpr": pool_res["over_defense"],
    }
    if not args.skip_e8:
        test = aa.assemble_arm_a_test(seed=0)
        slices = {sl: sub.reset_index(drop=True) for sl, sub in test.groupby("slice")}
        summary["e8_reference"] = e8_reference.score_all_dialects(slices, seed=0)

    out_dir.mkdir(parents=True, exist_ok=True)
    write_json_strict(summary, out_dir / "summary.json")
    print(f"\nB2.4 ({args.pool}) done — summary → {out_dir / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
