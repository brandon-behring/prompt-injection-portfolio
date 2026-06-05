"""B3 — cross-family-transfer ``lora`` rung trainer (the paid-GPU rung; B4 verdict input).

The train-ONLY orchestrator for the LoRA rung across **both arms**, the third and final rung of the
cross-family ladder (``criteria.md`` Rev 3/4, B3). The cheap rungs (tfidf + frozen) already ran
locally (B2.3/B2.4); this module adds *only* the ``lora`` rung, which trains on a paid GPU pod
(``runpod_crossfamily_sweep.yaml``). It is the schema-faithful sibling of ``run_b2_3.py`` (Arm B) +
``run_b2_4.py`` (Arm A): it **reuses their fold builders unchanged** and **imports the LoRA recipe**
(``detectors.make_detector("lora")``, ModernBERT-base, ``r_grid=(8,16)``; ADR-026, no
reimplementation), so the lora predictions parquet is byte-for-byte schema-identical to the frozen
sibling sitting next to it — and ``falsify_dialect_lodo`` + ``b4_verdict`` ingest it with **zero
scorer changes**.

It does **train only** — no frozen embedder, no E8, no bootstrap, no verdict (those stay local; the
SURVIVES/FALSIFIED/SMALL-THROUGHOUT verdict is computed by ``b4_verdict`` on the merged tree). The
matrix (criteria.md:240, "~27 training runs"): Arm A (1 pooled fold × 3 seeds) + Arm B B− (4
dialects × 3) + Arm B B+ (4 × 3) = 27, each a LoRA fit over ``r_grid=(8,16)``.

Output layout mirrors the cheap-rung trees **as subpaths under ``--out``** so the local post-pull
merge (:func:`merge_into_cheap_trees`) is a literal subpath copy of the ``lora.*`` files:

* Arm A      → ``<out>/B2_4_results/capped/seed=*/arm_a_pooled/lora.*``
* Arm B B−   → ``<out>/B2_3_results/natural/seed=*/dialect_lodo_*/lora.*``
* Arm B B+   → ``<out>/B2_3_results_Bplus/natural/seed=*/dialect_lodo_*/lora.*``

Run on the pod (cheapest-robust-first ordering — Arm A + B− land scorable even if B+ times out)::

    uv run python experiments/cross-family-transfer/run_b3_lora.py --arm A          --seeds 0 1 2 --out experiments/cross-family-transfer/B3_lora
    uv run python experiments/cross-family-transfer/run_b3_lora.py --arm B --variant B- --seeds 0 1 2 --out experiments/cross-family-transfer/B3_lora
    uv run python experiments/cross-family-transfer/run_b3_lora.py --arm B --variant B+ --seeds 0 1 2 --out experiments/cross-family-transfer/B3_lora

Local free smoke (1 dialect × 1 seed × r=8) — confirms the lora≡frozen schema before any spend::

    uv run python experiments/cross-family-transfer/run_b3_lora.py --arm B --variant B- --smoke --out /tmp/b3_smoke

Local post-pull merge (held; after the paid sweep is pulled to ``B3_results_runpod_lora/``)::

    uv run python experiments/cross-family-transfer/run_b3_lora.py --merge experiments/cross-family-transfer/B3_results_runpod_lora
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
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
import assemble_arm_a as aa  # noqa: E402
import detectors  # noqa: E402  # attack-type-lodo detectors (the imported LoRA recipe)
import folds_dialect as fd  # noqa: E402
import metrics  # noqa: E402
import run_b2_4 as b24  # noqa: E402  # reuse _build_fold + _over_defense + FOLD_NAME (Arm A)
from run_b2_3 import _PRED_COLUMNS  # noqa: E402  # Arm-B prediction schema (single source of truth)

RUNG = "lora"
DEFAULT_SEEDS: tuple[int, ...] = (0, 1, 2)
DEFAULT_RANKS: tuple[int, ...] = (8, 16)  # the pre-registered grid (criteria.md:115; == M1/carrier)
RESULTS_DIR = _HERE / "B3_lora"
CONTEXTS_PER_ATTACK = 12  # == run_b2_3 (criteria Rev 1)

# Output subpaths mirror the cheap-rung trees so :func:`merge_into_cheap_trees` is a literal copy.
_ARM_A_SUBPATH: tuple[str, ...] = ("B2_4_results", "capped")
_ARM_B_SUBPATH: dict[str, tuple[str, ...]] = {
    "B-": ("B2_3_results", "natural"),
    "B+": ("B2_3_results_Bplus", "natural"),
}


def _make_lora(*, seed: int, ranks: Sequence[int]) -> detectors.Detector:
    """The imported LoRA recipe with the (pre-registered) rank grid (ADR-026 — no reimplementation)."""
    return detectors.make_detector(RUNG, seed=seed, r_grid=tuple(ranks))


def _score_fn(det: detectors.Detector) -> Callable[[Sequence[str]], np.ndarray]:
    """A float-array scorer over the fitted detector (shape used by ``_over_defense``)."""

    def score(texts: Sequence[str]) -> np.ndarray:
        return np.asarray(det.predict_proba(list(texts)), dtype=float)

    return score


def _subsample_balanced(df: pd.DataFrame, n: int | None, *, seed: int) -> pd.DataFrame:
    """Up-to-``n`` rows, ~balanced by label (``--smoke`` only — a fast plumbing/schema check).

    Keeps both classes (the val/test ROC + ``_val_pr_auc`` need 2-class splits). A no-op when ``n``
    is ``None`` or the frame already fits. Never used on a paid run.
    """
    if n is None or len(df) <= n:
        return df
    rng = np.random.default_rng(seed)
    per = max(1, n // 2)
    parts = [
        sub.iloc[rng.choice(len(sub), size=min(per, len(sub)), replace=False)]
        for lab in (0, 1)
        if len(sub := df[df["label"] == lab])
    ]
    out = pd.concat(parts, ignore_index=True) if parts else df
    return out.sample(frac=1.0, random_state=seed).reset_index(drop=True)


def run_arm_a(
    *, seeds: Sequence[int], ranks: Sequence[int], out: Path, notinject: pd.DataFrame
) -> None:
    """Arm A (direct→indirect): one pooled fold × seeds; lora preds + over-defense (mirrors run_b2_4)."""
    base = out.joinpath(*_ARM_A_SUBPATH)
    for seed in seeds:
        fold = b24._build_fold(cap=aa.CAP, seed=seed)  # noqa: SLF001 — reuse the Arm-A fold builder
        det = _make_lora(seed=seed, ranks=ranks)
        recipe = det.fit(
            fold.train["text"].tolist(),
            fold.train["label"].tolist(),
            fold.val["text"].tolist(),
            fold.val["label"].tolist(),
        )
        score = _score_fn(det)
        val_scores = score(fold.val["text"].tolist())
        test_scores = score(fold.test["text"].tolist())
        val_roc = metrics.roc_auc_point(fold.val["label"].tolist(), val_scores)
        test_roc = metrics.roc_auc_point(fold.test["label"].tolist(), test_scores)

        fold_dir = base / f"seed={seed}" / b24.FOLD_NAME
        fold_dir.mkdir(parents=True, exist_ok=True)
        preds = fold.test.loc[:, ["cluster_id", "label", "slice"]].copy()
        preds["y_score"] = test_scores
        preds.to_parquet(fold_dir / f"{RUNG}.predictions.parquet", index=False)

        # Over-defense (Arm-A only; mirrors run_b2_4): NotInject FPR at a val-fixed low-FPR threshold.
        over = b24._over_defense(fold, {"val_scores": val_scores, "score_fn": score}, notinject)  # noqa: SLF001
        ni_cols = [c for c in ("text", "label") if c in notinject.columns]
        ni = notinject.loc[:, ni_cols].copy()
        ni["y_score"] = score(notinject["text"].tolist())
        ni.to_parquet(fold_dir / f"{RUNG}.notinject.predictions.parquet", index=False)

        record: dict[str, Any] = {
            "rung": RUNG,
            "pool": "capped",
            "fold": b24.FOLD_NAME,
            "seed": seed,
            "val_roc_auc": float(val_roc),
            "test_roc_auc": float(test_roc),
            "recipe": recipe,
            "over_defense": over,
            "n_train": int(len(fold.train)),
            "n_val": int(len(fold.val)),
            "n_test": int(len(fold.test)),
        }
        write_json_strict(record, fold_dir / f"{RUNG}.metrics.json")
        print(
            f"[armA capped seed={seed} lora] val_roc={val_roc:.3f} test_roc={test_roc:.3f} "
            f"Gx={val_roc - test_roc:+.3f} over_defense_fpr={over['over_defense_fpr']} "
            f"r={recipe.get('r')} n_train={len(fold.train)}"
        )


def run_arm_b(
    *,
    variant: fd.Variant,
    dialects: Sequence[str],
    seeds: Sequence[int],
    ranks: Sequence[int],
    out: Path,
    contexts_per_attack: int = CONTEXTS_PER_ATTACK,
    subsample: int | None = None,
) -> None:
    """Arm B (dialect-LODO): natural-mix only; lora preds per held dialect (mirrors run_b2_3).

    ``subsample`` (``--smoke`` only) caps each split to a small balanced sample for a fast plumbing
    check; it is ``None`` (full pools) on every real run.
    """
    base = out.joinpath(*_ARM_B_SUBPATH[variant])
    for seed in seeds:
        frame = asm.assemble(contexts_per_attack=contexts_per_attack, seed=seed)
        for held in dialects:
            fold = fd.make_dialect_fold(frame, held, variant=variant, seed=seed, val_frac=0.2)
            if subsample is not None:
                fold = fd.Fold(
                    name=fold.name,
                    train=_subsample_balanced(fold.train, subsample, seed=seed),
                    val=_subsample_balanced(fold.val, subsample, seed=seed),
                    test=_subsample_balanced(fold.test, subsample, seed=seed),
                    test_types=fold.test_types,
                )
            fold_name = f"dialect_lodo_{held}"
            det = _make_lora(seed=seed, ranks=ranks)
            recipe = det.fit(
                fold.train["text"].tolist(),
                fold.train["label"].tolist(),
                fold.val["text"].tolist(),
                fold.val["label"].tolist(),
            )
            test_scores = np.asarray(det.predict_proba(fold.test["text"].tolist()), dtype=float)
            val_scores = np.asarray(det.predict_proba(fold.val["text"].tolist()), dtype=float)
            val_roc = metrics.roc_auc_point(fold.val["label"].tolist(), val_scores)
            headline = metrics.compute_fold_metrics(
                fold.test["label"].tolist(), test_scores, n_bootstrap=0, seed=seed
            )

            fold_dir = base / f"seed={seed}" / fold_name
            fold_dir.mkdir(parents=True, exist_ok=True)
            preds = fold.test.loc[:, [c for c in _PRED_COLUMNS if c != "y_score"]].copy()
            preds["y_score"] = test_scores
            preds.to_parquet(fold_dir / f"{RUNG}.predictions.parquet", index=False)
            record: dict[str, Any] = {
                "rung": RUNG,
                "fold": fold_name,
                "condition": "natural",
                "variant": variant,
                "seed": seed,
                "val_roc_auc": float(val_roc),
                "recipe": recipe,
                "headline": headline,
                "n_train": int(len(fold.train)),
                "n_val": int(len(fold.val)),
                "n_test": int(len(fold.test)),
            }
            write_json_strict(record, fold_dir / f"{RUNG}.metrics.json")
            test_roc = metrics.roc_auc_point(fold.test["label"].tolist(), test_scores)
            print(
                f"[armB {variant} seed={seed} {fold_name} lora] "
                f"val_roc={val_roc:.3f} test_roc={test_roc:.3f} Gx={val_roc - test_roc:+.3f} "
                f"r={recipe.get('r')} n_train={len(fold.train)} n_test={len(fold.test)}"
            )


def merge_into_cheap_trees(src_root: Path, *, dst_parent: Path = _HERE) -> list[Path]:
    """Copy ``lora.*`` artifacts from a pulled B3 tree into the cheap-rung trees (local post-pull).

    A safe file-tree union: the ``lora.``-prefixed filenames never collide with the existing
    ``tfidf.*`` / ``frozen.*`` siblings. After this, ``falsify_dialect_lodo.directional_table(...,
    rungs=["tfidf","frozen","lora"])`` + ``b4_verdict.verdict`` run on the merged tree.

    Returns
    -------
    list[pathlib.Path]
        The destination paths written.
    """
    copied: list[Path] = []
    for sub in (_ARM_A_SUBPATH, _ARM_B_SUBPATH["B-"], _ARM_B_SUBPATH["B+"]):
        src = src_root.joinpath(*sub)
        if not src.exists():
            continue
        dst = dst_parent.joinpath(*sub)
        for f in sorted(src.rglob(f"{RUNG}.*")):
            if not f.is_file():
                continue
            target = dst / f.relative_to(src)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f.read_bytes())
            copied.append(target)
    return copied


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: train the lora rung for one arm (pod), run the schema smoke, or merge a pulled tree."""
    p = argparse.ArgumentParser(
        description="B3 cross-family-transfer LoRA rung trainer (train-only)."
    )
    p.add_argument(
        "--arm", choices=["A", "B"], help="A = direct→indirect (Arm A); B = dialect-LODO"
    )
    p.add_argument("--variant", choices=["B-", "B+"], default="B-", help="Arm B train composition")
    p.add_argument(
        "--dialects", nargs="+", default=list(fd.LODO_DIALECTS), choices=fd.LODO_DIALECTS
    )
    p.add_argument("--seeds", type=int, nargs="+", default=list(DEFAULT_SEEDS))
    p.add_argument(
        "--lora-ranks",
        type=int,
        nargs="+",
        default=list(DEFAULT_RANKS),
        help="LoRA rank grid (pre-registered (8,16); --smoke forces (8,) for a fast schema check)",
    )
    p.add_argument("--out", type=Path, default=RESULTS_DIR)
    p.add_argument(
        "--merge",
        type=Path,
        default=None,
        help="LOCAL post-pull: copy lora.* from this pulled B3 tree into the cheap-rung trees, then exit",
    )
    p.add_argument(
        "--smoke",
        action="store_true",
        help="Arm B × bipia × 1 seed × r=8 — free local schema check (lora≡frozen columns)",
    )
    p.add_argument(
        "--smoke-rows",
        type=int,
        default=48,
        help="--smoke balanced per-split row cap (fast plumbing check; ignored without --smoke)",
    )
    args = p.parse_args(argv)

    if args.merge is not None:
        written = merge_into_cheap_trees(args.merge)
        print(f"merged {len(written)} lora.* files from {args.merge} into the cheap-rung trees")
        return 0

    if args.smoke:
        args.arm, args.variant = "B", "B-"
        args.dialects, args.seeds, args.lora_ranks = ["bipia"], [0], [8]

    if args.arm is None:
        p.error("one of --arm {A,B} or --merge is required")

    if args.arm == "A":
        notinject = aa.load_notinject_overdefense()
        run_arm_a(seeds=args.seeds, ranks=args.lora_ranks, out=args.out, notinject=notinject)
    else:
        run_arm_b(
            variant=args.variant,
            dialects=args.dialects,
            seeds=args.seeds,
            ranks=args.lora_ranks,
            out=args.out,
            subsample=args.smoke_rows if args.smoke else None,
        )
    print(
        f"\nB3 lora ({args.arm}{'' if args.arm == 'A' else ' ' + args.variant}) done → {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
