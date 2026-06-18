"""B4 — the write-gated cross-family verdict rule (criteria.md Rev 4 §Statistics 2, lines 150-160).

**Locked before any ``lora`` datum** (write-gate discipline, criteria.md:179): the
SURVIVES / FALSIFIED / SMALL-THROUGHOUT logic is fixed here, not after seeing the paid result. It
consumes the :func:`falsify_dialect_lodo.directional_table` output (``per_rung[rung][fold]`` carries
``Gx`` + the one-sided 95 % label-stratified-cluster bootstrap ``ci_low`` / ``ci_high``) and applies
the per-unit rule, **per arm**:

* **SURVIVES**  iff ``Gx(lora)`` CI-low > 0 **AND** ``Gx(lora) >= ½·Gx(frozen)`` **AND**
  ``Gx(lora) >= 0.05`` (the pre-specified SESOI floor);
* **FALSIFIED** iff ``Gx(lora)`` CI-low <= 0 (the gap is statistically indistinguishable from
  dissolved at the ceiling — capacity climbs the wall);
* else **SMALL-THROUGHOUT** (a wall present but small / collapsed relative to frozen).

The **bare ½·Gx(frozen)** verdict (no SESOI floor) is also reported for direct cross-axis
comparability with the attack-type + carrier axes (criteria.md:155-156).

The aggregate is **descriptive** (mean over units + spread) — deliberately **NOT** a cross-fold
cluster bootstrap (known-bad at n=4/5; criteria.md:172). The **lead result is the per-unit table**,
not the aggregate (criteria.md:177); the verdict is labelled directional / low-power (n=4 dialects,
n=5 slices via the pooled cluster bootstrap; criteria.md:180-181).

The ``lora_rung`` / ``frozen_rung`` knobs let the **free B4-path pre-validation** exercise every code
path on the existing cheap-rung trees before any spend, by mapping ``lora→frozen`` and
``frozen→tfidf`` (the *real* verdict awaits the lora column; the arithmetic is fully covered)::

    uv run python experiments/cross-family-transfer/b4_verdict.py \
        --results B2_3_results/natural --folds-arm B --pre-validate
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Literal

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

SESOI: float = 0.05  # pre-registered SESOI floor (criteria.md:151-153)
HALF: float = (
    0.5  # the ½·Gx(frozen) non-collapse fraction (== §6.5 + carrier-LODO; criteria.md:154)
)

Verdict = Literal["SURVIVES", "FALSIFIED", "SMALL_THROUGHOUT"]


def _unit_verdict(
    gx_lora: float, ci_low_lora: float, gx_frozen: float, *, sesoi: float, frac: float
) -> Verdict:
    """The pre-registered per-unit verdict (criteria.md:150-160)."""
    if ci_low_lora <= 0:
        return "FALSIFIED"
    if gx_lora >= frac * gx_frozen and gx_lora >= sesoi:
        return "SURVIVES"
    return "SMALL_THROUGHOUT"


def _unit_verdict_bare(
    gx_lora: float, ci_low_lora: float, gx_frozen: float, *, frac: float
) -> Verdict:
    """The bare ½·Gx(frozen) verdict (no SESOI floor) for cross-axis comparability (criteria.md:155)."""
    if ci_low_lora <= 0:
        return "FALSIFIED"
    return "SURVIVES" if gx_lora >= frac * gx_frozen else "SMALL_THROUGHOUT"


def verdict(
    table: dict[str, Any],
    *,
    arm: str,
    lora_rung: str = "lora",
    frozen_rung: str = "frozen",
    sesoi: float = SESOI,
    frac: float = HALF,
) -> dict[str, Any]:
    """Apply the write-gated verdict rule to a ``directional_table`` output, per arm.

    Parameters
    ----------
    table : dict
        A :func:`falsify_dialect_lodo.directional_table` result (``per_rung[rung][fold]`` cells).
    arm : str
        Arm label for the report (e.g. ``"Arm A (direct→indirect)"``).
    lora_rung, frozen_rung : str
        Rung keys to treat as the ceiling rung and its half-comparator. Defaults
        ``"lora"`` / ``"frozen"`` (the real B4); the pre-validation passes ``"frozen"`` / ``"tfidf"``.
    sesoi, frac : float
        The pre-registered free knobs (fixed; here only to expose them in the report).

    Raises
    ------
    KeyError
        If either rung is absent from the table (e.g. the lora tree has not been merged).
    """
    per_rung = table["per_rung"]
    for r in (lora_rung, frozen_rung):
        if r not in per_rung:
            raise KeyError(
                f"directional_table has no {r!r} rung (have {sorted(per_rung)}) — "
                f"merge the lora tree first (run_b3_lora.py --merge ...) or use --pre-validate"
            )
    lora = per_rung[lora_rung]
    frozen = per_rung[frozen_rung]

    per_unit: dict[str, Any] = {}
    for fold_name, cell in lora.items():
        gx_l = float(cell["Gx"])
        ci_low = float(cell["ci_low"])
        gx_f = float(frozen[fold_name]["Gx"])
        per_unit[fold_name] = {
            "Gx_lora": gx_l,
            "ci_low_lora": ci_low,
            "ci_high_lora": float(cell["ci_high"]),
            "Gx_frozen": gx_f,
            "half_Gx_frozen": frac * gx_f,
            "ci_low_positive": ci_low > 0,
            "passes_half_frozen": gx_l >= frac * gx_f,
            "passes_sesoi": gx_l >= sesoi,
            "perm_p": (None if cell.get("perm_p") is None else float(cell["perm_p"])),
            "verdict": _unit_verdict(gx_l, ci_low, gx_f, sesoi=sesoi, frac=frac),
            "verdict_bare": _unit_verdict_bare(gx_l, ci_low, gx_f, frac=frac),
        }

    gx_loras = [u["Gx_lora"] for u in per_unit.values()]
    gx_frozens = [u["Gx_frozen"] for u in per_unit.values()]
    verdicts = [u["verdict"] for u in per_unit.values()]
    counts = {v: verdicts.count(v) for v in ("SURVIVES", "SMALL_THROUGHOUT", "FALSIFIED")}
    n_units = len(per_unit)

    # Directional arm read from the per-unit pattern (low-power; a catastrophic single-unit wall must
    # not be masked by a benign mean — criteria.md:177). NOT a bootstrapped arm verdict.
    if n_units == 0:
        arm_read = "NO_UNITS"
    elif counts["FALSIFIED"] == n_units:
        arm_read = "FALSIFIED (all units; directional)"
    elif counts["SURVIVES"] >= 1 and counts["FALSIFIED"] == 0:
        arm_read = "SURVIVES (>=1 unit, none falsified; directional)"
    elif counts["SURVIVES"] == 0 and counts["FALSIFIED"] == 0:
        arm_read = "SMALL_THROUGHOUT (directional)"
    else:
        arm_read = "MIXED (see per-unit table; directional)"

    return {
        "arm": arm,
        "rungs": {"ceiling": lora_rung, "half_comparator": frozen_rung},
        "rule": {
            "frac_of_frozen": frac,
            "sesoi_roc_auc": sesoi,
            "SURVIVES": "ci_low(ceiling)>0 AND Gx(ceiling)>=frac*Gx(frozen) AND Gx(ceiling)>=sesoi",
            "FALSIFIED": "ci_low(ceiling)<=0",
            "else": "SMALL_THROUGHOUT",
        },
        "per_unit": per_unit,
        "aggregate": {
            "Gx_lora_mean": (None if not gx_loras else float(np.mean(gx_loras))),
            "Gx_lora_min": (None if not gx_loras else float(min(gx_loras))),
            "Gx_lora_max": (None if not gx_loras else float(max(gx_loras))),
            "Gx_lora_per_unit": {k: v["Gx_lora"] for k, v in per_unit.items()},
            "Gx_frozen_mean": (None if not gx_frozens else float(np.mean(gx_frozens))),
            "verdict_counts": counts,
            "directional_arm_read": arm_read,
        },
        "note": (
            "Directional / low-power (n=4 dialects / n=5 slices via the pooled cluster bootstrap; "
            "criteria.md:180-181). The LEAD is the per-unit table, NOT the aggregate (criteria.md:177); "
            "the aggregate is descriptive (mean + spread), deliberately NOT a cross-fold cluster "
            "bootstrap (known-bad at n=4/5; criteria.md:172). Pre-validation (lora→frozen) exercises "
            "the arithmetic; the real verdict awaits the merged lora column."
        ),
    }


def verdict_from_results(
    results_dir: Path,
    folds: list[str],
    *,
    arm: str,
    rungs: tuple[str, ...] = ("tfidf", "frozen", "lora"),
    lora_rung: str = "lora",
    frozen_rung: str = "frozen",
    n_boot: int | None = None,
    n_perm: int | None = None,
) -> dict[str, Any]:
    """Run ``directional_table`` on ``results_dir`` then apply :func:`verdict` (the B4 entry point)."""
    import falsify_dialect_lodo as fdl

    kw: dict[str, Any] = {"rungs": rungs}
    if n_boot is not None:
        kw["n_boot"] = n_boot
    if n_perm is not None:
        kw["n_perm"] = n_perm
    table = fdl.directional_table(Path(results_dir), folds, **kw)
    return verdict(table, arm=arm, lora_rung=lora_rung, frozen_rung=frozen_rung)


def main(argv: list[str] | None = None) -> int:
    """CLI: compute the B4 verdict (or the free pre-validation) for one arm's merged results tree."""
    import folds_dialect as fd

    p = argparse.ArgumentParser(
        description="B4 cross-family verdict (write-gated; criteria Rev 4)."
    )
    p.add_argument(
        "--results", type=Path, required=True, help="results dir (e.g. B2_3_results/natural)"
    )
    p.add_argument(
        "--folds-arm", choices=["A", "B"], required=True, help="A → arm_a_pooled; B → 4 dialects"
    )
    p.add_argument(
        "--folds", nargs="+", default=None, help="explicit fold names (overrides --folds-arm)"
    )
    p.add_argument("--arm", default=None, help="arm label for the report")
    p.add_argument(
        "--pre-validate",
        action="store_true",
        help="free dry run: map lora→frozen, frozen→tfidf to exercise the arithmetic on cheap rungs",
    )
    p.add_argument("--n-boot", type=int, default=None)
    p.add_argument("--n-perm", type=int, default=None)
    p.add_argument(
        "--out", type=Path, default=None, help="write verdict.json here (default: stdout)"
    )
    args = p.parse_args(argv)

    folds = args.folds or (
        ["arm_a_pooled"] if args.folds_arm == "A" else list(fd.DIALECT_LODO_FOLDS)
    )
    arm = args.arm or (f"Arm {args.folds_arm}" + (" pre-validate" if args.pre_validate else ""))
    if args.pre_validate:
        rungs, lora_rung, frozen_rung = ("tfidf", "frozen"), "frozen", "tfidf"
    else:
        rungs, lora_rung, frozen_rung = ("tfidf", "frozen", "lora"), "lora", "frozen"

    result = verdict_from_results(
        args.results,
        folds,
        arm=arm,
        rungs=rungs,
        lora_rung=lora_rung,
        frozen_rung=frozen_rung,
        n_boot=args.n_boot,
        n_perm=args.n_perm,
    )
    text = json.dumps(result, indent=2)
    if args.out is not None:
        args.out.write_text(text + "\n", encoding="utf-8")
        print(f"verdict → {args.out}  (arm_read={result['aggregate']['directional_arm_read']})")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
