---
adr_id: "044"
slug: three-guide-architecture-with-shared-substrate
title: "3-guide architecture (textbook + narrative + academic IMRaD) + shared substrate authoring"
date: 2026-05-21
status: Accepted
linked_round: "R17"
plan_section: "§6.6 + §13"
---

# ADR-044: Three-guide architecture

## Status

Accepted (Round 17 lock; 4 follow-up `/exploring-options` rounds folded in).

## Context

User complaint at Round 17: "submission's Quarto hub-and-spoke ... has
neither a narrative structure nor an academic structure like a journal
paper — random parts of the results all over the place with no story."
Submission's reviewer-driven design maximized auditability at the cost
of narrative cohesion. Portfolio is open-ended → can do better.

## Decision

Portfolio ships **3 separate guides** instead of 1 book, each targeting
a different reader/use-case:

1. **Textbook** (`book/src/content/textbook/`; v0.7.0 M7): self-contained
   chapters; modular learning; KF triadic R/O/E per scaffold pedagogy.
2. **Narrative** (`book/src/content/narrative/`; v0.8.0): "Can we climb
   the wall?" story arc; heavy cross-chapter threading; recruiter-friendly.
3. **Academic IMRaD** (`book/src/content/academic/`; v0.9.0): journal-
   paper structure (Introduction → Background → Methods → Results →
   Discussion → Future Work); reviewer-defense-ready.

**Implementation**: ONE Astro book + 3 subsite folders per Round 17 Q1.
Single npm build; shared infrastructure (callouts, BibTeX, KaTeX,
PreReleaseBanner per scaffold v3.5 research-portfolio preset). Each
guide has its own TOC + nav + audience routing.

**Authoring pattern** (Round 17 Q2 shared-substrate): each lane has
fragments at `book/src/content/fragments/lane-N/{methodology,results,
interpretation}.mdx` — single source of truth for experiment data +
citations. Each guide's chapter MDX imports + sequences fragments with
guide-specific framing prose. ~1x data-write + 3x framing-write per lane.

**Sequential rollout** (Round 17 Q3): v0.7.0 textbook only → v0.8.0
narrative ship → v0.9.0 academic ship → v1.0.0 all 3 polished + citable.
Extends v0.7.0 → v1.0.0 window from 3mo to ~3-4mo.

**Round 17 follow-up locks**:
- Q1 M7 gate: textbook only at v0.7.0 (per-guide gates at v0.8/v0.9).
- Q2 v0.8/v0.9 ship: quiet (CHANGELOG only); only v1.0.0 = big announcement.
- Q3 model card pointers: update at each guide ship (3-link section at v1.0.0).
- Q4 cost commitment: best-effort within v0.7.0 → v1.0.0 window.

## Consequences

- M0 Day 14 chapter skeletons = TEXTBOOK ONLY (13 chapters at
  `book/src/content/textbook/`). Narrative + academic scaffold at
  v0.8+ / v0.9+.
- README's top-fold "3 ways to read this work" section (per Day 15
  governance polish) is the L0 entry-point routing the 3 guides.
- L2 book exec-summary collapsed into L0 README per Round 17 follow-up
  Q2 ("That can go in the readme"); no separate exec-summary.mdx.
- Test contract `experiment_records_complete` extended to verify 3
  fragment files per lane at lane CLOSE (per Round 17 follow-up Q2).
- v0.7.0 → v1.0.0 window extends from 3mo to ~3-4mo.

## Cross-references

- Round 17 Q1-Q4 + 3 follow-up Q-rounds
- Plan §6.6 + §6.7 + §6.8 (per-guide ToC outlines)
- ADR-047 (Round 22 M0 finish-out; Day 14 textbook scaffold)
- Submission ADR-079 v1.3.0 two-guide reader architecture (smaller-scale
  analog that VALIDATES portfolio's 3-guide direction)
