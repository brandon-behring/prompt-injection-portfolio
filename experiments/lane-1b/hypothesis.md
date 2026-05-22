---
lane_id: lane-1b
slug: lane-1b-adversarial-matrix
hypothesis_id: H-LANE-1B
title: Adversarial robustness matrix — 12-technique character_injection × N detectors + CourtGuard
date_opened: TBD-M1
date_closed: TBD-M1
budget_usd: 5-10
status: skeleton
---

# Lane 1b — Hypothesis

## Question

When the OOD eval slate is transformed by each of the 12 character_injection
techniques (`eval_toolkit.adversarial.ALL_TECHNIQUES` per v0.47.0), do the
Round 7 Tier B reference scorers retain their AUPRC + TPR@LowFPR margin
over the classical floor + frozen-probe baselines? CourtGuard's multi-agent
debate baseline tests whether ensemble defenses help.

## 3-way outcome pre-commitment

- **H1 (positive)**: At least one detector retains >50% of its baseline
  TPR@1%FPR under one or more advanced-6 transformations. Encoder
  classifiers can be hardened against character injection.
- **H0 (null)**: All detectors degrade uniformly to baseline-prevalence
  AUPRC under any character_injection technique. Encoder framing is
  structurally bypassed by surface transforms; no transformation-class
  asymmetry.
- **H∅ (negative)**: CourtGuard multi-agent debate measurably worsens
  detection on the OOD pool (over-defense / false-positive inflation).
  Multi-agent debate is not a free win; cost > benefit at this scale.

## Prior evidence references

- Microsoft Research 2024 arXiv 2404.13208 (12-technique character injection)
- Round 14 Q3 + Round 20: all 12 dataclasses shipped in eval-toolkit v0.47.0
- Bhagwatkar et al. NeurIPS 2025 arXiv 2510.05244 ("Are Firewalls All You
  Need?" critique) — relevant prior on multi-agent-defense saturation

## Success criteria

- Per-row predictions parquet with (text_id, technique, original_score,
  transformed_score, asr) columns per `eval_toolkit.sweep` output schema.
- TPR@LowFPR reported per ADR-036 for the baseline + each transformed slice.

## Bail-out criteria

- Total Lane 1b spend exceeds $10 (Round 7 Tier B budget). Halt + document.

## Cost envelope

- 12 char-injection transforms × N detectors × OOD slate: ~$5-8 API + GPU
- CourtGuard multi-agent baseline: ~$5-10 API

## ADR pointers

- ADR-036: TPR@LowFPR reporting
- ADR-045 (Round 20): v0.47 canonical surfaces (`ALL_TECHNIQUES` 12-tuple +
  top-level `sweep()`)

## Cross-references

- Lane 1 (reference scorer baselines)
- Book chapter 8 sidenote + fragments at
  `book/src/content/fragments/lane-1b/`
