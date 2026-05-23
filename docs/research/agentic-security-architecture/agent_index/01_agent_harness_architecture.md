# # D1 — Agent harness security architecture

_8 entries covering system shape of agentic deployment (tool-calling agents, multi-turn loops, side-effect surfaces)._


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
