# Direct vs Indirect Prompt Injection: A Detector-Centric Deep Dive

## TL;DR
- **Indirect prompt injection (XPIA) is a fundamentally different problem from direct injection, and most text-classification detectors (ProtectAI, InjecGuard, even Meta Prompt Guard v1) handle it poorly.** In Microsoft's AgentDojo / LLMail-Inject settings, only purpose-built defenses like Meta Llama Prompt Guard 2 (81.2% Attack Prevention Rate at ≤3% utility loss), Task Shield (2.07% ASR), MELON (0.24% ASR), and structural defenses like Google DeepMind's CaMeL (77% provably-secure task completion versus 84% undefended on AgentDojo v2) achieve usable indirect protection, whereas legacy DeBERTa detectors land near 22% APR on the same benchmark.
- **No detector currently solves indirect injection by itself.** The community has converged on a multi-layer model: (1) a content classifier (Prompt Guard 2 / Azure Document Shield / PromptShield-Llama-3.1-8B) over untrusted inputs, (2) a structural defense that marks trust boundaries (Spotlighting, StruQ, SecAlign, OpenAI's Instruction Hierarchy), and (3) information-flow or capability-based isolation at the agent layer (CaMeL, Task Shield, MELON, AgentDojo-style tool filters, output filters for Markdown/URL exfiltration). EchoLeak (CVE-2025-32711, CVSS 9.3, June 2025) and the August 2025 "Month of AI Bugs" from Johann Rehberger demonstrate that any single layer is bypassable in practice.
- **For an engineering team in 2026, the right answer is to treat detectors as a noisy first filter, not a security boundary.** Deploy Prompt Guard 2 86M (or Azure Document Shield with Spotlighting) for cheap pre-filtering, fine-tune a SecAlign- or instruction-hierarchy-trained backbone for the primary LLM, restrict tool outputs and Markdown image/link rendering at the rendering layer, and adopt CaMeL-style data/control-flow separation for any agent with side effects.

## Key Findings

1. **The conceptual split is now codified.** OWASP's LLM01:2025 Prompt Injection lists direct injection (user-controlled input, "jailbreaking the system prompt") and indirect injection (malicious content arriving via retrieved documents, tool outputs, web pages) as the two sub-categories of the #1 LLM risk. MITRE ATLAS tracks them as AML.T0051.000 (Direct) and AML.T0051.001 (Indirect). The seminal Greshake et al. paper (arXiv 2302.12173, AISec '23) introduced "indirect prompt injection" and the taxonomy still in use: passive (poisoned websites/documents retrieved by the LLM), active (attacker delivers the payload directly into the victim's agent context — e.g., email), user-driven (a user is socially engineered into pasting malicious content), and hidden (white text, comments, Unicode tags, encoded payloads).

2. **Encoder classifiers are mostly direct-only by construction.** ProtectAI's DeBERTa v1/v2, InjecGuard, Fmops, and CodeIntegrity PromptGuard all operate on a single text input with no trust-boundary signal. The PromptShield paper (arXiv 2501.15145, ACM CODASPY '25) shows that at the 0.1% false-positive rate critical for production deployment, ProtectAI v1/v2 achieve 0.00% TPR (i.e., they detect nothing at deployable FPRs) and Meta PromptGuard v1 achieves 9.39%.

3. **Meta Prompt Guard v1 was the only encoder explicitly designed for the direct/indirect distinction at the label level.** Its multi-label output exposed a "JAILBREAK" label for direct user attacks and an "INJECTION" label intended specifically for third-party / tool-output / retrieved content — developers are instructed to run the INJECTION filter only over the untrusted side of the prompt. Prompt Guard 2 (April 2025) collapsed this into a binary classifier and dropped the explicit "injection" label, with Meta noting "we don't include a specific 'injection' label to detect prompts that may cause unintentional instruction-following. In practice, we found this objective too broad to be useful." Prompt Guard 2 86M reports 81.2% APR @ ≤3% utility loss on AgentDojo, versus ProtectAI's 22.2% — a striking generational gap.

4. **PromptShield (Llama-3.1-8B, Berkeley, 2025) is the first published LLM-based detector explicitly designed for the application-structured (indirect) setting**, with training data that splits "conversational" (chatbot) from "application-structured" (developer-prompt + untrusted-data) inputs. It achieves AUC 0.998 with 94.80% TPR at 1% FPR and 65.33% TPR at 0.1% FPR — roughly a 7× improvement over Meta PromptGuard v1 in the low-FPR regime.

5. **Azure separates the two threat classes at the API level.** Azure AI Content Safety's Prompt Shields exposes `userPromptAnalysis` and `documentsAnalysis` as independent fields. The Document Shield is explicitly an indirect-injection classifier, and Microsoft has added Spotlighting (base-64 encoding the document portion of the prompt) as a structural augmentation announced GA at Microsoft Build 2025.

