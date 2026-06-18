# B2.3 — Arm-B B− cheap-rung directional read (tfidf + frozen + E8) — FINDINGS

**Status: directional read only — NOT a verdict** (the SURVIVES / FALSIFIED / SMALL-THROUGHOUT verdict is
`lora`-gated, B3). This covers the two **local/free** rungs — **tfidf** (lexical) + **frozen**
(ModernBERT-base embeddings → LogReg) — at the pre-registered **≥10 000-iter** bootstrap, plus the **E8**
off-the-shelf detector reference column. Generated 2026-06-04 by `run_b2_3.py` (Arm-B **B−**, 3 seeds,
`n-boot = n-perm = 10 000`) per `criteria.md` Rev 1/2.

## Result — within-indirect dialect transfer (tfidf → frozen)

`Gx = in-distribution-val ROC-AUC − held-out-dialect test ROC-AUC` (higher ⇒ bigger transfer wall).
Label-stratified cluster bootstrap (one-sided 95 % CI; positive- and negative-clusters resampled
separately). `perm_p` = presence-of-transfer diagnostic = P(permuted-null test_roc ≥ observed test_roc).

**natural-mix (primary verdict condition), 3 seeds × 10 000-iter bootstrap:**

| held-out dialect | rung | val ROC | test ROC | `Gx` | 95 % CI | `perm_p` |
|---|---|---|---|---|---|---|
| browsesafe (HTML) | tfidf | 0.996 | **0.535** | **+0.461** | [+0.456, +0.465] | 0.000 |
| browsesafe (HTML) | frozen | 0.997 | **0.538** | **+0.459** | [+0.455, +0.463] | 0.000 |
| bipia | tfidf | 0.954 | 0.601 | +0.353 | [+0.301, +0.464] | 0.000 |
| bipia | frozen | 0.965 | 0.609 | +0.356 | [+0.279, +0.518] | 0.000 |
| fujitsu (RAG-doc) | tfidf | 0.834 | 0.683 | +0.152 | [+0.148, +0.155] | 0.000 |
| fujitsu (RAG-doc) | frozen | 0.884 | **0.529** | **+0.354** | [+0.351, +0.358] | 0.000 |
| injecagent (tool) | tfidf | 0.952 | 0.988 | −0.036 | [−0.043, −0.027] | 0.000 |
| injecagent (tool) | frozen | 0.960 | 0.994 | −0.034 | [−0.037, −0.030] | 0.000 |

**dialect-balanced (robustness — downsample each train dialect to the smallest), frozen `Gx`:** bipia +0.347 ·
browsesafe +0.443 · **fujitsu +0.555** · injecagent −0.046 — the walls **survive** balancing, and fujitsu's
**grows further** ⇒ not a dialect-dominance artifact.

## Reading — the frozen rung does NOT climb the dialect walls

1. **Capacity (tfidf → frozen) does not shrink the transfer gap; for fujitsu it *grows* it.**
   - browsesafe: `Gx` +0.461 → +0.459 — **unchanged**, test stays **0.538 ≈ chance**. ModernBERT-base
     *frozen embeddings* still cannot transfer to held-out HTML.
   - bipia: +0.353 → +0.356 — **unchanged**.
   - **fujitsu: +0.152 → +0.354 — the wall GROWS** (frozen test **0.529 ≈ chance**, *below* tfidf's 0.683).
     The frozen embedding is *worse* than bag-of-words at transferring to held-out RAG-doc injection.
   - injecagent: −0.036 → −0.034 — the **no-wall exception** holds (tool-output attacks separate trivially
     at both rungs; the 17-negative low-power fold, criteria Rev 2 — indicative only).
2. **Why fujitsu *worsens* at frozen (the diagnostic line).** A RAG-doc injection's discriminative signal is
   the **literal injected snippet** — surface tokens tfidf keeps and that partially transfer across dialects
   (0.683). The frozen ModernBERT embedding instead encodes the document's **topic/carrier**; held-out fujitsu
   docs land in an alien topic region and the injection signal washes out (0.529 ≈ chance). This dovetails with
   the pre-modeling EDA finding "carrier dominates the embedding" — more *frozen* capacity actively destroys a
   lexical signal here.
3. **Contrast with the attack-type axis (§6.5).** There, capacity monotonically dissolved the wall
   (tfidf → frozen → lora, FALSIFIED at lora). Here tfidf → frozen leaves the dialect walls intact or larger.
   Two non-exclusive readings, both pre-registered as open: (a) the dialect wall is genuinely more
   capacity-resistant; (b) *frozen* is the wrong capacity probe — a frozen encoder cannot re-tokenize HTML
   structure or re-weight toward the injection snippet, so only the **end-to-end `lora`** (B3) tests true
   capacity-climbing. **Frozen-persistence here does NOT predict the `lora` verdict — it sharpens it.**

## E8 — off-the-shelf detector reference column (non-gating, deployed-baseline contrast)

Three frozen public guards (chunk + max-pool, `_MAX_DOCS_PER_DIALECT = 2000` label-stratified cap, **logged**,
seed-0). Reporting **AUROC + per-class score means** (the audit discipline — blind accuracy / high-prevalence
AUPRC hides indirect-blindness).

| held-out | ProtectAI-v2 | Prompt-Guard-2 | Prompt-Guard-1 |
|---|---|---|---|
| bipia | 0.470 (atk .287 / ben .256) | 0.671 | **0.973** (atk .866 / ben .048) |
| browsesafe (HTML) | 0.591 (atk **.999** / ben **.998**) | 0.670 | 0.635 |
| fujitsu (RAG) | 0.693 | **0.889** | 0.502 |
| injecagent (tool) | 0.608 | **0.915** | **0.917** |

**Reading:** **no deployed detector generalizes across the indirect dialects.** Each guard is strong on *some*
carrier and blind on others (PG1: bipia 0.97 / fujitsu 0.50; PG2: fujitsu+injecagent ~0.9 / bipia+browsesafe
~0.67; ProtectAI: ≤0.69 everywhere). **HTML (browsesafe) is the hardest for all three** (max 0.67) —
ProtectAI's per-class means are both ≈ **0.999** (it flags *everything* on HTML → saturated, not
discriminating; the AUROC 0.591 reveals what the high scores hide). This is the deployed-guards-are-blind
finding the audit predicted, now quantified across four indirect carriers.

