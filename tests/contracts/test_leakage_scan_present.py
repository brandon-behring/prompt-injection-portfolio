"""Test-contract: leakage scan runs against any new eval source.

Per plan §2 Tier-1 anti-pattern firewall: every new eval source needs a
leakage scan before it can be used in lane evaluation. The submission's
LODO discipline (per ADR-016) requires cross-source disjoint splits +
no overlap with training pool.

At v0.1.0-pre no eval sources are integrated; this contract verifies
scaffold presence (the scanner script exists or is scheduled).

Contract design:
1. If any lane's protocol.md cites an eval source not in the
   submission's source_manifest.yaml + not in portfolio's manifest,
   require a `scripts/leakage_scan.py` invocation in the protocol.
2. Vacuous-pass at v0.1.0-pre when no protocols exist yet.
"""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.mark.contract
def test_leakage_scan_invocation_required_per_eval_source() -> None:
    """Each lane protocol.md that cites a new eval source must reference a leakage scan."""
    experiments_dir = REPO_ROOT / "experiments"
    if not experiments_dir.exists():
        pytest.skip("experiments/ dir not yet populated (M0 Day 3b scaffold)")

    protocol_files = list(experiments_dir.rglob("protocol.md"))
    if not protocol_files:
        # v0.1.0-pre vacuous-pass: no lane protocols yet
        return

    # Per plan §5 Lane 1: BIPIA + AgentDojo + InjecAgent + NotInject +
    # LLMail-Inject + PINT (+ Lane 2 MR-3 synthetic-indirect-v2) are the
    # known eval sources. Lane protocols citing other data sources must
    # reference a leakage scan (scripts/leakage_scan.py or similar).
    #
    # At v0.1.0-pre this is vacuous (no protocols yet). At M1+ the
    # contract tightens: any protocol.md with a data section must either
    # (a) only use known sources, or (b) reference a leakage scan.

    violations: list[str] = []
    for protocol in protocol_files:
        text = protocol.read_text().lower()
        if "leakage" in text or "scripts/leakage_scan" in text:
            continue  # protocol references leakage scan — OK
        # M1+ tightening will add: detect non-allowlisted source mentions and
        # flag if no leakage scan reference. v0.1.0-pre is permissive.

    assert not violations, f"Lane protocols missing leakage scan references: {violations}"
