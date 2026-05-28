# EDA design — what EDA *means* for prompt-injection detection datasets

> **Status:** DRAFT foundation (2026-05-27) — to refine collaboratively. The domain-grounded design of the analyses + visualizations we run **before** modeling, so dataset quality honestly bounds the research. Companion to `prototype-postmortem.md` (the *why* — the predecessor's no-EDA failure) and the `eval_toolkit.eda` layer (the *how*). Method citations live in the build-time docstrings.

## Thesis

Generic EDA asks *"is the data clean and balanced enough to model?"* — necessary but **radically insufficient** here, and our own predecessor is the proof: it did careful dedup/leakage/balance checks and still hit the OOD wall, recovering the lexical-shortcut mechanism only as *post-hoc interpretation*. EDA for prompt-injection detection means **pre-registering what the data can support**, by *measuring* — before any model — the four properties discovered too late:

1. **The positive class is heterogeneous.** `label=1` silently unions *direct* / *indirect* / *jailbreak* / *benign-but-triggering*. Our training pool sits in **one corner** of the (intent × technique × channel) cube — direct × hijack × user-turn — while the OOD slate sits in the **opposite** corners (indirect, jailbreak). That mismatch *is* the OOD wall, and it's knowable with **zero modeling**.
2. **The lexical signal is separable from attack semantics.** Surface markers ("ignore previous instructions") win in-distribution and collapse OOD.
3. **Hard benign negatives** (NotInject) are injection-shaped and **eval-only** → the model never trains on one → it's *built* to false-positive.
4. **The train→test shift is *designed*** (attack-type / carrier / direct→indirect) → EDA must **quantify** the shift, not minimize it.

## Why PI data is special (8 traits)
1. **Adversarial/crafted** — not i.i.d.; an arms race; the dangerous examples are made to look benign (or vice-versa).
2. **Heterogeneous positive class** — the intent × technique × channel cube (above).
3. **A real attack taxonomy with a *technique* axis** — BIPIA's 15/15 disjoint attack-types + a clean obfuscation sub-family; technique determines surface form (base64 vs roleplay look opposite).
4. **Obfuscation / encoding / invisible-Unicode** — a *seen-text ≠ scored-text* hazard: zero-width/tag-block chars + encoded blobs silently corrupt any length/n-gram/embedding stat → detecting them is an **integrity prerequisite**, not just coverage.
5. **Carrier structure (indirect)** — the unit is `(carrier, payload, position)`; "lost in the middle" means position matters; a flat `(text,label)` table can't express it.
6. **Generalize-across-types is the goal** — shift is a *designed feature*; quantify its magnitude/structure as the prior probability any model clears the gap.
7. **Shortcut-proneness** — direct positives are saturated with formulaic markers; a lexical classifier hits ~0.99 in-pool and collapses OOD.
8. **Cross-dataset recycling + reference-scorer-training overlap** — PI corpora are heavily re-aggregated (InjecGuard⊇BIPIA; ProtectAI's recipe ⊇ jackhhao/xstest) → contamination + the PI-specific *reference-scorer-trained-on-eval* leakage type.

## Analysis catalog — Question → Method → Decision it gates
**A. Label composition** — *A1* positive cube decomposition (channel×intent×technique per source/split) → is the headline "PI detection" or actually cross-channel transfer? · *A2* negative easy-vs-hard (trigger-word load) → are hard negatives train-present or eval-only?
**B. Taxonomy/technique** — *B1* per-split technique histograms → per-type N / CI policy / memorization risk · *B2* obfuscation/encoding/unicode prevalence → **integrity gate** (normalize before any stat) + encoding-coverage gap · *B3* multilingual composition → language as confound / scope.
**C. Shortcut/confound** — *C1* log-odds (Monroe informative-Dirichlet) per class/type → what the shortcuts are, are they source-specific · *C2* partial-input / structural-only competency baselines (length-only, char-n-gram, BoW) → the **true floor**: is the label recoverable without semantics? · *C3* length/structure confounds by class/type (effect size).
**D. Duplication/contamination** — *D1* dedup + minimal-pair preservation (built) · *D2* **all-pairs** cross-dataset contamination matrix → is an "OOD" slate actually contaminated? · *D3* reference-scorer training-overlap → are ProtectAI numbers admissible or `suspected_contamination`?
**E. Shift** — *E1* per-fold **proxy-A-distance** + MMD (TF-IDF + embedding) → generalization-plausibility, *predicts* the wall per fold · *E2* embedding geometry (UMAP + silhouette/ARI) → does variation track label or source/type/carrier?
**F. Hard-neg/diversity** — *F1* NotInject characterization (which triggers drive over-defense) · *F2* BIPIA per-type diversity (within-type cosine) → is attack-type-LODO meaningful at ~75 strings/split?

## Visualization catalog (with pitfalls)
- **V1** attack-type count bars (train vs test) + **disjointness matrix** — annotate the ~5/type sparsity.
- **V2** cube-occupancy heatmap (source × channel×intent×technique) — mark native-vs-inferred tags.
- **V3** carrier × attack-type heatmap (BIPIA) — carrier-shift ≠ type-shift.
- **V4** UMAP 4-panel (label / attack-type / carrier / source) — **UMAP distances/sizes aren't metric**; pair with silhouette/ARI + PAD, never eyeball.
- **V5** per-class & per-type log-odds scatter — threshold on min count (rare-token noise).
- **V6** length violins/ECDF by class/type — a gap ≠ causal shortcut; confirm with C2.
- **V7** obfuscation/encoding/unicode prevalence bars + raw-vs-NFKC length delta — show detector precision (code carriers have legit base64).
- **V8** cross-dataset overlap matrix (exact + cosine) — separate exact from near.
- **V9** per-fold PAD/MMD bars + chance line — report both feature spaces.
- **V10** **reference-scorer score-distributions per slice** — *the literal figure the postmortem says was missing*; single-class slices → show **distributions, not AUROC**.
- **V11** dataset cartography (variability × confidence) — needs one training run (early-modeling, not pre-modeling).

## Scope tiers — R = reusable (`eval_toolkit.eda`) · D = dataset-specific (portfolio notebook)
- **Job-1 integrity** (built, held): counts/balance/length/dedup/leakage **[R]** + **fold B2 obfuscation in as an integrity prerequisite [R]**.
- **Job-2 shortcut:** C1 `log_odds` **[R]**, C2 `competency_baselines` **[R]**; V5/V6 **[D]**.
- **Job-3 shift:** E1 `shift` (proxy_a_distance, mmd) **[R]**, E2 embedding-map **[R]**; B1, V4, V9 **[D]**.
- **Domain additions:** B2 `obfuscation` **[R]**, B3 `language_profile` **[R]**, A1 cube (tagger scaffold **[R]** + taxonomy map **[D]**), V3 carrier **[D]** (needs a carrier+position-preserving BIPIA loader — the prototype's `loaders.py:527-562` collapses it), D3 ref-scorer-overlap **[D]**, F1/F2 **[D]**, V10 **[D]**, V11 `cartography` **[R]**.

## Highest-value — the analyses that would have *predicted* the wall pre-GPU
**V10** ref-scorer score-distributions · **A1** positive-class cube · **E1** per-fold proxy-A-distance · **B2** obfuscation integrity-prereq · **D2/D3** contamination + ref-scorer overlap · **C2** competency baselines.

## Build order (proposed)
1. **Fold B2 obfuscation-detection into the Job-1 integrity gate** (cheap; blocks corrupted stats).
2. **First Job-2/3 deliverables: V10 + A1** (directly target the predecessor's mechanism).
3. **E1 per-fold proxy-A-distance = the go/no-go** before any training rung.
4. **Fix the BIPIA loader** to preserve carrier + payload position.
- Durable output = `eval_toolkit.eda` primitives (`log_odds`, `competency_baselines`, `obfuscation`, `shift`, `cartography`, `language_profile`, embedding-map); portfolio-specific = BIPIA carrier/taxonomy views, NotInject characterization, the V10 ref-scorer plots.

## Standards note
The `eda` code follows eval-toolkit `STYLE.md` (frozen `slots=True` dataclasses, stdlib `raise`, `logging`, NumPy docstrings, immutability, report-type naming). **One fix pending:** drop `audit_dataset(..., seed=...)` — `rng` is the §3a canonical (SPEC 7) and the integrity gate is deterministic anyway (§1.5 anti-overengineering). Fold into the next eda iteration.

## Open questions to refine
- Which analyses to prioritize for the first *real* build beyond the integrity gate?
- Per-type CI policy given BIPIA's ~75 strings/split — descriptive-only, or augment diversity before the attack-type-LODO experiment?
- Scope of the carrier+position-preserving loader (which BIPIA scenarios first: email/code/table).
- A1 taxonomy mapping: adopt the Lasso intent×technique categories, or our own?
