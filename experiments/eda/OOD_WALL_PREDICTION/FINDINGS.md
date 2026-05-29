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

3. **Off-the-shelf direct-injection probes are blind to BIPIA (V10 scope caveat, confirmed).**
   `protectai-v2` scores BIPIA attacks (0.25) ≈ benign (0.28); `Prompt-Guard-2` barely fires
   (0.03 vs 0.007). Their "collapse" is **probe scope-blindness**, not data — exactly the
   pre-registered caveat. The one indirect-capable probe (`Prompt-Guard-86M`/PG1) is **pending**
   its Meta Llama gate; rerun `run_v10_probes.py` adds it once granted.

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
- V10 is incomplete pending PG1 (the indirect-valid probe).
- qa/abstract carriers (license-gated) + PINT + Indirect-in-the-Wild excluded (honest ceiling).

## Reproduce

```
uv run python experiments/eda/OOD_WALL_PREDICTION/run_prediction.py     # V5, V9, results.json
uv run python experiments/eda/OOD_WALL_PREDICTION/run_a1_v4.py          # A1, V4, a1_v4_metrics.json
uv run python experiments/eda/OOD_WALL_PREDICTION/run_v10_probes.py     # V10 (PG1 once gate granted)
uv run python experiments/eda/OOD_WALL_PREDICTION/run_audit_matrix.py   # D2, audit_matrix.json
```
