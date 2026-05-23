# # D5 — Agentic-bench critique + adaptive evaluation

_6 entries covering benchmark saturation critique; LLMail-Inject adaptive eval; defenses evaluated on AgentDojo._


## D5.1. AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defens

- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** — Debenedetti et al. (2024).
  - **Source:** https://arxiv.org/abs/2406.13352
  - **Code:** https://github.com/ethz-spylab/agentdojo
  - **Mechanism:** AgentDojo is a dynamic environment to evaluate prompt-injection attacks and defenses on LLM agents; cited here as the critique-target benchmark whose…
  - **Result:** Cross-classified as critique target (rather than benchmark catalogue) for this topic; original benchmark cataloguing lives in `direct-vs-indirect/B4`.…
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0024


## D5.2. The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Inje

- **The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents** — Jia, Wu, Qin & Squicciarini (2024).
  - **Source:** https://arxiv.org/abs/2412.16682
  - **Code:** —
  - **Mechanism:** Task Shield enforces instruction-and-tool-call goal verification: each tool call must align with the original user task; reports very low ASR (~2%) and high…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0026


## D5.3. MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents

- **MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents** — Zhu et al. (2025).
  - **Source:** https://arxiv.org/abs/2502.05174
  - **Code:** https://github.com/kaijiezhu11/MELON
  - **Mechanism:** MELON (Masked Re-Execution and Tool Comparison) defends against indirect prompt injection by re-executing tool calls with masked inputs and comparing…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0027


## D5.4. Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?

- **Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** — Bhagwatkar et al. (2025).
  - **Source:** https://arxiv.org/abs/2510.05244
  - **Code:** —
  - **Mechanism:** Are Firewalls All You Need? argues that existing agentic security benchmarks (AgentDojo, ASB, InjecAgent, tau-Bench) are easily saturated by two-firewall…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0028


## D5.5. LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge

- **LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge** — Abdelnabi et al. (2025).
  - **Source:** https://arxiv.org/abs/2506.09956
  - **Code:** —
  - **Mechanism:** LLMail-Inject is a Microsoft-organized IEEE SaTML 2025 challenge dataset capturing realistic adaptive prompt-injection attempts (208K adaptive attacks from 839…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0029


## D5.6. The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM

- **The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections** — Nasr et al. (2025).
  - **Source:** https://arxiv.org/abs/2510.09023
  - **Code:** —
  - **Mechanism:** The Attacker Moves Second argues stronger adaptive attacks bypass defenses against LLM jailbreaks and prompt injections; static-defense numbers are unreliable.…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0030
