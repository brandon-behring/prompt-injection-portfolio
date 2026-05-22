---
adr_id: "014"
slug: cost-contingency-unlock-reserved-1
title: "Cost contingency unlock — reserved slot 1"
date: 2026-05-19
status: Reserved
linked_round: "R1"
plan_section: "§1 Round 1 Q2 + §16"
---

# ADR-014: Cost contingency unlock — reserved slot 1

## Status

**Reserved** (per [ADR-013](ADR-013-cost-contingency-unlock-policy.md)
gating policy). Advances to `Accepted` if and only if an unlock event
fires that draws from the $100 contingency budget.

## Unlock criteria

This ADR advances `Reserved` → `Accepted` when ALL of the following hold:

1. Base $250 spend is approaching or exceeded with viable remaining
   lane work.
2. A specific research signal justifies the additional spend (not
   "we need more budget" in the abstract).
3. `decisions/contingency_unlock_N.md` is filed BEFORE the spend with:
   trigger condition + amount + expected outcome + bail-out criteria
   (per [ADR-013](ADR-013-cost-contingency-unlock-policy.md)).
4. `make cost-report` attests current + projected spend < $350 hard cap.
5. Slot 1 ([ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md))
   may have unlocked already; this slot is independent.

## Decision

*(blank pending unlock)*

The Decision section will be filled in when this ADR advances to
`Accepted`. It will record: (a) the trigger event, (b) the amount drawn,
(c) the specific contingency_unlock_N.md ratified, (d) post-draw budget
state.

## Consequences

*(blank pending unlock)*

The Consequences section will be filled in alongside the Decision when
this ADR advances. It will record: (a) lane(s) affected by the unlock,
(b) post-unlock cost-rollup, (c) effect on remaining contingency budget.

## Cross-references

- Plan §1 Round 1 Q2 (cost cap origin); plan §16 (contingency unlock gates)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) (base + contingency split)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (gating policy this ADR enforces)
- [ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md) (sibling reserved slot)
