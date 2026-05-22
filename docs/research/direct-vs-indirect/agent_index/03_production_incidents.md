# 03 — Production incidents + adversarial-bypass research (B3)

**Scope:** publicly disclosed real-world indirect-prompt-injection incidents in shipping products (Microsoft 365 Copilot / EchoLeak, Slack AI, ChatGPT plugins, Claude Chrome extension / ShadowPrompt, Gemini Trifecta, Perplexity Comet) and the adversarial-bypass research papers that document the structural limits of detector / firewall defenses (Hackett, Bhagwatkar, Nasr, Choudhary). This file records the existence, threat-class, and remediation status of incidents — it does NOT republish payloads or step-by-step exploit chains (ADR-041 + ETHICS.md §1).
**Out of scope:** detector-only literature (see `../../detector-landscape/agent_index/`); architectural defenses against these classes of attack (see `02_architectural_defenses.md`); benchmark formalizations of the threat (see `04_indirect_benchmarks.md`).

Section anchors below use the `## B3.` prefix from `../research_plan.md`. Each entry's Mechanism field describes the vulnerability class and impact only; the Result field records the disclosure-and-remediation timeline. The `(security disclosure)` flag in Status marks entries that originate from coordinated vulnerability disclosure rather than academic research.

## B3. Production incidents + adversarial-bypass research

- **Breaking down 'EchoLeak', the First Zero-Click AI Vulnerability Enabling Data Exfiltration from Microsoft 365 Copilot** — Ravia, Aim Labs (Cato Networks blog, 2025).
  - **Source:** https://www.catonetworks.com/blog/breaking-down-echoleak/
  - **Code:** —
  - **Mechanism:** Zero-click indirect prompt injection in Microsoft 365 Copilot enabling unauthenticated attackers to "exfiltrate sensitive data with no user interaction or misconfiguration" [claim_echoleak_zero_click_xpia]. The disclosed vulnerability class chained an XPIA-classifier bypass, a Markdown-redaction bypass, and a Content-Security-Policy bypass that allowed data egress via Markdown image rendering through a trusted Teams proxy domain [claim_echoleak_aim_labs_disclosure]; remediation discussion below. No payload reproduction included here per ADR-041.
  - **Result:** First publicly documented zero-click XPIA in a production GenAI assistant (Aim Labs disclosed CVE-2025-32711 / CVSS 9.3 in June 2025); Microsoft patched the chain before in-the-wild exploitation. Catalyzed industry-wide adoption of the "lethal trifecta" framing.
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0017, ev_direct_vs_indirect_0018

- **CVE-2025-32711 Detail (M365 Copilot AI command injection)** — NIST NVD (2025).
  - **Source:** https://nvd.nist.gov/vuln/detail/cve-2025-32711
  - **Code:** —
  - **Mechanism:** Official NVD record for the EchoLeak vulnerability: an AI command-injection class flaw in Microsoft 365 Copilot allowing an unauthorized attacker to disclose information over a network [claim_cve_2025_32711_record]. NVD record provides the canonical identifier + CVSS score for cross-referencing with vendor advisories.
  - **Result:** Anchors the EchoLeak disclosure to the federal CVE/NVD process; cross-walks to MITRE ATLAS AML.T0051.001 (Indirect Prompt Injection). Patch listed as available.
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0019

- **The Month of AI Bugs 2025 (announcement)** — Rehberger (embracethered.com, 2025).
  - **Source:** https://embracethered.com/blog/posts/2025/announcement-the-month-of-ai-bugs/
  - **Code:** —
  - **Mechanism:** Announcement of a coordinated daily-disclosure series running through August 2025: Rehberger publishes one indirect-prompt-injection (or related agentic-AI) vulnerability per day across major commercial AI coding assistants and copilots, with each post including vendor remediation guidance [claim_month_of_ai_bugs_announcement]. No exploit reproduction here; readers should consult the individual disclosure posts for technical detail.
  - **Result:** Public demonstration that indirect-injection vulnerabilities are systemic across the 2025 agentic-AI surface; spurred industry-wide patches and disclosure-discipline upgrades.
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0020

