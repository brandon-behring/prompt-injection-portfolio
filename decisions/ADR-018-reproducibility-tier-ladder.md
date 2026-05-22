---
adr_id: "018"
slug: reproducibility-tier-ladder
title: "Reproducibility tier ladder: T0 + T1 + T2 + T3 at v0.7.0"
date: 2026-05-19
status: Accepted
linked_round: "R2"
plan_section: "§7"
---

# ADR-018: Reproducibility tier ladder

## Status

Accepted.

## Context

Portfolio reviewers + community readers + future-self come at the
reproducibility surface with different time + tooling budgets. A
single-tier approach (e.g., "Docker only" or "notebooks only") fails
some audiences.

Submission's reproducibility experience (v1.0.x patches especially the
v1.0.9 T0 wiring) demonstrates that tier-laddering is the durable
shape: deeper tiers serve researchers; shallower tiers serve curious
engineers + recruiters in <30 min.

Four tiers naturally fall out of the L0-L5 hierarchical-depth model
(per [ADR-032](ADR-032-7-state-status-adoption-from-scaffold.md) +
plan §2 Tier-5):

- **T0** — laptop CPU eval-from-hub (15 min; verifies model card score
  matches portfolio's `evals/results.json`).
- **T1** — full retrain blueprint (paper-form documented; not bundled
  scripts; researchers replicate via `scripts/retrain_blueprint.py` +
  lane experiment records).
- **T2** — Docker container with all deps; reproducible across machines.
- **T3** — selective jupytext-paired notebooks for interactive deep-dives.

## Decision

Portfolio ships all 4 tiers at v0.7.0:

- **T0** (`scripts/eval_from_hub.py`) — portfolio-clean reimplementation
  per [ADR-035](ADR-035-portfolio-clean-t0-strategy.md); compares HF Hub
  checkpoint inference to `evals/results.json` within 1e-4.
- **T1** (`scripts/retrain_blueprint.py` + lane experiment records) —
  full LoRA retrain recipe; researcher-replicable.
- **T2** (`Dockerfile` + `compose.yaml` + `scripts/verify_docker.py`) —
  containerized eval; mandatory at M5; Day 16 shipped at M0.
- **T3** (`book/src/content/notebooks/`) — ~5-6 jupytext-paired
  notebooks (Ch 5 bootstrap, Ch 6 threshold-policy, Ch 8 char-injection
  matrix, Ch 9 attribution, Ch 11 stacker, Ch 12 activation probe).

## Consequences

- **Audience-laddered**: 15-min auditor (T0) vs 1-day researcher (T1) vs
  reproducible deployment (T2) vs interactive deep-dive (T3). Each tier
  has a clear use case.
- **CI gate**: `make verify-docker` (T2) green at M0; T0/T1/T3 smoke at
  M7 verification gate per plan §13.
- **Round 6 reframing applies**: T0 is portfolio-clean (not consuming
  submission's `eval_from_hub.py`) per
  [ADR-035](ADR-035-portfolio-clean-t0-strategy.md).
- **Cost**: $0 (laptop-only for T0 + T2; T1 cites lane experiment costs;
  T3 is human notebook authoring time).

## Cross-references

- Plan §7 (Reproducibility ladder); plan §13 (M7 verification gate)
- [ADR-035](ADR-035-portfolio-clean-t0-strategy.md) (T0 strategy)
- [ADR-032](ADR-032-7-state-status-adoption-from-scaffold.md) (L3 chapter freshness)
- Submission ADR-058 (T0 wiring origin)
