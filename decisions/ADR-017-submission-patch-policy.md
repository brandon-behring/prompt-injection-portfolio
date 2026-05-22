---
adr_id: "017"
slug: submission-patch-policy
title: "Submission patch policy: v1.0.x bug-fix only; ADRs frozen at v1.0.1"
date: 2026-05-19
status: Accepted
linked_round: "R2"
plan_section: "§1 Round 2 Q4'"
---

# ADR-017: Submission patch policy

## Status

Accepted.

## Context

Submission shipped v1.0.1 as the locked case-study artifact. Subsequent
work in the prompt-injection space (portfolio + future projects) creates
ambiguity: when does new finding belong in submission (as a patch) vs in
portfolio (as new experimental work)?

Without a policy, two failure modes appear:

- **Submission drift** — substantive scope-changes leak into submission
  as "patches"; reviewers can no longer cite v1.0.1 as a stable artifact.
- **Patch starvation** — genuine bugs in submission (label errors,
  metric bugs, broken reproducibility) go unfixed because they "belong
  in portfolio."

## Decision

Submission patch policy:

1. **v1.0.x patches permitted ONLY for**: (a) bugs that compromise
   v1.0.1's headline claims, (b) reproducibility breakages, (c)
   methodology-load-bearing corrections that emerged from the submission's
   own scope (not from portfolio findings).
2. **ADRs frozen at v1.0.1** — no new submission ADRs after v1.0.1; the
   `submission/decisions/` directory accepts no new entries.
3. **Portfolio findings stay in portfolio** — even if Lane 2 / Lane 5
   reveal something that would retroactively change a submission
   interpretation, the new finding lives in portfolio's `decisions/` +
   chapter prose, NOT in submission.
4. **Exception**: methodology-load-bearing corrections (ADR-052 / ADR-075
   supersession-cascade) that need to live in submission's decisions/
   for the artifact's coherence; these are explicitly named in advance
   and follow submission's immutability rule.

Submission v1.0.x stays under Brandon's maintenance; portfolio assumes
v1.0.X has been polished by the time portfolio cites it.

## Consequences

- **Submission CI ref pin** (portfolio's `.github/workflows/ci.yml`)
  advances per Round 14 Q1 + Round 22 Q3 (now at v1.3.0); the pin
  advances *only* with submission patches that were already accepted
  under this policy.
- **Dynamic-detection** (`git ls-remote --tags origin | grep refs/tags/v1.X.X
  | sort -V | tail -1`) picks up the latest pushed semver; the pin is
  documentary, not load-bearing.
- **Reviewer can cite submission v1.0.1** confidently — that artifact is
  stable.
- **Portfolio cites submission v1.X.Y** as the rolling sibling repo; the
  citation is to the live source, not the v1.0.1 snapshot.

## Cross-references

- Plan §1 Round 2 Q4'; plan §3 (Repo topology — sibling dep)
- Submission's `decisions/` immutability rule
- Round 22 Q3 CI ref bump v1.2.16 → v1.3.0