- **Wrap Up: The Month of AI Bugs** — Rehberger (embracethered.com, 2025).
  - **Source:** https://embracethered.com/blog/posts/2025/wrapping-up-month-of-ai-bugs/
  - **Code:** —
  - **Mechanism:** Wrap-up enumeration of the Month-of-AI-Bugs disclosures covering ChatGPT, GitHub Copilot, Anthropic MCP servers, Cursor, Amp, Devin, OpenHands, Claude Code, and Google Jules — indirect prompt injection is the dominant root-cause class across the campaign [claim_month_of_ai_bugs_wrapup].
  - **Result:** Quantifies the cross-vendor scope of indirect-injection exposure as of late 2025; demonstrates that even mature AI coding assistants ship with exploitable XPIA surfaces. Use as the canonical pointer for "what got patched in 2025".
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0021

- **ChatGPT Plugins: Data Exfiltration via Images & Cross Plugin Request Forgery** — Rehberger (embracethered.com, 2023).
  - **Source:** https://embracethered.com/blog/posts/2023/chatgpt-webpilot-data-exfil-via-markdown-injection/
  - **Code:** —
  - **Mechanism:** Disclosure of a malicious-website scenario where retrieved web content can "take control of a ChatGPT chat session and exfiltrate the history of the conversation" [claim_chatgpt_markdown_image_exfil] via Markdown image rendering as the egress channel. Earliest public production disclosure in this class.
  - **Result:** OpenAI subsequently restricted Markdown image rendering in ChatGPT to limit this exfiltration channel; the vulnerability class is a direct ancestor of EchoLeak's Markdown-image-egress sub-component.
  - **Status:** Verified (no widely-known repo) (security disclosure).
  - **Evidence:** ev_direct_vs_indirect_0022

- **Data Exfiltration from Slack AI via indirect prompt injection** — PromptArmor (promptarmor.substack.com, August 2024).
  - **Source:** https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via
  - **Code:** —
  - **Mechanism:** Indirect-prompt-injection class disclosure in Slack AI's RAG-over-channels feature: an attacker with only public-channel posting privileges can cause Slack AI to surface and exfiltrate private-channel content to later querents [claim_slack_ai_cross_channel_exfil]. Vector-and-impact only; consult the PromptArmor post for technical detail.
  - **Result:** Established that retrieval-augmented enterprise assistants leak cross-trust-boundary data when untrusted content sits inside the RAG corpus; Slack subsequently scoped retrieval and updated the trust boundary.
  - **Status:** Verified (no widely-known repo) (security disclosure).
  - **Evidence:** ev_direct_vs_indirect_0023

- **ShadowPrompt: How Any Website Could Have Hijacked Claude's Chrome Extension** — Yomtov, Koi Security (koi.ai blog, December 2025–January 2026).
  - **Source:** https://www.koi.ai/blog/shadowprompt-how-any-website-could-have-hijacked-anthropic-claude-chrome-extension
  - **Code:** —
  - **Mechanism:** DOM-XSS-class indirect prompt injection disclosure against the Anthropic Claude Chrome extension allowing any visited website to inject instructions into the extension's LLM session [claim_shadowprompt_claude_chrome]. Impact-and-class only; full technical detail in Koi's disclosure post.
  - **Result:** Fixed in Claude Chrome extension v1.0.41; demonstrates that browser-extension agentic surfaces inherit indirect-injection risk from arbitrary visited web pages.
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0024

- **The Trifecta: How Three New Gemini Vulnerabilities in Cloud Assist, Search Model, and Browsing Allowed Private Data Exfiltration** — Matan, Tenable (tenable.com, 2025).
  - **Source:** https://www.tenable.com/blog/the-trifecta-how-three-new-gemini-vulnerabilities-in-cloud-assist-search-model-and-browsing
  - **Code:** —
  - **Mechanism:** Tenable Research disclosure of three vulnerabilities in the Google Gemini AI assistant — across Cloud Assist, Search Model, and Browsing — that "could have exposed users to critical data privacy risks" via indirect prompt injection [claim_gemini_trifecta_three_vulns]. Each vulnerability is described at the class-and-impact level; consult the disclosure post for component-level detail.
  - **Result:** All three vulnerabilities reported to Google and remediated; canonical example of indirect-injection surface multiplying across product modules within a single assistant.
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0025

