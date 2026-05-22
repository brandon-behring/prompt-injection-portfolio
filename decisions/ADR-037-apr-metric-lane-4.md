---
adr_id: "037"
slug: apr-metric-lane-4
title: "APR metric reporting in Lane 4 agentic stacker eval"
date: 2026-05-19
status: Accepted
linked_round: "R7 Tier A"
plan_section: "§5"
---

# ADR-037: APR metric (Lane 4)

## Status

Accepted (Round 7 Tier A Q1'''''' — zero-cost methodology improvement).

## Context

Meta Prompt Guard 2 (PG2) shipped APR (Attack Prevention Rate) as its
canonical detector metric: % of attacks blocked at ≤3% utility loss on
benign queries. APR is utility-aware in a way that ASR (Attack Success
Rate) is not — ASR alone doesn't tell you whether the defense ruins the
benign-query experience.

For Lane 4 (score-fusion stacker on LLMail-Inject 5K + PINT-EN 3016), APR
captures the utility-security tradeoff explicitly. A stacker that beats
best-individual on ASR but inflates false positives is the unhelpful
outcome.

## Decision

Lane 4 reports APR alongside ASR + TPR@LowFPR (per ADR-036) on the agentic
eval slates. APR computation:

1. Compute per-row scores from the stacker on LLMail-Inject + PINT
2. Define "utility loss" = fraction of benign queries that get
   high-score-flagged
3. Sweep threshold to find the point where utility loss ≤ 3%
4. APR = TPR at that threshold

Reported per stacker variant (LogisticStacker + XGBoost meta-learner per
Round 7 Tier B) + per best-individual baseline for comparison.

## Consequences

- Zero additional cost ($0 — derives from existing scorecard outputs).
- Lane 4 protocol.md cites APR as a metric reporting deliverable.
- Future Tier C unlocks (PromptShield Lane 1 SOTA anchor) may also adopt
  APR if PG2 86M doesn't cover the same operating-point range.
- Cross-cutting: book chapter 11 (Lane 4) prose anchors on APR vs ASR
  comparison as the lane's interpretive finding.

## Cross-references

- Meta Prompt Guard 2 release notes / paper
- ADR-036 (TPR@LowFPR; complementary; both reported in Lane 4)
- Lane 4 protocol.md
- Plan §16 (cost envelope; ADR-037 is the no-cost Tier A item)
