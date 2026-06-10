# Cross-family transfer — B4 in-hand analysis (Arm A + Arm B−), 2026-06-06

Analysis on the data already in hand (Arm A 3/3 seeds; Arm B− 4 dialects × 3 seeds; **lora** rung)
performed while the B+ (bridging) rung runs on RunPod. **Arm A and Arm B− verdicts are FINAL** — B+ is
a separate arm (direct base added to the dialect-LODO train) and does not change the direct→indirect
(A) or dialect-LODO (B−) verdicts.

Reproduced with `b4_verdict.py` on the in-hand merged trees (real lora column, not `--pre-validate`):
`b4_verdict.py --results B2_4_results/capped --folds-arm A` and `--results B2_3_results/natural --folds-arm B`.

> **AUDIT (2026-06-06):** 5 independent adversarial verifiers -- verdict **ROBUST**. Numbers reproduce
> exactly, no bootstrap bug, no leakage, labels correct. **One correction applied: §4(ii) over-defense /
> shortcut claim downgraded** (mostly generic miscalibration). injecagent FALSIFIED confirmed
> *uninformative* (no wall at any rung). Full synthesis: `AUDIT_B4_2026-06-06.md`.

## 1. Self-audit — verdicts reproduce exactly

| unit | Gx_frozen | Gx_lora | CI_lora (label-strat. cluster bootstrap) | verdict |
|---|---|---|---|---|
| Arm A (`arm_a_pooled`) | +0.3127 | +0.3646 | [+0.2836, +0.4313] | **SURVIVES** |
| B− `bipia` | +0.3559 | +0.2911 | [+0.2071, +0.4634] | **SURVIVES** |
| B− `browsesafe` | +0.4590 | +0.4452 | [+0.4406, +0.4497] | **SURVIVES** |
| B− `fujitsu` | +0.3543 | +0.2275 | [+0.2244, +0.2308] | **SURVIVES** |
| B− `injecagent` | −0.0340 | −0.0140 | [−0.0140, −0.0140] | **FALSIFIED** |

All point estimates match the recorded verdict to the digit → **Arm A SURVIVES; Arm B− MIXED (3/4)**.
First-pass self-audit: PASS (point estimates deterministic; CIs are MC-noise around the recorded run).

## 2. The injecagent "transfer" is a degenerate-negative-class artifact

Held-out LODO test composition at the **lora** rung (per-seed `test_roc` mean over 3 seeds):

| dialect | n_test | n_neg | %pos | test_roc | median score (pos / neg) | reading |
|---|---|---|---|---|---|---|
| `browsesafe` | 14,719 | 7,422 | 49.6% | **0.555** | 0.983 / 0.982 | hardest wall — held-out pos≈neg, detector can't separate |
| `bipia` | 5,508 | 468 | 91.5% | 0.694 | 0.988 / 0.340 | real wall |
| `fujitsu` | 21,886 | 10,943 | 50.0% | 0.718 | 0.544 / 0.132 | real wall (balanced) |
| `injecagent` | 2,125 | **17** | **99.2%** | **1.000** | 1.000 / 0.0002 | **degenerate** — 17 negatives, trivially separable |

injecagent's held-out test has only **17 negatives** (0.8%), trivially separable (median score 0.0002
vs positives 1.000). Perfect separation makes `test_roc = 1.000` **invariant under the label-stratified
cluster bootstrap** → the CI collapses to a **zero-width point** at `Gx = val_roc − 1.0 = −0.014`
(observed CI `[−0.0140, −0.0140]`) → FALSIFIED triggers on `ci_low ≤ 0`.

This is **not** evidence of genuine cross-dialect capability transfer — it is that injecagent's held-out
negative class is degenerate, so the LODO test has essentially **no power** to detect a wall. The
FALSIFIED rule (`ci_low ≤ 0`) **conflates "transfers" (a tight CI at/below 0) with "uninformative" (a
degenerate/wide CI)**. injecagent is the latter.

