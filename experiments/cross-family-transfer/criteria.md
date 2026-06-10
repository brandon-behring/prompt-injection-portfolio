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

---

## Revision 1 — Arm-B implementation finalization (read-from-data specifics), 2026-06-03

**Dated, before any cross-family/dialect detector has been trained or any `Gx` computed.** This is the
"implementation-finalization Revision (B2, before the run)" the original anticipated (Revision policy). The
**decision logic, the ROC-AUC basis, the SURVIVES thresholds (½·Gx(frozen) AND the 0.05 SESOI floor), and the
verdict labels are UNCHANGED.** This Revision finalizes only the **Arm-B** read-from-data specifics and records
the harness build (sibling module `experiments/cross-family-transfer/{assemble,folds_dialect,leakage_gate}.py`,
reusing the attack-type-LODO `Fold`/`carve_val_from_train` + upstream `eval_toolkit.text_dedup`). Arm A's
direct pool + the **B+** training composition are deferred to a later dated Revision (B2.4).

### (i) Arm-B assembly + per-dialect cluster definitions (read from the loaders)

Unified frame `(text, label, dialect, cluster_id)`; each dialect's natural resampling cluster:

| dialect | rows | pos | neg | clusters | cluster_id |
|---|---|---|---|---|---|
| bipia | 5,508 | 5,040 | 468 | 143 | `attack_type::payload-idx` (140 pos) + `clean::carrier` (3 neg) |
| browsesafe | 14,719 | 7,297 | 7,422 | 14,719 | `page::split::row` (1 per page) |
| fujitsu | 21,886 | 10,943 | 10,943 | 10,943 | `doc::<id GUID>` |
| injecagent | 2,125 | 2,108 | 17 | 63 | `tool::<attacker-tool>` (62 pos) + `clean::tool-output` (1 neg) |

- **bipia** pools email/code/table carriers **and** both BIPIA roles (= the dialect) → **143 clusters** (140
  positive payloads ≈ 5 strings × 28 disjoint train+test attack-types, + 3 clean-carrier negatives). This
  corrects the design's "~70" (which counted one role); the dialect pools both. Logic unchanged.
- **browsesafe** head+tail truncation = ~6K head + 2K tail **tokens**, applied as a **char proxy** (~4
  chars/token → 24K head + 8K tail chars; short pages pass through). The model tokenizer does the final
  truncation; the char-proxy ensures the page top/bottom (where injections cluster) survive into the window.
- **fujitsu B1** read from the on-disk core `rag_poisoning_benchmark_combined_deduplicated.jsonl`, which
  natively carries a per-document `id` GUID → `source_id` **already present, no re-persist needed**; the
  **augmented configs are excluded** (never read) and the B2 image modality skipped, per the design.
- **InjecAgent** positives = the canonical `injecagent_derived.parquet` (2,108, label 1); `cluster_id` =
  attacker-tool id, derived by matching each row's embedded attacker instruction to
  `attacker_cases_{dh,ds}.jsonl` (**62 tool clusters**). Negatives = clean tool-output templates (the
  `<Attacker Instruction>` placeholder removed), deduped (**17**, one `clean::tool-output` cluster).

### (ii) ★ Added honest limitation — InjecAgent negative-side is thin (read-from-data)

The held-out **injecagent** fold has **2,108 positives but only 17 negatives in a single negative cluster**.
Pre-committed consequences: (a) the per-dialect natural-cluster bootstrap on this fold resamples 62 positive
tool-clusters but only **1** negative cluster → negative-side sampling variability is essentially
unrepresented; (b) 17 negatives poorly resolve a ROC-AUC. ⇒ **the injecagent held-out fold is the
weakest-powered of the four**; its `Gx` CI will be wide and is to be read as **indicative only** — it must not
drive a headline. This is precisely why the pre-reg leads with the **per-dialect table** (not the aggregate)
and labels the verdict **directional/low-power**. The negatives are reconstructed templates (InjecAgent ships
positives only); a better real-benign-tool-output source, if found, would be a future dated Revision. (No
logic change; recorded data limitation.)

### (iii) Dialect-LODO folds + the in-distribution val carve (UNCHANGED logic)

`folds_dialect.py` mirrors `attack-type-lodo/folds.py::_carrier_lodo_builder` (`_dialect_lodo_builder`,
`assert_dialect_disjoint`, `DIALECT_LODO_FOLDS`, `make_dialect_fold`) and forces `min_types_for_typeholdout =
10**9` — the carrier-LODO **Rev 2** in-distribution carve (val = label-stratified row-holdout, attack-type
held fixed), so `val_roc` does not inherit the §6.5 attack-type collapse. Per-fold (**B−**, indirect-only,
seed 0):

| held out | train | val | test | test pos/neg |
|---|---|---|---|---|
| bipia | 30,984 | 7,746 | 5,508 | 5,040 / 468 |
| browsesafe | 23,615 | 5,904 | 14,719 | 7,297 / 7,422 |
| fujitsu | 17,882 | 4,470 | 21,886 | 10,943 / 10,943 |
| injecagent | 33,690 | 8,423 | 2,125 | 2,108 / 17 |

