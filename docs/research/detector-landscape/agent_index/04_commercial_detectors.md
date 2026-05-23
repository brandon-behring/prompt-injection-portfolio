# A4. Commercial / proprietary detectors

Vendor-hosted prompt-injection detection products and their canonical benchmarks. The PINT leaderboard (§ A4.1, § A4.2) is the de facto industry comparison for these products despite the Lakera-designed-and-Lakera-evaluated structural-alignment caveat noted in the scope boundary. Treat vendor-reported numbers with skepticism throughout this section; the only independent reconciliations come from the PromptShield Berkeley paper (§ A3.1), the Firewalls NeurIPS paper (§ A5.12), and the "Attacker Moves Second" study (§ A5.15). All `vendor blog` and `Vendor documentation` Status flags are inline on the affected entries — see the scope-boundary section in the README.

## A4.1. Lakera PINT Benchmark blog (Lakera)

- **Lakera's Prompt Injection Test (PINT) — A New Benchmark for Evaluating Prompt Injection Solutions** — Lakera (Vendor blog, 2024).
  - **Source:** https://www.lakera.ai/product-updates/lakera-pint-benchmark
  - **Code:** https://github.com/lakeraai/pint-benchmark
  - **Mechanism:** Lakera's announcement blog for the PINT benchmark — a curated prompt-injection test set used to compare detection solutions (commercial guardrails alongside open-source HF model cards) [claim_detector_landscape_0017_01].
  - **Result:** Blog post documents the benchmark methodology; quantitative leaderboard entries live in the companion GitHub repo (§ A4.2). The benchmark is positioned as a Lakera contribution to the open-source community, but is also the headline metric used to compare Lakera Guard against competitors — note the structural caveat in the scope-boundary section of the README.
  - **Status:** Verified. (vendor blog) Definitive reference for the PINT methodology design intent. [ev_detector_landscape_0018]

## A4.2. lakeraai/pint-benchmark (Lakera AI)

- **lakeraai/pint-benchmark: A benchmark for prompt injection detection systems** — Lakera AI (GitHub repository, 2025).
  - **Source:** https://github.com/lakeraai/pint-benchmark
  - **Code:** https://github.com/lakeraai/pint-benchmark
  - **Mechanism:** Open-source GitHub repository hosting the PINT benchmark dataset, evaluation harness, and leaderboard tables; tracks scores for commercial detectors (Lakera Guard, Azure Prompt Shields, AWS Bedrock Guardrails, Google Model Armor, Aporia, etc.) alongside open-source models (deepset DeBERTa, ProtectAI DeBERTa, Meta Prompt Guard family) [claim_detector_landscape_0018_01]. Leaderboard entries from May 2025 through August 2025 are referenced in `research_plan.md`.
  - **Result:** Repo serves as the canonical PINT leaderboard surface. Specific score values for individual detectors are `(unverified body claim)` since they're not in abstract-equivalent area and rotate quarterly; the Google Model Armor 70.0664% row from 2025-08-27 is one snapshot visible in the cached repo content.
  - **Status:** Verified. (vendor repo; scores rotate quarterly) [ev_detector_landscape_0019]

## A4.3. Lakera Guard product page (Lakera)

- **Lakera Guard — Prompt Injection Protection (vendor product page; Cisco AI Defense post-acquisition May 2025)** — Lakera (Vendor product page, 2025).
  - **Source:** https://www.lakera.ai/risk/prompt-injection-attacks
  - **Code:** —
  - **Mechanism:** Vendor product page for Lakera Guard, the prompt-injection protection product. Page surfaces the product positioning: "Lakera protects your AI from coercive inputs that hijack instructions, expose data, or break compliance" [claim_detector_landscape_0019_01]. Specific architecture / mechanism details (parameter count, base model, training-data composition) are not disclosed on the public page. Cisco AI Defense acquisition context (unverified, 2026-05-22) — not anchored on the Lakera product page itself; cross-reference at § A4.8 is paraphrase-only.
  - **Result:** Vendor product page — no quantitative claim is anchored in the abstract-equivalent area. PINT leaderboard (§ A4.2) is the headline metric Lakera uses to position the product.
  - **Status:** Verified. (vendor product page; post-acquisition into Cisco AI Defense) [ev_detector_landscape_0020]

