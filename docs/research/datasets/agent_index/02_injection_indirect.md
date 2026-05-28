# Injection — indirect family

Indirect prompt-injection: the attack rides in a **retrieved / tool-returned / observed** document the model ingests (email, web page, RAG corpus, tool output) rather than in the user's own message. This is the dossier's gap — most public injection corpora are direct. Includes the only **disjoint attack-type train/test split** surveyed (BIPIA) plus the only genuine **in-the-wild indirect** corpus (Khodayari et al.; unreleased at verification time).

### B1. BIPIA — Microsoft (2023/2024)
- **Source:** https://github.com/microsoft/BIPIA
- **Access:** direct; auth_required: N
- **Schema:** attack JSON `{attack_type_name: [attack_string, ...]}` + per-domain context data (Email/WebQA/TableQA/Summarization/CodeQA); card at `benchmark/README`.
- **Size+License:** text 15+15 attack types × ~5 strings, code 10+10 types × ~5; paired with Email/WebQA/TableQA/Summarization/CodeQA contexts (~150 text + ~100 code attack strings × context tasks ⇒ eval instances). License: MIT (code, Microsoft Corporation) + **custom restrictions**: benchmark/README notes some context data (WebQA, Summarization) cannot be redistributed *"due to the license issue"* and must be regenerated locally.
- **Tasks:** **The direct input to [ADR-052](../../../decisions/ADR-052-attack-type-generalization.md) + the [attack-type-LODO harness spec](../../planning/attack-type-lodo-harness-spec.md).** Ships a **disjoint train/test attack-type split** — 15 text train types vs 15 test types, only "Language Translation" overlapping (intentional, for unseen-attack-type generalization); obfuscation sub-family (Alphanumeric/Homophonic Substitution, Anagramming, Substitution Ciphers, Base Encoding, ...) is a clean technique slice. Code: 10 train vs 10 disjoint test types. arXiv:2312.14197; KDD 2025. Encoder-readiness: **nearest to drop-in** — clean per-type malicious strings + benign carriers ⇒ a derivable `(text, binary-label)` corpus; the disjoint type split is exactly the attack-type-LODO axis. CAVEAT: small diversity (~75 strings/split ⇒ memorization risk). No official microsoft-org HF mirror yet.
- **Status:** Verified.
- **Soft tags:** family=injection-indirect · encoder_readiness=derivable · study_relevance=high