6. **Architectural defenses outperform content classifiers on agentic benchmarks.** On AgentDojo (Debenedetti et al., NeurIPS 2024, arXiv 2406.13352 — 97 user tasks × 629 security cases across banking/Slack/travel/workspace), the strongest published numbers come from defenses that change the system architecture, not the detector: Google DeepMind's CaMeL achieves 77% of tasks solved with provable security (versus 84% undefended) by extracting control and data flows from the trusted query and tracking capabilities on every value; Task Shield achieves 2.07% ASR with 69.79% utility on GPT-4o; MELON achieves 0.24% ASR with 68.52% utility.

7. **Real-world exploitation has caught up.** EchoLeak (CVE-2025-32711, CVSS 9.3, disclosed June 2025 by Aim Labs against Microsoft 365 Copilot) was the first publicly documented zero-click indirect-injection exploit in a production LLM system — it bypassed Microsoft's XPIA classifier, Markdown link redaction, and Copilot's reference-mention guard, then exfiltrated data via auto-fetched reference-style Markdown images proxied through a trusted Microsoft Teams domain allowed by the Content Security Policy. Johann Rehberger's August 2025 "Month of AI Bugs" published a new prompt-injection vulnerability per day against ChatGPT, GitHub Copilot, Anthropic MCPs, Cursor, Amp, Devin, OpenHands, Claude Code, and Google Jules. Slack AI was shown vulnerable to data exfiltration via cross-channel indirect injection (PromptArmor, August 2024).

8. **Bench-to-real-world performance gaps are large.** Microsoft's LLMail-Inject challenge ran from December 2024 until February 2025 as one of the four official competitions of the 3rd IEEE Conference on Secure and Trustworthy Machine Learning (SaTML), and yielded 208,095 unique attack submissions from 839 participants. It found that even state-of-the-art defenses — including TaskTracker (activation-delta probe) and Spotlighting — are routinely bypassed by adaptive attackers in a realistic end-to-end RAG email-assistant pipeline.

## Details

### 1. Conceptual foundations — Greshake's threat model and the OWASP framing

