---
lane_id: lane-4
slug: lane-4-stacker
hypothesis_id: H-LANE-4
title: Lane 4 execution protocol — LogisticStacker + XGBoost meta-learner on score matrix
date_locked: TBD-M6
status: skeleton
---

# Lane 4 — Protocol

## Setup

Stacker training matrix `(N_samples, N_detectors)` built from Lane 1
+ Lane 2 detector scores on the Lane 2 MR-3 corpus (per Round 16 Q3
same-corpus rule). Eval slate: LLMail-Inject 5K stratified + PINT-EN 3016
(per Round 1 Q5 lock).

## Detectors as columns

- TF-IDF + LogisticRegression baseline (Lane 1)
- Frozen-probe (Lane 1 baseline)
- ProtectAI v1 + v2 (Lane 1 reference)
- Meta PG2 86M (Lane 1 Tier B)
- Lane 2 LoRA CE variant
- Lane 2 LoRA RecallAtLowFPR variant
- XGBoost-on-OpenAI-embeddings (Round 7 Tier B Lane 4 row; ~$5)

## Stacker models

- `LogisticStacker(C=1.0, class_weight="balanced")` — baseline
- XGBoost classifier on the same `(N_samples, N_detectors)` matrix —
  per Round 7 Tier B Lane 4 row

## Execution sequence

### Phase 1: build score matrix (~$5-10)
1. Score Lane 2 MR-3 corpus through each detector
2. Score LLMail-Inject 5K + PINT-EN 3016 through each detector
3. Cost ~$25 across N detectors (inference-only)

### Phase 2: stacker training (~$0; CPU)
1. `LogisticStacker.fit(score_matrix_train, y_train)`
2. XGBoost `fit(score_matrix_train, y_train)`

### Phase 3: eval (~$0)
1. Eval both stackers on LLMail-Inject + PINT held-outs
2. Compute scorecard + TPR@LowFPR + APR per ADR-037
3. Paired-bootstrap delta vs best-individual

### Phase 4: aggregate + persist (~$0)
1. Per-row predictions parquet at `evals/lane-4/predictions.parquet`
2. Stacker coefficient inspection (`LogisticStacker.coef_`) for Ch 11
   interpretation prose

## Test-contract attestations

- `predictions_persisted`: `evals/lane-4/predictions.parquet`
- `library_imports_registered`: `LogisticStacker` + `MetaLearner` + xgboost
- `no_handrolled_metrics`: APR reported via `scorecard` extension or
  manual calc but never reimplementing `eval_toolkit.metrics`

## Cross-references

- Lane 1 / Lane 1b (detector inputs)
- Lane 2 (training corpus)
- Book Ch 11 + fragments at `book/src/content/fragments/lane-4/`
