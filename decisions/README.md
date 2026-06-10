# Architecture Decision Records (ADRs)

Portfolio uses **light retrospective ADRs** per plan §2 Tier-2 calibration
(see [[sdd-calibration-by-audience]] memory): each <400 words; written
shortly after a decision is locked + the work has been done, not in advance.
Format: [Michael Nygard ADR template](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions).

**~45 ADRs at v0.1.0 close** (30 substantive R1-R5 + 11 substantive R6-R22 +
4 reserved + 2 DROPPED-as-index-only). Plan §9 anticipated 37-39 at M7;
post-Round-22 count exceeds the anticipated range due to Round 14-22 cascade
additions.

## ADR frontmatter schema

```yaml
---
adr_id: "NNN"
slug: "decision-slug-here"
title: "Brief decision title"
date: 2026-MM-DD
status: Accepted | Reserved | Superseded | Deprecated
supersedes: ["NNN"]    # optional
superseded_by: ["NNN"] # optional
linked_round: "RN"     # the /exploring-options round that locked it
plan_section: "§N.M"   # cross-reference to plan
---
```

## ADR index

Status legend:
- ✓ = drafted at full Nygard density (Accepted status)
- 🔒 = Reserved (skeleton + unlock criteria; advances to Accepted on unlock)
- ⊘ = DROPPED (decision retired; entry preserved for historical record)

### Round 1 (architecture + sequencing)

- ✓ [ADR-001: repo name `prompt-injection-portfolio`](ADR-001-repo-name-prompt-injection-portfolio.md)
- ✓ [ADR-002: cost cap $250 base + $100 contingency](ADR-002-cost-cap-250-base-100-contingency.md)
- ✓ [ADR-003: Lane 2 loss ablation — CE + Recall@LowFPR](ADR-003-lane-2-loss-ablation-ce-recall-at-lowfpr.md) (superseded by ADR-043)
- ✓ [ADR-004: Lane 1b full 12-character-injection matrix](ADR-004-lane-1b-full-12-character-injection.md)
- ✓ [ADR-005: Lane 3 Spotlighting 3-variants](ADR-005-lane-3-spotlighting-3-variants.md)
- ✓ [ADR-006: Lane 4 adaptive eval LLMail + PINT](ADR-006-lane-4-adaptive-eval-llmail-pint.md)
- ✓ [ADR-007: dossier exhaustive 60-80 files](ADR-007-dossier-exhaustive-60-80-files.md)
- ✓ [ADR-008: license split Apache + CC-BY](ADR-008-license-apache-cc-by.md)
- ✓ [ADR-009: HF Hub naming scheme](ADR-009-hf-hub-naming-scheme.md)
- ✓ [ADR-010: anti-pattern firewall](ADR-010-anti-pattern-firewall.md)
- ✓ [ADR-011: commit discipline](ADR-011-commit-discipline.md)
- ✓ [ADR-012: test-contracts](ADR-012-test-contracts.md)
- ✓ [ADR-013: cost contingency unlock policy](ADR-013-cost-contingency-unlock-policy.md)
- 🔒 [ADR-014: cost contingency unlock reserved 1](ADR-014-cost-contingency-unlock-reserved-1.md)
- 🔒 [ADR-015: cost contingency unlock reserved 2](ADR-015-cost-contingency-unlock-reserved-2.md)
- ✓ [ADR-016: LODO methodology from submission](ADR-016-lodo-methodology-from-submission.md)

### Round 2 (positioning + reproducibility)

- ✓ [ADR-017: submission patch policy](ADR-017-submission-patch-policy.md)
- ✓ [ADR-018: reproducibility tier ladder](ADR-018-reproducibility-tier-ladder.md)
- ✓ [ADR-019: chapter authoring workflow](ADR-019-chapter-authoring-workflow.md)
- ✓ [ADR-020: notebook publication target](ADR-020-notebook-publication-target.md)

### Round 3 (public-facing + governance + commitment)

- ✓ [ADR-021: AI-assistance disclosure](ADR-021-ai-assistance-disclosure.md)
- ✓ [ADR-022: ETHICS + HF dataset card](ADR-022-ethics-and-hf-dataset-card.md)
- ✓ [ADR-023: build-in-public continuous weekly cadence](ADR-023-build-in-public-continuous-weekly-cadence.md)
- ✓ [ADR-024: public from M0 + pre-alpha banner](ADR-024-public-from-m0-pre-alpha-banner.md)
- ✓ [ADR-025: v0.7.0 → v1.0.0 community feedback window](ADR-025-community-feedback-window.md)
- ✓ [ADR-026: no-local-workarounds policy](ADR-026-no-local-workarounds-policy.md)

