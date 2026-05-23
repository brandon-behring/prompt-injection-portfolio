# # E5 — Production RAG-injection incidents

_7 entries covering EchoLeak + Slack AI + Comet + Gemini memory + ChatGPT MD exfil (vulnerability-class only per ADR-041)._


## E5.1. Breaking down 'EchoLeak', the First Zero-Click AI Vulnerability Enabling Data Ex

- **Breaking down 'EchoLeak', the First Zero-Click AI Vulnerability Enabling Data Exfiltration from Microsoft 365 Copilot** — Aim Labs / Cato Networks (2025).
  - **Source:** https://www.catonetworks.com/blog/breaking-down-echoleak/
  - **Code:** —
  - **Mechanism:** EchoLeak (CVE-2025-32711, CVSS 9.3, Aim Labs June 2025) — first publicly documented zero-click XPIA in production Microsoft 365 Copilot; RAG-specific layer is…
  - **Result:** CVE-2025-32711
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0006


## E5.2. Data Exfiltration from Slack AI via indirect prompt injection

- **Data Exfiltration from Slack AI via indirect prompt injection** — PromptArmor (2024).
  - **Source:** https://promptarmor.substack.com/p/data-exfiltration-from-slack-ai-via
  - **Code:** —
  - **Mechanism:** Data Exfiltration from Slack AI
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0007


## E5.3. Agentic Browser Security: Indirect Prompt Injection in Perplexity Comet

- **Agentic Browser Security: Indirect Prompt Injection in Perplexity Comet** — Chaikin & Sahib (2025).
  - **Source:** https://brave.com/blog/comet-prompt-injection/
  - **Code:** —
  - **Mechanism:** Indirect Prompt Injection in Perplexity Comet
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0016


## E5.4. Unseeable prompt injections in screenshots: more vulnerabilities in Comet and ot

- **Unseeable prompt injections in screenshots: more vulnerabilities in Comet and other AI browsers** — Sahib & Chaikin (2025).
  - **Source:** https://brave.com/blog/unseeable-prompt-injections/
  - **Code:** —
  - **Mechanism:** Unseeable prompt injections in screenshots
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0017


## E5.5. Hacking Gemini's Memory with Prompt Injection and Delayed Tool Invocation

- **Hacking Gemini's Memory with Prompt Injection and Delayed Tool Invocation** — Rehberger (2025).
  - **Source:** https://embracethered.com/blog/posts/2025/gemini-memory-persistence-prompt-injection/
  - **Code:** —
  - **Mechanism:** Hacking Gemini's Memory with Prompt Injection and Delayed Tool Invocation
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0018


## E5.6. ChatGPT Plugins: Data Exfiltration via Images & Cross Plugin Request Forgery

- **ChatGPT Plugins: Data Exfiltration via Images & Cross Plugin Request Forgery** — Rehberger (2023).
  - **Source:** https://embracethered.com/blog/posts/2023/chatgpt-webpilot-data-exfil-via-markdown-injection/
  - **Code:** —
  - **Mechanism:** ChatGPT Plugins: Data Exfiltration via Images
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0019


## E5.7. Prompt Injections are bad, mkay? (Bing Chat / Indirect Prompt Injection advisory

- **Prompt Injections are bad, mkay? (Bing Chat / Indirect Prompt Injection advisory companion to Greshake et al. AISec 2023)** — Greshake et al. (2023).
  - **Source:** https://greshake.github.io/
  - **Code:** —
  - **Mechanism:** Indirect Prompt Injection
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0020
