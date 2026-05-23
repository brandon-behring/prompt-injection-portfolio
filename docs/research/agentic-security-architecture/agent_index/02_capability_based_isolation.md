# # D2 — Capability-based isolation + dual-LLM patterns

_3 entries covering capability tags + provenance metadata; CaMeL + IsolateGPT/SecGPT + dual-LLM splits._


## D2.1. Defeating Prompt Injections by Design

- **Defeating Prompt Injections by Design** — Debenedetti et al. (2025).
  - **Source:** https://arxiv.org/abs/2503.18813
  - **Code:** https://github.com/google-research/camel-prompt-injection
  - **Mechanism:** CaMeL splits the LLM into a privileged + quarantined pair with a custom Python interpreter that tags every value with provenance metadata (capabilities);…
  - **Result:** Reports a provably-secure subset of AgentDojo tasks completed in v2 (around 77%), versus 84% completed undefended; substantial token-cost overhead (roughly…
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0011


## D2.2. IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems

- **IsolateGPT: An Execution Isolation Architecture for LLM-Based Agentic Systems** — Wu et al. (2024).
  - **Source:** https://arxiv.org/abs/2403.04960
  - **Code:** https://github.com/llm-platform-security/SecGPT
  - **Mechanism:** IsolateGPT/SecGPT proposes per-plugin sandboxing with an orchestrator that mediates inter-plugin communication; each plugin runs in an isolated execution…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0013


## D2.3. The Dual LLM pattern for building AI assistants that can resist prompt injection

- **The Dual LLM pattern for building AI assistants that can resist prompt injection** — Willison (2023).
  - **Source:** https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
  - **Code:** —
  - **Mechanism:** Willison articulates the informal Dual LLM pattern in April 2023: a privileged LLM with tool access never sees untrusted text; a quarantined LLM (tool-less)…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0014
