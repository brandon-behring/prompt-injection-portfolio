"""Honest-unit (payload-clustered) §6.5 OOD-wall estimator — criteria.md Revision 1.

The pre-registration's locked uncertainty spec resampled the per-(type, seed) *drop
scalars* / item-level rows, which pseudo-replicates: each test-type's positives are
**5 BIPIA attack strings (payloads) × 12 contexts × 3 carriers = 180 rows**, so the
independent unit is the **payload (n=5/type)**, not the row, and the permutation's
exchangeable unit is the **attack type** (n=k/tail), not the (type×seed) drop. This
module implements the corrected estimator (Revision 1) and is the scientific core the
write-gated `falsify_ood_wall.py` delegates to.

Contrast on per-type test-AUPRC **levels** (decision F1=A; the constant `val_auprc`
minuend cancels in the top-k − bottom-k difference, so levels and drops are an identical
contrast):

* point estimate — per-type AUPRC = mean over seeds of one-vs-rest AUPRC (that type's
  5 payloads' positives vs the seed's shared negatives); statistic
  ``T = mean(AUPRC[bottom_k]) − mean(AUPRC[top_k])`` (>0 ⇔ predicted-best out-detect
  predicted-worst ⇔ the predicted collapse-ordering holds).
* PRIMARY gate 1 — **type-level exact permutation**: all C(2k, k) splits of the 2k tail
  types; one-sided p = fraction with statistic ≥ observed. Min achievable p = 1/C(2k,k)
  (= 1/70 ≈ 0.0143 at k=4; near-saturated, disclosed in Revision 1).
* PRIMARY gate 2 — **payload-cluster bootstrap** (≥10 000): resample each type's 5 payload
  ids with replacement (shared across seeds), recompute per-type AUPRC, then T; one-sided
  95% percentile CI lower bound. Negatives held fixed; seeds averaged.
* SECONDARY — Kendall τ-b over all 14 types (measured −AUPRC vs predicted worseness rank);
  descriptive, higher resolution than the k=4 permutation.
* DECISION (unchanged rule, honest unit): SURVIVES iff permutation p<0.05 AND CI-low>0.

Reads the harness ``predictions.parquet`` files (the pre-pooled drop in ``metrics.json``
cannot support payload clustering). ``main()`` writes nothing; the write-gate lives in
``falsify_ood_wall.py``.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

_Pos = dict[int, dict[str, list[np.ndarray]]]
_Neg = dict[int, np.ndarray]

_HERE = Path(__file__).resolve().parent
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
_HEADLINE_FOLD = "core_attack_type"
_N_BOOT = 10_000

# Reuse the harness's exact AUPRC (eval_toolkit scorecard) for the *point* estimate so it
# is comparable to the persisted metrics.json; the bootstrap uses the fast numpy AP below.
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import metrics  # noqa: E402  # sibling module (hyphenated dir → sys.path inject, harness pattern)


def _ap_fast(y: np.ndarray, s: np.ndarray) -> float:
    """Step average-precision (sklearn-equivalent): mean precision over positive ranks."""
    order = np.argsort(-s, kind="mergesort")
    yy = y[order]
    tp = np.cumsum(yy)
    fp = np.cumsum(1.0 - yy)
    prec = tp / np.maximum(tp + fp, 1.0)
    n_pos = float(yy.sum())
    if n_pos == 0.0:
        return float("nan")
    return float(prec[yy == 1].sum() / n_pos)


def _recover_payload(text: pd.Series) -> pd.Series:
    """Payload = the injected attack string = last ``\\n\\n``-delimited segment."""
    return text.str.rsplit("\n\n", n=1).str[-1]


def load_clusters(results_dir: Path, rung: str) -> tuple[_Pos, _Neg, list[int]]:
    """Build per-seed cluster structure from predictions.parquet.

    Returns
    -------
    pos : ``{seed: {atype: [np.ndarray(scores) per payload, …]}}``
    neg : ``{seed: np.ndarray(neg_scores)}``
    seeds : sorted seed list
    """
    paths = sorted(results_dir.glob(f"seed=*/{_HEADLINE_FOLD}/{rung}.predictions.parquet"))
    if not paths:
        raise FileNotFoundError(f"no {rung} predictions under {results_dir}")
    pos: _Pos = {}
    neg: _Neg = {}
    seeds: list[int] = []
    for p in paths:
        seed = int(p.parent.parent.name.split("=")[1])
        seeds.append(seed)
        df = pd.read_parquet(p)
        neg[seed] = df.loc[df.label == 0, "y_score"].to_numpy(dtype=float)
        pdf = df.loc[df.label == 1].copy()
        pdf["payload"] = _recover_payload(pdf["text"])
        pos[seed] = {
            str(atype): [grp["y_score"].to_numpy(dtype=float) for _, grp in g.groupby("payload")]
            for atype, g in pdf.groupby("attack_type")
        }
    return pos, neg, sorted(seeds)


def point_auprc(pos: _Pos, neg: _Neg, seeds: list[int], *, exact: bool = True) -> dict[str, float]:
    """Per-type AUPRC = mean over seeds of one-vs-rest AUPRC (5 payloads' pos vs neg pool)."""
    types = sorted(pos[seeds[0]])
    out: dict[str, float] = {}
    for t in types:
        vals = []
        for s in seeds:
            ps = np.concatenate(pos[s][t])
            ns = neg[s]
            y = np.concatenate([np.ones(ps.size), np.zeros(ns.size)])
            sc = np.concatenate([ps, ns])
            vals.append(metrics._pr_auc(y, sc) if exact else _ap_fast(y, sc))
        out[t] = float(np.mean(vals))
    return out


def _statistic(auprc: dict[str, float], top_k: Sequence[str], bottom_k: Sequence[str]) -> float:
    """``mean(AUPRC[bottom_k]) − mean(AUPRC[top_k])`` (>0 ⇔ predicted ordering holds)."""
    return float(np.mean([auprc[t] for t in bottom_k]) - np.mean([auprc[t] for t in top_k]))


def permutation_exact(
    auprc: dict[str, float], top_k: Sequence[str], bottom_k: Sequence[str]
) -> tuple[float, int]:
    """Exact one-sided type-level permutation over the 2k tail types. Returns (p, n_splits)."""
    tail = list(top_k) + list(bottom_k)
    vals = np.array([auprc[t] for t in tail])
    n, k = len(tail), len(top_k)
    obs = _statistic(auprc, top_k, bottom_k)
    splits = list(itertools.combinations(range(n), k))  # which indices are "top"
    count = 0
    for top_idx in splits:
        top_mask = np.zeros(n, dtype=bool)
        top_mask[list(top_idx)] = True
        if float(vals[~top_mask].mean() - vals[top_mask].mean()) >= obs - 1e-12:
            count += 1
    return count / len(splits), len(splits)


def cluster_bootstrap(
    pos: _Pos,
    neg: _Neg,
    seeds: list[int],
    top_k: Sequence[str],
    bottom_k: Sequence[str],
    *,
    n_boot: int,
    seed: int,
) -> dict[str, float]:
    """Payload-cluster bootstrap on T; one-sided 95% CI lower bound + summary."""
    rng = np.random.default_rng(seed)
    tail = list(top_k) + list(bottom_k)
    n_payload = {t: len(pos[seeds[0]][t]) for t in tail}
    stats_b = np.empty(n_boot, dtype=float)
    for b in range(n_boot):
        auprc_b: dict[str, float] = {}
        for t in tail:
            idx = rng.integers(0, n_payload[t], size=n_payload[t])  # resample payload ids
            vals = []
            for s in seeds:
                ps = np.concatenate([pos[s][t][i] for i in idx])
                ns = neg[s]
                y = np.concatenate([np.ones(ps.size), np.zeros(ns.size)])
                sc = np.concatenate([ps, ns])
                vals.append(_ap_fast(y, sc))
            auprc_b[t] = float(np.mean(vals))
        stats_b[b] = _statistic(auprc_b, top_k, bottom_k)
    return {
        "ci_low": float(np.percentile(stats_b, 5.0)),
        "boot_mean": float(np.mean(stats_b)),
        "frac_gt0": float(np.mean(stats_b > 0.0)),
    }


def kendall_tau(
    auprc: dict[str, float], predicted_order: Sequence[str] | None
) -> tuple[float | None, float | None]:
    """Kendall τ-b over all 14 types: measured −AUPRC (worseness) vs predicted rank."""
    from scipy import stats as sstats  # type: ignore[import-untyped]

    ranked = [t for t in (predicted_order or []) if t in auprc]
    if len(ranked) < 3:
        return None, None
    worseness = [-auprc[t] for t in ranked]  # higher = worse-detected
    predicted_rank = list(range(len(ranked), 0, -1))  # rank len = predicted-worst = highest
    tau = sstats.kendalltau(worseness, predicted_rank, variant="b", alternative="greater")
    return float(tau.statistic), float(tau.pvalue)


def compute_verdict(
    results_dir: Path,
    rung: str,
    top_k: Sequence[str],
    bottom_k: Sequence[str],
    predicted_order: Sequence[str] | None = None,
    *,
    n_boot: int = _N_BOOT,
    seed: int = 0,
) -> dict[str, Any]:
    """Honest-unit §6.5 verdict payload (does not write). Raises if a tail type is absent."""
    pos, neg, seeds = load_clusters(results_dir, rung)
    auprc = point_auprc(pos, neg, seeds, exact=True)
    missing = [t for t in (*top_k, *bottom_k) if t not in auprc]
    if missing:
        raise ValueError(f"tail types absent from {rung} results: {missing}")

    obs = _statistic(auprc, top_k, bottom_k)
    perm_p, n_splits = permutation_exact(auprc, top_k, bottom_k)
    boot = cluster_bootstrap(pos, neg, seeds, top_k, bottom_k, n_boot=n_boot, seed=seed)
    tau, tau_p = kendall_tau(auprc, predicted_order)

    perm_pass = perm_p < 0.05
    ci_pass = boot["ci_low"] > 0.0
    return {
        "decision_rule": (
            "SURVIVES iff type-level permutation p<0.05 AND payload-cluster bootstrap CI-low>0"
        ),
        "estimator": "payload-clustered (criteria.md Revision 1)",
        "verdict": "SURVIVES" if (perm_pass and ci_pass) else "FALSIFIED",
        "statistic_T": obs,
        "mean_auprc_top_k": float(np.mean([auprc[t] for t in top_k])),
        "mean_auprc_bottom_k": float(np.mean([auprc[t] for t in bottom_k])),
        "seeds": seeds,
        "permutation": {
            "p_one_sided": perm_p,
            "n_splits": n_splits,
            "min_p": 1.0 / n_splits,
            "unit": "attack_type",
            "passed": perm_pass,
        },
        "bootstrap": {
            "ci_low": boot["ci_low"],
            "frac_gt0": boot["frac_gt0"],
            "n_resamples": n_boot,
            "unit": "payload_cluster",
            "passed": ci_pass,
        },
        "kendall_tau_b": {"statistic": tau, "p_one_sided": tau_p, "note": "secondary, 14 types"},
        "per_type_auprc": auprc,
    }


def main(argv: Sequence[str] | None = None) -> int:
    """Compute + print the honest-unit (payload-clustered) §6.5 contrast. Writes nothing."""
    ap = argparse.ArgumentParser(description="§6.5 honest-unit (payload-clustered) estimator.")
    ap.add_argument("--results-dir", type=Path, required=True)
    ap.add_argument("--rung", required=True)
    ap.add_argument("--n-boot", type=int, default=_N_BOOT)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args(argv)

    pred = json.loads((_OOD_DIR / "results.json").read_text(encoding="utf-8"))
    v = compute_verdict(
        args.results_dir,
        args.rung,
        pred["top_k_predicted_worst"],
        pred["bottom_k_predicted_best"],
        pred.get("predicted_collapse_order"),
        n_boot=args.n_boot,
        seed=args.seed,
    )
    perm, boot, tau = v["permutation"], v["bootstrap"], v["kendall_tau_b"]
    mt, mb = v["mean_auprc_top_k"], v["mean_auprc_bottom_k"]
    print(f"\n=== HONEST-UNIT §6.5 — rung={args.rung} seeds={v['seeds']} ===")
    print(f"mean AUPRC: worst-tail={mt:.3f}  best-tail={mb:.3f}")
    print(f"statistic T = mean(best)-mean(worst) = {v['statistic_T']:+.4f}")
    print(
        f"permutation (type-level, exact, n_splits={perm['n_splits']}): "
        f"p={perm['p_one_sided']:.4f} (min {perm['min_p']:.4f})  "
        f"{'PASS' if perm['passed'] else 'FAIL'}"
    )
    print(
        f"bootstrap (payload-cluster, n={boot['n_resamples']}): "
        f"ci_low(5%)={boot['ci_low']:+.4f}  frac(T*>0)={boot['frac_gt0']:.3f}  "
        f"{'PASS' if boot['passed'] else 'FAIL'}"
    )
    print(
        f"Kendall τ-b (14 types, secondary): τ={tau['statistic']:.3f} p={tau['p_one_sided']:.4f}"
        if tau["statistic"] is not None
        else "Kendall τ-b: n/a"
    )
    print(f"→ VERDICT (perm_p<0.05 AND ci_low>0): {v['verdict']}")
    print("(robustness rehearsal — nothing written)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
