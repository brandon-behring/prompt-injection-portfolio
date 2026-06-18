# Carrier-LODO M2 pre-flight — FINDINGS (SMALL-THROUGHOUT: capacity attenuates the carrier wall)

**Verdict (pre-registered, `criteria.md` Rev 1+2): `SMALL-THROUGHOUT`.** The carrier-LODO ROC-AUC gap is
**real at the frozen rung (+0.167) but attenuates ~60 % at the LoRA ceiling (+0.067)** — statistically
distinguishable from zero (CI-low +0.064 > 0) yet below the capacity-resistance bar (½·G(frozen) = +0.084).
So the carrier axis is **neither capacity-resistant (SURVIVES) nor fully capacity-dissolved (FALSIFIED)**:
it is **capacity-attenuated**, with a residual gap concentrated in the **table** carrier.

Independently re-verified pipeline (this session, 2026-06): the criteria were fixed (Rev 1 ROC basis + Rev 2
in-distribution val) **before** the registered sweep; the cheap rungs ran local + free, the `lora` rung ran
on a RunPod H100 (~$0.85–1.20, pod deleted), merged + falsified locally.

## Cross-rung gap — G(rung) = mean over carriers of [val_roc_auc − test_roc_auc(held-out carrier)]

| rung | G | CI-low (5%) | per-carrier G (email / code / table) | reading |
|---|---|---|---|---|
| tfidf | −0.156 | −0.158 | −0.278 / −0.041 / −0.148 | **no wall** — lexical attack-string features are carrier-invariant |
| frozen | +0.167 | +0.163 | −0.004 / +0.171 / +0.334 | **real wall** — the carrier-dominated embedding fails to cross carriers |
| **lora** | **+0.067** | **+0.064** | −0.012 / +0.007 / +0.205 | **residual wall** — email/code close, **table persists** |

Decision rule applied to `lora` (the M1 ceiling): SURVIVES iff `G(lora)>0` & CI-low>0 & `G(lora)≥½·G(frozen)`;
FALSIFIED iff CI-low ≤ 0; else SMALL-THROUGHOUT. Here CI-low = +0.064 > 0 (**not FALSIFIED**) and
G = +0.067 < ½·0.167 = 0.0835 (**not SURVIVES**) → **SMALL-THROUGHOUT** (10 000 payload-clustered-within-carrier
bootstrap; `verdict.json`).

## What it means — the carrier axis vs the attack-type axis

- The **attack-type** axis (§6.5) **fully collapsed** at lora (T −0.003, perm p = 0.90, CI-low −0.008 →
  FALSIFIED): end-to-end capacity dissolved it completely.
- The **carrier** axis does **not** fully collapse: a residual, statistically-real gap (+0.067, CI-low
  +0.064) persists at the same ceiling. The carrier axis is therefore **more capacity-resistant than the
  attack-type axis** — but the resistance is **partial** (the gap shrinks ~60 % from frozen to lora).
- The residual wall is **carrier-specific**: the email (−0.012) and code (+0.007) gaps close at lora; the
  **table** carrier keeps a substantial wall (+0.205, val_roc 0.998 → test_roc 0.793 seed-mean (seed-0
  illustration: 0.837)). Table-formatted
  contexts are the hard carrier to generalize to even with end-to-end fine-tuning.

## Spine implication (ADR-055) — refine, not validate or dissolve

The Round-30 spine asserted "the carrier axis … is the **standing wall**" (capacity-resistant). The modeling
result **refines** that: "standing wall" is too strong. The honest claim is **capacity-attenuated, residual,
table-concentrated** — the carrier axis is distinguishable from the attack-type axis (it does *not* fully
dissolve) but it is *not* a fully standing wall (it attenuates ~60 % with capacity). The multi-axis,
capacity-dependent spine survives in spirit (axes differ in capacity-resistance) with the carrier claim
**downgraded from "standing wall" to "partially capacity-resistant, residual at the table carrier."**

## Why ROC-AUC, not AUPRC (the metric that revealed this)

At lora the table fold's **AUPRC** was val 1.000 / test ~0.96 — a small gap, because the ~94 %-positive
prevalence inflates AUPRC. The **ROC-AUC** is val 0.999 / test 0.837 (seed-0) (G +0.16) — the real gap. `criteria.md`
Rev 1 moved the estimator to ROC-AUC precisely because the carriers are 83–94 % positive; on AUPRC this
verdict would have been mis-read as "no gap." (Rev 2's in-distribution row-holdout val is what makes the
val↔test comparison clean — without it the gap conflated with the attack-type axis.)

## Honest limitations (pre-committed)

- **n = 3 carriers** (email/code/table; qa/abstract license-gated) → the cross-carrier mean is a 3-point
  average; the read is directional. The per-carrier spread is wide (email ≈ 0, table +0.21 at lora), so the
  aggregate `SMALL-THROUGHOUT` **masks a real, persistent table-specific wall** — the per-carrier breakdown
  is the more informative view than the aggregate.
- The verdict **label** `SMALL-THROUGHOUT` is the pre-registered else-branch name; the **substance** here is
  "capacity-attenuated with a residual table wall," not "small at every rung" (frozen was +0.167). Reported
  per the fixed rule; substance described honestly (the rule's three labels do not name this middle case).
- Separability ≠ collapse (arXiv:2602.14161): the carrier dominates the embedding geometry (silhouette
  0.197) **and** produces a frozen-rung detection gap — but end-to-end capacity attenuates most of it.

## Records
- **Verdict:** `experiments/carrier-lodo/verdict.json` (per-rung G + CI + per-carrier; 10k bootstrap).
- **Pre-registration:** `experiments/carrier-lodo/criteria.md` (Rev 1 ROC basis + Rev 2 in-distribution val;
  both dated before the registered sweep).
- **Merged 3-rung tree:** `experiments/attack-type-lodo/results/` (gitignored; tfidf+frozen local, `lora`
  pulled from RunPod `results_runpod_carrier_lora/`).
- **Harness + estimator:** `experiments/attack-type-lodo/{folds.py, falsify_carrier_lodo.py}` (committed
  `876b867`).
