# Cross-family + within-indirect dialect transfer under fair tuning — does end-to-end capacity climb the cross-family OOD wall? PRE-REGISTERED criteria

**Pre-registered:** 2026-06-03, **before any cross-family or within-indirect-dialect split has been
constructed and before any cross-family/dialect detector has been trained in this repo.** Registered by
[ADR-055](../../decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md):68 (the timestamped-dir clause)
and by the second-opinion audit (`../../docs/planning/prototype-comparison-audit-2026-06.md` §A.5 + §E)
as the experiment that would *close* (not just scope) the cross-family gap. This is the cross-family /
dialect-transfer sibling of `../eda/OOD_WALL_PREDICTION/criteria.md` (attack-type) and
`../carrier-lodo/criteria.md` (carrier), and inherits their anti-prototype, write-gated discipline. It is
the full pre-registration promoted from the prior `criteria.DRAFT.md` skeleton; the elevation to **two
axes** (the 4-dialect within-indirect arm) follows the Phase-2 dataset windfall and the A2 program-review
reconciliation (`../../docs/planning/program-review-reconciliation-2026-06-03.md` §B.1).

**Attestation (write-gate).** At the time of writing, **no cross-family or dialect-LODO split has been
constructed and no detector trained** for this study. The decision *logic*, *thresholds*, *estimator*,
and *verdict labels* below are fixed in this dated document. The verdict is computed **only** on a
complete rung sweep, and the rule cannot be revised after any cross-family/indirect datum exists except
per the Revision policy (dated, written, never silent). Finalization therefore cannot cherry-pick the
outcome.

## Why this gate exists (the claim it tests)

The portfolio's headline modeling result is that **fair-tuned capacity dissolves the attack-type wall**
(§6.5 FALSIFIED at the `lora` ceiling, T 0.135 → 0.082 → −0.003 —
`../eda/OOD_WALL_PREDICTION/FINDINGS.md`) and **attenuates the carrier wall** (carrier-LODO
SMALL-THROUGHOUT, G frozen +0.167 → lora +0.067; residual **table** carrier +0.205, n=3 provisional —
`../carrier-lodo/verdict.json`). **Both of those axes are within BIPIA.** The prototype's original wall is
a *different, harder* shift — **cross-family**: train on direct-injection datasets, test on a cross-family
OOD slate. The prototype **claims** a cross-family wall — pooled-OOD AUPRC 0.364 ≤ 0.374 no-skill floor, AUROC 0.515 ≈
chance at its frozen probe, and a *worse* confounded LoRA run (AUPRC 0.293, AUROC 0.383), discarded as a
cross-rung mirage ([ADR-052](../../decisions/ADR-052-attack-type-generalization-study-design.md):17-18;
confounds A–C: frozen pre-head + untuned recipe + no model selection). **We trust none of these prototype
results.** Arm A re-establishes the wall *independently* — rebuilt from our own EDA-gated/deduped
`data/raw/` corpora with our pipeline; the prototype's numbers are cited only as the **claim under
re-test**, never as a trusted anchor or floor. So the **symmetric question is untested on trustworthy
footing**: does *fair-tuned capacity* climb the cross-family wall the way it climbed the attack-type wall?

The Phase-2 dataset expansion sharpened the question into **two axes**. The cross-dataset EDA established
that **BIPIA is only one indirect *dialect*** (E7: within-indirect PAD 1.92–1.98 ≈ indirect↔direct;
silhouette 0.095 — `../eda/CROSS_DATASET/`), and Phase-2 added **two more indirect carrier dialects**
(browsesafe = HTML, fujitsu B1 = RAG-document; PAD-vs-BIPIA 1.94–1.99, mutually distinct). A cross-family
OOD test must therefore hold out **multiple** indirect corpora, not BIPIA alone
(`dataset-strategy-rethink-and-acquisition` memory; A2 §B.1). This gate measures both the
**direct→indirect** gap (the prototype's wall) and the **within-indirect dialect-transfer** gap (the new
leave-one-out), under fair per-rung tuning, across the capacity ladder.

## Question

