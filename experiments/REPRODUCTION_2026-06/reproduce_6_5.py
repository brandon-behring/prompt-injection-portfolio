"""Reproduction audit — §6.5 attack-type OOD-wall verdict on `stratified_cluster_bootstrap_ci`.

Independently re-derives the §6.5 payload-clustered statistic ``T = mean(AUPRC[bottom_k]) −
mean(AUPRC[top_k])`` (per-type AUPRC = mean over seeds) with the upstream
`eval_toolkit.bootstrap.stratified_cluster_bootstrap_ci` (v1.8.0) and cross-checks against the
committed serial `OOD_WALL_PREDICTION/falsification_verdict.json` (the hand-rolled
`falsify_clustered`). The **lora**-rung FALSIFIED verdict is the one re-derived.

Strata = `{(attack_type, seed): (y, score, groups)}` over the 8 tail types × seeds; positives by
by recovered payload, negatives held fixed (`resample_labels=(1,)`); the composite `combine` is `T`.
Point uses the serial's exact AUPRC (`metrics._pr_auc`); the bootstrap uses the serial's fast AP
(`falsify_clustered._ap_fast`) — matching how the serial computes each.

Pre-stated rule (write-gate): point `T` exact-match; one-sided 95% CI-low within **±0.02**; the
verdict (sign of T / CI-low ≤ 0 ⇒ FALSIFIED) unchanged. CPU, `n_jobs=1`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
from eval_toolkit.bootstrap import stratified_cluster_bootstrap_ci

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
_ATTACK = _REPO / "experiments" / "attack-type-lodo"
if str(_ATTACK) not in sys.path:
    sys.path.insert(0, str(_ATTACK))
import falsify_clustered as fdc  # noqa: E402  (load_clusters + _ap_fast — the serial under audit)
import metrics  # noqa: E402  # _pr_auc (the serial's exact point AUPRC)

_RESULTS = _ATTACK / "results"
_VERDICT = _REPO / "experiments" / "eda" / "OOD_WALL_PREDICTION" / "falsification_verdict.json"
_RUNG = "lora"
_CI_TOL = 0.02
_N_BOOT = 5_000
_ONE_SIDED_CONF = 0.90


def _build(rung: str, tail: list[str]) -> dict[tuple, tuple]:
    """{(type, seed): (y, score, groups)} for the tail types from the clustered predictions."""
    pos, neg, seeds = fdc.load_clusters(_RESULTS, rung)  # pos[seed][type]=[payload arrays]
    strata: dict[tuple, tuple] = {}
    for t in tail:
        for s in seeds:
            arrays = pos[s][t]  # list of per-payload score arrays
            ns = neg[s]
            score = np.concatenate([*arrays, ns])
            y = np.concatenate([np.ones(score.size - ns.size), np.zeros(ns.size)])
            pos_groups = np.concatenate(
                [np.full(a.size, f"p{i}", dtype=object) for i, a in enumerate(arrays)]
            )
            groups = np.concatenate([pos_groups, np.full(ns.size, "__neg__", dtype=object)])
            strata[(t, s)] = (y, score, groups)
    return strata


def _make_combine(top: list[str], bottom: list[str]):
    """combine: T = mean(AUPRC[bottom]) − mean(AUPRC[top]); per-type AUPRC = mean over seeds."""

    def combine(m: dict) -> float:
        per_type: dict[str, list[float]] = {}
        for (t, _s), v in m.items():
            per_type.setdefault(t, []).append(v)
        auprc = {t: float(np.mean(vs)) for t, vs in per_type.items()}
        return float(np.mean([auprc[t] for t in bottom]) - np.mean([auprc[t] for t in top]))

    return combine


def main() -> int:
    """Reproduce the §6.5 lora-rung T + CI vs the committed serial verdict."""
    from eval_toolkit.artifacts import write_json_strict

    v = json.loads(_VERDICT.read_text())
    top, bottom = list(v["top_k_predicted_worst"]), list(v["bottom_k_predicted_best"])
    serial_t, serial_ci = float(v["statistic_T"]), float(v["bootstrap"]["ci_low"])

    strata = _build(_RUNG, top + bottom)
    combine = _make_combine(top, bottom)
    new_t = combine({k: metrics._pr_auc(strata[k][0], strata[k][1]) for k in strata})  # noqa: SLF001
    ci = stratified_cluster_bootstrap_ci(
        strata, fdc._ap_fast, combine, resample_labels=(1,),  # noqa: SLF001
        n_resamples=_N_BOOT, confidence=_ONE_SIDED_CONF, rng=0, n_jobs=1,
    )
    point_exact = bool(np.isclose(new_t, serial_t, atol=1e-9, rtol=0))
    drift = float(abs(ci.ci_low - serial_ci))
    verdict_ok = bool((ci.ci_low <= 0) == (serial_ci <= 0))  # FALSIFIED iff CI-low <= 0
    row: dict[str, Any] = {
        "rung": _RUNG, "serial_T": serial_t, "new_T": new_t, "point_exact_match": point_exact,
        "serial_ci_low": serial_ci, "new_ci_low": ci.ci_low, "ci_low_drift": drift,
        "ci_within_tol": bool(drift <= _CI_TOL), "verdict_unchanged": verdict_ok,
        "reproduced": point_exact and drift <= _CI_TOL and verdict_ok,
    }
    print("\n=== §6.5 reproduction (lora rung; FALSIFIED verdict) ===")
    print(
        f"  {_RUNG:6s} T {serial_t:+.4f}->{new_t:+.4f} "
        f"[{'exact' if point_exact else 'MISMATCH'}]  "
        f"ci_low {serial_ci:+.4f}->{ci.ci_low:+.4f} (Δ{drift:.4f})  "
        f"verdict {'OK' if verdict_ok else 'CHANGED'}  {'PASS' if row['reproduced'] else 'FAIL'}"
    )
    out = {"axis": "attack_type_6.5", "n_boot": _N_BOOT, "ci_tol": _CI_TOL, "row": row,
           "reproduced": row["reproduced"]}
    write_json_strict(out, _HERE / "attack_type_6_5_reproduction.json")
    print(f"written -> {_HERE / 'attack_type_6_5_reproduction.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
