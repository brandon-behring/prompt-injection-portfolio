"""Step-0 diagnostic — does the cluster-blind val carve inflate ``Gx = val_roc - test_roc``?

The B2.3 in-distribution val carve is **row-level** (``carve_val_from_train`` else-branch with
``min_types_for_typeholdout=10**9``); ``cluster_id`` is never passed. Fujitsu's paired
poison/benign (same ``cluster_id``) and bipia's 12-context payload expansion can therefore straddle
inner-train/val → an optimistic, fold-composition-dependent ``val_roc`` reference. The held-out
**test** ROC is unaffected (cluster-disjoint; leakage gate = 0) — only the ``Gx`` magnitude + the
cross-rung shrinkage story are at risk.

This script measures the effect at the cheap tfidf rung (CPU). For each LODO fold it refits tfidf
with val carved **two ways** on the same B− train pool and held-out test:

* (a) **row carve** = the production ``make_dialect_fold`` (row-level label-stratified holdout);
* (b) **cluster-aware carve** = hold out whole ``cluster_id``s (``GroupShuffleSplit`` on the group),
  so no cluster straddles inner-train/val.

Emits ``{dialect: val_roc_row, val_roc_cluster, dval, test_roc_row, test_roc_cluster, gx_row,
gx_cluster}`` (seed-mean) plus the **pre-stated decision verdict** (criteria write-gate):

* ``dval = val_roc_row - val_roc_cluster < 0.03`` on BOTH well-powered folds (browsesafe, fujitsu)
  AND no dialect's ``Gx`` flips sign or crosses the 0.05 SESOI  →  **ROW CARVE STANDS** (proceed);
* else  →  **SWITCH** to the cluster-aware carve (criteria Revision 3), re-run tfidf, then frozen.

CPU only; no GPU. Run::

    uv run python experiments/cross-family-transfer/val_carve_sensitivity.py
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
from sklearn.model_selection import GroupShuffleSplit

_HERE = Path(__file__).resolve().parent
_ATTACK_LODO_DIR = _HERE.parent / "attack-type-lodo"
for _p in (_HERE, _ATTACK_LODO_DIR):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import assemble as asm  # noqa: E402
import detectors  # noqa: E402
import folds_dialect as fd  # noqa: E402
import metrics  # noqa: E402

WELL_POWERED: tuple[str, ...] = ("browsesafe", "fujitsu")
_DVAL_THRESHOLD = 0.03  # pre-stated (criteria write-gate); material inflation if exceeded
_SESOI = 0.05  # pre-registered SESOI floor (criteria Rev 1 §decision rule)


def _fit_tfidf_val_test(
    inner: pd.DataFrame, val: pd.DataFrame, test: pd.DataFrame, *, seed: int
) -> tuple[float, float]:
    """Fit tfidf on ``inner`` (val drives C selection); return (val_roc, test_roc)."""
    det = detectors.make_detector("tfidf", seed=seed)
    det.fit(
        inner["text"].tolist(), inner["label"].tolist(), val["text"].tolist(), val["label"].tolist()
    )
    val_roc = metrics.roc_auc_point(val["label"].tolist(), det.predict_proba(val["text"].tolist()))
    test_roc = metrics.roc_auc_point(
        test["label"].tolist(), det.predict_proba(test["text"].tolist())
    )
    return float(val_roc), float(test_roc)


def _cluster_aware_carve(
    train_full: pd.DataFrame, *, seed: int, val_frac: float = 0.2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Hold out whole ``cluster_id`` groups into val (GroupShuffleSplit); both classes required."""
    gss = GroupShuffleSplit(n_splits=1, test_size=val_frac, random_state=seed)
    inner_idx, val_idx = next(
        gss.split(train_full, train_full["label"], groups=train_full["cluster_id"])
    )
    inner = train_full.iloc[inner_idx].reset_index(drop=True)
    val = train_full.iloc[val_idx].reset_index(drop=True)
    for name, split in (("inner", inner), ("val", val)):
        if set(split["label"].unique().tolist()) != {0, 1}:
            raise ValueError(f"cluster-aware {name} split is single-class (seed={seed})")
    return inner, val


