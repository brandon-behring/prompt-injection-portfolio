# B2.4 — Arm-A direct→indirect cross-family transfer: cheap-rung directional read

**Status: DIRECTIONAL — NO verdict.** The SURVIVES / FALSIFIED / SMALL-THROUGHOUT verdict is
**lora-gated** (B3, a separate present-first paid go). This records the local/free cheap rungs
(tfidf + frozen ModernBERT-base) under the pre-registered design (`criteria.md` Rev 3 + 4). Pre-reg
ratified before any Arm-A `Gx` existed; realized counts in Revision 4.

The question (criteria §Question, Arm A): train on direct-injection corpora, test on the cross-family
OOD slate — does the transfer gap **collapse toward zero at `lora`** (capacity climbs the cross-family
wall, repos unify) or **persist** (a real capacity-resistant standing wall)? H_crossfamily pre-committed
**capacity-resistant**. The cheap rungs only show whether capacity *starts* to climb.

## Pooled gate — `Gx = val_roc − test_roc` over the 4 two-class slices

`Gx` on the pooled cross-family ROC-AUC (BIPIA + InjecAgent + JBB + XSTest); label-stratified
cluster bootstrap (≥10 000 iters, one-sided 95 % CI); per-fold permutation = presence-of-transfer
(does the pooled test beat chance?). 3 seeds; capped-balanced primary pool.

| rung | val_roc | test_roc | **Gx** | one-sided 95 % CI | perm_p | reading |
|---|---|---|---|---|---|---|
| tfidf | 0.997 | 0.525 | **+0.472** | [+0.389, +0.512] | 0.000 | large wall (test ≈ chance) |
| frozen | 0.998 | 0.685 | **+0.313** | [+0.227, +0.364] | 0.000 | **attenuated, persists** |

- The cross-family wall is **large at the lexical rung** (tfidf test ROC 0.525 ≈ chance) and
  **attenuates with representation capacity** (frozen 0.685) **but persists** — the frozen `Gx` CI
  excludes 0, sits far above the 0.05 SESOI floor, and frozen ≥ ½·tfidf (0.313 ≥ 0.236). So at the cheap
  rungs the wall is real and only *partly* climbed by frozen capacity.
- `perm_p = 0.000` at both rungs: the pooled test beats chance (the detector transfers *somewhat*,
  more so at frozen) — a wall that attenuates, not an absolute one.
- The pre-registered comparison: the within-BIPIA attack-type axis FALSIFIED at `lora` (T 0.135 → 0.082
  → −0.003) and the carrier axis was SMALL-THROUGHOUT (G 0.167 → 0.067). Here the cheap-rung trajectory
  (+0.47 → +0.31) is the *steeper-walled* start; whether `lora` dissolves it (FALSIFIED, repos unify) or
  it stands (SURVIVES, the within-BIPIA headline is bounded to its corpus) is the B3 verdict.

## Per-slice ROC (the §v lead result; descriptive, mean over seeds)

A pooled mean must not mask a single-slice wall — so the lead is the per-slice table.

| rung | BIPIA | InjecAgent | JBB | XSTest |
|---|---|---|---|---|
| tfidf | 0.419 | 0.202 | 0.512 | 0.454 |
| frozen | 0.537 | 0.387 | 0.553 | **0.617** |

- At tfidf **every slice is at/below chance** — the direct-trained lexical detector does not transfer to
  any cross-family slice (InjecAgent 0.202 = strong *anti*-transfer: the tool-output dialect is lexically
  opposite to the direct-injection games).
- At frozen the wall attenuates **unevenly**: XSTest (jailbreak/harmful prompts) climbs most (0.617),
  BIPIA/JBB reach ~0.54–0.55, and **InjecAgent stays below chance (0.387)** — the tool-output slice is the
  hardest cross-family transfer (consistent with its distinct dialect; Revision 1 §ii flagged it
  thin-but-real on the Arm-B side too).
