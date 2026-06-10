"""C1 verdict: does table-targeted data close the residual table wall? (criteria.md)

Decision rule (FIXED at ratification 2026-06-10, BEFORE any treated datum):
with ``ΔG = G_table^control − G_table^treated`` (positive = augmentation helped),
judged at the ``lora`` ceiling,

* **CLOSED**     iff ``G_table^treated(lora) < 0.05`` (SESOI) AND ``CI-low(ΔG) > 0``;
* **REDUCED**    iff ``CI-low(ΔG) > 0`` AND ``G_table^treated(lora) >= 0.05``;
* **NOT-CLOSED** iff ``CI-low(ΔG) <= 0`` (targeted data does not bridge — the B+ pattern).

Estimator: per arm, ``G = mean_seed(val_roc − test_roc)`` on the held-table fold
(``falsify_carrier_lodo`` loaders; val_roc held fixed). The ΔG bootstrap is
**paired across arms** (control and treated share the fold's test rows, so each
iteration draws one payload resample per seed and scores BOTH arms on it) and —
audit W4 — **independent across seeds** (every (iteration, seed) draws fresh
cluster indices; no draw indexes all seeds' replicates). One-sided 95 %,
``>= 10_000`` iters.

W10 dual reading: alongside the labels, the carrier arc's two rule readings on
``G_table^treated`` (sign-only; ½·G(frozen)) are reported for cross-axis
comparability — prose says "small under the pre-registered knob", never "no wall".

Write-gates (W3 lesson, shipped from day one):
- **manifest completeness**: the verdict only writes when BOTH arms hold >= 3
  seeds for the decision rung (``lora``) + both cheap rungs. Without ``lora``
  this script is a READ-OUT (prints per-rung ΔG, writes nothing, exit 0).
- **overwrite refusal**: the default ``c1_verdict.json`` is never clobbered —
  use ``--out`` for a scratch copy or ``--force`` to intentionally regenerate
  (exit 3 on refusal, mirroring ``falsify_ood_wall``).

Run::

    uv run python experiments/carrier-table-training/c1_verdict.py [--readout]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np

_HERE = Path(__file__).resolve().parent
_LODO_DIR = _HERE.parent / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import falsify_carrier_lodo as fcl  # noqa: E402

FOLD_NAME = "carrier_lodo_table"
CONTROL_DIR = _LODO_DIR / "results"
TREATED_DIR = _HERE / "C1_results_treated"
SESOI = 0.05
RUNGS: tuple[str, ...] = ("tfidf", "frozen", "lora")
_N_BOOT = 10_000
_MIN_SEEDS = 3


def decide(g_treated_lora: float, ci_low_delta_lora: float, *, sesoi: float = SESOI) -> str:
    """The pre-registered CLOSED / REDUCED / NOT-CLOSED rule (criteria.md, logic FIXED)."""
    if ci_low_delta_lora <= 0.0:
        return "NOT-CLOSED"
    if g_treated_lora < sesoi:
        return "CLOSED"
    return "REDUCED"


def dual_reading(g_treated: dict[str, float]) -> dict[str, str]:
    """W10 dual reading on the treated arm (sign-only + ½·G(frozen) knob)."""
    g_lora = g_treated.get("lora")
    g_frozen = g_treated.get("frozen")
    if g_lora is None or g_frozen is None:
        return {"sign_only": "n/a", "half_frozen_knob": "n/a"}
    sign_only = "no residual wall (G<=0)" if g_lora <= 0 else f"wall persists (G=+{g_lora:.3f})"
    knob = (
        f"attenuated below the knob (G={g_lora:.3f} < ½·G_frozen={0.5 * g_frozen:.3f})"
        if g_lora < 0.5 * g_frozen
        else f"holds at the knob (G={g_lora:.3f} >= ½·G_frozen={0.5 * g_frozen:.3f})"
    )
    return {"sign_only": sign_only, "half_frozen_knob": knob}


def _arm_g_point(fold: fcl.CarrierFold) -> float:
    """Point ``G = mean_seed(val_roc − test_roc)`` for one arm/rung."""
    gaps = [fold.val_roc[s] - fcl._point_test_roc(fold, s) for s in fold.seeds]
    return float(np.mean(gaps))


def _assert_aligned(ctrl: fcl.CarrierFold, treat: fcl.CarrierFold, rung: str) -> None:
    """Both arms must share seeds and identical payload-cluster structure (same fold test)."""
    if ctrl.seeds != treat.seeds:
        raise ValueError(f"{rung}: seed mismatch control={ctrl.seeds} treated={treat.seeds}")
    for s in ctrl.seeds:
        c_sizes = [a.size for a in ctrl.payload_pos[s]]
        t_sizes = [a.size for a in treat.payload_pos[s]]
        if c_sizes != t_sizes:
            raise ValueError(
                f"{rung} seed={s}: payload-cluster structure differs across arms "
                f"({len(c_sizes)} vs {len(t_sizes)} clusters) — test sets are not identical"
            )


def paired_delta_g(
    ctrl: fcl.CarrierFold,
    treat: fcl.CarrierFold,
    *,
    n_boot: int,
    rng: np.random.Generator,
) -> dict[str, Any]:
    """Point + paired bootstrap of ``ΔG = G_control − G_treated`` for one rung.

    Each iteration draws ONE payload resample per seed (fresh per seed — W4) and
    evaluates both arms on it; ``val_roc`` is held fixed per arm/seed.
    """
    g_c = _arm_g_point(ctrl)
    g_t = _arm_g_point(treat)
    delta_b = np.empty(n_boot, dtype=float)
    seeds = ctrl.seeds
    for b in range(n_boot):
        gaps_c: list[float] = []
        gaps_t: list[float] = []
        for s in seeds:
            n = len(ctrl.payload_pos[s])
            idx = rng.integers(0, n, size=n)  # fresh draw per (iteration, seed) — W4
            for fold, acc in ((ctrl, gaps_c), (treat, gaps_t)):
                pos = np.concatenate([fold.payload_pos[s][int(i)] for i in idx])
                ns = fold.neg[s]
                y = np.concatenate([np.ones(pos.size), np.zeros(ns.size)])
                sc = np.concatenate([pos, ns])
                acc.append(fold.val_roc[s] - fcl._roc_auc_fast(y, sc))
        delta_b[b] = float(np.mean(gaps_c) - np.mean(gaps_t))
    return {
        "G_control": g_c,
        "G_treated": g_t,
        "delta_G": g_c - g_t,
        "ci_low_delta": float(np.percentile(delta_b, 5.0)),
        "frac_delta_gt0": float(np.mean(delta_b > 0.0)),
    }


def _available_rungs(results_dir: Path) -> dict[str, int]:
    """Map rung -> #seeds present on disk for the held-table fold."""
    out: dict[str, int] = {}
    for rung in RUNGS:
        out[rung] = len(sorted(results_dir.glob(f"seed=*/{FOLD_NAME}/{rung}.predictions.parquet")))
    return out


