---
adr_id: "024"
slug: public-from-m0-pre-alpha-banner
title: "Public from M0 + pre-alpha banner until v0.7.0"
date: 2026-05-19
status: Accepted
linked_round: "R3"
plan_section: "§8.1"
---

# ADR-024: Public from M0 + pre-alpha banner

## Status

Accepted.

## Context

Repo visibility timing has two extremes:

- **Private until v0.7.0** — clean reveal; but loses build-in-public
  framing + recruiter signal during the 13-14 week development window.
- **Public from M0** — full development visible; risk that early-state
  scaffolding misreads as "broken" or "incomplete."

The pre-alpha banner pattern (common in npm + scientific software)
resolves the tension: public from day 1 with explicit "this is under
active development" framing.

## Decision

- **Public on GitHub from M0** — `gh repo create --public
  prompt-injection-portfolio` at Day 1.
- **Pre-alpha banner active** on README + book frontmatter
  (`book/src/content/frontmatter/pre-alpha-banner.mdx`) until M7
  textbook-ratify (v0.7.0).
- **`PreReleaseBanner.astro` scaffold component** (per Round 12
  Q2''''''''') renders the banner from config:
  `<PreReleaseBanner state="alpha" dismissAt="v0.7.0" />`
- **Banner removal** on textbook routes at v0.7.0; narrative + academic
  routes carry their own pre-ship banners until their respective
  v0.8.0 / v0.9.0 ship dates.
- **v1.0.0 = all 3 guides polished + citable** — no banner anywhere; the
  v1.0.0 tag is the citable / hiring-discussion artifact.

## Consequences

- **Visibility timeline** (per plan §8.1):
  - M0-M6 (weeks 1-12): public; pre-alpha banner; develops in open
  - M7 (week 13-14): textbook banner removed; narrative + academic
    routes carry "shipping at v0.8.0 / v0.9.0" placeholders
  - v0.8.0 (~month 13): narrative banner removed
  - v0.9.0 (~month 14): academic banner removed
  - v1.0.0 (~month 16-17): all 3 polished + citable
- **`README.md` pre-alpha framing** (per
  [ADR-030](ADR-030-readme-scientific-abstract-structure.md)):
  educational pre-alpha banner with build-in-public feed pointers.
- **Build-in-public bootstrap** at M0 ([ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md))
  reads the pre-alpha banner state into thread framing.
- **First green CI push from Day 1** matches the public expectation:
  even at pre-alpha, the gates are green.

## Cross-references

- Plan §8.1 (visibility timeline)
- [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md) (build-in-public)
- [ADR-030](ADR-030-readme-scientific-abstract-structure.md) (README structure)
- Round 12 Q2''''''''' (`PreReleaseBanner.astro` reusable component)