In Greshake et al., "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection" (arXiv 2302.12173, AISec '23), the central claim is that "LLM-Integrated Applications blur the line between data and instructions… [enabling] adversaries to remotely (without a direct interface) exploit LLM-integrated applications by strategically injecting prompts into data likely to be retrieved." The paper's taxonomy still organizes the field:

- **Passive indirect injection**: malicious prompts hidden in webpages, public documents, or repositories that an LLM eventually retrieves (via search, RAG, or browsing).
- **Active indirect injection**: the attacker actively delivers the payload into the victim's context (the canonical instance is sending an email that a Copilot/Outlook assistant later summarizes — EchoLeak).
- **User-driven indirect injection**: a user is socially engineered into pasting attacker-controlled text into their own assistant.
- **Hidden injection**: the payload is visually invisible to a human reader (white text, HTML comments, zero-width Unicode, Unicode tag characters, ANSI escape codes, base-64 / homoglyph encodings, image steganography).

OWASP's LLM01:2025 Prompt Injection formalizes both flavors: "Direct prompt injections occur when a user's prompt input directly alters the behavior of the model… Indirect prompt injections occur when an LLM accepts input from external sources, such as websites or files." OWASP notes that indirect injections "do not need to be human-visible/readable, as long as the text is parsed by the LLM."

**Why indirect is fundamentally harder to detect**:

- **The trust-boundary problem.** A direct attack arrives in a single, well-defined channel (the user message); an encoder classifier scanning that channel has a real signal to learn (overt "ignore previous instructions" patterns). An indirect attack arrives concatenated to retrieved data, and at the token level the model sees no distinction between a developer's system prompt, a user's question, and 3,000 tokens of attacker-controlled email. As Simon Willison summarizes the issue in his April 11, 2025 analysis of CaMeL: "The original sin of LLMs that makes them vulnerable to this is when trusted prompts from the user and untrusted text from emails/web pages/etc are concatenated together into the same token stream. I called it 'prompt injection' because it's the same anti-pattern as SQL injection."
- **Distribution shift.** Indirect-injection payloads can look like ordinary documentation, code comments, or polite English. Meta's Prompt Guard v1 model card explicitly addresses this: "Commands that are benign in the context of user inputs (for example 'write me a poem') can be considered injections when placed out-of-context in outputs from third party APIs or tool outputs included into the context window of the LLM." A classifier with no awareness of source therefore faces an inherently ambiguous task.
- **Compositionality with side effects.** A direct jailbreak typically only causes the model to say something bad. An indirect injection in an agentic system can trigger a tool call (send email, transfer funds, exfiltrate via image rendering), so the same level of detection accuracy translates to vastly higher impact.

### 2. Detector coverage analysis

#### Encoder classifiers (ModernBERT, DeBERTa-based)

| Detector | Architecture | Direct coverage | Indirect coverage | Evidence |
|---|---|---|---|---|
| ProtectAI v1 | DeBERTa-v3-base, 184M | Strong on canonical "Ignore previous…" | **Weak**: 22.2% APR on AgentDojo (Meta card); 0.00% TPR @ 0.1% FPR on PromptShield benchmark | PromptShield Table 4 |
| ProtectAI v2 | DeBERTa-v3-base, 184M | Moderate | **Weak**: 0.00% TPR @ 0.1% FPR | PromptShield Table 4 |
| InjecGuard | DeBERTa-v3-base, 184M | Moderate (AUC 0.765) | **Weak**: 6.61% TPR @ 0.1% FPR | PromptShield Table 4 |
| Fmops | DistilBERT, 67M | Weak (AUC 0.754) | **Weak**: 2.10% TPR @ 0.1% FPR | PromptShield Table 4 |
| Meta Prompt Guard v1 | mDeBERTa-v3-base, 86M/279M | Strong via JAILBREAK label | Limited — explicit INJECTION label for third-party content, but high false-positive rate; 9.39% TPR @ 0.1% FPR | PromptShield Table 4; Meta model card |
| **Meta Llama Prompt Guard 2 86M** | mDeBERTa-v3-base | Binary "malicious" label; recall 97.5% @ 1% FPR (English OOD) | **Best in class for encoders**: 81.2% APR @ ≤3% utility loss on AgentDojo | Meta Llama Prompt Guard 2 model card |
| Meta Llama Prompt Guard 2 22M | mDeBERTa-v3-xsmall | Recall 88.7% @ 1% FPR | 78.4% APR on AgentDojo | Meta model card |
| Hlyn judge-deberta-70m | DeBERTa, 70M | Optimized for English direct | No indirect-specific eval published | HF model card |
| Sentinel / CodeIntegrity PromptGuard | DeBERTa variants | Optimized for direct | No indirect benchmark coverage in public docs | Vendor materials |

The pattern is clear: **encoder classifiers trained on a single text input cannot reliably encode the source/trust of that input**, and at deployment-realistic FPRs (≤0.5%) their TPR on indirect-styled attacks collapses. Prompt Guard v1's design was unusual in attempting to split direct vs indirect at the label level; Meta abandoned this in v2 because the "INJECTION" label generalized poorly across applications. The compensating move was to train v2 on a much broader corpus and rely on the developer to scan the right segments of the prompt.

#### LLM-based detectors

- **PromptShield (Berkeley, arXiv 2501.15145).** Fine-tunes Llama-3.1-8B-Instruct on a curated benchmark that explicitly distinguishes conversational vs application-structured inputs (i.e., developer-prompt-concatenated-with-untrusted-data). Achieves AUC 0.998, TPR 94.80% @ 1% FPR, 65.33% @ 0.1% FPR, 47.53% @ 0.05% FPR — the strongest published detection numbers in the low-FPR regime, and the first detector explicitly trained and evaluated on indirect-style prompts. The paper compares to Meta PromptGuard's self-reported "TPR of 71% and FPR of 1%" and shows that "without careful design and evaluation, prompt injection detectors might not be suitable for deployment."
- **Meta Prompt Guard v1 (mDeBERTa-v3-base, 86M).** Multi-label: BENIGN / INJECTION / JAILBREAK. The INJECTION label is documented as for "scanning content from untrusted third party sources, like tools, web searches, or APIs"; JAILBREAK is for user-side scanning. The cleanest public example of a detector that operationalizes the direct/indirect distinction. In practice users report high false-positive rates on benign third-party content.
- **Meta Llama Prompt Guard 2 (86M and 22M, April 2025).** Binary classifier, drops the explicit injection sub-label. Major architectural improvement on out-of-distribution and indirect content: 97.5% recall @ 1% FPR on Meta's private OOD jailbreak set, and 81.2% APR @ ≤3% utility loss on AgentDojo (vs ProtectAI's 22.2%). LlamaFirewall (arXiv 2505.03574) confirms: "PromptGuard v2 86M offers the best overall tradeoff—achieving a 57% reduction in ASR with negligible utility loss (1.5%)."
- **Llama Guard family.** Llama Guard 1/2/3/4 are content-safety classifiers (CSAM, violence, etc.) rather than prompt-injection classifiers, and do not have indirect-injection coverage by design.

#### Commercial detectors

