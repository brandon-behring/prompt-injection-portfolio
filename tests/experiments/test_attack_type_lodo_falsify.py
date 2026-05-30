"""Unit tests for the §6.5 payload-clustered falsification (criteria.md Revision 1).

Targets ``experiments/attack-type-lodo/{falsify_clustered,falsify_ood_wall}.py``. Verifies
the honest-unit decision logic on synthetic predictions (clear top-k<bottom-k AUPRC →
SURVIVES at the permutation floor; no separation / reversed → FALSIFIED), payload recovery
+ cluster structure, the missing-tail guard, and — the critical safety property — that the
write-gate refuses to persist a verdict from an incomplete sweep.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_LODO_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import falsify_clustered as fc  # noqa: E402
import falsify_ood_wall as fw  # noqa: E402

_TOP = ["w1", "w2", "w3", "w4"]  # predicted-worst (lower AUPRC expected)
_BOTTOM = ["b1", "b2", "b3", "b4"]  # predicted-best (higher AUPRC expected)
_ORDER = [*_TOP, *_BOTTOM]


def _write_synth(
    results_dir: Path,
    rung: str,
    top_levels: list[float],
    bottom_levels: list[float],
    *,
    seeds: tuple[int, ...] = (0, 1, 2),
    n_payload: int = 5,
    n_ctx: int = 4,
    n_neg: int = 40,
) -> None:
    """Write synthetic ``predictions.parquet`` per seed: 5 payloads/type, tight clusters.

    A type's positive scores sit near its ``level`` (higher ⇒ higher one-vs-rest AUPRC);
    negatives are spread across ``[0, 0.95]``. The injection template ``{ctx}\\n\\n{payload}``
    is what ``load_clusters`` inverts to recover the payload cluster.
    """
    typed_levels = list(zip(_TOP, top_levels, strict=True)) + list(
        zip(_BOTTOM, bottom_levels, strict=True)
    )
    neg_scores = np.linspace(0.0, 0.95, n_neg)
    for s in seeds:
        rows: list[dict[str, object]] = [
            {"text": f"clean ctx {j}", "label": 0, "attack_type": "", "y_score": float(v)}
            for j, v in enumerate(neg_scores)
        ]
        for atype, level in typed_levels:
            for pidx in range(n_payload):
                payload = f"PAYLOAD_{atype}_{pidx}"
                for c in range(n_ctx):
                    rows.append(
                        {
                            "text": f"ctx-{c}\n\n{payload}",
                            "label": 1,
                            "attack_type": atype,
                            "y_score": float(level + 0.01 * pidx + 0.001 * c),
                        }
                    )
        d = results_dir / f"seed={s}" / "core_attack_type"
        d.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_parquet(d / f"{rung}.predictions.parquet", index=False)


# ── decision logic on synthetic predictions ──────────────────────────────────


@pytest.mark.unit
def test_clear_separation_survives_at_permutation_floor(tmp_path: Path) -> None:
    """Best-tail AUPRC strictly above worst-tail → perfect separation → SURVIVES, perm p=1/70."""
    _write_synth(tmp_path, "tfidf", [0.30, 0.33, 0.36, 0.39], [0.60, 0.63, 0.66, 0.69])
    v = fc.compute_verdict(tmp_path, "tfidf", _TOP, _BOTTOM, _ORDER, n_boot=400, seed=0)
    assert v["verdict"] == "SURVIVES"
    assert v["statistic_T"] > 0
    assert v["permutation"]["passed"] and v["bootstrap"]["passed"]
    # perfect tail separation ⇒ the predicted split is the unique most-extreme of C(8,4)=70.
    assert v["permutation"]["p_one_sided"] == pytest.approx(1.0 / 70.0, abs=1e-9)
    assert v["bootstrap"]["frac_gt0"] == pytest.approx(1.0, abs=1e-9)


@pytest.mark.unit
def test_no_separation_falsified(tmp_path: Path) -> None:
    """All types at the same level → no ordering → FALSIFIED."""
    flat = [0.50, 0.50, 0.50, 0.50]
    _write_synth(tmp_path, "tfidf", flat, flat)
    v = fc.compute_verdict(tmp_path, "tfidf", _TOP, _BOTTOM, _ORDER, n_boot=400, seed=0)
    assert v["verdict"] == "FALSIFIED"
    assert not v["permutation"]["passed"]


@pytest.mark.unit
def test_reversed_separation_falsified(tmp_path: Path) -> None:
    """Worst-tail detected *better* than best-tail (wrong direction) → FALSIFIED, T<0."""
    _write_synth(tmp_path, "tfidf", [0.60, 0.63, 0.66, 0.69], [0.30, 0.33, 0.36, 0.39])
    v = fc.compute_verdict(tmp_path, "tfidf", _TOP, _BOTTOM, _ORDER, n_boot=400, seed=0)
    assert v["verdict"] == "FALSIFIED"
    assert v["statistic_T"] < 0


@pytest.mark.unit
def test_missing_tail_type_raises(tmp_path: Path) -> None:
    """A predicted tail type absent from the results makes the contrast undefined → ValueError."""
    _write_synth(tmp_path, "tfidf", [0.30, 0.33, 0.36, 0.39], [0.60, 0.63, 0.66, 0.69])
    with pytest.raises(ValueError, match="tail types absent"):
        fc.compute_verdict(tmp_path, "tfidf", _TOP, [*_BOTTOM, "ghost"], _ORDER, n_boot=50)


# ── permutation unit (no parquet) ────────────────────────────────────────────


@pytest.mark.unit
def test_permutation_exact_floor_and_resolution() -> None:
    """Perfect separation → p=1/70 (the floor); interleaved → p>0.05 (k=4 has no resolution)."""
    perfect = {
        **{t: 0.3 + 0.01 * i for i, t in enumerate(_TOP)},
        **{t: 0.7 + 0.01 * i for i, t in enumerate(_BOTTOM)},
    }
    p, n = fc.permutation_exact(perfect, _TOP, _BOTTOM)
    assert n == 70 and p == pytest.approx(1.0 / 70.0, abs=1e-9)

    interleaved = {
        "w1": 0.4,
        "w2": 0.8,
        "w3": 0.5,
        "w4": 0.9,
        "b1": 0.45,
        "b2": 0.85,
        "b3": 0.55,
        "b4": 0.6,
    }
    p2, _ = fc.permutation_exact(interleaved, _TOP, _BOTTOM)
    assert p2 > 0.05


# ── cluster loading ──────────────────────────────────────────────────────────


@pytest.mark.unit
def test_load_clusters_recovers_payloads(tmp_path: Path) -> None:
    """load_clusters recovers 5 payload clusters/type from the injection template + the neg pool."""
    _write_synth(tmp_path, "tfidf", [0.30, 0.33, 0.36, 0.39], [0.60, 0.63, 0.66, 0.69])
    pos, neg, seeds = fc.load_clusters(tmp_path, "tfidf")
    assert seeds == [0, 1, 2]
    assert set(pos[0]) == set(_TOP) | set(_BOTTOM)
    assert all(len(pos[0][t]) == 5 for t in pos[0])  # 5 payload clusters per type
    assert neg[0].size == 40


# ── write-gate (unchanged safety property) ───────────────────────────────────


@pytest.mark.unit
def test_write_gate_closed_on_incomplete_sweep(tmp_path: Path) -> None:
    """manifest_complete returns False when the sweep is partial (the write-gate signal)."""
    import yaml

    ok, reason = fw.manifest_complete(tmp_path)
    assert not ok and "MANIFEST" in reason

    (tmp_path / "MANIFEST.yml").write_text(
        yaml.safe_dump({"complete_headline_sweep": False, "config": {"seeds": [0]}})
    )
    ok, _reason = fw.manifest_complete(tmp_path)
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
