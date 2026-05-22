---
lane_id: lane-2
slug: lane-2-synthetic-retrain
hypothesis_id: H-LANE-2
title: Indirect-injection LoRA retrain (2-variant loss ablation) + classical baselines
date_opened: TBD-M2
date_closed: TBD-M4
budget_usd: 156-196
status: skeleton
---

# Lane 2 — Hypothesis

## Question

Does adding indirect-injection training data overcome (a) the active-harm
LoRA pattern from submission's direct-injection training AND (b) backbone-
invariant OOD limit per v1.1.2 DeBERTa null? Per Round 15 Q1: parameter
budget held at LoRA-only (no full-FT); two loss variants tested in
parallel (CE + Recall@LowFPR). All comparator baselines (TF-IDF + frozen-
probe + reference scorers) share the same training corpus per Round 16 Q1.

## 3-way outcome pre-commitment

- **H1 (positive)**: Both LoRA loss variants lift to non-negative AUPRC
  delta vs frozen-probe on pooled OOD with CI clearing zero. Indirect
  training data overcomes both prior limits; the OOD wall is data-bound
  (counter-evidence to backbone-dominant verdict).
- **H0 (data-bottleneck-partial)**: One LoRA variant lifts; the other
  does not. Loss-function asymmetry distinguishes the two recipes.
- **H∅ (null)**: Both LoRA variants still produce negative AUPRC deltas
  vs frozen-probe. The OOD wall is confirmed structural beyond data
  choice; the active-harm LoRA pattern persists with indirect-injection
  training data. Methodology lesson: current detector framing has a
  hard ceiling.

## Prior evidence references

- Submission ADR-075 (canonical; supersedes ADR-050 R2 + ADR-052): full-FT
  OOD drop methodologically load-bearing
- Submission v1.1.2 DeBERTa null result: backbone-invariance evidence
- Liu et al. NeurIPS 2020 (energy-based loss; optional Tier C 3rd variant)

## Success criteria

- 2-variant LoRA paired-bootstrap with CI per ADR-022 (10K resamples)
- TPR@LowFPR reported per ADR-036
- Per-row predictions parquet per `predictions_persisted` contract
- Lane 2 corpus seed pinned via `/dataset-synthesize` skill (MR-3 dependency)

## Bail-out criteria

- Total Lane 2 spend (data + train) exceeds $196 base envelope per
  Round 1 Q3 + Round 15 Q2. Halt + escalate.
- Lane 2 MR-3 corpus inter-annotator audit κ < 0.5 — bail per ADR-027
  protocol; re-spec synthesis recipe.

## Cost envelope

- Lane 2 synthetic data gen (Sonnet + Opus audit; bail at $80): $88-128
- Lane 2 retrain × 2 LoRA variants (CE + Recall@LowFPR): $68 GPU
- Optional Tier C energy-loss 3rd variant: +$34 (gated)

## ADR pointers

- ADR-043 (Round 15): Lane 2 LoRA-only scope + baseline expansion
- ADR-045 (Round 20): v0.47 canonical surfaces + RecallAtLowFPR
- ADR-022: paired-bootstrap methodology
- ADR-075 (submission): unified full-FT OOD drop rationale

## Cross-references

- MR-3 (research_toolkit#1) — STILL OPEN; dataset-synthesize skill blocker
- Lane 4 (stacker trains on same Lane 2 corpus per Round 16 Q3)
- Lane 5 (probe trains on same Lane 2 corpus per Round 16 Q4)
- Book chapter 7 (Ch 7 case study citation ADR-075) + chapter 9 (Lane 2
  detailed) + fragments at `book/src/content/fragments/lane-2/`
