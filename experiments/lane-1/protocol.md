---
lane_id: lane-1
slug: lane-1-attack-type-lodo
hypothesis_id: H-LANE-1
title: Lane 1 execution protocol — attack-type-LODO detector harness (ADR-052)
date_locked: 2026-05-29
status: active
supersedes: lane-1-direct-baselines (reference-scorer comparison; pre-ADR-052 skeleton)
---

# Lane 1 — Protocol (attack-type-LODO)

> **Reconciled 2026-05-29 (ADR-052).** The pre-ADR-052 framing of this lane (a reference-scorer
> comparison on a pooled-OOD slate, TF-IDF trained on the Lane-2 MR-3 corpus, slate incl.
> PINT/AgentDojo/InjecAgent) was a `skeleton` that the pre-modeling EDA arc superseded: it depended on
> the not-yet-built Lane-2 corpus and on datasets excluded as un-loadable (the EDA "honest ceiling"). Lane
> 1's modeling is now the **attack-type-LODO generalization study** locked by **ADR-052**. The reference-
> scorer baselines (ProtectAI v1/v2, Meta Prompt-Guard 2) are **descoped from Lane 1** (they survive only
> as the V10 reference-scorer diagnostic in `experiments/eda/OOD_WALL_PREDICTION/`).

**Executable spec (source of truth):** `docs/planning/attack-type-lodo-harness-spec.md`.
**Code:** `experiments/attack-type-lodo/`. **Pre-registration this lane validates:**
`experiments/eda/OOD_WALL_PREDICTION/{criteria.md,results.json}` (the §6.5 OOD-wall falsification, issue #2).

## Question

Does a content-injection detector trained on a disjoint set of BIPIA attack-types **generalize** to
held-out attack-types — and can the *ordering* of its per-type collapse be predicted pre-modeling
(`hypothesis.md`)? Carrier is held constant; the only shift is attack type.

## Data (spec §1)

BIPIA (`microsoft/BIPIA`, verified, local `data/raw/BIPIA/benchmark/`), via the reused loader
`experiments/eda/OOD_WALL_PREDICTION/bipia_carrier.py` (`build_examples()`):
- **Positive:** a scenario context with one BIPIA attack string suffix-injected (records `attack_type`,
  `subfamily ∈ {task-intent, obfuscation}`, `carrier`, `position`).
- **Negative:** the same contexts clean + NotInject benign-with-trigger prompts (over-defense control).
- Carriers: `email` / `code` / `table` (redistributable). `qa` / `abstract` license-gated → **excluded**.
- Attack pool: 15 types × 5 strings/split; **drop "Language Translation"** (only overlap) → **14v14 disjoint**.
- BIPIA's own context train/test split keeps contexts disjoint (no context-memorization confound).

## Folds (spec §2)

1. **Core — attack-type-LODO** (carrier constant): train contexts(train) × train-types → test contexts(test) × test-types. *Headline.*
2. **Obfuscation technique-LODO:** train {Alphanumeric, Homophonic, Misspelling, Anagram, Space-Removal} → test {Substitution-Ciphers, Base-Encoding, Reverse-Text, Emoji-Sub}.
3. **External — joint carrier+attack shift:** train {code, table} × train-types → test {email} × test-types.

Pre-run **source-disjointness assertion** (spec §6): no train↔test attack-type or context overlap.

## Detectors / rungs (spec §3–§4)

ModernBERT-base rungs — **frozen-probe**, **LoRA** (r∈{8,16} swept on val), **full-FT** (LR swept incl ~2e-5);
**TF-IDF + LogisticRegression** classical floor. Each rung gets its **own val-selected recipe** from a
**train-internal val split** (carve from TRAIN only; never touch test-types/contexts). Precision is
**device-adaptive** (bf16 on Ampere+, else fp16 + fp32-softmax-cast — the RTX 2070 SUPER is Turing);
`class_weight` balanced.

## Metrics + reporting (spec §5)

Per fold: **AUPRC** (primary) with bootstrap CI + **random-floor = positive prevalence**;
**TPR@{1, 0.5, 0.1}% FPR**; **benign FPR** on NotInject; **val→test (ID→LODO) inflation** per rung.
**Retention pre-commit:** the per-test-attack-type **diagnostic AUPRC + val→test drop** are **persisted**
per `(rung, fold, seed)` alongside the predictions parquet (the §6.5 test is impossible otherwise). They
stay diagnostic (N=5/type) — retention ≠ promotion.

## §6.5 deliverable — OOD-wall falsification (issue #2)

After the per-type drops are persisted, run `experiments/attack-type-lodo/falsify_ood_wall.py`: the FIXED
rule in `OOD_WALL_PREDICTION/criteria.md` (one-sided top-k vs bottom-k permutation p<0.05 **AND** ≥10k
bootstrap-CI lower bound >0; Kendall τ-b secondary) → **SURVIVES / FALSIFIED**, written into the
OOD_WALL_PREDICTION artifacts **only** for a complete headline sweep (write-gated). A null result is publishable.

## Reproducibility (spec §6)

Seeds ≥3; `experiments/attack-type-lodo/MANIFEST.yml`; predictions parquet per `(rung, fold, seed)`;
source-disjointness assertion as a pre-run check.

## Test-contract attestations (preserved)

- `no_handrolled_metrics`: metrics use `eval_toolkit.scorecard` + `metric_specs` + `losses.RecallAtLowFPR` exclusively.
- `predictions_persisted`: parquet per `(rung, fold, seed)` under `experiments/attack-type-lodo/`.
- `library_imports_registered`: every `from eval_toolkit …` registered in `decisions/library_imports.md`.
- `source_disjoint`: `assert_source_disjoint` proves no train↔test attack-type/context overlap.

## Single-class slice handling

NotInject (over-defense probe): val-fixed FPR only per submission ADR-027; AUPRC/AUROC skipped via
scorecard `status="skipped"` for single-class slices.

## Contingency-unlock gates

- **M1→M2 (Lane 1b)** — if M1 confirms `hackett2025bypassing` 100% char-injection ASR ±5pp → cut Lane 1b
  12-technique matrix → 3 representative + severity ranking (per `docs/planning/dossier_implications_for_roadmap.md` Zone 2; §16).
- Tier C PromptShield SOTA anchor: unlock only on a `decisions/contingency_unlock_N.md` row + ADR-039.

## Honest limitations (spec §7)

Small attack diversity (75 strings/split, 5/type) → memorization risk; generalization is to 75 disjoint
test strings, not an open technique space. Per-type N=5 → diagnostic only; headline is the aggregate
type-split + obfuscation sub-family. qa/abstract excluded (license-gated). Likely outcome: collapse to
~random on disjoint test-types — accepted; the value is the *correct, fair* measurement + the val→test
inflation demonstration.

## Cross-references

- Hypothesis: `experiments/lane-1/hypothesis.md`
- Spec: `docs/planning/attack-type-lodo-harness-spec.md`; ADR: `decisions/ADR-052-attack-type-generalization-study-design.md`
- Dependent lanes: Lane 4 (stacker consumes Lane 1 rung scores as base features); Lane 2 (distillation comparison)
- Book chapter 8 + fragments at `book/src/content/fragments/lane-1/`
