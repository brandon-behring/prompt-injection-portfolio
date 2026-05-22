---
adr_id: "019"
slug: chapter-authoring-workflow
title: "Chapter authoring workflow: skeleton-first at M0 + just-in-time prose"
date: 2026-05-19
status: Accepted
linked_round: "R2"
plan_section: "§6.4"
---

# ADR-019: Chapter authoring workflow

## Status

Accepted.

## Context

Book authoring competes with experimental work for Claude session time.
Two extreme strategies fail:

- **Author all chapters upfront** — chapters cite results that don't exist
  yet; freshness badges all read `planned`; M7 user-verification gate
  reads as fiction not finding.
- **Author all chapters post-M7** — single huge authoring sprint at M7;
  no chance to iterate on framing; build-in-public posts cite chapter
  states that don't exist.

Submission's chapter-authoring experience (`docs/benchmark/{01-04}.ipynb`
notebooks + supporting WRITEUP) suggests a middle path: scaffold
skeletons early; fill prose just-in-time when results land.

## Decision

Chapter authoring follows skeleton-first + JIT pattern:

1. **M0 Day 14** — 13 textbook chapter skeletons shipped (per Round 17
   Q4 textbook-only scope); freshness badges `scaffolded` per
   [ADR-032](ADR-032-7-state-status-adoption-from-scaffold.md).
2. **Per-milestone (M1-M6)** — chapter receiving the corresponding lane's
   results promotes to `prose_only` then `implemented`. Fragment files at
   `book/src/content/fragments/lane-N/{methodology,results,interpretation}.mdx`
   hold experiment data (per Round 17 Q2 shared-substrate pattern); each
   guide's chapter MDX imports + sequences fragments with guide-specific
   framing prose.
3. **M7 coherence-edit pass** — user reads textbook L3 chapters
   end-to-end; Claude fixes inconsistencies; freshness → `locked`;
   pre-alpha banner removed; v0.7.0 tag.
4. **v0.8.0 (~month 13)** — narrative guide chapters scaffold + write
   using same fragments (Round 17 Q3 sequential rollout).
5. **v0.9.0 (~month 14)** — academic IMRaD guide chapters scaffold + write
   using same fragments.

## Consequences

- **Round 17 textbook-only scope**: M0 ships TEXTBOOK chapter skeletons
  only; narrative + academic skeletons defer to v0.8+ / v0.9+ respectively.
- **Fragment maintenance discipline** (per Round 17 Q2 + test-contract
  `experiment_records_complete` per
  [ADR-012](ADR-012-test-contracts.md)): experiment data changes go to
  fragments ONLY; framing prose stays in guide-specific chapters.
- **Build-in-public cadence** matches per-milestone badge promotions
  (per [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md));
  weekly thread cites chapter freshness transitions.
- **No fiction in chapters at any time**: skeletons cite plan + dossier
  but never invent results; freshness badge always reflects truth.

## Cross-references

- Plan §6.4 (chapter authoring workflow); plan §6.6 (3-guide architecture)
- [ADR-032](ADR-032-7-state-status-adoption-from-scaffold.md) (7-state freshness)
- [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md) (3-guide architecture)
- `portfolio-chapter-outlines.md` (per-chapter scaffolding state)
