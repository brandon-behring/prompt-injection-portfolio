# Injection — direct family

Direct prompt-injection: attacker text lives in the **user turn** (or user-controlled field), not in a retrieved/tool-returned document. Most are drop-in `(text, label)` corpora; a few are large adversarial competition logs that need adaptation. **License watch:** `xTRam1`, both `jayavibhav` sets, and Tensor Trust are license-undisclosed — clear before publishing any trained artifact. **Citation watch:** `xTRam1` is mismatched (wrong arXiv on card).

### A1. deepset/prompt-injections — deepset (2023)
- **Source:** https://huggingface.co/datasets/deepset/prompt-injections
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 0/1).
- **Size+License:** 662 rows (546 train / 116 test), ~0.5 MB; apache-2.0.
- **Tasks:** Canonical small bilingual (DE+EN) injection set; label 1 = injection. Encoder-readiness: **drop-in** with a predefined split — ideal smoke-test, too small to train alone. Lineage: JasperLS/prompt-injections.
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=high

### A2. guychuk/benign-malicious-prompt-classification — guychuk (2024)
- **Source:** https://huggingface.co/datasets/guychuk/benign-malicious-prompt-classification
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `label` (ClassLabel 2-class 0/1).
- **Size+License:** 464,470 rows (single train split, no predefined test), ~186 MB; apache-2.0.
- **Tasks:** Largest single-file binary **injection-intent** corpus surveyed. CRITICAL labeling nuance (verbatim card): malicious only if *"an attemp to manipulate"* — a harmful-but-direct question ("how to create a bomb") is labeled BENIGN. So this is a manipulation/injection-intent label, **not** a harmful-content/toxicity label (aligns with injection detection). Encoder-readiness: **drop-in** `(prompt,label)` — strong primary-training candidate; supply your own test split. Provenance undocumented (no paper/source on card) — flag for data-provenance.
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=high

### A3. PromptShield (hendzh/PromptShield) — Jacob et al. (2025)
- **Source:** https://huggingface.co/datasets/hendzh/PromptShield
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `label` (int64 0/1), `lang`.
- **Size+License:** 43,425 rows (train 18.9k / validation 1k / test 23.5k), ~31.2 MB; apache-2.0.
- **Tasks:** Deployment-detection corpus from arXiv:2501.15145 (UC Berkeley). `prompt` holds full structured LLM input (instructions+inputs+delimiters, lengths 18–31.1k); examples include both direct ("ignore previous instructions") and indirect/obfuscated (unicode, context-injection) cases. Note the **test split is larger than train** by design. Encoder-readiness: **drop-in** `(prompt,label)` with native train/val/test — directly ModernBERT-usable.
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=high

### A4. reshabhs/SPML_Chatbot_Prompt_Injection — reshabhs (2024)
- **Source:** https://huggingface.co/datasets/reshabhs/SPML_Chatbot_Prompt_Injection
- **Access:** hf datasets; auth_required: N
- **Schema:** `System Prompt`, `User Prompt`, `Prompt injection` (0/1), `Degree`, `Source`.
- **Size+License:** 16,012 rows (single train split, no test), ~40 MB; mit.
- **Tasks:** Captures **system-vs-user** attack structure + injection severity (`Degree`). Encoder-readiness: **needs format work** — select/concatenate System+User as text, map `Prompt injection`→label, supply your own split. Assoc. arXiv:2402.11755. English.
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=derivable · study_relevance=high

### A5. Tensor Trust — Toyer et al. (2023)
- **Source:** https://github.com/HumanCompatibleAI/tensor-trust-data
- **Access:** direct; auth_required: N
- **Schema:** documented in the bundled "Using the Tensor Trust dataset.ipynb"; dirs raw-data/, benchmarks/, detecting-extractions/.
- **Size+License:** ~172,000 entries (~126k prompt-injection attacks + ~46k defense prompts); **license: unknown** (no LICENSE in repo).
- **Tasks:** Largest human-generated adversarial set from an online attack/defense game (arXiv:2311.01011); two interpretable families — prompt **extraction** + **hijacking** — plus defense prompts (natural malicious-vs-benign contrast). **Direct** injection in a game framing, not indirect/web/RAG. Encoder-readiness: **partial** — the extraction-detection benchmark is closest to `(text,label)`; column meanings need the bundled notebook. ⚠️ License unknown — do not redistribute/train-and-publish without confirming terms.
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=derivable · study_relevance=high

### A6. hackaprompt/hackaprompt-dataset — Schulhoff et al. (2023)
- **Source:** https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset
- **Access:** hf datasets; auth_required: N
- **Schema:** `level`, `user_input`, `prompt`, `completion`, `model`, `expected_completion`, `correct`, `score`, `dataset`, `timestamp`.
- **Size+License:** ~600,000 prompts across GPT-3/ChatGPT/FlanT5-XXL (paper headline; exact count not on card), ~150 MB; MIT (dataset card; companion paper arXiv:2311.16119 is CC BY 4.0 — different artifact).
- **Tasks:** Global prompt-hacking competition (EMNLP 2023); per-row `correct` boolean (attack succeeded) + 10 difficulty `level`s + `model`. Attack-type taxonomy lives in the **paper**, not a column. **Direct** injection / jailbreak (single-turn user-vs-system), not indirect/RAG. Encoder-readiness: **needs adaptation** — `(user_input, correct)` is a weak attack-success signal with no clean injection-type label; best as a large adversarial-prompt source, not a drop-in `(text,label)` set.
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=adaptation-heavy · study_relevance=medium

