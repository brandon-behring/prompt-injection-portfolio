"""Test-contract: no hand-rolled metric implementations in src/ or scripts/.

Per plan §2 Tier-1 (library-first invariant) + Round 10 strengthening:
NEVER hand-roll a primitive that belongs in eval-toolkit. This contract
scans portfolio code for any function definition whose name matches a
known eval_toolkit canonical metric — if found, that's a violation
(should be `from eval_toolkit import scorecard, metric_specs` instead).

At v0.1.0-pre src/ is essentially empty; this contract is vacuous-pass.
Bites as lane code grows at M1+.

Round 20 expansion: also forbids defining SimpleNamespace-style metric
shortcuts removed in eval-toolkit v0.47.0.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

# Canonical eval_toolkit metric symbols (per v0.47.0 + v0.46+ metric_specs).
# Defining a function with one of these names in portfolio's src/ or scripts/
# almost certainly means hand-rolling — should be `from eval_toolkit import ...`.
FORBIDDEN_METRIC_NAMES = frozenset(
    {
        # Threshold-free metrics (top-level removed in v0.47.0; submodule preserved)
        "pr_auc",
        "roc_auc",
        "auprc",
        "auroc",
        "brier_score",
        "brier",
        "expected_calibration_error",
        "expected_calibration_error_equal_mass",
        "expected_calibration_error_debiased",
        "expected_calibration_error_l2",
        "expected_calibration_error_l2_debiased",
        # Threshold-dependent metrics (reach via metrics_at_threshold)
        "metrics_at_threshold",
        # Bootstrap primitives
        "bootstrap_ci",
        "paired_bootstrap",
        # Calibration primitives (v0.40+ canonical family)
        "fit_platt_binary",
        "fit_beta_binary",
        "fit_isotonic_binary",
        "fit_temperature_binary",
    }
)


def _python_files() -> list[Path]:
    """Collect .py files under src/ + scripts/ to scan."""
    root = Path(__file__).resolve().parent.parent.parent
    files: list[Path] = []
    for sub in ("src", "scripts"):
        d = root / sub
        if d.exists():
            files.extend(d.rglob("*.py"))
    return files


@pytest.mark.contract
def test_no_handrolled_metric_function_defs() -> None:
    """No function definition shadows a canonical eval_toolkit metric name."""
    violations: list[tuple[Path, str, int]] = []
    for f in _python_files():
        try:
            tree = ast.parse(f.read_text(), filename=str(f))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                if node.name in FORBIDDEN_METRIC_NAMES:
                    violations.append((f, node.name, node.lineno))
    assert not violations, (
        f"Hand-rolled metric function definitions found (use eval-toolkit "
        f"primitives via `from eval_toolkit import scorecard, metric_specs`): "
        f"{violations}"
    )


@pytest.mark.contract
def test_no_removed_simplenamespace_patterns() -> None:
    """No imports/usages of v0.47-removed SimpleNamespace shortcuts.

    Removed at eval-toolkit v0.47.0:
    - `from eval_toolkit.adversarial import character_injection` (SimpleNamespace)
    - `from eval_toolkit.preprocessing import spotlighting` (SimpleNamespace)
    - Module-level `adversarial.sweep` + `preprocessing.sweep`

    Portfolio code uses 12 dataclasses + top-level `sweep()` per Round 20.
    """
    removed_patterns = [
        re.compile(r"from\s+eval_toolkit\.adversarial\s+import\s+.*character_injection"),
        re.compile(r"from\s+eval_toolkit\.preprocessing\s+import\s+.*spotlighting"),
        re.compile(r"from\s+eval_toolkit\.adversarial\s+import\s+sweep\b"),
        re.compile(r"from\s+eval_toolkit\.preprocessing\s+import\s+sweep\b"),
        # Top-level scalar metric imports removed in v0.47.0:
        re.compile(
            r"from\s+eval_toolkit\s+import\s+.*\b(pr_auc|roc_auc|brier_score|"
            r"expected_calibration_error|auprc|auroc)\b"
        ),
    ]
    violations: list[tuple[Path, int, str]] = []
    for f in _python_files():
        for lineno, line in enumerate(f.read_text().splitlines(), 1):
            for pat in removed_patterns:
                if pat.search(line):
                    violations.append((f, lineno, line.strip()))
    assert not violations, (
        f"Removed v0.47 patterns found (use canonical surfaces per Round 20): {violations}"
    )
