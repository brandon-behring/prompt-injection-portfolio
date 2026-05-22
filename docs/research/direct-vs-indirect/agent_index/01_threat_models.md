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

---
4 entries
