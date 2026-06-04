# B2.3 — Arm-B B− cheap-rung directional read (tfidf) — FINDINGS

**Status: directional read only — NOT a verdict** (the SURVIVES / FALSIFIED / SMALL-THROUGHOUT verdict is
lora-gated, B3). This is the **tfidf** rung only; the **frozen** rung, the ≥10 000-iter headline bootstrap,
and the **E8** off-the-shelf reference column are **deferred to a fresh session** (frozen is ~1–2 h on the
local 8 GB GPU, which is shared with another project). Generated 2026-06-04 by `run_b2_3.py` (Arm-B **B−**,
≥3 seeds, `n-boot = n-perm = 2000`) per `criteria.md` Rev 1/2.

## Result — within-indirect dialect transfer at the tfidf rung

`Gx = in-distribution-val ROC-AUC − held-out-dialect test ROC-AUC` (higher ⇒ bigger transfer wall).
Label-stratified cluster bootstrap (one-sided 95 % CI; positive- and negative-clusters resampled
separately). `perm_p` = presence-of-transfer diagnostic = P(permuted-null test_roc ≥ observed test_roc).

**natural-mix (primary verdict condition):**

| held-out dialect | val ROC | test ROC | `Gx` | 95 % CI | `perm_p` | neg clusters |
|---|---|---|---|---|---|---|
| browsesafe (HTML) | 0.996 | **0.535** | **+0.461** | [+0.456, +0.465] | 0.000 | 7422 |
| bipia | 0.954 | 0.601 | **+0.353** | [+0.299, +0.464] | 0.000 | 3 |
| fujitsu (RAG-doc) | 0.834 | 0.683 | **+0.152** | [+0.148, +0.155] | 0.000 | 10943 |
| injecagent (tool-output) | 0.952 | **0.988** | **−0.036** | [−0.043, −0.026] | 0.000 | 17 |

**dialect-balanced (robustness — downsample each train dialect to the smallest):** bipia +0.334 ·
browsesafe +0.439 · fujitsu +0.180 · injecagent −0.046 — materially identical ⇒ the walls are **not** a
dialect-dominance artifact.

## Reading

1. **A large within-indirect dialect-transfer wall at the lowest-capacity rung for 3 of 4 dialects.** A tfidf
   detector trained on the other indirect dialects barely transfers to a held-out dialect — **browsesafe
   tests at 0.535 ≈ chance** (its HTML carrier is lexically alien to a bag-of-words trained on
   email/RAG/tool text), bipia 0.60, fujitsu 0.68 — all far below their in-distribution val (0.83–0.996);
   the CIs exclude 0.
2. **InjecAgent is the exception** (`Gx −0.036`; held-out test 0.988 > val) — tfidf separates its tool-output
   attacks from benign trivially. But this is the **low-power fold** (17 negatives / 17 clusters vs 2,108
   positives; `criteria.md` Rev 2) → **indicative-only**, not headline-driving.
3. **`perm_p = 0` everywhere** = every held-out test_roc is statistically above chance (the large test sets
   resolve even browsesafe's 0.535 as non-zero). So the wall is about **magnitude** (the `Gx`), not literal
   chance — the bootstrap CI carries it. (Both bipia and injecagent are negative-cluster-poor — 3 and 17 — so
   their neg-side CIs are coarser; browsesafe/fujitsu are well-powered.)

## The open question (deferred — the point of the experiment)

This is the **cheap-rung baseline**. The pre-registered question is whether **capacity** climbs this wall:
does the **frozen** rung (ModernBERT-base embeddings), then the **lora** rung, shrink these `Gx`s toward 0
(capacity-dependent, as the attack-type axis was — §6.5 FALSIFIED) or do they persist (a real, capacity-
resistant dialect wall)? That comparison — frozen + lora + the E8 deployed-detector contrast — is the next
work. **No verdict is computed here** (lora-gated, B3).

## Caveats

- **tfidf only** — the frozen/lora rungs (the capacity comparison that the verdict needs) are not yet run.
- **`n-boot = 2000`** here (a directional preview); the pre-registered **≥10 000-iter** headline bootstrap is
  deferred to the same fresh session as frozen.
- The verdict logic in `criteria.md` (Rev 1/2: ½·Gx(frozen) + 0.05 SESOI floor, lora-gated) is **untouched**.

## Artifacts + reproduce

- `summary.json` (committed) — the full directional table (natural + dialect-balanced).
- Per-fold predictions/metrics under `B2_3_results/` are **gitignored** (648 MB; regenerated):
  `uv run python experiments/cross-family-transfer/run_b2_3.py --rungs tfidf --skip-e8 --n-boot 2000 --n-perm 2000`.
