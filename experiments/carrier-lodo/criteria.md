# Carrier-LODO validation — does end-to-end capacity dissolve the carrier OOD wall? PRE-REGISTERED criteria

**Pre-registered:** 2026-06-01, **before any carrier-LODO split has been constructed or any
carrier-held-out detector trained.** Registered by
[ADR-055](../../decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md) (Round 30 re-ladder) as the
**M1-exit → Lane-2-entry pre-flight** (PORTFOLIO_PLAN §16 Round-30 gates).

**Attestation:** at the time of writing, no carrier-LODO val/test AUPRC, per-fold gap, PAD, or MMD has
been computed. The decision logic + falsification rule below are fixed *before* any carrier-held-out
detector is trained. This is the carrier-axis sibling of the attack-type pre-registration
`../eda/OOD_WALL_PREDICTION/criteria.md`, and inherits its anti-prototype discipline (the predecessor
recovered the OOD wall as a *post-hoc* interpretation; here the rule is committed in advance and is
falsifiable).

## Why this gate exists (the claim it tests)

The Round-30 multi-axis spine
([ADR-055](../../decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md)) asserts: *the **attack-type**
axis is capacity-dependent (M1: end-to-end LoRA dissolves the per-type OOD gap — §6.5 FALSIFIED at the
`lora` ceiling, T 0.135 → 0.082 → −0.003), while the **carrier** axis dominates the representation
geometry and is the **standing wall**.* The carrier half is, so far, **geometric only**: the frozen
MiniLM embedding tracks the carrier, not the attack type (silhouette by-carrier **0.197** vs
by-attack-type **−0.023**; KMeans→carrier ARI **0.98** vs →attack-type **−0.001** —
`../eda/OOD_WALL_PREDICTION/FINDINGS.md` Key finding 1). M1 **held the carrier constant by design**
([attack-type-lodo-harness-spec.md](../../docs/planning/attack-type-lodo-harness-spec.md) §3), so
whether end-to-end capacity dissolves the *carrier* gap the way it dissolved the *attack-type* gap is
**untested**. This gate tests it, and sizes the gap Lane 2's training has to close.

## Question

Holding the method fixed (the M1 rung ladder tfidf → frozen → lora), does the **carrier-LODO
generalization gap** (train on a subset of carriers, test on a held-out carrier) **persist as capacity
rises** (→ the carrier wall is capacity-resistant; the spine is **validated** as a modeling result), or
does it **collapse toward zero at the `lora` rung** the way the attack-type gap did (→ end-to-end
capacity dissolves the carrier wall too; the spine is **revised** — capacity dissolves *both* axes)?

## Hypothesis (load-bearing, pre-committed)

**H_carrier (primary):** the carrier-LODO gap is **capacity-resistant** — it does **not** monotonically
collapse to ≈0 at the `lora` rung (contrast the attack-type axis, where T collapsed 0.135 → 0.082 →
−0.003). Directional, one-sided: G(lora) stays materially > 0.

