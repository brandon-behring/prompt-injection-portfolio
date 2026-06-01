# Independent re-examination report — 2026-06 audit

> **Method.** Five independent **adversarial** verifier agents (each instructed to *find discrepancies,
> not confirm*) recomputed each persisted result from the raw `predictions.parquet` files via the
> harness code path — not from the committed JSONs. Scope: **all 3 LODO fold families** + the EDA
> carrier-dominance geometry + the off-the-shelf reference column. Decision: any reproducibility
> **mismatch halts** before Phases 2–3.
>
> **Verdict: NO MISMATCH.** Every persisted number reproduced (several bit-for-bit). The §6.5
> FALSIFIED-at-`lora` headline survives independent recompute and adversarial scrutiny. Three
> non-blocking findings (2 methodological, 1 cosmetic) are recorded below as Phase-2/3 work items.

## V1 — §6.5 OOD-wall verdict (`core_attack_type`, pre-registered) — **REPRODUCES**

| rung | recomputed T | perm p | bootstrap ci_low | verdict | vs persisted |
|---|---|---|---|---|---|
| tfidf | +0.1351 | 0.0143 (PASS) | +0.1111 (PASS) | **SURVIVES** | ✓ headline +0.135 |
| frozen | +0.0819 | 0.0143 (PASS) | +0.0635 (PASS) | **SURVIVES** | ✓ headline +0.082 |
| **lora** | **−0.0031** | **0.900 (FAIL)** | **−0.0075 (FAIL)** | **FALSIFIED** | ✓ JSON (T=−0.0030903, ci_low=−0.007454) |

All ΔT ≤ 1e-4; verdicts identical. Adversarial integrity probes — **all clean:**
- **Pre-registration order:** `results.json` (the fixed top-k/bottom-k tails) + `criteria.md` committed
  2026-05-29; the `lora` parquets/verdict produced 2026-06-01. The rule + tails were frozen **before**
  the `lora` datum existed. `falsify_clustered.main()` reads the tails straight from `results.json`.
- **Clustering unit:** positives grouped by **payload** (5/type); the bootstrap resamples payload ids,
  not the 180 rows — no pseudo-replication. Permutation exchanges **attack types** (n=2k=8).
- **Leakage purge:** `purge_train_context_overlap` fires (BIPIA email 11 shared contexts → 0 on both
  email-bearing folds; `carrier_external` correctly 0). `assert_source_disjoint` passes post-purge.
- **Write-gate:** `manifest_complete` required `complete_headline_sweep==true` + seeds [0,1,2] + all 3
  required rungs — satisfied. The no-write rehearsal (`falsify_clustered.py`) was used; `falsify_ood_wall.py`
  (the writer) was not run.
- **Honest red flags disclosed:** k=4 exact-perm floor min-p=1/70≈0.0143 (near-saturated); ~5 payload
  clusters/type; "monotone collapse" is openly post-hoc — and the `lora` verdict is **gate-driven** (both
  primary gates FAIL regardless of narrative). All disclosed in `criteria.md` Rev 1 + the module docstring.

## V1-ext — the two additional folds (EXPLORATORY, non-pre-registered) — **REPRODUCE**

Both ran + saved properly (9/9 parquets **and** 9/9 per-fold `*.metrics.json`; predictions bit-exact to the
persisted `headline.pr_auc.value`). The §6.5 top-k/bottom-k contrast is hard-wired to `core`'s 14 task-types
and does **not** apply to these — so these are generalization diagnostics, **not** §6.5 verdicts.

**`obfuscation_technique`** (train surface-mutation types → test encoding types; carriers pooled):

| rung | held-out test AUPRC (mean ± sd, 3 seeds) |
|---|---|
| tfidf | 0.948 ± 0.008 |
| frozen | 0.963 ± 0.002 |
| lora | 0.990 ± 0.002 |

Strong, **monotone in capacity**, mild LODO penalty shrinking to ~0 under `lora`. No OOD collapse.

**`carrier_plus_attack_external`** (joint shift: train carriers {code,table} → test carrier {email} + disjoint
test attack-types):

| rung | held-out test AUPRC (mean ± sd, 3 seeds) | val→test drop |
|---|---|---|
| tfidf | 0.980 ± 0.008 | −0.063 |
| frozen | 0.986 ± 0.003 | −0.023 |
| lora | 0.998 ± 0.001 | −0.004 |

