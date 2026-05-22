---
lane_id: lane-1b
slug: lane-1b-adversarial-matrix
hypothesis_id: H-LANE-1B
title: Lane 1b execution protocol — top-level sweep() across 12 techniques + detectors
date_locked: TBD-M1
status: skeleton
---

# Lane 1b — Protocol

## Eval slate

Same OOD slate as Lane 1 (BIPIA + AgentDojo + InjecAgent + NotInject +
LLMail-Inject + PINT). Each row transformed by each of the 12 techniques.

## Detectors in matrix

- Frozen-probe (Lane 1 baseline)
- TF-IDF + LR (Lane 1 classical floor; same-corpus per Round 16 Q1)
- ProtectAI v1 + v2 (Lane 1 reference)
- Meta Prompt Guard 2 86M (Lane 1 Tier B)
- CourtGuard multi-agent debate (NEW Lane 1b Tier B per Round 7 Q1'''''')

## Execution sequence

### Phase 1: setup (~$0; M1 Day 6)
1. Confirm `eval_toolkit.adversarial.ALL_TECHNIQUES` exposes the 12 dataclasses
2. Construct strategies list = `list(ALL_TECHNIQUES)`

### Phase 2: top-level sweep (~$5-8; M1 Day 7)
For each detector:
1. Wrap as `Scorer` Protocol callable
2. `sweep(strategies, texts, scorer=detector, attack_threshold=detector_threshold)`
3. Result: DataFrame with `(text_id, variant, original_score, transformed_score, asr)`

### Phase 3: CourtGuard multi-agent baseline (~$5-10 API; M1 Day 8)
1. Per Round 7 Tier B Q1'''''': multi-agent debate as one matrix row
2. Wrap as `Scorer` Protocol; run through same sweep

### Phase 4: aggregate + persist (~$0)
1. Per-row predictions parquet at `evals/lane-1b/predictions.parquet`
2. Cross-tab summary (`groupby('variant')['asr'].mean()`) for Ch 8 matrix

## Test-contract attestations

- `predictions_persisted`: `evals/lane-1b/predictions.parquet`
- `library_imports_registered`: 12 dataclass imports + `sweep` registered

## Cross-references

- Lane 1 (baseline scorers)
- Book Ch 8 char-injection-bypass-matrix notebook
- Fragments at `book/src/content/fragments/lane-1b/`