- **Agentic Browser Security: Indirect Prompt Injection in Perplexity Comet** — Chaikin & Sahib, Brave (brave.com, 2025).
  - **Source:** https://brave.com/blog/comet-prompt-injection/
  - **Code:** —
  - **Mechanism:** Disclosure that "the attack we developed shows that traditional Web security assumptions don[']t hold" for AI-agentic browsers like Perplexity Comet, where retrieved web content can act as instruction input [claim_comet_indirect_injection]. Vulnerability class-and-impact framing only.
  - **Result:** Documents that indirect-injection risk extends to whole-browser agentic surfaces; Brave's framing motivates same-origin-style trust boundaries for AI browser features.
  - **Status:** Verified (no widely-known repo) (security disclosure) (recheck after 2026-08-20).
  - **Evidence:** ev_direct_vs_indirect_0026

- **Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems** — Hackett et al. (LLMSec 2025, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2504.11168
  - **Code:** —
  - **Mechanism:** Empirical evaluation of character-injection and adversarial-ML evasion against leading content-classifier guardrails [claim_guardrail_evasion_100pct]. Findings reported at the abstract-and-conclusion level; attack mechanics intentionally not reproduced here per ADR-041.
  - **Result:** Reports near-total evasion ASR (up to 100%) of character-injection variants against Azure Prompt Shield and Meta Prompt Guard; argues content-classifier guardrails are structurally insufficient as the sole defense layer.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0027

- **Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** — Bhagwatkar et al. (NeurIPS 2025, arXiv preprint).
  - **Source:** https://arxiv.org/abs/2510.05244
  - **Code:** —
  - **Mechanism:** Demonstrates that a minimal Tool-Input + Tool-Output firewall achieves near-perfect security on existing indirect-injection benchmarks (AgentDojo, ASB, InjecAgent, τ-Bench) — but the authors frame this as a critique of benchmark saturation, not defense adequacy [claim_firewalls_benchmark_saturation]. Findings reported at the abstract-and-conclusion level.
  - **Result:** Argues the community needs stronger adaptive-attacker benchmarks before any architectural defense can be declared sufficient; motivates the Nasr et al. and 2026 adaptive-benchmark work.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0028

- **The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections** — Nasr et al. (2025).
  - **Source:** https://arxiv.org/abs/2510.09023
  - **Code:** —
  - **Mechanism:** Argues that "we should evaluate defenses against adaptive attackers who explicitly modify their attack strategy to counter a defense" rather than against fixed-attack benchmarks [claim_attacker_moves_second_adaptive]. Establishes adaptive-attacker evaluation as the methodological standard.
  - **Result:** Empirically demonstrates that defenses reporting strong fixed-attack ASR reductions fall to adaptive attackers; co-anchor (with Bhagwatkar) of the 2025-2026 turn toward adaptive evaluation.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0029

- **How Not to Detect Prompt Injections with an LLM** — Choudhary et al. (2025).
  - **Source:** https://arxiv.org/abs/2507.05630
  - **Code:** —
  - **Mechanism:** Identifies a structural vulnerability in known-answer-detection (KAD) prompt-injection detectors that have reported "near-perfect performance by observing an LLM's output to classify input data as clean or contaminated" [claim_kad_structural_vulnerability] — the authors' adaptive DataFlip attack reduces KAD detection rate to near zero while preserving attacker utility. Mechanism reported at abstract level only.
  - **Result:** Demonstrates that an entire class of LLM-based content-classifier detectors is structurally bypassable; reinforces the Bhagwatkar critique of detector-only defenses.
  - **Status:** Verified (no widely-known repo) (recheck after 2026-08-20 — active freshness tier).
  - **Evidence:** ev_direct_vs_indirect_0030

---
13 entries
