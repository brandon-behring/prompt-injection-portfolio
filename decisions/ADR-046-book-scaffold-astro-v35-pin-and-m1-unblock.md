---
adr_id: "046"
slug: book-scaffold-astro-v35-pin-and-m1-unblock
title: "book-scaffold-astro v3.5 pin + M1 book authoring unblock"
date: 2026-05-21
status: Accepted
linked_round: "R21"
plan_section: "Context + §3 + §21"
---

# ADR-046: book-scaffold-astro v3.5 pin + M1 unblock

## Status

Accepted (Round 21 lock; commit `bc30c52` Day 3a/c1 bumped pin alongside
eval-toolkit advance).

## Context

Round 21 cascade survey revealed book-scaffold-astro jumped v3.1.0 → v3.6.0
over the same 2-day window as eval-toolkit's v0.43-v0.47 cascade. Per
scaffold v3.5.0 CHANGELOG explicitly: "Unblocks downstream
prompt-injection-portfolio M1 book authoring." The scaffold maintainer
shipped the long-awaited `research-portfolio` preset (Round 12 design)
+ closed both portfolio-filed scaffold MRs.

## Decision

**Pin floor**: advance `book/package.json` `@brandon_m_behring/book-scaffold-astro`
from `^3.1.0` → `^3.5.0` per Round 21 Q1. Caret range allows v3.5.x +
v3.6.x patches; portfolio's chapter outlines don't currently need v3.6
katexMacros so option B (`^3.5.0`) over Recommended (`^3.6.0`).

**M1 book authoring**: UNBLOCKED per Round 21 Q2. The Round 11
Q1'''''''' v3.2 blocker resolves favorably — v3.5.0 ships the
research-portfolio preset (the Round 12 design as upstream-shipped).
Day 14 chapter skeletons proceed without further wait.

**MR closures**:
- MR-8 (book-scaffold-astro#6) CLOSED 2026-05-19T19:29:53Z by v3.5.0
- MR-9 (book-scaffold-astro#7) CLOSED 2026-05-19T19:04:30Z by v3.3+

## Consequences

- §21 Day 14 "WAITS for scaffold v3.2.0" REMOVED; pre-condition becomes
  "confirm book/package.json pins ^3.5.0".
- Day 14 chapter skeletons (13 chapters at `book/src/content/textbook/`)
  proceeded per Round 22 priority order (Day 14 batch shipped at
  commit `dcf037a`).
- Round 22 narrative documents the M1 unblock + remaining open MR set
  shrinks to MR-3 (research_toolkit#1) + new MR-12 (eval-toolkit#69
  Tier-2 Protocol consolidation; not blocking).
- Submission v1.3.0's two-guide reader architecture (ADR-079) was
  developed in parallel + validates portfolio's Round 17 3-guide
  direction at a smaller scale.

## Cross-references

- Round 11 Q1'''''''' (original v3.2 blocker; resolved by v3.5.0)
- Round 12 Q1-Q2 (v3.2 design spec; superseded by v3.5.0 actual)
- Round 21 Q1-Q2
- Plan §3 dependency policy + §10 library-first audit table
- Day 3a/c1 commit `bc30c52`
- ADR-044 (3-guide architecture; consumes scaffold preset)
