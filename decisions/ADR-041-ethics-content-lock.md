---
adr_id: "041"
slug: ethics-content-lock
title: "ETHICS.md content + HF Hub dataset card alignment"
date: 2026-05-19
status: Accepted
linked_round: "R8"
plan_section: "§20"
---

# ADR-041: ETHICS content lock

## Status

Accepted (Round 8 — locked via 4 sub-questions).

## Context

Per Round 8 walkthrough, ETHICS.md content needs 4 lock decisions:
- Q1: dual-use disclosure tone (full-specificity vs context-trimmed)
- Q2: HF Hub publication terms (public CC-BY-4.0 vs gated)
- Q3: reporting channel (GH Security Advisories vs email vs hybrid)
- Q4: citation format (BibTeX + AI-collaboration acknowledgment)

Round 8 user answers (recommendations accepted):
- Q1: WildGuardMix-style full-specificity disclosure
- Q2: Public CC-BY-4.0 + terms-of-use note in HF Hub card frontmatter
- Q3: Hybrid (GH Security Advisories + secondary email channel)
- Q4: BibTeX + acknowledge Anthropic-ToS-compliant Claude collaboration

## Decision

Lock the ETHICS.md text + HF Hub dataset card text per the Round 8
choices above. The full ETHICS.md draft is captured in plan §20 + landed
in the repo at `/ETHICS.md` (committed Day 1, M0 9b07cdf).

ETHICS.md structure (final):
1. Dual-use disclosure (Round 8 Q1: full-specificity per WildGuardMix
   norms; no novel attack vectors — only documented techniques from
   Greshake et al. 2023 + OWASP LLM01:2025; withholding context would
   foreclose reproducibility without meaningful attacker uplift)
2. Intended use (research / safety eval / benchmarking / teaching)
3. Responsible use (cite + don't redistribute / don't train attack-gen /
   disclose AI assistance in derived work)
4. Anthropic Commercial Service Agreement compliance
5. Citation guidance (BibTeX + AI-collaboration acknowledgment)
6. Reporting concerns (Q3 hybrid: GH Security Advisories + ETHICS.md §6.2
   email channel)
7. Acknowledgments (OWASP / MITRE / Greshake / WildGuardMix / HarmBench /
   ACL Publication Ethics / Anthropic Responsible Disclosure)
8. Version + change log

HF Hub dataset card (frontmatter + body) cross-references ETHICS.md §1
+ §3 + §6.2 for terms-of-use.

## Consequences

- Day 1 ETHICS.md commit (9b07cdf) IS the authoritative text;
  ADR-041 ratifies retroactively.
- Day 15 SECURITY.md complements ETHICS.md §6.1 (GH Security Advisories
  channel) — they cross-reference each other.
- All HF Hub artifact pushes (M3 dataset + M2-M6 model checkpoints)
  include the terms-of-use frontmatter pointing back to portfolio's
  ETHICS.md.
- Future ETHICS.md changes require either a new ADR (substantive) or
  the immutability narrow-relaxation path (typo / link fix).

## Cross-references

- Plan §20 (full ETHICS.md draft text)
- ETHICS.md root file (committed Day 1)
- SECURITY.md (Day 15 governance complement)
- ADR-022 (Round 3 dual-use disclosure decision; superseded by ADR-041
  expansion)
- ADR-024 (Round 3 public-from-M0 visibility; co-ratified)