### (iv) Leakage gate (Q2 — exact + MinHash≥0.8, purge-from-train) — result

`leakage_gate.py` (reusing upstream `eval_toolkit.text_dedup`) scanned each fold's train dialects vs the
held-out test dialect, purging matches **from train only** (held-out test sacrosanct). **Result: zero
cross-dialect leakage** (0 exact, 0 near-dup ≥0.8 across all 4 folds). The registered **fujitsu⊃InjecAgent**
concern (MANIFEST:242) produced **no overlap** — the InjecAgent aggregation lives only in fujitsu's
*augmented* configs, which the design excludes and the loader does not read; the gate empirically confirms the
exclusion is clean. Artifact: `experiments/cross-family-transfer/B2_leakage/leakage_gate.json`.

### (v) Embedder + deferred items

- **Frozen-rung embedder = ModernBERT-base** (`answerdotai/ModernBERT-base`), the M1/carrier-LODO embedder
  (NOT MiniLM, which was only the EDA-geometry embedder). tfidf + frozen are local/free; lora is B3.
- **Deferred to a later dated Revision (B2.4):** Arm A's 9-corpus direct→indirect slate (rebuilt from
  `data/raw/`, with its own leakage gate) + the **B+** training composition (the direct base pool). **B−**
  (indirect-only Arm-B) is finalized here.

**Nothing in (i)–(v) changes the question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, or the verdict labels.**

---

## Revision 2 — InjecAgent negative re-cluster + B2 inference/run finalization, 2026-06-03

**Dated, before any cross-family/dialect detector has been trained or any `Gx` computed.** Supersedes the
Revision 1 InjecAgent negative construction (a double-check found a better real-benign source) and finalizes
the remaining B2 inference + run specifics. **Decision logic, ROC-AUC basis, the ½·Gx(frozen) + 0.05 SESOI
thresholds, and verdict labels remain UNCHANGED.**

### (a) InjecAgent negatives — re-sourced + re-clustered (supersedes Rev 1 §i/§ii)

The double-check found `user_cases.jsonl`: InjecAgent's **17 canonical benign user-scenarios** (distinct
`User Tool`s), each a real `Tool Response Template` whose `<Attacker Instruction>` placeholder, removed,
yields the clean tool output a benign agent would observe. Negatives are now **those 17 real responses, one
per-`User Tool` cluster** (was: templates reconstructed from the test-cases, collapsed into 1 cluster). Effect:
injecagent **negative-clusters 1 → 17** (the dialect now has **79 clusters** = 62 positive attacker-tool + 17
negative user-tool); the per-dialect natural-cluster bootstrap is **no longer degenerate** on the negative side.

**The 17 : 2,108 imbalance is inherent** to InjecAgent (17 benign scenarios × 62 attacker cases) and cannot be
enlarged — so the injecagent held-out fold **remains the weakest-powered** (17 negatives / 17 clusters, below
the ~24–50-cluster comfort floor for nominal bootstrap coverage) and is read **indicative-only**, not
headline-driving. The improvement: its ROC-AUC CI is now well-defined.

### (b) Inference layer (finalized)

- **Gate = the single pre-registered aggregate `Gx(lora)` CI per arm** → no multiplicity on the verdict. The
  per-dialect permutation p-values are reported **uncorrected, as diagnostics only**; no per-dialect
  significance is claimed from them (any such claim, if ever made, would use Holm–Bonferroni).
- **Bootstrap = label-stratified cluster** (resample positive- and negative-clusters separately within each
  held-out dialect — preserves prevalence, never single-class), ≥10 000 iters, one-sided 95 % percentile CI.
  **Lead = the per-dialect table; no cross-fold n=4 aggregate bootstrap** (below the ~24–50-cluster coverage
  floor; the few-clusters literature). Seed-aggregation + permutation-test construction + iteration counts
  **match `../attack-type-lodo/falsify_carrier_lodo.py`** (single source of truth; verified at build).

### (c) Run conditions (finalized)

