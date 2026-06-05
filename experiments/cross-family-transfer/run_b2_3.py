"""B2.3 orchestrator — Arm-B B− cheap-rung directional read (cross-family-transfer/criteria.md).

Runs the **B− (indirect-only)** Arm-B dialect-LODO sweep at the two *local/free* rungs (tfidf +
frozen ModernBERT-base) × ≥3 seeds × two train compositions (**natural-mix** and
**dialect-balanced**), holding out each of the 4 indirect dialects (bipia / browsesafe / fujitsu /
injecagent). It then computes the per-dialect × per-rung directional ``Gx`` table (label-stratified
cluster bootstrap + per-fold permutation; :mod:`falsify_dialect_lodo`) and the E8 off-the-shelf
reference column (:mod:`e8_reference`). It does **NOT** run lora, compute a verdict, or commit.

Pre-reg conformance (criteria Rev 1/2):

* B− only (B+ needs the Arm-A direct base → B2.4); the held-out dialect is the only shifted axis.
* In-distribution val carve (``min_types_for_typeholdout = 10**9``) via the shared
  ``make_dialect_fold`` — so ``val_roc`` does not inherit the §6.5 attack-type collapse.
* ``val_frac = 0.2``; ``contexts_per_attack = 12``; ModernBERT-base frozen embedder; fp16 on the
  local Turing GPU (``detectors._select_device_dtype``). Frozen embeddings are cached per text and
  reused across seeds (the carve is the only seed-dependent step).
* **Primary condition = B− natural-mix** (criteria Rev 2 (c)); dialect-balanced = the dominance
  robustness check.

Persists predictions + per-(rung,fold,seed) metrics under ``B2_3_results/<condition>/`` plus a
compact ``summary.json`` with the directional table + E8 column.

Run (full sweep — the smoke is ``--smoke``)::

    uv run python experiments/cross-family-transfer/run_b2_3.py
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

_HERE = Path(__file__).resolve().parent
_ATTACK_LODO_DIR = _HERE.parent / "attack-type-lodo"
for _p in (_HERE, _ATTACK_LODO_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import assemble as asm  # noqa: E402
import detectors  # noqa: E402  # attack-type-lodo detectors
import e8_reference  # noqa: E402
import falsify_dialect_lodo as fdl  # noqa: E402
import folds_dialect as fd  # noqa: E402
import metrics  # noqa: E402

RESULTS_DIR = _HERE / "B2_3_results"
DEFAULT_SEEDS: tuple[int, ...] = (0, 1, 2)
CONDITIONS: tuple[str, ...] = ("natural", "dialect_balanced")
_PRED_COLUMNS = ("text", "label", "dialect", "cluster_id", "y_score")


# --------------------------------------------------------------------------------------
# Frozen-embedding cache (reused across seeds; the carve is the only seed-dependent step)
# --------------------------------------------------------------------------------------
class _CachedFrozenEmbedder:
    """ModernBERT-base mean-pooled frozen embedder with a per-text cache.

    Wraps :class:`detectors.FrozenProbe`'s embed path so the (expensive) GPU forward pass for a
    text runs **once** across all seeds/conditions. The LogisticRegression head is still re-fit per
    fold/seed on the cached vectors, so model-selection on val is unchanged.
    """

    def __init__(self, *, batch_size: int = 16) -> None:
        self._probe = detectors.FrozenProbe(batch_size=batch_size)
        self._cache: dict[str, np.ndarray] = {}

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        """Return mean-pooled embeddings for ``texts`` (cache miss → GPU forward; hit → reuse)."""
        texts = [str(t) for t in texts]
        missing = [t for t in texts if t not in self._cache]
        if missing:
            uniq = list(dict.fromkeys(missing))
            vecs = self._probe._embed(uniq)  # noqa: SLF001 — intentional reuse of the embed path
            for t, v in zip(uniq, vecs, strict=True):
                self._cache[t] = v
        return np.vstack([self._cache[t] for t in texts])


def _fit_score_tfidf(fold: fd.Fold, *, seed: int) -> tuple[np.ndarray, float, dict[str, object]]:
    """Fit the tfidf rung on a fold and return (test_scores, val_roc_auc, recipe)."""
    det = detectors.make_detector("tfidf", seed=seed)
    recipe = det.fit(
        fold.train["text"].tolist(),
        fold.train["label"].tolist(),
        fold.val["text"].tolist(),
        fold.val["label"].tolist(),
    )
    val_scores = det.predict_proba(fold.val["text"].tolist())
    val_roc = metrics.roc_auc_point(fold.val["label"].tolist(), val_scores)
    test_scores = np.asarray(det.predict_proba(fold.test["text"].tolist()), dtype=float)
    return test_scores, val_roc, recipe


def _fit_score_frozen(
    fold: fd.Fold, embedder: _CachedFrozenEmbedder, *, seed: int
) -> tuple[np.ndarray, float, dict[str, object]]:
    """Fit the frozen rung (cached embeddings + LR head); return (test_scores, val_roc, recipe)."""
    from sklearn.linear_model import LogisticRegression

    x_tr = embedder.embed(fold.train["text"].tolist())
    x_val = embedder.embed(fold.val["text"].tolist())
    x_test = embedder.embed(fold.test["text"].tolist())
    best: tuple[float, float, LogisticRegression] | None = None
    for c in (0.1, 1.0, 10.0):
        clf = LogisticRegression(C=c, class_weight="balanced", max_iter=2000, random_state=seed)
        clf.fit(x_tr, fold.train["label"].tolist())
        score = detectors._val_pr_auc(  # noqa: SLF001 — reuse the selection metric
            fold.val["label"].tolist(), clf.predict_proba(x_val)[:, 1]
        )
        if best is None or score > best[0]:
            best = (score, c, clf)
    assert best is not None
    clf = best[2]
    val_scores = clf.predict_proba(x_val)[:, 1]
    val_roc = metrics.roc_auc_point(fold.val["label"].tolist(), val_scores)
    test_scores = np.asarray(clf.predict_proba(x_test)[:, 1], dtype=float)
    return test_scores, val_roc, {"C": best[1], "val_pr_auc": best[0]}


def _dialect_balance(frame: pd.DataFrame, held_out: str, *, seed: int) -> pd.DataFrame:
    """Down-sample each *train* dialect to the smallest train-dialect's row count (seeded).

    The held-out dialect's rows are left intact (they are the test set, not balanced). criteria
    Rev 2 (c) dialect-balanced condition.
    """
    train_dialects = [d for d in frame["dialect"].unique() if d != held_out]
    sizes = {d: int((frame["dialect"] == d).sum()) for d in train_dialects}
    n_min = min(sizes.values())
    rng = np.random.default_rng(seed)
    kept = [frame[frame["dialect"] == held_out]]
    for d in train_dialects:
        sub = frame[frame["dialect"] == d]
        take = rng.choice(len(sub), size=n_min, replace=False)
        kept.append(sub.iloc[take])
    return pd.concat(kept, ignore_index=True)


def run_condition(
    *,
    condition: str,
    seeds: Sequence[int],
    held_dialects: Sequence[str],
    rungs: Sequence[str],
    contexts_per_attack: int,
    out_dir: Path,
    embedder: _CachedFrozenEmbedder | None,
    variant: fd.Variant = "B-",
) -> None:
    """Run one training-composition condition: persist per-(rung,fold,seed) preds + metrics.

    ``variant="B+"`` (decision 6; B2.4) prepends the Arm-A direct base to each fold's train (via
    ``make_dialect_fold``, now that ``load_direct_base`` is built) for the B+−B− contrast.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    for seed in seeds:
        frame = asm.assemble(contexts_per_attack=contexts_per_attack, seed=seed)
        if condition == "dialect_balanced":
            # balance is per held-out fold (different train dialects each) → done inside the loop
            pass
        for held in held_dialects:
            fold_frame = (
                _dialect_balance(frame, held, seed=seed)
                if condition == "dialect_balanced"
                else frame
            )
            fold = fd.make_dialect_fold(fold_frame, held, variant=variant, seed=seed, val_frac=0.2)
            fold_name = f"dialect_lodo_{held}"
            fold_dir = out_dir / f"seed={seed}" / fold_name
            fold_dir.mkdir(parents=True, exist_ok=True)
            for rung in rungs:
                if rung == "tfidf":
                    test_scores, val_roc, recipe = _fit_score_tfidf(fold, seed=seed)
                elif rung == "frozen":
                    assert embedder is not None
                    test_scores, val_roc, recipe = _fit_score_frozen(fold, embedder, seed=seed)
                else:
                    raise ValueError(f"B2.3 is cheap-rung only; got rung {rung!r}")
                headline = metrics.compute_fold_metrics(
                    fold.test["label"].tolist(), test_scores, n_bootstrap=0, seed=seed
                )
                record: dict[str, object] = {
                    "rung": rung,
                    "fold": fold_name,
                    "condition": condition,
                    "variant": variant,
                    "seed": seed,
                    "val_roc_auc": val_roc,
                    "recipe": recipe,
                    "headline": headline,
                    "n_train": int(len(fold.train)),
                    "n_val": int(len(fold.val)),
                    "n_test": int(len(fold.test)),
                }
                preds = fold.test.loc[:, [c for c in _PRED_COLUMNS if c != "y_score"]].copy()
                preds["y_score"] = test_scores
                preds.to_parquet(fold_dir / f"{rung}.predictions.parquet", index=False)
                write_json_strict(record, fold_dir / f"{rung}.metrics.json")
                test_roc = metrics.roc_auc_point(fold.test["label"].tolist(), test_scores)
                print(
                    f"[{condition} seed={seed} {fold_name} {rung}] "
                    f"val_roc={val_roc:.3f} test_roc={test_roc:.3f} "
                    f"n_train={len(fold.train)} n_test={len(fold.test)}"
                )


