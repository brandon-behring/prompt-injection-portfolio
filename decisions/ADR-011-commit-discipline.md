---
adr_id: "011"
slug: commit-discipline
title: "Commit discipline: type-prefixed, Co-Authored-By, no amend/squash/force-push"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§2 Tier-1 invariants"
---

# ADR-011: Commit discipline

## Status

Accepted.

## Context

Portfolio's git history is part of the L0 public surface (browseable on
GitHub from M0 per [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md)).
A messy history degrades the build-in-public + reviewer experience.

Three discipline points:

- **Commit message format** — type prefix + Co-Authored-By trailer
  matches both global pattern (`~/Claude/lever_of_archimedes/patterns/git.md`)
  and submission convention.
- **History immutability** — no amend / squash / force-push because
  the public branch is browseable + the build-in-public weekly threads
  reference specific commit hashes.
- **AI-collaboration attribution** — Claude Co-Authored-By trailer
  matches plan §8.3 / [ADR-021](ADR-021-ai-assistance-disclosure.md)
  disclosure surface.

## Decision

Commits follow this discipline:

1. **Message format** — `<type>: <description>` prefix where type ∈
   {`feat`, `fix`, `refactor`, `test`, `docs`, `migrate`, `plan`}. Body
   uses 2-3 sentences of context + bulleted changes when applicable.
2. **Attribution trailer** — every commit ends with `Co-Authored-By:
   Claude <noreply@anthropic.com>`.
3. **No history rewriting** — no `git commit --amend`, no `git rebase
   -i`, no `git push --force` against the public `main`. Fixes happen
   as new commits.
4. **No `--no-verify` / `--no-gpg-sign`** — pre-commit hooks (ruff + mypy
   + test-contracts) must pass or be addressed; not bypassed.
5. **Specific file staging** — prefer `git add <file>` over `git add -A`
   to avoid accidental secret / large-binary inclusion.

## Consequences

- **Build-in-public threads cite hashes** (per
  [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md)) that
  remain stable; readers can `git checkout <hash>` to inspect state at
  publication time.
- **Reviewer auditability** — every commit is a discrete unit of work
  with clear `type:` + body; no need to disentangle squashed work.
- **CI runs on every push** — small frequent pushes work better than
  large rare ones; commits stay focused.
- **Pre-commit failure handling**: fix the underlying issue + create a
  new commit, NEVER `--amend` (which would mutate the prior commit and
  invalidate the public hash).

## Cross-references

- Plan §2 Tier-1 (invariants)
- Global `~/Claude/lever_of_archimedes/patterns/git.md` (canonical pattern)
- [ADR-021](ADR-021-ai-assistance-disclosure.md) (AI-collab disclosure)
- [ADR-023](ADR-023-build-in-public-continuous-weekly-cadence.md) (hash-citation surface)
