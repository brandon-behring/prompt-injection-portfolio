# OOD-wall prediction — pre-modeling collapse-RANK forecast: PRE-REGISTERED criteria

**Pre-registered:** 2026-05-29, **before any E1 shift metric (PAD/MMD), C1 log-odds, or C2
competency-baseline result has been computed on the BIPIA folds, and before any Lane-1 model
is trained.**

**Attestation:** at the time of writing, (a) no proxy-A-distance, MMD, log-odds, or
competency-baseline number has been observed on the constructed BIPIA train/test rows; (b) the
**validation target does not yet exist** — Lane-1 (ADR-052) modeling has not run, so the
per-test-attack-type LODO accuracy gaps this forecast will be judged against are unknown and
unknowable here. The fusion rule + falsification test below are fixed *before* the predicted
ranking is computed and *before* any detector is trained. This is the anti-prototype discipline:
the predecessor recovered the OOD wall as a *post-hoc interpretation*; here the prediction is
committed in advance and is falsifiable. Any later change requires a written rationale appended to
this file (not a silent edit).

*Prior observed information (disclosed for transparency):* RC0 (`../RC0_BIPIA/results.json`)
reported per-type *within-type* MiniLM cosine diversity (0.11–0.70). That is diversity **inside**
each type, not cross-type **shift** nor **shortcut**-transfer — neither input to the rule below.
The rule was fixed without consulting those values for ranking.

## Question

Can the magnitude of OOD collapse be **predicted pre-modeling**? Concretely: rank the **14 disjoint
BIPIA test-attack-types** by how much an attack-type-LODO detector's per-type detection performance
will collapse (in-distribution → held-out), using only pre-modeling signals (distribution shift +
shortcut-exposure) — then test that predicted ranking against the eventual measured per-type LODO
gaps once Lane-1 trains. An honest "the prediction fails to beat chance" is an acceptable, publishable
outcome (it would itself refute the shortcut-mediated-collapse hypothesis).

## Hypothesis (load-bearing, pre-committed)

**The OOD wall is shortcut-mediated, not distance-mediated.** A detector trained on the
train-attack-types learns class-discriminative *lexical shortcuts*; it collapses on a held-out
test-type to the extent that (a) that test-type's positives sit far from the training distribution
(shift) **and** (b) the train-pool shortcuts fail to transfer to it (shortcut-exposure). Therefore:

> **H1 (primary):** the test-types we rank as *most* likely to collapse will show *larger* measured
> per-type LODO AUPRC drops than the test-types we rank as *least* likely — a directional,
> one-sided claim.

Rationale + literature: distance alone is necessary-not-sufficient (Kpotufe & Martinet COLT 2018;
Geirhos NMI 2020); the H-divergence bound's λ term is non-estimable and large under our cross-type
label structure (Zhao et al. ICML 2019); and PI-specifically, separability ≠ collapse
(arXiv:2602.14161, 2026: a **96.6% dataset-classifier accuracy** *and, separately,* an **8.4pp CV→LODO AUC drop** (0.996→0.912) — two distinct figures the paper *associates*, not equates). Hence the fusion of shift **and**
shortcut, not shift alone.

## Prediction construction (fusion rule — FIXED here)

For each of the **14 test-attack-types** `t` (carrier pooled across email/code/table):

1. **E1 shift rank** — proxy-A-distance (PAD) and unbiased MMD between the **pooled train-positive**
   distribution and the **type-`t` test-positive** distribution, in both TF-IDF and MiniLM-embedding
   spaces. Higher distance ⇒ higher predicted collapse. Rank the 14 types by the mean of the
   (z-scored) PAD and MMD (embedding space primary; TF-IDF reported alongside).
2. **C2 shortcut-transfer rank** — fit the partial-input/competency baselines (length-only,
   char-n-gram, BoW logistic) on the **train pool**, evaluate per test-type `t`; the per-type
   competency AUPRC = how well the cheap shortcut transfers. *Lower* transfer ⇒ higher predicted
   collapse. (C1 log-odds identifies *which* train-pool tokens are the shortcuts and is reported as
   the mechanism evidence behind C2.)
3. **Fused collapse rank** = **equal-weight average of the E1-shift rank and the C2-shortcut-failure
   rank**; ties broken by the C2-shortcut-failure rank (the mechanism H1 privileges). This ordered
   list of 14 types is the **primary prediction**, recorded in `results.json` before Lane-1 trains.

**Secondary (coarse) prediction** — the collapse-severity *order* of the 3 committed fold-structures:
core attack-type-LODO vs obfuscation technique-LODO vs the joint carrier+attack external check. Stated
as a directional ordering with a one-sided sign check (n=3 — a weak sanity check, labeled as such).

