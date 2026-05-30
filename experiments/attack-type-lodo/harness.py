"""Attack-type-LODO harness (ADR-052, spec §5/§6) — orchestrate + persist.

Drives the three pre-registered LODO folds (:mod:`folds`) × four detector rungs
(:mod:`detectors`) × a seed loop, computing the spec-§5 metric battery
(:mod:`metrics`) and **persisting** — per ``(rung, fold, seed)`` — the per-row
predictions parquet **and** a metrics JSON carrying the per-test-attack-type
diagnostic AUPRC + its val→test drop (the §5 retention pre-commit; the §6.5
falsification is impossible without it). A top-level ``MANIFEST.yml`` records the
config + git provenance + the full artifact list.

The val→test ("benchmarks lie") inflation reference is each rung's own
val-selected ``val_pr_auc`` (the in-distribution AUPRC under the chosen recipe);
the per-type drop is ``val_pr_auc − per_type_test_auprc``.

Run (full sweep, ≥3 seeds)::

    python experiments/attack-type-lodo/harness.py

Run (CPU smoke — TF-IDF, core fold, one seed)::

    python experiments/attack-type-lodo/harness.py --rungs tfidf \
        --folds core_attack_type --seeds 0

Nothing here is GPU-gated; the transformer rungs self-select device
(:func:`detectors._select_device_dtype`). The smoke runs CPU-only by restricting
``--rungs`` to ``tfidf``.
"""

from __future__ import annotations

import argparse
import functools
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from eval_toolkit.artifacts import write_json_strict
from eval_toolkit.provenance import capture_git_sha

