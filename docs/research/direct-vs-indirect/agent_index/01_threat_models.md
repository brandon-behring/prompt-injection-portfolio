# 01 — Threat-model taxonomies + foundational framings (B1)

**Scope:** primary sources that define the direct-vs-indirect (XPIA) prompt-injection split, the systematic threat taxonomies built on top of it, and dual-LLM / privileged-vs-quarantined patterns that motivate the architectural defenses in `02_architectural_defenses.md`.
**Out of scope:** detector-only literature (see `../../detector-landscape/agent_index/`); benchmarks (see `04_indirect_benchmarks.md`); production incident reports (see `03_production_incidents.md`).

Section anchors below use the `## B1.` prefix from `../research_plan.md`. Each entry is a paper / standard / blog cited at minimum by title; canonical 5-bullet structure (Source / Code / Mechanism / Result / Status / Evidence) per `~/Claude/research_toolkit/templates/5_bullet_entry.template.md`.

## B1. Threat-model taxonomies + foundational framings

- **Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection** — Greshake et al. (AISec 2023, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2302.12173
  - **Code:** —
  - **Mechanism:** Coins the term "Indirect Prompt Injection" and shows that adversaries can exploit LLM-integrated applications remotely "without a direct interface" by strategically injecting prompts into content the application later retrieves [claim_direct_vs_indirect_greshake_taxonomy].
  - **Result:** Derives a comprehensive taxonomy from a computer-security perspective, enumerating impacts and vulnerabilities including data theft, worming, and information-ecosystem contamination [claim_direct_vs_indirect_greshake_taxonomy_impacts]. Canonical reference for the direct-vs-indirect split.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0001, ev_direct_vs_indirect_0002

- **LLM01:2025 Prompt Injection** — OWASP Gen AI Security Project (OWASP Top 10 for LLM Applications 2025).
  - **Source:** https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  - **Code:** —
  - **Mechanism:** Codifies the direct-vs-indirect split as the LLM01 entry in the OWASP Top 10 for LLM Applications 2025, listing both attack types as the highest-ranked LLM-application risk [claim_owasp_llm01_direct_indirect_split].
  - **Result:** Industry-baseline taxonomy referenced by vendor security advisories and regulators; cross-walks to MITRE ATLAS techniques.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0003

- **The Dual LLM pattern for building AI assistants that can resist prompt injection** — Willison (simonwillison.net, April 2023).
  - **Source:** https://simonwillison.net/2023/Apr/25/dual-llm-pattern/
  - **Code:** —
  - **Mechanism:** Introduces the dual-LLM pattern: a privileged LLM that sees only trusted inputs and emits tool calls, plus one or more quarantined LLMs that process untrusted content but cannot directly trigger tool calls [claim_willison_dual_llm_pattern].
  - **Result:** Conceptual ancestor of capability-based defenses (CaMeL, IsolateGPT) and the trust-boundary framing used by the Beurer-Kellner 2025 design patterns. Foundational blog post.
  - **Status:** Verified (no widely-known repo) (vendor / personal blog).
  - **Evidence:** ev_direct_vs_indirect_0004

- **The lethal trifecta for AI agents: private data, untrusted content, and external communication** — Willison (simonwillison.net, June 2025).
  - **Source:** https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
  - **Code:** —
  - **Mechanism:** Names the three-property risk pattern — when an AI agent simultaneously has (a) access to private data, (b) exposure to untrusted content, and (c) the ability to communicate externally — as the "lethal trifecta" predicting indirect-prompt-injection exfiltration [claim_willison_lethal_trifecta].
  - **Result:** Frames the EchoLeak / Slack AI / Comet incident class as instances of a single architectural anti-pattern, widely adopted as shorthand in 2025 vendor and researcher disclosures.
  - **Status:** Verified (no widely-known repo) (vendor / personal blog) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0005

- **Ignore Previous Prompt: Attack Techniques For Language Models** — Perez & Ribeiro (ML Safety Workshop NeurIPS 2022, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2211.09527
  - **Code:** https://github.com/agencyenterprise/PromptInject
  - **Mechanism:** Proposes PromptInject, "a prosaic alignment framework for mask-based iterative adversarial prompt composition," and examines goal hijacking and prompt leaking as two prompt-injection attack types against GPT-3 [claim_promptinject_framework, claim_goal_hijacking_prompt_leaking].
  - **Result:** First systematic naming of "goal hijacking" and "prompt leaking" — the canonical pre-Greshake reference for direct prompt-injection attacks. Defines the framework reused by later attack literature.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0040, ev_direct_vs_indirect_0041

- **Formalizing and Benchmarking Prompt Injection Attacks and Defenses** — Liu et al. (USENIX Security 2024, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2310.12815
  - **Code:** https://github.com/liu00222/Open-Prompt-Injection
  - **Mechanism:** Defines a prompt-injection attack as one that "aims to inject malicious instruction/data into the input of an LLM-Integrated Application" and provides a formal framework for systematic evaluation [claim_prompt_injection_definition_llm_integrated]. Runs a systematic evaluation across "5 prompt injection attacks and 10 defenses with 10 LLMs and 7 tasks" [claim_formalize_5_attacks_10_defenses].
  - **Result:** Canonical formalization paper — the standard reference for prompt-injection attack/defense matrices used across the 2024-2026 literature.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0042, ev_direct_vs_indirect_0043

- **Prompt Injection attack against LLM-integrated Applications** — Liu et al. (arXiv preprint, 2023).
  - **Source:** https://arxiv.org/abs/2306.05499
  - **Code:** —
  - **Mechanism:** Formulates HouYi, "a novel black-box prompt injection attack technique" targeting LLM-integrated applications [claim_houyi_blackbox_attack]. HouYi requires no internal model access, only public-facing app behavior.
  - **Result:** Deploys HouYi on "36 actual LLM-integrated applications and discern[s] 31 applications" as vulnerable [claim_houyi_36_apps_31_vulnerable] — first large-scale field-test demonstrating prompt-injection prevalence in shipping LLM apps.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0044, ev_direct_vs_indirect_0045

- **Optimization-based Prompt Injection Attack to LLM-as-a-Judge** — Shi et al. (ACM CCS 2024, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2403.17710
  - **Code:** https://github.com/ShiJiawenwen/JudgeDeceiver
  - **Mechanism:** Proposes JudgeDeceiver, "an optimization-based prompt injection attack to LLM-as-a-Judge" [claim_judgedeceiver_optimization_attack]. The attack "injects a carefully crafted sequence into an attacker-controlled candidate response" to coerce the judge's verdict [claim_judgedeceiver_attack_mechanism].
  - **Result:** First targeted prompt-injection attack against the LLM-as-a-Judge evaluation paradigm; demonstrates that evaluation-time judges are themselves an attack surface.
  - **Status:** Verified.
  - **Evidence:** ev_direct_vs_indirect_0046, ev_direct_vs_indirect_0047

- **Neural Exec: Learning (and Learning from) Execution Triggers for Prompt Injection Attacks** — Pasquini et al. (arXiv preprint, 2024).
  - **Source:** https://arxiv.org/abs/2403.03792
  - **Code:** —
  - **Mechanism:** Introduces "a new family of prompt injection attacks, termed Neural Exec" [claim_neural_exec_family], that "conceptualize the creation of execution triggers as a differentiable search problem and use learning-based methods to autonomously generate them" [claim_neural_exec_differentiable_search].
  - **Result:** Establishes the learning-based-trigger branch of injection attacks — adversaries can train transferable, model-agnostic triggers rather than hand-crafting payloads.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0048, ev_direct_vs_indirect_0049

- **Whispers in the Machine: Confidentiality in Agentic Systems** — Evertz et al. (DIMVA 2026, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2402.06922
  - **Code:** —
  - **Mechanism:** Evaluates "ten agents across 20 tool scenarios and 14 attack strategies" and finds that "all agents are vulnerable to at least one attack" [claim_whispers_agent_evaluation]. Specifically finds that "the tooling itself can amplify leakage risks" beyond the base-model failure surface [claim_whispers_tooling_amplifies_leakage].
  - **Result:** First systematic confidentiality study showing that tool-use itself — not just the LLM — expands the attack surface for indirect injection in agentic systems.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0050, ev_direct_vs_indirect_0051

- **Jailbroken: How Does LLM Safety Training Fail?** — Wei et al. (NeurIPS 2023, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2307.02483
  - **Code:** —
  - **Mechanism:** Hypothesizes "two failure modes of safety training: competing objectives and mismatched generalization" [claim_jailbreak_failure_modes]. The failure-mode framework explains how safety-aligned LLMs can be subverted by attacks that exploit gaps in training-data coverage.
  - **Result:** Shows that "new attacks utilizing our failure modes succeed on every prompt in a collection of unsafe requests" [claim_jailbreak_universal_success] — universal vulnerability to a structurally simple attack family. Canonical reference connecting jailbreak literature to prompt-injection threat models.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0052, ev_direct_vs_indirect_0053

- **An Early Categorization of Prompt Injection Attacks on Large Language Models** — Rossi et al. (arXiv preprint, 2024).
  - **Source:** https://arxiv.org/abs/2402.00898
  - **Code:** —
  - **Mechanism:** "Provide[s] an overview of these emergent threats and present[s] a categorization of prompt injections" attack types and impacts [claim_rossi_categorization_overview], synthesizing the 2022-2023 corpus into a single taxonomy.
  - **Result:** Early survey/taxonomy alternative to Greshake 2023; useful as a cross-reference taxonomy when comparing attack-class enumerations.
  - **Status:** Verified (no widely-known repo).
  - **Evidence:** ev_direct_vs_indirect_0054

- **MITRE ATLAS: Adversarial Threat Landscape for AI Systems** — MITRE Corporation (atlas.mitre.org, 2024).
  - **Source:** https://atlas.mitre.org/
  - **Code:** —
  - **Mechanism:** Provides the canonical adversarial-tactic taxonomy for AI systems, including AML.T0051 LLM Prompt Injection sub-techniques (direct AML.T0051.000 and indirect AML.T0051.001) [claim_mitre_atlas_taxonomy].
  - **Result:** Industry-baseline MITRE-style threat taxonomy referenced by vendor advisories, NIST AI RMF, and regulators; complements OWASP LLM01:2025 as the canonical structured-tactic catalog.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0055

---
13 entries
