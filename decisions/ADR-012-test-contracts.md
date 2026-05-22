---
adr_id: "012"
slug: test-contracts
title: "Test contracts: 6+1 invariant tests at Tier-4 CI gate"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§2 Tier-4 + §13"
---

# ADR-012: Test-contracts at Tier-4 CI gate

## Status

Accepted.

## Context

Portfolio's CI must enforce the [ADR-010](ADR-010-anti-pattern-firewall.md)
anti-pattern firewall + library-first invariant
([ADR-026](ADR-026-no-local-workarounds-policy.md)) automatically.
Hand-discipline drifts; CI does not.

Submission shipped 6 test-contracts as a canonical pattern. Portfolio
inherits the 6 + adds 1 (`mypy_strict_clean`, brought up to first-class
contract per Round 4 governance discussion).

## Decision

CI runs 7 test-contracts (`tests/contracts/test_*.py`) on every push:

1. **`no_handrolled_metrics`** — eval-toolkit primitives only; no local
   AUPRC / TPR@FPR reimplementations.
2. **`predictions_persisted`** — every Lane 1/2/4/5 eval emits per-row
   parquet output to `evals/predictions/`.
3. **`leakage_scan_present`** — every new eval source has a corresponding
   `docs/research/lane-N/leakage_audit.md` entry.
4. **`glossary_complete`** — project-specific terms in code + prose
   are registered in `docs/glossary.md` (canonical lookup).
5. **`library_imports_registered`** — every `from {eval_toolkit,
   runpod_deploy, research_toolkit}` import is registered in
   `decisions/library_imports.md`.
6. **`mypy_strict_clean`** — `mypy --strict` clean across `src/` +
   `scripts/` + `tests/`.
7. **`experiment_records_complete`** (per Round 7 + Round 17 Q2 fragment
   extension) — each lane has `hypothesis.md` + `protocol.md` populated
   at lane open; `results.md` + `decisions.md` + 3 fragment files at
   lane close.

## Consequences

- **Hard CI gate** — push fails if any contract fails; PR cannot merge
  without all 7 green.
- **Tier-4 enforcement layer** complements ruff + mypy + pytest unit/smoke;
  the contracts are *invariants*, not unit tests of specific functions.
- **Round 14 `predictions_persisted` extension**: extends to Lane 1b
  + Lane 3 + Lane 5 outputs as those lanes close.
- **`mypy_strict_clean` is repo-wide**: portfolio's `src/` + `scripts/`
  + `tests/` all clean under strict mode (no `Any`, no implicit Optional,
  no untyped definitions).

## Cross-references

- Plan §2 Tier-4 (CI / enforcement); plan §13 (Test-contracts)
- [ADR-010](ADR-010-anti-pattern-firewall.md) (anti-patterns these enforce)
- [ADR-026](ADR-026-no-local-workarounds-policy.md) (library-first enforced by `library_imports_registered`)
- `portfolio-experiment-record-template.md` (test-contract attestation source)
