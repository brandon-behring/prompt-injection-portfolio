"""Carrier-LODO ROC-AUC generalization-gap estimator — carrier-lodo/criteria.md Revision 1.

Tests whether the carrier-LODO gap ``G(rung) = mean over held-out carriers of
[val_roc_auc − test_roc_auc(held-out carrier)]`` **persists** as capacity rises (the carrier wall
is capacity-resistant → the ADR-055 multi-axis spine is validated as a modeling result) or
**collapses** toward 0 at the ``lora`` rung (capacity dissolves the carrier axis too → the spine is
revised), mirroring the attack-type §6.5 result.

ROC-AUC basis (not AUPRC): the BIPIA carriers are 83–94 % positive, so an AUPRC val→test gap is
prevalence-confounded (criteria.md Revision 1, motivated by ``../AUDIT_2026-06/``). ROC-AUC is
prevalence-invariant. The held-out **carrier** is the LODO unit (n=3); the **payload** is the
within-carrier bootstrap unit (never row-level), as ``../eda/OOD_WALL_PREDICTION/criteria.md``
Rev 1. ``val_roc_auc`` is read from the harness ``metrics.json`` (the predictions parquet holds only
test rows) and held fixed in the bootstrap.

Decision (UNCHANGED logic, ROC basis): with ``G(rung)`` = mean over the 3 held-out carriers,

* SURVIVES iff ``G(lora) > 0`` AND one-sided 95 % bootstrap ``CI-low(G(lora)) > 0`` AND
  ``G(lora) ≥ ½·G(frozen)``;
* FALSIFIED iff ``CI-low(G(lora)) ≤ 0``;
* else SMALL-THROUGHOUT.

Reads ``predictions.parquet`` (test scores) + ``metrics.json`` (``val_roc_auc``). ``main()`` writes
nothing — the write-gate lives in the caller, like ``falsify_clustered`` / ``falsify_ood_wall``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import rankdata  # type: ignore[import-untyped]

_HERE = Path(__file__).resolve().parent
_N_BOOT = 10_000
RUNGS: tuple[str, ...] = ("tfidf", "frozen", "lora")

if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import folds  # noqa: E402  # sibling module (hyphenated dir → sys.path inject, harness pattern)
import metrics  # noqa: E402

_SeedFloat = dict[int, float]


def _recover_payload(text: pd.Series) -> pd.Series:
    """Payload = the injected attack string = last ``\\n\\n``-delimited segment."""
    return text.str.rsplit("\n\n", n=1).str[-1]


def _roc_auc_fast(y: np.ndarray, s: np.ndarray) -> float:
    """Tie-corrected AUROC via the Mann-Whitney rank-sum (the fast bootstrap inner loop).

    Equivalent to ``sklearn.roc_auc_score`` including ties (average ranks). Used only inside the
    ≥10 000-iter bootstrap; the *point* estimate uses ``eval_toolkit`` (:func:`_point_test_roc`).
    """
    n_pos = int((y == 1).sum())
    n_neg = int((y == 0).sum())
    if n_pos == 0 or n_neg == 0:
        return float("nan")
    ranks = np.asarray(rankdata(s), dtype=float)
    sum_pos = float(ranks[y == 1].sum())
    return (sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


@dataclass(frozen=True)
class CarrierFold:
    """Per-seed test payload clusters, negatives, and ``val_roc`` for one (carrier, rung)."""

    payload_pos: dict[int, list[np.ndarray]]
    neg: dict[int, np.ndarray]
    val_roc: _SeedFloat
    seeds: list[int]


def load_carrier_fold(results_dir: Path, fold_name: str, rung: str) -> CarrierFold:
    """Build the per-seed cluster structure for one carrier-LODO fold + rung from on-disk artifacts.

    Reads each seed's ``predictions.parquet`` (positives grouped by recovered payload; negatives
    pooled) and its sibling ``metrics.json`` for ``val_roc_auc`` (held fixed in the bootstrap).
    """
    paths = sorted(results_dir.glob(f"seed=*/{fold_name}/{rung}.predictions.parquet"))
    if not paths:
        raise FileNotFoundError(f"no {rung} predictions for {fold_name} under {results_dir}")
    payload_pos: dict[int, list[np.ndarray]] = {}
    neg: dict[int, np.ndarray] = {}
    val_roc: _SeedFloat = {}
    seeds: list[int] = []
    for p in paths:
        seed = int(p.parent.parent.name.split("=")[1])
        seeds.append(seed)
        df = pd.read_parquet(p)
        neg[seed] = df.loc[df["label"] == 0, "y_score"].to_numpy(dtype=float)
        pdf = df.loc[df["label"] == 1].copy()
        pdf["payload"] = _recover_payload(pdf["text"])
        payload_pos[seed] = [
            grp["y_score"].to_numpy(dtype=float) for _, grp in pdf.groupby("payload")
        ]
        meta_path = p.with_name(f"{rung}.metrics.json")
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        if meta.get("val_roc_auc") is None:
            raise KeyError(
                f"{meta_path} lacks val_roc_auc — re-run the harness (run_one persists it per "
                "carrier-lodo/criteria.md Rev 1)"
            )
        val_roc[seed] = float(meta["val_roc_auc"])
    return CarrierFold(payload_pos, neg, val_roc, sorted(seeds))


def _point_test_roc(fold: CarrierFold, seed: int) -> float:
    """Pooled test ROC-AUC for one seed via ``eval_toolkit`` (comparable to the headline)."""
    pos = np.concatenate(fold.payload_pos[seed])
    ns = fold.neg[seed]
    y = np.concatenate([np.ones(pos.size), np.zeros(ns.size)])
    s = np.concatenate([pos, ns])
    return metrics.roc_auc_point(y, s)


def _resampled_test_roc(fold: CarrierFold, seed: int, rng: np.random.Generator) -> float:
    """One payload-cluster bootstrap draw of the test ROC-AUC (negatives held fixed)."""
    payloads = fold.payload_pos[seed]
    n = len(payloads)
    idx = rng.integers(0, n, size=n)
    pos = np.concatenate([payloads[int(i)] for i in idx])
    ns = fold.neg[seed]
    y = np.concatenate([np.ones(pos.size), np.zeros(ns.size)])
    s = np.concatenate([pos, ns])
    return _roc_auc_fast(y, s)


def _rung_gap(
    fold_data: dict[str, CarrierFold], *, n_boot: int, rng: np.random.Generator
) -> dict[str, Any]:
    """Point + bootstrap of ``G(rung)`` = mean over carriers of (val_roc − test_roc) per seed.

    The cross-carrier mean and its one-sided 95 % CI-low come from resampling every carrier's
    payloads per iteration and averaging the per-carrier gaps (held-out carrier = LODO unit, n=3).
    """
    val_roc_mean: dict[str, float] = {}
    test_roc_point: dict[str, float] = {}
    per_carrier_g: dict[str, float] = {}
    for fold_name, d in fold_data.items():
        vr = float(np.mean([d.val_roc[s] for s in d.seeds]))
        tr = float(np.mean([_point_test_roc(d, s) for s in d.seeds]))
        val_roc_mean[fold_name] = vr
        test_roc_point[fold_name] = tr
        per_carrier_g[fold_name] = vr - tr
    g_point = float(np.mean(list(per_carrier_g.values())))

    g_boot = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        per_carrier_b: list[float] = []
        for fold_name, d in fold_data.items():
            tr_b = float(np.mean([_resampled_test_roc(d, s, rng) for s in d.seeds]))
            per_carrier_b.append(val_roc_mean[fold_name] - tr_b)
        g_boot[b] = float(np.mean(per_carrier_b))
    return {
        "G": g_point,
        "ci_low": float(np.percentile(g_boot, 5.0)),
        "frac_gt0": float(np.mean(g_boot > 0.0)),
        "per_carrier_G": per_carrier_g,
        "val_roc_mean": val_roc_mean,
        "test_roc_point": test_roc_point,
    }


def compute_verdict(results_dir: Path, *, n_boot: int = _N_BOOT, seed: int = 0) -> dict[str, Any]:
    """Carrier-LODO ROC-AUC persistence-vs-collapse verdict (no write); criteria.md Rev 1 logic."""
    rng = np.random.default_rng(seed)
    rungs: dict[str, Any] = {}
    for rung in RUNGS:
        fold_data = {
            fold_name: load_carrier_fold(results_dir, fold_name, rung)
            for fold_name in folds.CARRIER_LODO_FOLDS
        }
        rungs[rung] = _rung_gap(fold_data, n_boot=n_boot, rng=rng)

    g_lora = float(rungs["lora"]["G"])
    ci_lora = float(rungs["lora"]["ci_low"])
    g_frozen = float(rungs["frozen"]["G"])
    if ci_lora <= 0.0:
        verdict = "FALSIFIED"
    elif g_lora > 0.0 and g_lora >= 0.5 * g_frozen:  # ci_lora > 0 guaranteed here
        verdict = "SURVIVES"
    else:
        verdict = "SMALL-THROUGHOUT"
    return {
        "decision_rule": (
            "SURVIVES iff G(lora)>0 AND bootstrap CI-low(G(lora))>0 AND G(lora)>=0.5*G(frozen); "
            "FALSIFIED iff CI-low(G(lora))<=0; else SMALL-THROUGHOUT"
        ),
        "estimator": (
            "carrier-LODO ROC-AUC gap, payload-clustered within carrier (criteria.md Revision 1)"
        ),
        "metric": "roc_auc (prevalence-invariant)",
        "verdict": verdict,
        "G_by_rung": {r: float(rungs[r]["G"]) for r in RUNGS},
        "ci_low_by_rung": {r: float(rungs[r]["ci_low"]) for r in RUNGS},
        "lora": {"G": g_lora, "ci_low": ci_lora, "half_G_frozen": 0.5 * g_frozen},
        "n_boot": n_boot,
        "carriers": list(folds.CARRIER_LODO_FOLDS),
        "per_rung": rungs,
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Compute + print the carrier-LODO ROC-AUC persistence read. Writes nothing (rehearsal)."""
    ap = argparse.ArgumentParser(
        description="Carrier-LODO ROC-AUC persistence verdict (criteria.md Rev 1)."
    )
    ap.add_argument("--results-dir", type=Path, required=True)
    ap.add_argument("--n-boot", type=int, default=_N_BOOT)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)
    v = compute_verdict(args.results_dir, n_boot=args.n_boot, seed=args.seed)
    print("\n=== CARRIER-LODO ROC-AUC gap (payload-clustered within carrier) ===")
    for r in RUNGS:
        pr = v["per_rung"][r]
        pc = {
            k.replace("carrier_lodo_", ""): round(float(g), 3)
            for k, g in pr["per_carrier_G"].items()
        }
        print(
            f"{r:6s} G={pr['G']:+.4f}  ci_low(5%)={pr['ci_low']:+.4f}  "
            f"frac(G*>0)={pr['frac_gt0']:.3f}  per-carrier={pc}"
        )
    print(
        f"\nG(lora)={v['lora']['G']:+.4f}  CI-low={v['lora']['ci_low']:+.4f}  "
        f"0.5*G(frozen)={v['lora']['half_G_frozen']:+.4f}"
    )
    print(f"-> VERDICT: {v['verdict']}")
    print("(rehearsal — nothing written)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
