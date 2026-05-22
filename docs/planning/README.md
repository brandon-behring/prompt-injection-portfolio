# Planning artifacts

This directory holds the **portfolio's design rationale + companion planning
documents**. These were authored during the 22 `/exploring-options` rounds
(R1-R22) that locked the portfolio's architectural decisions before M0
execution began.

These artifacts are **portable** (committed to the public repo so any
machine can clone-and-pick-up). They complement the ADRs at `decisions/`
which are the locked-decision authority.

## Files

| File | Purpose | Lines |
|---|---|---|
| [`PORTFOLIO_PLAN.md`](PORTFOLIO_PLAN.md) | Master plan; ratified across 22 `/exploring-options` rounds; 22 sections covering decision tables, repo topology, 6 lanes, book design, milestone sequence, risks, ETHICS draft, M0 day-by-day, library-first audit, Round 14-22 cascades | ~2032 |
| [`portfolio-chapter-outlines.md`](portfolio-chapter-outlines.md) | 13-chapter KF-decomposed outline (R/O/E triadic structure); referenced by §17 of the plan | ~247 |
| [`portfolio-experiment-record-template.md`](portfolio-experiment-record-template.md) | 4-file schema (hypothesis / protocol / results / decisions) per lane; Lane 1 worked example | ~263 |
| [`portfolio-lane-execution-playbooks.md`](portfolio-lane-execution-playbooks.md) | 6 self-contained per-lane execution playbooks (scope + eval slate + execution sequence + outcomes + gates + citations) | ~296 |
| [`eval-toolkit-v0.43-to-v1.0-roadmap.md`](eval-toolkit-v0.43-to-v1.0-roadmap.md) | eval-toolkit staggered v0.43→v1.0 release plan (upstream context referenced by ADR-045 Round 20 v0.47 pivot) | ~1301 |

## How to read these

1. **Start with `PORTFOLIO_PLAN.md`** — the Context section + Round 1
   decision table are the foundational ratchet. Then read each Round 6
   → Round 22 update narrative in order to see how the plan evolved
   across the 22 `/exploring-options` rounds.
2. **Cross-reference with `decisions/README.md`** for the ADR index. ADRs
   are the locked-decision authority; PORTFOLIO_PLAN.md is the
   pre-locked deliberation + ratified context.
3. **Read companions as-needed**: chapter outlines when authoring book
   prose; experiment-record template at lane open; lane playbooks at
   per-milestone execution.

## Provenance

These files are copies from the original author's `~/.claude/plans/`
directory (private session state). Committed to the repo at Round 22
close (2026-05-22 commit; see git log) so a fresh session on any machine
can pick up the full decision context without needing private
`~/.claude/` state.

## Update policy

The in-repo copies are **authoritative for cross-machine work**. The
`~/.claude/plans/` originals are working copies; sync changes to the
in-repo copies when a new decision lands. ADRs at `decisions/` capture
locked decisions canonically; updates to PORTFOLIO_PLAN.md happen at
each new `/exploring-options` round close (commit message describes
the round).

## Cross-references

- ADR index: [`decisions/README.md`](../../decisions/README.md)
- Upstream MR state machine: [`decisions/upstream_issues.md`](../../decisions/upstream_issues.md)
- Library imports registry: [`decisions/library_imports.md`](../../decisions/library_imports.md)
- Cold-start anchor: [`NEXT_SESSION.md`](../../NEXT_SESSION.md)
- Close-readiness handoff: [`M0_READINESS.md`](../../M0_READINESS.md)
