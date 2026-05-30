---
lane_id: lane-1
slug: lane-1-attack-type-lodo
hypothesis_id: H-LANE-1
title: Attack-type generalization of injection detectors — the OOD wall, measured fairly (ADR-052)
date_opened: 2026-05-29
date_closed: TBD-M1
budget_usd: 10-12
status: active
supersedes: lane-1-direct-baselines (reference-scorer comparison; pre-ADR-052 skeleton)
---

# Lane 1 — Hypothesis (attack-type-LODO)

> **Reconciled 2026-05-29 (ADR-052).** The pre-ADR-052 question (how reference scorers compare to a
> classical floor + frozen-probe on a pooled-OOD slate) was superseded: it depended on the unbuilt Lane-2
> corpus + excluded datasets. Lane 1 now asks the attack-type-generalization question that the pre-modeling
> EDA arc was built to validate.

## Question

When a content-injection detector is trained on a disjoint set of BIPIA attack-types and evaluated on
**held-out** attack-types (carrier held constant), (a) how far does per-type detection collapse, and
(b) can the **ordering** of that collapse be predicted **pre-modeling** from shift + shortcut-exposure
signals? The pre-registered prediction is in `experiments/eda/OOD_WALL_PREDICTION/criteria.md` (FIXED rule)
+ `results.json` (predicted collapse rank).

## Hypothesis (load-bearing, pre-committed in criteria.md:31-46)

**H1 — the OOD wall is shortcut-mediated, not distance-mediated.** A detector trained on the train-attack-
types learns class-discriminative *lexical shortcuts*; it collapses on a held-out test-type to the extent
that (a) that type's positives sit far from the training distribution (shift) **and** (b) the train-pool
shortcuts fail to transfer (shortcut-exposure). Directional claim: the test-types ranked *most* likely to
collapse will show *larger* measured per-type LODO AUPRC drops than those ranked *least* likely.

## Outcome pre-commitment

- **SURVIVES** — one-sided top-k vs bottom-k permutation p<0.05 **AND** ≥10k bootstrap-CI lower bound >0
  (criteria.md:88-90). Pre-modeling shift+shortcut signals forecast collapse ordering.
- **FALSIFIED** — the dual rule is not met. Pre-modeling signals do **not** forecast collapse ordering —
  itself a publishable methodological finding (measurement-error attenuation biases *against* H1, so a
  positive result is conservative).
- **Likely aggregate outcome** (spec §7): near-random collapse on the disjoint test-types — H1 is about the
  *ordering* of that collapse, not its absolute level. The deliverable is the **fair** measurement + the
  ID→LODO ("benchmarks lie") inflation demonstration.

## Prior evidence references

- EDA arc (`experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md`): **carrier dominates the MiniLM embedding**
  (silhouette by-carrier 0.197 vs by-attack-type −0.023; KMeans→carrier ARI 0.98 vs →type −0.001) — the
  attack-type signal is embedding-invisible; BIPIA uncontaminated vs the 8-dataset working set.
- Literature (criteria.md:42-45): distance necessary-not-sufficient (Kpotufe & Martinet 2018; Geirhos 2020);
  λ non-estimable (Zhao et al. 2019); separability ≠ collapse (arXiv:2602.14161 — 96.6% separable ↔ 8.4pp drop).
- Submission v1.1.2 DeBERTa null result (backbone-invariance); Round-7 V0 rung decomposition.

## Success criteria

- AUPRC (+ bootstrap CI) + TPR@LowFPR (1%, 0.5%, 0.1%) per fold per ADR-036; benign FPR on NotInject.
- Per-test-attack-type diagnostic AUPRC + val→test drop **persisted** (the §6.5 falsification input).
- Per-row predictions parquet persisted per `(rung, fold, seed)`.

## Bail-out criteria

- Local GPU sweep infeasible within budget → run the feasibility probe, then escalate to gated cloud GPU
  (`decisions/contingency_unlock_N.md`).
- eval-toolkit API breaking change (unlikely — v1.x frozen per ADR-051).

## ADR pointers

- ADR-052 (study design; defers lane/chapter reorg to post-results) · ADR-051 (eval-toolkit v1.x pin)
- ADR-036 (TPR@LowFPR) · ADR-027 (single-class over-defense metric)

## Cross-references

- `experiments/lane-1/protocol.md` · `docs/planning/attack-type-lodo-harness-spec.md`
- `experiments/eda/OOD_WALL_PREDICTION/{criteria.md,results.json,FINDINGS.md}`
- Book chapter 8 + fragments at `book/src/content/fragments/lane-1/{methodology,results,interpretation}.mdx`