- **Azure AI Prompt Shields** is the most architecturally explicit: a single API with `userPrompt` and `documents` arrays, returning `userPromptAnalysis.attackDetected` and `documentsAnalysis[].attackDetected`. The Document Shield "aims to safeguard against attacks that use information not directly supplied by the user or developer, such as external documents," and Microsoft has stacked **Spotlighting** on top of it — at Build 2025, Spotlighting went GA, transforming document content via base-64 encoding "so the model treats it as less trustworthy than direct user and system prompts."
- **AWS Bedrock Guardrails** offer a `PROMPT_ATTACK` filter that applies to user input only; AWS recommends tagging input as `[INPUT]` vs `[TOOL_RESULT]` via prompt templates so the model and guardrail can apply different policies. Indirect coverage is implementation-specific.
- **Lakera Guard** evaluates with the PINT benchmark, which includes some document-flavored scenarios but is dominated by direct attacks. Lakera's own "Indirect Prompt Injection" blog acknowledges the limits of content classification and advocates for output-side controls.
- **Google Model Armor** (2025) markets RAG-context indirect-injection detection as a separate capability; published benchmark numbers are limited.
- **NVIDIA NeMo Guardrails** uses a dialog-flow policy approach with a built-in `prompt_security_check` rail; indirect coverage depends on operator configuration.

#### Specialized indirect-injection defenses (architectural)

These are not "detectors" in the classifier sense — they are model- or system-level changes:

