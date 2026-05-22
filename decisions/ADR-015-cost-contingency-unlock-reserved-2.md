---
adr_id: "015"
slug: cost-contingency-unlock-reserved-2
title: "Cost contingency unlock — reserved slot 2"
date: 2026-05-19
status: Reserved
linked_round: "R1"
plan_section: "§1 Round 1 Q2 + §16"
---

# ADR-015: Cost contingency unlock — reserved slot 2

## Status

**Reserved** (per [ADR-013](ADR-013-cost-contingency-unlock-policy.md)
gating policy). Sibling to
[ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md); the two slots
together capture up to the full $100 contingency budget if drawn.

## Unlock criteria

This ADR advances `Reserved` → `Accepted` when ALL of the following hold:

1. Base $250 + Slot-1 unlock (if drawn) spend is approaching or exceeded
   with viable remaining lane work.
2. A specific research signal justifies the second-slot spend (not
   incremental scope-drift; documented in `decisions/contingency_unlock_N.md`).
3. `decisions/contingency_unlock_N.md` filed BEFORE the spend per
   [ADR-013](ADR-013-cost-contingency-unlock-policy.md).
4. `make cost-report` attests current + projected spend < $350 hard cap.
5. After this draw, no third contingency ADR pre-exists — third+
   contingency draws require user-led re-scoping conversation.

## Decision

*(blank pending unlock)*

The Decision section will be filled in when this ADR advances to
`Accepted`. It will record: (a) the trigger event, (b) the amount drawn,
(c) the specific contingency_unlock_N.md ratified, (d) post-draw budget
state.

## Consequences

*(blank pending unlock)*

The Consequences section will be filled in alongside the Decision. It
will record: (a) lane(s) affected by the unlock, (b) post-unlock
cost-rollup, (c) confirmation that no further contingency slots remain
without re-scoping.

## Cross-references

- Plan §1 Round 1 Q2 (cost cap origin); plan §16 (contingency unlock gates)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) (base + contingency split)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (gating policy this ADR enforces)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) (sibling reserved slot)
