---
adr_id: "042"
slug: round-14-upstream-mr-cascade
title: "Round 14 cascade — 5 of 7 eval-toolkit MRs shipped upstream + ADR-052 → ADR-075 supersession"
date: 2026-05-19
status: Accepted
linked_round: "R14"
plan_section: "Context + §10"
---

# ADR-042: Round 14 upstream MR cascade

## Status

Accepted (Round 14 lock; commit `bc30c52` Day 3a/c1 + `cbf7d25` Day 3a/c2).

## Context

Between portfolio M0 Day 2.5 (2026-05-19 issue-filing batch) and Day 3a
(2026-05-21 consume), eval-toolkit shipped 4 additional releases (v0.45.0
→ v0.46.0 → v0.46.1 → v0.47.0) closing portfolio's MR-1/2/4/5/7 + MR-6 via
parallel-Codex implementation. Simultaneously the submission predecessor
shipped v1.2.3..v1.2.12 introducing ADR-075 (unified full-FT OOD drop
rationale; supersedes ADR-052 entirely + ADR-050 R2 axis).

## Decision

Portfolio absorbs the cascade via Round 14 follow-up `/exploring-options`
rounds:

1. **CI submission ref pin**: advance v1.1.1 → v1.2.12 (HEAD per Round 14
   Q1). Dynamic-detect fallback for tag-not-pushed scenarios per round-3
   Q2.
2. **eval-toolkit floor**: advance >=0.42 → >=0.44 (Round 14 Q2;
   superseded by Round 20 ADR-045 → >=0.47).
3. **MR-2 advanced-6 follow-up**: file new MR-10 issue against
   eval-toolkit (Round 14 Q3; superseded by Round 20 ADR-045 — MR-10
   obsoleted by v0.47.0 12-tech consolidation).
4. **Task #6 transition**: split closed half (5/7 MRs shipped) + new
   follow-up #6a (consume + verify) + #6b (track open MRs).
5. **Citation cascade**: portfolio Lane 2 hypothesis + Ch 7 case study
   cite ADR-075 as canonical (was ADR-052 in Round 6).

## Consequences

- Day 3a 3-commit sequence (deps + tracking + NEXT_SESSION) lands the
  cascade per Round 14 round-3 Q3 split.
- Portfolio's M0 upstream-MR surface shrinks from 9 originally filed →
  only MR-3 (research_toolkit#1) + new MR-12 (filed Day 3a smoke-test;
  eval-toolkit#69 Tier-2 Protocol consolidation) open.
- Lane work at M1+ targets v0.44 canonical surfaces directly (re-targeted
  to v0.47 per Round 20).
- ADR-052 retained in submission/decisions/ as historical artifact per
  submission immutability rule; portfolio prose cites ADR-075.

## Cross-references

- Plan Round 14 narrative (post-Round-6) + Round 14 Q1-Q4 table
- Submission ADR-075 (canonical) + ADR-052 (superseded)
- Day 3a commits bc30c52 + cbf7d25 + 8d6a60d
- ADR-043 (Round 15; co-ratified scoping decisions)
- ADR-045 (Round 20; v0.47 advance supersedes Round 14 Q2 v0.44 pin)
