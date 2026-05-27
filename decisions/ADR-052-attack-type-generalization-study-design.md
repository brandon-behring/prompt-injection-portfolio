---
adr_id: "052"
slug: "attack-type-generalization-study-design"
title: "Attack-type-generalization study for indirect-injection detection (axis C: type-LODO + joint shift)"
date: 2026-05-26
status: Accepted
linked_round: "R26 (roadmap reorientation session)"
plan_section: "§5"
supersedes: []
---

# ADR-052: Attack-type-generalization study design

## Context

Verification of the sibling submission (RESULTS.md v1.3.0) showed that on pooled OOD **every rung AND
SOTA ProtectAI sit at/below the random floor (0.374)** — direct→indirect transfer has no signal, and
"frozen>LoRA" is a mirage (two sub-random detectors). The cross-rung comparison was also confounded
(frozen pre-head + uniform untuned recipe + no model selection; full-FT OOD never measured — ADR-075
crash). The open, decision-relevant question is **indirect→indirect: does a detector trained on some
*types* of indirect injection generalize to held-out types?** A data audit found this is feasible on
real data via **BIPIA's native disjoint attack-type train/test split** (verified: 15 vs 15 types, only
"Language Translation" overlapping; ~75 attack strings/split; task-intent + obfuscation-technique
sub-families), whereas pure carrier-isolation leaks (attacks shared across scenarios).

## Decision

Run an **honest attack-type-generalization study** (methodologist-first; an honest limitation/negative
result is an acceptable outcome iff the evaluation is correct). **Axis C:**
- **Core (clean):** train on BIPIA train-attack-types → test on the **disjoint** test-attack-types
  (drop the "Language Translation" overlap). Report a focused **obfuscation-technique** sub-split.
- **External check:** a joint **carrier+attack shift** (train {train-scenarios × train-attacks} → test
  {held-out scenario × test-attacks}).
- **Detectors:** frozen-probe + LoRA on ModernBERT-base, **+ full-FT** (closes the never-measured OOD
  gap). **Fair per-rung tuning + model selection on a TRAIN-INTERNAL val split** (LODO test untouched);
  option to train the pre-head for LoRA — correcting the submission's confound.
- **Metrics:** AUPRC + TPR@{1,0.5,0.1}%FPR + **random-floor per fold** + benign FPR (NotInject) +
  **in-distribution-vs-LODO inflation**.
- **Independent rebuild** — own pipeline; do not inherit submission predictions.

## Consequences

- Answers the type-generalization question on real data with no synthesis. Honest limitation: BIPIA's
  attack-string diversity is small (5/type, 75/split) → memorization risk; per-type N is noisy, so the
  headline is the aggregate train-types→test-types split + the obfuscation sub-family, not per-type CV.
- qa/abstract scenarios need license-gated context generation; email/code/table are immediately usable.
- Lane/chapter restructure is **deferred to Phase 3** (after results); this ADR locks the *design*, not
  the lane reorganization.

## Alternatives considered

- **Pure carrier/scenario-LODO** — rejected: BIPIA's shared attack pool leaks attack strings across
  scenarios, so it can't cleanly isolate carrier shift.
- **Technique-LODO via synthesis / LLM-re-labeling** — deferred: higher cost/risk (incl. the
  `/dataset-synthesize` #22 bug); revisit only if BIPIA's real-data split proves insufficient.
- **Inherit the submission's numbers** — rejected: the user requires an independent rebuild.
