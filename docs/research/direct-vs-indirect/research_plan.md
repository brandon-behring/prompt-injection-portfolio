# Research Plan: Direct vs indirect (XPIA) prompt injection — taxonomy, architectural defenses, production incidents

The conceptual + practical split between direct (user-supplied) and indirect / XPIA (retrieved-content) prompt injection: threat taxonomies, multi-layer defenses, architectural approaches beyond detection (Spotlighting, StruQ, SecAlign, CaMeL, Instruction Hierarchy), and the production-incident corpus that demonstrates each layer is bypassable. Target ~20-25 primary-source entries across 4 sub-areas.

## Sub-areas

- B1. Threat-model taxonomies + foundational framings
  - Source types: arXiv, OWASP standards docs, MITRE ATLAS, security analyst blog posts
  - Notes: Greshake et al. AISec 2023 (arXiv 2302.12173) introduced "indirect prompt injection." OWASP LLM01:2025 codifies direct + indirect split. MITRE ATLAS tracks AML.T0051.000 (Direct) + AML.T0051.001 (Indirect). Greshake's 4-flavor taxonomy: passive / active / user-driven / hidden. Simon Willison's "dual LLM" pattern (April 2023, April 2025 CaMeL analysis).

- B2. Architectural defenses (not classifier-shaped)
  - Source types: arXiv, conference proceedings (USENIX, CCS, NeurIPS), vendor docs
  - Notes: Spotlighting (Hines et al. Microsoft arXiv 2403.14720, CAMLIS 2024; GA Microsoft Build 2025) — 3 variants (delimiting / datamarking / encoding). StruQ (Chen, Piet, Sitawarin, Wagner USENIX 2025 arXiv 2402.06363). SecAlign (Chen et al. CCS 2025 arXiv 2410.05451). Meta SecAlign on Llama-3.3-70B (arXiv 2507.02735). Jatmo task-specific distillation (arXiv 2312.17673 ESORICS 2024). Instruction Hierarchy (Wallace et al. OpenAI arXiv 2404.13208). CaMeL Google DeepMind (Debenedetti et al. arXiv 2503.18813 v1 + v2). IsolateGPT/SecGPT (Wu et al.). LlamaFirewall (arXiv 2505.03574). AgentArmor / agent-layer firewalls. Cover the dual-LLM / privileged-vs-quarantined-LLM split formally.

- B3. Production incidents + adversarial-bypass research
  - Source types: CVE databases, vendor security advisories, researcher blogs (embracethered.com / Rehberger, Aim Labs, PromptArmor, Koi, Brave), arXiv papers documenting bypass
  - Notes: EchoLeak (CVE-2025-32711, CVSS 9.3, Aim Labs June 2025) — first publicly documented zero-click indirect injection in production (Microsoft 365 Copilot). Johann Rehberger's "Month of AI Bugs" (Aug 2025; one vuln/day against ChatGPT, GitHub Copilot, Anthropic MCPs, Cursor, Amp, Devin, OpenHands, Claude Code, Google Jules). Slack AI cross-channel exfiltration (PromptArmor Aug 2024). ChatGPT Markdown image exfil (April 2023 Rehberger). Bing Chat / Copilot manipulation 2023. Gemini long-term memory poisoning (Sept 2024 Rehberger). ShadowPrompt Claude Chrome extension DOM XSS (Koi Dec 2025-Jan 2026, fixed v1.0.41). Gemini Trifecta 2025. Comet browser indirect injection (Brave Aug 2025). "Bypassing Prompt Injection and Jailbreak Detection" (Hackett et al. arXiv 2504.11168 April 2025). "Are Firewalls All You Need?" (Bhagwatkar et al. arXiv 2510.05244 NeurIPS 2025). "Attacker moves second" (Nasr et al. arXiv 2510.09023). "How Not to Detect Prompt Injections with an LLM" (arXiv 2507.05630).

- B4. Indirect-injection benchmarks (agentic + RAG)
  - Source types: arXiv conference proceedings, benchmark GitHub repos
  - Notes: BIPIA (Yi et al. Microsoft/USTC arXiv 2312.14197 KDD 2025) — 5 application scenarios × 6 attack subtypes × 250 goals. InjecAgent (Zhan et al. arXiv 2403.02691 ACL 2024) — 1,054 cases, 17 user tools × 62 attacker tools. AgentDojo (Debenedetti et al. ETH/Google NeurIPS 2024 arXiv 2406.13352) — 97 user tasks × 629 security cases, banking/Slack/travel/workspace. LLMail-Inject Microsoft IEEE SaTML 2025 (arXiv 2506.09956) — 208K adaptive attacks from 839 participants. Agent Security Bench (ASB ICLR 2025). τ-Bench / WIPI / ToolEmu (2024-25). 2026 adaptive-attacker benchmarks: AgentDyn, AgentSentry, AgentVigil.

