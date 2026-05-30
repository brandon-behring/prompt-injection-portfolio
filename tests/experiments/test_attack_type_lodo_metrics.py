"""Unit tests for the attack-type-LODO metrics (``experiments/attack-type-lodo/metrics.py``).

Verifies the corrected ``eval_toolkit.scorecard`` usage (the bug the prior session
left unfixed): the headline battery returns finite AUPRC with a real bootstrap CI, a
single-class slice yields ``status="skipped"`` instead of crashing, non-finite CIs are
persisted as ``None`` (strict-JSON-safe), and the per-type val→test drop math is correct.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_LODO_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import metrics  # noqa: E402


@pytest.fixture
def separable() -> tuple[np.ndarray, np.ndarray]:
    """A discriminative (labels, scores) slice: positives score higher than negatives."""
    rng = np.random.default_rng(0)
    y = np.concatenate([np.zeros(60, dtype=int), np.ones(40, dtype=int)])
    s = y * 0.6 + rng.uniform(0, 0.5, size=100)
    return y, s


@pytest.mark.unit
def test_compute_fold_metrics_battery_keys(separable: tuple[np.ndarray, np.ndarray]) -> None:
    """The headline battery carries AUPRC/AUROC/Brier/ECE + floor + TPR@FPR."""
    y, s = separable
    m = metrics.compute_fold_metrics(y, s, n_bootstrap=200, seed=0)
    assert {"pr_auc", "roc_auc", "brier"} <= set(m)
    assert any(k.startswith("ece_n_bins_15") for k in m)  # exact parameterized key
    assert m["prevalence_floor"] == pytest.approx(0.4)
    assert set(m["tpr_at_fpr"]) == set(metrics.FPR_TARGETS)


@pytest.mark.unit
def test_auprc_finite_and_above_floor(separable: tuple[np.ndarray, np.ndarray]) -> None:
    """A discriminative slice yields a finite AUPRC with status ok, above the prevalence floor."""
    y, s = separable
    cell = metrics.compute_fold_metrics(y, s, n_bootstrap=200, seed=0)["pr_auc"]
    assert cell["status"] == "ok"
    assert cell["value"] is not None and math.isfinite(cell["value"])
    assert cell["value"] > 0.4  # beats random


@pytest.mark.unit
def test_single_class_slice_skipped_not_crash() -> None:
    """A single-class slice records status=skipped (value None) rather than raising."""
    rng = np.random.default_rng(1)
    y = np.zeros(40, dtype=int)
    s = rng.uniform(0, 1, size=40)
    cell = metrics.compute_fold_metrics(y, s, n_bootstrap=0)["pr_auc"]
    assert cell["status"] == "skipped"
    assert cell["value"] is None


@pytest.mark.unit
def test_cells_are_strict_json_safe(separable: tuple[np.ndarray, np.ndarray]) -> None:
    """All metric cells serialize under json.dumps(allow_nan=False) — no NaN leaks through."""
    y, s = separable
    m = metrics.compute_fold_metrics(y, s, n_bootstrap=200, seed=0)
    json.dumps(m, allow_nan=False)  # raises ValueError if any NaN/Inf survives


@pytest.mark.unit
def test_per_type_drop_math() -> None:
    """The per-type drop equals val_auprc − one-vs-rest test AUPRC for that type."""
    # Two test types: 't_easy' perfectly separated, 't_hard' inverted.
    rows = []
    for k in range(10):
        rows.append({"label": 0, "attack_type": "", "text": f"neg{k}"})
    for k in range(10):
        rows.append({"label": 1, "attack_type": "t_easy", "text": f"easy{k}"})
    for k in range(10):
        rows.append({"label": 1, "attack_type": "t_hard", "text": f"hard{k}"})
    df = pd.DataFrame(rows)
    scores = np.concatenate(
        [
            np.full(10, 0.1),  # negatives: low
            np.linspace(0.8, 0.99, 10),  # t_easy positives: high → easy
            np.full(10, 0.05),  # t_hard positives: lower than negatives → hard
        ]
    )
    out = metrics.per_type_diagnostics(df, scores, ["t_easy", "t_hard"], val_auprc=0.9)
    assert out["t_easy"]["test_auprc"] > out["t_hard"]["test_auprc"]
    for t in ("t_easy", "t_hard"):
        assert out[t]["drop"] == pytest.approx(0.9 - out[t]["test_auprc"])
    assert out["t_easy"]["n_pos"] == 10
    assert out["t_easy"]["n_total"] == 20  # 10 type-positives + 10 shared negatives


@pytest.mark.unit
def test_per_type_insufficient_items_records_none() -> None:
    """A type with too few scored rows / single class records None (merge policy handles it)."""
    df = pd.DataFrame({"label": [0, 1], "attack_type": ["", "rare"], "text": ["n", "p"]})
    scores = np.array([0.2, 0.8])
    out = metrics.per_type_diagnostics(df, scores, ["rare"], val_auprc=0.9, min_items=10)
    assert out["rare"]["test_auprc"] is None
    assert out["rare"]["drop"] is None


@pytest.mark.unit
def test_benign_fpr_threshold() -> None:
    """benign_fpr is the fraction of benign scores at or above the threshold; None when empty."""
    assert metrics.benign_fpr(np.array([0.1, 0.6, 0.9]), threshold=0.5) == pytest.approx(2 / 3)
    assert metrics.benign_fpr(np.array([]), threshold=0.5) is None