The interesting outcome is genuinely either way. **H_carrier confirmed** → the carrier wall is a real,
capacity-resistant structural limit (validates the spine; motivates Lane 2's carrier-axis headline).
**H_carrier falsified** (carrier gap collapses at lora like attack-type) → capacity dissolves both
axes; the spine is honestly revised and Lane 2's headline is resized. Both are publishable.

## Design (FIXED)

- **Carrier-LODO folds:** leave-one-carrier-out over the **available** BIPIA carriers — **email, code,
  table** (qa, abstract are **license-gated** per
  [ADR-052](../../decisions/ADR-052-attack-type-generalization-study-design.md) and excluded; honest
  ceiling). 3 folds: hold out each carrier in turn, train on the other two.
- **Rung ladder:** tfidf + frozen (local, free) + lora (~$1, RunPod). Reuses the M1 attack-type-LODO
  harness with the **LODO axis swapped** attack-type → carrier; ≥3 seeds on the trainable rung.
- **Per-fold gap:** `G(rung, held-out-carrier) = val_auprc − test_auprc(held-out-carrier)`, val per the
  train-internal split (same val discipline as M1).

## Estimator + decision rule (FIXED logic; implementation specifics finalized in a pre-run Revision)

**The carrier axis has only n=3 carriers** — materially fewer than the 14-type attack axis. So this gate
is **honestly a directional, lower-power read**, not the 14-type top-k/bottom-k permutation contrast.
The §6.5 *philosophy* is reused (directional, bootstrap-CI-gated, fixed before data); the *statistic* is
adapted to the carrier structure:

- **Within-carrier resolution (carrier-clustered).** For each held-out carrier the test set still has
  the full payload × attack-type structure, so the CI on each `G(rung, carrier)` comes from a
  **payload-clustered bootstrap within the held-out carrier** (resample the held-out carrier's payload
  ids with replacement; ≥10 000 iters; one-sided 95% percentile CI). The held-out **carrier** is the
  LODO unit (n=3); the **payload** is the within-fold resampling unit (as in
  `../eda/OOD_WALL_PREDICTION/criteria.md` Rev 1 — payload-clustered, never row-level).
- **Primary read — the cross-rung pattern.** Report `G(rung)` = mean over the 3 held-out carriers, for
  rung ∈ {tfidf, frozen, lora}. **H_carrier SURVIVES iff** `G(lora) > 0` with its one-sided 95%
  bootstrap CI-low > 0 **AND** `G(lora)` does **not** collapse relative to the frozen rung
  (pre-registered non-collapse: `G(lora) ≥ ½·G(frozen)`). **H_carrier is FALSIFIED iff** `G(lora)`'s
  CI-low ≤ 0 (the carrier gap is statistically indistinguishable from dissolved at the ceiling — the
  `lora` attack-type pattern, T = −0.003, CI-low = −0.008).
- **Secondary (descriptive):** the monotone-collapse check across the 3 rungs (does `G` fall toward 0
  as capacity rises, as it did on the attack-type axis?), reported as a directional sign pattern (n=3
  rungs — a weak sanity check, labeled as such, exactly like the attack-type criteria's secondary
  3-fold-structure ordering).

**Honesty (pre-committed):** (i) n=3 carriers ⇒ the per-fold gaps are noisy and the cross-carrier mean
is a 3-point average — power is limited; the read is **directional**. (ii) The `½·G(frozen)`
non-collapse threshold is the one free knob; it is fixed **here, before any carrier-LODO datum**, and
any change requires a dated written rationale (revision policy below). (iii) The exact within-carrier
resampling unit + the per-fold row counts are **finalized in a dated Revision before the run**, once
read from the harness for the carrier folds — the *logic* (persistence-vs-collapse, CI-gated) is fixed
now so the finalization cannot cherry-pick the outcome.

## Honest limitations (pre-committed)

- Only 3 of BIPIA's 5 carriers are usable (qa/abstract license-gated) — the carrier axis is measured on
  email/code/table; generalization to the gated carriers is out of scope and stated as a ceiling.
- Three honest outcomes, not two: the carrier gap may be **large but capacity-resistant** (validates the
  spine), **large at cheap rungs but capacity-dissolved at lora** (revises the spine), or **small
  throughout** (the carrier wall was overstated by the geometry — `SMALL-THROUGHOUT`).
- Separability ≠ collapse (arXiv:2602.14161) applies here too: the carrier dominating the embedding
  (silhouette 0.197) does **not** by itself prove a carrier *detection* gap — that is exactly what this
  modeling gate measures rather than assumes.

## Revision policy

Mirrors `../eda/OOD_WALL_PREDICTION/criteria.md`: any change to the question, hypothesis, design,
estimator, or decision rule after this timestamp requires a **written, dated rationale appended below**
(never a silent edit). The implementation-finalization Revision (within-carrier resampling unit + row
counts) is expected **before** the run and must not change the persistence-vs-collapse logic.

## Verification (deferred — run as the M2 pre-flight, a separate present-first go)

Apply the FIXED logic above to the carrier-LODO sweep once it runs; record **SURVIVES** (carrier
capacity-resistant — spine validated) / **FALSIFIED** (carrier dissolved at lora — spine revised) /
**SMALL-THROUGHOUT** (carrier wall overstated). No knob is revisited at that point except per the
revision policy.

---

## Revision 1 — finalize the estimator (metric basis + implementation), 2026-06-01

**Dated, before any carrier-LODO split has been constructed or any carrier-held-out detector trained.**
This is the "implementation-finalization Revision before the run" the original anticipated (estimator §
(iii) + Revision policy). The persistence-vs-collapse **logic is UNCHANGED**; this Revision (i) fixes the
metric basis of `G` from AUPRC to ROC-AUC and (ii) finalizes the implementation specifics, both **before**
any carrier datum exists.

### (i) Metric basis: AUPRC → ROC-AUC (the prevalence fix)

**Change.** `G(rung, carrier) = val_roc_auc − test_roc_auc(held-out carrier)` (was `val_auprc − test_auprc`).

**Rationale (independent of any carrier-LODO result — motivated by the attack-type-axis audit, not a peek
at carrier results).** The 2026-06 audit (`../AUDIT_2026-06/verification_report.md`) established from the
**M1** data that **every BIPIA carrier is 83–94 % positive** (`bipia_carrier.build_examples`: email/code
contexts cap at ~50 negatives vs 840 positives; table ~168 neg). AUPRC is prevalence-sensitive, so
`val_auprc − test_auprc` confounds the detection-generalization gap with the **per-carrier prevalence
difference** between the val split (train carriers) and the held-out carrier. This is not hypothetical: the
M1 `carrier_plus_attack_external` fold (email held out, 94 % positive) produced a **negative** val→test
AUPRC drop — the AUPRC gap was empirically **blind** to the carrier shift. ROC-AUC is prevalence-invariant,
so `val_roc_auc − test_roc_auc` isolates the carrier generalization gap. Fixing this **before** any
carrier-LODO datum means it cannot cherry-pick the outcome (the carrier sweep has not run).

### (ii) Implementation specifics (finalized; logic unchanged)

- **Folds.** `folds._build_carrier_lodo` + the 3 fold names `carrier_lodo_{email,code,table}`: for held-out
  carrier `c`, **train = all rows with carrier ≠ c** (both BIPIA roles, all attack types); **test = all rows
  with carrier = c**. The **only** held-out axis is the carrier — attack types are **shared** across
  train/test by design, so the M1 `assert_source_disjoint` attack-type check is replaced by
  `assert_carrier_disjoint` (no carrier overlap; cross-carrier context overlap is nil by construction and
  still asserted). Val is carved from the **train carriers** via the existing `carve_val_from_train`, so
  `val_roc_auc` is in-(train-carrier-)distribution.
- **Persisted reference.** The harness `run_one` additionally persists `val_roc_auc` (point estimate on the
  fold's own val split); the predictions parquet holds only test rows, so the val reference must be carried
  in `metrics.json` (held fixed in the bootstrap).
- **Within-carrier resampling unit (CI on each `G(rung, c)`):** payload-clustered bootstrap **within the
  held-out carrier** — resample the held-out carrier's **payload ids** (~5 strings/attack-type × 14 types
  ≈ 70 payloads) with replacement, recompute `test_roc_auc`, hold `val_roc_auc` fixed; negatives held fixed;
  ≥10 000 iters. The cross-carrier mean `G(rung)` and its one-sided 95 % CI-low come from resampling all 3
  carriers per iteration and averaging. Held-out **carrier** = LODO unit (n=3); **payload** = within-fold
  unit (never row-level), as `../eda/OOD_WALL_PREDICTION/criteria.md` Rev 1.
- **Per-fold row counts (read from the loader, for the record):** held-out **email** ≈ 840 pos / ~50 neg;
  **code** ≈ 840 pos / ~50 neg; **table** ≈ 840 pos / ~168 neg (positives = ~70 payloads × 12 contexts;
  negatives = min(carrier contexts, 168)). The 83–94 % prevalence range is exactly why (i) moved off AUPRC.

**2026-06-10 audit correction (record-only; estimator unaffected):** the Rev-1 counts above are
single-role; the materialized folds pool BOTH BIPIA roles per the fold definition — 140 payload
clusters, 1,680 positives, negatives 100 (email/code) / 268 (table).

- **Secondary (descriptive only, NOT a gate):** the TPR@1%FPR val→test gap is reported but flagged
  descriptive — the held-out-carrier test negatives are few (~50; ~168 for table), so 1%-FPR is ill-resolved
  (~0.5–1.7 negatives) and cannot carry the verdict. ROC-AUC is the sole gate metric.

### Decision rule (UNCHANGED, restated on the ROC-AUC basis)

`G(rung) = mean over the 3 held-out carriers of G(rung, c)`. **H_carrier SURVIVES** iff `G(lora) > 0` with
one-sided 95 % bootstrap CI-low > 0 **AND** `G(lora) ≥ ½ · G(frozen)`. **FALSIFIED** iff `G(lora)` CI-low ≤ 0.
Else **SMALL-THROUGHOUT**. (Verbatim the original logic; only `G`'s metric basis changed from AUPRC to ROC-AUC.)

---

## Revision 2 — in-distribution val reference (confound fix), 2026-06-01

**Dated, after a single 1-fold tfidf smoke (`carrier_lodo_email`, seed 0) validated the fold builder on
real BIPIA but exposed a confound in the val reference; logged before the registered ≥3-seed sweep.** The
metric basis (ROC-AUC) and the persistence-vs-collapse decision logic are **UNCHANGED**; this Revision
fixes only how the val reference `val_roc_auc` is constructed.

**Problem (structural — visible in `carve_val_from_train`, independent of the smoke's direction).** The
shared harness carves val by an **attack-type mini-LODO** (it holds out `n_val_types` attack types when the
train pool has ≥6 types). A carrier-LODO fold's pooled train carries all ~28 attack types, so the default
val is **attack-type-OOD**: `val_roc` then measures attack-type generalization (the §6.5 wall), not
in-(train-carrier-)distribution performance. The registered gap `G = val_roc − test_roc` would therefore
conflate the **carrier** shift with the **attack-type** axis — and since §6.5 showed the attack-type
component collapses with capacity, a confounded `G` would inherit that collapse and read FALSIFIED at
`lora` even if the pure carrier gap persists (a bias toward the wrong verdict). The smoke made this vivid:
attack-type-OOD `val_roc` 0.63 vs held-out-carrier `test_roc` 0.96.

**Fix.** For carrier-LODO folds, carve val as a **label-stratified row-holdout with attack type held fixed**
(force `min_types_for_typeholdout = 10**9` so the carve never holds out types). `val_roc` is then an
in-(train-carrier-)distribution reference (held-out contexts, all attack types), so `G = val_roc −
test_roc` isolates the **carrier** generalization gap. Implementation: `folds.make_fold` sets the carve
knob for `CARRIER_LODO_FOLDS` — one line; no change to the ROC basis or the decision rule.

Motivated by the **code structure** (the carve holds out types), not the smoke's outcome direction; logged
before the registered ≥3-seed × ≥2-rung sweep. (Note: a negative or ~zero `G` is a legitimate outcome — it
would say the carrier "wall" is a representation-geometry phenomenon that does **not** manifest as a
detection gap, the `SMALL-THROUGHOUT`/revise-the-spine branch.)

## Audit disclosures — P1.5 methods-hardening, 2026-06-10 (record-only; verdict unchanged)

**Dated, append-only.** From the full re-audit (`docs/planning/consolidated-audit-2026-06-09.md`);
neither note changes the estimator, thresholds, decision rule, or the ratified SMALL-THROUGHOUT
verdict.

- **W4 — seed-coupling in the CI aggregation (anti-conservative; quantified, no flip).** The
  hand-rolled carrier bootstrap (and the v1.8.0 stratified primitive as-used elsewhere) couples
  bootstrap draws across seeds — one draw indexes all seeds' replicates — which understates CI
  width. Audit quantification with independent per-seed draws: CIs widen **×1.2–1.7**; the carrier
  verdict does not flip (G_lora +0.067 CI-low stays >0 under the widened band). Upstream option
  (a `seed_independent=` draw mode) tracked on eval-toolkit#93 (DF-11) alongside the
  `return_samples`/`frac_gt` re-lock.
- **W10 — the SMALL-THROUGHOUT label is rule-sensitive (disclosure).** Under §6.5's **sign-only**
  rule (CI-low > 0 ⇒ SURVIVES) the carrier residual (G_lora +0.067, CI-low +0.064) would read
  **SURVIVES**; the SMALL-THROUGHOUT label rests on the **pre-registered ½·G(frozen) knob**
  (+0.067 < ½·0.167) — a legitimate pre-locked choice, but prose must say "small under the
  pre-registered ½-knob," never "no wall" or "never large." (The residual table-carrier wall
  +0.205 is the standing Lane-2 target either way.)
