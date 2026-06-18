# Agentic-trajectory family

End-to-end agent-environment benchmarks. These measure whether an injection succeeds across an **agent loop** (tool use, ReAct traces, planning) — they report **ASR**, not classification metrics. None are drop-in `(text,label)` corpora; all need substantial adaptation to mine labeled text. Strong for agent-level eval; weak as encoder training data.

### E1. AgentDojo — Debenedetti et al. (NeurIPS 2024 D&B)
- **Source:** https://github.com/ethz-spylab/agentdojo
- **Access:** direct; auth_required: N
- **Schema:** task suites: `user_tasks` + `injection_tasks`; environment state + tool defs (Python objects).
- **Size+License:** 97 tasks + 629 security test cases across 4 suites (workspace/email, banking, travel, slack); MIT.
- **Tasks:** Dynamic agent environment evaluating injection attacks **and** benign-task utility under attack. Organized by injection-task + attack strategy (e.g. `important_instructions`), not `(text,label)` per-string categories. 97 benign user tasks vs 629 security test cases; benign-utility AND under-attack performance both measured. arXiv:2406.13352. Encoder-readiness: **NOT a drop-in static corpus** — dynamic agent environment; heavy adaptation needed to render payloads vs benign tool outputs into text. Strong for agent-level eval, weak as encoder training data.
- **Status:** Verified.
- **Soft tags:** family=agentic-trajectory · encoder_readiness=adaptation-heavy · study_relevance=medium

### E2. Agent Security Bench (ASB) — Zhang et al. (ICLR 2025)
- **Source:** https://github.com/agiresearch/ASB
- **Access:** direct; auth_required: N
- **Schema:** scenario configs + agent/tool defs + attack/defense modules (code+config); combinatorial (scenarios × agents × attacks), not a flat row count.
- **Size+License:** 10 scenarios, 10 agents, 400+ tools, 27 attack/defense methods, 13 LLM backbones; MIT.
- **Tasks:** Formalizes 5 attack families — Direct Prompt Injection (DPI), Observation Prompt Injection (OPI), Memory Poisoning, Plan-of-Thought (PoT) Backdoor, Mixed — over 27 methods; labels at method/scenario level, not per-string. Attack-success-rate framework (peak ASR ~84%); not benign/malicious balanced. arXiv:2410.02644. Encoder-readiness: **NOT a drop-in `(text,label)` set** — ASR framework over a full agent stack; needs substantial adaptation to extract a labeled text corpus.
- **Status:** Verified.
- **Soft tags:** family=agentic-trajectory · encoder_readiness=adaptation-heavy · study_relevance=medium

### E3. InjecAgent — Zhan et al. (ACL 2024 Findings)
- **Source:** https://github.com/uiuc-kang-lab/InjecAgent
- **Access:** direct; auth_required: N
- **Schema:** `user_cases.jsonl` + `attacker_cases_dh/ds.jsonl` + `test_cases_dh/ds_{setting}.json`.
- **Size+License:** 1,054 test cases (17 user tools, 62 attacker tools); MIT.
- **Tasks:** Indirect-injection benchmark for **tool-integrated agents**. Two attack-intent categories: direct harm (`dh`) + data exfiltration/stealing (`ds`); not fine-grained per-string type labels. All-attack test cases (no benign control split); measures whether injection succeeds (ASR-valid / ASR-all over ReAct tool-calling traces). arXiv:2403.02691. Encoder-readiness: **NOT a drop-in `(text,label)` set** — agent ASR benchmark; injected attacker-tool prompts can be mined as malicious text but no paired benign set, so a classifier corpus needs benign carriers supplied.
- **Status:** Verified.
- **Soft tags:** family=agentic-trajectory · encoder_readiness=adaptation-heavy · study_relevance=medium

### E4. AgentDyn — SaFo-Lab (2026)
- **Source:** https://github.com/SaFo-Lab/AgentDyn
- **Access:** direct (git clone); auth_required: N
- **Schema:** n/a — an AgentDojo-based dynamic security benchmark (tasks + injection cases + trajectory JSONs), not `(text,label)`.
- **Size+License:** 60 tasks + 560 injection cases (built on AgentDojo); `runs/` = 48,672 trajectory JSONs; MIT.
- **Tasks:** A 2026 adaptive-attacker benchmark layered on **AgentDojo** — measures whether an injection succeeds across the agent loop (ASR), not classification metrics. Overlaps the AgentDojo lineage (E1). Research-role: an **execution / Lane-5 candidate** — extract its 560 injection cases into `(text, label)` only if it earns a role at a later gate. Encoder-readiness: **adaptation-heavy** — not a shipped `(text,label)` corpus; the injection cases must be mined out of the agent environment.
- **Status:** Verified.
- **Soft tags:** family=agentic-trajectory · encoder_readiness=adaptation-heavy · study_relevance=low

### E5. AgentDAM (facebookresearch/ai-agent-privacy) — facebookresearch
- **Source:** https://github.com/facebookresearch/ai-agent-privacy
- **Access:** direct (git clone); auth_required: N
- **Schema:** n/a — privacy / data-minimization trajectories on VisualWebArena, not `(text,label)`.
- **Size+License:** VisualWebArena-based agent benchmark (privacy-leakage / data-minimization); CC-BY-NC (+ Llama-3.1 terms).
- **Tasks:** **OFF-AXIS** — measures privacy-leakage / data-minimization by a web agent, **not injection detection**. EDA-gate verdict (2026-06-03): off-axis (privacy ≠ injection). Research-role: **catalogue-only-with-reason** (recorded so the universe scan is complete; not an injection set). Encoder-readiness: **adaptation-heavy** and off-axis. ⚠️ **NC license** (+ Llama-3.1 terms) ⇒ non-commercial.
- **Status:** Verified (off-axis — privacy, not injection).
- **Soft tags:** family=agentic-trajectory · encoder_readiness=adaptation-heavy · study_relevance=low

_5 entries._