### A7. Harelix/Prompt-Injection-Mixed-Techniques-2024 — Harelix (2024)
- **Source:** https://huggingface.co/datasets/Harelix/Prompt-Injection-Mixed-Techniques-2024
- **Access:** hf datasets; auth_required: N
- **Schema:** text + label (column name + label type NOT page-confirmed — see notes), ~1.17k rows.
- **Size+License:** 1,174 rows (single train split); apache-2.0.
- **Tasks:** A named component of the ProtectAI deberta-v3 v2 mixture (F3). Label schema reported as 3-class {0 benign, 1 prompt-injection, 2 direct harmful-request} — **NOT page-confirmed** (HF page returned HTTP 401 at gather time; facts from web-search snippets, not direct read). Encoder-readiness: **drop-in** `(text,label)` once schema is confirmed (collapse 2→1 for binary). Re-fetch via HF API/datasets lib to lock columns + label semantics before any training use.
- **Status:** Unverified (HF page 401 at gather; license corroborated by 2 search results).
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=medium

### A8. jayavibhav/prompt-injection — jayavibhav (2024)
- **Source:** https://huggingface.co/datasets/jayavibhav/prompt-injection
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 0/1).
- **Size+License:** 327,154 rows (train 262k / test 65.4k), ~327k rows; **license: unknown**.
- **Tasks:** Largest binary set surveyed; balance not stated; English. Strong **primary training-corpus candidate**. Encoder-readiness: **drop-in** `(text,label)` with split. ⚠️ License **undisclosed**; provenance undocumented (empty card, likely synthetic/aggregated) — clear before publishing a trained model.
- **Status:** Verified (license unknown).
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=medium

### A9. jayavibhav/prompt-injection-safety — jayavibhav (2024)
- **Source:** https://huggingface.co/datasets/jayavibhav/prompt-injection-safety
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 multiclass {0,1,2}).
- **Size+License:** 60,000 rows (train 50k / test 10k), ~13.3 MB; **license: unknown**.
- **Tasks:** 3-class safety variant (classes not explicitly named on card — appears benign / injection / a third safety class). Balance not stated; English. Encoder-readiness: **drop-in** `(text,label)` with split, but confirm the 3-class meaning before training (collapse to binary for an injection/benign head). ⚠️ License **undisclosed**.
- **Status:** Verified (license unknown).
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=medium

### A10. Open-Prompt-Injection — Liu et al. (USENIX Security 2024)
- **Source:** https://github.com/liu00222/Open-Prompt-Injection
- **Access:** direct; auth_required: N
- **Schema:** per-task config JSONs in `configs/task_configs/` (not a unified `text,label` schema).
- **Size+License:** framework over 7 NLP-task datasets (loaded at runtime); 5 attacks × 10 defenses × 10 LLMs; MIT.
- **Tasks:** NOT a labeled `(text,label)` corpus — a benchmark **framework** that injects attack instructions into 7 standard NLP tasks (MRPC dup-sentence, Jfleg grammar, HSOL hate, RTE NLI, SST2 sentiment, SMS-Spam, Gigaword summ; live `configs/task_configs/` holds 9 — adds compromise + math500). Formalizes 5 attacks (naive / escape / context-ignoring / fake-completion / combined) × 10 defenses × 10 LLMs. arXiv:2310.12815, USENIX Sec'24. Encoder-readiness: **derivable** — run the framework to emit (clean vs injected) pairs, then label; task data pulled from HF on load (API keys only for LLM targets, not data).
- **Status:** Verified.
- **Soft tags:** family=injection-direct · encoder_readiness=derivable · study_relevance=medium

### A11. xTRam1/safe-guard-prompt-injection — xTRam1 (2024)
- **Source:** https://huggingface.co/datasets/xTRam1/safe-guard-prompt-injection
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 0=safe / 1=prompt-injection).
- **Size+License:** 10,296 rows (train 8,240 / test 2,056), ~70/30, ~5 MB; **license: unknown**.
- **Tasks:** Good mid-size binary training set. Encoder-readiness: **drop-in** `(text,label)` with split. ⚠️ **Flagged mismatched**: license undisclosed AND the card cites arXiv:2402.13064 which is the unrelated *"Generalized Instruction Tuning (GLAN)"* paper — do not propagate that citation; verify provenance before publishing a trained model.
- **Status:** Mismatched (citation/license).
- **Soft tags:** family=injection-direct · encoder_readiness=drop-in · study_relevance=medium

_11 entries._
