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

**Re-pointed to the carrier axis per [ADR-055](../../decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md)
Decision 2 (Round 30); method unchanged.** M1 answered the attack-type axis (end-to-end LoRA already
generalizes near-uniformly across held-out attack types — §6.5 FALSIFIED), and the carrier-LODO M2
pre-flight sized the live gap: a **residual, capacity-attenuated carrier wall concentrated at the
*table* carrier** (aggregate G(lora)=+0.067, **+0.205 at table**; email/code close —
`experiments/carrier-lodo/FINDINGS.md`).

> **First datum (C1, 2026-06-11): `NOT-CLOSED` — an H∅-shaped answer for the synthetic
> format-matched recipe.** A leakage-gated 1800/600 synthetic table corpus (gpt-4.1-mini) reduced
> the frozen rung (ΔG +0.083, CI-supported) but did **not** bridge at the `lora` ceiling
> (ΔG −0.028, CI-low −0.032); the table wall is **data-resistant at the ceiling** for that recipe
> (n=1 fold; ADR-055 2026-06-11 amendment; 5-verifier audit ROBUST —
> `../carrier-table-training/AUDIT_C1_2026-06-11.md`). The H-branches below remain the
> pre-committed frame for any *carrier-diverse real-data* variant; the H-optimistic null was
> pre-committed as publishable and feeds the C2 style-vs-content mechanism probe.

Does **carrier-diverse indirect-injection training data** close that residual carrier wall — i.e.
lift held-out-carrier (esp. table) detection toward the in-distribution ceiling — under end-to-end
LoRA? Per Round 15 Q1: parameter budget held at LoRA-only (no full-FT); two loss variants tested in
parallel (CE + Recall@LowFPR). All comparator baselines (TF-IDF + frozen-probe + reference scorers)
share the same training corpus per Round 16 Q1. **Cheap §16 optional secondary:** confirm
attack-type generalization persists under the Lane-2 recipe (M1 showed it holds at the `lora` ceiling).

## 3-way outcome pre-commitment

Measured as the **carrier-LODO gap** (held-out-carrier val→test ROC-AUC drop, per
`experiments/carrier-lodo/criteria.md`; the **table** carrier is the live residual), each of
CE + Recall@LowFPR vs the same-corpus frozen-probe:

- **H1 (positive — carrier wall is data-bound)**: carrier-diverse training closes the residual
  table-carrier gap (held-out-carrier ROC-AUC drop → CI clears zero from above) for at least the CE
  variant. The residual carrier wall is a *data-diversity* limit, surmountable with carrier-diverse
  indirect data + capacity.
- **H0 (partial / loss-asymmetric)**: one loss variant closes the table gap, the other does not —
  loss-function asymmetry distinguishes the recipes on the hard carrier.
- **H∅ (null — residual carrier wall is structural)**: both variants leave a statistically-real
  table-carrier gap. The residual wall is structural at the table carrier beyond data choice + LoRA
  capacity. Methodology lesson: carrier (esp. tabular-context) generalization has a hard ceiling for
  encoder detectors.

## Prior evidence references

- **Carrier-LODO M2 pre-flight (`experiments/carrier-lodo/`): SMALL-THROUGHOUT — the carrier wall is
  capacity-attenuated (frozen +0.167 → lora +0.067) with a residual +0.205 at the table carrier.
  This is the gap Lane 2 targets; the spine ([ADR-055](../../decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md))
  is multi-axis capacity-dependent.**
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
