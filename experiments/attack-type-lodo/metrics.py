"""Metrics for the attack-type-LODO harness (spec §5).

All reported metrics flow through ``eval_toolkit`` — ``scorecard`` + ``metric_specs``
for AUPRC/AUROC/Brier/ECE (with bootstrap CIs) and ``thresholds.recall_at_fpr`` for
TPR@LowFPR — honouring the ``no_handrolled_metrics`` test-contract (no F1/AUC
reimplementation). The per-test-attack-type diagnostic AUPRC and its **val→test drop**
(the §6.5 falsification input) are computed here and persisted by the harness (the
§5 retention pre-commit); they stay diagnostic (per-type N=5), never headline.
"""

from __future__ import annotations

import math
from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
import pandas as pd
from eval_toolkit import MetricResult, metric_specs, scorecard
from eval_toolkit.thresholds import recall_at_fpr

__all__ = [
    "compute_fold_metrics",
    "per_type_diagnostics",
    "benign_fpr",
    "roc_auc_point",
    "FPR_TARGETS",
]

# pr_auc/roc_auc/brier are ready MetricSpec instances; ece is a parameterised builder.
_SPECS = [
    metric_specs.pr_auc,
    metric_specs.roc_auc,
    metric_specs.brier,
    metric_specs.ece(n_bins=15),
]
FPR_TARGETS: tuple[float, ...] = (0.01, 0.005, 0.001)


def _jsafe(x: float | None) -> float | None:
    """``float`` or ``None`` — mapping ``NaN`` to ``None`` (invalid-JSON guard).

    A BCa bootstrap CI legitimately degenerates to ``NaN`` on near-separable / small
    slices (eval_toolkit warns and returns ``NaN`` rather than raising). ``NaN`` is not
    valid JSON and a degenerate CI is honestly "uncomputable", so it is persisted as
    ``None`` — never as a silent ``NaN`` that downstream readers would mistake for a value.
    """
    return None if x is None or math.isnan(x) else float(x)


def _cell(m: MetricResult) -> dict[str, object]:
    """Serialise a ``MetricResult`` to a JSON-safe ``{value, ci_low, ci_high, status}`` cell.

    All three numbers are ``None`` when the metric is skipped (single-class slice),
    errored, or carries no (or a degenerate) bootstrap CI; ``status`` is retained so a
    skipped/errored cell is explicit rather than a silent null (no-silent-failure rule).
    """
    ci = m.ci
    return {
        "value": _jsafe(m.value),
        "ci_low": None if ci is None else _jsafe(ci.ci_low),
        "ci_high": None if ci is None else _jsafe(ci.ci_high),
        "status": m.status,
    }


def _pr_auc(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Single AUPRC via ``scorecard`` (no bootstrap) — the per-type diagnostic scalar."""
    cell = scorecard(y_true, y_score, metrics=[metric_specs.pr_auc], bootstrap=False)["pr_auc"]
    if cell.value is None:
        raise ValueError(f"pr_auc undefined on slice (status={cell.status}: {cell.reason})")
    return float(cell.value)


def roc_auc_point(y_true: npt.ArrayLike, y_score: npt.ArrayLike) -> float:
    """Single AUROC via ``scorecard`` (no bootstrap) — the carrier-LODO val→test gap reference.

    ROC-AUC is prevalence-invariant, so it is the carrier-LODO estimator's basis (the BIPIA carriers
    are 83-94 % positive; ``experiments/carrier-lodo/criteria.md`` Revision 1). Raises on a
    single-class slice (no silent ``None``).
    """
    cell = scorecard(
        np.asarray(y_true), np.asarray(y_score), metrics=[metric_specs.roc_auc], bootstrap=False
    )["roc_auc"]
    if cell.value is None:
        raise ValueError(f"roc_auc undefined on slice (status={cell.status}: {cell.reason})")
    return float(cell.value)


def compute_fold_metrics(
    y_true: npt.ArrayLike,
    y_score: npt.ArrayLike,
    *,
    n_bootstrap: int = 1000,
    seed: int = 0,
) -> dict[str, object]:
    """Headline fold metrics (spec §5): AUPRC[CI] / AUROC / Brier / ECE + floor + TPR@LowFPR.

    Parameters
    ----------
    y_true, y_score : sequence
        Binary labels and P(positive) scores for the fold's test rows.
    n_bootstrap : int
        Bootstrap resamples for the scorecard CIs (0 = no CI).
    seed : int
        Bootstrap seed.

    Returns
    -------
    dict
        ``{<metric>: {value, ci_low, ci_high}, "prevalence_floor": float,
        "tpr_at_fpr": {fpr: tpr}}``.
    """
    yt = np.asarray(y_true)
    ys = np.asarray(y_score)
    do_boot = n_bootstrap > 0
    res = scorecard(
        yt,
        ys,
        metrics=_SPECS,
        bootstrap=do_boot,
        n_resamples=n_bootstrap if do_boot else 1000,
        rng=seed,
    )
    out: dict[str, object] = {name: _cell(m) for name, m in res.items()}
    out["prevalence_floor"] = float(np.mean(yt == 1))
    out["tpr_at_fpr"] = {f: float(recall_at_fpr(yt, ys, f).recall) for f in FPR_TARGETS}
    return out


def benign_fpr(benign_scores: npt.ArrayLike, *, threshold: float = 0.5) -> float | None:
    """FPR on a benign-only slice: fraction scored ≥ ``threshold``.

    Single-class slice ⇒ a val-fixed-threshold FPR only (submission ADR-027); pass the
    val-derived threshold from the harness. Used for both the clean-context and the
    NotInject over-defense slices (the harness records each). Returns ``None`` if empty.
    """
    arr = np.asarray(benign_scores)
    return None if arr.size == 0 else float(np.mean(arr >= threshold))


def per_type_diagnostics(
    test_df: pd.DataFrame,
    test_scores: npt.ArrayLike,
    test_types: Sequence[str],
    *,
    val_auprc: float,
    min_items: int = 2,
) -> dict[str, dict[str, object]]:
    """Per-test-attack-type AUPRC + val→test drop (spec §5 retention; §6.5 input).

    For each held-out test-type ``t``, AUPRC is computed one-vs-rest (that type's
    positives vs **all** test negatives); the drop is ``val_auprc - test_auprc[t]``
    (in-distribution reference minus per-type LODO). Types with a single class present
    or fewer than ``min_items`` scored rows record ``None`` (the falsification runner
    applies the fold-size/merge policy).

    Returns
    -------
    dict
        ``{type: {test_auprc, drop, n_pos, n_total}}``.
    """
    labels = test_df["label"].to_numpy()
    atypes = test_df["attack_type"].to_numpy()
    scores = np.asarray(test_scores)
    neg_mask = labels == 0
    out: dict[str, dict[str, object]] = {}
    for t in test_types:
        pos_mask = (labels == 1) & (atypes == t)
        sel = pos_mask | neg_mask
        y = labels[sel]
        s = scores[sel]
        n_total = int(sel.sum())
        if n_total < min_items or len(np.unique(y)) < 2:
            out[t] = {
                "test_auprc": None,
                "drop": None,
                "n_pos": int(pos_mask.sum()),
                "n_total": n_total,
            }
            continue
        auprc = _pr_auc(y, s)
        out[t] = {
            "test_auprc": auprc,
            "drop": float(val_auprc - auprc),
            "n_pos": int(pos_mask.sum()),
            "n_total": n_total,
        }
    return out
