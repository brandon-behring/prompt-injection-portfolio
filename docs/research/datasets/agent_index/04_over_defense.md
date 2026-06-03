# Over-defense / false-refusal controls

Benign-heavy or benign-by-construction sets used to measure **false positives / exaggerated refusal**. **Keep all of these out of any training split** — they exist precisely to detect over-conservative guardrails. Pairs with the [harness spec](../../planning/attack-type-lodo-harness-spec.md)'s benign-FPR metric.

### D1. bench-llm/or-bench — Cui et al. (2024)
- **Source:** https://huggingface.co/datasets/bench-llm/or-bench
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `category` (10 classes).
- **Size+License:** ~33.7 MB (82,333 rows total across 3 configs); `or-bench-80k` ~80,400; `or-bench-hard-1k` ~1,320; `or-bench-toxic` ~655; cc-by-4.0.
- **Tasks:** Seemingly-toxic-but-safe prompts for over-refusal. THREE configs: `or-bench-80k` (~80,400, full over-refusal set), `or-bench-hard-1k` (~1,320, hardest/multi-model-refused), `or-bench-toxic` (~655, genuinely toxic ⇒ SHOULD refuse; the control). Single split each. arXiv:2405.20947. Encoder-readiness: **eval-only** as shipped — prompts+category, no benign/comply binary on 80k/hard-1k; derivable into an over-refusal eval (80k+hard = should-comply vs toxic = should-refuse). Largest over-refusal set surveyed; complements NotInject (D2) + XSTest (D3).
- **Status:** Verified.
- **Soft tags:** family=over-defense-control · encoder_readiness=eval-only · study_relevance=high

### D2. NotInject — Li & Liu / InjecGuard·PIGuard (2024)
- **Source:** https://huggingface.co/datasets/leolee99/NotInject
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `word_list` (the injection-trigger words deliberately embedded), `category` (topic, **NOT** an attack-type label).
- **Size+License:** 339 rows (3 subsets × 113, by trigger-word count); mit.
- **Tasks:** NO positive class — **all 339 samples are BENIGN by construction**; `category` in {Common Queries, Technique Queries, Virtual Creation, Multilingual Queries}; 3 difficulty subsets (1/2/3 trigger words, 113 each); multilingual. arXiv:2410.22770; ACL 2025. **NOT a training set** — an **over-defense / false-positive-rate eval**: score a detector by how few of these benign prompts it flags. Pairs with the harness-spec benign-FPR metric. Model: leolee99/PIGuard.
- **Status:** Verified.
- **Soft tags:** family=over-defense-control · encoder_readiness=eval-only · study_relevance=high

### D3. natolambert/xstest-v2-copy — Röttger et al. (NAACL 2024)
- **Source:** https://huggingface.co/datasets/natolambert/xstest-v2-copy
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompts` subset: `id_v1`, `id_v2`, `type` (18 classes), `prompt`, `focus`, `note`; model subsets add `completion` + `annotation_1/2` + `agreement` + `final_label` (3 classes).
- **Size+License:** ~450 prompts × 6 subsets (~2.7k rows); 450 per subset; 6 subsets (prompts, gpt4, llama2new, llama2orig, mistralguard, mistralinstruct); cc-by-4.0.
- **Tasks:** 250 SAFE prompts (10 categories) + 200 UNSAFE contrast prompts that superficially resemble them; `type` (18 classes) encodes category. NOTE: UNSAFE types carry a `contrast_` prefix (`contrast_homonyms`, ...), SAFE types are BARE names (`homonyms`, `figurative_language`, ...) — no `safe_` prefix. Model subsets add graded `final_label` {1_full_compliance, 2_full_refusal, 3_partial_refusal}. ~56% safe / 44% unsafe by design (over-refusal probe). arXiv:2308.01263. Encoder-readiness: **eval-only** — too small to train; a held-out over-defense probe (pairs with NotInject D2). License cc-by-4.0 (prompts; model completions retain Meta/Mistral/OpenAI terms). Confirmed component of the ProtectAI deberta-v3-v2 training mixture (F3).
- **Status:** Verified.
- **Soft tags:** family=over-defense-control · encoder_readiness=eval-only · study_relevance=high

### D4. Prompt Injection Test (PINT) Benchmark — Lakera AI (2024)
- **Source:** https://github.com/lakeraai/pint-benchmark
- **Access:** credentialed (request from Lakera); auth_required: Y
- **Schema:** `text`, `label`, `category` (YAML schema expected by the harness; real data withheld).
- **Size+License:** 4,314 inputs (3,016 English / 1,298 non-English); MIT (harness/code) + **custom restrictions**: the labeled PINT dataset is NOT publicly distributed (anti-contamination).
- **Tasks:** **Contamination-avoidance non-public** (verbatim Lakera): *"The PINT Benchmark dataset is not publicly available in order to prevent the dilution of the PINT Benchmark from overfitting due to training on the inputs"* and *"Lakera Guard is not - and will never be - directly trained on any of the inputs in the PINT Benchmark dataset."* Categories: public/internal prompt injection, jailbreak, hard_negatives, chat, documents (approx mix: injections ~5%, jailbreaks ~1%, hard negatives ~21%, chat ~36%, documents ~36%); ~4,314 inputs, mostly benign by design. Encoder-readiness: **NOT encoder-ready / NOT for training** — held-out neutral eval only; repo ships the scoring harness + an EXAMPLE yaml, not the corpus. Request via Lakera.
- **Status:** Unverified (data deliberately withheld; harness verified).
- **Soft tags:** family=over-defense-control · encoder_readiness=eval-only · study_relevance=medium

### D5. AmazonScience/FalseReject — Amazon Science (2025)
- **Source:** https://huggingface.co/datasets/AmazonScience/FalseReject
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt` (no binary label — all-benign by construction); 44 topical categories.
- **Size+License:** ~15.8K rows (all benign); cc-by-nc-4.0.
- **Tasks:** Benign prompts deliberately **crafted to look unsafe** — the textbook over-refusal / false-positive probe. EDA-gate verdict (2026-06-03): leakage-clean; all-benign (no positive class). Research-role: a **benign-FPR / over-defense control** (same family as NotInject D2 / XSTest D3 / OR-Bench D1) — score a detector by how few of these benign prompts it flags. **Keep out of any training split.** Encoder-readiness: **eval-only** — `prompt` only, no benign/comply binary, derivable into an over-refusal eval. ⚠️ **NC license** ⇒ non-commercial research / eval-only.
- **Status:** Verified.
- **Soft tags:** family=over-defense-control · encoder_readiness=eval-only · study_relevance=medium

_5 entries._
