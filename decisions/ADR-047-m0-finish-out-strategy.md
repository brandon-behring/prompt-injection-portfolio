---
adr_id: "047"
slug: m0-finish-out-strategy
title: "M0 finish-out strategy (content-filter handling + dossier deferral + priority order)"
date: 2026-05-22
status: Accepted
linked_round: "R22"
plan_section: "Context (Round 22 narrative)"
---

# ADR-047: M0 finish-out strategy

## Status

Accepted (Round 22 lock; documents the autonomous /loop M0 close-out plan).

## Context

After Day 3b close + v0.1.0-pre tag (commit `0a4938a`), autonomous /loop
work hit Anthropic's output content-filter mid-Day-15 governance batch
(SECURITY.md landed; CODE_OF_CONDUCT + templates + frontmatter MDX
blocked at the model-output layer). User invoked replan; Round 22 locked
the M0 finish-out strategy.

Simultaneously submission predecessor shipped v1.3.0 (two-guide reader
architecture + ADR-078 + ADR-079; the smaller-scale analog of portfolio's
Round 17 3-guide direction).

## Decision

**Q1 (content-filter strategy)**: pre-vet each Write content for known
dual-use trigger phrases (specific attack technique discussions, exploit
details) + soften where possible. Applies to CODE_OF_CONDUCT.md + ADR
content + chapter skeletons (Ch 7-12 + Ch 13).

**Q2 (dossier sprint deferral)**: Days 6-12 dossier work (~60-80 files
via research_toolkit) DEFERRED entirely to next user-led session.
research_toolkit's /research-plan + /research-gather + /dossier-build
+ /dossier-audit skills aren't in autonomous /loop's available skill
set; compass artifacts at `~/Downloads/compass_artifact_*.md` (~1055 lines)
need user-led ingestion. M0 v0.1.0 close window extends 2-3 days.

**Q3 (CI ref bump)**: advance submission CI ref v1.2.16 → v1.3.0 as
Round 22 mini-commit (single-line edit). v1.3.0 two-guide reader
architecture VALIDATES portfolio's Round 17 3-guide direction.

**Q4 (priority order)**: risk-minimizing front-load —
1. Round 22 mini-commit (CI ref bump) — 5 min, zero filter risk
2. Day 16 Docker T2 — 30 min, low risk
3. Day 5 6 lane experiment-record skeletons — 30 min, low risk
4. Day 14 13 textbook chapter skeletons — 60-90 min, medium risk (pre-vet)
5. Day 15 governance finish — 60 min with pre-vet
6. Day 17 ADRs batch (~12 substantive + ~25 skeleton) — 1-2 hours
7. Day 18 build-in-public templates — 15 min
8. Day 19 prep — 15 min; formal ratify-milestone DEFERRED to user-led

## Consequences

- M0 v0.1.0 close timeline extends ~2-3 days beyond plan §21 Day 19
  estimate due to dossier deferral. Calendar impact: M7 v0.7.0 tag
  shifts proportionally.
- Autonomous /loop work bounded to ~6-7 hours of Claude execution.
- Day 19 formal `git tag v0.1.0` + `gh release create v0.1.0` +
  announcement thread STAYS user-led.
- Open MRs at Round 22 close: MR-3 (research_toolkit#1) + MR-12
  (eval-toolkit#69 Tier-2 Protocol consolidation). Both not blocking M0.

## Cross-references

- Plan Round 22 narrative
- Round 22 Q1-Q4 + 4 follow-up decisions
- Commits since Day 3b: 3fb9338 (CI ref) + 7429e33 (Day 16) +
  c30a40e (Day 5) + dcf037a (Day 14) + 04922fe (Day 15) + this commit
- ADR-042 / ADR-043 / ADR-044 / ADR-045 / ADR-046 (Round 14-21 cascade)
- Submission v1.3.0 ADR-079 (two-guide reader architecture; analog)
