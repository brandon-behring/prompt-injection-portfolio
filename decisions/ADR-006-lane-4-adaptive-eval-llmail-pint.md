---
adr_id: "006"
slug: lane-4-adaptive-eval-llmail-pint
title: "Lane 4 adaptive eval: LLMail-Inject 5K + PINT-EN 3,016"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q5 + §5"
---

# ADR-006: Lane 4 adaptive eval — LLMail-Inject 5K + PINT-EN 3,016

## Status

Accepted.

## Context

Lane 4 builds a multi-detector fusion stacker + adaptive-eval surface
(per plan §5). Two questions: (1) does fusing per-row scores from prior
lanes improve over the best individual? (2) what is the
detection-vs-utility frontier via APR metric?

Eval set selection is load-bearing:

- **LLMail-Inject 5K** (SaTML 2025; stratified subset): real-world email
  agentic-injection corpus; never trained by submission or portfolio;
  matches deployment surface.
- **PINT-EN 3,016**: Lakera's held-out benchmark; never trained by
  evaluated detectors; English-only subset (compass §3.3 cites the
  English-only as Lane 4's appropriate slice).

A smaller eval set risks underpowered bootstrap CI; a larger combined
set risks leaking into adjacent Lane 2 corpus.

## Decision

Lane 4 evaluates on the **combined LLMail-Inject 5K + PINT-EN 3,016
(≈8,016 row pool)** held-out from all training:

- **LLMail-Inject 5K stratified** — agentic-flow indirect; never-trained
- **PINT-EN 3,016** — Lakera held-out English-only

Bootstrap CI on stacker delta vs best individual; APR metric (per
[ADR-037](ADR-037-apr-metric-lane-4.md)) at 1% / 3% / 5% utility-loss
thresholds.

## Consequences

- **Benchmark integrity audit** at M0 (per [ADR-038](ADR-038-benchmark-integrity-audit.md))
  confirms portfolio does not train on PINT or LLMail-Inject — the
  audit ratifies this ADR's load-bearing held-out claim.
- **Cost**: ~$5-30 (Tier B embedding-scorer dominates at ~$5; APR
  computation is $0; stacker training is $0).
- **Output**: HF Hub `BBehring/prompt-injection-fusion-v2-stacker` with
  stacker coefficients + constituent score table + APR curves.
- **Lane 5 timing**: Lane 5 activation probe trains on Lane 2 corpus per
  Round 16 Q4 (cross-lane comparability); Lane 4 stacker also trains on
  Lane 2 corpus per Round 16 Q3. Both eval on LLMail + PINT.

## Cross-references

- Plan §1 Round 1 Q5; plan §5 (Lane 4 hypothesis); Round 16 Q3
- [ADR-037](ADR-037-apr-metric-lane-4.md) (APR metric)
- [ADR-038](ADR-038-benchmark-integrity-audit.md) (held-out audit)
- Lane execution playbook §4 (`portfolio-lane-execution-playbooks.md`)
