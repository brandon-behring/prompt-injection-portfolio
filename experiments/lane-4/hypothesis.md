---
lane_id: lane-4
slug: lane-4-stacker
hypothesis_id: H-LANE-4
title: Score-fusion stacker (LogisticStacker + XGBoost) + APR metric on LLMail-Inject + PINT
date_opened: TBD-M6
date_closed: TBD-M6
budget_usd: 30
status: skeleton
---

# Lane 4 — Hypothesis

## Question

Does stacking N detector scores via `eval_toolkit.stacking.LogisticStacker`
(or XGBoost meta-learner for the Round 7 Tier B embedding-based scorer row)
beat the best individual detector on TPR@LowFPR + APR on LLMail-Inject
5K stratified + PINT-EN 3016? Stacker trains on the same Lane 2 MR-3
corpus per Round 16 Q3.

## 3-way outcome pre-commitment

- **H1 (positive)**: Stacker beats best-individual on TPR@1%FPR by a
  margin clearing paired-bootstrap CI on at least one slate (LLMail or
  PINT). Score fusion meaningfully improves the utility-security
  frontier per APR metric.
- **H0 (null)**: Stacker matches best-individual within CI. Diversity
  among the N detectors isn't sufficient for a meta-learner to extract
  additional signal.
- **H∅ (negative)**: Stacker WORSENS one of TPR@LowFPR / APR vs the best
  individual. Meta-learner overfits to the Lane 2 corpus + doesn't
  generalize to LLMail/PINT distributions.

## Prior evidence references

- Round 7 Q1'''''': stacker + embedding-based scorer rows (CodeIntegrity
  approach: XGBoost on OpenAI embeddings)
- ADR-037: APR metric (Meta PG2 utility-aware framing)
- Round 16 Q3: stacker trains on Lane 2 MR-3 corpus

## Success criteria

- TPR@LowFPR + APR reported per ADR-036 + ADR-037
- Paired-bootstrap delta vs best-individual

## Cost envelope

- Stacker training (sklearn LogisticStacker + XGBoost): ~$0 CPU
- OpenAI embeddings (Round 7 Tier B embedding-based scorer): ~$5 API
- LLMail 5K + PINT 3016 inference: ~$25 API

## ADR pointers

- ADR-037: APR metric
- ADR-045 (Round 20): `LogisticStacker` + `MetaLearner` v0.47 surfaces

## Cross-references

- Lane 1 + Lane 1b (detector inputs)
- Lane 2 (training corpus per Round 16 Q3)
- Book chapter 11 + fragments at `book/src/content/fragments/lane-4/`