_HERE = Path(__file__).resolve().parent
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
for _p in (_HERE, _OOD_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

# Sibling-module imports: the experiment dir name is hyphenated, so it is not an
# importable package; these resolve via the sys.path injection above (same pattern
# as OOD_WALL_PREDICTION/run_prediction.py). Hence the E402 suppressions.
import detectors  # noqa: E402
import folds  # noqa: E402
import metrics  # noqa: E402
from bipia_carrier import build_examples  # noqa: E402  # type: ignore[import-not-found]

REPO_ROOT = _HERE.parent.parent
BIPIA_ROOT = REPO_ROOT / "data" / "raw" / "BIPIA" / "benchmark"
RESULTS_DIR = _HERE / "results"
DEFAULT_SEEDS: tuple[int, ...] = (0, 1, 2)

# Persisted prediction columns (full provenance for downstream paired-bootstrap).
_PRED_COLUMNS = ("text", "label", "attack_type", "subfamily", "carrier", "role", "y_score")
# Val-fixed FPR target for the over-defense (benign) threshold (spec §5; ADR-027).
_BENIGN_FPR_TARGET = 0.01


def _val_threshold(val_df: pd.DataFrame, val_scores: np.ndarray, *, fpr: float) -> float:
    """Score threshold fixing ``fpr`` false-positive rate on the val negatives.

    The over-defense (benign) FPR is reported at a **val-fixed** threshold so the
    test-negative slice can be single-class without re-tuning on test (spec §5;
    submission ADR-027). Returns ``inf`` when val has no negatives (no benign
    rows scored ≥ inf ⇒ a reported benign FPR of 0).

    Parameters
    ----------
    val_df : pandas.DataFrame
        The fold's validation rows (needs a ``label`` column).
    val_scores : numpy.ndarray
        P(positive) aligned with ``val_df``.
    fpr : float
        Target false-positive rate in ``(0, 1)``.

    Returns
    -------
    float
    """
    neg = val_scores[val_df["label"].to_numpy() == 0]
    if neg.size == 0:
        return float("inf")
    return float(np.quantile(neg, 1.0 - fpr))


@functools.lru_cache(maxsize=1)
def _load_notinject() -> tuple[str, ...]:
    """Load NotInject benign-with-trigger prompts (over-defense control, spec §5).

    Best-effort: returns an empty tuple if the dataset cannot be fetched, so the
    over-defense FPR is recorded as an explicit ``None`` (never a silent pass). Cached
    across the (rung, fold, seed) calls of a sweep.
    """
    try:
        from datasets import load_dataset

        ds = load_dataset("leolee99/NotInject", split="NotInject_one")
        return tuple(str(p) for p in ds["prompt"])
    except Exception as exc:  # noqa: BLE001 — optional over-defense control; never block the sweep
        print(f"[warn] NotInject unavailable ({type(exc).__name__}: {exc}); notinject_fpr=None")
        return ()


def run_one(
    frame: pd.DataFrame,
    fold_name: str,
    rung: str,
    *,
    seed: int,
    n_bootstrap: int,
) -> tuple[dict[str, object], pd.DataFrame]:
    """Build one fold, fit one rung, score test, and assemble its metrics + predictions.

    Parameters
    ----------
    frame : pandas.DataFrame
        The ``build_examples`` frame for this seed.
    fold_name : str
        One of :data:`folds.FOLD_NAMES`.
    rung : str
        One of :data:`detectors.RUNG_NAMES`.
    seed : int
        Seed for fold val-carve + detector recipe.
    n_bootstrap : int
        Bootstrap resamples for the headline scorecard CIs (0 = point-only).

    Returns
    -------
    (record, predictions) : tuple[dict, pandas.DataFrame]
        ``record`` is the JSON-bound metrics payload (headline + recipe + per-type
        drops); ``predictions`` is the per-row parquet frame.
    """
    fold = folds.make_fold(frame, fold_name, seed=seed)
    detector = detectors.make_detector(rung, seed=seed)
    recipe = detector.fit(
        fold.train["text"].tolist(),
        fold.train["label"].tolist(),
        fold.val["text"].tolist(),
        fold.val["label"].tolist(),
    )
    test_scores = np.asarray(detector.predict_proba(fold.test["text"].tolist()), dtype=float)

    val_auprc = float(recipe["val_pr_auc"])  # type: ignore[arg-type]  # in-distribution reference
    headline = metrics.compute_fold_metrics(
        fold.test["label"].tolist(), test_scores, n_bootstrap=n_bootstrap, seed=seed
    )
    per_type = metrics.per_type_diagnostics(
        fold.test, test_scores, fold.test_types, val_auprc=val_auprc
    )

    val_scores = np.asarray(detector.predict_proba(fold.val["text"].tolist()), dtype=float)
    thr = _val_threshold(fold.val, val_scores, fpr=_BENIGN_FPR_TARGET)
    # Two benign FPRs at the val-fixed threshold: clean carrier contexts (the fold's own
    # negatives) and NotInject benign-with-trigger prompts (the spec §5 over-defense control).
    clean_context_fpr = metrics.benign_fpr(
        test_scores[fold.test["label"].to_numpy() == 0], threshold=thr
    )
    ni_texts = _load_notinject()
    notinject_fpr = (
        metrics.benign_fpr(
            np.asarray(detector.predict_proba(list(ni_texts)), dtype=float), threshold=thr
        )
        if ni_texts
        else None
    )

    record: dict[str, object] = {
        "rung": rung,
        "fold": fold_name,
        "seed": seed,
        "val_auprc": val_auprc,
        "recipe": recipe,
        "headline": headline,
        "clean_context_fpr": clean_context_fpr,
        "notinject_fpr": notinject_fpr,
        "benign_threshold": None if thr == float("inf") else thr,
        "n_notinject": len(ni_texts),
        "test_types": list(fold.test_types),
        "per_type": per_type,
        "n_train": int(len(fold.train)),
        "n_val": int(len(fold.val)),
        "n_test": int(len(fold.test)),
    }
    predictions = fold.test.loc[:, [c for c in _PRED_COLUMNS if c != "y_score"]].copy()
    predictions["y_score"] = test_scores
    return record, predictions


def run_sweep(
    *,
    seeds: Sequence[int],
    fold_names: Sequence[str],
    rungs: Sequence[str],
    n_bootstrap: int,
    contexts_per_attack: int,
    out_dir: Path,
) -> dict[str, object]:
    """Run the full ``seeds × folds × rungs`` sweep, persisting every artifact.

    Writes, per ``(rung, fold, seed)``, ``{out}/seed={s}/{fold}/{rung}.predictions.parquet``
    and ``…/{rung}.metrics.json``; then a top-level ``{out}/MANIFEST.yml`` with config +
    git provenance + the artifact list.

    Returns
    -------
    dict
        The manifest payload (also written to disk).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts: list[dict[str, str]] = []
    for seed in seeds:
        frame = build_examples(
            root=BIPIA_ROOT, contexts_per_attack=contexts_per_attack, seed=seed
        ).frame
        for fold_name in fold_names:
            fold_dir = out_dir / f"seed={seed}" / fold_name
            fold_dir.mkdir(parents=True, exist_ok=True)
            for rung in rungs:
                record, predictions = run_one(
                    frame, fold_name, rung, seed=seed, n_bootstrap=n_bootstrap
                )
                pq_path = fold_dir / f"{rung}.predictions.parquet"
                json_path = fold_dir / f"{rung}.metrics.json"
                predictions.to_parquet(pq_path, index=False)
                write_json_strict(record, json_path)
                artifacts.append(
                    {
                        "rung": rung,
                        "fold": fold_name,
                        "seed": str(seed),
                        "predictions": str(pq_path.relative_to(out_dir)),
                        "metrics": str(json_path.relative_to(out_dir)),
                    }
                )
                print(
                    f"[seed={seed} {fold_name} {rung}] "
                    f"val_auprc={record['val_auprc']:.3f} "
                    f"test_auprc={headline_auprc(record):.3f} "
                    f"n_test={record['n_test']}"
                )

    manifest: dict[str, object] = {
        "spec": "docs/planning/attack-type-lodo-harness-spec.md",
        "adr": "ADR-052",
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_sha": capture_git_sha(REPO_ROOT),
        "config": {
            "seeds": list(seeds),
            "folds": list(fold_names),
            "rungs": list(rungs),
            "n_bootstrap": n_bootstrap,
            "contexts_per_attack": contexts_per_attack,
            "bipia_root": str(BIPIA_ROOT.relative_to(REPO_ROOT)),
        },
        "complete_headline_sweep": (
            set(fold_names) >= {"core_attack_type"}
            and len(seeds) >= 3
            and set(rungs) >= set(detectors.RUNG_NAMES)
        ),
        "artifacts": artifacts,
    }
    (out_dir / "MANIFEST.yml").write_text(
        yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8"
    )
    print(f"\nwrote {len(artifacts)} (rung,fold,seed) records + MANIFEST.yml to {out_dir}")
    return manifest


def headline_auprc(record: dict[str, object]) -> float:
    """Extract the headline test AUPRC value from a sweep record (``nan`` if skipped)."""
    headline = record["headline"]
    assert isinstance(headline, dict)
    cell = headline.get("pr_auc")
    if not isinstance(cell, dict) or cell.get("value") is None:
        return float("nan")
    return float(cell["value"])


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the harness CLI (sweep scope + persistence target)."""
    p = argparse.ArgumentParser(description="Attack-type-LODO harness (ADR-052, spec §5/§6).")
    p.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    p.add_argument("--folds", nargs="+", default=list(folds.FOLD_NAMES), choices=folds.FOLD_NAMES)
    p.add_argument(
        "--rungs", nargs="+", default=list(detectors.RUNG_NAMES), choices=detectors.RUNG_NAMES
    )
    p.add_argument("--n-bootstrap", type=int, default=1000)
    p.add_argument("--contexts-per-attack", type=int, default=12)
    p.add_argument("--out", type=Path, default=RESULTS_DIR)
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point: parse args, run the sweep, persist artifacts."""
    args = _parse_args(argv)
    if not BIPIA_ROOT.exists():
        raise FileNotFoundError(
            f"BIPIA benchmark not found at {BIPIA_ROOT}; expected data/raw/BIPIA/benchmark/."
        )
    run_sweep(
        seeds=args.seeds,
        fold_names=args.folds,
        rungs=args.rungs,
        n_bootstrap=args.n_bootstrap,
        contexts_per_attack=args.contexts_per_attack,
        out_dir=args.out,
    )


if __name__ == "__main__":
    main()
