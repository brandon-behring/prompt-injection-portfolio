"""Test-contract: every upstream library import is registered in library_imports.md.

Per plan §2 Tier-1 library-first invariant + Round 10 strengthening: every
primitive imported from a Python load-bearing library (eval-toolkit /
runpod-deploy) must appear as a row in `decisions/library_imports.md`. Adding
a new upstream import without registering it fails this contract.

research_toolkit is consumed as TOOLING — the dossier-audit validators + Claude
skills, via a repo-local pinned clone (ADR-051) — not a Python import, so it is
not scanned here. book-scaffold-astro is an npm package (book/), likewise not scanned.

At v0.1.0-pre src/ has only `__init__.py` (no upstream imports yet); this
contract is vacuous-pass. Bites at M1+ when lane code starts importing.

Round 20 expansion: scans for v0.47 canonical surface imports specifically.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LIBRARY_IMPORTS = REPO_ROOT / "decisions" / "library_imports.md"

# research_toolkit dropped: consumed as a tooling clone, not a Python import (ADR-051).
LOAD_BEARING_LIBS = ("eval_toolkit", "runpod_deploy")


def _python_files() -> list[Path]:
    """Collect .py files under src/ + scripts/ to scan."""
    files: list[Path] = []
    for sub in ("src", "scripts"):
        d = REPO_ROOT / sub
        if d.exists():
            files.extend(d.rglob("*.py"))
    return files


def _extract_imports(file_path: Path) -> set[str]:
    """Extract `from eval_toolkit.X import Y` or `from eval_toolkit import Y` symbols."""
    imports: set[str] = set()
    pattern = re.compile(
        r"^\s*from\s+(eval_toolkit|runpod_deploy)"
        r"(?:\.\w+(?:\.\w+)*)?\s+import\s+(.+?)(?:\s+as\s+\w+)?$",
        re.MULTILINE,
    )
    for match in pattern.finditer(file_path.read_text()):
        # Parse the imported names (handle commas + parens)
        names_str = match.group(2)
        # Strip surrounding parens for multi-line imports
        names_str = names_str.strip("() ").replace("\n", " ")
        for name in names_str.split(","):
            name = name.strip().split(" as ")[0].strip()
            if name and not name.startswith("#"):
                imports.add(name)
    return imports


@pytest.mark.contract
def test_library_imports_file_exists() -> None:
    """decisions/library_imports.md must exist."""
    assert LIBRARY_IMPORTS.exists(), (
        f"decisions/library_imports.md not found at {LIBRARY_IMPORTS}. "
        f"Per Round 10 library-first invariant + ADR-026, this registry is "
        f"mandatory."
    )


@pytest.mark.contract
def test_all_upstream_imports_registered() -> None:
    """Every upstream-library import in src/ + scripts/ appears in library_imports.md."""
    registry_text = LIBRARY_IMPORTS.read_text() if LIBRARY_IMPORTS.exists() else ""

    unregistered: list[tuple[Path, str]] = []
    for f in _python_files():
        imports = _extract_imports(f)
        for imp in imports:
            # The registry uses backtick-wrapped symbol names; check for substring
            if imp not in registry_text:
                unregistered.append((f, imp))

    assert not unregistered, (
        f"Upstream imports not registered in decisions/library_imports.md "
        f"(per Round 10 library-first invariant): {unregistered}"
    )
