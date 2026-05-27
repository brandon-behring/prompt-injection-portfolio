# # D1 — Agent harness security architecture

_10 entries covering system shape of agentic deployment (tool-calling agents, multi-turn loops, side-effect surfaces). D1.9-D1.10 are vendor/harness defense primary sources (Anthropic)._


## D1.1. LlamaFirewall: An open source guardrail system for building secure AI agents

- **LlamaFirewall: An open source guardrail system for building secure AI agents** — Chennabasappa et al. (2025).
  - **Source:** https://arxiv.org/abs/2505.03574
  - **Code:** https://github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall
  - **Mechanism:** LlamaFirewall is an open-source guardrail system designed as a layered defense for AI agents, addressing risks like prompt injection, agent misalignment, and…
  - **Result:** Reports PromptGuard v2 86M with substantial ASR reduction and small utility loss on AgentDojo as part of the layered harness composition.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0001


## D1.2. AgentArmor: Enforcing Program Analysis on Agent Runtime Trace to Defend Against 

- **AgentArmor: Enforcing Program Analysis on Agent Runtime Trace to Defend Against Prompt Injection** — Wang et al. (2025).
  - **Source:** https://arxiv.org/abs/2508.01249
  - **Code:** —
  - **Mechanism:** AgentArmor intercepts agent execution traces, converts them into program-dependence-graph intermediate representations, and enforces security policies via a…
  - **Result:** Reports ~3% ASR with low functional overhead on AgentDojo; treats the agent trace as a program to be analysed, not text to be classified.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0003


## D1.3. Design Patterns for Securing LLM Agents against Prompt Injections

- **Design Patterns for Securing LLM Agents against Prompt Injections** — Beurer-Kellner et al. (2025).
  - **Source:** https://arxiv.org/abs/2506.08837
  - **Code:** —
  - **Mechanism:** Catalogues design patterns for securing LLM agents against prompt injections (Action-Selector, Plan-Then-Execute, Map-Reduce, Dual LLM, Code-Then-Execute,…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0005


## D1.4. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions

- **The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions** — Wallace et al. (2024).
  - **Source:** https://arxiv.org/abs/2404.13208
  - **Code:** —
  - **Mechanism:** Instruction Hierarchy proposes training LLMs to prioritise privileged instructions (system > developer > user > tool), addressing the lack of trust-channel…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0006


## D1.5. StruQ: Defending Against Prompt Injection with Structured Queries

- **StruQ: Defending Against Prompt Injection with Structured Queries** — Chen et al. (2024).
  - **Source:** https://arxiv.org/abs/2402.06363
  - **Code:** https://github.com/Sizhe-Chen/StruQ
  - **Mechanism:** StruQ uses structured queries with reserved-token-protected delimiters separating prompt from data, plus an SFT phase, to defend against direct + indirect…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0007


## D1.6. SecAlign: Defending Against Prompt Injection with Preference Optimization

- **SecAlign: Defending Against Prompt Injection with Preference Optimization** — Chen et al. (2024).
  - **Source:** https://arxiv.org/abs/2410.05451
  - **Code:** https://github.com/facebookresearch/SecAlign
  - **Mechanism:** SecAlign uses preference-optimization (DPO) over secure/insecure response pairs to train the model to prefer following the system prompt over the injected one;…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0008


## D1.7. Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks

- **Meta SecAlign: A Secure Foundation LLM Against Prompt Injection Attacks** — Chen et al. (2025).
  - **Source:** https://arxiv.org/abs/2507.02735
  - **Code:** —
  - **Mechanism:** Meta SecAlign on Llama-3.3-70B introduces an explicit `input` role distinct from `user` for untrusted tool/document data, formalizing harness-contract…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0009


## D1.8. Jatmo: Prompt Injection Defense by Task-Specific Finetuning

- **Jatmo: Prompt Injection Defense by Task-Specific Finetuning** — Piet et al. (2023).
  - **Source:** https://arxiv.org/abs/2312.17673
  - **Code:** https://github.com/wagner-group/prompt-injection-defense
  - **Mechanism:** Jatmo trains task-specific fine-tuned models that cannot follow instructions in their inputs; reports very low ASR (<0.5%) and is the narrow-agent extreme of…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0010


## D1.9. Mitigating the risk of prompt injections in browser use

- **Mitigating the risk of prompt injections in browser use** — Anthropic (2025).
  - **Source:** https://www.anthropic.com/research/prompt-injection-defenses
  - **Code:** —
  - **Mechanism:** Vendor primary source describing Anthropic's layered browser-agent prompt-injection defenses; trains robustness directly into the model — "we use reinforcement learning to build prompt injection robustness directly into Claude" by exposing it to injections embedded in simulated web content during training, layered with post-preview safeguards across all Claude models.
  - **Result:** Frames residual risk explicitly: "A 1% attack success rate—while a significant improvement—still represents meaningful risk. No browser agent is immune to prompt injection" — a vendor-stated floor, shared to show progress rather than claim the problem solved (1% ASR figure verbatim from the post).
  - **Status:** Verified (vendor research post — anthropic.com/research, T1-official; no separate code repo).
  - **Evidence:** ev_agentic_security_architecture_0032 ev_agentic_security_architecture_0033


## D1.10. Computer use tool

- **Computer use tool** — Anthropic (2026).
  - **Source:** https://docs.claude.com/en/docs/agents-and-tools/tool-use/computer-use-tool
  - **Code:** —
  - **Mechanism:** Vendor primary docs for the computer-use action surface — the tool "provides screenshot capabilities and mouse/keyboard control for autonomous desktop interaction"; the harness-defense guidance recommends "using a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents" as a defense-in-depth precaution.
  - **Result:** Documents an added prompt-injection classifier layer on top of model-level resistance: "If you use the computer use tools, classifiers will automatically run on your prompts to flag potential instances of prompt injections" (and steer the model when injections are detected in screenshots) — VM/container isolation plus a classifier layer as the documented harness defenses.
  - **Status:** Verified (vendor docs — docs.claude.com, T1-official; no separate code repo).
  - **Evidence:** ev_agentic_security_architecture_0034 ev_agentic_security_architecture_0035 ev_agentic_security_architecture_0036
