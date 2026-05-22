---
lane_id: lane-5
slug: lane-5-activation-probe
hypothesis_id: H-LANE-5
title: TaskTracker activation probe port on encoder backbone (Lane 2 corpus)
date_opened: TBD-M4
date_closed: TBD-M4
budget_usd: 10-20
status: skeleton
---

# Lane 5 — Hypothesis

## Question

When TaskTracker's linear activation-probe methodology (Abdelnabi et al.
2024 arXiv 2406.00799) is ported to ModernBERT-base + trained on the same
Lane 2 MR-3 corpus (per Round 16 Q4 same-corpus rule), does it match or
exceed the LoRA + reference-scorer baselines on TPR@LowFPR? Round 16 Q5
shifted timing M2 → M4 (post-Lane-2-corpus).

## 3-way outcome pre-commitment

- **H1 (positive)**: ActivationDeltaProbe TPR@1%FPR exceeds frozen-probe
  baseline by margin clearing paired-bootstrap CI. Encoder + linear-probe
  on hidden-state deltas extracts signal that the Scorer-head doesn't.
- **H0 (null)**: Probe matches frozen-probe baseline within CI. Encoder
  representation surfaces the same signal that the classifier head already
  uses; no methodology gain.
- **H∅ (negative — F8 anticipated)**: Probe materially under-performs
  baseline. TaskTracker methodology was designed for decoder LMs where
  the prompt-vs-completion boundary creates the activation signal;
  encoders process input simultaneously. F8 risk realized; methodology
  port test fails as predicted.

## Prior evidence references

- Abdelnabi et al. 2024 arXiv 2406.00799 (TaskTracker)
- Submission v1.1.2 DeBERTa null result (backbone-invariance)
- F8 risk resolution (per plan §15): encoder-vs-decoder methodology
  mismatch is the prior

## Cost envelope

- ModernBERT activation extraction on Lane 2 MR-3 corpus + OOD: ~$10-20
  GPU per plan §16

## ADR pointers

- ADR-045 (Round 20): `ActivationDeltaProbe` + `Probe` Protocol v0.47

## Cross-references

- Lane 2 (training corpus per Round 16 Q4 + timing shift Q5)
- Book chapter 12 + fragments at `book/src/content/fragments/lane-5/`
- F8 risk resolution (encoder-vs-decoder methodology port)
- F1 risk resolution (Lane 5 timing — UPDATED via Round 16 Q5 from M2 → M4)
