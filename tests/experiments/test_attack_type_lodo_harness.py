"""Unit tests for harness helpers — the NotInject over-defense loader (M1).

Target: ``experiments/attack-type-lodo/harness.py``. The loader is best-effort by design
(an unreachable HuggingFace fetch must NOT block a paid sweep), so we verify both the
failure path (empty tuple → explicit ``None`` FPR downstream) and the success path.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_LODO_DIR = Path(__file__).resolve().parent.parent.parent / "experiments" / "attack-type-lodo"
if str(_LODO_DIR) not in sys.path:
    sys.path.insert(0, str(_LODO_DIR))

import harness  # noqa: E402


@pytest.mark.unit
def test_load_notinject_empty_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fetch failure yields an empty tuple (→ explicit None FPR), never a raise."""
    harness._load_notinject.cache_clear()

    def _boom(*_a: object, **_k: object) -> object:
        raise RuntimeError("offline")

    monkeypatch.setattr("datasets.load_dataset", _boom)
    assert harness._load_notinject() == ()
    harness._load_notinject.cache_clear()


@pytest.mark.unit
def test_load_notinject_returns_prompt_tuple(monkeypatch: pytest.MonkeyPatch) -> None:
    """A successful fetch returns the ``prompt`` column as a tuple of strings."""
    harness._load_notinject.cache_clear()

    class _FakeDS:
        def __getitem__(self, key: str) -> list[str]:
            assert key == "prompt"
            return ["benign with trigger one", "benign with trigger two"]

    monkeypatch.setattr("datasets.load_dataset", lambda *_a, **_k: _FakeDS())
    assert harness._load_notinject() == ("benign with trigger one", "benign with trigger two")
    harness._load_notinject.cache_clear()
