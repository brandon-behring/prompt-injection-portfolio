# Competition, real-world & web-agent sets

Large human-generated competition logs (direct injection) plus the genuinely
**indirect / in-the-wild / web-agent** sources — the latter are the gap the dossier
most wants filled.

### D1. hackaprompt/hackaprompt-dataset — Schulhoff et al. (2023)
- **Source:** https://huggingface.co/datasets/hackaprompt/hackaprompt-dataset
- **Access:** hf datasets; auth_required: N
- **Schema:** `level`, `user_input`, `prompt`, `completion`, `model`, `correct`, `score`, `dataset`, `timestamp`.
- **Size+License:** ~600,000 prompts (paper; exact count not on card); MIT (card; companion paper arXiv:2311.16119 is CC BY 4.0).
- **Tasks:** Global prompt-hacking competition (EMNLP 2023); per-row `correct` boolean + 10 difficulty `level`s. Attack-type taxonomy lives in the **paper**, not a column. **Direct** injection / jailbreak (single-turn user-vs-system), not indirect/RAG. Encoder-readiness: **needs adaptation** — `(user_input, correct)` is a weak attack-success signal with no clean injection-type label; best as a large adversarial-prompt source.
- **Status:** Verified.

### D2. Tensor Trust — Toyer et al. (2023)
- **Source:** https://github.com/HumanCompatibleAI/tensor-trust-data
- **Access:** direct; auth_required: N
- **Schema:** documented in the bundled "Using the Tensor Trust dataset.ipynb"; dirs raw-data/, benchmarks/, detecting-extractions/.
- **Size+License:** ~172,000 entries (~126k attacks + ~46k defenses); **license: unknown** (no LICENSE in repo).
- **Tasks:** Largest human-generated adversarial set from an online attack/defense game (arXiv:2311.01011); two interpretable families — prompt **extraction** + **hijacking** — plus defense prompts (natural malicious-vs-benign contrast). **Direct** injection in a game framing, not indirect. Encoder-readiness: **partial** — the extraction-detection benchmark is closest to `(text,label)`; needs the notebook for column meanings. ⚠️ License unknown — don't redistribute/publish trained artifacts without confirming terms.
- **Status:** Verified (data) / license unknown.

### D3. WAInjectBench — Liu et al. (2025)
- **Source:** https://github.com/Norrrrrrr-lyn/WAInjectBench
- **Access:** direct; auth_required: N
- **Schema:** text JSONL `{"text","label"}` (1=malicious/0=benign); image JSONL `{"path","label"}`.
- **Size+License:** 8 text + 7 image attack types, 4 benign text categories (totals not on README — count after clone); **license: unknown**.
- **Tasks:** **Web-agent / indirect-injection** detection benchmark (arXiv:2510.01354) with built-in benign/malicious balance + fine-grained attack-type stratification. Encoder-readiness: **drop-in for the text modality** (JSONL `{"text","label"}`) — the most directly encoder-usable web-agent/indirect detection set found. Image modality separate; confirm license before publishing.
- **Status:** Verified.

### D4. InjecGuard / PIGuard training corpus — Li & Liu (2024)
- **Source:** https://github.com/SaFoLab-WISC/InjecGuard
- **Access:** direct; auth_required: N
- **Schema:** binary benign vs malicious-injection `(text, label)` (training); 144-sample validation set.
- **Size+License:** training set aggregated from ~20 open-source datasets + LLM-augmented data (count after clone); MIT.
- **Tasks:** Purpose-built guardrail training corpus (arXiv:2410.22770, ACL 2025) that **aggregates BIPIA (indirect) + Wildguard-Benign + PINT** among ~20 sources — so it carries some indirect content (unlike HackAPrompt/TensorTrust, which are direct-only). Companion = NotInject (C1). Encoder-readiness: **drop-in** `(text,label)` in PIGuard/datasets; verify exact composition after clone.
- **Status:** Verified.

### D5. Indirect Prompt Injection in the Wild — Khodayari et al. (2026)
- **Source:** https://arxiv.org/abs/2604.27202
- **Access:** direct (paper only); auth_required: N
- **Schema:** unknown (no downloadable dataset located as of 2026-05-27).
- **Size+License:** 15,387 validated indirect-injection instances across 11,700 pages (paper counts; **corpus NOT released**); license unknown.
- **Tasks:** The only genuinely **in-the-wild indirect** corpus surveyed — categorizes instances by recurring lexical templates (a few drive ~95%), objective (offensive vs defensive), and visibility (~87% non-visible, in HTML headers/comments/metadata). arXiv id **verified genuine** (April-2026; do **not** conflate with arXiv:2601.07072 "Overcoming the Retrieval Barrier…", USENIX Sec '26). Encoder-readiness: **not released** as `(text,label)` yet — citable as evidence; re-check for a data link in a later revision.
- **Status:** Unverified (dataset unreleased; paper/id verified).

_5 entries._