## A4.4. Azure AI Prompt Shields (Microsoft)

- **Prompt Shields in Azure AI Content Safety (User Prompt + Document attacks; Spotlighting capability)** — Microsoft (Vendor documentation, 2025).
  - **Source:** https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/jailbreak-detection
  - **Code:** —
  - **Mechanism:** Azure AI Content Safety's prompt-injection detection feature — distinguishes "User Prompt" attacks (direct injection) from "Document" attacks (indirect injection via tool outputs / retrieved content) [claim_detector_landscape_0020_01]. The Microsoft "Spotlighting" technique is referenced in the broader Microsoft AI-safety story (see `../direct-vs-indirect/`) but is not anchored as a Prompt Shields capability on this product docs page (unverified, 2026-05-22).
  - **Result:** Vendor documentation — no quantitative claim is anchored in the abstract-equivalent area. PINT leaderboard entries for Azure Prompt Shields rotate quarterly (§ A4.2); the Bypassing Guardrails paper (§ A5.13) reports up to 100% evasion success against Azure Prompt Shield via character-injection methods.
  - **Status:** Verified. (vendor documentation) [ev_detector_landscape_0021]

## A4.5. Amazon Bedrock Guardrails — prompt attacks (AWS)

- **Detect prompt attacks with Amazon Bedrock Guardrails (Jailbreaks + Prompt Injection + Prompt Leakage)** — AWS (Vendor documentation, 2025).
  - **Source:** https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-prompt-attack.html
  - **Code:** —
  - **Mechanism:** AWS Bedrock Guardrails' prompt-attack detection feature — covers jailbreaks, prompt injection, and prompt leakage as a unified detection layer. Page is a JavaScript-required documentation surface; the anchor span is the JavaScript-disabled fallback text rather than a substantive mechanism description [claim_detector_landscape_0021_01].
  - **Result:** Vendor documentation — no quantitative claim is anchored in the abstract-equivalent area. Categorization of jailbreaks alongside prompt-injection and prompt-leakage is the design choice; PINT leaderboard entries for Bedrock Guardrails are in § A4.2.
  - **Status:** Verified. (vendor documentation; doc surface is JavaScript-required) [ev_detector_landscape_0022]

## A4.6. Google Cloud Model Armor (Google Cloud)

- **Google Cloud Model Armor — Prompt injection / jailbreak / malicious-URL / PII filter (GA)** — Google Cloud (Vendor product page, 2025).
  - **Source:** https://cloud.google.com/security/products/model-armor
  - **Code:** —
  - **Mechanism:** Google Cloud Model Armor — a runtime safety layer for generative and agentic AI applications. Vendor page positions it as covering prompt injection, sensitive data leaks, and harmful content as the headline protections [claim_detector_landscape_0022_01]. GA-status product per the vendor page header.
  - **Result:** Vendor product page — no quantitative claim is anchored in the abstract-equivalent area. PINT leaderboard records 70.0664% for Google Model Armor as of 2025-08-27 (cached snapshot in § A4.2); treat this as a single time-point and re-verify before citing.
  - **Status:** Unverified. (vendor product page; PINT score is a snapshot, rotates quarterly) [ev_detector_landscape_0023]

## A4.7. NVIDIA NeMo Guardrails — Injection Detection (NVIDIA)

- **NVIDIA NeMo Guardrails — Configuring Injection Detection (YARA-based; SQLi, XSS, template, code injection)** — NVIDIA (Vendor documentation, 2025).
  - **Source:** https://docs.nvidia.com/nemo/microservices/latest/guardrails/tutorials/injection-detection.html
  - **Code:** —
  - **Mechanism:** NeMo Guardrails' Injection Detection feature uses YARA-rule-based pattern matching to detect classic security-injection attack signatures: code injection, cross-site scripting (XSS), SQL injection, and template injection [claim_detector_landscape_0023_01]. Note this is structurally different from the prompt-injection (instruction-hijacking) detection covered elsewhere in this section — NVIDIA's injection detector targets traditional security-engineering injection signatures rather than natural-language instruction hijacking.
  - **Result:** Vendor documentation — no quantitative claim is anchored in the abstract-equivalent area. Listed here as the canonical example of a vendor product that uses YARA / signature-based detection rather than ML-classifier detection — useful to distinguish from the encoder-classifier and LLM-judge entries elsewhere.
  - **Status:** Verified. (vendor documentation; signature-based detector, not ML-classifier) [ev_detector_landscape_0024]

