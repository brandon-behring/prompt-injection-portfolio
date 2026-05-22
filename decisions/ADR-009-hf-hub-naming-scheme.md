---
adr_id: "009"
slug: hf-hub-naming-scheme
title: "HF Hub naming scheme: BBehring/prompt-injection-{rung}-indirect-v2-{variant}"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q7"
---

# ADR-009: HF Hub naming scheme

## Status

Accepted.

## Context

Portfolio ships ~5-8 HF Hub model checkpoints + 1 dataset across the
6 lanes (per plan §5 + lane playbooks §1-6). Naming must:

1. Disambiguate from submission's checkpoints
   (`BBehring/prompt-injection-{frozen-probe,lora}`).
2. Encode the rung (which baseline / variant family) + variant (which
   loss / data variant within the family).
3. Support `v2` major-version stamping (portfolio is the "v2" iteration
   built from submission's v1 experience).
4. Sort lexicographically into family clusters on the HF Hub user page.

## Decision

HF Hub naming scheme:

```
BBehring/prompt-injection-{rung}-indirect-v2-{variant}
```

Where:
- `{rung}` = one of `frozen-probe` / `lora` / `direct` / `fusion` /
  `reference-scorers` (matches submission convention).
- `indirect-v2` = scope marker (Lane 2's indirect-injection focus +
  portfolio v2 versioning).
- `{variant}` = one of `ce` / `rfpr` / `energy` / `stacker` / `probe`
  (matches the loss / approach within the rung family).

Examples:
- `BBehring/prompt-injection-lora-indirect-v2-ce` (Lane 2 CE variant)
- `BBehring/prompt-injection-lora-indirect-v2-rfpr` (Lane 2 RFPR variant)
- `BBehring/prompt-injection-fusion-v2-stacker` (Lane 4 stacker; drops
  `indirect-v2-` since fusion isn't training-data-specific)
- `BBehring/prompt-injection-direct-v2-reference-scorers` (Lane 1 score artifacts)

Dataset: `BBehring/prompt-injection-synthetic-indirect-v2` (Lane 2 corpus).

## Consequences

- **Sortable**: HF user page groups by rung family.
- **Test-contract**: `library_imports_registered` + per-lane `decisions.md`
  references the exact HF Hub path; `make hf-publish-smoke` (plan §13)
  validates the slug at publication.
- **License headers**: each HF Hub model card cites both
  [ADR-008](ADR-008-license-apache-cc-by.md) license files +
  [ADR-022](ADR-022-ethics-and-hf-dataset-card.md) ETHICS cross-ref.
- **Citation in book chapters**: `<Cite>` references to model cards
  use the canonical HF Hub URL `https://huggingface.co/BBehring/<slug>`.

## Cross-references

- Plan §1 Round 1 Q7; plan §13 (HF publication smoke test)
- [ADR-008](ADR-008-license-apache-cc-by.md) (license sibling decision)
- [ADR-022](ADR-022-ethics-and-hf-dataset-card.md) (HF dataset card)
- [ADR-001](ADR-001-repo-name-prompt-injection-portfolio.md) (repo name derivation)
