"""Reproduction audit — carrier-LODO (M2) verdict on `stratified_cluster_bootstrap_ci`.

Independently re-derives `G(rung) = mean over carriers of [val_roc − test_roc(held-out carrier)]`
with the upstream `eval_toolkit.bootstrap.stratified_cluster_bootstrap_ci` (v1.8.0) and cross-checks
against the committed serial `carrier-lodo/verdict.json` (the hand-rolled `falsify_carrier_lodo`).

Strata = `{(carrier, seed): (y, score, groups)}` over the 3 carriers (code/email/table) × seeds;
positives grouped by recovered payload, negatives held fixed (`resample_labels=(1,)`); the composite
`combine` is the cross-carrier mean of `val[c] − mean_seed(test_roc[c, ·])`. All three rungs
(tfidf / frozen / lora) — so the SMALL-THROUGHOUT lora verdict is re-derived.

Pre-stated rule (write-gate): point `G` exact-match vs the committed serial; one-sided 95% CI-low
within **±0.02 ROC-AUC**; verdict (sign of `G(lora)` + ½-rule) unchanged. CPU, `n_jobs=1`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from eval_toolkit.bootstrap import stratified_cluster_bootstrap_ci

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent
_ATTACK = _REPO / "experiments" / "attack-type-lodo"
if str(_ATTACK) not in sys.path:
    sys.path.insert(0, str(_ATTACK))
import metrics  # noqa: E402

_RESULTS = _ATTACK / "results"
_VERDICT = _REPO / "experiments" / "carrier-lodo" / "verdict.json"
_CARRIERS = ("code", "email", "table")
_RUNGS = ("tfidf", "frozen", "lora")
_CI_TOL = 0.02
_N_BOOT = 5_000  # plenty for the CI cross-check (point is n_boot-invariant; serial baseline used 10k)
_ONE_SIDED_CONF = 0.90


def _recover_payload(text: pd.Series) -> pd.Series:
    """Payload = last ``\\n\\n``-delimited segment (mirrors the serial ``_recover_payload``)."""
    return text.str.rsplit("\n\n", n=1).str[-1]


def _build(rung: str) -> tuple[dict[tuple, tuple], dict[str, float]]:
    """{(carrier, seed): (y, score, groups)} + {carrier: seed-mean val_roc} for one rung."""
    strata: dict[tuple, tuple] = {}
    val_by_carrier: dict[str, float] = {}
    for carrier in _CARRIERS:
        vrs: list[float] = []
        glob = f"seed=*/carrier_lodo_{carrier}/{rung}.predictions.parquet"
        for pred in sorted(_RESULTS.glob(glob)):
            seed = int(pred.parent.parent.name.split("=")[1])
            df = pd.read_parquet(pred)
            labels = df["label"].to_numpy()
            payloads = _recover_payload(df["text"]).to_numpy()
            groups = np.where(labels == 1, payloads, "__neg__")
            strata[(carrier, seed)] = (labels, df["y_score"].to_numpy(dtype=float), groups)
            meta = json.loads(pred.with_name(f"{rung}.metrics.json").read_text())
            vrs.append(float(meta["val_roc_auc"]))
        val_by_carrier[carrier] = float(np.mean(vrs))
    return strata, val_by_carrier


def _make_combine(val_by_carrier: dict[str, float]):
    """combine: mean over carriers of (val[c] − mean over that carrier's seeds of the metric)."""

    def combine(m: dict) -> float:
        per_carrier: dict[str, list[float]] = {}
        for (carrier, _seed), v in m.items():
            per_carrier.setdefault(carrier, []).append(v)
        gaps = [val_by_carrier[c] - float(np.mean(vs)) for c, vs in per_carrier.items()]
        return float(np.mean(gaps))

    return combine


def reproduce_rung(rung: str, serial_g: float, serial_ci: float) -> dict[str, Any]:
    """Point-exact + CI cross-check for one rung vs the committed serial."""
    strata, val_by_carrier = _build(rung)
    combine = _make_combine(val_by_carrier)
    new_point = combine({k: metrics.roc_auc_point(strata[k][0], strata[k][1]) for k in strata})
    ci = stratified_cluster_bootstrap_ci(
        strata, metrics.roc_auc_point, combine, resample_labels=(1,),
        n_resamples=_N_BOOT, confidence=_ONE_SIDED_CONF, rng=0, n_jobs=1,
    )
    point_exact = bool(np.isclose(new_point, serial_g, atol=1e-9, rtol=0))
    drift = float(abs(ci.ci_low - serial_ci))
    return {
        "rung": rung, "serial_g": serial_g, "new_G": new_point, "point_exact_match": point_exact,
        "serial_ci_low": serial_ci, "new_ci_low": ci.ci_low, "ci_low_drift": drift,
        "ci_within_tol": bool(drift <= _CI_TOL),
        "sign_unchanged": bool(np.sign(new_point) == np.sign(serial_g)),
        "reproduced": point_exact and drift <= _CI_TOL and np.sign(new_point) == np.sign(serial_g),
    }


def main() -> int:
    """Run carrier reproduction over the 3 rungs; print + write a report."""
    from eval_toolkit.artifacts import write_json_strict

    v = json.loads(_VERDICT.read_text())
    g_by, ci_by = v["G_by_rung"], v["ci_low_by_rung"]
    print("\n=== CARRIER reproduction (point-exact + CI cross-check, all rungs) ===")
    rows = [reproduce_rung(r, float(g_by[r]), float(ci_by[r])) for r in _RUNGS]
    for r in rows:
        print(
            f"  {r['rung']:6s} G {r['serial_g']:+.4f}->{r['new_G']:+.4f} "
            f"[{'exact' if r['point_exact_match'] else 'MISMATCH'}]  "
            f"ci {r['serial_ci_low']:+.4f}->{r['new_ci_low']:+.4f} (Δ{r['ci_low_drift']:.4f})  "
            f"{'PASS' if r['reproduced'] else 'FAIL'}"
        )
    n_pass = sum(r["reproduced"] for r in rows)
    print(f"\n{n_pass}/{len(rows)} reproduced. (lora verdict = SMALL-THROUGHOUT re-derived)")
    write_json_strict(
        {"axis": "carrier", "n_boot": _N_BOOT, "ci_tol": _CI_TOL, "rows": rows,
         "all_reproduced": n_pass == len(rows)},
        _HERE / "carrier_reproduction.json",
    )
    print(f"written -> {_HERE / 'carrier_reproduction.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
