---
adr_id: "040"
slug: lane-2-energy-loss-tier-c
title: "Lane 2 energy-based loss 3rd variant (Round 7 Tier C contingency unlock)"
date: 2026-05-19
status: Reserved
linked_round: "R7"
plan_section: "§5 + §16 Tier C"
---

# ADR-040: Lane 2 energy-loss 3rd variant (Tier C)

## Status

**Reserved** (Round 7 Q2'''''' Tier C contingency-unlock; scoped LoRA-only
per Round 15 Q1 / [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md)).
Advances to `Accepted` if and only if M3+M4 signal triggers the unlock.

## Unlock criteria

This ADR advances `Reserved` → `Accepted` when ALL of the following hold:

1. **M3 audit kappa ≥0.5** — Lane 2 synthetic indirect-injection
   corpus audit passes inter-annotator kappa threshold (per Lane 2
   playbook protocol.md bail-out criteria).
2. **M4 two-variant CI shows interpretable signal** — RFPR delta CI
   clear of zero on pooled OOD; ambiguous CIs (crossing zero) do NOT
   trigger.
3. **Budget gate** — ~$34 GPU available within base + contingency
   envelope.
4. **`decisions/contingency_unlock_N.md`** filed with the M3+M4 signal
   evidence + energy-loss execution plan (Meta PG2 recipe; Liu NeurIPS
   2020 reference).
5. **Round 15 scope holds** — Variant C is LoRA-only on ModernBERT-base.
   No full-FT.

## Decision

*(blank pending unlock)*

The Decision section will be filled in if this ADR advances to
`Accepted`. It will record:
- M3 audit + M4 two-variant signal that triggered unlock
- Energy-based loss configuration (LoRA r=32; ModernBERT-base; Meta PG2
  recipe + Liu NeurIPS 2020 mechanics)
- Training cost + wall-clock
- Predictions parquet + HF Hub model card
  (`BBehring/prompt-injection-lora-indirect-v2-energy`)

## Consequences

*(blank pending unlock)*

The Consequences section will be filled in alongside the Decision. It
will record:
- Lane 2 results extension (Variant C AUPRC vs CE + RFPR; 3-way
  comparison)
- Whether loss-function diversity overcomes the OOD wall (vs data-only
  bound from CE / RFPR comparison)
- Ch 9 prose impact (per `portfolio-chapter-outlines.md` Ch 9 outline)
- Cost-rollup post-unlock

## Cross-references

- Plan §5 (Lane 2 hypothesis); plan §16 (Tier C contingency-unlock framing)
- [ADR-003](ADR-003-lane-2-loss-ablation-ce-recall-at-lowfpr.md) (base 2-variant ablation; this Tier C 3rd variant extends)
- [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md) (Round 15 LoRA-only scope)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (gating policy)
- Lane execution playbook §2 (`portfolio-lane-execution-playbooks.md` — Lane 2 Tier C gate)
- Liu et al. NeurIPS 2020 energy-based loss