## Falsification test + decision rule (FIXED here)

Judged later against the **per-test-attack-type diagnostic LODO AUPRC drops** that Lane-1 records
(see the harness-spec pre-commit; per-type N=5 ⇒ these are *diagnostic*, so the test below uses only
the tails, never a full correlation, which N=5 noise would attenuate toward zero — regression
dilution, Spearman 1904).

- **PRIMARY — one-sided top-k vs bottom-k permutation contrast** (`k = 4`): the `k` test-types we
  predict will collapse **most** have a larger *mean* measured LODO drop than the `k` we predict will
  collapse **least**. Tested by a one-sided exact/permutation test (`scipy.stats.permutation_test`,
  `permutation_type='independent'`, statistic = difference in mean drop, `alternative='greater'`).
  Chosen over a full rank correlation because the tail contrast is materially more powerful + more
  noise-robust at small n (it averages `k` types per tail).
- **SECONDARY effect size — Kendall τ-b** over all 14 types (`scipy.stats.kendalltau`,
  `variant='b'`, exact null when untied), reported one-sided; *descriptive, not the gate* (n=14
  critical τ-b ≈ 0.36 one-sided, but attenuation makes it conservative).
- **Uncertainty** — bootstrap the whole pipeline (**≥10 000** item-level resamples within each type — **superseded by payload-cluster, Revision 1**;
  percentile **and** BCa CIs on the top-k−bottom-k mean-drop difference); flag fragility if
  percentile and BCa disagree materially.
- **DECISION RULE — the prediction SURVIVES iff:** (1) the one-sided permutation p < 0.05 **AND**
  (2) the one-sided 95% bootstrap CI lower bound on the top-k−bottom-k mean-drop difference > 0.
  Otherwise the shortcut-mediated-collapse hypothesis (H1) is **falsified** for this study.
  Measurement-error attenuation biases *against* H1, so a positive result is conservative — stated
  in advance.
- **Fold-size policy:** any fold with < 10 scored items is merged into its attack-family×carrier
  parent before ranking (keeps per-fold estimates reliable; bounds attenuation).

## Locked metric knobs (committed before measurement)

| Component | Locked choice |
|-----------|---------------|
| Embedding | `make_minilm_embedder` (`all-MiniLM-L6-v2`), L2-normalized; GPU |
| **PAD** | **linear** domain-classifier (LinearSVC), **fixed strong regularization** (`C=0.1`, pre-registered), ε = stratified **5-fold CV** held-out 0/1 error; PAD = 2(1−2ε) with CV/bootstrap CI. **NOT** the rpryzant `SVC(C=3000)`+MAE recipe (overfits to PAD≈2 at small n). |
| PAD sanity floor | within-dataset random-split PAD must be ≈0; reported as a false-positive floor |
| **MMD** | **unbiased** estimator (negatives retained), **RBF** kernel, bandwidth = **median heuristic on a frozen pooled reference**, held fixed across all type-folds; permutation test **B ≥ 1000**, p = (1+count)/(B+1) (Phipson–Smyth 2010) |
| MMD caveat | a non-significant MMD p is **not** evidence of "no shift" (low power at d=384, small n) — pre-committed |
| Log-odds (C1) | Monroe et al. 2008 informative-Dirichlet, per class/type, min-count threshold (pre-registered, e.g. ≥ 5 occurrences) |
| Competency (C2) | length-only, char-n-gram, BoW logistic; trained on train pool, evaluated per test-type; AUPRC vs per-type floor |
| Bootstrap | ≥ 10 000 item-level resamples; percentile + BCa **(superseded → payload-cluster, Revision 1)** |
| Rank fusion | equal-weight average of E1-shift rank + C2-shortcut-failure rank; C2 tiebreak |

## Cross-dataset confound controls (for the DESCRIPTIVE audit matrix only — NOT the prediction)

The prediction is BIPIA-internal. The separate D2/D3 contamination/landscape **audit matrix** (the
"usable + flagged, seed-sampled" working set) computes the same PAD/MMD across *different datasets*,
where the distance largely measures a **dataset fingerprint** (length, vocabulary, formatting,
tokenization) and conflates covariate with label-semantics shift. For the audit matrix only:
length-matching / length-stratification; near-dedup (MinHash); mask dataset-ID-predictive tokens
(delimiters/templates); report PAD/MMD **with and without** controls + the within-dataset random-split
≈0 sanity baseline. The audit matrix is descriptive context; it is **not** an input to H1.

## Honesty notes (pre-committed)