### Round 4 (technical + governance)

- ⊘ ADR-027 **DROPPED** (single-class metric upstream-enforced via eval-toolkit#39 + submission ADR-055)
- ✓ [ADR-028: community governance](ADR-028-community-governance.md)
- ✓ [ADR-029: book callout + citation infrastructure](ADR-029-book-callout-citation-infrastructure.md)
- ✓ [ADR-030: README scientific-abstract structure](ADR-030-readme-scientific-abstract-structure.md)

### Round 5 (post-survey realignment)

- ✓ [ADR-031: book-scaffold-astro consumption](ADR-031-book-scaffold-astro-consumption.md)
- ✓ [ADR-032: 7-state status adoption](ADR-032-7-state-status-adoption-from-scaffold.md)
- ⊘ ADR-033 **DROPPED** (T0 deferral reversed by Round 6 + ADR-035)
- ✓ [ADR-034: notebooks reference submission as foundation](ADR-034-notebooks-reference-submission-as-foundation.md)

### Round 6 (overnight realignment)

- ✓ [ADR-035: portfolio-clean T0 strategy](ADR-035-portfolio-clean-t0-strategy.md) (supersedes ADR-033)

### Round 7 (Tier A + B + C)

- ✓ [ADR-036: TPR@LowFPR reporting requirement](ADR-036-tpr-at-low-fpr-reporting.md)
- ✓ [ADR-037: APR metric Lane 4](ADR-037-apr-metric-lane-4.md)
- ✓ [ADR-038: benchmark integrity audit](ADR-038-benchmark-integrity-audit.md)
- 🔒 [ADR-039: Lane 1 SOTA-anchor PromptShield (Tier C)](ADR-039-lane-1-sota-anchor-promptshield-tier-c.md)
- 🔒 [ADR-040: Lane 2 energy-loss 3rd variant (Tier C)](ADR-040-lane-2-energy-loss-tier-c.md)

### Round 8 (ETHICS content)

- ✓ [ADR-041: ETHICS.md content lock](ADR-041-ethics-content-lock.md)

### Round 14-22 cascade

- ✓ [ADR-042: Round 14 upstream MR cascade](ADR-042-round-14-upstream-mr-cascade.md)
- ✓ [ADR-043: Lane 2 LoRA-only scope + baseline expansion](ADR-043-lane-2-lora-only-and-baseline-expansion.md) (Round 15)
- ✓ [ADR-044: three-guide architecture with shared substrate](ADR-044-three-guide-architecture-with-shared-substrate.md) (Round 17)
- ✓ [ADR-045: eval-toolkit v0.47 pin + API pivot](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md) (Round 20)
- ✓ [ADR-046: book-scaffold-astro v3.5 pin + M1 unblock](ADR-046-book-scaffold-astro-v35-pin-and-m1-unblock.md) (Round 21)
- ✓ [ADR-047: M0 finish-out strategy](ADR-047-m0-finish-out-strategy.md) (Round 22)

### Round 24 (M0 close — Sprint 2 dossier closure + Sprint 3 fold-in)

- ✓ [ADR-048: cross-classification policy](ADR-048-cross-classification-policy.md) (topic-prefixed bibkeys for multi-topic primary sources)
- ✓ [ADR-049: body-quote anchoring discipline](ADR-049-body-quote-anchoring-discipline.md) (PDF body vs abstract-level extraction)
- ✓ [ADR-050: vendor cluster posture](ADR-050-vendor-cluster-posture.md) (unverified-by-design for parked/acquired commercial detector vendors)

Round 24 cross-references added to ADR-036 + ADR-038 + ADR-041 + ADR-045
(inline "Sprint 2 dossier evidence" subsections citing dossier bibkeys
+ claim families; per Sprint 2 E6 deferral).

**Erratum (2026-05-23, post-publication count refresh — Round 25)**:
ADR-048's "Sprint 2 inventory" paragraph references "28 cross-classified
entries (16 `agentic_*` + 12 `rag_*`)." Direct YAML inspection across
the 5 topic bib_ledgers shows the actual count is **31 entries (25
`agentic_*` + 6 `rag_*`)**. The 3-entry delta is within ADR-048's own
deferral language ("see `make dossier-audit` per-topic bib_ledger
summaries"). ADR text preserved unchanged per ADR-011 immutability
discipline; this note documents the count refresh.

### Round 26 (dogfood-driven upstream adoption — post-v0.1.0-close)

- ✓ [ADR-051: dogfood-driven upstream adoption batch](ADR-051-dogfood-driven-upstream-adoption-batch.md) — eval-toolkit `>=1.0` (v1.0 stability contract); research_toolkit v2.4.0 reclassified as a repo-local tooling clone (dropped as a pip dep); book-scaffold-astro v4.x + research-portfolio profile. Advances ADR-045 / ADR-046; dogfooding findings logged in `upstream_issues.md`.
- ✓ [ADR-052: attack-type-generalization study design](ADR-052-attack-type-generalization-study-design.md) — reorients the detector effort to indirect→indirect attack-type generalization (axis C: BIPIA disjoint type-LODO + joint carrier+attack shift), fair per-rung tuning on train-internal val, honest metric suite. Motivated by `docs/planning/submission-methodology-audit.md`; harness in `docs/planning/attack-type-lodo-harness-spec.md`. Lane/chapter restructure deferred to Phase 3.

### Round 29 (M1 Lane-1 launch wiring)

- ✓ [ADR-053: RunPod launch via job spec + `run_job` (phantom-`Session` correction); Lane-1 sweep base-budget](ADR-053-runpod-job-spec-run-job-not-session.md) — `runpod_deploy.load_job_spec → run_job` over a strict YAML job spec replaces the phantom `runpod_deploy.Session` (plan + submission ADR-059); `lifecycle.on_success: delete` for one-shot sweeps; $5–15 sweep classified base-budget ($0.00 realized) so ADR-014 stays Reserved. Glue committed `4862e21`.
- ✓ [ADR-054: M1 attack-type-LODO ceiling = LoRA (3-rung write-gate); full-FT deferred to a §16 trigger-gate; hybrid local+RunPod execution; off-the-shelf reference column](ADR-054-m1-lora-ceiling-full-ft-deferred.md) — amends (not supersedes) ADR-052 (rung set) + ADR-053 (launch YAML now `--rungs lora`, on-pod falsify dropped, `cost_cap` 15→8). `REQUIRED_RUNGS=(tfidf,frozen,lora)` decoupled from 4-wide `RUNG_NAMES`; `full_ft` selectable but not required; `criteria.md` Revision 2 (decision rule UNCHANGED). **Trigger resolved 2026-06-01: does NOT fire** — the §6.5 verdict is FALSIFIED on `lora` (decisively null), so `full_ft` stays deferred.

### Round 30 (post-M1 milestone re-ladder)

- ✓ [ADR-055: post-M1 re-ladder — the multi-axis capacity-dependent OOD spine; Lane 2 re-pointed to the carrier axis; Lane 5 sharpened to intermediate-activation recovery; a carrier-LODO M2 pre-flight gate](ADR-055-post-m1-re-ladder-multi-axis-spine.md) — discharges ADR-052's deferred Phase-3 re-ladder (and the Round-27 placeholder). Multi-axis spine: the **attack-type** axis is capacity-dependent (M1: LoRA dissolves it), the **carrier** axis is **partially capacity-resistant (provisional, n=3; carrier-LODO `SMALL-THROUGHOUT`, residual at table)**, and the **cross-family** axis is **capacity-resistant (`SURVIVES` at the LoRA ceiling, B4 2026-06-06; Arm A grows, B+ does not bridge; 5-verifier audit ROBUST; a transfer result, not a mechanism claim — Mirror/corpus-style confound, audit W12 2026-06-10)** — the spine is **axis-dependent**, not uniformly capacity-dependent. Re-points Lane 2's headline to carrier generalization (method unchanged per ADR-043); sharpens Lane 5 to intermediate-activation recovery (d′ > 0.5 M3 gate kept); registers a **carrier-LODO M2 pre-flight gate** (reuses the attack-type-LODO harness, axis swapped, carrier-clustered estimator). Builds on ADR-054; supersedes nothing. Reconciles the submission's backbone-invariant carrier null (backbone-invariant ≠ capacity-invariant).

## Tally

| Status | Count |
|---|---:|
| ✓ Accepted | 49 |
| 🔒 Reserved | 4 |
| ⊘ DROPPED | 2 |
| **Total entries** | **55** |
| Files in `decisions/` | 53 (DROPPED entries are index-only) |
