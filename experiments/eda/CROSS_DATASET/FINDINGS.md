# Cross-dataset EDA findings (E1–E7) — the restored explore-first pass (2026-06)

> **What this is.** The cross-dataset EDA that `ADR-052` deferred when it narrowed modeling to BIPIA
> (see `docs/planning/dataset-utilization-and-eda-plan-2026-06.md`). It characterizes the **cross-family
> wall's geometry** *before* any modeling — the analog of the BIPIA-carrier EDA that made M1 credible.
> Local/free; reproducible via `experiments/eda/cross_dataset_geometry.py`.
> **Status:** E1–E7 done — E7 (within-indirect cross-corpus) run 2026-06-02; see below.

## Headline

At the frozen MiniLM embedding, the **cross-family wall is geometrically real and wide — as
*supervised-linear separability*, not as unsupervised clustering.** Any two datasets are near-trivially
separable (PAD off-diagonal mean **1.698**, max 2.0), and **BIPIA (indirect) sits near-maximally far from
every direct/jailbreak/toxicity source (PAD 1.86–2.0)** — yet the global silhouette is ≈ 0
(by_dataset **0.004**, by_family **−0.001**). This is *consistent with* the prototype's
frozen-probe-at-chance cross-family result, and it sizes — but does **not** resolve — the OPEN question
(whether fair-tuned capacity climbs the wall; that remains the cross-family #1 experiment).

**E7 sharpens "cross-family" → "per-corpus."** Even the three *indirect* corpora (BIPIA, LLMail-Inject,
WAInjectBench) are as mutually separable (PAD **1.92–1.98**, within-indirect silhouette **0.095**) as
indirect is from direct — there is no cohesive "indirect family" cluster at this embedding. ⇒ **BIPIA is
one indirect dialect, not a representative indirect anchor**; the apparent family wall is a *sum of
per-corpus walls*, and a cross-family test must hold out **multiple** indirect corpora, not BIPIA alone.

## E2 — cross-dataset geometry (the main result)

`experiments/eda/CROSS_DATASET/cross_dataset_geometry.json` (15 datasets × 250 rows = 3,750):

| metric | value | reading |
|---|---|---|
| silhouette by_dataset / by_family / by_coarse | 0.004 / −0.001 / 0.014 | **not** blob-clustered by source (contrast BIPIA carriers: 0.197) |
| KMeans ARI vs family / dataset | 0.126 / 0.127 | unsupervised clustering only weakly recovers source |
| **PAD off-diagonal mean / min** | **1.698 / 0.672** | pairwise **near-trivially separable** (~92% linear acc avg) |
| **PAD: BIPIA vs each direct source** | **1.86 – 2.0** | indirect is **uniformly maximally far** from the direct cloud |

★ Insight — the structural nuance ─────────────────
The cross-family signal is **supervised-linear, not unsupervised-cluster**: a classifier easily
fingerprints the source (PAD high), but sources interleave in most directions (silhouette ≈ 0). For a
*trained* detector — which learns supervised directions — the high PAD is exactly what makes
cross-family transfer fail. This is the opposite character to the carrier wall (a dominant *cluster*
geometry, silhouette 0.197), and it explains *why* the prototype's frozen probe sat at chance
cross-family.
─────────────────────────────────────────────────

**Two design-relevant structures inside the direct cloud:**
1. **A redundant, near-duplicate sub-cluster** — `jackhhao↔shen_dan` PAD **0.672**, `promptshield↔xtram1`
   **0.80**, `guychuk↔promptshield` 0.94, `toxicchat↔xtram1` 0.96, `guychuk↔xtram1` 1.03. These
   jailbreak/direct sources share upstream provenance → **pooling them adds far less diversity than their
   row-count suggests.**
2. **`spml` is a genuine outlier** — PAD 1.94–2.0 vs *everything* (its System-Prompt+User-Prompt
   structure embeds distinctively) → the one direct source that adds real diversity.

## E4 — cross-dataset leakage (LODO contamination)

80 cross-dataset near-dup rows (TF-IDF cosine ≥ 0.9; **2.13%**). The critical pair:
- **`jackhhao ↔ shen_dan` = 45 near-dups** — effectively the same jailbreak source (corroborates their
  PAD 0.672). **Must be grouped, never split across train/test.**
- `guychuk↔promptshield` 10, `gentelbench↔jackhhao` 9, `shen_dan↔xtram1` 7 (smaller).
- **External (not in this HF set):** `InjecGuard/PIGuard` **bundles `BIPIA_text/code.json`** (acquisition
  deep-dive) → a must-exclude if InjecGuard is ever used against a BIPIA test.

## E1 / E3 / E5 / E6 — from existing artifacts (no new run needed)

- **E1 (universe).** 30-dataset candidate universe characterized (`docs/research/datasets/agent_index/`)
  + acquirability live-verified (`docs/planning/dataset-acquisition-deep-dive-2026-06.md`): only
  Harelix/PINT hard-unavailable; ~5 loadable-but-unlicensed.
- **E3 (label harmonization).** `configs/data/dataset_specs.yml` **is** the harmonization map — verified
  `feature_col(s)` + `label_col` + `label_map` per dataset (e.g. `jackhhao type→{benign:0,jailbreak:1}`,
  `shen_dan jailbreak:bool→{true:1}`, `spml feature_cols:[System Prompt,User Prompt]`). Pooling for a
  cross-family slate is a config exercise, not a research gap.
- **E5 (prevalence → AUROC-primary).** Prevalence varies wildly: ToxicChat ~7% positive
  (`class_balance` FAIL), BIPIA 83–94% positive, the controls all-benign. Confirms AUROC must be the
  primary metric universe-wide (the BIPIA lesson generalizes), AUPRC reported alongside.
- **E6 (obfuscation → Lane 1b candidates).** Invisible-char rates (`survey_summary.json`): **shen_dan
  1.05%** > guychuk 0.76% ≈ jackhhao 0.67% > deepset 0.55% > jayavibhav 0.3% ; PromptShield's card flags
  explicit unicode/obfuscated cases. → ranked char-injection-robustness material is ready.

## E7 — within-indirect cross-corpus (DONE)

`experiments/eda/CROSS_DATASET/within_indirect_e7.json` (`within_indirect_e7.py`; 250/corpus, seed 0,
attack-positive text; reuses the E2 `pad()`/`_load_bipia()`/MiniLM embedder, both scripts library-first).
*Do the other indirect corpora sit **with** BIPIA or **apart** from it?*

| pair (indirect ↔ indirect) | PAD | reading |
|---|---|---|
| BIPIA ↔ LLMail-Inject | **1.984** | as far apart as BIPIA↔direct |
| BIPIA ↔ WAInjectBench | **1.920** | as far apart as BIPIA↔direct |
| LLMail-Inject ↔ WAInjectBench | **1.944** | the two *non*-BIPIA indirect corpora are also far apart |
| within-indirect 3-way silhouette | **0.095** | no cohesive "indirect family" cluster |

**Verdict — BIPIA is one indirect *dialect*, not a representative indirect anchor.** The indirect↔indirect
PADs (1.92–1.98) are indistinguishable from the indirect↔direct baseline (1.864–2.0) — indirect corpora
are as separable *from each other* as from the direct cloud. So E2's "cross-family wall" is really a
**per-corpus** wall: corpus identity (driven by construction/provenance) dominates the frozen embedding;
*family* (direct vs indirect) is not itself a low-PAD axis. The three indirect corpora differ by
construction — BIPIA = synthetic attack-strings-in-contexts, LLMail = SaTML competition emails,
WAInjectBench = web-agent documents — and the embedding separates them accordingly.

*Loaders (E7):* LLMail-Inject = HF `microsoft/llmail-inject-challenge` streamed, text = `subject`+`body`
(all-attack). WAInjectBench = git clone (EDA-only, unlicensed); live layout encodes the label **by
directory** (`data/text/{malicious,benign}/*.jsonl`, each line `{"id","text"}`) — *not* the carded in-row
`{"text","label"}`; malicious pool 991 rows (250 sampled), benign 2,707. *Scope:* frozen MiniLM, 250/corpus,
PAD = 5-fold LR — same caveats as E2; says nothing about whether a *tuned* detector learns a
corpus-invariant injection feature (that is the OPEN capacity question, unchanged).

## What this determines — "what we can do"

1. **TRAIN side — favor diversity over count (the direct pool is redundant + leaky).** Keep `spml`
   (distinct), pick *one* of the `{jackhhao, shen_dan, xtram1, promptshield, guychuk, toxicchat}`
   near-duplicate cluster (or dedup across it), and **group jackhhao+shen_dan** to avoid LODO leakage.
   guychuk (464k) and PromptShield stay as primary clean-licensed anchors.
2. **TEST side — hold out *multiple* indirect corpora, not BIPIA alone (E7).** BIPIA is one indirect
   dialect (PAD ~1.95 from LLMail-Inject and WAInjectBench, indistinguishable from indirect↔direct), so a
   BIPIA-only OOD test measures transfer to *BIPIA*, not to the indirect family. Pool/stratify
   {BIPIA, LLMail-Inject, WAInjectBench} (+ InjecAgent/JBB as available) and report **per-corpus** as well
   as pooled — which is exactly the prototype's original multi-corpus pooled-OOD design (E7 *validates* it
   and cautions against narrowing to BIPIA).
