# ADR-055 cross-family amendment — DRAFT (pending ratification), 2026-06-06

> Prepared by `adr-scribe` (read-only; drafts only). **NOT ratified** — not written to the canonical
> `decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md` body. Ratification (append to ADR-055,
> reword Decision 1, update `decisions/README.md`, commit) is **user-led**. Markdown links below are
> relative to `decisions/` (where the section will be pasted on ratification). Sources:
> `B4_FINDINGS.md`, `AUDIT_B4_2026-06-06.md`, `criteria.md` (Rev 1–9).

---

## Proposed amendment (append this `##` section to ADR-055)

## Cross-family transfer resolution — 2026-06-06 (B4 LoRA-ceiling verdict in; third spine axis)

**Status: FILED — this section is the formal amendment to Decision 1** (the spine becomes a three-axis taxonomy) and **discharges the deferral registered in [Reproduction stamp + dialect open-axis — 2026-06-04](#reproduction-stamp--dialect-open-axis--2026-06-04)** ("the formal dialect capacity-dependence amendment is deferred until its `lora` verdict — this note registers the axis as open/directional, *not* a spine claim"). The cross-family / dialect `lora` verdict is now in; the axis graduates from OPEN/directional to a recorded spine claim. It also **closes the cross-family gap that [`prototype-comparison-audit-2026-06.md §A.5`](../docs/planning/prototype-comparison-audit-2026-06.md) marked "Open (the sharpest item)"** — *does fair-tuned capacity climb the cross-family wall the way it climbed the attack-type wall?* — on trustworthy footing (an independent rebuild from our audited `data/raw/`, never the prototype's artifacts).

The Decision-5 carrier gate and this gate are siblings: both ask whether end-to-end LoRA dissolves an OOD gap. The carrier axis landed `SMALL-THROUGHOUT` (capacity-attenuated). The **cross-family** axis lands on the **opposite** pole — **`SURVIVES`** — making it the **first axis where the wall is capacity-resistant** (the gap persists, and in places *grows*, at the LoRA ceiling). The pre-registration (`experiments/cross-family-transfer/criteria.md`, Rev 1–9 — all dated before any cross-family/dialect datum) fixed the three honest outcomes (`SURVIVES` / `FALSIFIED` / `SMALL-THROUGHOUT`) and the byte-for-byte decision rule (the §6.5 + carrier rule, on the ROC-AUC basis: SURVIVES iff `Gx(lora) > 0` AND one-sided 95% bootstrap CI-low > 0 AND `Gx(lora) ≥ ½·Gx(frozen)` AND `Gx(lora) ≥ 0.05` SESOI; FALSIFIED iff CI-low ≤ 0; else SMALL-THROUGHOUT) before any LoRA datum.

**Verdict (computed by `b4_verdict.py` on the merged rung tree; narrative `experiments/cross-family-transfer/B4_FINDINGS.md`, audit `experiments/cross-family-transfer/AUDIT_B4_2026-06-06.md`): cross-family `SURVIVES` — capacity-resistant.** Three triangulating reads, each at the `lora` (M1) ceiling, with `Gx(rung) = in-distribution-val ROC-AUC − held-out-test ROC-AUC`:

| read | unit | Gx_frozen | Gx_lora | CI_lora (one-sided 95%, label-strat. cluster bootstrap) | verdict |
|---|---|---|---|---|---|
| **Arm A** (direct→indirect, pooled) | `arm_a_pooled` | +0.313 | **+0.365** | [+0.284, +0.431] | **SURVIVES** (wall *grew* with capacity) |
| **Arm B−** (dialect-LODO, indirect-only train) | bipia | +0.356 | +0.291 | [+0.207, +0.463] | **SURVIVES** |
| | browsesafe | +0.459 | +0.445 | [+0.441, +0.450] | **SURVIVES** (hardest — held-out pos≈neg≈0.98) |
| | fujitsu | +0.354 | +0.228 | [+0.224, +0.231] | **SURVIVES** |
| | injecagent | −0.034 | −0.014 | [−0.014, −0.014] | FALSIFIED — **uninformative**, NOT a counterexample (see Caveats) |

**Arm B− = 3/4 SURVIVE** (the three dialects with a genuine negative class); **Arm A SURVIVES**. Unlike the attack-type axis (`lora` T = −0.003, FALSIFIED — fully dissolved) and the carrier axis (`SMALL-THROUGHOUT`, ~60% attenuated), the cross-family wall **persists frozen → lora in every genuine test**, and Arm A's wall *grows* (+0.313 → +0.365). It is **capacity-resistant**.

**Arm B+ — adding direct-injection training data does NOT bridge to held-out indirect dialects.** The pre-registered B+ arm (`train = K−1 indirect dialects ∪ the Arm-A direct base`, on the cheap Ada 4090 bf16 card per `criteria.md` Rev 8) is the same shape — **3/4 SURVIVE** (bipia +0.291, browsesafe +0.391, fujitsu +0.470; injecagent −0.009 uninformative). The **B+ − B− bridging contrast** is ≈0-or-worse: bipia +0.000, browsesafe −0.054, **fujitsu +0.242 (worsens)**, injecagent +0.005. **fujitsu B+ anti-transfers** — permutation p = 0.9988, held-out `test_roc` *below chance* (B− perm p was 0.0): adding the direct base makes the detector anti-correlate on held-out fujitsu. So capacity-resistance is **not bought off by mixing in cross-family training data** — a notable secondary finding.

**Cross-arch reconciliation (discharges the `criteria.md` Rev-8 caveat).** browsesafe seed-0 B+ was trained on both the cheap Ada RTX-4090 (`test_roc` 0.5999) and the Hopper H100 all-27 run (0.5928); |Δ| 0.0072 ≪ the 0.05 SESOI → the cheap-card B+ rung is comparable to the H100 A+B−, so the bf16 cross-arch drift does not perturb the verdict.

**Independent multi-verifier audit — ROBUST (the Rev-5(e) verdict-trust gate, satisfied).** The A+B− verdict was audited by **5 adversarial verifiers** (blind reproduction, bootstrap/CI integrity, data/leakage, claims red-team, verdict-rule), each read-only and prompted to refute: V1 REPRODUCED (every Gx recomputes to <0.001 with no project imports; sklearn == `eval_toolkit.roc_auc_point`), V2 SOUND (the injecagent zero-width CI is a *genuine* degeneracy from 17 singleton negative clusters + perfect separation, not a bootstrap bug), V3 CLEAN (composition exact, 0 train-in-test leakage re-verified, labels correct), V4 1 OVER-STATEMENT (corrected — below), V5 CORRECT (all 5 labels re-derive; MC noise ~0.004, none near a gate). **No verdict label changes.** Full synthesis: `experiments/cross-family-transfer/AUDIT_B4_2026-06-06.md`.

**The one correction (V4, independently re-verified).** The B4 finding-note's §4(ii) — that Arm A's elevated `lora` over-defense (38.5% of benign NotInject flagged at the 1%-val-FPR threshold) and the cross-family wall are "two faces of one lexical-shortcut mechanism" — was **over-stated and is downgraded**. At the *same* threshold, **21.4%** of the genuine held-out *test* negatives also fire, so **~56% of the over-defense is generic threshold miscalibration under distribution shift**, not trigger-specific; the trigger-attributable excess is +17.2pp on average but **seed-variable** (4.9 / 24.6 / 22.0) and the "keys on the injection lexicon" mechanism was never tested. Lexical-shortcut overfitting is now recorded as a **plausible contributing hypothesis, not a demonstrated mechanism**. What stands: the frozen pretrained embedding transfers *best* (Arm A `test_roc` 0.685, Gx +0.313), LoRA fine-tuning trades a modest amount of that transfer for in-distribution sharpness (`test_roc` 0.685 → 0.635, val 0.998 → 0.999), and the elevated benign FPR under shift is a real deployment cost.

**Resolution: the spine becomes a three-axis taxonomy, not a single capacity-dependent wall.**

> **attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family SURVIVES**

Decision 1's "OOD is several axes" framing is **confirmed and sharpened**: capacity does not act uniformly across axes. End-to-end LoRA **dissolves** the within-BIPIA attack-type gap ([ADR-054](ADR-054-m1-lora-ceiling-full-ft-deferred.md) "Trigger-gate resolution"), **attenuates** the within-BIPIA carrier gap to a residual table-carrier wall ([Carrier-LODO resolution](#carrier-lodo-resolution--2026-06-01-m2-pre-flight-verdict-in)), but **does not climb** the cross-family direct↔indirect wall — which is the one axis that is **capacity-resistant** (persists, grows in Arm A, and is not bridged by cross-family training data). This **bounds the within-BIPIA capacity-dependent headline to its corpus** and reconciles cleanly with the submission's "the OOD wall is real and backbone-invariant" carrier null: backbone-invariant ≠ capacity-invariant, and the cross-family wall is now shown capacity-resistant on independent footing.

**Caveats (pre-committed; recorded with the verdict).**
- **injecagent FALSIFIED is uninformative, NOT a counterexample.** Its held-out fold has **17 negatives** (0.8%, perfectly separable, median neg score 0.0002 vs pos 1.000) → `test_roc` = 1.000 is invariant under the label-stratified cluster bootstrap → the CI collapses to a **zero-width point** at Gx = −0.014. **Gx is negative at all three rungs** (tfidf −0.036 / frozen −0.034 / lora −0.014) → there was **no wall at any capacity**, so this fold has essentially no power to detect one. This is the thin-negative limitation pre-committed in `criteria.md` Rev 1 §(ii) / Rev 2 §(a) — read indicative-only, never headline-driving.
- **The FALSIFIED rule conflates "transfers" with "uninformative."** `ci_low ≤ 0` fires both for a genuine collapse (a tight CI at/below 0) and for a degenerate/no-power fold (injecagent). This is a **documented, pre-registered limitation** of the decision rule (`criteria.md` Rev 1–2), not a defect introduced here; the genuine cross-family wall rests on the three dialects with real negative classes + Arm A.
- **bipia / browsesafe are lower-power but valid.** bipia has 468 negatives over only 3 negative clusters (coarse but *wide*, conservative CI, far from 0 → SURVIVES unaffected); browsesafe's val is near-saturated (~0.9998) but its `test_roc` is genuinely mid-range (0.555, std 0.0027) → real resolution, not a val artifact.
- **fujitsu B+ below-chance anti-bridge** (perm p 0.9988) is a notable secondary finding recorded above, not a verdict-bearing result.
- **n=5 Arm-A slices / n=4 Arm-B dialects** ⇒ the aggregate is low-power; the read is **directional** (as on the n=3 carrier axis). The per-unit table carries the evidence, not a cross-fold aggregate (`criteria.md` Rev 2 §(b)). The corpus-OOD confound (Arm B holds out a *corpus* = carrier + source + style bundle, not carrier alone) is the pre-committed E5 limitation.

**Estimator + cost.** Label-stratified cluster bootstrap within each held-out unit (positive- and negative-clusters resampled separately, ≥10,000 iters, one-sided 95% percentile CI; per-unit clusters per `criteria.md` Rev 1: bipia → payload-id, browsesafe → page-id, fujitsu → doc-id, injecagent → tool-id, Arm A → test-dataset slice). The `lora` rung trained on RunPod across an A→B−→B+ matrix; the spend reconciliation (`criteria.md` Rev 5: cap raised $6 → $14, base-budget per `contingency_unlock_1.md`) and the realized run record (Rev 6–9: the live H100 cost-capped at ~$14, recovery blocked → unified all-27 H100 re-run recovered Arm A + B−, B+ finished on a cheaper sub-L40S Ada bf16 card ~$3–5). **Base-budget throughout** — [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md)'s $250 base « $350 hard cap is untouched and [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) **stays Reserved**.

**Cross-references resolved.** The [2026-06-04 dialect-open-axis note](#reproduction-stamp--dialect-open-axis--2026-06-04)'s "`lora` verdict is OPEN (B3-gated)" → **RESOLVED → `SURVIVES`**; its "formal dialect capacity-dependence amendment is deferred until its `lora` verdict" → **discharged here**. `prototype-comparison-audit-2026-06.md §A.5` ("the cross-family wall under fair tuning — Open, the sharpest item") → **CLOSED**: fair-tuned capacity does **not** climb the cross-family wall (Arm A SURVIVES, grows; B+ does not bridge). The criteria's §Verification B4 step + Rev 5(e) verdict-trust gate (multi-verifier audit) → **discharged**.

---

## Ratification checklist

### Open questions (user judgment calls)
1. **Amendment-in-place vs new ADR.** Drafted as an appended `##` section to ADR-055 (matches the carrier-LODO + dialect-open-axis precedent). Alternative: a standalone **ADR-056** (next free id) — unconventional for this spine. *Recommend: in-place.*
2. **Reword Decision 1 in place?** The carrier amendment reworded Decision 1's body. For symmetry, Decision 1's spine sentence should name three axes. ADR-011 immutability argues for leaving the body + letting the dated section govern. *Recommend: light reword of Decision 1's spine sentence (precedent set by carrier).*
3. **Title / framing tension.** ADR-055's title + Decision 1 say "**capacity-dependent** OOD spine" — but cross-family is capacity-*resistant*. Honest one-liner: "OOD is **axis-dependent**: attack-type dissolves, carrier attenuates, cross-family resists." *Recommend: reword Decision 1 to "axis-dependent taxonomy"; add a title erratum note (frontmatter title change optional).*
4. **Emit a `verdict.json`?** The carrier amendment cites `experiments/carrier-lodo/verdict.json`; cross-family has none on disk (only `b4_verdict.py` output + the markdown). *Recommend (optional): emit `experiments/cross-family-transfer/verdict.json` for parity before ratifying — a build step, generatable from `b4_verdict.py`.*
5. **Lane 6 promotion — RESOLVED.** `grep` confirms **no "Lane 6"** in `PORTFOLIO_PLAN.md`. → **drop** the criteria's "promote Lane 6 to active" clause (no target). No action.
6. **injecagent table label.** Kept **FALSIFIED** (literal recorded label) + inline "uninformative, NOT a counterexample". Alternative: show **UNINFORMATIVE** as operative (FALSIFIED noted as the mechanical rule output). *Recommend: keep as drafted (faithful to the recorded run + audit "no labels change").*
7. **Commit trailer (note, not a question).** Project trailer is `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.

### Downstream impacts (apply on ratification)
- **ADR-055 Decision 1** — refine the spine statement to the three-axis taxonomy (see Q2/Q3).
- **`decisions/README.md`** (the ADR-055 row, ~:141) — update the one-line summary to record the third axis (cross-family SURVIVES, capacity-resistant, B4 2026-06-06, audit ROBUST).
- **`docs/planning/prototype-comparison-audit-2026-06.md` §A.5** — mark **CLOSED** (cross-family wall confirmed capacity-resistant under fair tuning).
- **`docs/planning/PORTFOLIO_PLAN.md`** — §5 (Lane-2 framing + submission backbone-invariance reconciliation), §16 (gate registry), §17 (Ch 7/8/9/13 anchors): headline shifts from "OOD is capacity-dependent" → "axis-dependent: one axis resists capacity."
- **`docs/planning/SESSION-HANDOFF.md`** — record cross-family SURVIVES / audit ROBUST as the latest landed result; drop "B3 = next / lora-gated" framing.
- **`MEMORY.md` cross-family entry** — stale ("B3 wiring built … NEXT = paid go → B4"); the auto-memory body is already updated.
- **ADR-052 / ADR-054** — no change owed (design anchor / contrast pole).

### Proposed `decisions/README.md` row edit
> - ✓ [ADR-055: post-M1 re-ladder — the multi-axis OOD spine; …] — … the **attack-type** axis is capacity-dependent (M1: LoRA dissolves it), the **carrier** axis is **partially capacity-resistant (provisional, n=3; carrier-LODO `SMALL-THROUGHOUT`, residual at table)**, and the **cross-family** axis is **capacity-resistant (`SURVIVES` at the LoRA ceiling, B4 2026-06-06; Arm A grows, B+ does not bridge; audit ROBUST)**.
