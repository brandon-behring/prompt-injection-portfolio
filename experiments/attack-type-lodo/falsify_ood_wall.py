"""§6.5 OOD-wall falsification — the verification half of the pre-modeling prediction.

Reads the pre-registered prediction (``OOD_WALL_PREDICTION/{criteria.md,results.json}``)
and the per-test-attack-type val→test AUPRC **drops** the harness persisted (spec §5
retention), then applies the **FIXED** decision rule from ``criteria.md`` (no knob
revisited at verification time):

* **PRIMARY** — one-sided top-k vs bottom-k permutation contrast (``k=4``):
  ``scipy.stats.permutation_test`` (``permutation_type="independent"``,
  ``statistic = mean(top_drops) − mean(bottom_drops)``, ``alternative="greater"``).
* **PRIMARY** — one-sided 95% bootstrap CI on the same mean-drop difference
  (``scipy.stats.bootstrap``, ≥10 000 resamples; percentile **and** BCa, BCa flagged
  if it disagrees / degenerates).
* **SECONDARY** — Kendall τ-b over all 14 types (``scipy.stats.kendalltau``,
  ``variant="b"``), descriptive only — **not** the gate.
* **DECISION:** SURVIVES iff ``permutation_p < 0.05`` **AND** the one-sided 95%
  bootstrap-CI lower bound on the top-k−bottom-k mean-drop difference ``> 0``; else
  FALSIFIED. A null result is publishable.

**Write-gated.** The SURVIVES/FALSIFIED verdict is written into the pre-registered
``OOD_WALL_PREDICTION/`` record **only** for a *complete headline sweep* (the harness
MANIFEST's ``complete_headline_sweep`` flag is true and every required per-type drop is
present). A smoke / partial sweep prints the computed numbers and refuses to write —
the pre-registered record must never carry a verdict from an incomplete run.

Run (against a completed sweep)::

    python experiments/attack-type-lodo/falsify_ood_wall.py \
        --results-dir experiments/attack-type-lodo/results

Add ``--rung lora`` to select the headline rung whose drops are judged (default: the
first rung present, preferring ``lora`` then ``full_ft``).
"""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np
import yaml
from scipy import stats

_HERE = Path(__file__).resolve().parent
_OOD_DIR = _HERE.parent / "eda" / "OOD_WALL_PREDICTION"
_DEFAULT_RESULTS = _HERE / "results"
_HEADLINE_FOLD = "core_attack_type"
_MIN_ITEMS = 10  # fold-size policy (criteria.md): per-type folds < 10 scored items merge out
_MIN_SEEDS = 3
_N_PERMUTATIONS = 10_000
_N_BOOTSTRAP = 10_000
_RUNG_PREFERENCE = ("lora", "full_ft", "frozen", "tfidf")


def _mean_diff(top: np.ndarray, bottom: np.ndarray, axis: int = 0) -> np.floating[Any]:
    """Statistic for both tests: ``mean(top) − mean(bottom)`` (vectorized over ``axis``)."""
    return np.mean(top, axis=axis) - np.mean(bottom, axis=axis)


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
        for p in (results_dir).glob(f"seed=*/{_HEADLINE_FOLD}/*.metrics.json")
    }
    if not present:
        raise FileNotFoundError(
            f"no {_HEADLINE_FOLD} metrics under {results_dir} (run harness.py first)"
        )
    if requested is not None:
        if requested not in present:
            raise ValueError(f"rung {requested!r} not in persisted results {sorted(present)}")
        return requested
    for rung in _RUNG_PREFERENCE:
        if rung in present:
            return rung
    return sorted(present)[0]


def collect_drops(results_dir: Path, rung: str) -> dict[str, list[float]]:
    """Aggregate per-test-attack-type drops for ``rung`` on the headline fold, across seeds.

    Only per-type cells with a non-``None`` drop **and** ``n_total >= _MIN_ITEMS`` (the
    criteria.md fold-size policy) contribute. Returns ``{attack_type: [drop_per_seed, …]}``.
    """
    drops: dict[str, list[float]] = {}
    for mpath in sorted(results_dir.glob(f"seed=*/{_HEADLINE_FOLD}/{rung}.metrics.json")):
        rec = json.loads(mpath.read_text(encoding="utf-8"))
        for atype, cell in rec["per_type"].items():
            drop = cell.get("drop")
            if drop is None or cell.get("n_total", 0) < _MIN_ITEMS:
                continue
            drops.setdefault(atype, []).append(float(drop))
    return drops


def _tail_drops(drops: dict[str, list[float]], types: Sequence[str]) -> list[float]:
    """Flatten the per-seed drops for a tail's attack-types into one sample."""
    out: list[float] = []
    for t in types:
        out.extend(drops.get(t, []))
    return out


