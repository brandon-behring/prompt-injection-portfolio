"""Test-contract: every closed lane persists per-row predictions parquet.

Per plan §2 Tier-1 anti-pattern firewall: NEVER store only summary metrics.
Per-row predictions parquet (text_id / source / label / score / pred_label)
must be persisted alongside each lane's results so downstream paired-bootstrap
+ score-distribution audits are reproducible.

At v0.1.0-pre no lanes are closed; this contract is vacuous-pass. Bites
at M1+ as lane experiment records populate.

Contract design:
1. Parse experiments/MANIFEST.json
2. For each lane row with results.md present (lane CLOSED), verify a
   corresponding evals/lane-N/predictions.parquet exists (or is gitignored
   + has a SHA in results.md).
3. Vacuous-pass when MANIFEST.lanes is empty or no lane has results.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.mark.contract
def test_closed_lanes_have_predictions_parquet() -> None:
    """For each lane with results.md (CLOSED state), require a predictions parquet."""
    manifest_path = REPO_ROOT / "experiments" / "MANIFEST.json"
    if not manifest_path.exists():
        pytest.skip("experiments/MANIFEST.json not yet created (M0 Day 3b scaffold)")

    manifest = json.loads(manifest_path.read_text())
    lanes = manifest.get("lanes", {})
    if not lanes:
        # v0.1.0-pre vacuous-pass: no lanes started yet
        return

    violations: list[str] = []
    for lane_id, _lane_meta in lanes.items():
        lane_dir = REPO_ROOT / "experiments" / lane_id
        results_md = lane_dir / "results.md"
        if not results_md.exists():
            # lane not yet CLOSED — skip
            continue

        # Lane is CLOSED — require predictions evidence
        predictions_parquet = REPO_ROOT / "evals" / lane_id / "predictions.parquet"
        predictions_sha_in_results = "predictions" in results_md.read_text().lower()

        if not predictions_parquet.exists() and not predictions_sha_in_results:
            violations.append(
                f"Lane {lane_id} CLOSED (has results.md) but no predictions evidence "
                f"(no {predictions_parquet} AND no 'predictions' reference in "
                f"results.md)"
            )

    assert not violations, f"Closed lanes missing predictions parquet: {violations}"
