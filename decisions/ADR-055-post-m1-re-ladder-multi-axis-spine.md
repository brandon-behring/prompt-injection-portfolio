---
adr_id: "055"
slug: "post-m1-re-ladder-multi-axis-spine"
title: "Post-M1 re-ladder: the multi-axis capacity-dependent OOD spine; Lane 2 re-pointed to the carrier axis; Lane 5 sharpened to intermediate-activation recovery; a carrier-LODO M2 pre-flight gate"
date: 2026-06-01
status: Accepted
linked_round: "R30 (post-M1 milestone re-ladder session)"
plan_section: "§5 + §9 + §16 + §17"
supersedes: []
---

# ADR-055: Post-M1 re-ladder — the multi-axis capacity-dependent OOD spine

## Status

Accepted (Round 30 lock). **Discharges the re-ladder deferral in [ADR-052](ADR-052-attack-type-generalization-study-design.md)** ("locks the *design*, not the lane reorganization; restructure deferred to Phase 3 — after results") and the placeholder in the Round-27 update (`docs/planning/PORTFOLIO_PLAN.md`) ("ADR-053 left available for when the LODO results actually trigger a re-ladder" — that slot is now 055, since 053/054 were consumed by the launch-wiring session). **Builds on, does not supersede, [ADR-054](ADR-054-m1-lora-ceiling-full-ft-deferred.md)** (M1's measured result + the full-FT trigger resolution it records). This ADR reorganizes *narrative + lane framing + sequencing*; it changes no committed M1 artifact and queues no compute (the one run it schedules is a separate present-first go — see Decision 5).

## Context

M1 (the attack-type-LODO study, Lane 1) is closed, ratified, and pushed. Its pre-registered §6.5 "OOD-wall" prediction was **FALSIFIED at the LoRA ceiling**, and the falsification is **capacity-dependent**: judged on `lora` per `criteria.md` Revision 2, the per-type contrast collapses monotonically as capacity rises — **tfidf T = +0.135 / frozen T = +0.082 SURVIVE, `lora` T = −0.003 (perm p = 0.90) FALSIFIED** (`falsification_verdict.json`; end-to-end LoRA detects every held-out type near-uniformly, test AUPRC 0.98–0.999). The `full_ft` §16 trigger is already **RESOLVED — does not fire** ([ADR-054](ADR-054-m1-lora-ceiling-full-ft-deferred.md) "Trigger-gate resolution"): more capacity only dissolves the wall further. M1's modeling scope is closed.

[ADR-052](ADR-052-attack-type-generalization-study-design.md) deferred the M0→M7 lane re-ladder to "Phase 3 — after results." That condition is met, and a `/exploring-options` deliberation (this session, **Round 30**) ran the deferred re-ladder against two folded input streams: `docs/planning/milestone-rethink-inputs.md` (the M1 result distilled) and `dossier_implications_for_roadmap.md` Zone 2 (the dossier-driven per-lane rescopes, already trigger-gated at Round 27).

**The axis distinction that governs everything below.** M1's "capacity-dependent" finding is on the **attack-type** axis ONLY, and M1 **held the carrier constant** by design (harness-spec §3: "same scenario set both sides → the only shift is attack type"). The portfolio's other OOD claim — that the **carrier** (the direct→indirect / email↔code↔table trust-boundary) is the standing wall — currently rests on **geometry, not a modeling result**: the frozen MiniLM embedding tracks the carrier, not the attack type (silhouette **by-carrier 0.197 vs by-attack-type −0.023**; KMeans→carrier **ARI 0.98** vs →attack-type **−0.001** — `OOD_WALL_PREDICTION/FINDINGS.md`; `a1_v4_metrics.json`). Whether end-to-end LoRA dissolves the *carrier* gap the way it dissolved the *attack-type* gap is **untested**. The re-ladder must therefore reframe the spine without overclaiming, and schedule the test that would close the gap.

This also reconciles with the **sibling submission**'s "the OOD wall is real and backbone-invariant" finding (the v1.1.2 DeBERTa null; submission ADR-060/063, cited in plan §5 + Ch 7). **These are not contradictory:** backbone-invariant ≠ capacity-invariant, and the submission measured the **carrier / direct→indirect** axis (pooled OOD across scenarios) while M1 measured the **attack-type** axis *within* indirect. The multi-axis spine is exactly what unifies them.

## Decision

Adopt the re-ladder as **five enumerated sub-decisions** (all Accepted; user-decided in the R30 deliberation):

1. **Narrative spine → multi-axis, capacity-dependent.** Replace the single "there is an OOD wall" thesis with: *OOD is several axes; the **attack-type** axis is **capacity-dependent** (end-to-end LoRA dissolves it), while the **carrier** axis dominates the representation geometry and is the **standing wall**.* This is a stronger, more precise story (a pre-registered falsification that passed a write-gate at the cheap rungs and was overturned only at the LoRA ceiling), not a retreat. The spine explicitly carries the submission-reconciliation (backbone-invariant ≠ capacity-invariant; submission measured carrier, M1 measured attack-type-within-indirect).

2. **Lane 2 → re-point headline + evaluation axis to the *carrier* axis.** Lane 2's method is **UNCHANGED** (LoRA-retrain + 2-variant loss ablation per [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md)); only the *axis it interrogates* moves: from attack-type generalization (now answered by M1 — LoRA already generalizes near-perfectly across attack types) to **carrier generalization**. State the hypothesis axis-precisely against the **available** carrier set (**email / code / table** immediately usable; **qa / abstract** license-gated per [ADR-052](ADR-052-attack-type-generalization-study-design.md)). Register "confirm attack-type generalization persists under the Lane-2 recipe" as a **cheap §16 optional secondary**, not the headline.

3. **Lane 5 → sharpen the activation-probe hypothesis; keep the gate.** Re-point the probe hypothesis to recover the signal from **intermediate activations** — the layers *between* the embedding-invisible final representation (silhouette −0.023 by attack-type) and the LoRA-visible end-to-end signal (test AUPRC 0.98–0.999). The existing **M3-entry d′ > 0.5 gate** (`dossier_implications_for_roadmap.md` Lane 5; §16) is **kept unchanged** as the port-only-vs-surface-third-path decision; the **surface-third-path** (CaMeL / capability-isolation pairing) stays the flagged lead alternative.

4. **§16 rescope gates → both stay registered as-is; add one Lane-4 watch-note.** M1 tested **neither** the Lane 1b (`hackett2025bypassing` char-injection ASR ±5pp) **nor** the Lane 4 (benchmark saturation) trigger — M1 measured attack-type LODO, not adversarial robustness and not the stacker. **Both gates stay registered unchanged.** Add one **watch-note** to the Lane-4 gate: M1's **0.98–0.999 LoRA AUPRC** is an early foreshadow of the saturation the M5-close gate watches for (revisit at M5-close).

5. **Converge → reframe + this ADR + one sequencing tweak.** Insert a new **carrier-LODO validation gate** at the **M1-exit → Lane 2-entry boundary** (an **M2 pre-flight**, mirroring the EDA-arc-as-M1-entry-gate pattern locked at Round 27). Milestone **order is otherwise unchanged** (still M0→M7; no rung added).

### The carrier-LODO gate (Decision 5, precisely)

- **Why it exists.** Decision 1's spine *asserts* the carrier is the standing wall, but M1 **held the carrier constant**, so that claim is presently **geometric** (carrier dominates the frozen MiniLM embedding — silhouette 0.197 vs −0.023; carrier ARI 0.98), **not a modeling result**. This gate converts the geometric claim into a modeling result (or revises the spine).
- **What it is.** A **leave-one-carrier-out (carrier-LODO)** read across the rung ladder (tfidf / frozen local + free; `lora` ~$1), **reusing the attack-type-LODO harness** (`docs/planning/attack-type-lodo-harness-spec.md`) with the **LODO axis swapped** (attack-type → carrier) and a **carrier-clustered** estimator (the §6.5 estimator was **payload-clustered**, `criteria.md` Rev 1 / `falsify_clustered.py` — the resampling unit must change with the held-out axis). Criteria **pre-registered before any run**, mirroring `experiments/eda/OOD_WALL_PREDICTION/criteria.md`, at `experiments/carrier-lodo/criteria.md`.
- **The decision it answers.** Does LoRA dissolve the **carrier** gap too (→ capacity dissolves *both* axes; the spine's "carrier is the standing wall" half is **revised**) or does the carrier gap **persist under LoRA** (→ carrier is **capacity-resistant**; the spine is **validated** as a modeling result)? It also **sizes Lane 2's scope** (the size of the gap Lane-2 training has to close).
- **Status.** **Scheduled now; the run is a separate present-first go** (NOT this session). This ADR registers the gate + commissions the criteria pre-registration; it does not run compute.

### Scope boundary

This ADR reorganizes narrative, lane framing, and the M1→M2 sequencing checkpoint. It does **not** change M1's committed artifacts, does **not** re-decide the `full_ft` trigger (resolved in [ADR-054](ADR-054-m1-lora-ceiling-full-ft-deferred.md)), and does **not** alter milestone *order*. The carrier-LODO run, the formal `v0.1.0` M0 close, and all public-facing acts remain user-led.

## Consequences

- **The spine becomes axis-typed.** Every downstream "OOD wall" mention must now name its axis (attack-type vs carrier) and its capacity regime (frozen vs LoRA). Surfaced as a downstream-impact list at ratification: plan §5 (Lane-2 framing + an axis-precision note reconciling the submission's backbone-invariant carrier null), §9 (the M2 pre-flight checkpoint), §16 (the carrier-LODO gate + the Lane-4 watch-note + a one-line "1b/4 untripped by M1" confirmation), §17 chapter outlines (Ch 7 anchor reframe; Ch 8 "backbone-invariance" → capacity-axis; Ch 9 Lane-2 axis re-point; Ch 12 Lane-5 intermediate-activation sharpening; Ch 13 lessons), and a new `experiments/carrier-lodo/criteria.md` pre-registration.
- **A pre-registration is now owed before the carrier-LODO run.** It must state the carrier-LODO split, the **carrier-clustered** estimator (not payload-clustered), the decision rule (reuse the §6.5 byte-for-byte rule — one-sided perm p < 0.05 AND one-sided 95% bootstrap CI-low > 0), the rung set, seeds, and the carrier set actually available (email/code/table; qa/abstract gated). This file does not yet exist; it is the gating artifact for Decision 5.
- **Lane 2's three-outcome framing (plan §5) is preserved but re-axised.** The existing "data-bound / structural / worsened" trichotomy stays; "structural wall (likely per ADR-052)" must be reworded — M1 showed the *attack-type* wall is *not* structural (capacity dissolves it), so the open structural question is now specifically the **carrier** wall, which the carrier-LODO gate sizes before Lane 2 commits.
- **No ADR is superseded; one deferral is discharged.** [ADR-052](ADR-052-attack-type-generalization-study-design.md)'s *design* stays Accepted and intact; only its "restructure deferred to Phase 3" clause is now executed. [ADR-054](ADR-054-m1-lora-ceiling-full-ft-deferred.md) is unaffected (this ADR consumes its result).
- **Cost.** $0 to file this ADR + write the pre-registration. The carrier-LODO read is **tfidf/frozen local (free) + `lora` ~$1** — base-budget by the same logic as `contingency_unlock_1.md` ([ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) stays Reserved); a fresh `contingency_unlock` tally is owed only at that run's launch, not now.
- **Watch-note, not a trigger trip.** The Lane-4 watch-note (Decision 4) records foreshadowing only; it does **not** fire the M5-close saturation gate now (the gate's criterion is 2-of-{PINT, PromptShield, WildGuardMix} > 95% AUPRC *on the stacker at M5 close* — none of which M1 measured).

## Alternatives considered

- **Full re-ladder: reorganize lanes/chapters/milestone-order now.** Rejected — overreach. M1 falsified a *prediction* on one axis, not a lane hypothesis; Round 27 already established that the EDA findings "reframe value-props but falsify no lane hypothesis," and that still holds. Re-point framing + insert one validation gate; do not re-sequence.
- **Treat M1's result as dissolving the OOD wall outright (drop the "wall" thesis).** Rejected — it would silently overclaim across the untested carrier axis and would *contradict* the submission's backbone-invariant carrier null. The multi-axis spine keeps both findings true.
- **Re-point Lane 2 to the carrier axis without a pre-flight gate.** Rejected — Lane 2's scope (and whether its headline is even live) depends on whether the carrier gap survives LoRA, which is exactly the geometric-vs-modeling gap. Sizing it first (cheap: ~$1) is the EDA-arc-as-entry-gate pattern that served M1 well.
- **Re-point Lane 5 to "embedding-invisible ⇒ probe can't work" (weaken it).** Rejected — that conflates the *final-layer* embedding (invisible) with *intermediate* activations (untested) and with the *end-to-end* LoRA signal (strongly present). The sharpened intermediate-activation hypothesis is the live, informative version; the d′ > 0.5 M3-entry gate already protects against a null port.
- **Fold the carrier-LODO criteria into this ADR's body.** Rejected — pre-registration belongs in a dedicated, timestamped `criteria.md` under the experiment dir (matching `OOD_WALL_PREDICTION/criteria.md`), so the write-gate discipline and revision policy apply; an ADR is not a pre-registration surface.

## Cross-references

- [ADR-052](ADR-052-attack-type-generalization-study-design.md) (attack-type-generalization study design — its "Phase 3 restructure deferred" clause is discharged here; its design + the harness it locks are reused with the LODO axis swapped to carrier)
- [ADR-054](ADR-054-m1-lora-ceiling-full-ft-deferred.md) (M1's measured ceiling = LoRA + the `full_ft` trigger resolution; this ADR consumes that result and does not re-open it)
- [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md) (Lane 2 LoRA-only + 2-variant loss — the method Decision 2 leaves unchanged while re-pointing the axis)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) ($250 base + $100 contingency; $350 hard cap — the carrier-LODO read's ~$1 `lora` increment is base-budget)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) (cost slot — **stays Reserved**; the carrier-LODO run is base-budget like `contingency_unlock_1.md`)
- `docs/planning/milestone-rethink-inputs.md` (the read-first brief that distilled M1's inputs for this R30 deliberation)
- `docs/planning/dossier_implications_for_roadmap.md` Zone 2 (the per-lane rescopes — Lane 2 carrier/data reframe, Lane 5 surface-third-path + d′ > 0.5 gate, Lane 1b/Lane 4 trigger gates — folded into this re-ladder)
- `docs/planning/PORTFOLIO_PLAN.md` §5 (the Lane-2 three-outcome framing + the submission backbone-invariant carrier null re-pointed here), §9 (M1→M2 pre-flight checkpoint), §16 Round-27 gates (carrier-LODO gate added; Lane-4 watch-note; 1b/4 untripped), §17 (Ch 7/8/9/12/13 outlines)
- `docs/planning/attack-type-lodo-harness-spec.md` §3 (the "carrier held constant" core design the carrier-LODO read inverts) + §5 (retention pre-commit pattern the new criteria mirror)
- `experiments/eda/OOD_WALL_PREDICTION/` — `FINDINGS.md` (silhouette 0.197 vs −0.023; carrier ARI 0.98; LoRA test AUPRC 0.98–0.999), `criteria.md` Rev 1 (payload-clustered estimator — the unit the carrier-LODO read must swap to carrier-clustered), `falsification_verdict.json` (tfidf +0.135 / frozen +0.082 / lora −0.003), `a1_v4_metrics.json` (by_carrier 0.197 / kmeans_vs_carrier 0.980)
- Submission **ADR-060 / ADR-063** (`prompt-injection-detection-submission` series — the v1.1.2 DeBERTa backbone-invariant carrier null reconciled by the multi-axis spine; a *different* ADR series, not amendable from this repo)
