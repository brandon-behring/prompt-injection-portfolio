---
adr_id: "043"
slug: lane-2-lora-only-and-baseline-expansion
title: "Lane 2 retrain LoRA-only + baseline expansion (TF-IDF + open category)"
date: 2026-05-21
status: Accepted
linked_round: "R15"
plan_section: "§5 + §16"
---

# ADR-043: Lane 2 LoRA-only scope + baseline expansion

## Status

Accepted (Round 15 lock + Round 16 cross-lane-comparability refinements).

## Context

Submission predecessor's evidence (ADR-075 — unified full-FT OOD drop
rationale) showed full-FT OOD inference was methodology-load-bearing to
drop. LoRA's -0.071 AUPRC delta vs frozen-probe established the bottleneck
as DATA, not parameter budget. Round 15 Q1 makes the implicit Lane 2
parameter-budget scope explicit.

## Decision

**Lane 2 retrain is LoRA-only** on ModernBERT-base. Full fine-tuning is
OUT OF SCOPE for portfolio. The 2-variant loss ablation (CE + Recall@LowFPR
per Round 1 Q3) + optional Tier C energy-loss 3rd variant (per Round 7
Q2'''''') are ALL LoRA scope.

**Baseline expansion** (Round 15 Q1 user-custom):
- TF-IDF + LogisticRegression (sklearn; CPU; ~$0) as classical floor
- Frozen-probe baseline (submission HF Hub; non-trainable) RETAINED
- ProtectAI v1/v2 + Meta PG2 86M (reference scorers; Round 7 Tier B)
- Open category for "other appropriate open-source models" — locked at
  M1 protocol.md per Round 16 Q2 amendment-friendly workflow

**Round 16 cross-lane comparability**:
- All trainable baselines train on the SAME corpus as Lane 2 LoRA —
  Lane 2's synthetic indirect-injection-heavy MR-3 output (~20k rows)
- Lane 4 stacker (Q3) + Lane 5 probe (Q4) ALSO train on this corpus
- Lane 5 timing shifts M2 → M4 (Round 16 Q5) — post-Lane-2-corpus dependency

## Consequences

- Round 1 Q3's $68 / 2-variant budget IS implicitly LoRA-cost; Round 15
  makes it explicit (full-FT would have been 5-10x). Cost envelope holds.
- Lane 2 hypothesis (§5) sharpens: "does indirect-injection data overcome
  the active-harm LoRA pattern + backbone-invariant limit AT LoRA scope?"
- Lane 1 baselines (TF-IDF + frozen-probe + reference scorers) all
  participate in Round 16 Q1 same-corpus comparability — apples-to-apples
  experimental design.
- Cost re-budget deferred per Round 15 Q2 ("better estimate when we get
  closer"; recompute at M2/M3 gate).
- ADR-043 supports + is supported by ADR-075 (full-FT OOD drop rationale)
  + Round 7 Tier B Lane 1 expansion.

## Cross-references

- Round 1 Q3 (Lane 2 ablation 2-variant lock)
- Submission ADR-075 (canonical full-FT OOD drop rationale)
- Round 16 Q1-Q5 (cross-lane comparability + Lane 5 timing shift)
- Plan §5 + §16 cost envelope (revised at Round 15)
- Lane 2 hypothesis.md + protocol.md