- Per-type N=5 ⇒ the per-type LODO drops are genuinely noisy; this is *why* the test is a tail
  contrast, not a correlation. The harness-spec pre-commit only requires that these diagnostic
  per-type AUPRCs be **recorded** — they remain diagnostic, never headline.
- The likely study outcome (harness-spec §7) is near-random collapse on the disjoint test-types. H1
  is about the *ordering* of that collapse, not its absolute level.
- Obfuscation test-types (Substitution Ciphers, Base Encoding, Reverse Text, Emoji Substitution) are
  character-transformation attacks; if char-n-gram shortcuts trained on the *train* obfuscation types
  fail to transfer, H1 predicts they collapse hardest — a concrete, checkable sub-claim.
- A null result (H1 falsified) is reported as such; it would mean pre-modeling shift+shortcut signals
  do **not** forecast collapse ordering — itself a publishable methodological finding.

## Revision policy

Any change to the hypothesis, fusion rule, metric knobs, fold set, test statistic, or decision rule
after this timestamp requires a **written rationale appended below** (never a silent edit). The
predicted ranking, once computed, is likewise frozen and dated.

## Predicted ranking (computed after this pre-registration, before Lane-1 trains)

*To be recorded in `results.json` + `V5`/`V9` figures — the 14 test-types in predicted
collapse-rank order, the per-type E1/C2 components, the top-k/bottom-k sets, and the secondary
3-fold-structure ordering. Dated on production.*

## Verification (deferred — run once Lane-1 produces the per-type diagnostic LODO gaps)

*Apply the FIXED decision rule above: top-k vs bottom-k one-sided permutation test + bootstrap CI;
report Kendall τ-b; record SURVIVES / FALSIFIED. No knob is revisited at that point.*

## Revision 1 — 2026-05-30: resampling unit (payload-clustered) + what the gate tests

**Status:** amendment to the FIXED test, appended per the Revision policy. Adopted
**before the confirmatory Lane-1 LoRA/full-FT headline data exists** (only the $0
cheap-rung rehearsal — tfidf + frozen — has run); motivated by a statistical error in
the locked uncertainty spec, not by any confirmatory result.

**R1 — resampling unit corrected to the payload cluster (the honest independent unit).**
Each test-type's positives are **5 BIPIA attack strings (payloads) × 12 contexts × 3
carriers = 180 rows**, so the independent unit is the **payload (n=5/type)**, not the row.
- *Bootstrap (gate 2)* — the locked "≥10 000 **item-level** resamples within each type"
  (§Falsification, §Locked knobs) is **pseudo-replicated** (treats 180 dependent rows as
  independent). Corrected to **payload-cluster** resampling: resample each type's 5 payload
  ids with replacement (shared across seeds), recompute per-type AUPRC, then the
  top-k−bottom-k contrast; ≥10 000 iters; one-sided 95% percentile CI lower bound.
  Negatives held fixed (shared across types ⇒ cancel in the contrast); seeds averaged.
