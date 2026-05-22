---
adr_id: "021"
slug: ai-assistance-disclosure
title: "AI-assistance disclosure in book frontmatter + commits"
date: 2026-05-19
status: Accepted
linked_round: "R3"
plan_section: "§6.1 + §8.3"
---

# ADR-021: AI-assistance disclosure

## Status

Accepted.

## Context

Portfolio is developed in active collaboration with Claude (Anthropic).
Public-from-M0 visibility ([ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md))
+ build-in-public cadence ([ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md))
mean every step of the work is visible. Honest disclosure matches both
the ethics-of-AI-research norm + Anthropic's Commercial Service
Agreement obligations.

Three surface points for disclosure:

- **Book title page** — sole author "Brandon Behring" (per Round 3 Q1'').
- **Frontmatter `ai-assistance-disclosure.mdx`** — publisher-style
  paragraph describing the collaboration.
- **Commit trailer** — every commit ends with `Co-Authored-By: Claude
  <noreply@anthropic.com>` (per [ADR-011](ADR-011-commit-discipline.md)).

## Decision

Three-surface AI-assistance disclosure:

1. **Book title page** (`book/src/content/frontmatter/title-page.mdx`):
   sole author "Brandon Behring." No co-authorship attribution at the
   title page level — Brandon is the methodologist + decision-maker.
2. **Frontmatter `ai-assistance-disclosure.mdx`** (publisher-style):

   > *This book was developed in collaboration with Claude (Anthropic).
   > Claude assisted with literature review, methodology drafting, code
   > authoring, experiment design, and prose drafting. All experimental
   > work and methodology choices were directed by the human author;
   > Claude served as a research and writing collaborator throughout.
   > Detailed per-commit attribution is preserved via `Co-Authored-By:`
   > git trailers; the overall workflow is described in
   > `docs/build-in-public/` and the project's README.*

3. **Commit trailer**: `Co-Authored-By: Claude <noreply@anthropic.com>`
   on every commit (per [ADR-011](ADR-011-commit-discipline.md)).
4. **HF Hub model cards**: "Training methodology" section mentions the
   AI-assisted research workflow + links back to the frontmatter
   disclosure.

Citation format: `Behring, B. (2026). The OOD Wall: A Methodology Case
Study in Prompt-Injection Detection. https://...`

## Consequences

- **Disclosure surface** matches scientific publication norms
  (e.g., Nature Sept 2023 AI tool disclosure guidance).
- **Honest attribution chain** at multiple zoom levels: title page
  (sole author) → frontmatter (publisher-style paragraph) → commit
  (per-action trailer).
- **Citation tracking via Anthropic ToS**: Sonnet-generated outputs in
  ETHICS.md cite the Anthropic Commercial Service Agreement
  (per [ADR-022](ADR-022-ethics-and-hf-dataset-card.md) + ETHICS.md
  §4).
- **`AICollaborationDisclosure.astro`** scaffold component (per Round 12
  Q2''''''''') renders the disclosure paragraph from YAML config.

## Cross-references

- Plan §6.1 (frontmatter) + §8.3 (author identity)
- [ADR-022](ADR-022-ethics-and-hf-dataset-card.md) (ETHICS sibling)
- [ADR-011](ADR-011-commit-discipline.md) (commit trailer)
- Anthropic Commercial Service Agreement (cited in ETHICS.md §4)
