---
adr_id: "001"
slug: repo-name-prompt-injection-portfolio
title: "Repo name: prompt-injection-portfolio"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q1"
---

# ADR-001: Repo name `prompt-injection-portfolio`

## Status

Accepted.

## Context

Portfolio is a new public sibling repo to the locked
`prompt-injection-detection-submission` (v1.0.1+). The submission's
case-study findings (LoRA OOD drop -0.071 AUPRC vs frozen-probe per
submission ADR-052 / ADR-075) frame the portfolio's central question:
*can the OOD wall be climbed, or is it structural?* (plan §0).

The repo name must signal three things: (1) this is a portfolio piece,
not a one-off case study; (2) prompt-injection is the domain; (3) it is
the next version built from submission's experience, done cleaner
(Round 5 reframing).

## Decision

Repo name: **`prompt-injection-portfolio`** (Round 1 Q1).

Domain prefix matches submission convention; `-portfolio` suffix
distinguishes from submission's `-submission` suffix. Single hyphen
separator throughout for legibility.

## Consequences

- GitHub canonical path: `github.com/brandon-behring/prompt-injection-portfolio`.
- HF Hub model/dataset naming derives from this: `BBehring/prompt-injection-{rung}-indirect-v2-{variant}` (per [ADR-009](ADR-009-hf-hub-naming-scheme.md)).
- Sibling submission editable-dep path in `pyproject.toml [tool.uv.sources]` is relative: `../prompt-injection-detection-submission`.
- Public-from-M0 visibility per [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md).

## Cross-references

- Plan §1 Round 1 Q1; plan §3 (Repo topology)
- Submission convention: `prompt-injection-detection-submission`