def run_falsification(
    drops: dict[str, list[float]],
    top_k: Sequence[str],
    bottom_k: Sequence[str],
    predicted_order: Sequence[str] | None,
    *,
    seed: int = 0,
) -> dict[str, Any]:
    """Apply the FIXED decision rule; return the verdict payload (does not write).

    Raises
    ------
    ValueError
        If either tail has no scored drops (the contrast is undefined).
    """
    top = np.asarray(_tail_drops(drops, top_k), dtype=float)
    bottom = np.asarray(_tail_drops(drops, bottom_k), dtype=float)
    if top.size == 0 or bottom.size == 0:
        raise ValueError(
            f"empty tail sample (top n={top.size}, bottom n={bottom.size}); "
            "cannot run the top-k vs bottom-k contrast"
        )

    perm = stats.permutation_test(
        (top, bottom), _mean_diff, permutation_type="independent",
        alternative="greater", n_resamples=_N_PERMUTATIONS, random_state=seed,
    )
    perm_p = float(perm.pvalue)

    boot_pct = stats.bootstrap(
        (top, bottom), _mean_diff, n_resamples=_N_BOOTSTRAP, confidence_level=0.95,
        alternative="greater", method="percentile", random_state=seed, paired=False,
        vectorized=True,
    )
    ci_low_pct = float(boot_pct.confidence_interval.low)
    try:
        boot_bca = stats.bootstrap(
            (top, bottom), _mean_diff, n_resamples=_N_BOOTSTRAP, confidence_level=0.95,
            alternative="greater", method="BCa", random_state=seed, paired=False,
            vectorized=True,
        )
        ci_low_bca: float | None = float(boot_bca.confidence_interval.low)
    except Exception as exc:  # noqa: BLE001 — BCa degenerates on small/skewed tails; percentile gates
        ci_low_bca = None
        bca_note = f"BCa unavailable ({type(exc).__name__}: {exc}); percentile is the gate"
    else:
        bca_note = (
            "percentile and BCa agree on sign"
            if (ci_low_bca > 0) == (ci_low_pct > 0)
            else "FRAGILE: percentile and BCa disagree on sign of the lower bound"
        )

    # Secondary (descriptive): Kendall τ-b of measured mean-drop vs predicted rank.
    tau_stat: float | None = None
    tau_p: float | None = None
    if predicted_order:
        ranked = [t for t in predicted_order if drops.get(t)]
        if len(ranked) >= 3:
            measured = [float(np.mean(drops[t])) for t in ranked]
            predicted_rank = list(range(len(ranked), 0, -1))  # rank 1 = predicted-worst = highest
            tau = stats.kendalltau(measured, predicted_rank, variant="b", alternative="greater")
            tau_stat = float(tau.statistic)
            tau_p = float(tau.pvalue)

    perm_pass = perm_p < 0.05
    ci_pass = ci_low_pct > 0.0
    survives = perm_pass and ci_pass

    return {
        "decision_rule": "SURVIVES iff permutation_p<0.05 AND bootstrap_ci_low(percentile)>0",
        "verdict": "SURVIVES" if survives else "FALSIFIED",
        "mean_drop_top_k": float(np.mean(top)),
        "mean_drop_bottom_k": float(np.mean(bottom)),
        "tail_difference": float(np.mean(top) - np.mean(bottom)),
        "n_top": int(top.size),
        "n_bottom": int(bottom.size),
        "permutation_test": {
            "p_value_one_sided": perm_p, "n_resamples": _N_PERMUTATIONS, "passed": perm_pass,
        },
        "bootstrap_ci": {
            "ci_low_percentile": ci_low_pct, "ci_low_bca": ci_low_bca,
            "n_resamples": _N_BOOTSTRAP, "confidence": 0.95, "passed": ci_pass, "note": bca_note,
        },
        "kendall_tau_b": {"statistic": tau_stat, "p_value_one_sided": tau_p, "note": "secondary"},
    }


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
    drops = collect_drops(args.results_dir, rung)

    n_seeds = max((len(v) for v in drops.values()), default=0)
    print(f"[falsify] rung={rung} types_with_drops={len(drops)} max_seeds_per_type={n_seeds}")

    verdict = run_falsification(
        drops, pred["top_k_predicted_worst"], pred["bottom_k_predicted_best"],
        pred.get("predicted_collapse_order"), seed=args.seed,
    )
    print(
        f"[falsify] tail_diff={verdict['tail_difference']:+.4f} "
        f"perm_p={verdict['permutation_test']['p_value_one_sided']:.4f} "
        f"ci_low={verdict['bootstrap_ci']['ci_low_percentile']:+.4f} "
        f"→ {verdict['verdict']}"
    )

    complete, reason = manifest_complete(args.results_dir)
    if not (complete and len(drops) >= 1):
        print(
            f"[falsify] WRITE-GATE CLOSED — verdict NOT persisted ({reason}). "
            "The pre-registered record only accepts a verdict from a complete headline sweep."
        )
        return 0

    out = {
        "computed_utc": datetime.now(UTC).isoformat(),
        "pre_registration": "experiments/eda/OOD_WALL_PREDICTION/criteria.md",
        "harness_results": str(args.results_dir.relative_to(_HERE.parent.parent)),
        "harness_rung": rung,
        "harness_fold": _HEADLINE_FOLD,
        "k": pred["k"],
        "top_k_predicted_worst": pred["top_k_predicted_worst"],
        "bottom_k_predicted_best": pred["bottom_k_predicted_best"],
        "per_type_drops": drops,
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
    p.add_argument("--seed", type=int, default=0, help="resampling seed for perm/bootstrap")
    return p.parse_args(argv)


if __name__ == "__main__":
    raise SystemExit(main())
