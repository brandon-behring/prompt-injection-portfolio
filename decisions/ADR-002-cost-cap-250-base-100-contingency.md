---
adr_id: "002"
slug: cost-cap-250-base-100-contingency
title: "Cost cap: $250 base + $100 contingency"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q2"
---

# ADR-002: Cost cap — $250 base + $100 contingency

## Status

Accepted.

## Context

Portfolio runs ~13-14 weeks of lane experiments + dossier + book authoring
across 6 lanes (per plan §5). Cost budget must:

1. Constrain total spend to a verifiable envelope for solo / unfunded
   research-portfolio context.
2. Allow legitimate scope-expansion (Tier C method-expansions, Tier B
   detector additions) via gated unlock — not silent overspend.
3. Reconcile against per-lane budgets from the lane execution playbooks
   (lane-execution-playbooks.md §1-6): Lane 1 $10-12 + Lane 1b $5-8 +
   Lane 2 $156-196 + Lane 3 ~$1 + Lane 4 $5-30 + Lane 5 $10-20 ≈
   $187-267 base before contingency.

## Decision

**Base cost cap**: $250.
**Contingency budget**: $100 (gated unlock).

Total hard cap: **$350**. Cost rollup tracked via `make cost-report`
(per plan §13). Each contingency unlock requires a
`decisions/contingency_unlock_N.md` per [ADR-013](ADR-013-cost-contingency-unlock-policy.md)
+ optionally [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) /
[ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md) ratifying the
specific unlock.

## Consequences

- **Per-lane soft caps** flow from this: ~$100/lane informal target;
  Lane 2 (the most expensive at $156-196) consumes the majority.
- **Tier C method-expansions** (PromptShield Llama-3.1-8B Lane 1 +
  energy-loss Lane 2 3rd variant) **MUST** route through contingency
  unlock — they're not base-budget items per plan §16.
- **Cost monitoring is manual**: no auto-shutoff. `make cost-rollup-check`
  invoked at each RunPod-deploy stage; budget-overrun must surface in
  results.md per the experiment-record schema (`portfolio-experiment-record-template.md` §results).
- **Hard cap enforcement**: at $350 total, no further work without
  user-led re-scoping conversation.

## Cross-references

- Plan §1 Round 1 Q2; plan §13 (Verification — Cost monitoring); plan §16 (Prioritized roadmap — Tier C gates)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (gating policy)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) + [ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md) (reserved instances)
- [ADR-039](ADR-039-lane-1-sota-anchor-promptshield-tier-c.md) + [ADR-040](ADR-040-lane-2-energy-loss-tier-c.md) (Tier C method-expansion ADRs)