## A4.8. Cisco AI Defense (Cisco — post-Robust-Intelligence-acquisition + Lakera integration)

- **Security for the Agentic Era: Cisco AI Defense (Robust Intelligence post-acquisition AI Firewall + Lakera Guard integration)** — Cisco (Vendor blog, 2025).
  - **Source:** https://blogs.cisco.com/ai/security-for-the-agentic-era-cisco-ai-defense-breaks-new-ground
  - **Code:** —
  - **Mechanism:** Cisco AI Defense — the consolidated enterprise AI security product line (Feb 2026 blog post). Blog positions Cisco AI Defense as "the industry's first truly comprehensive enterprise AI security solution" [claim_detector_landscape_0024_01] (verbatim anchored at cache offset 1312-1444). Robust Intelligence and Lakera Guard acquisition context (unverified, 2026-05-22) — discussed in broader Cisco product narrative but not anchored verbatim on this blog page.
  - **Result:** Vendor blog — no quantitative claim is anchored in the abstract-equivalent area. Acquisition history (Robust Intelligence ~2024, Lakera ~May 2025) is widely reported elsewhere but the specific integration details are not anchored on this blog page.
  - **Status:** Unverified. (vendor blog; specific integration claims unverified, 2026-05-22) [ev_detector_landscape_0025]

## A4.9. protectai/rebuff (Protect AI)

- **protectai/rebuff: LLM Prompt Injection Detector (4-layer: heuristic + LLM-judge + VectorDB + canary tokens; archived 2025-05)** — Protect AI (GitHub repository, 2023).
  - **Source:** https://github.com/protectai/rebuff
  - **Code:** https://github.com/protectai/rebuff
  - **Mechanism:** 4-layer self-hardening prompt-injection detector: (1) heuristic regex rules, (2) LLM-as-judge layer, (3) VectorDB similarity to known injection prompts, (4) canary tokens for detecting exfiltration. Repo positions the model as a "self-hardening prompt injection detector"; cache surface anchors GitHub feedback footer [claim_detector_landscape_0025_01]. Archived 2025-05 per bib_ledger title field (`retrieved 2026-05-22`).
  - **Result:** GitHub repo surface — no quantitative claim is anchored in abstract-equivalent area. Historically the canonical multi-layer detector architecture; superseded by single-LLM-judge approaches (PromptArmor § A3.7) and game-theoretic approaches (DataSentinel § A5.10).
  - **Status:** Verified. (vendor repo; archived 2025-05) Listed for historical / architectural-reference value rather than active deployment recommendation. [ev_detector_landscape_0026]

## A4.10. Meta Llama Prompt Guard 2 product doc (Meta)

- **Llama Prompt Guard 2 — Model Cards and Prompt formats (official Meta product documentation)** — Meta (Vendor documentation, 2025).
  - **Source:** https://www.llama.com/docs/model-cards-and-prompt-formats/prompt-guard/
  - **Code:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
  - **Mechanism:** Official Meta product documentation page for Llama Prompt Guard 2; positions the product line as "LLM-powered applications are susceptible to prompt attacks, which are prompts intentionally designed to subvert the intended behavior of the LLM as specified by the developer" [claim_detector_landscape_0026_01]. Cross-references the HF model cards at § A3.3 (86M) and § A3.4 (22M) for technical details.
  - **Result:** Vendor product doc — no quantitative claim is anchored in the abstract-equivalent area. Companion to the HF model cards; provides Meta-side positioning prose that the HF cards omit.
  - **Status:** Verified. (vendor documentation; complements HF model cards at § A3.3, § A3.4) [ev_detector_landscape_0027]

