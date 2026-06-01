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