def _build_e8_tests(
    *, held_dialects: Sequence[str], contexts_per_attack: int, seed: int
) -> dict[str, pd.DataFrame]:
    """Build the held-out-dialect test frames for the E8 column (seed-0 representative)."""
    frame = asm.assemble(contexts_per_attack=contexts_per_attack, seed=seed)
    return {
        held: fd.make_dialect_fold(frame, held, variant="B-", seed=seed, val_frac=0.2).test
        for held in held_dialects
    }


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: smoke or full B2.3 sweep → directional table + E8 column → summary.json."""
    p = argparse.ArgumentParser(description="B2.3 Arm-B B− cheap-rung directional read.")
    p.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    p.add_argument(
        "--dialects", nargs="+", default=list(fd.LODO_DIALECTS), choices=fd.LODO_DIALECTS
    )
    p.add_argument("--conditions", nargs="+", default=list(CONDITIONS), choices=CONDITIONS)
    p.add_argument("--rungs", nargs="+", default=["tfidf", "frozen"], choices=["tfidf", "frozen"])
    p.add_argument("--contexts-per-attack", type=int, default=12)
    p.add_argument(
        "--variant",
        choices=["B-", "B+"],
        default="B-",
        help="B+ (decision 6, B2.4) prepends the Arm-A direct base for the B+−B− contrast",
    )
    p.add_argument("--out", type=Path, default=RESULTS_DIR)
    p.add_argument("--n-boot", type=int, default=fdl._N_BOOT)
    p.add_argument("--n-perm", type=int, default=fdl._N_PERM)
    p.add_argument("--frozen-batch-size", type=int, default=16)
    p.add_argument("--skip-e8", action="store_true", help="skip the E8 reference column")
    p.add_argument(
        "--smoke",
        action="store_true",
        help="1 dialect (bipia) × tfidf × 1 seed × natural — pipeline validation",
    )
    args = p.parse_args(argv)

    if args.smoke:
        args.seeds = [0]
        args.dialects = ["bipia"]
        args.conditions = ["natural"]
        args.rungs = ["tfidf"]
        args.skip_e8 = True

    # B+ (decision 6): natural-mix only; sibling results dir so it never overwrites B−.
    if args.variant == "B+":
        if args.conditions == list(CONDITIONS):
            args.conditions = ["natural"]
        if args.out == RESULTS_DIR:
            args.out = RESULTS_DIR.parent / "B2_3_results_Bplus"

    embedder = (
        _CachedFrozenEmbedder(batch_size=args.frozen_batch_size) if "frozen" in args.rungs else None
    )

    folds = [f"dialect_lodo_{d}" for d in args.dialects]
    summary: dict[str, Any] = {
        "study": f"cross-family-transfer B2.3 (Arm-B {args.variant} cheap-rung directional read)",
        "criteria": "experiments/cross-family-transfer/criteria.md (Rev 1/2; B+ per Rev 3/4)",
        "note": (
            "Directional only — NO verdict (lora-gated at B3). Primary = natural-mix (Rev 2 (c)). "
            "B+ = +Arm-A direct base; compare to B− for the B+−B− direct-data-bridging contrast."
        ),
        "variant": args.variant,
        "seeds": list(args.seeds),
        "dialects": list(args.dialects),
        "conditions": list(args.conditions),
        "rungs": list(args.rungs),
        "directional_table": {},
    }

    for condition in args.conditions:
        cond_dir = args.out / condition
        run_condition(
            condition=condition,
            seeds=args.seeds,
            held_dialects=args.dialects,
            rungs=args.rungs,
            contexts_per_attack=args.contexts_per_attack,
            out_dir=cond_dir,
            embedder=embedder,
            variant=args.variant,
        )
        table = fdl.directional_table(
            cond_dir, folds, rungs=args.rungs, n_boot=args.n_boot, n_perm=args.n_perm
        )
        summary["directional_table"][condition] = table

    if not args.skip_e8:
        e8_tests = _build_e8_tests(
            held_dialects=args.dialects, contexts_per_attack=args.contexts_per_attack, seed=0
        )
        summary["e8_reference"] = e8_reference.score_all_dialects(e8_tests, seed=0)

    args.out.mkdir(parents=True, exist_ok=True)
    write_json_strict(summary, args.out / "summary.json")
    print(f"\nB2.3 done — summary written to {args.out / 'summary.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
