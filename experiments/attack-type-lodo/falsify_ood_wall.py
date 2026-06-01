"""§6.5 OOD-wall falsification — write-gated entry for the verification half.

Reads the pre-registered prediction (``OOD_WALL_PREDICTION/{criteria.md,results.json}``)
and the harness ``predictions.parquet`` files, applies the **FIXED** decision rule from
``criteria.md`` (estimator corrected by **Revision 1** — payload-clustered resampling;
required rung set scoped by **Revision 2** — the 3-rung ``tfidf+frozen+lora`` ceiling, ADR-054),
and persists the SURVIVES/FALSIFIED verdict into the pre-registered record **only** for a
*complete headline sweep*.

The scientific computation (type-level permutation + payload-cluster bootstrap, contrast
on per-type test-AUPRC levels) lives in ``falsify_clustered.compute_verdict``; this module
owns the write-gate, the manifest/seed-completeness checks, and the verdict persistence.

* **DECISION:** SURVIVES iff type-level permutation ``p < 0.05`` **AND** the one-sided 95%
  payload-cluster bootstrap CI lower bound ``> 0`` (else FALSIFIED). A null is publishable.
* **Write-gated.** The verdict is written into ``OOD_WALL_PREDICTION/`` only when the
  harness MANIFEST's ``complete_headline_sweep`` flag is true and ≥3 seeds are present.
  A smoke / partial sweep prints the computed numbers and refuses to write.

Run (against a completed sweep)::

    python experiments/attack-type-lodo/falsify_ood_wall.py \
        --results-dir experiments/attack-type-lodo/results

Add ``--rung lora`` to select the headline rung whose per-type AUPRCs are judged
(default: the first rung present, preferring ``lora`` then ``full_ft``).
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))
import falsify_clustered as fc  # noqa: E402  # sibling module (hyphenated dir → sys.path inject)

_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
_DEFAULT_RESULTS = _HERE / "results"
_HEADLINE_FOLD = "core_attack_type"
_MIN_SEEDS = 3
_RUNG_PREFERENCE = ("lora", "full_ft", "frozen", "tfidf")


def load_prediction(ood_dir: Path) -> dict[str, Any]:
    """Load the pre-registered ``results.json`` (top-k / bottom-k / k)."""
    payload: dict[str, Any] = json.loads((ood_dir / "results.json").read_text(encoding="utf-8"))
    for key in ("top_k_predicted_worst", "bottom_k_predicted_best", "k"):
        if key not in payload:
            raise KeyError(f"results.json missing required key {key!r}")
    return payload


def select_rung(results_dir: Path, requested: str | None) -> str:
    """Pick the headline rung to judge: the request, else the preferred one present on disk."""
    present = {
        p.name.split(".")[0]
        for p in results_dir.glob(f"seed=*/{_HEADLINE_FOLD}/*.predictions.parquet")
    }
    if not present:
        raise FileNotFoundError(
            f"no {_HEADLINE_FOLD} predictions under {results_dir} (run harness.py first)"
        )
    if requested is not None:
        if requested not in present:
            raise ValueError(f"rung {requested!r} not in persisted results {sorted(present)}")
        return requested
    for rung in _RUNG_PREFERENCE:
        if rung in present:
            return rung
    return sorted(present)[0]


def manifest_complete(results_dir: Path) -> tuple[bool, str]:
    """Return ``(is_complete, reason)`` reading the harness MANIFEST's sweep-complete flag."""
    man_path = results_dir / "MANIFEST.yml"
    if not man_path.exists():
        return False, f"no MANIFEST.yml under {results_dir}"
    man = yaml.safe_load(man_path.read_text(encoding="utf-8"))
    seeds = man.get("config", {}).get("seeds", [])
    if not man.get("complete_headline_sweep", False):
        return False, "MANIFEST.complete_headline_sweep is false (partial rung/fold/seed set)"
    if len(seeds) < _MIN_SEEDS:
        return False, f"only {len(seeds)} seeds (< {_MIN_SEEDS} required)"
    return True, "complete headline sweep"


def main(argv: Sequence[str] | None = None) -> int:
    """Compute the §6.5 verdict; write it into OOD_WALL_PREDICTION/ only if write-gate opens."""
    args = _parse_args(argv)
    pred = load_prediction(_OOD_DIR)
    rung = select_rung(args.results_dir, args.rung)

    verdict = fc.compute_verdict(
        args.results_dir,
        rung,
        pred["top_k_predicted_worst"],
        pred["bottom_k_predicted_best"],
        pred.get("predicted_collapse_order"),
        n_boot=args.n_boot,
        seed=args.seed,
    )
    print(
        f"[falsify] rung={rung} seeds={verdict['seeds']} "
        f"T={verdict['statistic_T']:+.4f} "
        f"perm_p={verdict['permutation']['p_one_sided']:.4f} "
        f"ci_low={verdict['bootstrap']['ci_low']:+.4f} → {verdict['verdict']}"
    )

    complete, reason = manifest_complete(args.results_dir)
    if not complete:
        print(
            f"[falsify] WRITE-GATE CLOSED — verdict NOT persisted ({reason}). "
            "The pre-registered record only accepts a verdict from a complete headline sweep."
        )
        return 0

    out = {
        "computed_utc": datetime.now(UTC).isoformat(),
        "pre_registration": "experiments/eda/OOD_WALL_PREDICTION/criteria.md (Revision 2)",
        "harness_results": str(args.results_dir.relative_to(_HERE.parent.parent)),
        "harness_rung": rung,
        "harness_fold": _HEADLINE_FOLD,
        "k": pred["k"],
        "top_k_predicted_worst": pred["top_k_predicted_worst"],
        "bottom_k_predicted_best": pred["bottom_k_predicted_best"],
        **verdict,
    }
    verdict_path = _OOD_DIR / "falsification_verdict.json"
    verdict_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[falsify] WRITE-GATE OPEN — verdict written to {verdict_path}")
    return 0


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse the falsification-runner CLI."""
    p = argparse.ArgumentParser(description="§6.5 OOD-wall falsification (write-gated).")
    p.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS)
    p.add_argument("--rung", default=None, help="headline rung to judge (default: prefer lora)")
    p.add_argument("--n-boot", type=int, default=fc._N_BOOT, help="cluster bootstrap resamples")
    p.add_argument("--seed", type=int, default=0, help="resampling seed for perm/bootstrap")
    return p.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
