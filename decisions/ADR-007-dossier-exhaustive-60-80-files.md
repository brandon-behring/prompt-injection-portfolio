---
adr_id: "007"
slug: dossier-exhaustive-60-80-files
title: "Dossier target: exhaustive ~60-80 files"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q6 + §4"
---

# ADR-007: Dossier target — exhaustive ~60-80 files

## Status

Accepted.

## Context

The dossier (`docs/research/`) is the L5 ground-truth layer per plan
§2 Tier-5 hierarchical-depth architecture. It anchors every L3 chapter
claim + every L4 experiment-record hypothesis via `claim_family` keys.

Three plausible sizing choices:

- **Light (~20-30 files)**: faster; covers headline topics; risks
  shallow citation density (fewer than ~3-5 anchor papers per
  `claim_family`).
- **Medium (~40-50 files)**: middle ground; covers most chapters.
- **Exhaustive (~60-80 files)**: covers all 11 sub-areas per plan §4
  (per-paper deep dives + per-benchmark deep dives + commercial-detector
  survey + production-incident corpus + critique literature).

The portfolio's "next version done cleaner" framing (Round 5) +
hierarchical-depth verification gate (user reads L3-L5) demand the
exhaustive sizing — shallower dossier means shallower chapter prose.

## Decision

Dossier target: **exhaustive ~60-80 files** across 11 sub-areas, per
plan §4 (3 compass artifacts → `_inbox/` decomposition →
`research_toolkit`'s `/research-gather` + `/dossier-build` skills →
`/dossier-audit` integrity gate).

Workflow:

1. Compass artifacts at `~/Downloads/compass_artifact_*.md` (~1055 lines
   total) seed the work.
2. Decomposition into `claim_family`-keyed structured files.
3. Per-family deep dives via research_toolkit skills.
4. Audit via `make dossier-audit`.

## Consequences

- **Dossier sprint** = M0 Days 6-12 (~25-40h Claude session); per Round 22
  Q2 deferred to user-led session on a separate Anthropic account.
- **`claim_family` key naming**: domain-prefixed lowercase
  (e.g., `ood_evaluation_methodology`, `adversarial_robustness`,
  `direct_injection`, `production_incidents`). Each L3 chapter cites
  by family key; the dossier `MANIFEST.json` is the resolution table.
- **Test-contract**: `dossier_integrity` (per plan §13) verifies
  `make dossier-audit` clean before M7 ratify.
- **Test contract** + audit catch dossier drift (claim_family rename;
  citation orphans; missing anchors).

## Cross-references

- Plan §1 Round 1 Q6; plan §4 (dossier scope); plan §2 Tier-5 (L5 layer)
- `portfolio-chapter-outlines.md` (per-chapter `claim_family` references)
- Round 22 Q2 (dossier sprint deferred to user-led session on separate account)