## A4.11. ProtectAI llm-guard (Protect AI)

- **protectai/llm-guard: The Security Toolkit for LLM Interactions (production deployment toolkit wrapping ProtectAI detectors)** — Protect AI (GitHub repository, 2024).
  - **Source:** https://github.com/protectai/llm-guard
  - **Code:** https://github.com/protectai/llm-guard
  - **Mechanism:** Production-grade deployment toolkit wrapping the ProtectAI detector family (DeBERTa-v3-base / small at § A2.1, § A2.2, § A2.6); README anchors the tagline "The Security Toolkit for LLM Interactions" [claim_detector_landscape_0048_01]. Sister-product to the rebuff layered detector at § A4.9.
  - **Result:** GitHub repo surface — no quantitative claim is anchored. Practitioner reference value is as the canonical pipeline glue around the ProtectAI HF detectors for input/output scanning.
  - **Status:** Verified. (vendor repo; deployment toolkit) [ev_detector_landscape_0049]

## A4.12. Lakera Guard product page — Check Point post-acquisition (Lakera)

- **Lakera Guard — AI Agent Security: Runtime visibility and protection for AI applications and agents (Check Point post-acquisition)** — Lakera / Check Point (Vendor product page, 2026).
  - **Source:** https://www.lakera.ai/lakera-guard
  - **Code:** —
  - **Mechanism:** Lakera Guard product page following Check Point's acquisition of Lakera; page positions the product as "AI Agent Security: Runtime visibility and protection for AI applications and agents" [claim_detector_landscape_0049_01]. Supersedes the standalone Lakera Guard positioning at § A4.3; product is now part of the Check Point AI-security portfolio.
  - **Result:** Vendor product page — no independent quantitative claim is anchored. Reconcile with PINT-leaderboard structural-alignment caveat (README "Verification & limits") and § A5.16 industry postmortem for vendor-number skepticism.
  - **Status:** Verified. (vendor product page; Check Point acquisition context) Re-verify after 2026-08-22. [ev_detector_landscape_0050]

## A4.13. Lakera Year-of-the-Agent Q4 2025 blog (Lakera)

- **The Year of the Agent: What Recent Attacks Revealed in Q4 2025 (and What It Means for 2026)** — Lakera Team (Vendor blog, 2026).
  - **Source:** https://www.lakera.ai/blog/the-year-of-the-agent-what-recent-attacks-revealed-in-q4-2025-and-what-it-means-for-2026
  - **Code:** —
  - **Mechanism:** Lakera's Q4 2025 retrospective blog on agentic-attack trends; positions 2025 as "The Year of the Agent" [claim_detector_landscape_0050_01]. Vendor-side framing prose that contextualizes Lakera Guard's product positioning at § A4.3 / § A4.12.
  - **Result:** Vendor blog — no independent quantitative benchmark claims; reference value is as Lakera's narrative framing of the threat landscape, useful for vendor-positioning context only.
  - **Status:** Verified. (vendor blog; narrative framing) Treat as vendor-positioning prose, not benchmark evidence. [ev_detector_landscape_0051]

## A4.14. Azure AI Prompt Shields GA announcement (Microsoft)

- **Azure AI announces Prompt Shields GA (Microsoft Tech Community announcement, Sept 2024)** — Microsoft (Vendor blog, 2024).
  - **Source:** https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/azure-ai-announces-prompt-shields-ga/4236033
  - **Code:** —
  - **Mechanism:** Microsoft's Sept 2024 general-availability announcement for Azure Prompt Shields; companion to the Azure AI Foundry docs at § A4.4 [claim_detector_landscape_0051_01]. The GA announcement marks Prompt Shields' move from preview to production-ready status within Azure AI Content Safety.
  - **Result:** Vendor blog — GA announcement, no independent quantitative claims; cross-reference § A4.4 for the technical detection-category breakdown (jailbreak / indirect attacks / Spotlighting).
  - **Status:** Verified. (vendor blog; GA milestone) [ev_detector_landscape_0052]