## Out-of-scope

- Direct-injection detectors — covered comprehensively in `detector-landscape/`
- Adversarial-suffix optimization (AdvBench, HarmBench, GCG, AutoDAN) — they're attack benchmarks against base LLMs, not direct-vs-indirect literature
- Operational red-team payloads or step-by-step exploit reproductions — per ADR-041 + ETHICS.md §1, dossier records the existence and impact of incidents but does NOT republish exploit content
- Multimodal indirect injection (vision-language attacks on surgical decision support etc.) — open research thread, no canonical taxonomy yet
- Pre-Greshake 2023 work on instruction-data confusion (the conceptual ancestors exist in SQL injection / XSS literature; reference but don't survey)
- Content-safety / jailbreak literature when not explicitly framed as direct-vs-indirect

## Claim family taxonomy

- injection_threat_model — Greshake taxonomy, OWASP LLM01:2025, MITRE ATLAS, instruction-hierarchy framings, dual-LLM patterns
- direct_vs_indirect_split — the conceptual + empirical distinction; trust-boundary problem; information-theoretic limits
- architectural_defense_methods — Spotlighting, StruQ, SecAlign, Jatmo, Instruction Hierarchy, CaMeL, IsolateGPT, dual-LLM splits, tool-call constraints, output filtering
- agentic_benchmarks — BIPIA, InjecAgent, AgentDojo, LLMail-Inject, ASB, τ-Bench, adaptive 2026 benchmarks
- production_incidents — EchoLeak, Month-of-AI-Bugs, Slack AI, ChatGPT image exfil, ShadowPrompt, Gemini Trifecta, Comet — each entry records vector + impact + remediation, no exploit reproduction

## Known landmark papers

- greshake2023indirect: "Not what you've signed up for" (arXiv 2302.12173 AISec 2023) — coined "indirect prompt injection"
- debenedetti2024agentdojo: AgentDojo (NeurIPS 2024 arXiv 2406.13352) — the de facto indirect-injection benchmark
- hines2024spotlighting: Spotlighting (arXiv 2403.14720 CAMLIS 2024) — base-64 / datamarking / delimiting variants
- chen2025struq: StruQ (USENIX Security 2025 arXiv 2402.06363) — reserved-delimiter SFT
- chen2025secalign: SecAlign (CCS 2025 arXiv 2410.05451) — DPO over secure/insecure response pairs
- chen2025metasecalign: Meta SecAlign on Llama-3.3-70B (arXiv 2507.02735) — `input` role separation
- debenedetti2025camel: CaMeL (Google/DeepMind arXiv 2503.18813) — capability-based isolation; 77% provably-secure on AgentDojo
- wallace2024instructionhierarchy: Instruction Hierarchy (OpenAI arXiv 2404.13208) — system > developer > user > tool training priority
- piet2024jatmo: Jatmo (arXiv 2312.17673 ESORICS 2024) — task-specific distillation; <0.5% ASR
- abdelnabi2025llmailinject: LLMail-Inject competition (Microsoft IEEE SaTML 2025 arXiv 2506.09956) — 208K adaptive attacks
- yi2025bipia: BIPIA (Microsoft/USTC arXiv 2312.14197 KDD 2025) — first indirect-injection benchmark
- zhan2024injecagent: InjecAgent (ACL 2024 arXiv 2403.02691) — agentic tool-use benchmark
- bhagwatkar2025firewalls: "Are Firewalls All You Need?" (NeurIPS 2025 arXiv 2510.05244) — benchmark-saturation critique
- hackett2025bypassing: "Bypassing Prompt Injection and Jailbreak Detection" (arXiv 2504.11168) — character-injection 100% ASR
- aimlabs2025echoleak: EchoLeak CVE-2025-32711 (Aim Labs June 2025) — first zero-click XPIA in production Copilot
- rehberger2025monthofaibugs: Johann Rehberger "Month of AI Bugs" (Aug 2025; embracethered.com) — daily disclosures
