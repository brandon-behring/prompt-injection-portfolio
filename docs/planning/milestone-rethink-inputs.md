> **SUPERSEDED (2026-06-10):** this deliberation is folded into docs/planning/roadmap-refresh-2026-06-09.md §6 — all four implications resolved by the ADR-055 arc. Kept as the historical input brief.

# Milestone rethink — inputs (captured 2026-06-01; deliberation deferred to a fresh session)

**Purpose.** The full M0→M7 re-ladder was deferred at Round 27 (2026-05-29) to *post-LODO-results* per
[ADR-052](../../decisions/ADR-052-attack-type-generalization-study-design.md) ("locks the *design*, not the
lane reorganization; restructure deferred to Phase 3 — after results"). **That condition is now met** — M1
(attack-type-LODO) produced its §6.5 verdict on 2026-06-01. This doc distills the M1 inputs so the deferred
re-ladder can be run *fresh* without re-deriving them. **It decides nothing** — it is the read-first brief for
that session.

## What M1 delivered (the new evidence)

- **§6.5 OOD-wall verdict: FALSIFIED at the LoRA ceiling** (judged on `lora` per criteria Revision 2;
  `falsification_verdict.json`). Cross-rung on the merged tree: **tfidf +0.135 / frozen +0.082 SURVIVE,
  `lora` −0.003 FALSIFIED** — `T` collapses monotonically as capacity rises.
- **The headline reframe:** the OOD wall is a property of the **representation, not the task** — real for
  lexical / frozen-embedding detectors, **dissolved by end-to-end LoRA** (test ROC-AUC 0.965–0.981; per-type AUPRC 0.956–0.984 over a 0.926 prevalence floor). A **capacity-dependence** effect (S2 pre-registered the frozen-encoder transfer, verified at frozen; the LoRA dissolution is broader than S2's letter).
- **`full_ft` §16 trigger RESOLVED — does not fire** (ADR-054 "Trigger-gate resolution"): LoRA is the
  measured M1 ceiling; more capacity adds no decision-relevant OOD signal. M1's modeling scope is closed.
- **Cost:** $0.83 (base-budget; ADR-014 stays Reserved). Both runpod-deploy frictions filed (#116 rsync,
  #117 pricing-403).

## Implications to weigh in the re-ladder (OPEN — do not pre-decide here)

1. **Narrative / value-props.** The portfolio's "OOD wall" framing should shift from "there is a wall" to
   "**the wall is capacity-dependent — and we measured exactly where it dissolves**." This is a *stronger*,
   more nuanced story (a pre-registered falsification that survived a write-gate), not a weaker one. Does the
   M1 chapter's thesis / the book's spine need re-pointing around this?
2. **M2–M7 lane hypotheses.** Round 27's read — "the EDA reframes value-props but **falsifies no lane
   hypothesis**" — still holds; M1 falsified a *prediction*, not a lane. But the M1 finding plausibly
   *reframes* several lanes; capture as questions, not decisions:
   - **Lane 2 (LoRA detector / training):** M1 shows LoRA already generalizes across attack types near-
     perfectly on BIPIA. Does that change Lane 2's framing (the interesting axis may now be *data/carrier*
     generalization, not attack-type)?
   - **Lane 5 (activation probes):** does "the signal is learnable end-to-end but embedding-invisible"
     sharpen or weaken the probe story?
   - **Lanes 1b / 4 (§16 rescope gates):** already trigger-gated — recheck whether M1's result trips any.
3. **Sequencing.** Does the M1 outcome change the M2→M7 *order* or scope, or only the prose? (Round 27
   left the ladder intact pending exactly this.)
4. **An ADR-055** likely lands iff the re-ladder actually reorganizes lanes/chapters (per Round 27,
   ADR-053 was the placeholder number then; 053/054 are now taken → the re-ladder ADR is **055+**).

## Scope boundary / not in this deliberation
- The formal **`v0.1.0` M0 close** (tag + `gh release` + announcement) stays **user-led** (accounts not
  created) — orthogonal to the re-ladder; see `M0_READINESS.md`.
- M1 itself is closed; no more M1 compute is queued.

## Read first (for the fresh session)
- `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md` §"Realized verdict" + `falsification_verdict.json`.
- [ADR-054](../../decisions/ADR-054-m1-lora-ceiling-full-ft-deferred.md) (M1 ceiling + the trigger resolution).
- `PORTFOLIO_PLAN.md` Round-27 block (§ "Round 27 update — milestone rethink") + §16 gates.
- [ADR-052](../../decisions/ADR-052-attack-type-generalization-study-design.md) (governs the deferral).
- `dossier_implications_for_roadmap.md` (the *other*, dossier-driven input stream — fold both together).