- *Permutation (gate 1)* — **restored to the pre-registered type unit** ("averages k types
  per tail", §primary), which the multi-seed implementation had inflated by pooling seeds.
  Exact one-sided permutation over the 2k=8 tail types, all C(2k,k)=**70** splits. Minimum
  achievable one-sided p = **1/70 ≈ 0.0143** (the k=4 design is near-saturated; disclosed).
- *Decision rule UNCHANGED*: SURVIVES iff permutation p<0.05 AND bootstrap CI-low>0.
- *Estimator*: `experiments/attack-type-lodo/falsify_clustered.py` (reads
  `predictions.parquet`; the pre-pooled drop in `metrics.json` cannot support clustering).

**R2 — what the gate tests (levels, not magnitude).** The per-type drop is
`val_auprc − test_auprc[t]` with `val_auprc` one per-(rung,seed) scalar; in the
top-k−bottom-k difference the constant minuend **cancels**, so the contrast is
algebraically a test on per-type test-AUPRC **levels** — the predicted **detectability
ordering**, not collapse *magnitude*. H1's "collapse" wording stands as the motivating
hypothesis; the gate is honestly an ordering test. The "benchmarks-lie / ID→LODO
inflation" claim is carried **separately and descriptively** by the per-rung val-vs-test
table and the headline-AUPRC-vs-prevalence-floor observation (headline AUPRC ≈0.96–0.98
vs no-skill floor ≈0.926 at 92.6% positive prevalence) — **not** by this gate.

**R3 — permutation resolution (disclosure, no rule change).** At k=4 the exact
permutation is near-saturated (min-p 0.0143, no headroom). The bootstrap CI and the
Kendall τ-b over all 14 types (secondary) carry the higher-resolution evidence.

**Rehearsal validation (cheap rungs, NOT confirmatory).** Under the corrected estimator
both cheap rungs SURVIVE — tfidf: T=+0.135, perm p=0.0143 (floor = perfect tail
separation), cluster-bootstrap CI-low=+0.111 (100% of resamples >0), τ-b=0.45 (p=.013);
frozen: T=+0.082, perm p=0.0143, CI-low=+0.064 (100% >0), τ-b=0.58 (p=.0015). The
confirmatory verdict still requires the complete ≥3-seed × 4-rung sweep (write-gate).
[Superseded by **Revision 2** (2026-06-01): the required set is now the 3-rung
`tfidf+frozen+lora` ceiling; `full_ft` deferred to a trigger-gate — ADR-054.]

## Revision 2 — 2026-06-01: write-gate required rung set 4→3 (full-FT deferred to a trigger-gate)

**Status:** amendment to the FIXED test, appended per the Revision policy. Adopted **before any
confirmatory LoRA headline data exists** (only the $0 cheap-rung rehearsal — tfidf + frozen — has
run); motivated by an **execution/cost reprioritization** (ADR-054), **not** by any confirmatory
result. The decision rule, statistics, fold set, `k`, tail sets, and the payload-clustered estimator
(Revision 1) are all **unchanged**; only the *manifest-completeness predicate* moves.

**R2.1 — required rung set reduced from 4 to 3.** The write-gate (`falsify_ood_wall.manifest_complete`,
fed by `harness.rebuild_manifest` / `detectors.REQUIRED_RUNGS`) now opens on the complete ≥3-seed
**`tfidf + frozen + lora`** sweep. The §6.5 verdict is judged on the **`lora`** rung — already the
preferred headline rung (`falsify_ood_wall._RUNG_PREFERENCE` lists `lora` first) and the confirmatory
target this criteria always named ("LoRA/full-FT"). `full_ft` is **deferred to a conditional
trigger-gate** (PORTFOLIO_PLAN §16, ADR-054): it stays selectable (`--rungs full_ft`) and is run +
folded in **iff** the trigger fires. This supersedes Revision 1's closing "still requires … 4-rung" clause.

**R2.2 — the decision rule is UNCHANGED.** SURVIVES iff the type-level permutation p < 0.05 **AND** the
payload-cluster bootstrap one-sided 95% CI lower bound > 0. No knob, statistic, fold set, `k`, tail set,
embedding, or estimator changes. The evidence basis (which rung's per-type AUPRCs are judged) was always
LoRA-first; only *which rungs must finish before the verdict may be written* moved.

**R2.3 — why this is not goalpost-moving (honesty clause).** (i) the decision rule is byte-for-byte
unchanged; (ii) the judged rung (`lora`) is unchanged and was always the headline; (iii) `full_ft` is
*deferred with a written, fireable re-activation trigger*, not deleted — the never-measured full-FT OOD
point remains a registered branch (ADR-052's goal preserved, not abandoned); (iv) logged with a timestamp
+ rationale, not a silent edit; (v) adopted before the confirmatory LoRA data exists, so it cannot be a
reaction to a result. The dropped rung is the *ceiling above the ceiling*, not the rung H1 is about.

**Reference column (non-gating).** ADR-054 also adds an off-the-shelf reference column
(`reference_scorers.py`: ProtectAI now; Meta PG1/PG2 when their gate is granted) scored on the LODO test
sets. These untrained probes are **outside** the rung ladder (`reference_*.test_scores.parquet`, not in
`REQUIRED_RUNGS`) and **cannot** affect this gate or the verdict — they are descriptive context only.

---

## Realized verdict — 2026-06-01 (record only; does NOT alter the fixed test above)

The write-gate opened on the complete `tfidf + frozen + lora` sweep (3 folds × 3 seeds; LoRA on a
RunPod H100). Applying the **unchanged** rule to the **`lora`** rung: `T = −0.003`, perm p = 0.900,
CI-low = −0.008 → **FALSIFIED**. The cheap rungs SURVIVE on the same merged tree (tfidf T = +0.135 /
frozen T = +0.082; both perm p = 0.014, CI-low > 0). The monotone collapse of `T` with capacity is the
realized reading: the OOD wall is real for lexical / frozen-embedding detectors and **dissolves** under
end-to-end LoRA — a **capacity-dependence** effect. (The pre-registered S2 caveat covered prediction-*encoder* choice — MiniLM → frozen ModernBERT — and held: the ranking transferred to the frozen rung; the LoRA dissolution is the broader capacity finding S2 did not pre-commit.) Full record + interpretation:
`FINDINGS.md` §"Realized verdict"; machine-readable: `falsification_verdict.json`.
