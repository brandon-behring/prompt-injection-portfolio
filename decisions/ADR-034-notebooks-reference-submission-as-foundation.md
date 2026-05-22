---
adr_id: "034"
slug: notebooks-reference-submission-as-foundation
title: "Notebooks: reference submission's 4 as foundation; portfolio adds NEW analyses only"
date: 2026-05-19
status: Accepted
linked_round: "R5"
plan_section: "§6.3"
---

# ADR-034: Notebooks reference submission as foundation

## Status

Accepted.

## Context

Submission ships 4 foundational jupytext notebooks at
`docs/benchmark/{01-04}.ipynb` (LODO methodology + bootstrap analysis +
threshold policy + reference scorer comparison). Three strategies for
portfolio's notebook surface:

- **Duplicate submission notebooks** in portfolio — diverges over time;
  reader sees two versions of "the same" analysis.
- **Skip submission analyses entirely** — portfolio notebooks omit
  foundational analyses; readers lack context.
- **Reference submission's 4 + add NEW portfolio analyses only** —
  cite-as-foundation pattern; portfolio's surface is incremental.

The Round 5 reframing ("next version built from submission's
experience, done cleaner") + [ADR-017](ADR-017-submission-patch-policy.md)
(submission ADRs frozen) argue for the reference pattern.

## Decision

Portfolio notebooks reference submission's 4 foundational notebooks +
add only NEW analyses:

- **Foundation references** (cite submission's
  `docs/benchmark/{01-04}.ipynb` via book chapter `<Cite>` + link;
  link points to submission's rendered version on its Quarto/Astro site).
- **Portfolio NEW notebooks** (per plan §6.3):
  - Ch 5 bootstrap-CI walkthrough (extends submission's bootstrap)
  - Ch 6 threshold-policy walkthrough (extends submission's threshold
    work + extends with APR metric per
    [ADR-037](ADR-037-apr-metric-lane-4.md))
  - Ch 8 char-injection-bypass matrix (NEW; 12-technique × N-detector
    grid)
  - Ch 9 attribution table (NEW; Lane 2 result attribution)
  - Ch 11 stacker analysis (NEW; Lane 4)
  - Ch 12 activation probe (NEW; Lane 5)

Notebook publication target per
[ADR-020](ADR-020-notebook-publication-target.md):
`book/src/content/notebooks/`.

## Consequences

- **No notebook duplication** — readers go to submission for foundational
  context; portfolio for new analyses.
- **Submission patch policy holds** — submission's 4 notebooks accept
  v1.0.x patches (per [ADR-017](ADR-017-submission-patch-policy.md));
  portfolio's references track the latest submission tag (per Round 22
  Q3 dynamic-detect).
- **Round 22 CI ref v1.3.0**: portfolio's cite to submission notebooks
  resolves at v1.3.0 reading-guide (which preserves the 4 benchmark
  notebooks per submission's two-guide architecture).
- **Future v0.8+ iteration**: portfolio may iterate on its NEW notebooks
  (e.g., extend Ch 8 matrix); this ADR doesn't lock incremental
  authoring.

## Cross-references

- Plan §6.3 (notebooks)
- [ADR-017](ADR-017-submission-patch-policy.md) (submission immutability)
- [ADR-020](ADR-020-notebook-publication-target.md) (publication target)
- [ADR-037](ADR-037-apr-metric-lane-4.md) (APR metric extension)
