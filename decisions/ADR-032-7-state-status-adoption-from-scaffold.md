---
adr_id: "032"
slug: 7-state-status-adoption-from-scaffold
title: "Adopt scaffold's 7-state freshness machine"
date: 2026-05-19
status: Accepted
linked_round: "R5"
plan_section: "§2 Tier-5"
---

# ADR-032: 7-state freshness machine adoption

## Status

Accepted (Round 5 Q2''''; replaces prior 4-state framing).

## Context

Portfolio needs a per-chapter / per-notebook freshness badge that
honestly signals state through the M0 → M7 → v1.0.0 lifecycle. Two
options:

- **Custom 4-state** — `exploratory` → `experimental-result` → `locked`
  → `superseded` (initial plan §2 Tier-5 framing).
- **Scaffold's 7-state** — `implemented` / `chapter_only` / `reading_only`
  / `prose_only` / `code_only` / `scaffolded` / `planned`.

The 7-state captures finer distinctions (chapter prose ready vs notebook
code ready vs both vs neither) that matter for build-in-public framing
+ M7 verification gate granularity. The 4-state collapses several
useful distinctions.

The pre-alpha banner is orthogonal — it's a repo-wide dimension, not a
per-chapter state.

## Decision

Adopt scaffold's 7-state freshness machine:

- **`planned`** — chapter exists in TOC only; no skeleton.
- **`scaffolded`** — skeleton with KF R/O/E section headers + frontmatter;
  no prose.
- **`chapter_only`** — chapter prose drafted; no companion notebook.
- **`reading_only`** — citations + prose in place; no code/experimental
  results yet.
- **`code_only`** — companion notebook implemented + tested; chapter
  prose still skeleton/partial.
- **`prose_only`** — chapter prose complete; notebook still planned or
  code_only.
- **`implemented`** — chapter + companion notebook both complete +
  cross-referenced + validated.

Pre-alpha banner = separate dimension (per
[ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md)); applies
repo-wide until M7 textbook ratify.

`<StatusBadge>` component (scaffold-provided) renders state from chapter
frontmatter.

## Consequences

- **Per-chapter freshness in scaffold v3.5+** is first-class; portfolio
  doesn't hand-roll badge logic per
  [ADR-026](ADR-026-no-local-workarounds-policy.md).
- **M0 Day 14 textbook chapter skeletons** (per Round 17 Q4 +
  [ADR-019](ADR-019-chapter-authoring-workflow.md)) ship with freshness
  `scaffolded`.
- **M7 textbook ratify** advances all textbook chapters to
  `implemented`; pre-alpha banner removed on textbook routes
  per [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md).
- **Narrative + academic guides** carry their own freshness through
  v0.8.0 / v0.9.0 ship dates; v1.0.0 has all 3 guides at `implemented`.
- **Build-in-public surface**: weekly thread cites chapter freshness
  transitions (per [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md)).

## Cross-references

- Plan §2 Tier-5 (hierarchical-depth claim register)
- [ADR-019](ADR-019-chapter-authoring-workflow.md) (skeleton-first workflow)
- [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md) (pre-alpha banner dimension)
- [ADR-031](ADR-031-book-scaffold-astro-consumption.md) (scaffold v3.5 source of 7-state machine)
