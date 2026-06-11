---
lane_id: lane-2
slug: lane-2-synthetic-retrain
hypothesis_id: H-LANE-2
title: Lane 2 execution protocol — MR-3 synthesis + 2-variant LoRA + same-corpus baselines
date_locked: TBD-M2
status: skeleton
---

# Lane 2 — Protocol

> **Re-pointed to the carrier axis per [ADR-055](../../decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md)
> Decision 2 (Round 30); LoRA-only method + 2-variant loss unchanged
> ([ADR-043](../../decisions/ADR-043-lane-2-lora-only-and-baseline-expansion.md)).** Headline axis =
> **carrier generalization** — close the residual **table**-carrier wall (+0.205) the carrier-LODO M2
> pre-flight sized (`experiments/carrier-lodo/FINDINGS.md`: SMALL-THROUGHOUT, capacity-attenuated).
> **First Lane-2 datum (C1, 2026-06-11): `NOT-CLOSED`** — the synthetic format-matched table corpus
> did not bridge the wall at the `lora` ceiling (ΔG −0.028, CI-low −0.032; frozen-rung reduction
> +0.083 did not survive; `../carrier-table-training/{c1_verdict.json, AUDIT_C1_2026-06-11.md}`);
> the wall is **data-resistant at the ceiling** for that recipe (ADR-055 2026-06-11 amendment).
> Attack-type generalization is a cheap §16 optional secondary (M1 showed it holds). Headline eval =
> **carrier-LODO** (held-out carrier, ROC-AUC gap) reusing
> `experiments/attack-type-lodo/{folds.py, falsify_carrier_lodo.py}`, not pooled OOD.

## Phases

- **M2**: `dataset-synthesize` skill (research_toolkit MR-3) + Opus audit
- **M3**: LLM-rater audit + κ gate
- **M4**: 2-variant LoRA training + Lane 1 baseline retraining
- **M4-M5**: eval + paired-bootstrap

## Synthetic corpus

- Generator: Claude Sonnet 4.6 via research_toolkit `/dataset-synthesize`
- Target: ~10k indirect-injection positives + ~10k benign carriers
- 12-18 templated carrier frameworks (per ETHICS.md §1)
- Opus N=50 inter-annotator audit; κ gate ≥ 0.5 per ADR-027 protocol
- Output: `data/synthetic/indirect-v2/` + HF Hub dataset card

## Training variants (LoRA-only per Round 15 Q1)

| Variant | Loss | Cost | ADR |
|---|---|---|---|
| ce | CrossEntropy (sklearn-style binary) | ~$34 GPU | ADR-019 LoRA recipe |
| rfpr | `RecallAtLowFPR(fpr_target=0.01)` per v0.44.0 | ~$34 GPU | ADR-045 v0.47 pin |
| energy (Tier C optional) | Liu NeurIPS 2020 energy-based loss | ~$34 GPU | ADR-040 (gated) |

Backbone: ModernBERT-base (submission inherited; per Round 16 Q4 backbone
held constant across all LoRA + baselines for same-corpus comparability).

## Comparator baselines (all train on same Lane 2 MR-3 corpus per Round 16 Q1)

- TF-IDF + LogisticRegression (sklearn; ~$0)
- Frozen-probe ModernBERT (no train; off-the-shelf eval only)
- Sentence-transformer + LogisticRegression head (Round 15 Q1 open
  category candidate; pre-decided at M1 protocol.md lock per Round 16 Q2)

## Test-contract attestations

- `no_handrolled_metrics`: lane code uses scorecard + metric_specs
- `predictions_persisted`: `evals/lane-2-ce/predictions.parquet` +
  `evals/lane-2-rfpr/predictions.parquet`
- `leakage_scan_present`: confirm no overlap between Lane 2 MR-3 +
  OOD eval slates
- `library_imports_registered`: `RecallAtLowFPR` + `LogisticStacker` (if used)

## Single-class slice handling

- NotInject + AgentDojo: val-fixed TPR only per submission ADR-027
  (upstream-enforced via eval-toolkit#39)

## Metric reporting

- AUPRC + AUROC + Brier + ECE(n_bins=15) on multi-class slices
- TPR@LowFPR (1%, 0.5%, 0.1%, 0.05%) per ADR-036
- Paired-bootstrap delta CI vs frozen-probe (CE variant)
- Paired-bootstrap delta CI CE-vs-RecallAtLowFPR (loss-asymmetry signal)

## Contingency-unlock gates

- Tier C energy-loss 3rd variant ($34): unlock if M3 data audit κ ≥ 0.5
  AND M4 baseline 2-variant retrain shows interpretable signal. Requires
  `decisions/contingency_unlock_N.md` + ADR-040.

## Cross-references

- Lane 1 / Lane 1b (corpus dependency)
- Lane 4 (stacker uses Lane 2 LoRA scores as detectors per Round 16 Q3)
- Lane 5 (probe trains on same corpus per Round 16 Q4)
- MR-3 dependency: research_toolkit#1 STILL OPEN
- Book chapters 7 + 9 + fragments at `book/src/content/fragments/lane-2/`