def resolve_verdict_path(out: Path | None, *, force: bool) -> tuple[Path, bool, str]:
    """W3 overwrite gate: refuse to clobber the committed verdict by default."""
    path = out if out is not None else _HERE / "c1_verdict.json"
    if path.exists() and not force:
        return (
            path,
            False,
            f"{path} already exists; refusing to overwrite. Use --out <new-path> for a "
            "scratch copy, or --force to intentionally regenerate the canonical record",
        )
    return path, True, "ok"


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="C1 ΔG verdict (write-gated; criteria.md rule).")
    ap.add_argument("--control", type=Path, default=CONTROL_DIR)
    ap.add_argument("--treated", type=Path, default=TREATED_DIR)
    ap.add_argument("--n-boot", type=int, default=_N_BOOT)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--force", action="store_true")
    ap.add_argument(
        "--readout",
        action="store_true",
        help="Print per-rung ΔG for whatever rungs exist; never write (cheap-rung mode).",
    )
    args = ap.parse_args(argv)

    avail_c = _available_rungs(args.control)
    avail_t = _available_rungs(args.treated)
    print(f"[c1-verdict] control seeds/rung: {avail_c}", flush=True)
    print(f"[c1-verdict] treated seeds/rung: {avail_t}", flush=True)

    rng = np.random.default_rng(args.seed)
    per_rung: dict[str, Any] = {}
    for rung in RUNGS:
        if avail_c[rung] == 0 or avail_t[rung] == 0:
            continue
        ctrl = fcl.load_carrier_fold(args.control, FOLD_NAME, rung)
        treat = fcl.load_carrier_fold(args.treated, FOLD_NAME, rung)
        _assert_aligned(ctrl, treat, rung)
        per_rung[rung] = paired_delta_g(ctrl, treat, n_boot=args.n_boot, rng=rng)
        r = per_rung[rung]
        print(
            f"[{rung}] G_control={r['G_control']:+.4f} G_treated={r['G_treated']:+.4f} "
            f"ΔG={r['delta_G']:+.4f} (CI-low {r['ci_low_delta']:+.4f})",
            flush=True,
        )

    complete = all(avail_c[r] >= _MIN_SEEDS and avail_t[r] >= _MIN_SEEDS for r in RUNGS)
    if args.readout or not complete:
        if not complete:
            print(
                "[c1-verdict] WRITE-GATE CLOSED — decision needs >=3 seeds on BOTH arms for "
                f"all of {RUNGS} (lora = a separate present-first paid go). Read-out only.",
                flush=True,
            )
        return 0

    g_treated = {r: float(per_rung[r]["G_treated"]) for r in per_rung}
    verdict = decide(g_treated["lora"], float(per_rung["lora"]["ci_low_delta"]))
    record = {
        "experiment": "carrier-table-training (C1)",
        "fold": FOLD_NAME,
        "rule": "CLOSED iff G_treated(lora)<0.05 AND CI-low(dG)>0; REDUCED iff CI-low(dG)>0 "
        "AND G_treated(lora)>=0.05; NOT-CLOSED iff CI-low(dG)<=0",
        "sesoi": SESOI,
        "n_boot": args.n_boot,
        "verdict": verdict,
        "per_rung": per_rung,
        "w10_dual_reading_treated": dual_reading(g_treated),
    }
    verdict_path, allowed, reason = resolve_verdict_path(args.out, force=args.force)
    if not allowed:
        print(f"[c1-verdict] OVERWRITE-GATE CLOSED — {reason}", flush=True)
        return 3
    verdict_path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(f"[c1-verdict] VERDICT={verdict} → wrote {verdict_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
