"""Test-contract: docs/glossary.md exists and has entries.

Per plan §2 Tier-1 anti-pattern firewall: any project-specific term
introduced in code or prose must land in docs/glossary.md in the same
commit. This contract verifies the glossary file exists + has content.

At v0.1.0-pre the glossary has starter entries (Day 3b commit); this
contract passes. Grows stricter as lane work introduces new terms.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GLOSSARY = REPO_ROOT / "docs" / "glossary.md"


@pytest.mark.contract
def test_glossary_file_exists() -> None:
    """docs/glossary.md must exist."""
    assert GLOSSARY.exists(), (
        f"docs/glossary.md not found at {GLOSSARY}. "
        f"Per plan §2 Tier-1 anti-pattern firewall, every project-specific "
        f"term needs a glossary entry."
    )


@pytest.mark.contract
def test_glossary_has_minimum_entries() -> None:
    """Glossary must have at least 5 entries at v0.1.0-pre (grows as project does)."""
    content = GLOSSARY.read_text()
    # Markdown level-2 headings (## Term) are glossary entries
    entries = [line for line in content.splitlines() if line.startswith("## ")]
    assert len(entries) >= 5, (
        f"docs/glossary.md has only {len(entries)} entries; expected >=5 "
        f"at v0.1.0-pre. Add foundational terms (Lane / OOD wall / ADR-NNN / "
        f"Fragment / Guide / etc.)."
    )


@pytest.mark.contract
def test_glossary_entries_have_definitions() -> None:
    """Every level-2 heading must have non-empty body content before the next heading."""
    content = GLOSSARY.read_text()
    lines = content.splitlines()
    issues: list[str] = []
    for i, line in enumerate(lines):
        if not line.startswith("## "):
            continue
        # Find body content until next ## or end of file
        body_lines = []
        j = i + 1
        while j < len(lines) and not lines[j].startswith("## "):
            stripped = lines[j].strip()
            if stripped and not stripped.startswith("#"):
                body_lines.append(stripped)
            j += 1
        if not body_lines:
            issues.append(f"Glossary entry '{line[3:]}' has no definition body")
    assert not issues, f"Glossary entries missing definitions: {issues}"
