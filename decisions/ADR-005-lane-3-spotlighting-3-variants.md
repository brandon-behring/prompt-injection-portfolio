---
adr_id: "005"
slug: lane-3-spotlighting-3-variants
title: "Lane 3 breadth: all 3 Spotlighting variants (delimit + datamark + encode)"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q4 + §5"
---

# ADR-005: Lane 3 breadth — all 3 Spotlighting variants

## Status

Accepted.

## Context

Lane 3 evaluates whether trust-boundary marking (Spotlighting; Hines et al.
arXiv 2403.14720) improves *detection AUPRC* on indirect-injection corpora.
Spotlighting is proven to reduce *LLM ASR* (>50% → <2%); whether the
same transformation aids encoder-only detection is open.

Spotlighting has three published variants (compass §7):

- **Delimiting** — wrap untrusted region in `[UNTRUSTED_START] ... [UNTRUSTED_END]` tags
- **Datamarking** — replace every whitespace with marker token (`^`)
- **Encoding** — base-64 encode untrusted region + prepend `ENCODED:` marker

Each variant has different mechanics (signal-preservation,
truncation-cost, token-overhead). A 2-of-3 study would risk missing the
operative mechanism; a 1-of-3 study under-determines which marking
strategy is detection-relevant.

## Decision

Lane 3 evaluates **all 3 Spotlighting variants** at M5:

1. **Delimiting** — tag-wrap variant
2. **Datamarking** — whitespace-marker variant
3. **Encoding** — base-64 variant

All three apply at inference-time only (no retraining); evaluated against
submission's frozen-probe + LoRA on BIPIA indirect + InjecAgent +
LLMail-Inject sample (~1000-1500 rows; reuse Lane 2 eval slate).

Library discipline: 3 dataclasses ship in eval-toolkit v0.44+
(`preprocessing.DelimitVariant` + `DatamarkVariant` + `EncodeVariant`;
MR-5 closed).

## Consequences

- **Lane 3 cost**: ~$1 API (inference-only; no GPU retraining).
- **Result decomposition**: per-variant × detector AUPRC delta vs raw
  baseline. Distinguishes "marking helps generically" from "specific
  variant operative."
- **HF Space interactive demo** (per plan §6.3 + Lane 3 playbook):
  reader-toggle between delimit/datamark/encode; reads as Ch 10
  case-study.
- **Round 20 API pivot**: dataclasses (not SimpleNamespace) per v0.47;
  see [ADR-045](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md).

## Cross-references

- Plan §1 Round 1 Q4; plan §5 (Lane 3 hypothesis); plan §6.3 (HF Space demo)
- Lane execution playbook §3 (`portfolio-lane-execution-playbooks.md`)
- [ADR-045](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md) (v0.47 dataclass API)
- Hines et al. 2024 (Spotlighting); compass `claim_family=structural_defenses`
