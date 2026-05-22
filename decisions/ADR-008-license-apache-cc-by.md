---
adr_id: "008"
slug: license-apache-cc-by
title: "License split: Apache-2.0 (code) + CC-BY-4.0 (prose + notebooks)"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q7"
---

# ADR-008: License split — Apache-2.0 (code) + CC-BY-4.0 (prose + notebooks)

## Status

Accepted.

## Context

Portfolio combines two distinct output classes that warrant separate
licensing:

- **Code** (`src/`, `scripts/`, `tests/`, `Makefile`, configs) — needs a
  permissive software license matching the open-source dependency
  ecosystem (eval-toolkit / runpod-deploy / research_toolkit / scaffold,
  all Apache-2.0 or MIT-class).
- **Prose + notebooks** (`book/`, `docs/`, dossier, build-in-public
  archive) — needs an attribution-friendly content license that
  matches academic publication conventions + supports redistribution
  with credit.

A single permissive license (e.g., MIT) for everything would understate
the prose's expectation of citation; CC-BY only would discourage code
contribution under Apache's patent grant.

## Decision

Two-license split:

- **`LICENSE`** (repo root) — **Apache-2.0** covers all code (`src/`,
  `scripts/`, `tests/`, `Makefile`, configs, `pyproject.toml`).
- **`book/LICENSE`** — **CC-BY-4.0** covers all prose + notebooks
  (`book/`, dossier `docs/research/`, `docs/build-in-public/`).

Citation guidance (per [ADR-021](ADR-021-ai-assistance-disclosure.md)):
`Behring, B. (2026). The OOD Wall: A Methodology Case Study in
Prompt-Injection Detection. https://...`

## Consequences

- **Apache patent grant** covers the eval-toolkit dataclass primitives +
  portfolio's local orchestration code; matches submission's licensing
  parity (submission ships Apache-2.0 as well).
- **CC-BY-4.0 attribution requirement** for prose enables academic +
  blog-post reuse with credit; supports the Round 19 v1.0.0 final
  citation surface.
- **HF Hub dataset card** (per [ADR-022](ADR-022-ethics-and-hf-dataset-card.md))
  references both licenses + the ETHICS.md cross-link.
- **Headers**: not required (per scaffold + submission convention);
  LICENSE file at root + `book/LICENSE` sufficient.

## Cross-references

- Plan §1 Round 1 Q7; plan §3 (Repo topology — `LICENSE` + `book/LICENSE`)
- [ADR-009](ADR-009-hf-hub-naming-scheme.md) (HF naming scheme — Q7 sibling)
- [ADR-021](ADR-021-ai-assistance-disclosure.md) (citation format)
- [ADR-022](ADR-022-ethics-and-hf-dataset-card.md) (HF dataset card licensing)
