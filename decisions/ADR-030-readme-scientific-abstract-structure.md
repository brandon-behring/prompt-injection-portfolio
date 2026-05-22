---
adr_id: "030"
slug: readme-scientific-abstract-structure
title: "README scientific-abstract-scaled structure + educational pre-alpha banner"
date: 2026-05-19
status: Accepted
linked_round: "R4"
plan_section: "§10 (README + banner)"
---

# ADR-030: README structure + pre-alpha banner

## Status

Accepted; **L2 exec-summary collapsed into L0 README per Round 17
follow-up Q2** (user: "That can go in the readme").

## Context

Portfolio's README is the L0 60-second-scan surface for ALL audiences
arriving at GitHub. Three failure modes for a 5-min-read README:

- **Generic project README** ("install + run") — fails recruiters who
  want methodology + findings in 60 seconds.
- **Academic abstract only** — fails engineers who need install path +
  Quick Start.
- **Marketing-style README** — fails researchers who want auditable
  citations.

The "scientific-abstract-scaled" framing (Problem → Why → Approach →
Results → Supporting) serves all three audiences in scan-then-deep-dive
form.

Round 17 follow-up Q2 absorbed the L2 exec-summary into L0 because
the README's exec-summary section is already serving that audience —
no separate `book/src/content/frontmatter/exec-summary.mdx` needed.

## Decision

README structure (scientific-abstract-scaled; per plan §10):

1. **Pre-alpha banner** (top; educational-framed per Q5''') — explains
   what pre-alpha means + build-in-public feed pointers.
2. **Problem** — 1 paragraph: prompt-injection detection's OOD wall.
3. **Why this matters** — 1 paragraph: production incidents (EchoLeak)
   + the methodology question.
4. **Approach** — 1 paragraph: 6 lanes; library-first; 3-guide book.
5. **Headline results** — bulleted; cites submission's findings +
   portfolio's open questions; per-lane status + freshness badge.
6. **Three peer-level entry-points** (per Round 17 follow-up Q3):
   textbook + narrative + academic routes side-by-side; reader picks.
7. **Supporting** — install path + Docker T2 + dossier link + plan link
   + dossier `claim_family` index entry + roadmap + CHANGELOG.

Pre-alpha banner copy:

> *Status: pre-alpha — under active development. This portfolio is a
> live build-in-public research project. v0.1.0 marks M0 close (M0
> deliverables shipped); subsequent milestones track lane completions
> through M7 / v0.7.0 textbook ratify. See `docs/build-in-public/` for
> weekly progress.*

## Consequences

- **L2 exec-summary REMOVED** from `book/src/content/frontmatter/`;
  README's exec-summary section serves the 5-min-scan audience (per
  Round 17 follow-up Q2).
- **3 peer-level entry-points** (per Round 17 follow-up Q3) — shared
  exec-summary across all 3 guides via this single README link
  pattern.
- **Pre-alpha banner state**: active until M7 textbook ratify
  (per [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md)).
- **Educational framing** of pre-alpha (vs apologetic) explains *what*
  pre-alpha means in this context, links to the build-in-public feed.

## Cross-references

- Plan §10 (README structure); Round 17 follow-up Q2/Q3
- [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md) (banner state machine)
- [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md) (3 entry-points)
- [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md) (build-in-public feed)
