# Architecture Decision Records (ADRs)

Portfolio uses **light retrospective ADRs** per plan §2 Tier-2 calibration
(see [[sdd-calibration-by-audience]] memory): each <400 words; written
shortly after a decision is locked + the work has been done, not in advance.
Format: [Michael Nygard ADR template](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

**~35-37 ADRs anticipated** at M7 close per plan §9.

## ADR frontmatter schema

```yaml
---
adr_id: "NNN"
slug: "decision-slug-here"
title: "Brief decision title"
date: 2026-MM-DD
status: Accepted | Superseded | Deprecated
supersedes: ["NNN"]    # optional
superseded_by: ["NNN"] # optional
linked_round: "RN"     # the /exploring-options round that locked it
plan_section: "§N.M"   # cross-reference to plan
---
```

## ADR index

Status legend: ✓ = drafted at Day 17; — = scheduled for fill-in at v0.7.0
ratification (skeleton only).

### Round 1 (architecture + sequencing)

- — ADR-001 through ADR-013: foundational locks per plan §1 Round 1 Q1-Q7
  (repo name, cost cap, Lane 2 ablation, Lane 1b/3 breadth, Lane 4 adaptive
  eval, dossier target, license/HF naming). Skeleton at v0.7.0.
- — ADR-014: cost contingency unlock reserved (per plan §16).
- — ADR-015: cost contingency unlock reserved.
- — ADR-016: LODO methodology (carried from submission). Skeleton at v0.7.0.

### Round 2 (positioning + reproducibility)

- — ADR-017: submission patch policy (v1.0.x bug-fix; ADRs frozen at v1.0.1).
- — ADR-018: reproducibility-tier-ladder (T0/T1/T2/T3 per plan §7).
- — ADR-019: chapter-authoring-workflow (skeleton-first at M0 + JIT prose).
- — ADR-020: notebook-publication-target (inside `book/src/content/notebooks/`).

### Round 3 (public-facing + governance + commitment)

- — ADR-021: AI-assistance disclosure in book frontmatter.
- — ADR-022: ETHICS.md + HF Hub dataset card dual-use disclosure.
- — ADR-023: continuous build-in-public weekly cadence.
- — ADR-024: public-from-M0 visibility + pre-alpha banner.
- — ADR-025: v0.7.0 → v1.0.0 ~3-month community feedback window.
- — ADR-026: no-local-workarounds policy (strengthened Round 10).

### Round 4 (technical + governance)

- — ADR-027 **DROPPED** (single-class metric upstream-enforced via eval-toolkit#39).
- — ADR-028: community-governance (SECURITY + CODE_OF_CONDUCT + templates).
- — ADR-029: book-callout-citation-infrastructure (via scaffold v3.5+).
- — ADR-030: README scientific-abstract-scaled structure.

### Round 5 (post-survey realignment)

- — ADR-031: book-scaffold-astro-consumption (reframed Round 6).
- — ADR-032: 7-state status adoption from scaffold v3.x.
- — ADR-033 **DROPPED** (T0 deferral reversed by Round 6).
- — ADR-034: notebooks-reference-submission-as-foundation.

### Round 6 (overnight realignment)

- ✓ [ADR-035: portfolio-clean-T0-strategy](ADR-035-portfolio-clean-t0-strategy.md)
  (supersedes ADR-033).

### Round 7 (Tier A + B + C)

- ✓ [ADR-036: TPR@LowFPR reporting requirement](ADR-036-tpr-at-low-fpr-reporting.md)
- ✓ [ADR-037: APR metric Lane 4](ADR-037-apr-metric-lane-4.md)
- ✓ [ADR-038: benchmark integrity audit](ADR-038-benchmark-integrity-audit.md)
- — ADR-039: Lane 1 SOTA-anchor PromptShield expansion (Tier C reserved).
- — ADR-040: Lane 2 energy-loss 3rd variant (Tier C reserved).

### Round 8 (ETHICS content)

- ✓ [ADR-041: ETHICS.md content lock](ADR-041-ethics-content-lock.md)

### Round 14-22 cascade

- ✓ [ADR-042: Round 14 upstream MR cascade](ADR-042-round-14-upstream-mr-cascade.md)
- ✓ [ADR-043: Lane 2 LoRA-only scope + baseline expansion](ADR-043-lane-2-lora-only-and-baseline-expansion.md)
- ✓ [ADR-044: three-guide architecture with shared substrate](ADR-044-three-guide-architecture-with-shared-substrate.md)
- ✓ [ADR-045: eval-toolkit v0.47 pin + API pivot](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md)
- ✓ [ADR-046: book-scaffold-astro v3.5 pin + M1 unblock](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md)
- ✓ [ADR-047: M0 finish-out strategy](ADR-047-m0-finish-out-strategy.md)