## Step 0 — val-carve sensitivity (write-gate diagnostic, ROW CARVE STANDS)

Before the frozen rung, a cheap CPU diagnostic (`val_carve_sensitivity.py`, 3 seeds × 4 folds, tfidf)
quantified whether the **cluster-blind** row-level val carve inflates `Gx` (fujitsu's paired poison/benign +
bipia's 12-context expansion can straddle inner-train/val). **Pre-stated rule (fixed before the numbers):**
material iff Δval ≥ 0.03 on a well-powered fold OR any `Gx` sign/SESOI flip.

| held-out | Δval (row − cluster-aware) | verdict |
|---|---|---|
| browsesafe | **+0.022** | < 0.03 |
| fujitsu | +0.008 | < 0.03 |
| bipia | −0.001 | — |
| injecagent | −0.004 | — |

**Verdict: ROW CARVE STANDS** (`val_carve_sensitivity.json`). The cluster-blind carve's optimism is real but
**sub-threshold** (max +0.022, on the HTML fold) and never flips a `Gx` sign or crosses the 0.05 SESOI — so
the pre-registered row carve is vindicated *on the record*, and the headline walls are unaffected (the largest
shift, browsesafe, leaves a +0.44 wall). Honest residue: browsesafe carries a small, measured val optimism.

## Caveats

- **No verdict** — the `lora` rung (the capacity ceiling that the verdict needs) is B3-gated; frozen is a
  mid-capacity directional datapoint, not the gate.
- **Frozen representational ceiling:** the frozen rung reads only the **first 512 tokens** (`FrozenProbe.max_length=512`)
  of each head+tail-truncated page — browsesafe's tail is largely unseen at this rung (the canonical
  `FrozenProbe` recipe, method-consistent with M1 / carrier-LODO; stated, not changed).
- **`perm_p = 0` everywhere** is near-vestigial: at these test-set sizes *any* above-chance signal resolves, so
  it tests **presence-of-transfer**, not the wall (browsesafe's 0.538 is statistically > chance yet still a
  +0.46 wall). The magnitude lives in the bootstrap CI; do **not** read `perm_p = 0` as "wall confirmed."
- **bipia (3) and injecagent (17) are negative-cluster-poor** → coarser neg-side CIs; browsesafe/fujitsu are
  well-powered. injecagent stays the stated low-power, indicative-only fold.
- **Bootstrap re-derived on the upstream primitive (2026-06-04).** The headline `Gx` point estimates +
  CI-low were **independently reproduced** on `eval_toolkit.bootstrap.stratified_cluster_bootstrap_ci`
  (v1.8.0, DF-10 — the composite multi-stratum generalisation; the single-block `cluster_bootstrap_ci`
  DF-9/v1.7.0 could not express the seed-averaging): **point EXACT, CI-low within MC noise** (bipia/injecagent
  Δ ≤ 0.0010 ≪ the 0.05 SESOI), directional reading unchanged — see
  [`experiments/REPRODUCTION_2026-06/`](../REPRODUCTION_2026-06/README.md). The committed numbers here
  remain the serial `falsify_dialect_lodo` reference; the production loop is unchanged (re-locking it onto the
  primitive for parallel future runs is a separate, optional follow-up).

## The open question (deferred — the point of the experiment)

Does the **`lora`** rung climb these walls (capacity-dependent, as the attack-type axis was — §6.5 FALSIFIED) or
do they persist (a real, capacity-resistant dialect wall)? The frozen rung says the walls do **not** climb so
far, and fujitsu's *grows* — but frozen cannot re-tokenize the carrier, so the `lora` rung (B3, paid, separate
present-first go) is the verdict gate. **No verdict is computed here.**

## Artifacts + reproduce

- `B2_3_results/summary.json` (committed) — both rungs (tfidf + frozen) at 10 000 iters + the E8 column.
- `val_carve_sensitivity.json` (committed) — the Step-0 diagnostic + verdict.
- Per-fold predictions/metrics under `B2_3_results/` are **gitignored** (regenerated):
  `PYTHONUNBUFFERED=1 uv run python experiments/cross-family-transfer/run_b2_3.py --rungs tfidf frozen --n-boot 10000 --n-perm 10000`
  (frozen needs the local 8 GB GPU; ~1–2 h, embeddings cached across seeds).
