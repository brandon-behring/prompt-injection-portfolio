---
adr_id: "031"
slug: book-scaffold-astro-consumption
title: "book-scaffold-astro consumption: academic profile + portfolio-local extras (reframed for v3.0 npm + v3.5 research-portfolio preset)"
date: 2026-05-19
status: Accepted
linked_round: "R5"
plan_section: "§6 + §10"
---

# ADR-031: book-scaffold-astro consumption strategy

## Status

Accepted (reframed twice: Round 6 v3.0 npm pivot; Round 21 v3.5
research-portfolio preset closure).

## Context

book-scaffold-astro is the 4th load-bearing library
([ADR-026](ADR-026-no-local-workarounds-policy.md)). Three consumption
strategies considered across Round 5 → Round 6 → Round 21:

- **Round 5 (Q1''''')** — GitHub-template fork at v2.0: copy scaffold's
  files into portfolio; freeze at v2.0 state. Pre-Round-6.
- **Round 6 (Q2''''')** — npm-package consumer at v3.0 (academic profile)
  + portfolio-local extras. v3.0 pivoted scaffold from GH-template to
  `npx @brandon_m_behring/create-book <name> --profile=...`.
- **Round 21 (Q1)** — npm-package consumer at v3.5 research-portfolio
  preset. MR-8 v3.5 closed shipping the research-portfolio preset
  (union of academic ∪ tools schema) + 4 new generalized components +
  recipe + chapter template — exactly the v3.2 schema portfolio
  designed in Round 12.

The Round 21 state resolves the Round 11 Q1'''''''' "wait for v3.2" blocker.

## Decision

Portfolio consumes scaffold v3.5+ via npm:

1. **Bootstrap**: `npx @brandon_m_behring/create-book
   prompt-injection-portfolio --profile=research-portfolio` (Day 1 M0).
2. **Pin**: `book/package.json: "@brandon_m_behring/book-scaffold-astro":
   "^3.5.0"` per [ADR-046](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md).
   `npm update` picks up patches automatically within the caret range.
3. **Profile**: `research-portfolio` (per Round 12 Q1''''''''' design;
   shipped in v3.5.0 via MR-8 closure).
4. **Portfolio-local extras**: anything NOT in the research-portfolio
   preset that portfolio specifically needs lives in
   `book/src/components/portfolio/`; if any such extra would be
   reusable across research portfolios, file scaffold issue + upstream
   per [ADR-026](ADR-026-no-local-workarounds-policy.md).
5. **3 new reusable components** (per Round 12 Q2''''''''') ship as
   scaffold primitives: `PreReleaseBanner.astro` + `PolicyRef.astro` +
   `AICollaborationDisclosure.astro` — portfolio passes specific props
   at consumption.

## Consequences

- **Round 11 Q1'''''''' M1 chapter authoring blocker RESOLVES** at
  Round 21 (per [ADR-046](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md));
  Day 14 textbook skeleton authoring unblocked at M0.
- **No GitHub-template fork** — clean npm-consumer relationship.
- **`npm update` propagates scaffold fixes** to portfolio
  automatically; portfolio reads scaffold CHANGELOG on upgrades.
- **Round 12 Q2''''''''' design** is encoded in scaffold v3.5.0+ as
  reusable components; portfolio's local impl at v0.1.0 IS the
  prototype that motivated the upstream design.

## Cross-references

- Plan §6 (book design); plan §10 (MR-8 — closed via v3.5.0)
- [ADR-026](ADR-026-no-local-workarounds-policy.md) (library-first invariant)
- [ADR-046](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md) (Round 21 pin)
- [ADR-029](ADR-029-book-callout-citation-infrastructure.md) (scaffold-provided primitives)
- [ADR-035](ADR-035-portfolio-clean-t0-strategy.md) (Round 6 reframing companion)
