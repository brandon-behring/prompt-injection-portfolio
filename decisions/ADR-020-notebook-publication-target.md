---
adr_id: "020"
slug: notebook-publication-target
title: "Notebook publication target: inside book/src/content/notebooks/"
date: 2026-05-19
status: Accepted
linked_round: "R2"
plan_section: "§6.3"
---

# ADR-020: Notebook publication target

## Status

Accepted.

## Context

T3 notebooks (per [ADR-018](ADR-018-reproducibility-tier-ladder.md))
serve interactive deep-dives for Ch 5 bootstrap walkthrough + Ch 6
threshold-policy + Ch 8 char-injection matrix + Ch 9 attribution + Ch 11
stacker + Ch 12 activation probe.

Three plausible publication targets:

- **Repo root `notebooks/`** — conventional Python project layout;
  separate from book; risks notebook/book drift.
- **Inside `book/src/content/notebooks/`** — co-located with the
  chapters that cite them; Astro renders them via
  `scripts/render-notebooks.mjs`; pagefind-indexable.
- **External (e.g., GitHub Gist + Colab links)** — easy to share; but
  splits the artifact graph + breaks reproducibility self-containment.

Scaffold v3.5+ ships notebook rendering as a first-class consumer
feature; co-location is the well-supported path.

## Decision

Notebooks live at **`book/src/content/notebooks/`** as jupytext-paired
`.py` (canonical) + `.ipynb` (rendered) files. Astro routes:
`/notebooks/[slug]`. Each chapter that has a companion notebook links
via the scaffold's `<Cite>` or chapter cross-reference component.

Workflow:

1. Authoring + editing in `.py` (jupytext-paired) for clean git diffs.
2. `make book-notebooks-render` regenerates `.ipynb` outputs via
   `scripts/render-notebooks.mjs`.
3. **nbval CI gate** (per [ADR-012](ADR-012-test-contracts.md) +
   plan §13) validates notebooks execute cleanly + output cells match
   expected fixtures.
4. Round 17 update: notebooks are SHARED across 3 guides — textbook +
   narrative + academic all link to the same notebook URL.

## Consequences

- **Search-indexable**: pagefind indexes notebook prose alongside chapter
  prose; reader searches surface relevant notebooks.
- **Reproducibility surface**: T3 tier per
  [ADR-018](ADR-018-reproducibility-tier-ladder.md) is operationalized
  via this co-location.
- **Notebook + chapter parity**: chapter freshness badge tracking
  (per [ADR-032](ADR-032-7-state-status-adoption-from-scaffold.md))
  applies to notebook + chapter as a unit.
- **Submission notebook reference** (per
  [ADR-034](ADR-034-notebooks-reference-submission-as-foundation.md)):
  portfolio adds NEW notebooks; references submission's 4 foundational
  notebooks where applicable.

## Cross-references

- Plan §6.3 (T3 notebooks); plan §13 (nbval CI gate)
- [ADR-018](ADR-018-reproducibility-tier-ladder.md) (T0-T3 ladder)
- [ADR-034](ADR-034-notebooks-reference-submission-as-foundation.md) (submission reference)
- [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md) (3-guide shared notebook)
