"""Test-contract: pyproject.toml has [tool.mypy] strict block.

Per plan §2 Tier-4 quality gate: mypy --strict is required across src/ +
scripts/ + tests/. This contract verifies the configuration block exists
in pyproject.toml. Actual mypy execution is covered by the CI workflow's
mypy step (which becomes a hard gate after Day 3b allow-failure shell
removal).

At v0.1.0-pre the strict block is configured per Day 2 pyproject scaffold;
this contract passes.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PYPROJECT = REPO_ROOT / "pyproject.toml"


@pytest.mark.contract
def test_pyproject_has_mypy_strict_block() -> None:
    """pyproject.toml must declare [tool.mypy] strict = true."""
    assert PYPROJECT.exists(), f"pyproject.toml not found at {PYPROJECT}"
    text = PYPROJECT.read_text()
    assert "[tool.mypy]" in text, "pyproject.toml missing [tool.mypy] block"
    # Strip comments before checking strict = true (false-positive guard)
    code_lines = [line.split("#", 1)[0].strip() for line in text.splitlines()]
    code = "\n".join(code_lines)
    assert "strict = true" in code, (
        "pyproject.toml [tool.mypy] missing `strict = true`. Per plan §2 Tier-4 "
        "quality gate, mypy --strict is mandatory."
    )


@pytest.mark.contract
def test_pyproject_pins_eval_toolkit_v047_floor() -> None:
    """pyproject.toml must pin eval-toolkit >=0.47 per Round 20."""
    text = PYPROJECT.read_text()
    # Match the [probes,losses]>=0.47 pin pattern
    assert "eval-toolkit" in text, "pyproject.toml missing eval-toolkit dep"
    # Either [probes,losses]>=0.47 or just >=0.47 satisfies; reject <0.47
    pinned_v047 = ">=0.47" in text
    assert pinned_v047, (
        "pyproject.toml eval-toolkit pin must be >=0.47 per Round 20 "
        "(canonical v0.47 API surfaces: scorecard + metric_specs + sweep + "
        "TextTransform + 12 dataclasses)."
    )
