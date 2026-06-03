# Phase-3 EDA findings — the pre-modeling OOD-wall prediction

**Recorded 2026-05-29, pre-modeling** (no Lane-1 detector has been trained; the
LODO accuracy gaps this forecast will be judged against do not yet exist). Method
locked in `criteria.md` *before* any metric was computed. Artifacts: `results.json`
(machine-readable), `audit_matrix.json`, `a1_v4_metrics.json`, `v10_scores.json`,
figures `V5_*.png` / `V9_*.png` / `V4_*.png` / `A1_*.png` / `V10_*.png` / `D2_*.png`.

## The prediction (falsifiable, ordinal — NOT a magnitude)

Per-test-attack-type **collapse RANK** = weighted-rank-average of E1 embedding-shift
and C2 shortcut-transfer-failure (tie-break C2). The 14 disjoint BIPIA test-attack-types,
predicted **most → least** likely to collapse:

- **top-4 predicted-worst (most collapse):** Task Automation, Business Intelligence,
  Conversational Agent, Research Assistance — all **task-intent** types.
- **bottom-4 predicted-best (least collapse):** Reverse Text, Substitution Ciphers,
  Scams & Fraud, Misinformation & Propaganda.

**Falsification (deferred to verification time):** a one-sided top-k vs bottom-k
permutation contrast on the eventual per-test-type diagnostic LODO AUPRC drops
(k=4); dual rule p<0.05 AND bootstrap-CI(top−bottom)>0; Kendall τ-b secondary.
Survives iff the predicted-worst tail collapses more than the predicted-best tail.

## Key structural findings (the EDA's real payload)

1. **The carrier dominates the embedding — the attack-type signal is embedding-invisible.**
   MiniLM silhouette by carrier = **0.197** vs by attack-type = **−0.023** (negative);
   KMeans→carrier ARI = **0.98** vs →attack-type = **−0.001**. The secondary folds agree:
   carrier+attack-external PAD = **2.0** (maximal) ≫ core attack-type PAD = **0.51**.
   ⇒ A detector keying on MiniLM embeddings would track the email/code/table *carrier*,
   not the injected payload. This is the dominant geometric fact and reframes "OOD":
   the largest shift is *carrier*, which the ADR-052 design holds constant.

2. **BIPIA indirect attacks are lexically subtle.** C1 top injected-leaning tokens are
   generic (`your`, `you`, `to`, punctuation), **not** crude `ignore previous instructions`
   markers — consistent with indirect injection (benign-looking task queries embedded in
   content). The lexical shortcut is weak/generic, so a shortcut-reliant detector has
   little to over-fit — but C2 still discriminates across types (AUPRC spread 0.29).

