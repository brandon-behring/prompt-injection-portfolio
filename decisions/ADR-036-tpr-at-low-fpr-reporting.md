---
adr_id: "036"
slug: tpr-at-low-fpr-reporting
title: "TPR@LowFPR reporting requirement in all Lane 1 + Lane 4 evals"
date: 2026-05-19
status: Accepted
linked_round: "R7 Tier A"
plan_section: "§5 + §16"
---

# ADR-036: TPR@LowFPR reporting

## Status

Accepted (Round 7 Tier A Q1'''''' — zero-cost methodology improvement).

## Context

Per the compass artifact survey and PromptShield 2025 (Jacob et al.
arXiv 2501.15145), the single most important methodological advance in
prompt-injection detection 2024-25 is reporting TPR (True Positive Rate)
at constrained low False Positive Rates (FPR), rather than headline AUPRC
or AUROC alone.

Why TPR@LowFPR matters:
- A detector with AUPRC 0.85 might have only 20% TPR at 1% FPR — useless
  in production where every false positive costs operator attention.
- The operating-point detail is the actionable signal for production
  threshold-policy design (per plan §6 + ADR-025 dual-policy).
- Single-class slices need val-fixed TPR specifically (per ADR-027
  upstream-enforced via eval-toolkit#39).

## Decision

All Lane 1 + Lane 4 eval surfaces in portfolio MUST report TPR at:
- 1% FPR
- 0.5% FPR
- 0.1% FPR
- 0.05% FPR

alongside AUPRC + AUROC + Brier + ECE(n_bins=15) on multi-class slices.

Reporting via eval-toolkit v0.46+ `scorecard()` with `metric_specs.*` for
the multi-class metrics; TPR@LowFPR via `metrics_at_threshold` + manual
FPR-target threshold selection (or a follow-up MR if eval-toolkit ships
a canonical TPR@LowFPR metric_spec helper).

## Consequences

- Zero additional cost ($0 — derives from existing scorecard outputs).
- Test-contract `predictions_persisted` ensures per-row predictions
  parquet so any reader can re-derive TPR@LowFPR.
- Lane 1 + Lane 1b + Lane 4 protocol.md files include TPR@LowFPR in
  metric reporting deliverables.
- PR template (Day 15 governance) requires confirmation that
  TPR@LowFPR is reported.

## Sprint 2 dossier evidence (added M0 close, Round 24)

The Sprint 2 literature dossier (5 topics, 210 entries, validated via
`make dossier-audit`) provides multi-paper convergence on the low-FPR
forcing function. Three carriers from the
`detector-landscape/` + `training-and-evaluation/` dossiers reinforce
this ADR's decision:

- **`jacob2025promptshield`** (PromptShield, arXiv 2501.15145; already
  cited above) — Table 4 reports TPR@FPR{1%, 0.5%, 0.1%, 0.05%} for
  every detector in their comparison, treating these as the headline
  operating-point metrics rather than AUPRC/AUROC alone. This is the
  paper that operationalized the rule for the field.
- **`li2024injecguard`** (InjecGuard, evaluation_metrics +
  detector_benchmarks claim families) — over-defense quantification
  (NotInject) demonstrates that AUPRC-only reporting masks the
  benign-rejection cost that low-FPR slices surface.
- **`meta2025promptguard2-86m`** + **`meta2025promptguard2-22m`**
  (commercial_detector_performance claim family) — Meta's official
  Prompt-Guard-2 dataset cards report TPR@LowFPR alongside AUC,
  ratifying the operating-point reporting convention at the
  open-weight vendor level.

Claim families anchored: `evaluation_metrics` (8 entries),
`detector_benchmarks` (13 entries). See
`docs/research/training-and-evaluation/` + `docs/research/detector-landscape/`
for full bib_ledger entries + body-quote anchored excerpts.

## Cross-references

- Jacob et al. arXiv 2501.15145 PromptShield (2025) — dossier bibkey
  `jacob2025promptshield`
- ADR-027 (DROPPED; single-class metric upstream-enforced)
- ADR-037 (APR metric; complementary utility-aware metric)
- Lane 1/1b/4 protocol.md files
- ADR-048 (Round 24, cross-classification policy — formalizes how
  the same primary source appears in multiple topic dossiers)
- `docs/research/detector-landscape/bib_ledger.yml` +
  `docs/research/training-and-evaluation/bib_ledger.yml`