- **Injection-only sub-aggregate** (BIPIA + InjecAgent, non-gating §v): tfidf 0.403 / frozen 0.546 — the
  injection-specific slices are *even more* walled than the pooled (which JBB/XSTest lift).

## Over-defense (NotInject; non-gating §v) — the trigger-word failure mode, loud *[2026-06-10: mechanism downgraded per AUDIT_B4 — over-defense is visible but not causally attributed; the lora-rung control showed ~56% generic firing.]*

NotInject FPR at a **val-fixed** threshold (FPR target 0.01 on in-distribution val; mirrors M1
`_BENIGN_FPR_TARGET` / ADR-027 §5):

| rung | over-defense FPR (mean, 3 seeds) |
|---|---|
| tfidf | **0.389** (0.398 / 0.392 / 0.378) |
| frozen | **0.359** (0.372 / 0.319 / 0.386) |

At a 1 % in-distribution benign-FPR operating point, the direct-trained detector flags **~36–39 % of
NotInject** (benign prompts carrying injection trigger-words) as attacks — the documented **trigger-word
over-defense** the InjecGuard/PIGuard MOF strategy targets (criteria §viii). The hard-negative training
(neuralchemy MOF + guychuk diversity) only partly mitigates it; capacity (frozen) barely helps. A
deployment-realistic caution that the headline ROC-AUC gate alone hides. *[2026-06-10: mechanism
downgraded per AUDIT_B4 — over-defense is visible but not causally attributed; the lora-rung control
showed ~56% generic firing.]*

## E8 — off-the-shelf deployed-guard reference (non-gating; AUROC per slice)

Frozen open-weights guards scored on each slice (chunk + max-pool); *do deployed guards generalize?*

| slice | ProtectAI-v2 | Prompt-Guard-2-86M | Prompt-Guard-1-86M |
|---|---|---|---|
| BIPIA | 0.470 | 0.671 | **0.973** |
| InjecAgent | 0.608 | 0.915 | 0.917 |
| JBB | 0.600 | 0.754 | **0.332** |
| XSTest | 0.411 | 0.638 | 0.644 |

- The deployed guards are **scope-specific, not universal**: Prompt-Guard-1 is strong on the *injection*
  slices (BIPIA 0.973, InjecAgent 0.917) but **fails on JBB (0.332 — below chance)**, the harmful-behavior
  slice — it is an injection detector, blind to (cross-task) harmful-content. ProtectAI is broadly weak
  (0.41–0.61). No single off-the-shelf guard covers the cross-family slate — the same scope-blindness the
  M1 reference column showed (ProtectAI mean-attack < mean-benign on BIPIA).

## Robustness — uncapped natural-mix pool (decision 5)

The dominance-robustness check: does the C=3,000 cap manufacture the wall? Uncapped natural-mix pool
(all 562,450 direct positives + 229,461 negatives, ratio 0.408 — positive-heavy by construction, the
cap's benign-heaviness cannot hold), tfidf-only (frozen-uncapped deferred — embedding ≈0.8M texts on
the local RTX 2070S is impractical; logged, not silently skipped).

| pool | tfidf Gx | one-sided 95 % CI | test_roc |
|---|---|---|---|
| capped (primary) | +0.472 | [+0.389, +0.512] | 0.525 |
| **uncapped** | **+0.487** | [+0.430, +0.515] | 0.512 |

**The wall is not a capping artifact** — uncapped (Gx +0.487) ≈ capped (+0.472), both ≈ chance test ROC.
Per-slice uncapped tfidf (BIPIA 0.437 / InjecAgent 0.148 / JBB 0.492 / XSTest 0.424) tracks the capped
pattern (InjecAgent the worst anti-transfer). The mosscap/hackaprompt game-domination does not create
the cross-family wall; capping (to bound the corpus-style confound, §viii) leaves the directional read
unchanged.

## Arm-B B+ — direct-data-bridging contrast (decision 6)

