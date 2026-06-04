"""Reproduction audit — dialect-LODO (B2.3) verdict on `stratified_cluster_bootstrap_ci`.

Independently re-derives the dialect-transfer `Gx` directional read with the **upstream**
`eval_toolkit.bootstrap.stratified_cluster_bootstrap_ci` (v1.8.0) and cross-checks it against the
**committed serial** numbers (`B2_3_results/summary.json`, produced by the hand-rolled
`falsify_dialect_lodo`) — restoring trust via an independent implementation.

Pre-stated reproduction rule (write-gate — fixed before any number is read):

* **point `Gx` must match the committed serial EXACTLY** — it is deterministic
  (`val − mean_seed(test_roc)` on the persisted predictions; no bootstrap). The strong check: any
  implementation bug in the point path shows here.
* **CI-low cross-check on the genuinely-clustered folds** (bipia, injecagent — few clusters): the
  new one-sided 95% CI-low must agree with the committed serial within **±0.02 ROC-AUC** (≫ the
  bootstrap MC SE, ≪ the 0.05 SESOI). browsesafe/fujitsu are cluster=row (mechanically a row
  bootstrap) → point-exact + identical scheme + the upstream-tested primitive covers them.
* the directional reading (sign of `Gx`) is unchanged.

CPU only, `n_jobs=1`; reads the gitignored `B2_3_results/` parquets. Writes a compact JSON report.
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
import metrics  # noqa: E402  # the exact point fn the serial used (roc_auc_point)

_RESULTS = _REPO / "experiments" / "cross-family-transfer" / "B2_3_results" / "natural"
_SUMMARY = _REPO / "experiments" / "cross-family-transfer" / "B2_3_results" / "summary.json"
_DIALECTS = ("bipia", "browsesafe", "fujitsu", "injecagent")
_CI_FOLDS = ("bipia", "injecagent")  # genuinely-clustered + low-power → the meaningful CI check
_CI_TOL = 0.02
_N_BOOT = 10_000
_ONE_SIDED_CONF = 0.90  # two-sided 90% -> 5th-percentile = one-sided 95% lower bound


def _load(fold: str, rung: str) -> tuple[dict[int, tuple], float]:
    """{seed: (y, score, cluster_id)} + seed-mean val_roc from the persisted parquets."""
    strata: dict[int, tuple] = {}
    val_rocs: list[float] = []
    for pred in sorted(_RESULTS.glob(f"seed=*/dialect_lodo_{fold}/{rung}.predictions.parquet")):
        seed = int(pred.parent.parent.name.split("=")[1])
        df = pd.read_parquet(pred)
        strata[seed] = (
            df["label"].to_numpy(),
            df["y_score"].to_numpy(dtype=float),
            df["cluster_id"].to_numpy(),
        )
        meta = json.loads(pred.with_name(f"{rung}.metrics.json").read_text())
        val_rocs.append(float(meta["val_roc_auc"]))
    return strata, float(np.mean(val_rocs))


def reproduce_fold(fold: str, rung: str, serial: dict[str, float]) -> dict[str, Any]:
    """Point-exact (all folds) + CI cross-check (clustered folds) vs the committed serial."""
    strata, val = _load(fold, rung)

    def combine(m: dict) -> float:
        return float(val - np.mean(list(m.values())))

    new_point = combine({s: metrics.roc_auc_point(strata[s][0], strata[s][1]) for s in strata})
    point_exact = bool(np.isclose(new_point, serial["Gx"], atol=1e-9, rtol=0))
    sign_ok = bool(np.sign(new_point) == np.sign(serial["Gx"]))

    row: dict[str, Any] = {
        "fold": fold, "rung": rung,
        "serial_Gx": serial["Gx"], "new_Gx": new_point,
        "point_exact_match": point_exact, "sign_unchanged": sign_ok,
        "ci_checked": fold in _CI_FOLDS,
    }
    if fold in _CI_FOLDS:
        ci = stratified_cluster_bootstrap_ci(
            strata, metrics.roc_auc_point, combine, resample_labels=(0, 1),
            n_resamples=_N_BOOT, confidence=_ONE_SIDED_CONF, rng=0, n_jobs=1,
        )
        drift = float(abs(ci.ci_low - serial["ci_low"]))
        row.update(serial_ci_low=serial["ci_low"], new_ci_low=ci.ci_low,
                   ci_low_drift=drift, ci_within_tol=bool(drift <= _CI_TOL))
        row["reproduced"] = point_exact and sign_ok and row["ci_within_tol"]
    else:
        row["reproduced"] = point_exact and sign_ok  # CI covered by point + tested primitive
    return row


def main() -> int:
    """Run dialect reproduction over 4 folds × {tfidf, frozen}; print + write a report."""
    from eval_toolkit.artifacts import write_json_strict

    nt = json.loads(_SUMMARY.read_text())["directional_table"]["natural"]["per_rung"]
    rows = []
    print(f"\n=== DIALECT reproduction (point-exact all folds; CI cross-check {_CI_FOLDS}) ===")
    for rung in ("tfidf", "frozen"):
        for fold in _DIALECTS:
            serial = nt[rung][f"dialect_lodo_{fold}"]
            r = reproduce_fold(fold, rung, serial)
            rows.append(r)
            ci_s = (
                f"ci {r['serial_ci_low']:+.4f}->{r['new_ci_low']:+.4f} (Δ{r['ci_low_drift']:.4f})"
                if r["ci_checked"] else "ci: covered by point+scheme"
            )
            print(
                f"  {rung:6s} {fold:11s} Gx {r['serial_Gx']:+.4f}->{r['new_Gx']:+.4f} "
                f"[{'exact' if r['point_exact_match'] else 'MISMATCH'}]  {ci_s}  "
                f"{'PASS' if r['reproduced'] else 'FAIL'}"
            )
    n_pass = sum(r["reproduced"] for r in rows)
    print(f"\n{n_pass}/{len(rows)} reproduced.")
    write_json_strict(
        {"axis": "dialect", "n_boot": _N_BOOT, "ci_tol": _CI_TOL, "rows": rows,
         "all_reproduced": n_pass == len(rows)},
        _HERE / "dialect_reproduction.json",
    )
    print(f"written -> {_HERE / 'dialect_reproduction.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