3. **Off-the-shelf probe behaviour splits by training scope (V10 — now complete; PG1 added 2026-06-01).**
   The two *direct*-injection probes are blind to BIPIA's indirect attacks: `protectai-v2` scores attacks
   (0.25) **below** its own benign floor (0.28) — no separation; `Prompt-Guard-2` barely fires (0.03 vs
   0.007). But the one *indirect*-capable probe, `Prompt-Guard-86M` (PG1; Meta gate now granted), **fires
   strongly** — mean attack **0.86** vs benign **0.04**, clean separation across all 14 attack types. So the
   "collapse" of the off-the-shelf probes is **scope-blindness, not undetectable data** — the pre-registered
   caveat, now confirmed *both* ways: a direct-trained probe misses indirect injection, while the
   indirect-trained probe catches it. (Closes issue #1; `v10_scores.json` `skipped_probes={}`.)

4. **The study anchor is uncontaminated.** Cross-dataset audit: BIPIA shares **0.0**
   near-duplicates (TF-IDF cosine ≥ 0.9) with any of the 8 certified working-set datasets;
   within-dataset PAD floor ≈ 0 (sanity passes). Off-diagonal PAD is saturated (~2.0,
   datasets trivially separable) — read **ordinal only** (a dataset fingerprint), per the
   pre-registered caveat that separability ≠ collapse (arXiv:2602.14161).

## Honest limitations

- Per-type N=5 attack strings → per-type estimates are noisy; the prediction is **ordinal**
  and falsified only via the **tail contrast** (never a full correlation, which N=5 attenuates).
- Embedding-space shift is small *because* the carrier dominates — the per-type PAD spread
  (0.69–1.27) is modest; the prediction leans on C2 shortcut-transfer to break ties.
- qa/abstract carriers (license-gated) + PINT + Indirect-in-the-Wild excluded (honest ceiling).

## Realized verdict — 2026-06-01 (post-LoRA, write-gate OPEN)

The headline §6.5 falsification ran on the complete 3-rung sweep (`tfidf + frozen + lora`,
3 folds × 3 seeds; LoRA trained on a RunPod H100, ~$0.83). Verdict judged on `lora` per
criteria Revision 2; machine-readable record in `falsification_verdict.json`.

| rung | capacity / representation | T (top−bottom per-type AUPRC) | perm p | CI-low | verdict |
|---|---|---|---|---|---|
| tfidf | lexical | +0.135 | 0.014 | +0.111 | **SURVIVES** |
| frozen | frozen MiniLM emb + LogReg | +0.082 | 0.014 | +0.064 | **SURVIVES** |
| **lora** | **end-to-end ModernBERT fine-tune** | **−0.003** | **0.900** | **−0.008** | **FALSIFIED** |

**The prediction is FALSIFIED at the LoRA ceiling — and that is the finding, not a miss.**
`T` collapses monotonically as capacity rises (0.135 → 0.082 → 0.000): the predicted-worst
attack-type tail is genuinely harder for lexical / frozen-embedding detectors, but a LoRA
fine-tune detects **every** type near-uniformly (test AUPRC 0.956–0.984, held-out types
included), erasing the per-type gap.

This is **capacity-dependence** — it confirms the pre-registered **S2** caveat where S2 applied, and
goes beyond it. S2 (`lane-1/hypothesis.md`) pre-registered only that the *prediction-encoder choice*
(MiniLM → frozen ModernBERT) does not change the ordering — and that held: the ranking **SURVIVES**
at the frozen rung (T +0.082). S2 said nothing about end-to-end capacity; the LoRA dissolution is the
broader, not-pre-committed finding (S2 argued, if anything, that the ordering *transfers*). The ranking was built from the
**frozen MiniLM embedding**, where the carrier dominates and the attack-type signal is
embedding-invisible (Key finding 1). End-to-end LoRA learns the attack-type signal directly, so
an embedding-derived ordering does not transfer. **On the attack-type axis, within BIPIA indirect injection, the "OOD wall" is a property of the
representation, not the task:** real for lexical / frozen-embedding detectors, and surmountable by a
small amount of end-to-end capacity, which detects every held-out attack-type near-uniformly (test
AUPRC 0.956–0.984). *Two scope caveats:* (a) at that near-ceiling level the top-k−bottom-k contrast is
partly saturation-compressed, so `T → 0` reflects uniform high detection as much as a "dissolved"
gap; (b) the held-out type shares carrier and corpus with training — this is *within-corpus*
generalization, **not** the prototype's *cross-family* (direct→indirect, cross-dataset) wall, which
was not re-derived under fair tuning (`ADR-052`) and remains **open**.

The FALSIFIED verdict is credible *because* it could not be gamed: the rule (judge on `lora`;
SURVIVES iff perm p < 0.05 AND CI-low > 0), the tail sets, `k`, and the estimator were all fixed
in `criteria.md` *before* any LoRA datum existed, and the write-gate only opened on a complete sweep.

## Reproduce

```
uv run python experiments/eda/OOD_WALL_PREDICTION/run_prediction.py     # V5, V9, results.json
uv run python experiments/eda/OOD_WALL_PREDICTION/run_a1_v4.py          # A1, V4, a1_v4_metrics.json
uv run python experiments/eda/OOD_WALL_PREDICTION/run_v10_probes.py     # V10 (PG1 once gate granted)
uv run python experiments/eda/OOD_WALL_PREDICTION/run_audit_matrix.py   # D2, audit_matrix.json
```
