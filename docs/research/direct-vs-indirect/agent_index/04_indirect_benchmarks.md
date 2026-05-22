# 04 — Indirect-injection benchmarks (agentic + RAG) (B4)

**Scope:** primary sources for benchmarks that measure indirect-prompt-injection attack-success rate and defense robustness — BIPIA (5 scenarios × 6 subtypes), InjecAgent (tool-use agents), AgentDojo (97 user tasks / 629 cases), LLMail-Inject (adaptive challenge), Agent Security Bench / ASB (10 scenarios / 400+ tools), WASP (web agents).
**Out of scope:** detector-only benchmarks (see `../../detector-landscape/agent_index/`); architectural defenses that report on these benchmarks (see `02_architectural_defenses.md`); production incidents involving these attack classes (see `03_production_incidents.md`).

Section anchors below use the `## B4.` prefix from `../research_plan.md`. The 6 entries are roughly ordered along the threat-model continuum: RAG-only (BIPIA) → tool-use (InjecAgent) → agentic-environment (AgentDojo) → adaptive-challenge (LLMail-Inject) → comprehensive-benchmark (ASB) → web-agent (WASP).

## B4. Indirect-injection benchmarks (agentic + RAG)

- **Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models (BIPIA)** — Yi et al. (KDD 2025).
  - **Source:** https://arxiv.org/abs/2312.14197
  - **Code:** —
  - **Mechanism:** Introduces "the first benchmark for indirect prompt injection attacks, named BIPIA, to assess the risk of such vulnerabilities" [claim_bipia_first_indirect_benchmark]. Covers 5 application scenarios × 6 attack subtypes × 250 goals according to the research plan; benchmark numbers cited at abstract level.
  - **Result:** First standardized indirect-injection benchmark from Microsoft / USTC; canonical reference for early evaluation of indirect-injection ASR.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0031

- **InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents** — Zhan et al. (ACL 2024 Findings).
  - **Source:** https://arxiv.org/abs/2403.02691
  - **Code:** https://github.com/uiuc-kang-lab/InjecAgent
  - **Mechanism:** Defines indirect prompt injection (IPI) attacks as the case where "external content introduces the risk of indirect prompt injection (IPI) attacks, where malicious instructions are embedded within the content processed by LLMs" [claim_injecagent_ipi_definition], and introduces InjecAgent as "a benchmark designed to" measure IPI ASR against tool-integrated LLM agents [claim_injecagent_tool_integrated_benchmark]. The plan-level dataset is 1,054 cases × 17 user tools × 62 attacker tools.
  - **Result:** First tool-use-focused IPI benchmark; canonical reference for agent-tool-call ASR.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0032, ev_direct_vs_indirect_0033

- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** — Debenedetti et al. (NeurIPS 2024, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2406.13352
  - **Code:** https://github.com/ethz-spylab/agentdojo
  - **Mechanism:** Introduces AgentDojo, "an evaluation framework for agents that execute tools over untrusted data" [claim_agentdojo_dynamic_environment]; the framework "is not a static test suite, but rather an extensible environment for designing and evaluating new agent tasks, defenses, and adaptive" attacks [claim_agentdojo_extensible_environment]. Covers banking, Slack, travel, and workspace scenarios with 97 user tasks × 629 security cases per the research plan.
  - **Result:** De facto indirect-injection benchmark for agent evaluation; adopted by Anthropic, OpenAI, Meta, and Google reports. Referenced in CaMeL's 77% provably-secure result (see `02_architectural_defenses.md` § B2.5).
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0034, ev_direct_vs_indirect_0035

- **LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge** — Abdelnabi et al. (IEEE SaTML 2025, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2506.09956
  - **Code:** —
  - **Mechanism:** Presents the results of LLMail-Inject, "a public challenge simulating a realistic scenario in which participants adaptively attempted to inject malicious instructions into emails" handled by an LLM-based assistant [claim_llmail_inject_adaptive_dataset]. Plan-level scale: 208K adaptive attacks from 839 participants.
  - **Result:** Establishes the adaptive-challenge benchmark format — a counterpoint to fixed-attack benchmarks like BIPIA/InjecAgent — and provides the dataset for follow-up work on adaptive-attacker evaluation.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0036

- **Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents** — Zhang et al. (ICLR 2025).
  - **Source:** https://arxiv.org/abs/2410.02644
  - **Code:** https://github.com/agiresearch/ASB
  - **Mechanism:** Introduces Agent Security Bench (ASB), "a comprehensive framework designed to formalize, benchmark, and evaluate the attacks and defenses of LLM-based agents" [claim_asb_formalize_benchmark]; covers "10 scenarios (e.g., e-commerce, autonomous driving, finance), 10 agents targeting the scenarios, over 400 tools" [claim_asb_10_scenarios_400_tools] together with 27 attack/defense method types and 7 evaluation metrics.
  - **Result:** Largest comprehensive agentic-security benchmark as of ICLR 2025; covers a wider attack/defense matrix than AgentDojo's banking/Slack/travel/workspace surface.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0037, ev_direct_vs_indirect_0038

- **WASP: Benchmarking Web Agent Security Against Prompt Injection Attacks** — Evtimov et al. (2025).
  - **Source:** https://arxiv.org/abs/2504.18575
  - **Code:** https://github.com/facebookresearch/wasp
  - **Mechanism:** Introduces WASP, "a new publicly available benchmark for end-to-end evaluation of Web Agent Security against Prompt injection attacks" [claim_wasp_web_agent_benchmark] targeting browser-agentic surfaces (Perplexity Comet, Claude Chrome extension etc.).
  - **Result:** Companion to the production-incident reports in `03_production_incidents.md` (ShadowPrompt, Comet, Gemini Trifecta); provides a reproducible benchmark for browser-agentic indirect injection.
  - **Status:** Verified (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0039

---
6 entries
