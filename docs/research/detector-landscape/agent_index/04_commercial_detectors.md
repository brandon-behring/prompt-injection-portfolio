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