Holding the method fixed (the rung ladder tfidf → frozen → lora) under **fair per-rung tuning**
([ADR-052](../../decisions/ADR-052-attack-type-generalization-study-design.md): per-rung tuning on a
train-internal val split, model selection, no frozen-pre-head confound):

- **Arm A (direct→indirect cross-family).** Train on direct-injection datasets, test on the cross-family
  OOD slate. Does the transfer gap **collapse toward zero at `lora`** (→ capacity climbs the cross-family
  wall too; both repositories unify and "capacity-dependent" generalizes), or **persist as capacity rises**
  (→ cross-family is a real, capacity-resistant standing wall; the within-BIPIA headline does **not**
  generalize)?
- **Arm B (within-indirect dialect transfer).** Train on K−1 indirect dialects + the direct base, test on
  the held-out indirect dialect (rotated). Does the **dialect-transfer gap** collapse at `lora`, or persist?

## Hypothesis (load-bearing, pre-committed)

**H_crossfamily (primary, Arm A):** the cross-family gap is **capacity-resistant** — it does **not**
collapse to ≈0 at the `lora` rung (contrast the attack-type axis, where it did). Directional, one-sided.

**H_dialect (primary, Arm B):** the within-indirect dialect-transfer gap is **smaller than Arm A's
direct→indirect gap but non-zero**, and is **at least partially attenuated by capacity** (consistent with
the carrier-LODO SMALL-THROUGHOUT pattern, which is the within-BIPIA carrier analogue). Directional,
one-sided.

The interesting outcome is genuinely either way on each arm, and **all outcomes are publishable**: a gap
that **collapses** unifies the repos and generalizes the capacity-dependent story; one that **persists**
identifies the real standing wall and honestly bounds the within-BIPIA headline to its corpus.

## Design (FIXED)

### Arm A — direct→indirect cross-family (the prototype's wall, fair-tuned)

