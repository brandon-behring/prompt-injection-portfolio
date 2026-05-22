---
adr_id: "039"
slug: lane-1-sota-anchor-promptshield-tier-c
title: "Lane 1 SOTA-anchor PromptShield Llama-3.1-8B (Round 7 Tier C contingency unlock)"
date: 2026-05-19
status: Reserved
linked_round: "R7"
plan_section: "§5 + §16 Tier C"
---

# ADR-039: Lane 1 SOTA-anchor PromptShield (Tier C)

## Status

**Reserved** (Round 7 Q2'''''' Tier C contingency-unlock). Advances to
`Accepted` if and only if M1 Tier B results trigger the unlock signal.

## Unlock criteria

This ADR advances `Reserved` → `Accepted` when:

1. **M1 signal** — Lane 1 + Tier B results show ALL base detectors
   (frozen-probe + LoRA + ProtectAI v1/v2 + Meta PG2 86M) cluster
   **below 0.40 AUPRC pooled OOD**. The Lane 1 hypothesis would then be
   "the detector ceiling sits below 0.40 across base detectors; does a
   larger SOTA model break the ceiling?"
2. **Budget gate** — $40-50 GPU available within base + contingency
   envelope (via [ADR-013](ADR-013-cost-contingency-unlock-policy.md) +
   `decisions/contingency_unlock_N.md`).
3. **`decisions/contingency_unlock_N.md`** filed with the M1 signal
   evidence + the PromptShield Llama-3.1-8B execution plan.

## Decision

*(blank pending unlock)*

The Decision section will be filled in if this ADR advances to
`Accepted`. It will record:
- The exact M1 cluster (per-detector AUPRC + CI on pooled OOD)
- The PromptShield Llama-3.1-8B execution plan (gated HF Hub access,
  prompt template, inference cost, eval slate)
- Expected vs realized cost
- Linkage to Ch 8 sidenote prose extension

## Consequences

*(blank pending unlock)*

The Consequences section will be filled in alongside the Decision. It
will record:
- Lane 1 results extension (PromptShield AUPRC vs base detectors)
- Whether SOTA breaks the 0.40 ceiling or confirms structural wall
- Ch 8 prose impact (per `portfolio-chapter-outlines.md` Ch 8 outline)
- Cost-rollup post-unlock

## Cross-references

- Plan §5 (Lane 1 hypothesis); plan §16 (Tier C contingency-unlock framing)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (gating policy)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) / [ADR-015](ADR-015-cost-contingency-unlock-reserved-2.md) (cost contingency slots — distinct from method-expansion)
- Lane execution playbook §1 (`portfolio-lane-execution-playbooks.md` — Lane 1 contingency-unlock signal)
- Jacob et al. arXiv 2501.15145 PromptShield
