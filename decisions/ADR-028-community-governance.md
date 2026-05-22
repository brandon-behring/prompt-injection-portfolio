---
adr_id: "028"
slug: community-governance
title: "Community governance: SECURITY + CODE_OF_CONDUCT + issue templates + PR template"
date: 2026-05-19
status: Accepted
linked_round: "R4"
plan_section: "§10 governance + §8"
---

# ADR-028: Community governance

## Status

Accepted.

## Context

Portfolio is public from M0 ([ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md))
+ accepts community PRs during the v0.7.0 → v1.0.0 feedback window
(per [ADR-025](ADR-025-community-feedback-window.md)). Without governance
artifacts, three failure modes appear:

- **Drive-by PRs** without test-contract green or CHANGELOG entry land
  + introduce regression.
- **Security disclosures** go to the wrong channel (GitHub Issues
  instead of private contact).
- **Community-conduct ambiguity** — no published code of conduct means
  community-moderation decisions read as arbitrary.

Submission shipped no governance artifacts; portfolio remediates at M0.

## Decision

5 governance artifacts shipped at M0 Day 15:

1. **`SECURITY.md`** — responsible disclosure policy + private contact
   path (security@brandon-behring or equivalent); cross-references
   `ETHICS.md` §6 "Reporting concerns."
2. **`CODE_OF_CONDUCT.md`** — Contributor Covenant v2.1 vendored
   (industry-standard; matches GitHub default).
3. **3 issue templates** at `.github/ISSUE_TEMPLATE/`:
   - `bug.md` — reproduction steps + expected/actual + environment
   - `question.md` — methodology question routing (chapter/lane cite)
   - `research-discussion.md` — propose-a-finding format with dossier
     `claim_family` reference requirement
4. **`PULL_REQUEST_TEMPLATE.md`** at `.github/` — requires:
   - Test-contracts green attestation
   - CHANGELOG.md entry (per [ADR-025](ADR-025-community-feedback-window.md)
     patch policy)
   - Freshness-badge state update (if chapter/notebook touched)
   - Cross-link to relevant ADR (if methodology touched)
5. **Cross-references**: `SECURITY.md` ↔ `ETHICS.md` cross-linked at
   the "Reporting concerns" section; `PR template` cites `CHANGELOG.md`
   + relevant ADR.

## Consequences

- **First green CI push from M0** depends on `.github/` templates +
  governance files being present.
- **GitHub Issues UX** surfaces 3 issue templates (PR + issue templates
  show on Github's issue/PR creation page).
- **Round 22 ADR-047 strategy** (M0 finish-out): governance files
  shipped at Day 15 (`04922fe`) after Round 22 content-filter incident
  was navigated.
- **Per-PR friction** = one CHANGELOG line + one test-contract green;
  matches submission's PR review experience.

## Cross-references

- Plan §10 (governance files); plan §8 (public-facing commitments)
- [ADR-022](ADR-022-ethics-and-hf-dataset-card.md) (ETHICS sibling)
- [ADR-025](ADR-025-community-feedback-window.md) (PR-acceptance policy)
- [ADR-047](ADR-047-m0-finish-out-strategy.md) (Round 22 M0 strategy)
