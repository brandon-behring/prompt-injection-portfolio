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

import detectors  # noqa: E402
import falsify_clustered as fc  # noqa: E402
import falsify_ood_wall as fw  # noqa: E402
import folds  # noqa: E402
import harness  # noqa: E402
import reference_scorers as rs  # noqa: E402

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


# ── ADR-054: rebuild_manifest disk-union write-gate + non-gating reference column ──


@pytest.mark.unit
def test_rebuild_manifest_complete_on_required_rungs(tmp_path: Path) -> None:
    """rebuild_manifest opens the gate when the 3 REQUIRED_RUNGS × ≥3 seeds are on disk."""
    levels = ([0.30, 0.33, 0.36, 0.39], [0.60, 0.63, 0.66, 0.69])
    for rung in detectors.REQUIRED_RUNGS:  # tfidf, frozen, lora — the ADR-054 ceiling
        _write_synth(tmp_path, rung, *levels)
    manifest = harness.rebuild_manifest(tmp_path)
    assert manifest["complete_headline_sweep"] is True
    cfg = manifest["config"]
    assert isinstance(cfg, dict)
    assert set(cfg["rungs"]) == set(detectors.REQUIRED_RUNGS)
    ok, _reason = fw.manifest_complete(tmp_path)
    assert ok


@pytest.mark.unit
def test_rebuild_manifest_incomplete_without_lora(tmp_path: Path) -> None:
    """Cheap rungs only (lora absent) → gate CLOSED — the honest local-only state (ADR-054)."""
    levels = ([0.30, 0.33, 0.36, 0.39], [0.60, 0.63, 0.66, 0.69])
    for rung in ("tfidf", "frozen"):
        _write_synth(tmp_path, rung, *levels)
    manifest = harness.rebuild_manifest(tmp_path)
    assert manifest["complete_headline_sweep"] is False
    ok, _reason = fw.manifest_complete(tmp_path)
    assert not ok


@pytest.mark.unit
def test_required_rungs_ceiling_and_full_ft_selectable() -> None:
    """lora is the write-gate ceiling; full_ft is deferred-not-dropped (still runnable). ADR-054."""
    assert detectors.REQUIRED_RUNGS == ("tfidf", "frozen", "lora")
    assert "full_ft" not in detectors.REQUIRED_RUNGS
    assert "full_ft" in detectors.RUNG_NAMES  # selectable for the trigger-gate
    assert detectors.make_detector("full_ft").name == "full_ft"


@pytest.mark.unit
def test_reference_scores_are_non_gating(tmp_path: Path) -> None:
    """reference_*.test_scores.parquet is invisible to the rung scan / write-gate (ADR-054)."""
    levels = ([0.30, 0.33, 0.36, 0.39], [0.60, 0.63, 0.66, 0.69])
    for rung in detectors.REQUIRED_RUNGS:
        _write_synth(tmp_path, rung, *levels)
    ref_dir = tmp_path / "seed=0" / "core_attack_type"
    pd.DataFrame(
        {"text": ["x"], "label": [1], "attack_type": ["w1"], "carrier": ["email"], "y_score": [0.9]}
    ).to_parquet(ref_dir / "reference_protectai_v2.test_scores.parquet", index=False)
    rungs = {a["rung"] for a in harness._scan_artifacts(tmp_path)}
    assert rungs == set(detectors.REQUIRED_RUNGS)  # the reference file is not counted as a rung
    assert harness.rebuild_manifest(tmp_path)["complete_headline_sweep"] is True


@pytest.mark.unit
def test_reference_scorer_skips_gated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A gated/unavailable probe is recorded 'skipped' and writes nothing (never raises)."""
    test_df = pd.DataFrame(
        {
            "text": ["ctx\n\nP", "clean"],
            "label": [1, 0],
            "attack_type": ["w1", ""],
            "carrier": ["email", "email"],
        }
    )
    fold = folds.Fold(
        name="core_attack_type", train=test_df, val=test_df, test=test_df, test_types=("w1",)
    )

    def _fake_make_fold(*_a: object, **_k: object) -> folds.Fold:
        return fold

    def _boom(*_a: object, **_k: object) -> object:
        raise OSError("403 gated repo")

    monkeypatch.setattr(folds, "make_fold", _fake_make_fold)
    monkeypatch.setattr(rs, "score_texts", _boom)
    records = rs.score_fold(
        test_df,
        "core_attack_type",
        seed=0,
        probes={"prompt_guard_1": "meta-llama/Prompt-Guard-86M"},
        out_dir=tmp_path,
    )
    assert records["prompt_guard_1"]["status"] == "skipped"
    assert not list(tmp_path.glob("**/*.test_scores.parquet"))
