"""Unit tests for the carrier-LODO ROC-AUC falsifier (carrier-lodo/criteria.md Revision 1).

Targets ``experiments/attack-type-lodo/falsify_carrier_lodo.py``. Verifies the
persistence-vs-collapse decision logic on synthetic predictions (a clear, persistent gap at lora →
SURVIVES; a gap that dissolves at lora → FALSIFIED; a sub-threshold gap → SMALL-THROUGHOUT), payload
recovery + ``val_roc`` from ``metrics.json``, the missing-``val_roc_auc`` guard, and that the
fast bootstrap ROC matches the eval_toolkit point ROC.

Synthetic design: per (carrier-fold, rung, seed) the positives sit near a target level ``τ``; the
negatives are ~uniform on (0,1), so test ROC-AUC ≈ ``τ`` and ``G = val_roc − τ`` is controllable.
Small per-payload jitter gives the payload-cluster bootstrap non-zero (tight) variance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_LODO_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import falsify_carrier_lodo as fcl  # noqa: E402
import folds  # noqa: E402
import metrics  # noqa: E402


def _write_carrier_results(
    results_dir: Path,
    test_roc_by_rung: dict[str, float],
    *,
    val_roc: float = 0.92,
    seeds: tuple[int, ...] = (0, 1, 2),
    n_payload: int = 30,
    n_ctx: int = 5,
    n_neg: int = 50,
    jitter: float = 0.005,
    write_val_roc: bool = True,
) -> None:
    """Write a synthetic carrier-LODO results tree (3 folds × given rungs × seeds).

    Each rung's positives cluster near ``τ = test_roc_by_rung[rung]`` (so test ROC-AUC ≈ τ); the
    metrics.json carries ``val_roc_auc = val_roc`` → controllable gap ``G = val_roc − τ``.
    """
    rng = np.random.default_rng(0)
    neg_scores = np.linspace(0.001, 0.999, n_neg)
    for fold_name in folds.CARRIER_LODO_FOLDS:
        carrier = fold_name.replace("carrier_lodo_", "")
        for rung, tau in test_roc_by_rung.items():
            for s in seeds:
                rows: list[dict[str, object]] = [
                    {
                        "text": f"clean-{j}",
                        "label": 0,
                        "attack_type": "",
                        "carrier": carrier,
                        "y_score": float(v),
                    }
                    for j, v in enumerate(neg_scores)
                ]
                for p in range(n_payload):
                    level = float(np.clip(tau + jitter * rng.standard_normal(), 0.0, 1.0))
                    for c in range(n_ctx):
                        rows.append(
                            {
                                "text": f"ctx{c}\n\nPAY_{rung}_{p}",
                                "label": 1,
                                "attack_type": f"type{p % 14}",
                                "carrier": carrier,
                                "y_score": level,
                            }
                        )
                d = results_dir / f"seed={s}" / fold_name
                d.mkdir(parents=True, exist_ok=True)
                pd.DataFrame(rows).to_parquet(d / f"{rung}.predictions.parquet", index=False)
                meta: dict[str, object] = {"rung": rung, "fold": fold_name, "seed": s}
                if write_val_roc:
                    meta["val_roc_auc"] = val_roc
                (d / f"{rung}.metrics.json").write_text(json.dumps(meta))


# ── decision logic ────────────────────────────────────────────────────────────


@pytest.mark.unit
def test_persistent_gap_survives(tmp_path: Path) -> None:
    """A clear gap that persists at lora (G≈0.25 ≥ ½·G(frozen)) with CI-low>0 → SURVIVES."""
    _write_carrier_results(tmp_path, {"tfidf": 0.52, "frozen": 0.57, "lora": 0.67}, val_roc=0.92)
    v = fcl.compute_verdict(tmp_path, n_boot=300, seed=0)
    assert v["verdict"] == "SURVIVES"
    assert v["lora"]["G"] > 0 and v["lora"]["ci_low"] > 0
    assert v["lora"]["G"] >= v["lora"]["half_G_frozen"]


@pytest.mark.unit
def test_gap_dissolves_at_lora_falsified(tmp_path: Path) -> None:
    """The gap collapses (even reverses) at lora → CI-low(G(lora)) ≤ 0 → FALSIFIED."""
    _write_carrier_results(tmp_path, {"tfidf": 0.52, "frozen": 0.57, "lora": 0.95}, val_roc=0.92)
    v = fcl.compute_verdict(tmp_path, n_boot=300, seed=0)
    assert v["verdict"] == "FALSIFIED"
    assert v["lora"]["ci_low"] <= 0


@pytest.mark.unit
def test_subthreshold_gap_small_throughout(tmp_path: Path) -> None:
    """A positive but sub-½·G(frozen) lora gap (CI-low>0) → neither SURVIVES nor FALSIFIED."""
    _write_carrier_results(tmp_path, {"tfidf": 0.55, "frozen": 0.72, "lora": 0.86}, val_roc=0.92)
    v = fcl.compute_verdict(tmp_path, n_boot=300, seed=0)
    assert v["verdict"] == "SMALL-THROUGHOUT"
    assert v["lora"]["ci_low"] > 0  # not FALSIFIED
    assert v["lora"]["G"] < v["lora"]["half_G_frozen"]  # not SURVIVES


# ── loader + guards ───────────────────────────────────────────────────────────


@pytest.mark.unit
def test_load_carrier_fold_recovers_payloads_and_val_roc(tmp_path: Path) -> None:
    """load_carrier_fold recovers the payload clusters, negatives, and the val_roc reference."""
    _write_carrier_results(tmp_path, {"tfidf": 0.6}, val_roc=0.9, n_payload=30, n_ctx=5, n_neg=50)
    fold = fcl.load_carrier_fold(tmp_path, "carrier_lodo_email", "tfidf")
    assert fold.seeds == [0, 1, 2]
    assert len(fold.payload_pos[0]) == 30  # 30 payload clusters
    assert fold.neg[0].size == 50
    assert fold.val_roc[0] == pytest.approx(0.9)


@pytest.mark.unit
def test_load_carrier_fold_raises_without_val_roc(tmp_path: Path) -> None:
    """A metrics.json lacking val_roc_auc fails loud (no silent default)."""
    _write_carrier_results(tmp_path, {"tfidf": 0.6}, write_val_roc=False)
    with pytest.raises(KeyError, match="val_roc_auc"):
        fcl.load_carrier_fold(tmp_path, "carrier_lodo_email", "tfidf")


@pytest.mark.unit
def test_roc_auc_fast_matches_eval_toolkit() -> None:
    """The fast Mann-Whitney ROC (bootstrap inner loop) matches the eval_toolkit point ROC."""
    rng = np.random.default_rng(1)
    y = np.array([1] * 20 + [0] * 30)
    s = np.concatenate([rng.normal(0.7, 0.2, 20), rng.normal(0.4, 0.2, 30)])
    assert fcl._roc_auc_fast(y, s) == pytest.approx(metrics.roc_auc_point(y, s), abs=1e-9)