3. **Cross-family #1 is worth running, and now well-motivated.** The frozen wall is wide+real per-corpus
   ⇒ a demanding test; geometry can't say whether *capacity* climbs it (that's the GPU experiment), but it
   confirms the wall is real at the frozen rung — not a fishing trip. **This is the sharpest OPEN item.**
4. **Lane 1b + benign-FPR slates are ready** (E6 ranking; OR-Bench/XSTest/NotInject).

## Reproduce
```
uv run python experiments/eda/cross_dataset_geometry.py --out experiments/eda/CROSS_DATASET --per-dataset 250
uv run python experiments/eda/within_indirect_e7.py   # E7: within-indirect (BIPIA/LLMail/WAInjectBench)
```
Metrics → `cross_dataset_geometry.json` (+ `within_indirect_e7.json`); figure → `cross_dataset_geometry.png`.
Reuses `configs/data/dataset_specs.yml` loaders + `eval_toolkit.embeddings.make_minilm_embedder`
(library-first; E7 imports `pad`/`_load_bipia`/`_sample_texts` from the E2 script).

## Scope guard
- Pre-modeling **geometry**, not a modeling result: it sizes the cross-family wall, it does not resolve capacity.
- Streaming/sampled (250/dataset); PAD = 5-fold LR proxy-A-distance; silhouette/ARI on the full embedding.
- No canonical record edited, nothing committed (user-led).
