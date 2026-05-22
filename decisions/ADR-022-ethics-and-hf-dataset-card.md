---
adr_id: "022"
slug: ethics-and-hf-dataset-card
title: "ETHICS.md + HF Hub dataset card with dual-use disclosure"
date: 2026-05-19
status: Accepted
linked_round: "R3"
plan_section: "§8.4"
---

# ADR-022: ETHICS.md + HF Hub dataset card dual-use disclosure

## Status

Accepted.

## Context

Portfolio publishes synthetic adversarial training data
(`BBehring/prompt-injection-synthetic-indirect-v2`; per
[ADR-009](ADR-009-hf-hub-naming-scheme.md)). This data could be misused
for attacker training even though it's intended for detector training.

Dual-use disclosure is required by:

- Norms in security research (responsible-release framing).
- Anthropic Commercial Service Agreement (Sonnet outputs redistributed
  for research require attribution + responsible-use guidance).
- HF Hub dataset card guidelines (`task_categories` + `tags` + restricted-use
  notes).

The submission lacked an explicit ETHICS surface — portfolio remediates
at M0.

## Decision

Portfolio publishes a 6-section `ETHICS.md` (plan §8.4):

1. **Dual-use disclosure** — synthetic adversarial data could be misused;
   intended for detector training, not attacker training.
2. **Intended use** — research, detector development, defensive evaluation.
3. **Responsible use** — recommendations against production attacker training.
4. **Anthropic ToS compliance** — Sonnet-generated outputs redistributed
   per Anthropic Commercial Service Agreement for research purposes
   with attribution.
5. **Citation guidance**.
6. **Reporting concerns** — security@brandon-behring.com or equivalent
   contact for security/ethics issues.

HF Hub dataset card `BBehring/prompt-injection-synthetic-indirect-v2`:
- `task_categories: ["text-classification"]`
- `tags: ["prompt-injection", "research-use", "responsible-ai"]`
- Restricted-use note in frontmatter
- Cross-link back to portfolio's `ETHICS.md`

## Consequences

- **`PolicyRef.astro` scaffold component** (per Round 12 Q2''''''''')
  enables `<PolicyRef file="ETHICS.md" section="dual-use">` cites from
  any book chapter — generic cross-document citation primitive.
- **Lane 1b chapter sidenote** (per Round 17 + chapter outline Ch 8)
  cites ETHICS dual-use specifically when discussing the 12 character-
  injection techniques (which double as evasion + research tool).
- **Round 8 ADR-041** ratifies the ETHICS content lock specifically;
  this ADR establishes the architectural decision (ETHICS surface
  exists + 6-section structure); ADR-041 locks the actual content.
- **SECURITY.md cross-reference** (per [ADR-028](ADR-028-community-governance.md))
  links ethics + security concerns reporting paths.

## Cross-references

- Plan §8.4 (ethics + dual-use disclosure)
- [ADR-041](ADR-041-ethics-content-lock.md) (Round 8 content lock)
- [ADR-028](ADR-028-community-governance.md) (SECURITY cross-ref)
- [ADR-021](ADR-021-ai-assistance-disclosure.md) (AI-assistance disclosure sibling)
