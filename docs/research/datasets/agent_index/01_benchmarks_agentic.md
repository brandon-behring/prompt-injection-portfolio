# Injection benchmarks & agentic harnesses

Attack-success / agent-environment benchmarks. Most are **not** drop-in `(text, label)`
corpora — they measure whether an injection succeeds in an agent loop — except **BIPIA**,
whose per-attack-type malicious strings make a labeled corpus directly derivable.

### A1. BIPIA — Microsoft (2023/2024)
- **Source:** https://github.com/microsoft/BIPIA
- **Access:** direct (git); auth_required: N
- **Schema:** attack JSON `{attack_type_name: [attack_string, ...]}` + per-domain context (Email/WebQA/TableQA/Summarization/CodeQA); card at benchmark/README.
- **Size+License:** text 15+15 types × ~5 strings, code 10+10 types × ~5; MIT (code) **+ custom restriction**: WebQA/Summarization context must be regenerated locally ("license issue").
- **Tasks:** **The direct input to [ADR-052](../../../decisions/ADR-052-attack-type-generalization.md) + the [attack-type-LODO harness spec](../../planning/attack-type-lodo-harness-spec.md).** Ships a **disjoint train/test attack-type split** — 15 text train types vs 15 test types, only "Language Translation" overlapping; obfuscation sub-family (substitution ciphers, base encoding, anagramming, …) is a clean technique slice. Encoder-readiness: **nearest to drop-in** — per-type malicious strings injected into benign carriers → derivable `(text, binary-label)` corpus; the disjoint split *is* the attack-type-LODO axis. ⚠️ ~75 strings/split → memorization risk.
- **Status:** Verified (license corrected to MIT — a "CC BY-SA" web snippet was unreliable).

### A2. InjecAgent — UIUC (2024)
- **Source:** https://github.com/uiuc-kang-lab/InjecAgent
- **Access:** direct; auth_required: N
- **Schema:** JSONL test cases (user_cases + attacker_cases_dh/ds + test_cases_dh/ds_{setting}).
- **Size+License:** 1,054 test cases (17 user tools, 62 attacker tools); MIT.
- **Tasks:** Indirect-injection benchmark for **tool-integrated agents**; two attack intents — direct harm (dh) + data exfiltration (ds). Measures ASR-valid/ASR-all over ReAct traces. Encoder-readiness: **needs adaptation** — all-attack, no paired benign set; injected attacker-tool prompts can be mined as malicious text but you must supply benign carriers.
- **Status:** Verified.

### A3. AgentDojo — ETH Zürich (2024)
- **Source:** https://github.com/ethz-spylab/agentdojo
- **Access:** direct; auth_required: N
- **Schema:** 4 task suites (workspace/email, banking, travel, slack); user_tasks + injection_tasks; environment state + tool defs as Python objects.
- **Size+License:** 97 benign tasks + 629 security test cases; MIT.
- **Tasks:** Dynamic agent environment evaluating injection attacks **and** benign-task utility under attack. Organized by injection-task + attack strategy (e.g. `important_instructions`), not per-string type. Encoder-readiness: **not a static corpus** — heavy adaptation needed; strong for agent-level eval, weak as encoder training data.
- **Status:** Verified.

### A4. LLMail-Inject — Microsoft (2025)
- **Source:** https://huggingface.co/datasets/microsoft/llmail-inject-challenge
- **Access:** hf datasets; auth_required: N
- **Schema:** RowKey, subject, body, objectives (13 classes), scenario (40 classes), success flags (email.retrieved / defense.undetected / exfil.sent / …).
- **Size+License:** ~462k rows (208,095 unique attack prompts; 839 participants); MIT.
- **Tasks:** Largest **real-world adaptive-attack** corpus here (SaTML 2025 challenge). Encoder-readiness: **partial** — subject+body are genuine adversarial text and `defense.undetected` is a usable binary-ish target, but all rows are attacks (no benign emails) → add benign carriers. Excellent hard-positive pool for detector-robustness work.
- **Status:** Verified.

### A5. Agent Security Bench (ASB) — AGI-Research (2024)
- **Source:** https://github.com/agiresearch/ASB
- **Access:** direct; auth_required: N
- **Schema:** scenario configs + agent/tool defs + attack/defense modules (code+config), not a flat table.
- **Size+License:** 10 scenarios, 10 agents, 400+ tools, 27 attack/defense methods, 13 LLM backbones; MIT.
- **Tasks:** Formalizes 5 attack families — Direct (DPI) / Observation (OPI) Prompt Injection, Memory Poisoning, Plan-of-Thought Backdoor, Mixed. Attack-success-rate framework (peak ASR ~84%). Encoder-readiness: **not drop-in** — labels at method/scenario level; substantial adaptation to extract labeled text.
- **Status:** Verified.

_5 entries._
