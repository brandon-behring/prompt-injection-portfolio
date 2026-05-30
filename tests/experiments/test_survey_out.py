"""Unit tests for ``survey_run.py --out`` per-invocation output paths.

Target: ``experiments/eda/survey_run.py``. Verifies that ``--out`` writes the
survey JSON to the requested path and that two invocations with distinct
``--out`` paths persist independently — the collision-free property that lets
the ``dataset-auditor`` subagent fan out one dataset per process (the prior
single shared ``survey_summary.json`` would have clobbered under parallelism).

The tests pass an unknown bibkey so the target set is empty: no dataset is
downloaded and no tokenizer is loaded, so only the output-path plumbing is
exercised (fast, offline, deterministic).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_EDA_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "eda"
if str(_EDA_DIR) not in sys.path:
    sys.path.insert(0, str(_EDA_DIR))

import survey_run as sr  # noqa: E402

_UNKNOWN = "__not_a_real_bibkey__"


@pytest.mark.unit
def test_out_writes_to_given_path(tmp_path: Path) -> None:
    """``--out`` creates parent dirs and writes the records JSON there (no datasets)."""
    out = tmp_path / "nested" / "survey.json"
    rc = sr.main([_UNKNOWN, "--out", str(out)])
    assert rc == 0
    assert out.exists()
    assert json.loads(out.read_text()) == []


@pytest.mark.unit
def test_distinct_out_paths_do_not_collide(tmp_path: Path) -> None:
    """Two invocations with different ``--out`` persist independently (parallel-safe)."""
    a = tmp_path / "a.json"
    b = tmp_path / "b.json"
    assert sr.main([_UNKNOWN, "--out", str(a)]) == 0
    assert sr.main([_UNKNOWN, "--out", str(b)]) == 0
    assert a.exists() and b.exists()
    assert json.loads(a.read_text()) == []
    assert json.loads(b.read_text()) == []


@pytest.mark.unit
def test_out_rejects_directory(tmp_path: Path) -> None:
    """A directory ``--out`` is an explicit error, not a silent failure."""
    with pytest.raises(ValueError, match="must be a file path"):
        sr.main([_UNKNOWN, "--out", str(tmp_path)])
