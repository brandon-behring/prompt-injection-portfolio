---
lane_id: lane-3
slug: lane-3-spotlighting
hypothesis_id: H-LANE-3
title: Lane 3 execution protocol — top-level sweep() across 3 Spotlighting variants
date_locked: TBD-M5
status: skeleton
---

# Lane 3 — Protocol

## Eval slate

Same OOD pool as Lane 1 / Lane 1b. Each row preprocessed by each of the
3 Spotlighting dataclass variants.

## Detectors in scope

- Frozen-probe (Lane 1 baseline)
- Lane 2 LoRA variants (CE + Recall@LowFPR)
- Lane 1 reference scorers (ProtectAI v1/v2, PG2 86M)

## Execution sequence

### Phase 1: setup (~$0)
1. Confirm `eval_toolkit.preprocessing.{DelimitVariant, DatamarkVariant, EncodeVariant}`
   importable per Day 3a smoke-test
2. Construct strategies list with default kwargs (delimiter="<<",
   marker="^", encoding="base64")

### Phase 2: sweep (~$1)
1. `sweep(strategies, texts, scorer=detector)` for each detector
2. Compute scorecard + TPR@LowFPR per ADR-036

### Phase 3: aggregate + persist (~$0)
1. Per-row predictions parquet at `evals/lane-3/predictions.parquet`
2. Per-detector × per-variant summary

## Test-contract attestations

- `predictions_persisted`: `evals/lane-3/predictions.parquet`
- `library_imports_registered`: 3 dataclass imports + `sweep`

## Cross-references

- Lane 1 (baseline detectors)
- Lane 2 (LoRA variants)
- Book Ch 10 + fragments at `book/src/content/fragments/lane-3/`
