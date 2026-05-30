"""Unit tests for the §6.5 falsification runner.

Target: ``experiments/attack-type-lodo/falsify_ood_wall.py``. Verifies the FIXED
decision-rule logic on synthetic drops (clear top-k>bottom-k → SURVIVES; no
separation → FALSIFIED), the fold-size merge policy, and — the critical safety
property — that the write-gate refuses to persist a verdict from an incomplete sweep.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_LODO_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import falsify_ood_wall as fw  # noqa: E402

_TOP = ["t1", "t2", "t3", "t4"]
_BOTTOM = ["b1", "b2", "b3", "b4"]


def _drops(top_val: float, bottom_val: float, n: int = 4) -> dict[str, list[float]]:
    """Synthetic per-type drops: each top/bottom type gets ``n`` slightly-jittered seeds."""
    out: dict[str, list[float]] = {}
    for i, t in enumerate(_TOP):
        out[t] = [top_val + 0.01 * j + 0.001 * i for j in range(n)]
    for i, b in enumerate(_BOTTOM):
        out[b] = [bottom_val + 0.01 * j + 0.001 * i for j in range(n)]
    return out


@pytest.mark.unit
def test_clear_separation_survives() -> None:
    """Top-k collapsing markedly more than bottom-k → SURVIVES (p<0.05 AND CI_low>0)."""
    verdict = fw.run_falsification(_drops(0.40, 0.02), _TOP, _BOTTOM, [*_TOP, *_BOTTOM], seed=0)
    assert verdict["verdict"] == "SURVIVES"
    assert verdict["permutation_test"]["passed"]
    assert verdict["bootstrap_ci"]["passed"]
    assert verdict["tail_difference"] > 0


@pytest.mark.unit
def test_no_separation_falsified() -> None:
    """Top-k and bottom-k drawn from the same level → FALSIFIED."""
    verdict = fw.run_falsification(_drops(0.20, 0.20), _TOP, _BOTTOM, [*_TOP, *_BOTTOM], seed=0)
    assert verdict["verdict"] == "FALSIFIED"


@pytest.mark.unit
def test_reversed_separation_falsified() -> None:
    """Bottom-k collapsing more than top-k (wrong direction) → FALSIFIED."""
    verdict = fw.run_falsification(_drops(0.02, 0.40), _TOP, _BOTTOM, [*_TOP, *_BOTTOM], seed=0)
    assert verdict["verdict"] == "FALSIFIED"
    assert verdict["tail_difference"] < 0


@pytest.mark.unit
def test_empty_tail_raises() -> None:
    """A tail with no scored drops makes the contrast undefined → ValueError."""
    with pytest.raises(ValueError, match="empty tail"):
        fw.run_falsification({"t1": [0.3]}, _TOP, _BOTTOM, None, seed=0)


@pytest.mark.unit
def test_fold_size_policy_excludes_small_types(tmp_path: Path) -> None:
    """collect_drops drops per-type cells with n_total < the fold-size floor."""
    import json

    seed_dir = tmp_path / "seed=0" / "core_attack_type"
    seed_dir.mkdir(parents=True)
    rec = {
        "per_type": {
            "big": {"drop": 0.3, "n_total": 50},
            "small": {"drop": 0.9, "n_total": 4},  # below _MIN_ITEMS → excluded
            "missing": {"drop": None, "n_total": 50},  # None drop → excluded
        }
    }
    (seed_dir / "tfidf.metrics.json").write_text(json.dumps(rec))
    drops = fw.collect_drops(tmp_path, "tfidf")
    assert "big" in drops and drops["big"] == [0.3]
    assert "small" not in drops
    assert "missing" not in drops


@pytest.mark.unit
def test_write_gate_closed_on_incomplete_sweep(tmp_path: Path) -> None:
    """manifest_complete returns False when the sweep is partial (the write-gate signal)."""
    import yaml

    # No manifest at all.
    ok, reason = fw.manifest_complete(tmp_path)
    assert not ok and "MANIFEST" in reason

    # Manifest present but flagged incomplete.
    (tmp_path / "MANIFEST.yml").write_text(
        yaml.safe_dump({"complete_headline_sweep": False, "config": {"seeds": [0]}})
    )
    ok, reason = fw.manifest_complete(tmp_path)
    assert not ok


@pytest.mark.unit
def test_write_gate_open_on_complete_sweep(tmp_path: Path) -> None:
    """manifest_complete returns True only for a complete ≥3-seed headline sweep."""
    import yaml

    (tmp_path / "MANIFEST.yml").write_text(
        yaml.safe_dump({"complete_headline_sweep": True, "config": {"seeds": [0, 1, 2]}})
    )
    ok, _reason = fw.manifest_complete(tmp_path)
    assert ok
