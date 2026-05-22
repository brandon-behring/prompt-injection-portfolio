---
adr_id: "025"
slug: community-feedback-window
title: "v0.7.0 → v1.0.0 community feedback window: 3-4 months"
date: 2026-05-19
status: Accepted
linked_round: "R3"
plan_section: "§8.5"
---

# ADR-025: v0.7.0 → v1.0.0 community feedback window

## Status

Accepted; **extended from 3mo to ~3-4mo by Round 17 Q3** to accommodate
sequential ship of narrative (v0.8.0) + academic (v0.9.0) guides.

## Context

Submission's "ship then forget" model fails portfolio's hiring-narrative
context: a v1.0.0 tag without a community-feedback window reads as a
toy project. Conversely, an indefinite "always pre-alpha" tagline never
crosses the citable threshold.

A bounded community-feedback window resolves this:

- **Long enough** to incorporate feedback + ship sequential guides
  (narrative v0.8.0 + academic v0.9.0 per Round 17 Q3).
- **Short enough** to converge to a citable v1.0.0 within a hiring-cycle
  timeline (~16-17 months from M0).

## Decision

3-4 month community feedback window post-M7:

- **M7 (week 13-14)** — v0.7.0 textbook ratified; pre-alpha banner
  removed on textbook routes; community feedback intake begins.
- **v0.7.x patches** (months 1-3 post-M7) — accept GitHub Issues + PRs
  for typos, citation fixes, clarifications; no new lanes; no
  methodology changes that supersede locked ADRs.
- **v0.8.0 (~month 13, ~1mo post-M7)** — narrative guide ships per
  [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md);
  quiet ship per Round 19 Q2.
- **v0.9.0 (~month 14, ~2mo post-M7)** — academic IMRaD ships; quiet
  ship.
- **v1.0.0 (~month 16-17, ~3-4mo post-M7)** — all 3 guides polished +
  citable; LOUD announcement; freshness badges definitively `locked`.
- **Post-v1.0.0**: maintenance mode; v1.0.x patches for critical bugs
  only; v2.0 ideas documented in NEXT_SESSION.md only (no active
  commitment).

## Consequences

- **Hiring narrative**: v0.7.0 ratifies the methodology lock; v1.0.0 is
  the citable / hiring-discussion artifact.
- **Round 17 extension**: 3mo → 3-4mo absorbed the narrative + academic
  authoring time (~30-50h each); calendar timeline shifts +1mo.
- **Build-in-public cadence** continues at monthly volume during the
  window (per [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md));
  v0.8.0 + v0.9.0 are "quiet" ships per Round 19 Q2 to reserve the loud
  push for v1.0.0.
- **No v2.0 plans** during this window — protects the community-feedback
  surface from scope drift.

## Cross-references

- Plan §8.5 (maintenance commitment); plan §13 (M7 + v0.8.0 + v0.9.0 + v1.0.0 ship gates)
- [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md) (3-guide architecture)
- [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md) (loudness policy)
- Round 17 Q3 (sequential rollout); Round 19 Q2 (quiet ship)
