"""Attack-type-LODO harness (ADR-052, spec §5/§6) — orchestrate + persist.

Drives the three pre-registered LODO folds (:mod:`folds`) × the detector rungs
(:mod:`detectors`) × a seed loop, computing the spec-§5 metric battery
(:mod:`metrics`) and **persisting** — per ``(rung, fold, seed)`` — the per-row
predictions parquet **and** a metrics JSON carrying the per-test-attack-type
diagnostic AUPRC + its val→test drop (the §5 retention pre-commit; the §6.5
falsification is impossible without it). A top-level ``MANIFEST.yml`` records the
config + git provenance + the full artifact list.

The val→test ("benchmarks lie") inflation reference is each rung's own
val-selected ``val_pr_auc`` (the in-distribution AUPRC under the chosen recipe);
the per-type drop is ``val_pr_auc − per_type_test_auprc``.

Run (default = the headline ceiling ``tfidf frozen lora``; ``full_ft`` deferred per ADR-054)::

    python experiments/attack-type-lodo/harness.py

``lora`` needs a 24 GB+ card (RunPod); the local cheap-rung half restricts ``--rungs``::

    python experiments/attack-type-lodo/harness.py --rungs tfidf frozen \
        --folds core_attack_type obfuscation_technique carrier_plus_attack_external --seeds 0 1 2

Re-stamp ``MANIFEST.yml`` from the on-disk union after a RunPod ``lora`` merge (no training)::

    python experiments/attack-type-lodo/harness.py \
        --finalize-manifest --out experiments/attack-type-lodo/results

The transformer rungs self-select device (:func:`detectors._select_device_dtype`); the CPU
smoke is ``--rungs tfidf --folds core_attack_type --seeds 0``.
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


def _scan_artifacts(out_dir: Path) -> list[dict[str, str]]:
    """Discover every persisted ``(rung, fold, seed)`` record on disk under ``out_dir``.

    Mirrors the ``seed=*/{fold}/{rung}.predictions.parquet`` layout :func:`run_sweep` writes.
    The ``{rung}.``-prefixed filenames are what make a merge of independently-produced rung
    trees a safe file-tree union (ADR-054 hybrid: local ``tfidf``/``frozen`` + a RunPod
    ``lora`` pull). Reference-scorer files (``reference_*.test_scores.parquet``) do not match
    the ``*.predictions.parquet`` glob, so they are never counted as rungs.
    """
    artifacts: list[dict[str, str]] = []
    for pq_path in sorted(out_dir.glob("seed=*/*/*.predictions.parquet")):
        rung = pq_path.name.split(".")[0]
        fold_name = pq_path.parent.name
        seed = pq_path.parent.parent.name.split("=")[1]
        json_path = pq_path.with_name(f"{rung}.metrics.json")
        artifacts.append(
            {
                "rung": rung,
                "fold": fold_name,
                "seed": seed,
                "predictions": str(pq_path.relative_to(out_dir)),
                "metrics": str(json_path.relative_to(out_dir)),
            }
        )
    return artifacts


def rebuild_manifest(
    out_dir: Path,
    *,
    base_config: dict[str, object] | None = None,
    git_sha: str | None = None,
) -> dict[str, object]:
    """(Re)write ``MANIFEST.yml`` from the **on-disk union** of artifacts under ``out_dir``.

    ``complete_headline_sweep`` is computed from what is present on disk (the union across
    possibly several invocations — e.g. local ``tfidf``/``frozen`` merged with a RunPod
    ``lora`` pull) against :data:`detectors.REQUIRED_RUNGS` (ADR-054). ``full_ft`` is
    selectable but **not** required, so it never blocks the §6.5 write-gate. The read-side
    gate (``falsify_ood_wall.manifest_complete``) is unchanged — it still trusts this flag.

    Parameters
    ----------
    out_dir : pathlib.Path
        The results tree (``seed=*/{fold}/{rung}.predictions.parquet``).
    base_config : dict, optional
        Invocation config to record (``n_bootstrap`` / ``contexts_per_attack`` / ``bipia_root``);
        when finalizing a merge, missing keys fall back to the prior manifest.
    git_sha : str, optional
        Provenance sha; falls back to the prior manifest's value, else a fresh capture.

    Returns
    -------
    dict
        The manifest payload (also written to ``{out_dir}/MANIFEST.yml``).
    """
    artifacts = _scan_artifacts(out_dir)
    present_rungs = {a["rung"] for a in artifacts}
    present_folds = {a["fold"] for a in artifacts}
    present_seeds = sorted({int(a["seed"]) for a in artifacts})

    prior_path = out_dir / "MANIFEST.yml"
    prior = (
        yaml.safe_load(prior_path.read_text(encoding="utf-8")) or {}
        if prior_path.exists()
        else {}
    )
    prior_cfg = prior.get("config", {}) if isinstance(prior.get("config"), dict) else {}
    cfg = dict(base_config or {})
    for key in ("n_bootstrap", "contexts_per_attack", "bipia_root"):
        cfg.setdefault(key, prior_cfg.get(key))

    manifest: dict[str, object] = {
        "spec": "docs/planning/attack-type-lodo-harness-spec.md",
        "adr": "ADR-052; ceiling per ADR-054",
        "generated_utc": datetime.now(UTC).isoformat(),
        "git_sha": git_sha or prior.get("git_sha") or capture_git_sha(REPO_ROOT),
        "config": {
            "seeds": present_seeds,
            "folds": sorted(present_folds),
            "rungs": sorted(present_rungs),
            "n_bootstrap": cfg.get("n_bootstrap"),
            "contexts_per_attack": cfg.get("contexts_per_attack"),
            "bipia_root": cfg.get("bipia_root"),
        },
        "required_rungs": list(detectors.REQUIRED_RUNGS),
        "complete_headline_sweep": (
            "core_attack_type" in present_folds
            and len(present_seeds) >= 3
            and present_rungs >= set(detectors.REQUIRED_RUNGS)
        ),
        "artifacts": artifacts,
    }
    prior_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    return manifest


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
    n_written = 0
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
                predictions.to_parquet(fold_dir / f"{rung}.predictions.parquet", index=False)
                write_json_strict(record, fold_dir / f"{rung}.metrics.json")
                n_written += 1
                print(
                    f"[seed={seed} {fold_name} {rung}] "
                    f"val_auprc={record['val_auprc']:.3f} "
                    f"test_auprc={headline_auprc(record):.3f} "
                    f"n_test={record['n_test']}"
                )

    # Completeness is derived from the on-disk UNION, not this invocation's rungs: a hybrid run
    # adds only some rungs (e.g. local tfidf+frozen, later merged with a RunPod lora pull —
    # ADR-054), and the manifest must reflect the merged tree to open the §6.5 write-gate.
    manifest = rebuild_manifest(
        out_dir,
        base_config={
            "n_bootstrap": n_bootstrap,
            "contexts_per_attack": contexts_per_attack,
            "bipia_root": str(BIPIA_ROOT.relative_to(REPO_ROOT)),
        },
        git_sha=capture_git_sha(REPO_ROOT),
    )
    on_disk = manifest["artifacts"]
    assert isinstance(on_disk, list)
    print(
        f"\nwrote {n_written} (rung,fold,seed) record(s) this run; MANIFEST.yml now lists "
        f"{len(on_disk)} on disk (complete_headline_sweep={manifest['complete_headline_sweep']}) "
        f"in {out_dir}"
    )
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
    # Default = the REQUIRED_RUNGS ceiling (tfidf+frozen+lora); full_ft stays selectable via
    # ``choices`` for the deferred trigger-gate (ADR-054).
    p.add_argument(
        "--rungs", nargs="+", default=list(detectors.REQUIRED_RUNGS), choices=detectors.RUNG_NAMES
    )
    p.add_argument("--n-bootstrap", type=int, default=1000)
    p.add_argument("--contexts-per-attack", type=int, default=12)
    p.add_argument("--out", type=Path, default=RESULTS_DIR)
    p.add_argument(
        "--finalize-manifest",
        action="store_true",
        help="re-stamp MANIFEST.yml from the on-disk union (post-merge), no training, then exit",
    )
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    """CLI entry point: parse args, run the sweep (or finalize a merged manifest), persist."""
    args = _parse_args(argv)
    if args.finalize_manifest:
        # Post-merge re-stamp only (ADR-054 hybrid): no training, no BIPIA needed.
        manifest = rebuild_manifest(args.out)
        print(
            f"re-stamped {args.out}/MANIFEST.yml from the on-disk union "
            f"(complete_headline_sweep={manifest['complete_headline_sweep']})"
        )
        return
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
