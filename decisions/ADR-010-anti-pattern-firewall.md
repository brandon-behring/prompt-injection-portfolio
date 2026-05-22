---
adr_id: "010"
slug: anti-pattern-firewall
title: "Anti-pattern firewall: real tests, persisted predictions, leakage scan, glossary"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§2 Tier-1 invariants"
---

# ADR-010: Anti-pattern firewall

## Status

Accepted.

## Context

Submission carried 4-5 named anti-patterns that load-bearing methodology
discipline depended on. Portfolio inherits these. Without explicit
re-locking, they degrade by default (anti-pattern arguments are negative
claims; positive incentives drift toward them).

Specific anti-patterns to firewall:

- **Test-tuning** — adjusting test data or metrics after seeing model
  outputs.
- **Stub tests / placeholder asserts** — tests that don't actually
  assert correctness.
- **Predictions not persisted** — running eval without parquet output
  prevents bootstrap CI rerun.
- **Leakage scan elision** — adding new eval sources without auditing
  for training-data overlap.
- **Glossary drift** — project-specific terms introduced without same-commit
  glossary entries.

## Decision

Portfolio firewalls 5 anti-patterns at Tier-4 CI gate level:

1. **No test-tuning** — eval metrics + thresholds locked in protocol.md
   before results.md; protocol.md amendments require explicit ADR cite.
2. **Real tests only** — no stub functions; assertions test
   observable behavior (per CLAUDE.md global rule).
3. **Predictions persisted** — per-row parquet output mandatory from
   every Lane 1/2/4/5 eval; test-contract `predictions_persisted`
   enforces.
4. **Leakage scan on every new eval source** — `docs/research/lane-N/leakage_audit.md`
   required before lane close; test-contract `leakage_scan_present`
   enforces.
5. **New project-specific term → glossary entry in same commit** —
   `docs/glossary.md` carries the canonical term list; test-contract
   `glossary_complete` enforces.

## Consequences

- **6 test-contracts at CI gate** ([ADR-012](ADR-012-test-contracts.md))
  operationalize these.
- **No silent failure** matches submission CLAUDE.md global invariant
  (per global `~/.claude/CLAUDE.md`).
- **Per-lane discipline**: each lane's decisions.md cites which
  anti-patterns were checked + how (per
  `portfolio-experiment-record-template.md`).

## Cross-references

- Plan §2 Tier-1 (invariants); plan §2 Tier-4 (CI / enforcement)
- [ADR-012](ADR-012-test-contracts.md) (test-contracts operationalize this)
- [ADR-026](ADR-026-no-local-workarounds-policy.md) (related: library-first)
- Global `~/.claude/CLAUDE.md` (real tests only invariant)
