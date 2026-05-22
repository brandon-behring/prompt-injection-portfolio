---
lane_id: lane-5
slug: lane-5-activation-probe
hypothesis_id: H-LANE-5
title: Lane 5 execution protocol — ActivationDeltaProbe on ModernBERT (Lane 2 corpus)
date_locked: TBD-M4
status: skeleton
---

# Lane 5 — Protocol

## Setup

Per Round 16 Q4 (train-on-Lane-2-corpus) + Q5 (timing shift M2 → M4):
ActivationDeltaProbe trains on Lane 2 MR-3 corpus (~20k rows), evaluates
on the OOD pool. Uses eval-toolkit v0.47+ `ActivationDeltaProbe` (per
Round 20 canonical surface).

## Backbone

ModernBERT-base — submission's encoder backbone (held constant across
Lane 2 LoRA + Lane 5 probe + Lane 1 frozen-probe for cross-lane
comparability per Round 16).

## Probe configuration

```python
from eval_toolkit import ActivationDeltaProbe

probe = ActivationDeltaProbe(
    backbone="answerdotai/ModernBERT-base",
    layer_index=-1,           # last hidden state; tweak at protocol-lock if needed
    aggregate="mean",          # pool over sequence
    clean_baseline_text="\n",  # reference input for delta
)
```

## Execution sequence

### Phase 1: activation extraction (~$10-20 GPU; M4 Day 1-2)
1. Compute activations for clean baseline + Lane 2 MR-3 corpus
2. Compute activations for OOD eval slate

### Phase 2: probe training (~$0; CPU)
1. `probe.fit(clean_texts, injected_texts)` on Lane 2 MR-3 corpus
2. Inspect `probe.coef_` for interpretability prose (Ch 12)

### Phase 3: eval (~$0)
1. `probe.predict_proba(oo_texts)` on pooled OOD
2. Scorecard + TPR@LowFPR per ADR-036
3. Paired-bootstrap delta vs frozen-probe baseline

### Phase 4: aggregate + persist
1. Per-row predictions parquet at `evals/lane-5/predictions.parquet`

## Test-contract attestations

- `predictions_persisted`: `evals/lane-5/predictions.parquet`
- `library_imports_registered`: `ActivationDeltaProbe` + `Probe` registered

## Cross-references

- Lane 2 (training corpus per Round 16 Q4)
- F8 risk (encoder-vs-decoder methodology port; primary outcome hypothesis)
- Book Ch 12 + fragments at `book/src/content/fragments/lane-5/`
