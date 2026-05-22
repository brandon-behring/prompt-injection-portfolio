---
adr_id: "016"
slug: lodo-methodology-from-submission
title: "LODO methodology carried from submission"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§5 + §10"
---

# ADR-016: LODO methodology carried from submission

## Status

Accepted.

## Context

Leave-One-Domain-Out (LODO) is submission's load-bearing eval discipline.
Submission's ADR-016 documents the methodology: cross-source disjoint
splits prevent contamination signature (~8.4pp aggregate AUC inflation
random vs source-disjoint LODO, per V4 finding cited in Ch 2).

Portfolio inherits LODO as the baseline eval framing across all
6 lanes (per plan §5). Without re-locking, future portfolio lanes might
drift toward easier random-split evals — a known regression-hiding
anti-pattern.

The submission's V4 contamination signature finding (Round 7 Tier B
citation) is operative evidence: random-split eval inflates AUC by
~8.4pp on average vs source-disjoint LODO. LODO is the discipline
that makes the OOD wall observable.

## Decision

Portfolio LODO methodology = identical to submission's ADR-016:

- **6 OOD sources** held disjoint by source (per plan §5):
  BIPIA + AgentDojo + InjecAgent + NotInject + LLMail-Inject +
  PINT-EN.
- **Cross-source held-out** — never train on a source that's evaluated
  on; train-test source-disjoint check in eval-toolkit
  `loaders.ood_dataset_from_manifest` (per upstream MR-1; released
  v0.43.0).
- **5-rung ladder framing** (per Round 7 Tier B citation to submission's
  V0 rung decomposition): frozen-probe + LoRA + reference scorers +
  Tier B additions + portfolio's 2-variant Lane 2 retrains.

LODO is the eval-discipline floor; portfolio-specific Lane evaluations
add ablations on top of LODO (not in place of).

## Consequences

- **Test-contract `leakage_scan_present`** (per
  [ADR-012](ADR-012-test-contracts.md)) operationalizes LODO at
  CI gate.
- **Benchmark integrity audit** ([ADR-038](ADR-038-benchmark-integrity-audit.md))
  ratifies that portfolio doesn't train on PINT / PromptShield /
  NotInject / HackAPrompt (all held-out per LODO).
- **Submission carry-over**: portfolio's `experiments/MANIFEST.json`
  records the 6 OOD sources matching submission's manifest schema.
- **Round 6 reframing applies**: portfolio writes its OWN clean T0
  ([ADR-035](ADR-035-portfolio-clean-t0-strategy.md)) but the LODO
  methodology itself doesn't need a clean reimplementation — it's a
  *discipline*, not a *codebase*.

## Cross-references

- Plan §5 (eval-slate per-lane); plan §10 (eval-toolkit MR-1)
- Submission ADR-016 (LODO methodology origin)
- [ADR-038](ADR-038-benchmark-integrity-audit.md) (held-out audit at M0)
- V4 contamination signature finding (Round 7 Tier B; Ch 2 case study)
