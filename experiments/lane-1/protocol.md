---
lane_id: lane-1
slug: lane-1-direct-baselines
hypothesis_id: H-LANE-1
title: Lane 1 execution protocol — reference scorers + classical floor + same-corpus baselines
date_locked: TBD-M1
status: skeleton
---

# Lane 1 — Protocol

## Eval slate

| Source | SHA pin | Size | Stratification | Notes |
|---|---|---|---|---|
| BIPIA | TBD | TBD | source-disjoint LODO | Inherited from submission `configs/data/source_manifest.yaml` |
| AgentDojo | TBD | TBD | agentic-flow | Carryover per plan §5 |
| InjecAgent | TBD | TBD | agentic | Carryover |
| NotInject | TBD | TBD | over-defense probe | Carryover (per ADR-027 retired single-class metric) |
| LLMail-Inject EN | TBD | 5000 | LLMail subset | Round 1 Q5 stratified pull |
| PINT EN | TBD | 3016 | hard-negative | Lakera English-only |

## Checkpoints in scope

- Frozen-probe baseline (from submission HF Hub `BBehring/prompt-injection-frozen-probe-v1`)
- ProtectAI v1 + v2 (HF Hub `protectai/deberta-v3-base-prompt-injection*`)
- Meta Prompt Guard 2 86M (HF Hub `meta-llama/Prompt-Guard-86M`)
- TF-IDF + LogisticRegression (sklearn; trained on Lane 2 MR-3 corpus per Round 16 Q1)
- Optional: PromptShield Llama-3.1-8B (Tier C; gated)

## Execution sequence

### Phase 1: data prep (~$0; M1 Day 1)
1. `make verify-data-sources` (re-verify all 6 OOD sources reachable + SHA-pinned)
2. `python scripts/eval_from_hub.py --slate pooled_ood --predictions out/` (T0 entry)
3. Stratified pulls: LLMail-Inject 5K + PINT-EN 3016

### Phase 2: reference scorer eval (~$10 GPU; M1 Day 2-3)
1. Score each detector against pooled OOD slate
2. Compute `scorecard()` + `metric_specs.{pr_auc, roc_auc, brier, ece(n_bins=15)}`
3. Compute TPR@LowFPR (1%, 0.5%, 0.1%, 0.05%) per ADR-036
4. Paired-bootstrap delta CIs vs frozen-probe (10K resamples; BCa 95%)

### Phase 3: TF-IDF + LR training (~$0; M1 Day 4)
1. Train sklearn TfidfVectorizer + LogisticRegression on Lane 2 MR-3
   synthetic-indirect-v2 corpus (~20k rows; per Round 16 Q1 same-corpus rule)
2. Eval on pooled OOD; compute scorecard + TPR@LowFPR

### Phase 4: aggregate + persist (~$0; M1 Day 5)
1. Per-row predictions parquet at `evals/lane-1/predictions.parquet`
2. Cost ledger row at `evals/cost_ledger.csv`
3. results.md + decisions.md drafts

## Contingency-unlock gates

- Tier C PromptShield SOTA anchor ($40-50): unlock if M1 Tier B results show
  base detectors fall meaningfully behind expected SOTA on TPR@LowFPR
  benchmarks. Requires `decisions/contingency_unlock_N.md` row + ADR-039.

## Test-contract attestations

- `no_handrolled_metrics`: lane code uses `eval_toolkit.scorecard` +
  `metric_specs` exclusively (no F1/AUC reimplementation).
- `predictions_persisted`: parquet at `evals/lane-1/predictions.parquet`.
- `leakage_scan_present`: `scripts/leakage_scan.py` confirms no overlap
  between Lane 2 MR-3 training data + Lane 1 eval slates.
- `library_imports_registered`: every `from eval_toolkit ...` import
  registered in `decisions/library_imports.md`.

## Single-class slice handling

- NotInject (over-defense probe): val-fixed TPR only per submission ADR-027
  upstream enforcement (eval-toolkit#39); AUPRC/AUROC skipped via
  scorecard `status="skipped"` for single-class slices.

## Metric reporting deliverables

- Tier A (per ADR-036): TPR@LowFPR (1%, 0.5%, 0.1%, 0.05%) for every detector
- Tier B citations (per Round 7 Q1''''''): V0 rung decomposition (Ch 4
  citation); V4 contamination signature (Ch 5 sidenote)
- AUPRC + AUROC + Brier + ECE(n_bins=15) on multi-class slices via
  `scorecard()`
- Paired-bootstrap delta CIs vs frozen-probe

## Cross-references

- Hypothesis: `experiments/lane-1/hypothesis.md`
- Dependent lanes: Lane 2 (training corpus); Lane 4 (stacker uses Lane 1
  scores as detectors)
- Book chapter 8 + fragments at `book/src/content/fragments/lane-1/`
