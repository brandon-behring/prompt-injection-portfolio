---
lane_id: lane-3
slug: lane-3-spotlighting
hypothesis_id: H-LANE-3
title: Spotlighting structural defense (3 variants) on encoder-only detectors
date_opened: TBD-M5
date_closed: TBD-M5
budget_usd: 1
status: skeleton
---

# Lane 3 — Hypothesis

## Question

Do the 3 Spotlighting variants (Hines et al. 2024 arXiv 2403.14720) —
delimit / datamark / encode — improve OOD detection when applied as
preprocessing to encoder-only classifiers (frozen-probe + Lane 2 LoRA
variants + reference scorers)?

## 3-way outcome pre-commitment

- **H1 (positive)**: At least one Spotlighting variant produces a
  non-negative AUPRC delta on OOD for at least one detector. Structural
  defense composes with encoder detectors.
- **H0 (null)**: All 3 variants × N detectors produce within-bootstrap-CI
  AUPRC deltas. Spotlighting was designed for LLM-side rejection
  (Hines et al. used decoder-LLM-as-judge); encoder classifiers don't
  inherit the benefit.
- **H∅ (negative)**: One or more variants WORSEN detection (e.g., base64
  encoding masks legitimate patterns the classifier learned). Per F8
  encoder-vs-decoder methodology asymmetry, this is the most likely.

## Prior evidence references

- Hines et al. 2024 arXiv 2403.14720 (Microsoft Research)
- Round 14 Q3 + Round 20: 3 dataclasses ship in eval-toolkit v0.47.0
  (`DelimitVariant`, `DatamarkVariant`, `EncodeVariant`)

## Cost envelope

- 3 preprocessing transforms × N detectors × OOD slate: ~$1 API
  (preprocessing is CPU; detector inference is the cost driver but
  small at this scale)

## ADR pointers

- ADR-036: TPR@LowFPR reporting
- ADR-045 (Round 20): v0.47 canonical surfaces (`DelimitVariant` etc.)

## Cross-references

- Book chapter 10 (Lane 3 RAG demo) + fragments at
  `book/src/content/fragments/lane-3/`
