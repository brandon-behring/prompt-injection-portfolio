---
lane_id: lane-1
slug: lane-1-direct-baselines
hypothesis_id: H-LANE-1
title: Direct-injection baseline detection with v0.47 reference scorers + classical floor
date_opened: TBD-M1
date_closed: TBD-M1
budget_usd: 10-12
status: skeleton
---

# Lane 1 — Hypothesis

## Question

How do existing reference scorers (ProtectAI v1/v2, Meta Prompt Guard 2 86M)
compare to a classical TF-IDF + LogisticRegression floor + the submission's
frozen-probe baseline on the portfolio's OOD slate, when ALL trainable baselines
are trained on the same Lane 2 MR-3 corpus (per Round 16 Q1 comparability)?

## 3-way outcome pre-commitment

- **H1 (positive)**: At least one reference scorer (PG2 86M or PromptShield
  Llama-3.1-8B if Tier C unlocked) exceeds the frozen-probe baseline by a
  significant TPR@1%FPR margin on pooled OOD. The wall is not at the
  bottom-rung; better off-the-shelf detectors exist.
- **H0 (null)**: All reference scorers cluster within the frozen-probe
  baseline's bootstrap CI on TPR@1%FPR + AUPRC. The OOD wall framing
  (per submission ADR-075) holds across the off-the-shelf detector
  landscape.
- **H∅ (negative)**: TF-IDF + LogisticRegression beats one or more
  reference scorers on the OOD slate. The classical floor exposes that
  the reference scorers are overfit to in-distribution patterns; OOD
  wall is real + classical baseline is the appropriate floor.

## Prior evidence references

- Submission ADR-075: unified full-FT OOD drop rationale; methodology-
  load-bearing per ADR-050 R2 + ADR-052 supersession.
- Submission v1.1.2 DeBERTa null result: chunk_and_average 0.2912 ≈
  head_truncation 0.2895 on pooled OOD; backbone-invariance evidence.
- Round 7 Tier B citations: V0 rung decomposition (~68% of work in
  pretraining); V4 contamination signature (~8.4pp aggregate AUC inflation
  random vs source-disjoint LODO); Bhagwatkar 2025 "Firewalls" critique.

## Success criteria

- TPR@LowFPR (1%, 0.5%, 0.1%, 0.05%) reported per ADR-036 for all rows.
- Bootstrap CI per ADR-022 + paired-bootstrap delta vs frozen-probe for
  each new detector.
- Per-row predictions parquet persisted per `predictions_persisted`
  test-contract.

## Bail-out criteria

- Total Lane 1 spend exceeds $12 (Round 7 Tier B base; Round 22 cost
  envelope holds). Halt + document.
- Reference-scorer API breaking change in eval-toolkit v0.48+ (unlikely
  per Round 20 stability lock).

## Cost envelope

- Meta PG2 86M inference: ~$10 GPU (Round 7 Tier B Q1'''''')
- ProtectAI v1/v2 inference: ~$0 (HF Hub CPU inference; off-the-shelf)
- TF-IDF + LR baseline: ~$0 (sklearn; CPU)
- Optional Tier C PromptShield Llama-3.1-8B SOTA anchor: ~$40-50; gated
  on M1→M2 review per plan §16.

## ADR pointers

- ADR-036: TPR@LowFPR reporting requirement
- ADR-038: benchmark integrity audit (no PINT/PromptShield/NotInject
  training overlap)
- ADR-043 (Round 15 Q1): Lane 2 LoRA-only scope + baseline expansion
- ADR-045 (Round 20): v0.47 canonical API surfaces

## Cross-references

- `experiments/lane-2/protocol.md` (Round 16 Q1 train-corpus dependency)
- `experiments/lane-1b/protocol.md` (Round 7 Tier B CourtGuard row)
- Book chapter 8 (Lane 1 outcomes) + fragments at
  `book/src/content/fragments/lane-1/{methodology,results,interpretation}.mdx`