- **Slate (the prototype's dataset *set*, rebuilt by us — not its artifacts).** **Train:** deepset /
  Gandalf / Mosscap / HackAPrompt (direct injection). **Test:** BIPIA / InjecAgent / JBB / XSTest /
  NotInject (cross-family OOD; n=5 test slices). Source-disjoint by construction. **All 9 corpora are
  built from our audited `data/raw/` with our own dedup/leakage discipline — we do NOT consume the
  prototype's processed folds or configs** (per "trust no prototype result"). All 9 verified present in
  `data/raw/` (BIPIA = the M1-core dir; Gandalf has two variants `gandalf_ignore` + `gandalf_summ` — the
  variant(s) used logged at build). Any substitution (availability/license) is logged with rationale; the
  prototype repo is a historical reference only.

### Arm B — within-indirect leave-one-dialect-out (the Phase-2 elevation)

- **Dialects (4, mutually distinct; PAD-vs-BIPIA 1.94–1.99):** **BIPIA** (email/code/table carriers
  pooled = the dialect) · **browsesafe** (HTML) · **fujitsu B1** (RAG-document) · **InjecAgent**
  (tool-output). WAInjectBench is **excluded** (unlicensed, eda-only). Each fold holds out one dialect;
  the test is the held-out dialect. **Run BOTH training compositions and report the contrast:**
  **(B+)** `train = (the other 3 indirect dialects) ∪ (the direct base pool from Arm A)` —
  deployment-realistic (the detector has seen direct + most indirect injection); and **(B−)**
  `train = (the other 3 indirect dialects) only` — the purer indirect→indirect transfer. The
  **(B+) − (B−) contrast** measures how much direct-injection data buys indirect-dialect transfer; both
  isolate the *dialect*-transfer gap on the held-out dialect.
- **Dialect units (load-shape, FIXED):**
  - **browsesafe** — per-page; `content` = full HTML (p50 46 KB, p95 140 KB), so **head+tail truncation**
    (~6 K head + 2 K tail tokens; Sun et al. 2019 — injections cluster at page top/bottom); label
    {`no`→0, `yes`→1} (7422 neg / 7297 pos). Chunked windowing is a future rigor upgrade, stated as a ceiling.
  - **fujitsu B1** — per-document; `poison_content`=1 / `benign_content`=0 (balanced 10,943 / 10,943);
    **exclude** the augmented configs (leak) and **skip** the B2 image modality.
  - **InjecAgent** — static (`text`, `attack_type`) tool-output rows (the Phase-2 audit confirmed
    InjecAgent ships a static text slate, not execution-only).
  - **BIPIA** — the M1 core (payload × context × attack-type); email/code/table carriers pooled into the
    single "BIPIA dialect" (the within-BIPIA carrier split is the *separate* carrier-LODO axis).

### Shared (both arms)

- **Rung ladder = tfidf + frozen (local, free) + lora (RunPod) — ALL THREE on BOTH arms**, under **fair
  per-rung tuning** (ADR-052). This is the whole point: the prototype's cross-family LoRA was confounded
  (frozen pre-head + untuned recipe + no model selection); the fair re-run removes those on **both** arms.
- **Per-rung fair tuning (locked grid; mirrors M1 / carrier-LODO):** reuse the **M1 LoRA recipe + grid**;
  **≥3 seeds** on the trainable (`lora`) rung; **model-selection on val ROC-AUC**; per-rung tuning on a
  train-internal val split (ADR-052). The grid is **fixed here and reported in full** in the verdict
  (no silent grid — fair per-rung tuning IS this study's only claim to novelty over the prototype).
- **Val reference = in-(train-)distribution** (mirrors carrier-LODO `criteria.md` **Rev 2**, the confound
  fix). Val is carved from the **train pool** (Arm A: the direct train-family; Arm B: each variant's own
  train pool — B+ = K−1 indirect + direct base, B− = K−1 indirect only) via the existing
  `carve_val_from_train`, with the attack-type mini-LODO **disabled**
  (`min_types_for_typeholdout = 10**9`) so the carve is a **label-stratified row-holdout with attack type
  held fixed** — never a type-holdout. `val_roc` is then in-(train-)distribution, so `Gx = val_roc −
  test_roc` isolates the **cross-family / dialect** shift and does **not** inherit the §6.5 attack-type
  collapse (the bias-toward-FALSIFIED that Rev 2 fixed for the carrier axis).
- **Fold construction (B2; mirrors `folds.py`):** a dialect-LODO axis built like
  `folds.py::_carrier_lodo_builder` (`folds.py:125`) — `DIALECT_LODO_FOLDS` + a per-fold builder; the only
  held-out axis is the **dialect/family**, asserted by a new `assert_dialect_disjoint` (sibling of
  `assert_carrier_disjoint`, `folds.py:232`); `make_fold` (`folds.py:320`) sets the Rev-2 carve knob for
  dialect folds exactly as it does for `CARRIER_LODO_FOLDS` (`folds.py:352`). No carrier/dialect leakage;
  cross-corpus context overlap is nil by construction and still asserted.

## Statistics + decision rule (BOTH statistics; logic FIXED, on the ROC-AUC basis)

Report **two** statistics — one for comparability, one as the pre-registered decision gate — per arm.

1. **Comparability anchor (descriptive — NOT the gate).** **Our own** frozen-rung pooled-OOD **AUPRC vs
   the no-skill floor** + **AUROC** (prevalence-invariant) is the anchor. The prototype's claimed numbers
   (0.364 / 0.374 floor / 0.515) are reported alongside **only as the claim under re-test** — does our
   independent frozen rung reproduce, beat, or refute them, and does any fair-tuned rung clear *our own*
   floor? AUPRC is prevalence-inflated at the slate's prevalence, so it is the comparability anchor only,
   never the gate (the reporting-discipline fix).

2. **Cross-rung transfer-gap (the pre-registered DECISION statistic), metric basis ROC-AUC**
   (prevalence-invariant; consistent with carrier-LODO Rev 1 and the per-carrier-prevalence lesson):

   `Gx(rung) = in-distribution-val ROC-AUC − held-out-test ROC-AUC`, computed **per arm**.

   - **SURVIVES** iff `Gx(lora) > 0` with one-sided 95 % bootstrap CI-low **> 0** **AND** `Gx(lora)` does
     **not** collapse relative to frozen: `Gx(lora) ≥ ½ · Gx(frozen)` **AND** `Gx(lora) ≥ 0.05` absolute
     ROC-AUC (a pre-specified **SESOI floor** — a gap below 0.05 is not a wall worth claiming; Lakens 2017
     equivalence-testing rationale, a formal TOST left out as underpowered at n=4/5). Both are the
     pre-registered free knobs, fixed here **before any datum** (the ½-fraction is identical to §6.5 +
     carrier-LODO; the 0.05 SESOI floor is added on this axis). **The bare-`½·Gx(frozen)` verdict is ALSO
     reported** for direct cross-axis comparability to the attack-type + carrier axes.
   - **FALSIFIED** iff `Gx(lora)` CI-low **≤ 0** (the gap is statistically indistinguishable from dissolved
     at the ceiling — capacity climbs the wall, the `lora` attack-type pattern T = −0.003).
   - else **SMALL-THROUGHOUT** (the carrier-axis pattern — the wall was overstated by the geometry / cheap
     rungs and never large).

   **Resampling unit (per-dialect / per-slice natural cluster).** For each held-out unit, the CI on
   `Gx(rung, unit)` comes from a **natural-cluster bootstrap within that held-out unit** — resample the
   unit's deployment-realistic cluster with replacement, recompute `test_roc`, hold `val_roc` fixed;
   ≥ **10 000** iters; one-sided 95 % percentile CI. The cluster per unit:
   - **BIPIA** → payload-id (~70 payloads = ~5 strings × 14 attack-types; as carrier-LODO Rev 1).
   - **browsesafe** → page/row-id.
   - **fujitsu B1** → document-id.
   - **InjecAgent** → tool-output / attack-id.
   - **Arm A** → the **test-dataset slice** (n=5; resample slices' within-slice cluster, analogous).

   **Aggregate (deliberately NOT a cross-fold cluster bootstrap — known-bad at n=4/5).** The robust
   aggregate `Gx(rung)` = **mean over the held-out units**, reported **with its per-unit spread**; the
   per-unit CIs come from the within-unit bootstrap above, and a **per-fold permutation test** (label
   permutation within the held-out unit; presence-of-effect, robust at few clusters — mirrors §6.5 perm p)
   accompanies each. **The lead result is the per-dialect (Arm B) / per-slice (Arm A) × per-rung table**,
   not the aggregate — a catastrophic single-dialect wall must not be masked by a benign mean.

   - **Write-gated:** verdict computed only on a complete rung sweep; rule fixed before any LoRA datum.
   - **Verdict labelled directional / low-power** (n=4 dialects, n=5 slices — the read is directional, as
     on the n=3 carrier axis).

## E8 — off-the-shelf detector reference column (deployed-baseline contrast; non-gating)

Score frozen, open-weights, locally-runnable detectors on the held-out dialects / slices as a
**deployed-baseline contrast** (non-gating, like the M1 reference column). Tests: *do deployed guards
generalize to HTML / RAG indirect carriers, or are they blind there too?* (Likely blind — ProtectAI on
BIPIA already shows mean-attack 0.259 < mean-benign 0.262, AUROC 0.44 — scope-blind to indirect.)

- **Detector set (the 3 already wired in `../attack-type-lodo/reference_scorers.py`):**
  ProtectAI-v2 (`protectai/deberta-v3-base-prompt-injection-v2`) · Prompt-Guard-2-86M
  (`meta-llama/Llama-Prompt-Guard-2-86M`) · Prompt-Guard-1-86M (`meta-llama/Prompt-Guard-86M`, gated but
  granted). Reuse `reference_scorers.py:score_texts(texts, model_id)` (`reference_scorers.py:74`).
- **Discipline:** frozen, inference-only, CPU-runnable, **skip-gracefully** on any gate; **local + free**
  (runs independent of the paid `lora` rung). **EXCLUDE** commercial / vendor-hosted guards
  (Lakera/Azure/AWS/NVIDIA/Google/Cisco — can't run ourselves) and heavy LLM-judges (need a big LLM).
- **Report AUROC + per-class means** per dialect (the audit discipline — blind accuracy hides the
  indirect-blindness). Sourced from the detector-landscape atlas (`../../docs/research/detector-landscape/`,
  67 entries), which the program review references only via these three.

## Honest limitations (pre-committed)

- **The confound fix is the contribution.** The prototype's cross-family LoRA was confounded (A–C); this
  re-run's only novelty is *fair per-rung tuning* — so the tuning protocol is locked and reported in full.
- **No prototype artifact is trusted.** Arm A is an *independent* re-build from our audited `data/raw/`
  (not the prototype's processed folds/configs); the prototype's published numbers are the claim under
  re-test, cited never as a floor. This removes any dependence on the prototype's (audited-as-confounded)
  pipeline, at the cost that exact numeric comparability to the prototype is approximate by construction.
- **n=5 test slices (Arm A) / n=4 dialects (Arm B)** ⇒ the aggregate is low-power; the read is
  **directional** (labelled as such, like the n=3 carrier axis). The per-unit table + within-unit
  bootstrap + permutation test carry the evidence, not a cross-fold aggregate.
- **Corpus-OOD confound (E5).** Arm B is reported as leave-one-indirect-**corpus**-out: a held-out corpus
  bundles **carrier + source + writing-style + label provenance**, not carrier alone. This is
  deployment-realistic (a new corpus *is* a bundle), but it means Arm B measures *corpus* transfer, not a
  decomposed carrier effect. The discussion cross-references the within-BIPIA **carrier-LODO** (residual
  table carrier +0.205) for carrier-vs-source attribution. Pre-committed as a stated limitation.
- **Prevalence varies across slices/dialects** ⇒ ROC-AUC is the gate metric; AUPRC-vs-floor is the
  comparability anchor only (the same prevalence lesson that moved the carrier axis off AUPRC in Rev 1).
- **Separability ≠ collapse** (arXiv:2602.14161): the dialects being geometrically distinct (PAD 1.94–1.99)
  does **not** by itself prove a *detection* gap — that is exactly what this gate measures rather than
  assumes.
- **browsesafe truncation** (head+tail) may miss a mid-document injection; chunked windowing is the future
  rigor upgrade, stated as a ceiling.

## Revision policy

Mirrors `../eda/OOD_WALL_PREDICTION/criteria.md` and `../carrier-lodo/criteria.md`: any change to the
question, hypothesis, design, estimator, or decision rule after this timestamp requires a **written, dated
rationale appended below** (never a silent edit). The implementation-finalization (the exact `data/raw/`
corpus dirs + the Gandalf variant used, the per-rung grid as logged from the M1 recipe, the per-unit row
counts read from the loaders) is the expected first dated Revision (B2, before the run) and **must not
change the collapse-vs-persistence logic, the ROC-AUC basis, the SURVIVES thresholds (½·Gx(frozen) AND the
0.05 SESOI floor), or the verdict labels.**

## Verification (deferred — cheap rungs first, then a separate present-first paid go)

1. **B2 (local, free):** build the dialect-LODO harness (the `folds.py` mirror above), run **tfidf +
   frozen** on both arms + the **E8** reference column; emit the per-unit × per-rung ROC-AUC table + the
   within-unit bootstrap CIs + permutation p. Directional read on whether capacity *starts* to climb.
2. **B3 (paid, separate present-first go):** the `lora` rung, both arms (Arm B **both-ways**, B+ and B−),
   ≥3 seeds — ~27 training runs on pools larger than carrier-LODO. **Hard cap ~$6** (base-budget;
   contingency untouched); the real cost estimate is computed at B2 and **reconciled at this present-first
   go** (raise cap or trim) before launch.
3. **B4:** apply the FIXED logic to the complete rung sweep → record **SURVIVES** (cross-family /
   dialect capacity-resistant — within-BIPIA headline bounded) / **FALSIFIED** (dissolved at `lora` —
   repos unify, story generalizes) / **SMALL-THROUGHOUT**, **per arm**, with the per-unit table and the
   E8 deployed-baseline (likely-blind) contrast. No knob is revisited except per the Revision policy.

A **separate present-first ADR action** (sibling of the carrier amendment) then promotes Lane 6 to active
and adds the "indirect-dialect / corpus-level carrier generalization" axis to the ADR-055 spine — drafted
**from** the result, not pre-committed beyond the directional hypotheses above (E7).