## A4.15. Anthropic Claude-for-Chrome browser-PI defenses (Anthropic)

- **Piloting Claude in Chrome (Anthropic browser-PI defenses; permissions framework, blocklists, classifiers; ASR 23.6 to 11.2%, 0% on browser-specific attacks)** — Anthropic (Vendor blog, 2025).
  - **Source:** https://claude.com/blog/claude-for-chrome
  - **Code:** —
  - **Mechanism:** Anthropic blog announcing Claude-for-Chrome browser integration and its PI-defense stack — permissions framework, site blocklists, classifier-based screening; blog headline anchors "Piloting Claude in Chrome" [claim_detector_landscape_0052_01]. ASR reductions per bib_ledger title (23.6% to 11.2% overall, 0% on browser-specific attacks) are `(unverified body claim)` since not in the headline-anchored span.
  - **Result:** Vendor blog — ASR-reduction headline numbers are vendor-self-reported and should be treated per the README "vendor numbers with skepticism" caveat. Reference value is as the canonical Anthropic-side browser-PI defense documentation.
  - **Status:** Verified. (vendor blog; self-reported ASR deltas) Re-verify after 2026-08-22. [ev_detector_landscape_0053]

## A4.16. Anthropic Mitigate-Jailbreaks Claude API docs (Anthropic)

- **Mitigate jailbreaks and prompt injections (Anthropic Claude API docs — defensive recipes: harmlessness screens, input validation, prompt engineering, monitoring)** — Anthropic (Vendor documentation, 2024).
  - **Source:** https://platform.claude.com/docs/en/docs/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks
  - **Code:** —
  - **Mechanism:** Anthropic Claude API documentation page on defensive recipes — harmlessness screens, input validation, prompt engineering, monitoring; page title anchors "Mitigate jailbreaks and prompt injections" [claim_detector_landscape_0053_01]. The official Anthropic-side companion to § A4.15 (Claude-for-Chrome) for non-browser deployments.
  - **Result:** Vendor docs — no independent quantitative claims; the page's value is as a checklist of Anthropic-recommended defensive practices for Claude API consumers.
  - **Status:** Verified. (vendor documentation; defensive-recipes checklist) [ev_detector_landscape_0054]

## A4.17. HiddenLayer AI Security Platform (HiddenLayer)

- **HiddenLayer AI Security Platform (commercial agentic-AI security; deterministic classifiers outside inference path; 2026 Threat Landscape Report)** — HiddenLayer (Vendor product page, 2026).
  - **Source:** https://hiddenlayer.com/platform/
  - **Code:** —
  - **Mechanism:** HiddenLayer's commercial agentic-AI security platform; product page positions itself as "Most Comprehensive AI Security Platform" with deterministic classifiers run outside the LLM inference path [claim_detector_landscape_0059_01]. Companion 2026 Threat Landscape Report is referenced from the same page.
  - **Result:** Vendor product page — no independent benchmark numbers; treat as private-detector vendor reference (see README scope-boundary note on privately-trained vendor detectors).
  - **Status:** Unverified. (vendor product page; privately-trained detector, no published benchmarks) Surfaced from compass scan; included for completeness of the commercial-detector landscape. [ev_detector_landscape_0060]

## A4.18. Robust Intelligence — Cisco acquisition announcement (Cisco)

- **Fortifying the future of Security for AI: Cisco Announces intent to acquire Robust Intelligence (Aug 2024; AI Firewall pioneer)** — Cisco (Vendor blog, 2024).
  - **Source:** https://blogs.cisco.com/news/fortifying-the-future-of-security-for-ai-cisco-announces-intent-to-acquire-robust-intelligence
  - **Code:** —
  - **Mechanism:** Cisco's Aug 2024 announcement of intent to acquire Robust Intelligence (pioneer of the "AI Firewall" product category); blog title anchors the acquisition headline [claim_detector_landscape_0060_01]. Companion to § A4.8 (Cisco AI Defense post-acquisition).
  - **Result:** Vendor blog — acquisition announcement, no benchmark numbers. Reference value is as the acquisition-timeline anchor for the Cisco AI Defense → Robust Intelligence + Lakera integration narrative.
  - **Status:** Unverified. (vendor blog; acquisition announcement) Surfaced from compass scan. [ev_detector_landscape_0061]