**Reclassification:** injecagent = **uninformative / low-power**, not a cross-family counterexample. The
cross-family wall is genuinely demonstrated by the three dialects with real negative classes —
`browsesafe` the hardest (held-out pos≈neg≈0.98, `test_roc` 0.555).

> **2026-06-10 (audit W2 — slice RETIRED, second independent ground).** The full re-audit found a
> materialization bug upstream of this slice: `experiments/eda/materialize_datasets.py` *concatenated*
> the attacker instruction above the `Tool Response Template` instead of *substituting* it at the
> template's `<Attacker Instruction>` placeholder — so **all 2,108 injecagent positives carry the
> literal placeholder string**, making the positive class separable by a template artifact, and the
> "tool-output dialect" framing structurally off (the attack never sits inside the tool response).
> Verdict-conservative: the slice was already reclassified uninformative above, and no headline number
> rests on it. Disposition (P1.5): **the slice stays retired** — the materializer is fixed
> forward-only (substitution; `assemble.py` join made format-robust) and the ratified parquet is left
> as-run; any future use of injecagent requires re-materialization + a fresh leakage scan. Related
> data nits (audit W14): 2 duplicated positives; 45 inner⊗val near-dups — same disposition.

## 3. Capacity trajectory (frozen → lora): the wall persists

| unit | frozen | lora | Δ(lora−frozen) |
|---|---|---|---|
| Arm A | +0.313 | +0.365 | **+0.052 (did not shrink; point-only)** |
| `bipia` | +0.356 | +0.291 | −0.065 (attenuated, still strong) |
| `browsesafe` | +0.459 | +0.445 | −0.014 (flat, strongest) |
| `fujitsu` | +0.354 | +0.228 | −0.127 (attenuated, still real) |

(tfidf rung: see the B2.4 cheap-rung directional read, `B2_4_FINDINGS.md`.) Unlike **attack-type**
(wall dissolved at the lora ceiling) and **carrier** (small-throughout), the **cross-family** wall
**persists frozen → lora** in every genuine test → **capacity-resistant**.

> **W13 (2026-06-10 audit):** the Arm-A Δ = +0.052 is a **point contrast with no CI** (per-seed
> range **+0.020…+0.075**; the bootstrap was run within-rung, not on the cross-rung difference).
> Headlines must not present "the wall GREW" as established — the established claim is the
> verdict-bearing one: the wall **did not shrink** at the LoRA ceiling (SURVIVES on the
> pre-registered rule). The "grew" direction is consistent across all 3 seeds but unquantified.

## 4. Arm A over-defense @ the lora ceiling + the shortcut-learning reading

Capacity trajectory (Arm A, mean over 3 seeds):

| rung | val_roc | test_roc | Gx | over-defense FPR (NotInject @ 1% val) |
|---|---|---|---|---|
| tfidf | 0.997 | 0.525 | +0.472 | (not computed) |
| frozen | 0.998 | **0.685** | **+0.313** | (not computed) |
| lora | 0.999 | 0.635 | +0.365 | **38.5%** (33.9 / 42.5 / 39.2) |

(i) **The wall is non-monotonic in capacity.** The *frozen* pretrained embedding transfers **best**
(test_roc 0.685, Gx +0.313); tfidf (pure lexical) worst (+0.472); lora fine-tuning **erodes** the
frozen embedding's transfer (test_roc 0.685→0.635, Gx +0.313→+0.365) while sharpening in-distribution
fit (val 0.998→0.999). Fine-tuning trades cross-family transfer for in-distribution sharpness.

(ii) **Over-defense @ lora is elevated, but mostly generic miscalibration (corrected by audit, 2026-06-06).**
At the 1%-val-FPR threshold, **38.5%** of benign NotInject prompts are flagged -- but at the *same*
threshold **21.4%** of the genuine held-out *test* negatives also fire, so **~56% of the "over-defense"
is generic threshold miscalibration under distribution shift, not trigger-specific**. The
trigger-attributable excess is **+17.2pp on average but highly seed-variable** (seed-0 +4.9, seed-1
+24.6, seed-2 +22.0). NotInject scores are bimodal (median ~0.01; 28.9% score >0.9 — the ~38% figure is the over-defense FPR at the val-fixed threshold, not the near-1.0 mass *(corrected 2026-06-10)*), consistent with
*some* lexical sensitivity, but the specific "keys on the injection lexicon" mechanism is **not tested**.