- **Spotlighting** (Hines et al., Microsoft, arXiv 2403.14720, CAMLIS 2024). Three variants: *delimiting* (wrap untrusted content in `[START]…[END]`); *datamarking* (replace every whitespace in untrusted content with a marker token like `^`); *encoding* (base-64 or similar). Per the abstract: "Using GPT-family models, we find that spotlighting reduces the attack success rate from greater than 50% to below 2% in our experiments with minimal impact on task efficacy" (tested on GPT-3.5-Turbo and GPT-4). Datamarking has near-zero downstream task degradation; encoding is most effective but requires a high-capacity model (GPT-4 class) to decode.
- **StruQ** (Chen, Piet, Sitawarin, Wagner, USENIX Security 2025, arXiv 2402.06363). A secure front-end concatenates prompts and data using reserved delimiter tokens that are filtered out of any data, and a base (non-instruction-tuned) LLM is fine-tuned to follow instructions only in the prompt channel. Order-of-magnitude ASR reductions on hand-crafted and optimization-based attacks.
- **SecAlign** (Chen et al., CCS 2025, arXiv 2410.05451). Builds preference-optimization pairs of (prompt-injected input, secure response, insecure response) and uses DPO to teach the LLM to prefer the secure response. "Reduces the success rates of various prompt injections to <10%, even against attacks much more sophisticated than ones seen during training." SecAlign Llama3-8B-Instruct achieves 8% ASR under the strongest optimization-based prompt injections evaluated.
- **Meta SecAlign** (Chen, Zharmagambetov, Wagner, Guo, arXiv 2507.02735, July 2025). Productionized SecAlign on Llama-3.3-70B-Instruct, introducing an `input` role separate from `system` and `user`.
- **Jatmo** (Piet et al., arXiv 2312.17673, ESORICS 2024). Task-specific fine-tuning of a non-instruction-tuned base model on outputs from a teacher instruction-tuned LLM, so the deployed model cannot follow injected instructions because it never learned general instruction-following. Per the abstract: "The best attacks succeeded in less than 0.5% of cases against our models, versus 87% success rate against GPT-3.5-Turbo. Only two prompt-injected inputs out of 23,400 succeeded against a Jatmo model." Threat model is narrow: single-task LLM only.
- **DataSentinel** (Liu, Jia et al., arXiv 2504.11358). Formulates detection as a minimax game between attacker and defender, fine-tuning a small detection LLM (Mistral-7B or Llama-3.2-1B) on a known-answer detection (KAD) signal. Achieves FPR ~0.00 / FNR ~0.00–0.01 across 7 target NLP tasks. The robustness paper "How Not to Detect Prompt Injections with an LLM" (arXiv 2507.05630) finds that DataSentinel is brittle under adaptive `DataFlip` attacks, with FNR "as large as 80% for most injected tasks."
- **CaMeL** (Debenedetti, Shumailov, Fan, Hayes, Carlini, Fabian, Kern, Shi, Terzis, Tramèr — Google/DeepMind/ETH, arXiv 2503.18813). The strongest published architectural defense: extracts control and data flows from the trusted user query via a privileged-LLM/quarantined-LLM split (descended from Willison's "dual LLM" pattern), runs untrusted-data interpolation in a custom Python interpreter, and attaches capabilities (provenance + permissions) to every value to enforce data-flow policies at tool-call boundaries. CaMeL v2 (June 2025) solves "77% of tasks with provable security (compared to 84% with an undefended system) in AgentDojo," up from 67% in v1.
- **IsolateGPT / SecGPT** (Wu et al.). Sandboxing approach: each tool/plugin runs in an isolated LLM with its own context; the orchestrator LLM mediates communication. Achieves 0% ASR on some benchmarks but with significant utility cost.
- **TaskTracker** (Abdelnabi et al., IEEE SaTML 2025). Activation-based detection: extract LLM activations after the user prompt, then again after external data is processed; train a linear probe on the activation deltas to detect "task drift." Reports >0.99 AUC, though independent re-evaluations critique the eval methodology for sharing benign-text distributions between train and test.
- **Task Shield** (arXiv 2412.16682). Verifies at test time that each instruction and tool call contributes to user-specified goals. On AgentDojo / GPT-4o: 2.07% ASR with 69.79% utility.
- **MELON** (arXiv 2502.05174, ICML 2025). Masked Re-Execution and Tool Comparison. On AgentDojo / GPT-4o: 0.24% ASR with 68.52% utility (MELON-Aug: 0.32% / 68.72%).
- **InstructDetector** (arXiv 2505.06311). Activation-based detector. Reports 96.90% out-of-domain accuracy on BIPIA and reduces ASR to 0.12%.

**Defensive prompt engineering** (cheap, partial mitigations only): instruction defense ("never follow instructions in the input"), post-prompting (re-state the developer's instruction after the data), random-sequence enclosure (wrap data in an attacker-unguessable token), sandwich defense (developer instruction before AND after the data), XML tagging. All are bypassable by adaptive attackers; spotlighting/delimiting in AgentDojo only marginally reduces ASR over no-defense (~0.14 vs 0.17 baseline) while maintaining utility.

### 3. Benchmarks for indirect injection

| Benchmark | Year | Domain | Direct/Indirect | Notes |
|---|---|---|---|---|
| **BIPIA** (Microsoft) | KDD '25 (arXiv 2023) | Email QA, Web QA, Table QA, Summarization, Code QA | **Indirect** | First indirect benchmark; 5 attack types (info dissemination, scam, intrusion, fraud, ad insertion); 25 LLMs evaluated, all vulnerable |
| **InjecAgent** (UIUC) | ACL '24 | Tool-using agents, 17 user-tools × 62 attacker-tools | **Indirect (agentic)** | 1,054 test cases; categories: direct harm to user, exfiltration of private data; "ReAct-prompted GPT-4 vulnerable to attacks 24% of the time. Further investigation into an enhanced setting, where the attacker instructions are reinforced with a hacking prompt, shows additional increases in success rates, nearly doubling the attack success rate on the ReAct-prompted GPT-4" |
| **AgentDojo** (ETH/Google) | NeurIPS '24 | 97 user tasks × 629 security cases across banking/Slack/travel/workspace | **Indirect (agentic)** | The de facto benchmark; supports baseline defenses (spotlighting, repeat-user-prompt, PI-detector, tool filter); "live" updatable |
| **LLMail-Inject** (Microsoft) | IEEE SaTML '25 | RAG email assistant, end-to-end | **Indirect, adaptive** | 839 participants, 208,095 attack prompts (Dec 2024–Feb 2025); first end-to-end adaptive challenge |
| Agent Security Bench (ASB) | ICLR '25 | Two-stage tool-use agents | **Indirect (agentic)** | Complementary to AgentDojo; broader attack/defense matrix |
| TensorTrust (ICLR '24) | 2024 | Prompt-extraction CTF game | **Direct** | Crowd-sourced; conversational |
| WIPI / tau-bench / ToolEmu | 2024–25 | Web-based, tool-use scenarios | **Indirect** | Smaller, used as supplementary |
| AgentDyn / AgentSentry / AgentVigil | 2026 | Adaptive red-teaming against AgentDojo | **Indirect, adversarial** | New 2026 benchmarks that critique earlier evals and propose adaptive attacks |

BIPIA's design (5 application scenarios × 5 attack-intent types × 50 attacker goals = 250 base attacks) is the most-used indirect benchmark for LLM (not detector) evaluation. The original Microsoft paper reports that "GPT-4 and GPT-3.5, which power the popular ChatGPT integrated applications, demonstrate relatively higher vulnerability under indirect prompt injection attacks," with ASRs as high as ~80% for GPT-4 in unmitigated configurations versus averages of 50–70% across all 25 evaluated models — a counterintuitive result attributed to stronger instruction-following.

### 4. Real-world incidents

| Incident | Date | Vector | Notes |
|---|---|---|---|
| ChatGPT Markdown image exfiltration | April 2023 (Rehberger, Samoilenko) | Plugin / web data → Markdown image render | OpenAI initially deemed it a "feature"; only partially mitigated |
| Bing Chat / Copilot manipulation via webpages | 2023 | Browsing webpage | Greshake et al. demonstrated arbitrary persona / data extraction |
| GitHub Copilot indirect injection | 2023–2024 | Hidden instructions in source code | Rehberger demonstrated remote data exfil |
| Google Bard / Gemini long-term memory poisoning | Sept 2024 (Rehberger) | Uploaded document → memory write → cross-session exfil | Google restricted Markdown link rendering |
| Slack AI cross-channel exfiltration | Aug 2024 (PromptArmor) | Public-channel message → RAG retrieval → Markdown link | Slack initially declined to fix; "intended behavior" |
| ChatGPT persistent memory injection | Sept 2024 (Rehberger) | False memories planted via document | OpenAI patched exfiltration channel only |
| **EchoLeak (CVE-2025-32711, CVSS 9.3)** | June 2025 (Aim Labs) | Single crafted email → Copilot RAG → Markdown image via Teams proxy | First publicly documented zero-click indirect prompt injection in production; bypassed XPIA, link redaction, CSP |
| Month of AI Bugs | Aug 2025 (Rehberger) | Daily-published vulnerabilities | ChatGPT, Codex, Anthropic MCPs, Cursor, Amp, Devin, OpenHands, Claude Code, GitHub Copilot, Google Jules |
| ShadowPrompt (Claude Chrome ext.) | Dec 2025–Jan 2026 (Koi) | DOM XSS on `a-cdn.claude.ai` → cross-origin postMessage → prompt injection | Fixed in v1.0.41 |
| Gemini Trifecta | 2025 | Search injection, log-to-prompt, indirect | Disclosed by multiple researchers |
| Comet (Perplexity) browser indirect injection | Aug 2025 (Brave) | Webpage content → cross-tab exfil | Banking/email credentials |

### 5. Why indirect detection is fundamentally harder

The deeper problem is that **content classification cannot reconstruct source attribution that the underlying transformer has already discarded**. When system prompt + user prompt + retrieved doc are concatenated into one token stream, no detector operating on that stream can distinguish "instruction" from "data" except by surface features (which adaptive attackers manipulate). Three theoretical observations follow:

1. **Information-theoretic limit.** As long as the LLM treats all tokens as equal-priority instructions, a detector's job is to identify a needle (malicious imperative) in a haystack of perfectly legitimate imperatives (the developer's own system prompt). The FP/FN tradeoff has no good operating point because both classes share surface features.
2. **Dual-LLM / privileged-vs-quarantined-LLM split (Willison 2023).** The structural fix is to give one LLM only trusted inputs and another LLM only untrusted ones; the latter cannot make tool calls or affect control flow. CaMeL formalizes this with a custom Python interpreter and capability metadata. The cost is utility (CaMeL drops from 84% to 77% benign task completion on AgentDojo v2) and ~2.8× input tokens / 2.7× output tokens.
3. **Scaling does not solve indirect.** BIPIA found GPT-4 *more* vulnerable than smaller models. AgentDojo's strongest backbones (Claude 3.5 Sonnet, GPT-4o) still show 10–25% baseline ASR under "important_instructions" attacks. Prompt Guard 2's improvement comes from training-data curation, not parameter count: the 22M model achieves 78.4% APR vs the 86M's 81.2%.

### 6. Detector performance on indirect benchmarks (head-to-head)

| Defense | Benchmark | ASR / detection metric | Source |
|---|---|---|---|
| No defense (baseline) | AgentDojo (GPT-4o, important-msg) | 17.6% ASR / 47.7% utility | LlamaFirewall reproduction |
| ProtectAI DeBERTa "PI-detector" | AgentDojo | ASR drops to ~8% (from baseline) | AgentDojo paper |
| Spotlighting (delimiting) | AgentDojo all suites (GPT-4o) | ASR 0.14 vs 0.17 baseline | AgentArmor paper |
| Tool filter | AgentDojo (GPT-4o) | ASR 7.5%, utility 53.3% | AgentDojo paper |
| Meta Prompt Guard 2 86M | AgentDojo | 81.2% APR @ ≤3% utility loss | Meta model card |
| ProtectAI on Meta's eval | AgentDojo | 22.2% APR | Meta model card |
| Task Shield | AgentDojo (GPT-4o) | 2.07% ASR / 69.79% utility | Task Shield paper |
| MELON | AgentDojo (GPT-4o) | 0.24% ASR / 68.52% utility | MELON paper |
| CaMeL v2 | AgentDojo | 77% provably-secure / 84% undefended | arXiv 2503.18813 v2 |
| InstructDetector | BIPIA (OOD) | 96.90% accuracy, ASR 0.12% | arXiv 2505.06311 |
| DataSentinel (Mistral-7B) | 7 NLP target-task eval | FPR ~0.00, FNR ~0.00–0.01 | DataSentinel paper |
| DataSentinel under adaptive DataFlip | Same, adversarial | FNR up to 80% worse than base Mistral | arXiv 2507.05630 |
| PromptShield Llama-3.1-8B | PromptShield benchmark (application-structured) | 94.80% TPR @ 1% FPR, 65.33% @ 0.1% FPR | PromptShield Table 4 |
| Meta PromptGuard v1 (86M) | Same | 12.78% @ 1% FPR, 9.39% @ 0.1% FPR | PromptShield Table 4 |
| ProtectAI v2 | Same | 1.97% @ 1% FPR, 0.00% @ 0.1% FPR | PromptShield Table 4 |

**Headline interpretation**:

- Among **encoder content classifiers**, Meta Prompt Guard 2 is now significantly ahead of all legacy DeBERTa detectors on indirect (agentic) benchmarks — a ~3–4× improvement in APR.
- Among **LLM-based content detectors**, PromptShield Llama-3.1-8B currently sets the bar in the low-FPR regime, but it is evaluated on its own benchmark and the field lacks independent reproduction.
- Among **architectural defenses**, CaMeL, Task Shield, and MELON dominate any classifier-only approach by 1–2 orders of magnitude on ASR — but they require system redesign and impose utility/token costs.
- The **gap between direct and indirect performance** is starkest for legacy detectors (e.g., ProtectAI's APR drops from competitive on direct benchmarks to 22.2% on AgentDojo) and smallest for purpose-built or architectural defenses.

### 7. Architectural approaches beyond detection

| Technique | Threat addressed | Mechanism | Reference |
|---|---|---|---|
| Spotlighting (datamarking/encoding) | Indirect: instruction-vs-data confusion | Transform untrusted text so model recognizes its provenance | Hines et al. 2024 |
| StruQ | Indirect: reserved-token delimiter forgery | Special tokens + fine-tuning to ignore data-channel instructions | Chen et al. USENIX 2025 |
| SecAlign / Meta SecAlign | Indirect: model preference for injection-following | DPO over (secure, insecure) response pairs | Chen et al. CCS 2025 |
| Instruction Hierarchy | Indirect + direct: priority confusion | Train model to prioritize system > developer > user > tool messages | Wallace et al. OpenAI 2024 |
| CaMeL | Indirect: control-flow + data-flow exfiltration | Capability tags on every value, custom Python interpreter | Debenedetti et al. DeepMind 2025 |
| Tool-call constraints | Indirect: unauthorized tool invocation | LLM pre-selects allowed tools; per-tool policy | AgentDojo |
| Output filtering | Exfiltration via Markdown image / URL | Restrict image domains, filter URLs in output, disable auto-fetch | Industry standard post-EchoLeak |
| Allow-listing tool outputs | Indirect: arbitrary tool returns | Validate / sanitize tool returns to fixed schema | "Firewalls" paper, arXiv 2510.05244 |
| Anthropic Constitutional / hierarchy | Indirect: untrusted instruction following | Trained refusals + permission prompts in Claude for Chrome | Anthropic 2025 |

OpenAI's "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions" (Wallace et al., arXiv 2404.13208, April 2024) is the foundational training-time approach: define a strict priority order (system > developer > user > tool) and fine-tune the model so that lower-priority "misaligned" instructions are ignored. Deployed in GPT-4o Mini and subsequent OpenAI models. Subsequent OpenAI work (the "IH-Challenge" training dataset) expands this with adversarially generated training data.

### 8. Practical guidance — what to deploy in 2026

For a team building an LLM-integrated application that processes any untrusted content (email, web, RAG documents, tool outputs), the current consensus is **four overlapping layers**:

1. **Pre-filter** untrusted content with a fast classifier — *Prompt Guard 2 86M* (or 22M for edge), Azure Document Shield, or PromptShield Llama-3.1-8B if you can afford the latency. Treat this as a noisy first cut, not a guarantee.
2. **Mark trust boundaries structurally** — Spotlighting (datamarking by default; encoding if you're on GPT-4 class) or StruQ-style reserved delimiters in your prompt template. Microsoft's GA Spotlighting is one line of config in Azure.
3. **Train the model with instruction hierarchy** — use a SecAlign-fine-tuned backbone (Meta SecAlign Llama-3.3-70B is the public option) or rely on OpenAI's instruction-hierarchy-trained models. Pass untrusted content via the new `input` / `tool` role rather than concatenating into the user message.
4. **Enforce information-flow control at the agent layer** — CaMeL-style capability tracking if the agent has high-value tool access (banking, email, code execution); at minimum, deterministic checks on outgoing URLs (no attacker-controlled Markdown images), domain allow-lists for image rendering, and human confirmation for destructive tool calls. Microsoft's defense-in-depth response to EchoLeak adds Data Loss Prevention controls; Anthropic's Claude for Chrome adds per-site permissions and action confirmations.

**When detection is insufficient**: any time the agent has side effects (sending email, transferring funds, executing code, writing to memory). Detection latency and FPR/FNR tradeoffs become structurally inadequate; structural defenses are required. LLMail-Inject's results — adaptive attackers defeated *every* defense including TaskTracker + Spotlighting in the realistic email pipeline — should be the default working assumption.

## Recommendations

**Stage 1: Immediate (within 1 week).**
- Deploy Meta Llama Prompt Guard 2 86M (or Azure Prompt Shields with both User and Document modes enabled) over all untrusted segments. Set thresholds at 1% FPR initially.
- Disable Markdown image auto-rendering and apply a strict domain allow-list to all outbound URL rendering. This single change neutralizes most public exfiltration PoCs (Markdown image exfiltration was the primary vector in EchoLeak and almost every Rehberger disclosure).
- Audit all tool calls that have side effects (send_email, transfer, browse) and add explicit human confirmation for any path reachable from untrusted-content tokens.

**Stage 2: 1–3 months.**
- Enable Spotlighting (Azure: `spotlighting_enabled: true` for documents) or implement datamarking in your own prompt templates.
- Move all untrusted content (RAG retrievals, tool outputs, email bodies) into an explicit non-user role (OpenAI: `tool` / `input`; Anthropic: `tool_result`). Stop concatenating into the user message.
- If you self-host, fine-tune your backbone with the SecAlign recipe or migrate to Meta SecAlign Llama-3.3-70B-Instruct (FAIR Non-commercial license; check applicability).

**Stage 3: 3–9 months for high-value agents.**
- Adopt CaMeL-style capability-based isolation for any agent that has access to private user data + outbound communication tools. The open-source reference implementation is at `github.com/google-research/camel-prompt-injection`.
- Stand up an internal AgentDojo-equivalent harness against your own tool catalog. Pull in InjecAgent / LLMail-Inject prompts as your initial corpus.
- Continuously red-team with adaptive attackers — the "attacker moves second" result (Nasr et al., arXiv 2510.09023) shows that static defenses are routinely defeated.

**Benchmarks that would change these recommendations.**
- If a future encoder classifier achieves >70% APR @ ≤3% utility on AgentDojo while staying under 50ms — that would reduce the case for CaMeL/Task Shield in lower-tier deployments.
- If an LLM provider ships a verified instruction hierarchy with formal guarantees — that would compress layers 2 and 3.
- If retrieval-side provenance (signed documents, mTLS-style content authentication) becomes available — that would let detectors operate on a trustworthy source signal rather than text alone, potentially closing the indirect gap.

## Caveats

- **Benchmark validity in flux.** The "Are Firewalls All You Need" paper (arXiv 2510.05244) and "When Benchmarks Lie" (arXiv 2602.14161) argue that AgentDojo, InjecAgent, and ASB allow trivial wins for some defenses because of artifacts (injection vectors overwriting task-critical content, biased benign/attack splits). Several headline ASR numbers (e.g., Task Shield's 2.07%) may not generalize to adaptive attackers — LLMail-Inject's data is the best current adversarial benchmark.
- **Two CaMeL numbers in circulation.** The CaMeL v1 abstract (March 2025) reports 67% provably-secure on AgentDojo; v2 (June 2025) reports 77% vs 84% undefended. Both are legitimate; v2 supersedes.
- **Meta Prompt Guard 2 BIPIA numbers are not published.** Meta's model card uses an AgentDojo APR metric rather than BIPIA; treat the 81.2% APR as evidence of generalization but not as a BIPIA-equivalent claim.
- **DataSentinel's robustness is contested.** The headline FPR/FNR ~0 results are on its own evaluation suite; under adaptive `DataFlip` attacks (arXiv 2507.05630), FNR can rise by 80 percentage points.
- **Production detectors evolve weekly.** Azure, AWS, Lakera, Google, and NVIDIA all update guardrails frequently; the table above reflects state as of May 2026.
- **No evidence of in-the-wild EchoLeak exploitation** prior to patch (per Microsoft and Aim Labs), but the design class — zero-click indirect injection in RAG pipelines — should be assumed exploitable in any system that does not adopt at least Stages 1 and 2 above.