## A4.19. F5 AI Guardrails — CalypsoAI post-acquisition (F5 / CalypsoAI)

- **F5 AI Guardrails (CalypsoAI post-acquisition; commercial agentic-security platform)** — F5 / CalypsoAI (Vendor product page, 2026).
  - **Source:** https://www.f5.com/products/ai-guardrails
  - **Code:** —
  - **Mechanism:** F5's AI Guardrails product page following the CalypsoAI acquisition; product page anchors the "F5 AI Guardrails" identifier [claim_detector_landscape_0061_01]. Successor positioning for CalypsoAI's pre-acquisition agentic-security stack.
  - **Result:** Vendor product page — no independent benchmark numbers; treat as private-detector vendor reference.
  - **Status:** Unverified. (vendor product page; private-detector vendor) Surfaced from compass scan. [ev_detector_landscape_0062]

## A4.20. Vijil Dome — open-source agentic guardrail (Vijil AI)

- **vijilAI/vijil-dome: Vijil's Dome Repository (open-source agentic guardrail library; 20+ detectors; Apache 2.0)** — Vijil AI (GitHub repository, 2026).
  - **Source:** https://github.com/vijilAI/vijil-dome
  - **Code:** https://github.com/vijilAI/vijil-dome
  - **Mechanism:** Open-source agentic guardrail library shipping 20+ detectors under Apache 2.0; GitHub repo anchors the "vijilAI/vijil-dome: Vijil's Dome" identifier [claim_detector_landscape_0062_01]. Companion to the Vijil mBERT detector at § A1.3.
  - **Result:** GitHub repo surface — 20+ detectors claim per bib_ledger title is `(unverified body claim)`; repo positioning is as an open-source agentic guardrail framework alternative to guardrails-ai (§ A4.21).
  - **Status:** Unverified. (vendor repo; open-source guardrail framework) Surfaced from compass scan. [ev_detector_landscape_0063]

## A4.21. Guardrails AI — open-source framework (Guardrails AI)

- **guardrails-ai/guardrails: Adding guardrails to large language models (open-source Python framework; Apache 2.0)** — Guardrails AI (GitHub repository, 2026).
  - **Source:** https://github.com/guardrails-ai/guardrails
  - **Code:** https://github.com/guardrails-ai/guardrails
  - **Mechanism:** Open-source Python framework for adding guardrails to LLM applications; GitHub repo anchors "guardrails-ai/guardrails: Adding guardrails" [claim_detector_landscape_0063_01]. Apache 2.0 license; positioned as a vendor-neutral integration layer.
  - **Result:** GitHub repo surface — no benchmark numbers; reference value is as the canonical vendor-neutral open-source guardrail orchestration framework.
  - **Status:** Unverified. (vendor repo; open-source framework) Surfaced from compass scan. [ev_detector_landscape_0064]

## A4.22. SafePrompt — prompt-injection API launch (SafePrompt)

- **SafePrompt Launches Prompt Injection Protection API for AI Developers (Feb 2026 launch; multi-layer pipeline, <100ms latency)** — SafePrompt (Press release, 2026).
  - **Source:** https://natlawreview.com/press-releases/safeprompt-launches-prompt-injection-protection-api-ai-developers
  - **Code:** —
  - **Mechanism:** Press-release announcement of the SafePrompt prompt-injection-protection API launch (Feb 2026); release anchor is "SafePrompt Launches Prompt Injection Protection API" [claim_detector_landscape_0064_01]. Multi-layer pipeline + <100ms latency claims live in bib_ledger title and are `(unverified body claim)`.
  - **Result:** Press release — no independent benchmark verification; primary safeprompt.ai domain returned 403 at retrieval time per bib_ledger note, so this press release is the only available anchor.
  - **Status:** Unverified. (press release; secondary source — primary domain returned 403) Surfaced from compass scan. [ev_detector_landscape_0065]
