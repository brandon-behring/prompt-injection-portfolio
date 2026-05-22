---
adr_id: "013"
slug: cost-contingency-unlock-policy
title: "Cost contingency unlock policy"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q2 + §16"
---

# ADR-013: Cost contingency unlock policy

## Status

Accepted.

## Context

[ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) locks
$250 base + $100 contingency. The contingency is not a budget *line*
to be drawn down at will — it is a *gated escrow* requiring explicit
justification before each draw. This ADR locks the gating mechanism.

Without explicit gates, contingency degrades to base budget by default
(Goodhart's law on cost cap). The portfolio's solo-researcher context
makes runaway-cost particularly damaging — every $50 unlocked here is
$50 not available for Lane 6+ or v0.8+ work.

## Decision

Each contingency draw requires:

1. **`decisions/contingency_unlock_N.md`** filed BEFORE the spend, listing:
   - Triggering condition (signal that justifies the unlock)
   - Amount requested
   - Expected outcome / hypothesis being tested
   - Bail-out criteria (when to stop drawing further)
2. **One of [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) or
   [ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md)** advances
   from `Reserved` → `Accepted` ratifying the specific unlock.
3. **Cost-rollup attestation**: `make cost-report` showing current spend
   + projected post-unlock spend < $350 hard cap.

Two reserved slots exist (ADR-014 / ADR-015). If both unlock and a third
draw is needed, plan re-scoping (user-led) is required — no third
contingency ADR is pre-allocated.

## Consequences

- **No silent overspend** — each draw is auditable + reviewable in `decisions/`.
- **Mid-milestone gating** — Lane experiments check budget envelope
  before committing GPU time per the experiment-record protocol.md
  bail-out criteria.
- **Tier C method-expansions** ([ADR-039](ADR-039-lane-1-sota-anchor-promptshield-tier-c.md) +
  [ADR-040](ADR-040-lane-2-energy-loss-tier-c.md)) route through this
  policy: their unlock criteria are tied to research signal (e.g., Lane 1
  results clustering below 0.40 AUPRC), separate from cost-driven unlocks
  ADR-014/015.
- **2 reserved slots** means at most $200 unlocked contingency total
  before user-led re-scoping (assuming $100 each, though slots may share
  the $100 budget).

## Cross-references

- Plan §1 Round 1 Q2; plan §16 (Prioritized roadmap — contingency unlock gates)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) (base + contingency split)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) + [ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md) (reserved instances)