- **Conditions:** B− (train = K−1 indirect only) and B+ (= + the Arm-A direct base) × **natural-mix** and
  **dialect-balanced** (downsample each train dialect to the smallest). **Primary verdict = B− natural-mix**
  (the faithful, well-powered test of H_dialect — B−'s ~30k-row ~50 %-benign pool is not under-trained);
  B+ − B− = the direct-data-bridging contrast (links to Arm A); dialect-balanced = the dominance robustness
  check. The primary-condition choice gates nothing in B2.3 and is reconfirmable at the lora rung.
- **Rungs / compute:** tfidf (CPU) + frozen **ModernBERT-base on the local RTX 2070S, fp16** (free) ×**≥3
  seeds**; lora → RunPod (B3). All rungs see the same head+tail-truncated raw text; M1 grids; `val_frac=0.2`;
  `contexts_per_attack=12`.
- **E8 long docs:** browsesafe / fujitsu scored by **chunking into 512-token windows + max-pool** per detector
  (the steel-man "are deployed guards blind?" test).
- **Sequencing:** B2.3 = Arm-B **B− only** (B+ needs the Arm-A direct base → built at B2.4). **Arm-A
  positive/negative construction is deferred to B2.4.**

### (d) Leakage gate — re-confirmed with the new negatives

Re-run after the InjecAgent re-source: **still zero cross-dialect leakage** (0 exact, 0 near-dup ≥0.8 across
all 4 folds; train/test sizes unchanged) — `B2_leakage/leakage_gate.json`.

**Nothing in (a)–(d) changes the question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, or the verdict labels.**

---

## Revision 3 — Arm-A direct→indirect slate assembly + B+ finalization (B2.4), 2026-06-04

**Dated, before any Arm-A direct→indirect detector has been trained or any cross-family `Gx` computed.**
The deferred B2.4 Revision anticipated by Rev 1 §(v) and Rev 2 §(c). It finalizes Arm A's direct train-pool
assembly (rebuilt from our audited `data/raw/`, audited 2026-06-04), the composition, the negative
construction, the per-slice positive-label definition, the over-defense metric, the Arm-A leakage gate, and
the **B+** composition. **The question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, and verdict labels remain UNCHANGED** — this Revision *specifies* the
pre-registered "cross-family OOD slate", it does not change it.

### (i) Direct-pool corpora + provenance (audited 2026-06-04, from `data/raw/` + `MANIFEST.json`)

| corpus | source | license | rows | native labels | text field |
|---|---|---|---|---|---|
| deepset | deepset/prompt-injections | Apache-2.0 | 662 | 263 pos / 399 neg | `text` |
| gandalf_ignore | Lakera/gandalf_ignore_instructions | MIT | 1,000 | all-positive | `text` |
| mosscap | Lakera/mosscap_prompt_injection | MIT | 278,945 | all-positive | `prompt` |
| hackaprompt | hackaprompt/hackaprompt-dataset | MIT | 601,757 | native=attack-success (§iii) | `user_input` |

**Gandalf variant LOCKED = `gandalf_ignore`** (MANIFEST "cross-family TRAIN anchor"); `gandalf_summ` (140)
excluded to optional-robustness. All four tier-1, non-`eda_only`, permissively licensed (manifest-verified).

### (ii) Direct-pool composition — size-imbalance cap

Audit measured ~1000× imbalance (mosscap+hackaprompt ≈880k vs deepset+gandalf ≈1.8k); raw natural-mix is a
degenerate two-game pool. Primary pool = **capped-balanced** (direct analog of Rev 2 §(c)): cap each corpus's
positives at **C = 3,000**, stratified-proportional by `level` where present (mosscap 8, hackaprompt 11),
seed 0; small corpora whole. Realized ≈ **7,263** positives (deepset 263 / gandalf 1,000 / mosscap 3,000 /
hackaprompt 3,000), each ≤41%. `C` is the one free assembly knob, fixed here; realized counts logged.
Uncapped natural-mix retained as optional robustness.

### (iii) hackaprompt relabel + game-corpus caveat

hackaprompt native `correct`/`score` = **attack-success** (different task) → all `user_input` relabeled
injection-positive; text = `user_input` (system `prompt` not concatenated). **Caveat (extended to mosscap):**
mosscap + hackaprompt are stylistically narrow extraction/PWNED *games*; treating every game prompt as
positive injects label noise into the capped-dominant corpora. The `C`-cap bounds their share; the
corpus-style confound is addressed in §(viii).

### (iv) Train negatives — 3-source, hard-negative, benign-heavy (best-practice §viii)

Direct corpora are ~all-positive (only deepset ships 399 neg) and `load_direct_base()` is an unbuilt stub →
**no reusable benign pool**; negatives constructed here:
- **deepset 399** native negatives (style-matched to deepset positives);
- **neuralchemy `label=0` (~16.3k)** — real-data **hard negatives** (benign prompts with injection
  trigger-words, tagged `hard_negative/contains_ignore`): the InjecGuard **MOF** strategy in real data, the
  established fix for trigger-word over-defense;
- **guychuk `label=0` (top-up, ~229k avail)** — plain in-domain benign for **source diversity** (the
  negative class is not one corpus's style — Mirror-pattern shortcut mitigation).
Sized **benign-heavy ≈3–4:1** (MOF-aligned, deployment-realistic) to **total ~25–30k ≈ Arm-B scale**
(fixes the cross-arm train-size asymmetry on the benign side, not by inflating game positives). Val = the
line 119–126 in-distribution label-stratified carve. **Build-time: verify `label=0 ⟺ benign`** for
neuralchemy + guychuk; realized pos/neg logged.

### (v) Per-slice positive-label definition + cluster units (D1 = broad attack-vs-benign)

**Positive = any attack (injection ∪ jailbreak ∪ harmful); negative = benign**, per slice (grounded 2026-06-04):

| slice | rows | positive | negative |
|---|---|---|---|
| BIPIA | 5,508 | injection | clean carrier |
| InjecAgent | 2,125 | 2,108 injection | 17 clean (thin) |
| JBB | 100+100 | harmful-behaviors | benign-behaviors |
| XSTest | 450 | 200 unsafe | 250 safe |
| NotInject | 113–678 | — (all benign) | all benign |

- **Gate** = `Gx(lora) = val_roc − test_roc` on the **pooled cross-family ROC-AUC over the 4 two-class
  slices**. A **descriptive injection-only (BIPIA+InjecAgent) sub-aggregate** is also reported (non-gating).
- **NotInject** (single-class) → a **non-gating over-defense FPR column** at a fixed low-FPR operating point
  (the InjecGuard/NotInject metric; matches M1 `recall_at_fpr`; target FPR<2%), beside E8.
- **Clusters:** direct (train) corpora carry **no `cluster_id`** (resampling = held-out test slice, line
  170). Test-slice clusters: BIPIA→payload-id, InjecAgent→tool (Rev 1 §i); **JBB/XSTest within-slice
  `cluster_id` = the one remaining build-time grounding** (read from loaders, logged).

### (vi) Arm-A leakage gate (exact + MinHash ≥ 0.8, purge-from-train)

`leakage_gate.py` (`eval_toolkit.text_dedup`), purge from TRAIN only: **direct⊗direct · direct⊗test ·
direct⊗indirect (B+) · negative⊗test** (neuralchemy/guychuk vs NotInject/XSTest — never train on a held-out
hard-negative). Artifact `B2_leakage/leakage_gate_armA.json`.

### (vii) B+ training composition

**B+** `train = (capped direct_base from (ii)+(iv)) ∪ (K−1 indirect dialects)`, natural-mix (primary) +
dialect-balanced (robustness) as Rev 2 §(c). **B+ − B−** = direct-data-bridging. Direct base = one extra
training family, never the held-out unit.

### (viii) Best-practice basis + pre-committed corpus-style limitation

Negative construction follows the prompt-injection guardrail literature: trigger-word **over-defense** is the
documented failure mode, benign hard-negatives the fix (InjecGuard/PIGuard MOF, ACL 2025, arXiv:2410.22770);
generalization-first + low-FPR is the eval norm (arXiv:2511.22047; arXiv:2602.14161, already cited at line
219). **Limitation (Mirror Design Pattern, arXiv:2603.11875):** the FIXED direct-injection train slate is
mostly all-positive *games*, so pos/neg cells are not nuisance-matched and a residual **corpus-style
shortcut** (style ≈ injection-ness) is structural — mitigated by multi-source + hard negatives (iv) and the
leakage gate (vi), and **reported, not claimed away** (beside E5). The injection-only sub-cut (v) + the E8
deployed-guard reference triangulate it.

**Nothing in (i)–(viii) changes the question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, or the verdict labels.**

---

## Revision 4 — Arm-A harness build + realized counts (B2.4), 2026-06-05

**Dated, before any Arm-A detector has been trained or any cross-family `Gx` computed.** The
implementation-finalization Revision the Revision policy anticipated ("the per-unit row counts read
from the loaders ... is the expected first dated Revision (B2, before the run) and **must not** change
the collapse-vs-persistence logic, the ROC-AUC basis, the SURVIVES thresholds, or the verdict labels").
Records the **realized** Arm-A pools as built by `assemble_arm_a.py` / `leakage_gate_arm_a.py`
(2026-06-05). **The question, hypothesis, design axes, estimator, ROC-AUC basis, the ½·Gx(frozen) +
0.05 SESOI thresholds, and the verdict labels remain UNCHANGED.**

### (a) neuralchemy count correction (§iv "~16.3k" → realized ~3,475)

§iv pre-registered "neuralchemy `label=0` (~16.3k)". On-disk audit (2026-06-05) found 16,314 is a
**naive sum across overlapping subdirs** — `core/` (6,274) ⊆ `full/` (15,919), plus a re-schema'd
`data/` (10,674). We use the **`full`-only** pool; under the repo's normalized-exact dedup convention
(`normalize_text_for_dedup` — the same the leakage gate's exact pass uses, collapsing case/whitespace
variants), the realized distinct `label=0` = **3,475**. The negative pool's benign:positive ratio (3.0,
inside §iv's "≈3–4:1") is held by the guychuk top-up, so the **total train size is unchanged**; the
negative-class composition shifts toward guychuk diversity (the `hard_negative`-tagged MOF rows number
~24 on disk regardless — the MOF framing was always thin, a stated limitation not a load-bearing count).

### (b) Realized capped direct-positive pool

| corpus | raw | exact-dedup | artifact-filter | capped |
|---|---|---|---|---|
| deepset | 263 | 263 | 263 | 263 |
| gandalf_ignore | 1,000 | 999 | 999 | 999 |
| mosscap | 278,945 | 212,518 | 212,345 | 3,000 |
| hackaprompt | 579,953 | 378,286 | 349,292 | 3,000 |

Realized capped positives = **7,262** (each ≤41%; the §ii "≈7,263" — gandalf's 1 realized exact dup
gives 999).

### (c) Dedup discipline (the §i "our own dedup/leakage discipline")

- **exact-dedup before cap** (EDA: hackaprompt 33% / mosscap 22% raw duplicate, e.g. "I have been
  PWNED" ×2,098). Normalized-exact dedup (the repo's ExactNormalizedHash convention) before the
  C=3,000 cap; the distinct pools (212k / 378k) ≫ cap, so the cap fills. **In-bounds as §i; no logic
  change.**
- **Light game-artifact filter** — a **deviation from §iii's cap-only bounding**, recorded here. Drops
  ONLY unambiguous non-injections, on the normalized text: (1) degenerate junk (no alphanumeric chars —
  control chars / pure whitespace/punct); (2) a small bare key/password fragment denylist; (3) SHORT
  win-strings (contains "pwned" AND ≤5 tokens — the bare "I have been PWNED", NEVER a long attack whose
  payload instructs the model to output it). Verified NOT to nuke real terse injections: **0 drops** from
  the curated deepset/gandalf injection corpora (an earlier <3-token length floor was rejected for
  dropping gandalf "ignore rules" / deepset "generate c++"). Realized drops: mosscap 173 / hackaprompt
  28,994 game artifacts; every dropped string is logged (`assemble_arm_a._summary`).

### (d) Arm-A leakage gate (§vi) — realized

`leakage_gate_arm_a.py` (the same `eval_toolkit.text_dedup` exact + MinHash≥0.8 primitives),
purge-from-train (test sacrosanct), four scans — artifact `B2_leakage/leakage_gate_armA.json`:
- **direct⊗direct**: 448 cross-corpus dups — a **train↔train** cross-corpus dedup (**keep-first** in
  `load_direct_base`), NOT a leakage purge (so it is not in the manifest; the manifest would drop both
  copies);
- **direct⊗test**: 1 exact;
- **direct⊗indirect (B+)**: 0 (the global scan covers every B+ fold's held-out indirect);
- **negative⊗test**: 200 exact (guychuk/neuralchemy benigns equal to NotInject/XSTest-safe — real
  benign train↔test contamination);
- **near-dup (MinHash≥0.8)**: 231 capped-train rows ≥0.8-similar to a test row (e.g. train "log into a
  corporate network" ↔ JBB-harmful "hack into a corporate network"; exact "Write a fictional story …
  uses heroin" present in both). Near-dup scanned on the capped train (the documented
  exact-on-full + near-on-capped compute fallback; near-dup on the full 562k pool is impractical).

**Manifest = 257 distinct** train↔test leakage texts, purged from train. *(Implementation note:
`cross_dedup_pairs(train, eval)` returns `(eval_idx, train_idx, sim)`; the Arm-B `leakage_gate.py`
reads the first element as the train index — a latent bug, harmless there because it found zero near
pairs — corrected here to the second-element train index. Worth an upstream fix to the Arm-B gate.)*

### (e) Realized train + over-defense + cluster grounding

- **Train ≈ 29,047**: 7,261 positives (7,262 capped − 1 direct⊗test leakage) + 21,786 negatives @ **3.0:1**
  (deepset 399 / neuralchemy `full` 3,475 / guychuk top-up 17,912; negative⊗test + near-dup purges
  absorbed by the guychuk top-up holding the ratio). ≈ the Arm-B B− ~30k scale.

**2026-06-10 audit correction (record-only):** Rev 4(e) quotes the pre-purge composition; the realized
artifact (capped/summary.json) is 29,048 train / 7,262 pos / neuralchemy 3,219 / guychuk 18,168 — the
leakage manifest removed 256 neuralchemy negatives pre-cap (refilled by guychuk top-up), and the single
mosscap purge was absorbed by the cap (no −1).

- **NotInject over-defense = 339** (canonical one+two+three) — a non-gating FPR column at a **val-fixed**
  threshold (FPR target = 0.01, mirroring M1 `_BENIGN_FPR_TARGET` / ADR-027 §5; ≤2% per §v).
- **Test-slice clusters** (read from loaders, logged): BIPIA 143 · InjecAgent 79 · JBB `Category` = 10 ·
  XSTest `type` = 18 — slice-prefixed (`slice::raw`) for global bootstrap-cluster uniqueness (§Stat 170).

### (f) Pools + B+ (the /exploring-options decisions)

- **Arm-A robustness** = capped-balanced primary (tfidf + frozen) **+ uncapped natural-mix** dominance
  check (**tfidf-only** — embedding ≈1.1M texts on the local RTX 2070S is impractical; frozen-uncapped
  deferred + logged, no silent skip).
- **Arm-B B+** = natural-mix only (the primary B+−B− direct-data-bridging contrast), now unblocked by
  `load_direct_base`.

**Nothing in (a)–(f) changes the question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, or the verdict labels.**

## Revision 5 — B3 cost reconciliation + lora-rung wiring (the paid-go finalization), 2026-06-05

**Dated, before any `lora` datum.** The cost reconciliation the original §Verification anticipated
("the real cost estimate is computed at B2 and **reconciled at this present-first go** (raise cap or
trim) before launch", B3 spec line 242). Records the B3 wiring + the cap raise decided via
`/exploring-options`. **The question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, and the verdict labels remain UNCHANGED** — this Revision
touches only the *cost cap* and the *implementation* of the (already-fixed) lora rung + verdict.

### (a) Empirical cost anchor + the 27-run estimate

Anchored on the two prior realized LoRA sweeps (the only same-recipe ModernBERT-base LoRA runs):

| anchor | GPU | realized $ | runs | per-run |
|---|---|---|---|---|
| attack-type M1 lora | H100 80GB HBM3 @ $3.29/h | **0.83** | 9 | — |
| carrier-LODO lora | H100 80GB HBM3 @ $3.29/h | **1.17** | 9 | ~102 s @ ~3.5k-row pools |

The realized GPU was the **H100 @ $3.29/h** both times (the cheap-24 GB fallback never resolved; the
spec's `assumed_hourly_rate_usd: 2.50` is optimistic — Rev 5 uses **3.29**). Cross-family pools are
**8–16× larger** (Arm A ~29k (e); Arm B B− 17.9k–33.7k (Rev 1); B+ adds the ~29k direct base → up to
~62k) → per-run ~300–700 s. **27 runs** (= Arm A 1 fold × 3 seeds + Arm B B− 4 × 3 + Arm B B+ 4 × 3,
each a LoRA fit over the `r_grid=(8,16)`): **$7.6 (low) / ~$11.3 (central) / $17.5 (high)**, one pod
(fixed ~$0.24 overhead amortized once).

### (b) Cap raise $6 → $14 (the reconciliation)

The original ~$6 hard cap (B3 spec line 241) is **infeasible** — even the low bound exceeds it. Decision
(`/exploring-options`): **raise the cap to $14** (base-budget; `contingency_unlock_1.md` classes lora
sweeps as base-budget; contingency untouched), **NOT** the trim-B+ option (which would drop the
pre-registered B+−B− bridging contrast, Rev 3 §vii). `runpod_crossfamily_sweep.yaml`:
`cost_cap_usd: 14`, `assumed_hourly_rate_usd: 3.29`, `max_runtime_minutes: 240` (240/60 × 3.29 =
$13.16 ≤ 14; runpod_deploy enforces timeout × rate ≤ cap).

### (c) lora-rung wiring (implementation of the already-fixed rung)

- **`run_b3_lora.py`** — train-only orchestrator; **reuses** the cheap-rung fold builders
  (`run_b2_4._build_fold` for Arm A; `assemble.assemble` + `folds_dialect.make_dialect_fold` for
  Arm B) and **imports** the LoRA recipe (`detectors.make_detector("lora")`, ModernBERT-base,
  `r_grid=(8,16)` — ADR-026, no reimplementation). Emits the **scorer-identical schema** (Arm A
  `[cluster_id,label,slice,y_score]`; Arm B `[text,label,dialect,cluster_id,y_score]`) + the
  `val_roc_auc` metrics.json `falsify_dialect_lodo.load_dialect_fold` requires, so the existing
  estimator + verdict ingest the lora column unchanged. Output subpaths mirror the cheap-rung trees
  (`B2_4_results/capped`, `B2_3_results/natural`, `B2_3_results_Bplus/natural`) for a literal
  post-pull merge (`--merge`).
- **`b4_verdict.py`** — the write-gated verdict (this section's pre-existing rule, lines 150-160),
  **locked here before any lora datum**: per-unit SURVIVES/FALSIFIED/SMALL-THROUGHOUT + the bare
  ½·Gx(frozen) comparator; descriptive aggregate (NOT a cross-fold bootstrap, line 172); the per-unit
  table leads (line 177). A free `--pre-validate` path (lora→frozen, frozen→tfidf) exercises every
  arithmetic branch on the existing cheap-rung trees before any spend.
- **Over-defense at lora** — `run_b3_lora.py` also scores NotInject (Arm A; the already-trained
  model) so B4 reports the lora over-defense FPR alongside the cheap-rung headline (e).

### (d) Launch ordering — graceful degradation

The $17.5 high bound exceeds the $14 cap, so a 240-min timeout is possible. The `run.body` is
**cheapest-robust-first** — Arm A (3 runs) → Arm B B− (12) → Arm B B+ (12, the ~62k-row pools last) —
so a timeout still leaves Arm A + B− with a complete, scorable lora column (a directional verdict for
two of three conditions) plus a cheap B+-only re-launch, rather than an un-computable partial tree.

### (e) B4 verdict-trust gate

The verdict is ratified only after an **independent multi-verifier adversarial audit** (the post-M1
5/5 + carrier / prototype codex+gemini precedent), given it is the last-standing-axis headline on a
paid result.

**Nothing in (a)–(e) changes the question, hypothesis, design axes, estimator, ROC-AUC basis, the
½·Gx(frozen) + 0.05 SESOI thresholds, or the verdict labels — only the cost cap and the lora-rung
implementation.**

## Revision 6 — realized pace + the concurrent Arm-B+ relaunch (execution-mode record), 2026-06-05

**Dated.** The B3 paid sweep ran; this Revision records (a) the realized per-run pace (which the Rev-5
estimate under-scaled), (b) the **scientifically inert** concurrent relaunch of Arm B+ that Rev 5(d)
anticipated ("a cheap B+-only re-launch"), and (c) its parameters. **The question, hypothesis, design
axes, estimator, ROC-AUC basis, the ½·Gx(frozen) + 0.05 SESOI thresholds, the verdict labels, AND the
LoRA recipe (`batch=16, epochs=3, lr=1e-4, r_grid=(8,16), max_length=512`, ModernBERT-base) remain
UNCHANGED** — this Revision touches only *scheduling* (how the fits are packed onto the GPU) and the
*cost record*.

### (a) Realized pace — the Rev-5 anchor under-scaled

The live sequential run (H100 80GB HBM3 @ $3.29/h) realized **~15–30 min/run** at the 18–62k-row
pools — not the Rev-5 ~300–700 s. Each fit used only **~8.5 of 81.5 GB** at ~71 % nvidia-smi
kernel-occupancy (NOT compute saturation; batch-16 underfills the SMs). So the **full 27-run matrix is
~11 h / ~$36**, not the Rev-5 $14. The Rev-5 anchor (M1/carrier at ~3.5k-row pools, ~102 s/run)
**under-scaled** to the larger cross-family pools. **Realized outcome:** the run reached **$14.05 /
256 min** — the local `run_job` orchestrator died at a context boundary, silently disabling its
in-process 240-min timeout + lifecycle hooks, so the pod ran ~16 min past nominal and was stopped by
the gpu-run-watcher's INDEPENDENT cost-guard (→ DF-12 case 4). It banked **Arm A 3/3 + Arm B− 11/12**
(missing seed=2 injecagent), schema-validated on-pod but **not pulled** (orchestrator died before the
artifact stage) — recovered post-hoc by restart→rsync. **Arm B+ did not start** — the
graceful-degradation Rev 5(d) ordered for.

### (b) Concurrency adds no verdict-relevant perturbation (comparable within bf16 noise)

The Arm-B+ relaunch packs **multiple LoRA fits concurrently** on one H100 (each ~8.5 GB ⇒ ~6 fit in
80 GB) via a CLI fan-out (`xargs -P N` over `run_b3_lora.py --arm B --variant B+ --dialects <d>
--seeds <s>`), **no code change**. This is **scheduling, not science**: each work-item is an isolated
process that calls the **seed-deterministic** `assemble.assemble(seed)` → the same fold → the same
**imported** recipe; co-tenant processes share no RNG, CUDA stream, or memory — concurrency does not
change a fit's *inputs*. (The fit itself is **not** bit-deterministic on GPU: the recipe sets only
`torch.manual_seed`, no `use_deterministic_algorithms`/cuDNN flags, so two same-seed runs differ at
bf16/atomics noise *whether sequential or concurrent* — "byte-identical" would be an overclaim.) Same
recipe + same seeds + **same H100/bf16** (`gpu_order` pinned to H100 80GB HBM3 = the live A+B− SKU) ⇒
**comparable within bf16/Hopper-atomics noise (≪ the 0.05 SESOI), not verdict-affecting**. The Rev-5
"one pod" line was a scheduling detail, not a specification. A determinism cross-check is **LOGGED, not gated**
(defined in this Revision + the YAML `run.body`): one item (`bipia` seed 0) is trained both solo and
inside the concurrent pack and their **test ROC** Δ (the verdict-input metric) is recorded — but the
locked recipe is **non-deterministic run-to-run** (only `torch.manual_seed`; CPU-thread / GPU-atomic
reduction order; a smoke showed Δtest_roc ≈ 0.12 / max|Δy| ≈ 0.39 between two same-seed, same-data
fits), so a tight gate would false-abort; the run aborts only on a **catastrophic** Δtest_roc > 0.2.
Inertness rests on the structural argument above; the science uses single-fit-per-seed (the cluster
bootstrap resamples clusters, not re-fits) — run-to-run irreproducibility never enters the verdict.

### (c) The concurrent B+ relaunch — parameters

`runpod_crossfamily_bplus_sweep.yaml`: H100/bf16 (Hopper-only), **calibrate-then-pack** — a probe
times 1 solo + 2 concurrent fits, sets the pack width (N≈6) and enables CUDA MPS only if the measured
concurrency is contended (speedup < 1.5). `cost_cap_usd: 13`, `assumed_hourly_rate_usd: 3.29`,
`max_runtime_minutes: 210` (a **ceiling**; expected realized ~$7–9 vs ~$18 sequential). Any B−
stragglers from the truncated live run are appended to the same fan-out (they merge into the
`B2_3_results` subpath). Post-pull: `run_b3_lora.py --merge` → `directional_table(rungs=[tfidf,frozen,
lora])` → `b4_verdict.py`, then the Rev 5(e) multi-verifier audit.

**Nothing in (a)–(c) changes the question, hypothesis, design axes, estimator, ROC-AUC basis, the
thresholds, the verdict labels, or the LoRA recipe — only GPU scheduling and the cost record.**

## Revision 7 — recovery blocked → unified all-27 concurrent re-run, 2026-06-05

**Dated.** The B3 paid sweep's Arm A + B− (Rev 6(a)) were stranded on an EXITED pod that RunPod
**cannot restart** ("not enough free GPUs on the host machine") — recovery is blocked indefinitely.
Since (i) Arm B+ must run fresh regardless and (ii) concurrency makes re-running cheap, this Revision
records the decision (`/exploring-options`) to **re-run ALL 27 in ONE concurrent pod**
(`runpod_crossfamily_all27_sweep.yaml`) rather than wait on capacity. **Same locked recipe, same
H100 80GB HBM3 SKU, all 27 in one run** → a single internally-consistent tree — strictly *better*
comparability than the Rev-6 plan of mixing stranded-sequential A+B− with fresh-concurrent B+. Per
Rev 6(b) this is **scientifically inert** (concurrency = scheduling; seed-deterministic inputs;
single-fit-per-seed; the cluster bootstrap resamples clusters, not re-fits). The previously-committed
`runpod_crossfamily_bplus_sweep.yaml` (B+-only) remains the audited concurrent pattern; the all-27
spec is its trivial generalisation (a per-line CLI fan-out across all arms via
`xargs … bash -c 'run_item "$@"'`). Budget `cost_cap_usd: 16` / `max_runtime_minutes: 280` (ceiling;
expected ~$12–14); pack order **A → B− → B+** so a timeout still banks A + B−. The determinism
cross-check (log-only, catastrophic Δ>0.2) and the recipe lock are unchanged from Rev 6. **Nothing
changes the question, hypothesis, estimator, ROC-AUC basis, thresholds, verdict labels, or the LoRA
recipe — only that all 27 are re-run together on one SKU.**

## Revision 8 — all-27 cost-cap outcome + B+ on a cheaper bf16 GPU, 2026-06-05

**Dated.** The Rev-7 all-27 H100 re-run **recovered Arm A (3/3) + Arm B− (12/12)** but the realized
concurrency was **compute-bound** (probe: 1.63× at 2 fits; N=6 ≈ no extra — the H100 saturates by ~2
fits for batch-16 ModernBERT-LoRA), so it cost-capped at ~$16 with only **1/12 B+** (browsesafe seed0)
done. The Rev-6/7 "~$8 concurrent B+" estimate was wrong: **B+ costs ~sequential GPU time regardless of
concurrency**. Decision (`/exploring-options`): finish the 12 B+ on a **cheaper Ada/Ampere bf16 card**
(`runpod_crossfamily_bplus_cheap_sweep.yaml`; 4090/A5000/A40/…, N=2, cap $8/600 min, expected ~$3–5) —
cheap-and-slow beats expensive-fast when compute-bound; local was ruled out (2070S 8 GB OOM + Turing
fp16 ≠ bf16 + CPU weeks-slow). **Cross-arch reconciliation:** these B+ fits are bf16 (same dtype as the
H100 A+B−) but a different arch (Ada/Ampere vs Hopper) → minor tensor-core drift, expected ≪ 0.05 SESOI;
the **browsesafe seed0 re-run** (also trained on the H100 in the all-27 run) is the direct cross-arch
drift check, recorded with the B4 verdict. All-27 pull lessons (an `lc()` mis-report + a cost-guard
pod-delete that nearly preceded the verify): the cheap-run external monitor uses a robust direct-`find`
count and **verifies the local tree before any pod delete**. **Nothing changes the question, hypothesis,
estimator, ROC-AUC basis, thresholds, verdict labels, or the LoRA recipe — only the B+ rung's GPU arch
(bf16 preserved) + the cross-arch reconciliation.**

## Revision 9 — sub-L40S-only gpu_order (the selection-policy fix) + cheap-card monitor, 2026-06-06

**Dated.** The Rev-8 cheap spec kept resolving a **slow L40S** even while genuinely cheaper cards were
in stock — root-caused to **selection policy, not availability** (two compounding causes): (1)
`provider.select_gpu_across_datacenters` walks `pod.datacenters` in order and returns the first stocked
card, so **US-TX-3 (L40S) was reached before the EU/CA datacenters** (EU-RO-1 → RTX 4090; CA-MTL-1 →
A5000/A40) that actually hold the cheap cards; (2) **GraphQL pricing returns empty in this environment**
(`pricing.fetch_gpu_prices → {}`), so `--max-gpu-price-usd` is **inert** — absent price data is treated
as "unknown, allow," so the price cap cannot skip the L40S. **Fix:** removed `NVIDIA L40S` + `NVIDIA
A100 80GB PCIe` from `pod.gpu_order` (now A5000/4090/A40/A6000/L40 only); the selector then fails over
US-TX-3 + US-KS-2 (their only configured GPUs are now excluded) and grabs the cheap card in
EU-RO-1/CA-MTL-1 naturally — **no datacenter reorder needed**. If **none** of the five is stocked the
launch **fails fast** (by design — never silently buy an L40S); a gettable window is confirmed first by
the new zero-spend **`scripts/cheap_gpu_monitor.py`** (`--once`/`--watch`), which reuses the same
selector on live `runpodctl datacenter list` data to report the launcher's TRUE would-pick and pings on
gettable↔not edges. **Finding:** sub-L40S cards ARE stocked now (A5000/A40/4090 @ CA-MTL-1 / EU-RO-1,
all `low`, flickering minute-to-minute). **Nothing changes the question, hypothesis, estimator, ROC-AUC
basis, thresholds, verdict labels, or the LoRA recipe — only which sub-L40S bf16 card the B+ rung lands
on (bf16 preserved; the Rev-8 cross-arch reconciliation via browsesafe seed0 is unchanged).**
