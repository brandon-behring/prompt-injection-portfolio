---
adr_id: "035"
slug: portfolio-clean-t0-strategy
title: "Portfolio writes its own clean T0 reproducibility tier"
date: 2026-05-19
status: Accepted
supersedes: ["033"]
linked_round: "R6"
plan_section: "§7"
---

# ADR-035: Portfolio-clean T0 strategy

## Status

Accepted (supersedes ADR-033 — T0-deferral reversed by Round 6 Q1''''').

## Context

Submission predecessor `prompt-injection-detection-prototype` wired its own
T0 reproducibility surface at v1.0.9 (ADR-058): `scripts/eval_from_hub.py`
non-dry-run download-and-compare. Portfolio could consume that surface
directly, but the "next version built from submission's experience, done
cleaner" framing (Round 5 reframing) argues for portfolio owning its own
T0 implementation.

## Decision

Portfolio writes its own clean T0 implementation at
`scripts/eval_from_hub.py` (portfolio-local file; parallel name; different
implementation).

Why portfolio writes own clean T0 vs consuming submission's:

- Maintains "next version, done cleaner" framing.
- Submission's T0 was retrofitted onto v1.0.x + carries that complexity;
  portfolio's clean reimplementation can apply lessons learned (cleaner
  error handling + CLI surface + dataset-loader integration + single-class
  slice handling baked in).
- Independent codebase prevents portfolio's reproducibility surface from
  breaking when submission patches.

## Consequences

- ADR-033 (T0-deferral) is dropped + superseded.
- Day 17 deliverable: `scripts/eval_from_hub.py` portfolio-local
  implementation; downloads HF Hub checkpoint → CPU inference → compares
  to portfolio's `evals/results.json` within 1e-4. ~15 min on a laptop.
- T0 tier mapping (per plan §7): T0 = `scripts/eval_from_hub.py`;
  T1 = `scripts/retrain_blueprint.py` + lane experiment records;
  T2 = Dockerfile + compose.yaml (Day 16); T3 = ~5-6 jupytext-paired
  notebooks at `book/src/content/notebooks/`.
- Cost: $0 (CPU-only laptop eval).

## Cross-references

- Plan §7 (Reproducibility ladder) + plan §6.3 (T3 notebooks)
- Submission ADR-058 (T0 wiring in submission)
- Round 5 reframing + Round 6 Q1'''''
