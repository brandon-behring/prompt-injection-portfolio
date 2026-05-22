---
adr_id: "029"
slug: book-callout-citation-infrastructure
title: "Book callout + citation infrastructure via scaffold v3.5+ academic profile"
date: 2026-05-19
status: Accepted
linked_round: "R4"
plan_section: "§6"
---

# ADR-029: Book callout + citation infrastructure

## Status

Accepted (reframed in Round 6 + Round 21 for v3.5 scaffold).

## Context

Portfolio's 3-guide architecture ([ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md))
needs uniform callout + citation infrastructure across textbook +
narrative + academic guides. Two strategies:

- **Hand-rolled per-guide** — portfolio implements its own
  `<Cite>` + `<MarginNote>` + `<KeyIdea>` + ~18 callouts; ~30-50h dev.
- **Consume scaffold's** — scaffold v3.5 academic + research-portfolio
  presets already ship all primitives (per Round 6 Q2''''' + Round 21
  MR-8 closure).

The library-first invariant ([ADR-026](ADR-026-no-local-workarounds-policy.md))
+ scaffold's parity-with-portfolio-needs (MR-8 v3.5 closure) make the
consume-scaffold path correct.

## Decision

Portfolio consumes scaffold v3.5+ as the callout + citation
infrastructure layer:

- **18 typed callouts** (8 original + 10 academic): SkillBox + CaseStudy
  + ConceptBox + KeyIdea + TryThis + Recovery + Convergence + Divergence
  + NoteBox + ExampleBox + DynConnect + InsightBox + WarnBox + CounterBox
  + TipBox + OpenQuestion + PaperBox + ResultBox.
- **Theorem family (8)**: theorem / proposition / lemma / corollary /
  definition / example / exercise / remark via amsthm-style.
- **KaTeX math** via `remark-math` + `rehype-katex`; 36-macro custom
  library bundled with scaffold; Round 21 v3.6 adds `katexMacros`
  consumer option (not adopted by portfolio at v0.1.0).
- **BibTeX pipeline**: `scripts/build-bib.mjs` via citation-js converts
  `book/bibliography.bib` → `src/data/references.json`; `<Cite key="...">`
  component with hyperlinked references on generated `references.astro`
  page.
- **`<MarginNote>`** for Tufte sidenotes alongside `<Cite>` for inline
  citations.
- **Pre-flight validator** `scripts/validate.mjs` catches typo'd bibkeys,
  XRef slugs, figure paths.
- **`Cite`-from-`claim_family`** discipline: every L3 prose claim
  cites a dossier `claim_family` key via `<Cite>` against the
  corresponding bibtex entry; one citation graph from dossier → book.

## Consequences

- **Scaffold v3.5 pin** via `book/package.json: ^3.5.0` per Round 21 Q1
  (per [ADR-046](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md));
  `npm update` picks up patches within caret range.
- **Bibliography seeded 1:1 from dossier**: each `claim_family` key
  becomes a bibtex entry in `book/bibliography.bib` (Day 18 task per
  plan §9; deferred per dossier sprint timing).
- **Round 12 Q2''''''''' 3 new reusable components**: `PreReleaseBanner` +
  `PolicyRef` + `AICollaborationDisclosure` ship as scaffold primitives
  (research-portfolio preset); portfolio passes specific props at
  consumption.
- **Hand-rolled equivalents NOT permitted** per
  [ADR-026](ADR-026-no-local-workarounds-policy.md); if a callout is
  missing, file scaffold issue + wait for ship.

## Cross-references

- Plan §6 (book design — scaffold pedagogy)
- [ADR-031](ADR-031-book-scaffold-astro-consumption.md) (scaffold consumption strategy)
- [ADR-046](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md) (v3.5 pin)
- [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md) (3-guide architecture)
