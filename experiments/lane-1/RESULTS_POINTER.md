# Lane 1 — results pointer (formal close deferred)

> **State: STARTED (not CLOSED).** Lane 1 — the attack-type-LODO OOD-wall study (ADR-052) — has RUN, and
> its results are recorded **canonically in the EDA pre-registration directory** (where the write-gated
> §6.5 verdict must live). This pointer summarizes them and links the canonical records. The formal lane
> close (`results.md` + `decisions.md` + 3 book fragments) is **deferred to the prose pass** (Round-30 Q4
> + the 2026-06 audit): the closure contract (`tests/contracts/test_experiment_records_complete.py`) has
> no "results-recorded, fragments-deferred" state, so we keep the lane formally STARTED rather than stub
> fragments. **Independently re-verified 2026-06-01** — `experiments/AUDIT_2026-06/verification_report.md`
> (5/5 results reproduce from raw parquets, no mismatch).

## Headline — the §6.5 OOD wall is capacity-dependent (FALSIFIED at the LoRA ceiling)

| rung | representation | T (bottom−top per-type AUPRC) | perm p | CI-low | verdict |
|---|---|---|---|---|---|
| tfidf | lexical | +0.135 | 0.014 | +0.111 | SURVIVES |
| frozen | frozen MiniLM + LogReg | +0.082 | 0.014 | +0.064 | SURVIVES |
| **lora** | **end-to-end ModernBERT FT** | **−0.003** | **0.900** | **−0.008** | **FALSIFIED** |

Judged on `lora` per criteria Revision 2 → **FALSIFIED at the ceiling**. The pre-modeling collapse-ordering
prediction (built on the carrier-dominated frozen MiniLM embedding) does **not** transfer to an end-to-end
LoRA, which detects every attack type near-uniformly (test AUPRC 0.98–0.999). This is **capacity-dependence** (S2 pre-registered the frozen-encoder transfer, verified at frozen; the LoRA dissolution extends beyond S2's letter) — credible because the rule + tail sets + judged rung were fixed and
write-gated before any LoRA datum existed (audit V1 confirmed the pre-registration order + clustering unit +
leakage purge + write-gate all hold). Canonical:
`experiments/eda/OOD_WALL_PREDICTION/{falsification_verdict.json, FINDINGS.md, criteria.md, results.json}`.

## Exploratory companion folds (NOT pre-registered — generalization diagnostics only)

Two further LODO folds were run. The §6.5 top-k/bottom-k contrast is hard-wired to the core fold's 14
task-types and does **not** apply to these, so they are reported as held-out test AUPRC (mean over 3 seeds),
labelled exploratory:

| fold | what it holds out | tfidf | frozen | lora |
|---|---|---|---|---|
| `obfuscation_technique` | train surface-mutation → test encoding types (carrier pooled) | 0.948 | 0.963 | 0.990 |
| `carrier_plus_attack_external` | train carriers {code,table} → test {email} + disjoint types | 0.980 | 0.986 | 0.998 |

Both are monotone in capacity. **`carrier_plus_attack_external` shows no pooled carrier-shift gap** (val→test
drop is negative at every rung) — **but** its email test slice is 94% positive (prevalence-inflated), so a
carrier wall, if real, would surface in a **low-FPR / per-type** view, not pooled AUPRC. ⟹ This directly
shapes the carrier-LODO M2 pre-flight criteria (measure at low-FPR / balanced-benign, not pooled AUPRC).

## Off-the-shelf reference column (non-gating)

PG1 (Prompt-Guard-86M) separates BIPIA indirect attacks (≈0.84 attack / 0.04 benign, AUROC 0.97); the
direct-injection-trained ProtectAI-v2 is scope-blind (AUROC 0.44, below chance) → off-the-shelf collapse.
**Reporting caveat (audit V3):** report **AUROC / means**, not AUPRC alone — at prevalence ~0.93, AUPRC ≈0.92
is chance, which flatters a chance-level direct probe to look like a 0.92 "separator." Structurally
non-gating (outside `REQUIRED_RUNGS`; both verdict scripts glob only `*.predictions.parquet`).

## Canonical records (the actual results live here)
- §6.5 verdict + prediction: `experiments/eda/OOD_WALL_PREDICTION/{falsification_verdict.json, results.json, criteria.md, FINDINGS.md, v10_scores.json}`
- EDA geometry: `experiments/eda/OOD_WALL_PREDICTION/a1_v4_metrics.json` (carrier silhouette 0.197 / type −0.023; ARI 0.98 / −0.001)
- Per-fold metrics + predictions: `experiments/attack-type-lodo/results/seed={0,1,2}/<fold>/<rung>.{predictions.parquet, metrics.json}` (gitignored; 36 parquets + per-fold metrics.json)
- Independent re-verification: `experiments/AUDIT_2026-06/verification_report.md`
- Decisions: `decisions/{ADR-052, ADR-054, ADR-055}-*.md`

## Formal-close checklist (deferred to the prose pass)
- [ ] `results.md` — per-type AUPRC table + NotInject over-defense FPR (per-fold `metrics.json`) + val→test inflation
- [ ] `decisions.md` — capacity-dependent reading (S2 = frozen-encoder transfer verified; LoRA dissolution beyond S2's letter); Lane-2 → carrier-axis implication
- [ ] 3 book fragments — `book/src/content/fragments/lane-1/{methodology,results,interpretation}.mdx`
- [ ] flip MANIFEST `lane-1.state` → `closed`
