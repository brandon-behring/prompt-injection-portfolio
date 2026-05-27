---
adr_id: "051"
slug: "dogfood-driven-upstream-adoption-batch"
title: "Dogfood-driven adoption of eval-toolkit v1.x, research_toolkit v2.4.0, book-scaffold-astro v4.x"
date: 2026-05-26
status: Accepted
linked_round: "R26 (dogfooding adoption session)"
plan_section: "§10"
---

# ADR-051: Dogfood-driven upstream adoption batch

## Context

The three load-bearing upstream libraries had drifted ~2 majors ahead of the
portfolio's pins. Rather than a hygiene bump, the goal was **dogfooding**: adopt
the new versions by *using* them as a real consumer, surface friction, and feed
it back upstream as tracked issues (advances ADR-045 / ADR-046).

## Decision

- **eval-toolkit `>=0.47` → `>=1.0`** (lock resolves 1.2.0). Opts into the upstream
  v1.0 stability contract (their ADR 0003: Tier-1 API + 9 Protocols frozen for 1.x).
  No consumer code exists yet (`src/` placeholder) → dogfooding **deferred to M1**;
  this pass is pin + forward-guidance only.
- **research_toolkit reclassified as TOOLING, not a Python dependency.** Removed the
  vestigial `git+…@v1.9.1` dep (nothing imports it; it dragged docling/pdfplumber).
  `make dossier-audit` now bootstraps a repo-local clone pinned to `v2.4.0`
  (`.tooling/research_toolkit`, gitignored) and runs validators in an ephemeral
  `uv` env (PyYAML only) — reproducible, lean, no torch.
- **book-scaffold-astro `^3.6.5` → `^4.4.0`** (resolves 4.5.1) **+ switch to the
  `research-portfolio` profile.** v4's `defineStyle` architecture: `styles:
  [researchPortfolioStyle]` in `astro.config.mjs`; `defineBookSchemas({ preset:
  'research-portfolio', chaptersBase: './src/content/textbook' })` in
  `content.config.ts` (BOOK_PROFILE env is dead in v4).
- **runpod-deploy unchanged** — `>=0.8.4` already equals PyPI latest (the GitHub
  Releases page lagged PyPI; not an unsatisfiable pin).

## Consequences

- Consumer fixes the build forced: per-chapter `freshness` values (the blanket
  `exploratory` was invalid *and* conflated freshness-vs-status); added the
  **required** `last_verified` to all 13 chapters; converted HTML comments
  (`<!-- -->`) to MDX (`{/* */}`) in 6 chapters. Book builds green; 13 chapters
  validate under research-portfolio.
- **Dogfooding friction filed upstream (issues-only):** see
  `upstream_issues.md` — book-scaffold `last_verified`-required-not-optional +
  `book-scaffold validate` CLI ignoring `preset`/`chaptersBase` (reports
  profile=minimal); research_toolkit docling/pdfplumber as hard deps for
  validator-only consumers + evidence_ledger validator can't distinguish
  "cache not populated (re-fetchable)" from a broken anchor.
- **Lane 2 `/dataset-synthesize` stays designated-but-gated** on research_toolkit
  #21/#22/#23 (silent-failure + install gaps); no reliance until they close.
- `make dossier-audit` full pass now requires the populated body-text cache
  (`~/Claude/research_cache`), a heavy re-fetchable artifact — like torch, a CI /
  cache-present concern, not a clean-checkout gate.
- Verification was lightweight-local (contracts + book build + validator mechanism)
  per the chosen posture; full `uv sync` (torch) + cache population stay in CI.
