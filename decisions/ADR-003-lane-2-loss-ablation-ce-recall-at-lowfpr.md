---
adr_id: "003"
slug: lane-2-loss-ablation-ce-recall-at-lowfpr
title: "Lane 2 loss ablation: CE + Recall@LowFPR (2-variant pre-commit)"
date: 2026-05-19
status: Accepted
superseded_by: ["043"]
linked_round: "R1"
plan_section: "§1 Round 1 Q3 + §5"
---

# ADR-003: Lane 2 loss ablation — CE + Recall@LowFPR

## Status

Accepted; **scope narrowed by [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md)**
(Round 15 LoRA-only scoping + baseline expansion). The 2-variant
loss-ablation locks here remain valid; full-FT was implicit in this ADR's
"variant" framing but is explicitly OUT OF SCOPE per ADR-043.

## Context

Lane 2's central hypothesis (per plan §5): *does training data on
indirect-injection corpora overcome the active-harm pattern observed in
submission's direct-injection LoRA training* (submission ADR-052 / ADR-075)?
A pre-committed ablation prevents post-hoc loss-choice that would
contaminate the experimental design.

Two losses are well-motivated from prior literature:

- **Cross-Entropy (CE)** — classical baseline; matches submission's
  training regime; isolates the data-effect.
- **Recall@LowFPR (RFPR)** — Meta Prompt Guard 2 recipe (compass §2.1);
  targets the operating point the deployment cares about (low-FPR
  detection); isolates the loss-function effect.

A single-loss study would conflate "indirect data helps" with "loss
choice helps." The 2-variant design separates them.

## Decision

Lane 2 retraining is a **pre-committed 2-variant LoRA ablation**:

1. **Variant A — CE loss**: ModernBERT-base + LoRA r=32; standard CE;
   trained on the synthetic indirect-injection corpus (50/50 paired
   per [ADR-005](ADR-005-lane-3-spotlighting-3-variants.md) ratio
   discipline carried from Round 4 Q2''').
2. **Variant B — Recall@LowFPR loss**: same backbone + data + LoRA
   adapter; loss function targets recall ≥95% at FPR ≤1%; eval-toolkit
   primitive `losses.RecallAtLowFPR` per upstream MR-4 (released
   v0.44.0).

Cost envelope: ~$68 GPU (2 × $34 per RunPod-deploy job).

## Consequences

- **Lane 2 hypothesis tests both factors** (data + loss) independently.
- **3-way pre-commitment** (positive / null / negative) per
  `portfolio-experiment-record-template.md` — three outcome branches
  enumerated in Lane 2 hypothesis.md.
- **Tier C optional 3rd variant** (energy-based loss; ~$34) gated via
  [ADR-040](ADR-040-lane-2-energy-loss-tier-c.md) — not part of base
  ablation.
- **Round 15 narrowing**: [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md)
  scopes all Lane 2 variants to LoRA-only (no full-FT) + adds TF-IDF +
  open-baseline category; this ADR's 2-variant base remains.

## Cross-references

- Plan §1 Round 1 Q3; plan §5 (Lane 2 hypothesis)
- [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md) (Round 15 LoRA-only)
- [ADR-040](ADR-040-lane-2-energy-loss-tier-c.md) (Tier C 3rd variant)
- Submission ADR-052 / ADR-075 (active-harm pattern foundation)
