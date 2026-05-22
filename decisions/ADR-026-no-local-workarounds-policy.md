---
adr_id: "026"
slug: no-local-workarounds-policy
title: "No local workarounds: library-first invariant strictly enforced"
date: 2026-05-19
status: Accepted
linked_round: "R10"
plan_section: "§2 Tier-1 + §10"
---

# ADR-026: No-local-workarounds policy

## Status

Accepted (Round 10 reinforcement of Round 3 Tier-1 invariant).

## Context

Portfolio depends on 4 load-bearing libraries (all Brandon-maintained):

- `eval-toolkit` (PyPI; v0.47+ per Round 20)
- `runpod-deploy` (PyPI; v0.8.4+)
- `research_toolkit` (PyPI)
- `@brandon_m_behring/book-scaffold-astro` (npm; v3.5+ per Round 21)

Without explicit policy, missing primitives invite local hand-rolls:
"just write the loader/scorer/component here, fix upstream later." This
fails for three compounding reasons:

1. **Drift** — the local impl diverges from what upstream eventually
   ships; portfolio runs on a fork-in-spirit.
2. **Lost feedback signal** — upstream doesn't see what's missing because
   portfolio "solved" it locally.
3. **Reuse loss** — other projects can't benefit from primitives buried
   in portfolio's `src/`.

Submission's experience demonstrated the strong form of this discipline:
the parallel-Codex agent implemented 5 of 7 portfolio-filed eval-toolkit
MRs in 2 days (per Round 14) precisely because portfolio filed clean
upstream issues rather than working around them.

## Decision

Strict library-first invariant:

1. **All reusable primitives belong upstream** (in one of the 4 libraries).
   Portfolio NEVER hand-rolls equivalents.
2. **No local workarounds whatsoever** — no `src/_overrides/`, no
   `# TODO(upstream #N)` markers, no "ship now and refactor later."
3. **Missing primitive workflow** — file upstream issue → implement as
   MR → release new version → portfolio's `pyproject.toml` (or
   `book/package.json`) pins the new version → lane work proceeds.
4. **Lane blocked until upstream ships** — if a primitive is needed and
   not in upstream, the portfolio lane is BLOCKED. No partial work
   against an interim local solution.
5. **Project-specific glue is OK** — lane orchestration scripts, data
   loaders that *compose* eval-toolkit primitives, project-named CLI
   wrappers belong in portfolio's `src/`. The line: reusable across
   projects → upstream; project-specific glue → portfolio local.
6. **Ongoing-issue-filing discipline** (Round 10 user grant): standing
   permission to file GitHub issues against the 4 libraries during
   execution — feature requests, papercuts, API improvements, docs gaps.
   Tracked in `decisions/upstream_issues.md` state machine.

## Consequences

- **Upstream MRs at M0** per plan §10 + `decisions/upstream_issues.md`
  state machine; closure tracked from `issue-filed` → `pr-opened` →
  `released-vX.Y.Z` → `pinned-in-portfolio`.
- **Test-contract `library_imports_registered`** (per
  [ADR-012](ADR-012-test-contracts.md)) enforces — every `from
  {eval_toolkit, runpod_deploy, research_toolkit}` import is registered
  in `decisions/library_imports.md`.
- **Round 14 outcome**: 5/7 eval-toolkit MRs shipped in 2 days via
  parallel-Codex; this policy made that feedback loop tight.
- **Round 21 outcome**: scaffold v3.5 research-portfolio preset shipped
  + closed both portfolio-filed scaffold MRs; M1 book authoring
  unblocked.

## Cross-references

- Plan §2 Tier-1 (library-first invariant); plan §10 (upstream MR audit)
- [ADR-012](ADR-012-test-contracts.md) (`library_imports_registered` test-contract)
- [ADR-042](ADR-042-round-14-upstream-mr-cascade.md) (Round 14 MR cascade)
- [ADR-045](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md) (Round 20 v0.47 pivot)
- [ADR-046](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md) (Round 21 scaffold v3.5)
