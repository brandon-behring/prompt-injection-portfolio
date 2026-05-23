# 02 — Architectural defenses (not classifier-shaped) (B2)

**Scope:** primary sources on prompt-injection defenses that act on system architecture — prompt-engineering separators (Spotlighting), training-time interventions (StruQ, SecAlign, Meta SecAlign, Instruction Hierarchy), task-specific distillation (Jatmo), capability-based isolation (CaMeL, IsolateGPT), guardrail frameworks (LlamaFirewall), and design-pattern surveys (Beurer-Kellner et al.).
**Out of scope:** classifier-shaped detectors (Llama Guard, Prompt Guard, PromptShield) — see `../../detector-landscape/agent_index/`; benchmarks evaluating these defenses (see `04_indirect_benchmarks.md`); production incidents demonstrating bypass (see `03_production_incidents.md`).

Section anchors below use the `## B2.` prefix from `../research_plan.md`. The 10 entries are roughly ordered along the architectural-layer continuum: prompt-engineering → training-time → task-specific → capability-isolation → guardrail-stack → design-pattern survey.

## B2. Architectural defenses (not classifier-shaped)

- **Defending Against Indirect Prompt Injection Attacks With Spotlighting** — Hines et al. (CAMLIS 2024, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2403.14720
  - **Code:** —
  - **Mechanism:** Introduces "spotlighting", a family of prompt-engineering techniques (delimiting, datamarking, encoding) that mark untrusted input so the LLM treats it as data rather than instructions [claim_hines_spotlighting_method].
  - **Result:** Provides a deployment-ready prompt-time defense usable on production LLMs without retraining; GA in Microsoft Build 2025 announcements.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0006

- **StruQ: Defending Against Prompt Injection with Structured Queries** — Chen et al. (USENIX Security 2025).
  - **Source:** https://arxiv.org/abs/2402.06363
  - **Code:** https://github.com/Sizhe-Chen/StruQ
  - **Mechanism:** Introduces "structured queries", a general approach that fine-tunes the LLM with reserved delimiters so that instruction text and data text occupy distinct, non-overlapping token spaces [claim_struq_structured_queries].
  - **Result:** Establishes the reserved-delimiter SFT branch of architectural defenses; companion line of work to SecAlign and Instruction Hierarchy.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0007

- **SecAlign: Defending Against Prompt Injection with Preference Optimization** — Chen et al. (ACM CCS 2025).
  - **Source:** https://arxiv.org/abs/2410.05451
  - **Code:** https://github.com/facebookresearch/SecAlign
  - **Mechanism:** Casts prompt-injection defense as preference optimization: builds (secure, insecure) response pairs and uses DPO to train the model to prefer the secure response under untrusted input [claim_secalign_dpo_defense].
  - **Result:** Strong reduction in attack-success rate while preserving utility; positioned as the DPO complement to StruQ's SFT formulation. Body-anchored quote: "SecAlign reduces the attack success rate of the strongest tested prompt injection to 8% without hurting the utility from Llama3-8B-Instruct" [claim_secalign_llama3_8b_8pct_asr].
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0008, ev_direct_vs_indirect_0057

- **Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks** — Chen et al. (2025).
  - **Source:** https://arxiv.org/abs/2507.02735
  - **Code:** —
  - **Mechanism:** Develops Meta SecAlign as "the first fully open-source LLM with built-in model-level defense that achieves commercial-grade performance" against prompt injection, applying the SecAlign DPO recipe to produce Meta-SecAlign-70B and Meta-SecAlign-8B model variants [claim_meta_secalign_open_model]. Body-anchored detail: the paper specifies "SecAlign++, which fine-tunes Llama-3.1-8B-Instruct and Llama-3.3-70B-Instruct" as the base models — resolving the round-1 audit flag on the Llama-3.3-70B base.
  - **Result:** Open-weight model designed to let the security community red-team injection defenses without depending on proprietary APIs; meaningful for reproducibility.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0009, ev_direct_vs_indirect_0059

- **Defeating Prompt Injections by Design (CaMeL)** — Debenedetti et al. (Google DeepMind, 2025).
  - **Source:** https://arxiv.org/abs/2503.18813
  - **Code:** https://github.com/google-research/camel-prompt-injection
  - **Mechanism:** Proposes CaMeL, "a robust defense that creates a protective system layer around the LLM" so that even when the underlying model is susceptible to attacks the system as a whole remains secure [claim_camel_capability_isolation]. CaMeL "explicitly extracts the control and data flows from the (trusted) query" so that untrusted data retrieved by the LLM "can never impact the program flow" [claim_camel_control_data_flow].
  - **Result:** Capability-based-isolation paradigm; reports provably-secure behavior on a substantial subset of AgentDojo. Body-anchored quote: "77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo" [claim_camel_agentdojo_provable_security_77pct]. Conceptual descendant of Willison's dual-LLM pattern (see `01_threat_models.md` § B1.3).
  - **Status:** Verified (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0010, ev_direct_vs_indirect_0011, ev_direct_vs_indirect_0056

- **The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions** — Wallace et al. (OpenAI, 2024).
  - **Source:** https://arxiv.org/abs/2404.13208
  - **Code:** —
  - **Mechanism:** Proposes an instruction hierarchy that "explicitly defines how models should behave when instructions of different priorities conflict" and trains the model to honor that priority order [claim_instruction_hierarchy_priority]. Body-anchored quote: the paper enumerates "System Messages provided by application developers, User Messages provided by end users, and Tool Outputs" — resolving the round-1 audit flag on the privileged-to-untrusted ordering.
  - **Result:** Training-time defense complementary to StruQ/SecAlign; shipped in OpenAI models from GPT-4o onward.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0012, ev_direct_vs_indirect_0058

- **Jatmo: Prompt Injection Defense by Task-Specific Finetuning** — Piet et al. (ESORICS 2024, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2312.17673
  - **Code:** https://github.com/wagner-group/prompt-injection-defense
  - **Mechanism:** Introduces Jatmo, "a method for generating task-specific models resilient to prompt-injection attacks" by distilling a base instruction-tuned LLM into a narrower task model that never sees free-form instructions at inference time [claim_jatmo_task_specific_distillation].
  - **Result:** Establishes the task-specific-distillation branch of defenses; effective when the application has a fixed task surface.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0013

- **IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems** — Wu et al. (NDSS 2025).
  - **Source:** https://arxiv.org/abs/2403.04960
  - **Code:** https://github.com/llm-platform-security/SecGPT
  - **Mechanism:** Proposes "an execution isolation architecture for LLM-based agentic systems" (a.k.a. SecGPT) that confines each app/extension to its own sandbox and mediates inter-app communication, limiting what an injected instruction can reach [claim_isolategpt_execution_isolation].
  - **Result:** Capability-isolation architecture analogous in spirit to mobile-OS app sandboxes; complements CaMeL on the agent-platform layer.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0014

- **LlamaFirewall: An open source guardrail system for building secure AI agents** — Chennabasappa et al. (Meta, 2025).
  - **Source:** https://arxiv.org/abs/2505.03574
  - **Code:** https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall
  - **Mechanism:** Introduces LlamaFirewall, "an open-source security focused guardrail framework" bundling multiple defenses — input/output classifiers, tool-call constraints, and policy enforcement — into a deployable agent-layer firewall [claim_llamafirewall_open_guardrail].
  - **Result:** Packages multiple defenses into a single open-source deployable framework; reference architecture for agent-layer firewalls.
  - **Status:** Verified (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0015

- **Design Patterns for Securing LLM Agents against Prompt Injections** — Beurer-Kellner et al. (2025).
  - **Source:** https://arxiv.org/abs/2506.08837
  - **Code:** —
  - **Mechanism:** Proposes "a set of principled design patterns for building AI agents with provable resistance to prompt injection" by structurally limiting what untrusted data can influence in the agent control flow [claim_designpatterns_provable_resistance].
  - **Result:** Survey + framework that unifies CaMeL, IsolateGPT, dual-LLM, and Spotlighting under a common design-pattern taxonomy; influential follow-up to Greshake 2023.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0016

---
10 entries