### B2. Indirect Prompt Injection in the Wild — Khodayari et al. (2026)
- **Source:** https://arxiv.org/abs/2604.27202
- **Access:** direct (paper only); auth_required: N
- **Schema:** unknown (no downloadable dataset located as of 2026-05-27).
- **Size+License:** 15,387 validated indirect-injection instances across 11,700 pages (paper counts; **corpus NOT released**); license: unknown.
- **Tasks:** The only genuinely **in-the-wild indirect** corpus surveyed — categorizes instances by recurring lexical **templates** (a small set drives ~95%), by objective (offensive vs defensive), and by visibility (~87% non-visible / in HTML headers/comments/metadata). arXiv id **verified genuine** (April-2026 submission; corroborated across arxiv + alphaXiv + cs.CR feed) — do **NOT** confuse with arXiv:2601.07072 *"Overcoming the Retrieval Barrier: Indirect Prompt Injection in the Wild"* (USENIX Security '26, Chang et al.). Encoder-readiness: **not released** as `(text,label)` at verification time (no data-availability statement / repo found). Citable as evidence; re-check for a data link in a later revision before relying on it.
- **Status:** Unverified (dataset unreleased; paper/id verified).
- **Soft tags:** family=injection-indirect · encoder_readiness=pointer · study_relevance=high

### B3. LLMail-Inject — Microsoft (2025)
- **Source:** https://huggingface.co/datasets/microsoft/llmail-inject-challenge
- **Access:** hf datasets; auth_required: N
- **Schema:** `RowKey`, `Timestamp`, `subject`, `body`, `completed_time`, `job_id`, `objectives` (stringclasses 13 — a JSON-string column whose values are combinations of 5 nested success flags `email.retrieved` / `defense.undetected` / `exfil.sent` / `exfil.destination` / `exfil.content`), `output`, `scenario` (stringclasses 40 = unique scenario×defense×LLM **levels**; only **4 underlying scenarios**), `scheduled_time`, `started_time`, `team_id`. NOTE the success flags are NESTED inside the `objectives` JSON — not separate top-level columns.
- **Size+License:** ~462k rows (Phase1 ~371k + Phase2 ~90.9k); 208,095 unique attack prompts; MIT.
- **Tasks:** Largest **real-world adaptive-attack** corpus surveyed (SaTML 2025 competition; 839 participants). Labeled by `objectives` (13 distinct JSON-string flag combinations) + `scenario` (40 distinct level-strings); per-submission success parsed out of the `objectives` JSON (`defense.undetected` is a usable detector target). Heavily attack-skewed — 208k+ adaptive ATTACK submissions; the signal is which attacks BYPASS which defense, not benign/malicious balance. arXiv:2506.09956. Encoder-readiness: **partial** — `subject+body` are real adversarial text and `defense.undetected` is a binary-ish target, but ALL rows are attacks (no benign emails) ⇒ add benign carriers for a balanced classifier. Excellent hard-positive pool for detector robustness.
- **Status:** Verified.
- **Soft tags:** family=injection-indirect · encoder_readiness=derivable · study_relevance=high

### B4. WAInjectBench — Liu et al. (2025)
- **Source:** https://github.com/Norrrrrrr-lyn/WAInjectBench
- **Access:** direct; auth_required: N
- **Schema:** text JSONL `{"text", "label"}`; image JSONL `{"path", "label"}`.
- **Size+License:** 6 attack types × 2 modalities (text + image); 8 text attack types + 4 benign text categories; totals not aggregated on README — count from JSONL after clone; **license: unknown**.
- **Tasks:** **Web-agent / indirect-injection** detection benchmark (arXiv:2510.01354) with binary label (1=malicious / 0=benign), fine-grained attack-type stratification (8 text + 7 image attack types) + 4 benign text categories. Both malicious and benign provided (built-in balance) but README gives no totals — count post-download. Encoder-readiness: **drop-in for the text modality** — shipped as JSONL `{"text","label"}`; the most directly encoder-usable web-agent/indirect detection set found. Image modality separate. License unconfirmed.
- **Status:** Verified.
- **Soft tags:** family=injection-indirect · encoder_readiness=drop-in · study_relevance=high

### B5. WASP — Evtimov et al. (2025)
- **Source:** https://github.com/facebookresearch/wasp
- **Access:** direct; auth_required: N
- **Schema:** n/a — agent environment (web-app state, tool defs, attacker goals, harness, eval scripts).
- **Size+License:** executable web-agent environment (Docker); not a `(text,label)` corpus. Attacker-goal/user-goal configs + injection formats; counts not on the repo landing page (see paper). License: CC-BY-NC-4.0 (majority); VisualWebArena = MIT; Claude computer-use demo code = separate terms.
- **Tasks:** Realistic end-to-end **executable web-agent environment** (sandboxed GitLab + Reddit in Docker) + attacker-goal/user-goal config framework + agent harness (GPT-4o(-mini), Claude-3.5/3.7; accessibility-tree / set-of-marks scaffolding). Measures whether a web agent is hijacked by an injected instruction (ASR), not text balance; exact goal/scenario counts not on the landing page (paper arXiv:2504.18575 has them). Encoder-readiness: **adaptation-heavy** — to mine a classifier corpus you must run the env + extract injected-vs-benign web content; no shipped labeled strings. ⚠️ Majority CC-BY-NC-4.0 (non-commercial); public repo (clone needs no auth; running needs your own API keys). bibkey corrected liao→evtimov (first author) 2026-05-27.
- **Status:** Verified.
- **Soft tags:** family=injection-indirect · encoder_readiness=adaptation-heavy · study_relevance=medium

_5 entries._