Now that `load_direct_base` is built, the Arm-B **B+** variant (train = the 3 other indirect dialects
**∪ the Arm-A direct base**) runs alongside B− (3 indirect only). **B+ − B−** = how much the direct
injection data buys indirect-dialect transfer. Natural-mix, 3 seeds (criteria §c primary).

| rung | dialect | B+ Gx | B− Gx | **B+ − B−** | B+ test_roc |
|---|---|---|---|---|---|
| tfidf | bipia | +0.372 | +0.353 | +0.019 | 0.590 |
| tfidf | browsesafe | +0.459 | +0.461 | −0.002 | 0.536 |
| tfidf | fujitsu | +0.227 | +0.152 | +0.075 | 0.655 |
| tfidf | injecagent | −0.021 | −0.036 | +0.015 | 0.981 |
| frozen | bipia | +0.350 | +0.356 | −0.006 | 0.623 |
| frozen | browsesafe | +0.456 | +0.459 | −0.003 | 0.541 |
| frozen | **fujitsu** | +0.494 | +0.354 | **+0.140** | 0.425 |
| frozen | **injecagent** | +0.089 | −0.034 | **+0.123** | 0.879 |

**Direct-injection data does not bridge to the indirect dialects.** The B+ − B− delta is ≈0 for
bipia/browsesafe (the well-powered dialects: ±0.02 at both rungs) and **positive (gap *widens*)** for
fujitsu (+0.14 frozen) and injecagent (+0.12 frozen) — i.e. adding the direct base makes indirect-dialect
transfer *worse*, not better. Frozen fujitsu B+ is the sharpest: test ROC 0.425 < chance, perm_p = 1.000
(the direct-augmented detector anti-transfers to RAG-document poisoning). Reading: **direct and indirect
are genuinely distinct families** — more direct-injection data pulls the detector toward the games'
style and away from the indirect carriers, rather than building a bridge. This independently corroborates
Arm A's large direct→indirect wall: the gap is a real family shift, not a data-quantity artifact.

## Realized pools (criteria Rev 4)

- **Train = 29,048**: 7,262 direct positives (deepset 263 / gandalf 999 / mosscap 3,000 / hackaprompt
  3,000, capped C=3,000) + 21,786 negatives @ 3.0:1 (deepset 399 / neuralchemy `full` 3,219 /
  guychuk top-up 18,168 — the 257-text leakage purge removed 256 neuralchemy negatives pre-cap; the
  guychuk top-up refilled). Exact-dedup + game-artifact filter + the §vi leakage manifest (257 train↔test
  texts) applied. *(reconciled to summary.json, 2026-06-10)*
- **Test (pooled gate)**: BIPIA 5,508 (143 clusters) / InjecAgent 2,125 (79) / JBB 200 (10) / XSTest 450
  (18). **Over-defense**: NotInject 339.

## Honest limitations (carried from criteria)

- **No verdict** — cheap rungs only; `lora` (B3) is the pre-registered decision rung.
- **n = 4 slices** ⇒ the read is directional; the per-slice table + within-slice cluster bootstrap carry
  the evidence, not a cross-slice aggregate.
- **Corpus-style confound (Mirror Design Pattern, §viii)**: the direct slate is mostly all-positive games;
  a residual style≈injection shortcut is structural (mitigated by multi-source + hard negatives + the
  leakage gate, reported not claimed away). The injection-only sub-cut + E8 triangulate it.
- **Prevalence varies across slices** ⇒ ROC-AUC is the gate metric (prevalence-invariant); AUPRC-vs-floor
  is the comparability anchor only.

## Next

**B3 (paid, separate present-first go):** the `lora` rung, both arms (Arm-B B+ and B−), ≥3 seeds; hard
cap ~$6 (`gpu-run-watcher`). **B4:** apply the FIXED logic (½·Gx(frozen) + 0.05 SESOI, lora-gated) to the
complete rung sweep → SURVIVES / FALSIFIED / SMALL-THROUGHOUT, per arm.