def _one_fold(frame: pd.DataFrame, held: str, *, seed: int) -> dict[str, float]:
    """Both carve arms for one held-out dialect at one seed."""
    # (a) row carve = exact production path.
    fold = fd.make_dialect_fold(frame, held, variant="B-", seed=seed, val_frac=0.2)
    val_roc_row, test_roc_row = _fit_tfidf_val_test(fold.train, fold.val, fold.test, seed=seed)

    # (b) cluster-aware carve on the same B- train pool + same held-out test.
    train_full, test = fd._dialect_lodo_builder(held)(frame)  # noqa: SLF001 — intentional reuse
    inner_clu, val_clu = _cluster_aware_carve(train_full, seed=seed)
    val_roc_clu, test_roc_clu = _fit_tfidf_val_test(inner_clu, val_clu, test, seed=seed)

    return {
        "val_roc_row": val_roc_row,
        "test_roc_row": test_roc_row,
        "gx_row": val_roc_row - test_roc_row,
        "val_roc_cluster": val_roc_clu,
        "test_roc_cluster": test_roc_clu,
        "gx_cluster": val_roc_clu - test_roc_clu,
        "dval": val_roc_row - val_roc_clu,
    }


def _mean_over_seeds(per_seed: list[dict[str, float]]) -> dict[str, float]:
    """Mean each metric over seeds."""
    keys = per_seed[0].keys()
    return {k: float(np.mean([d[k] for d in per_seed])) for k in keys}


def _verdict(table: dict[str, dict[str, float]]) -> dict[str, Any]:
    """Apply the pre-stated rule → ROW-CARVE-STANDS vs SWITCH, with the triggering reasons."""
    reasons: list[str] = []
    for d in WELL_POWERED:
        if d in table and table[d]["dval"] >= _DVAL_THRESHOLD:
            reasons.append(f"dval[{d}]={table[d]['dval']:+.3f} >= {_DVAL_THRESHOLD}")
    for d, row in table.items():
        if np.sign(row["gx_row"]) != np.sign(row["gx_cluster"]):
            reasons.append(
                f"Gx sign flip [{d}]: row={row['gx_row']:+.3f} cluster={row['gx_cluster']:+.3f}"
            )
        if (row["gx_row"] >= _SESOI) != (row["gx_cluster"] >= _SESOI):
            reasons.append(
                f"Gx SESOI flip [{d}]: row={row['gx_row']:+.3f} cluster={row['gx_cluster']:+.3f}"
            )
    material = bool(reasons)
    return {
        "material": material,
        "decision": "SWITCH to cluster-aware carve (criteria Revision 3)"
        if material
        else "ROW CARVE STANDS — proceed to frozen on existing folds",
        "reasons": reasons,
        "rule": (
            f"material iff dval >= {_DVAL_THRESHOLD} on a well-powered fold "
            f"({'/'.join(WELL_POWERED)}) OR any Gx sign/SESOI({_SESOI}) flip"
        ),
    }


def main(argv: Sequence[str] | None = None) -> int:
    """CLI: run the tfidf val-carve sensitivity diagnostic → table + pre-stated verdict."""
    p = argparse.ArgumentParser(description="Step-0 val-carve sensitivity (tfidf, CPU).")
    p.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    p.add_argument(
        "--dialects", nargs="+", default=list(fd.LODO_DIALECTS), choices=fd.LODO_DIALECTS
    )
    p.add_argument("--contexts-per-attack", type=int, default=12)
    p.add_argument("--out", type=Path, default=_HERE / "val_carve_sensitivity.json")
    args = p.parse_args(argv)

    frames = {
        s: asm.assemble(contexts_per_attack=args.contexts_per_attack, seed=s) for s in args.seeds
    }

    table: dict[str, dict[str, float]] = {}
    for held in args.dialects:
        per_seed = [_one_fold(frames[s], held, seed=s) for s in args.seeds]
        table[held] = _mean_over_seeds(per_seed)
        r = table[held]
        print(
            f"[{held:11s}] val_row={r['val_roc_row']:.3f} val_clu={r['val_roc_cluster']:.3f} "
            f"dval={r['dval']:+.3f} | test={r['test_roc_row']:.3f} | "
            f"Gx_row={r['gx_row']:+.3f} Gx_clu={r['gx_cluster']:+.3f}"
        )

    verdict = _verdict(table)
    out = {
        "study": "B2.3 Step-0 val-carve sensitivity (tfidf, CPU)",
        "threshold_dval": _DVAL_THRESHOLD,
        "sesoi": _SESOI,
        "well_powered_folds": list(WELL_POWERED),
        "seeds": list(args.seeds),
        "table": table,
        "verdict": verdict,
    }
    write_json_strict(out, args.out)
    print(f"\nVERDICT: {verdict['decision']}")
    if verdict["reasons"]:
        for reason in verdict["reasons"]:
            print(f"  - {reason}")
    print(f"\nwritten → {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