**Material finding (carrier axis):** at the *pooled held-out-test* level this fold shows **no carrier-shift
gap** — the val→test drop is *negative* at every rung (email test ≥ in-distribution val). ⚠️ **But the email
test slice is 94% positive (50 negatives), so pooled AUPRC is prevalence-inflated**; a carrier gap, if real,
would surface in a **low-FPR / benign-FPR or per-type** view, not this headline number. → **Directly informs
the carrier-LODO Phase-3 criteria (C1): measure at low-FPR / balanced-benign / per-type, not pooled AUPRC.**

## V2 — EDA carrier-dominance geometry — **REPRODUCES (bit-for-bit, Δ=0)**

| metric | grouping | recomputed | persisted | Δ |
|---|---|---|---|---|
| silhouette | by_carrier | 0.197333 | 0.197333 | 0 |
| silhouette | by_attack_type | −0.022693 | −0.022693 | 0 |
| ARI (kmeans) | vs carrier | 0.980348 | 0.980348 | 0 |
| ARI (kmeans) | vs attack_type | −0.000649 | −0.000649 | 0 |

Computed on the full 384-dim MiniLM embedding (not UMAP). Carrier dominates the geometry; attack-type is
embedding-invisible. The "carrier is the standing wall" claim is geometrically well-founded.
- *Cosmetic:* `run_a1_v4.py:53` inline comment says "PCA-2D" while the code uses UMAP (the header docstring
  is correct; the projector does not feed silhouette/ARI, so no metric impact). → trivial fix.

## V3 — off-the-shelf reference column (non-gating) — **REPRODUCES**, with a metric caveat

| scorer | mean attack | mean benign | AUPRC | **AUROC** |
|---|---|---|---|---|
| PG1 (Prompt-Guard-86M, indirect-capable) | 0.843 | 0.041 | 0.998 | **0.972** |
| PG2 (Llama-Prompt-Guard-2) | 0.037 | 0.006 | 0.958 | 0.661 |
| ProtectAI-v2 (direct-trained) | 0.259 | 0.262 | 0.922 | **0.444** |

- PG1 0.843/0.041 reproduces the 0.86/0.04 EDA headline (mean over 14 slices; not cherry-picked). A live
  re-score of 16 BIPIA texts reproduced the persisted `y_score` **exactly (max abs err 0.0)**.
- **Non-gating CONFIRMED:** `reference_*.test_scores.parquet` is structurally walled off — `harness.py`
  `_scan_artifacts` globs only `*.predictions.parquet`; both verdict scripts ignore `reference_`/`test_scores`;
  `REQUIRED_RUNGS=("tfidf","frozen","lora")`.
- **Methodological finding (reference reporting):** at prevalence ~0.93, chance AUPRC ≈ 0.92, so
  **ProtectAI's AUPRC 0.922 is at-chance** and its mean attack (0.259) < mean benign (0.262) — its **AUROC
  0.444 (below random)** is what actually confirms scope-blindness. → **The reference column should be
  reported with AUROC (or means), not AUPRC alone** — AUPRC at this prevalence flatters a chance-level
  direct probe to look like a 0.92 "separator." The narrative (off-the-shelf collapse) is correct; the AUPRC
  framing is misleading.

## Findings → Phase-2/3 work items

1. **[Phase 3 / C1 — carrier-LODO criteria]** The carrier shift is invisible in prevalence-inflated pooled
   AUPRC; the carrier-LODO must measure at **low-FPR / balanced-benign / per-type**. Fold this into the
   criteria Revision *before* the run, and weigh it when deciding whether the paid `lora` rung is worth it.
2. **[Phase 2 — reference reporting]** Add **AUROC / means** alongside AUPRC for the reference column (and
   note the prevalence caveat in the Lane-1 record). Non-gating, so this is a reporting improvement, not a
   verdict change.
3. **[Phase 2 — cosmetic]** Fix the stale `run_a1_v4.py:53` "PCA-2D" comment (code uses UMAP).

## Provenance
- Verifiers: 5 independent `general-purpose` agents, 2026-06-01; each recomputed from
  `experiments/attack-type-lodo/results/seed={0,1,2}/<fold>/<rung>.predictions.parquet` (36 parquets / 15 MB,
  local + gitignored). Models (MiniLM, PG1/PG2/ProtectAI) were HF-cached; no environment block.
- Persisted records cross-checked: `experiments/eda/OOD_WALL_PREDICTION/{falsification_verdict.json,
  results.json, criteria.md, a1_v4_metrics.json, v10_scores.json}`; per-fold `results/seed=*/<fold>/*.metrics.json`.
