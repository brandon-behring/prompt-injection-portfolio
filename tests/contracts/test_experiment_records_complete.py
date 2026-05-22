"""Test-contract: every lane has 4-file experiment record + 3 book fragments.

Per plan §18 + Round 17 follow-up Q2: each lane in experiments/MANIFEST.json
must have:

Experiment record (4 files):
- hypothesis.md (skeleton at lane START)
- protocol.md (skeleton at lane START)
- results.md (retrospective at lane CLOSE)
- decisions.md (retrospective at lane CLOSE)

Book fragments (3 files; shared substrate per Round 17 Q2):
- book/src/content/fragments/lane-N/methodology.mdx
- book/src/content/fragments/lane-N/results.mdx
- book/src/content/fragments/lane-N/interpretation.mdx

At v0.1.0-pre MANIFEST.lanes is empty; this contract is vacuous-pass.
Bites at M1+ as lanes open + lane-record skeletons populate.

State semantics:
- Lane STARTED (hypothesis.md + protocol.md present): enforce those 2 files.
- Lane CLOSED (results.md + decisions.md also present): enforce all 4 +
  all 3 fragments.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
MANIFEST = REPO_ROOT / "experiments" / "MANIFEST.json"


@pytest.mark.contract
def test_manifest_exists_and_well_formed() -> None:
    """experiments/MANIFEST.json must exist + parse as JSON with 'lanes' dict."""
    assert MANIFEST.exists(), f"experiments/MANIFEST.json not found at {MANIFEST}"
    data = json.loads(MANIFEST.read_text())
    assert isinstance(data, dict), "MANIFEST.json must be a JSON object"
    assert "lanes" in data, "MANIFEST.json missing 'lanes' key"
    assert isinstance(data["lanes"], dict), "MANIFEST.json 'lanes' must be an object"


@pytest.mark.contract
def test_each_lane_has_complete_records() -> None:
    """For each lane in MANIFEST, verify required record files + fragments exist."""
    data = json.loads(MANIFEST.read_text())
    lanes = data.get("lanes", {})

    violations: list[str] = []
    for lane_id, _lane_meta in lanes.items():
        lane_dir = REPO_ROOT / "experiments" / lane_id
        if not lane_dir.exists():
            violations.append(f"Lane {lane_id} listed in MANIFEST but dir missing")
            continue

        # Lane STARTED (hypothesis.md + protocol.md required at lane open)
        for required in ("hypothesis.md", "protocol.md"):
            file_path = lane_dir / required
            if not file_path.exists():
                violations.append(f"Lane {lane_id} missing {required} (lane START state)")
                continue
            if not file_path.read_text().strip():
                violations.append(f"Lane {lane_id} {required} is empty")

        # Lane CLOSED — if results.md present, require decisions.md + 3 fragments
        results_md = lane_dir / "results.md"
        if results_md.exists():
            decisions_md = lane_dir / "decisions.md"
            if not decisions_md.exists():
                violations.append(
                    f"Lane {lane_id} has results.md but missing decisions.md (lane CLOSED state)"
                )

            # Round 17 Q2 fragment-completeness extension
            fragments_dir = REPO_ROOT / "book" / "src" / "content" / "fragments" / lane_id
            for fragment in ("methodology.mdx", "results.mdx", "interpretation.mdx"):
                fragment_path = fragments_dir / fragment
                if not fragment_path.exists():
                    violations.append(
                        f"Lane {lane_id} CLOSED but missing book fragment "
                        f"{fragment_path} (per Round 17 follow-up Q2)"
                    )
                elif not fragment_path.read_text().strip():
                    violations.append(f"Lane {lane_id} fragment {fragment} is empty")

    assert not violations, f"Experiment record completeness violations: {violations}"