**Reading (downgraded from an earlier over-claim).** A lexical-shortcut account would tie the
cross-family wall to the over-defense ("two faces of one mechanism"), but the evidence is weaker than
that warrants: ~56% of the over-defense is generic miscalibration, the trigger-excess is seed-variable,
over-defense is lora-only (no rung trajectory), and no shared-feature test links the two.
Distribution-shift miscalibration is an equally-supported alternative -- treat shortcut-learning as a
**plausible contributing hypothesis, not a demonstrated mechanism**. What *is* solid: frozen transfers
best, and lora trades a (modest) amount of transfer for in-distribution sharpness.

Caveat: over-defense is a lora-only datum (frozen/tfidf NotInject not scored), so no over-defense
*trajectory* is available from in-hand data. See `AUDIT_B4_2026-06-06.md`.

## Implications

- **Mechanism (downgraded by audit):** Arm A's over-defense is *elevated* (38.5%) but ~56% is generic
  threshold miscalibration (21.4% of real held-out negatives fire at the same threshold); the
  trigger-specific excess (+17.2pp) is seed-variable and the lexical-shortcut link to the wall is a
  hypothesis, not demonstrated. The lora ceiling's deployment cost (elevated benign FPR under shift) is real.
- **ADR-055 (spine):** cross-family **SURVIVES** is robust at the lora ceiling; the lone apparent
  "exception" (injecagent) is artifactual, not a capacity-dissolved wall.
- **Multi-verifier audit (DONE 2026-06-06 -- verdict ROBUST):** 5/5 verifiers; injecagent's zero-width
  CI confirmed a genuine degeneracy (not a bug) + uninformative at every rung; §4(ii) over-defense claim
  corrected. Full synthesis: `AUDIT_B4_2026-06-06.md`.
- The recorded B4 verdict labels **stand**, but injecagent's FALSIFIED should carry the
  degenerate-negative caveat (uninformative, not transfer).

## 5. B+ arm + bridging + cross-arch (3-arm complete, 2026-06-06)
The 3-arm **B+−B− bridging** contrast at the lora ceiling + the browsesafe-s0 **cross-arch
reconciliation**:

**B+ arm verdict (3 seeds; cheap 4090 run, ~7h, within $8 cap):** 3/4 SURVIVE — bipia +0.291
[+0.200,+0.477], browsesafe +0.391 [+0.387,+0.396], fujitsu +0.470 [+0.466,+0.473]; injecagent
-0.009 [-0.011,-0.007] FALSIFIED (uninformative again -- near-zero, the degenerate unit). Same shape
as B-.

**Bridging (B+ - B-, point):** direct-injection training data does NOT bridge to held-out indirect
dialects -- bipia +0.000, browsesafe -0.054 (slight reduction), fujitsu **+0.242 (worsens)**,
injecagent +0.005. fujitsu B+ is an *anti-transfer* wall: perm_p 0.9988 (held-out test_roc **below
chance**; B- perm_p was 0.0) -- adding the direct base makes the detector anti-correlate on held-out
fujitsu.

**Cross-arch reconciliation (browsesafe seed-0 B+, cheap Ada 4090 vs Hopper H100 all-27):** test_roc
0.5999 vs 0.5928, |Δ| 0.0072 ≪ SESOI 0.05 -> the cheap-card 4090 B+ rung is comparable to the H100
A+B- (criteria Rev-8 cross-arch caveat discharged).

**3-arm spine:** attack-type FALSIFIED · carrier SMALL-THROUGHOUT · **cross-family SURVIVES** --
triangulated: the direct→indirect wall (Arm A +0.365), the dialect-LODO walls (B- 3/4), and
direct-data-does-not-bridge (B+). The cross-family wall is **capacity-resistant** and is not dissolved
by mixing in cross-family training data.
