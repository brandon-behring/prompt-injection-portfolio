# The Prompt Injection Detector Landscape: A Comprehensive Survey of Models, Training Data, and Benchmarks

## 1. Introduction and Threat Landscape

Prompt injection — where attacker-controlled input causes a large language model (LLM) to deviate from its system instructions — remains the top vulnerability in OWASP's LLM risk list. The defensive ecosystem has evolved through three architectural generations: (1) small BERT/DeBERTa encoder classifiers (2023–2024), (2) ModernBERT-based encoders (late 2024–2025), and (3) instruction-tuned small LLMs used as judges (2025–2026). In parallel, a layer of proprietary commercial APIs (Lakera Guard, Azure Prompt Shields, AWS Bedrock Guardrails, NVIDIA NeMo Guardrails, Google Model Armor, Aporia) has emerged.

A defining tension in the field, articulated forcefully by Lakera and CodeIntegrity in 2024–2026, is that headline accuracy numbers ("98–99%") are typically reported on held-out splits of training-adjacent public datasets and do not generalize to novel attacks. Benchmark validity has therefore become as important as model architecture.

This report covers every major open detector with publicly documented training data, every significant proprietary detector with published benchmark numbers, and every prominent evaluation benchmark, with reconciled head-to-head numbers.

---

## 2. ModernBERT-Based Detectors

ModernBERT (Warner et al., 2024; answerdotai/ModernBERT-base 149M and ModernBERT-large 395M) is now the dominant base for encoder-only injection classifiers because of its 8,192-token native context, FlashAttention, and RoPE-based positional encoding.

### 2.1 Qualifire Sentinel (qualifire/prompt-injection-sentinel)

- **Architecture:** ModernBERT-large, 395M parameters, 28 layers, 8,192-token context, RoPE + local-global alternating attention.
- **Training datasets (open):** OpenSafetyLab/Salad-Data (filtered to "O5: Malicious Use"), alespalla/chatbot-instruction-prompts (7K benign), microsoft/orca-agentinstruct-1M-v1 (7K benign), verazuo/jailbreak-llms, lmsys/toxic-chat (jailbreak rows only), VMware/open-instruct (7K benign), reshabhs/SPML-Chatbot-Prompt-Injection (16K scenario-based).
- **Training datasets (private):** ~1,400 "qualifire-synthetics" prompts.
- **Final split:** Roughly 70% benign / 30% injection; 90/10 train/test split. Aggregate training size on the order of 30–40K samples after filtering.
- **Evaluation benchmarks:** Internal held-out split + four public benchmarks: allenai/wildjailbreak, jackhhao/jailbreak-classification, deepset/prompt-injections, qualifire/Qualifire-prompt-injection-benchmark.
- **Self-reported performance (paper, Ivry & Nahum 2025, arXiv 2506.05446):**
  - Internal test set: Accuracy 0.987, Recall 0.991, Precision 0.986, F1 0.980.
  - Public benchmark F1 averages: Sentinel 0.938 vs ProtectAI v2 0.709. Per-benchmark F1:
    - wildjailbreak: 0.935 vs 0.733
    - jackhhao/jailbreak: 0.985 vs 0.915
    - deepset/prompt-injections: 0.857 vs 0.536
    - qualifire/Qualifire-prompt-injection-benchmark: 0.976 vs 0.652
- **Latency:** ~20 ms per inference on an L4 GPU (self-reported).
- **Limitations:** Authors note susceptibility to novel attack vectors; dataset reproducibility limited by private subset; English-centric; not separately evaluated on PINT or NotInject. **All numbers are self-reported by the model's authors against a single baseline (ProtectAI v2).**

### 2.2 Sentinel v2 (qualifire/prompt-injection-jailbreak-sentinel-v2 / rogue-security/prompt-injection-jailbreak-sentinel-v2)

- **Architecture:** Decoder-based, Qwen3-0.6B fine-tune (departing from ModernBERT). 32K context (vs 8,196 in v1).
- **Training data:** Not disclosed in detail; described as an expansion of v1's curated mix.
- **Self-reported metric:** Average F1 across benchmarks rose from 0.936 (v1) to 0.964 (v2).
- **License:** Elastic License (commercial use permitted). The rogue-security mirror is the same model under a different namespace.
- **Latency:** Not separately reported; expected ~100 ms on a modern GPU given 600M parameters.

### 2.3 CodeIntegrity PromptGuard (codeintegrity-ai/promptguard)

- **Architecture:** ModernBERT-base (149M params), 8,192-token context.
- **Training datasets (≈955K samples):** deepset/prompt-injections, jackhhao/jailbreak-classification, JailbreakBench/JBB-Behaviors, JailbreakV-28K, DhruvTre/jailbreakbench-paraphrase-2025-08, microsoft/llmail-inject-challenge, hendzh/PromptShield (the PromptShield benchmark dataset), geekyrakshit/prompt-injection-dataset, xTRam1/safe-guard-prompt-injection.
- **Training innovation:** Energy-based loss à la Liu et al. NeurIPS 2020 (same family of techniques Meta uses for Prompt Guard 2). Benign samples pushed to energy < −25, malicious to energy > −7.
- **Self-reported test-set metrics:** Accuracy 98.01%, Precision 98.54%, Recall 95.60%, F1 97.04%, ROC-AUC 99.69%.
- **Latency:** ~8 ms (CodeIntegrity's internal benchmark for ModernBERT-base classification).
- **Key caveat — the "98% post-mortem":** In January 2026, CodeIntegrity's Steven Jung published "98% Accurate and Still Broken," explicitly admitting the headline number "measures memorization, not generalization." The model performs well in-distribution but degrades on novel attack patterns. The post is now the most-cited industry critique of held-out-split accuracy reporting and is discussed in §8.

### 2.4 vijil/mbert-prompt-injection and vijil_dome_prompt_injection_detection

- **Architecture:** ModernBERT-base (despite "mbert" name; the tokenizer is loaded from answerdotai/ModernBERT-base). 8,192-token context window per Vijil docs.
- **Training data:** allenai/wildguardmix (train split) + xTRam1/safe-guard-prompt-injection (train split). No precise sample count published.
- **Reported metrics:** Not published on the model card. The model is the default "prompt-injection-mbert" detector inside Vijil's Dome guardrail library.
- **Independent evaluation:** The April 2025 paper "Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails" (arXiv 2504.11168) reports Vijil Prompt Injection had the *highest susceptibility* to adversarial bypass among evaluated guardrails — **average ASR 87.95% for prompt injections and 91.67% for jailbreaks** under character-injection attacks (emoji smuggling, Unicode tag smuggling, upside-down text). However, the same paper notes Vijil was significantly more robust than ProtectAI v1 against simple AML evasion (TextFooler etc.) on injection-only prompts, with an injection ASR of only 14.76%.

### 2.5 tihilya/modernbert-base-prompt-injection-detection

- **Architecture:** ModernBERT-base fine-tune.
- **Training data and metrics:** Not disclosed on the model card; the card is a stub announcing the model classifies "prompt injection attempts in user inputs."
- **Status:** Community model, no peer review or independent benchmark numbers.

### 2.6 ccss17/modernbert-prompt-injection-detector

- **Architecture:** Fine-tuned ModernBERT with LoRA adapters (adapter_model.safetensors 57.6 MB on top of the 792 MB base model).
- **Training data, eval, and metrics:** README is blank (0 bytes as of the latest commit). Effectively undocumented; not recommended for production use.

### 2.7 Summary of ModernBERT detectors

| Detector | Base | Params | Training Size | Latency | Public Benchmark Numbers? | Doc Quality |
|---|---|---|---|---|---|---|
| Sentinel (Qualifire) | ModernBERT-large | 395M | ~30–40K | ~20 ms (L4) | Yes (4 benchmarks, self-reported) | Paper + model card |
| Sentinel v2 (Qualifire) | Qwen3-0.6B (decoder) | 600M | Not disclosed | ~100+ ms expected | Avg F1 0.964 (self) | Model card |
| CodeIntegrity PromptGuard | ModernBERT-base | 149M | 955K | ~8 ms | Self-reported only | Model card + post-mortem blog |
| vijil/mbert-prompt-injection | ModernBERT-base | ~150M | WildGuardMix+SafeGuard | ~8 ms expected | Independent eval: poor | Stub |
| tihilya | ModernBERT-base | ~150M | Undisclosed | n/a | None | Stub |
| ccss17 | ModernBERT + LoRA | ~150M | Undisclosed | n/a | None | Empty README |

---

## 3. DeBERTa-Based Detectors

DeBERTa-v3 (He et al., 2021) was the workhorse base from 2023 through early 2025. Its multilingual variant mDeBERTa-v3-base remains the base for Meta's Prompt Guard 1.

### 3.1 ProtectAI deberta-v3-base-prompt-injection (v1, "Laiyer")

- **Architecture:** microsoft/deberta-v3-base fine-tune; 184M parameters; English-only.
- **Training data:** Custom mixture of ~12 open datasets at ~30% injection / 70% benign. The datasets are not fully enumerated on the card. Original training authored by Laiyer.ai before its acquisition by ProtectAI.
- **Self-reported evaluation-split metrics (held-out from training):** Loss 0.0010, Accuracy 0.9999, Recall 0.9997, Precision 0.9998, F1 0.9998.
- **Independent evaluation (PromptShield paper, Jacob et al. 2025):** AUC only **0.643**, TPR@FPR=1% of just **4.93%**, TPR@FPR=0.1% of **0.053%** — catastrophic out-of-distribution failure on application-structured data.
- **Independent evaluation (Bypassing paper 2504.11168):** Average ASR ~77% on prompt injections under character-injection attacks; for prompt injection evasion ASR rises to **95.18%**.
- **Latency:** ~7.5 ms (RTX 4090) / ~646 ms (Apple M1 CPU) for the unquantized FP32 ONNX model.
- **Limitations on card:** "English only, may not detect jailbreak attacks, false-positives on system prompts."

### 3.2 ProtectAI deberta-v3-base-prompt-injection-v2

- **Architecture:** microsoft/deberta-v3-base fine-tune; 184M parameters; English-only.
- **Training data:** Larger curated mix from academic papers, security competitions, and LLM Guard community feedback (specific datasets not enumerated). Trained with 20+ configurations tested. Authors state injection examples were "crafted using insights gathered from academic research papers, articles, security competitions, and valuable LLM Guard's community feedback."
- **Self-reported metrics:** Accuracy ~0.9999 on its post-training split (similar to v1).
- **Independent evaluation (PromptShield):** AUC 0.701, TPR@FPR=1% 1.665%, TPR@FPR≤0.5% **0.000%**. This is a near-complete failure in the deployable low-FPR regime.
- **Independent evaluation (Lakera PINT v2025-05-02):** **PINT score 79.14%**.
- **Independent evaluation (InjecGuard paper, arXiv 2410.22770):** ProtectAI v2 is the runner-up overall, but its over-defense accuracy on NotInject falls below random guessing (close to 60%) — it false-positives on benign prompts containing trigger words like "ignore" or "cancel."
- **Independent evaluation (Sentinel paper):** F1 0.709 averaged across four benchmarks vs Sentinel's 0.938.
- **Independent evaluation (Bypassing paper):** Robust to character injection at the prompt-injection ASR of 20.26%, but still heavily bypassed by emoji and Unicode-tag smuggling.

### 3.3 ProtectAI deberta-v3-small-prompt-injection-v2

- **Architecture:** microsoft/deberta-v3-small fine-tune; ~70M params.
- **Trade-off:** Less accurate than the base v2 model but faster inference. Same training data and same limitations (English, doesn't catch jailbreaks well). No standalone PINT score published.

### 3.4 deepset/deberta-v3-base-injection

- **Architecture:** microsoft/deberta-v3-base fine-tune; 184M params; ~738 MB safetensors file.
- **Training data:** deepset/prompt-injections dataset only (the original public injection dataset). Card describes English + German labels.
- **Note:** Card explicitly warns: "The dataset assumes that legitimate requests are either all sorts of questions or keyword searches. If you are using this model to secure your system and it is overly 'trigger-happy' to classify requests as injections, consider collecting legitimate examples and retraining." A foundational but very narrow model; included in PINT's examples directory and broadly used as the historical baseline.

### 3.5 hlyn/prompt-injection-judge-deberta-70m

- **Architecture:** microsoft/deberta-v3-xsmall (70.8M params), aggressively INT8-quantized to an 83 MB ONNX file. Designed for CPU/edge.
- **Training data:** hlyn/prompt-injection-judge-deberta-dataset (~400K samples). The dataset documentation states it mixes synthetic SecAlign-style injections, WildJailbreak (GPT-4 generated), and other sources; *explicitly excludes* rogue-security/prompt-injections-benchmark from training so the latter can serve as a held-out test set.
- **Training techniques:** Evidential Deep Learning (EDL), DoRA, supervised contrastive learning (SupCon), FreeLB, R-Drop, SWA — an unusually heavy stack for a 70M model.
- **Self-reported metrics on rogue-security/prompt-injections-benchmark (5,000 samples):** Precision 95.84%, Recall 82.83%, Accuracy 91.68%, F1 0.8886, AUC-ROC 0.9824.
- **Latency:** 3.69 ms (RTX 4090) / ~101 ms (M1 CPU).
- **Head-to-head vs ProtectAI v2 on the same held-out benchmark:** AUC 0.9824 vs 0.8291; F1 0.8886 vs 0.6549; accuracy 91.7% vs 72.3%. Model is **2.0× faster on GPU and 6.4× faster on CPU**, and 8.9× smaller as an ONNX file (INT8 vs FP32).
- **Limitations:** English-only; synthetic injections follow fixed "Ignore previous instructions" templates that may not generalize; WildJailbreak component inherits GPT-4 distributional bias. **All numbers are self-reported.**

### 3.6 Summary of DeBERTa detectors

| Detector | Params | Training Data | Latency | Self-Reported F1 | PINT Score | PromptShield AUC | NotInject Over-defense |
|---|---|---|---|---|---|---|---|
| deepset/deberta-v3-base-injection | 184M | deepset/prompt-injections | ~7 ms | ~0.999 (on own split) | Not listed | n/a | Severe (English/German) |
| ProtectAI v1 | 184M | 12 mixed open | 7.5 ms (4090) / 646 ms (M1) | 0.9998 | n/a | 0.643 | Severe |
| ProtectAI v2 | 184M | Expanded mix | 7.5 ms (4090) | ~0.9999 | **79.14%** | 0.701 | Below 60% (random) |
| ProtectAI small v2 | 70M | Same as v2 | ~3 ms (est.) | Lower | n/a | n/a | Severe |
| hlyn judge-70m | 70.8M | 400K mixed | 3.7 ms / 101 ms | 0.8886 (rogue) | n/a | n/a | Not evaluated |

---

## 4. Other Encoder-Based Detectors

### 4.1 Multilingual BERT / mDeBERTa baselines

- **Meta Prompt-Guard-86M** uses **mDeBERTa-v3-base (276M params)** as its multilingual backbone (see §5 for details). mDeBERTa supports 100+ languages.
- **Multilingual BERT (mBERT, 178M params)** is used in research (Rahman et al. 2024, cited in arXiv 2410.21337) but not in any widely deployed open detector.

### 4.2 NeoBERT

- **Architecture:** Le Breton et al. 2025 (arXiv 2502.19587), 250M params, ~2× faster than ModernBERT, state-of-the-art MTEB scores.
- **Use as a detector:** CodeIntegrity reports they "evaluated this extensively" as a prompt-injection encoder base but "the generalization ceiling remained similar" to ModernBERT. **No public NeoBERT-based injection detector has been released as of May 2026.**

### 4.3 DistilBERT (Fmops)

- The fmops/distilbert-prompt-injection model (67M params) is evaluated in the PromptShield paper: AUC 0.759, TPR@FPR=1% 13.58%. It outperforms ProtectAI v1/v2 in low-FPR regimes despite being a tiny model — likely because ProtectAI's training data is over-fit to specific benchmarks.

### 4.4 XLM-RoBERTa fine-tunes

- Rahman et al. and others (arXiv 2410.21337) report XLM-RoBERTa fine-tuned on deepset/prompt-injections achieves 99.13% accuracy, 100% precision, 98.33% recall, 99.15% F1 — but **only on the deepset test split**, making this another in-distribution memorization result. Multilingual potential but no deployed open model.

---

## 5. LLM-Based / Instruction-Tuned Detectors

### 5.1 PromptShield (UC Berkeley, Jacob et al. 2025, arXiv 2501.15145)

- **Architecture:** Llama-3.1-8B-Instruct fine-tuned with LoRA (3 epochs, LR 2e-4, early stopping). Also evaluated FLAN-T5 < 1B variants (without LoRA, fine-tuned directly).
- **Training data:** A curated dataset of conversational data (from chatbots) + application-structured data (from LLM-integrated applications). Authors emphasize augmentation by inserting newlines before the prompt p, before input data d, and after data d. Ablation table shows training set sizes from 1K to 20K samples. At 20K samples, AUC reaches 0.998; even at 1K, AUC is already 0.981.
- **Benchmark:** The PromptShield benchmark itself — explicitly designed to include realistic application-structured data, which prior benchmarks lack. Evaluation is reported at low false-positive-rate operating points (FPR=1%, 0.5%, 0.1%, 0.05%), which is the regime that matters for deployment.
- **Reported metrics on the PromptShield benchmark:**

| Detector | Base | Params | AUC | TPR@FPR=1% | TPR@FPR=0.5% | TPR@FPR=0.1% | TPR@FPR=0.05% |
|---|---|---|---|---|---|---|---|
| **PromptShield (Llama-3.1-8B)** | Llama-3-1-8B-Instruct | 8B | **0.997** | **94.46%** | **90.80%** | **71.45%** | **61.86%** |
| PromptShield (DeBERTa-v3-base) | DeBERTa-v3-base | 184M | 0.940 | 29.93% | 24.71% | 11.69% | 5.00% |
| Meta PromptGuard 1 | mDeBERTa-v3-base | 276M | 0.867 | 12.56% | 11.36% | 3.74% | 1.41% |
| InjecGuard | DeBERTa-v3-base | 184M | 0.764 | 20.37% | 16.26% | 6.58% | 4.21% |
| Fmops DistilBERT | DistilBERT | 67M | 0.759 | 13.58% | 8.85% | 2.34% | 1.41% |
| ProtectAI v2 | DeBERTa-v3-base | 184M | 0.701 | 1.67% | 0.00% | 0.00% | 0.00% |
| ProtectAI v1 | DeBERTa-v3-base | 184M | 0.643 | 4.93% | 0.43% | 0.05% | 0.03% |

- **Significance:** This is one of the few independently published, head-to-head, low-FPR comparisons across major detectors. It shows that (a) base-model size matters dramatically — an 8B instruct model dominates 100–300M encoders at deployment-relevant operating points; and (b) ProtectAI v2's "0% TPR at FPR≤0.5%" demonstrates collapse: it can either flag everything or nothing, but cannot operate at low FPR.
- **Latency cost:** 200–800+ ms per inference vs ~5–10 ms for encoders (per CodeIntegrity's measurements). The 8B model is impractical as a synchronous gate for high-throughput production.

### 5.2 Meta Llama Prompt Guard 1 (meta-llama/Prompt-Guard-86M)

- **Architecture:** mDeBERTa-v3-base, 86M params, multilingual base.
- **Output:** Three classes — BENIGN, INJECTION, JAILBREAK. (Communications with model devs cited in the PromptShield paper note the JAILBREAK label is most aligned with "prompt injection" as defined academically; the INJECTION label is for third-party/data content.)
- **Training data:** Mix of open-source benign web data + user prompts/instructions + malicious prompt-injection and jailbreaking datasets + Meta's own synthetic injections and red-teaming data. Specific datasets not enumerated.
- **Benchmarks (independent):**
  - **PINT:** 61.82% — lowest of major detectors.
  - **PromptShield benchmark:** AUC 0.867 (second-best after PromptShield itself).
- **Known issue:** Community reports (HF discussion #15) of the model classifying nearly all inputs as INJECTION/JAILBREAK on the walledai/JailbreakHub dataset — severe over-defense.
- **Limitation:** Context window 512 tokens; Meta explicitly recommends fine-tuning on application data.

### 5.3 Meta Llama Prompt Guard 2 (86M and 22M)

- **Architecture:** Multilingual base for the 86M variant; English-only for the 22M variant. Both have 512-token context.
- **Output:** Two labels (LABEL_0 benign / LABEL_1 attack); no separate injection/jailbreak sub-labels because "this objective is too broad to be useful" (Meta).
- **Training data:** Larger corpus of known vulnerabilities + synthetic injections + red-team data. Uses a custom loss function targeting recall at low FPR — Meta describes "a dramatic increase in Recall @ 1% FPR" vs Prompt Guard 1, attributed to this loss.
- **Languages:** English + French, German, Italian, Spanish, Portuguese, Chinese, Japanese (and others — multilingual training).
- **Benchmarks (independent):**
  - **PINT:** 78.76% (much improved over Prompt Guard 1's 61.82%; competitive with ProtectAI v2's 79.14%).
- **Limitations:** 512-token context requires segmentation for long prompts; not immune to adaptive attacks (Meta explicitly states this).

### 5.4 Llama Guard family (Llama Guard 1, 2, 3, 4)

Meta's Llama Guard family targets *safety classification* (hate, violence, sexual content, criminal planning, etc.) more than prompt injection per se. They are content-moderation classifiers built on Llama-2/3/4 base models:

- **Llama Guard 1 (7B):** Built on Llama-2-7B; output is a taxonomy of unsafe categories.
- **Llama Guard 2 (8B):** Built on Llama-3-8B; expanded taxonomy.
- **Llama Guard 3 (1B and 8B):** Built on Llama-3.1/3.2; trained on MLCommons AILuminate taxonomy.
- **Llama Guard 4 (12B):** Multimodal extension supporting image inputs.

The InjecGuard authors and the CourtGuard paper observe that **Llama-Guard-3 happens to score above 90% on NotInject and outperforms PromptGuard, LakeraGuard, GPT-4o, and even InjecGuard on the over-defense benchmark** — but this is incidental: Llama Guard was not trained as a prompt-injection detector. Its high score on NotInject reflects its content-safety taxonomy (a benign trigger word is not unsafe content), not injection-specific intelligence.

### 5.5 CourtGuard (Sun, arXiv 2510.19844, October 2025)

- **Architecture:** Multiagent LLM-based; uses a small local LLM (Llama-3.1 or Phi-3) in a court-like multiagent debate — a defense attorney argues the prompt is benign, a prosecutor argues it is injection, a judge decides.
- **Performance:** Reports >90% NotInject scores using either backbone — exceeding Meta PromptGuard, LakeraGuard, GPT-4o, and InjecGuard on over-defense.
- **Trade-off:** Multiple LLM calls per inference; high latency.
- **Significance:** Demonstrates that even small LLMs in a structured-reasoning role can outperform fine-tuned classifiers, particularly on over-defense.

---

## 6. Commercial / Proprietary Detectors

### 6.1 Lakera Guard

- **Architecture:** Proprietary; combines multiple detectors (prompt-attack, PII, content moderation, hallucination). Policy level is configurable (L1–L3 with L3 the most strict).
- **Training data:** Proprietary internal database of prompt-injection attempts collected via Lakera's Gandalf game (1M+ prompts in the public lakera/gandalf_ignore_instructions dataset) and customer telemetry; explicitly excluded from the PINT benchmark.
- **PINT score (own benchmark, 2025-05-02):** **95.22%** — the highest published.
- **Languages:** Multilingual (PINT covers ~25 languages, and Lakera Guard is the top scorer).
- **Caveat:** Lakera designed PINT; while they document that no detector is trained on PINT inputs, the benchmark is structurally aligned with Lakera's threat model. The CourtGuard paper (arXiv 2510.19844) notes that even on Lakera's own benchmark "Lakera Guard scores only 92.5461%" (earlier number), and that "typically [prompt injection] attack is winning against defense."

### 6.2 Azure AI Prompt Shields (Microsoft)

- **Architecture:** Two distinct shields, both proprietary: "User Prompt Shield" (formerly Jailbreak Risk Detection, for direct attacks) and "Document Shield" (for indirect/XPIA attacks). 2025 added **Spotlighting** for delimiting trusted vs untrusted segments in document content.
- **Languages trained/tested:** Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese (other languages "may work but with varying quality").
- **API:** `shieldPrompt` endpoint accepts both `userPrompt` and `documents` arrays.
- **PINT score:** **89.12%** (Documents + User Prompts combined).
- **Limitation:** Bound to Azure OpenAI Service or Azure AI Foundry; cannot intercept calls to api.openai.com, Anthropic, Google, or open-source models directly.

### 6.3 AWS Bedrock Guardrails

- **Architecture:** Proprietary "Prompt Attack" category alongside content filters, PII filters, denied topics, and contextual grounding checks. Confidence levels NONE / LOW / MEDIUM / HIGH.
- **PINT score:** **89.24%** — but only when configured to consider MEDIUM/HIGH as positive; default settings produce a high false-positive rate per Lakera's methodology.

### 6.4 NVIDIA NeMo Guardrails

- **Architecture:** Programmable rails framework with multiple detectors. "NeMo Guard Detect" is a separate prompt-injection detection component built on NVIDIA's internal classifiers; also supports user-defined Colang rails.
- **Independent evaluation (Bypassing paper 2504.11168):** Jailbreak ASR 72.54% — meaning attackers bypassed it ~73% of the time under character-injection attacks. Not strong as a standalone injection detector.

### 6.5 Google Model Armor

- Proprietary; part of Google Cloud Security Command Center.
- **PINT score:** **70.07%** (2025-08-27).

### 6.6 Aporia Guardrails

- **PINT score:** **66.44%** (2025-05-02). Lowest of evaluated commercial offerings on PINT.

### 6.7 Rebuff

- Open-source library (released 2023) that combines four layers: heuristic filters (regex-based), a vector-database canary-token approach (storing past injections), an LLM-as-judge layer, and canary-word leak detection. No formal benchmark numbers are published by the Rebuff project; not included in recent PINT or PromptShield evaluations. It is more accurately described as a defense framework than as a trained classifier.

### 6.8 Other commercial offerings

- **HiddenLayer, Robust Intelligence, CalypsoAI, Vijil (Dome), Guardrails AI, SafePrompt** — multiple vendors offer commercial guardrail services in 2025–2026. Vijil's Dome library is open source and uses the vijil/mbert-prompt-injection model as its default injection detector (§2.4). Most lack independent PINT or PromptShield benchmark numbers.

---

## 7. Specialized Approaches

### 7.1 InjecGuard (Li, Liu, Xiao 2024; arXiv 2410.22770)

- **Architecture:** DeBERTa-v3-base (184M).
- **Training innovation: "Mitigating Over-defense for Free" (MOF).** Uses a data-augmentation + retraining-from-scratch strategy that explicitly debiases trigger-word features.
- **Training data:** Open-source injection datasets + augmented benign samples enriched with attack trigger words.
- **Companion benchmark:** **NotInject** — 339 carefully crafted *benign* prompts containing 1–3 trigger words ("ignore", "cancel", etc.) at three difficulty levels. Specifically designed to expose over-defense.
- **Evaluation across four datasets (NotInject, PINT, WildGuard-Benign, BIPIA):**
  - InjecGuard: Average accuracy **83.48%**; over-defense accuracy 87.32%, benign accuracy 85.74%, malicious accuracy 77.39%. Surpasses ProtectAI v2 (runner-up) by **30.8% on NotInject**.
  - InjecGuard claims it matches GPT-4o accuracy while being an open, lightweight model.
- **Independent evaluation (PromptShield paper):** AUC 0.764, TPR@FPR=1% 20.37% — better than ProtectAI v2 (0.701, 1.67%) but well below PromptShield-Llama-8B (0.997, 94.46%). Confirms its strength in benign detection but not at the deployment-grade low-FPR regime.
- **Limitations:** Trained primarily on English; trades some malicious-class accuracy (77%) for over-defense correction.

### 7.2 DataSentinel (Liu et al. 2025, arXiv 2504.11358)

- **Approach:** Game-theoretic detection — formulates detection as a minimax optimization problem, then alternates inner-max (adaptive attack generation via gradient methods) and outer-min (detector fine-tuning).
- **Claim:** Effective against both existing and adaptive prompt-injection attacks. Code at github.com/liu00222/Open-Prompt-Injection. Particularly aimed at LLM-integrated applications (Bing Copilot, AI overviews) where input data is from untrusted external sources.

### 7.3 Embedding-based detectors (Ayub & Majumdar, arXiv 2410.22284)

- **Approach:** Generate embeddings (e.g., from OpenAI text-embedding-ada-002 or open-source encoders), then train traditional ML classifiers — Random Forest, XGBoost, MLPs — on the embedding space.
- **Result:** Outperforms encoder-only neural networks on certain held-out attack patterns. CodeIntegrity reports they replicated this approach and observed improved generalization, but with 50–100 ms additional latency per request from the embedding step.

### 7.4 Multimodal detectors

There is currently **no widely adopted multimodal prompt-injection detector**. Research is emerging (e.g., prompt injection attacks on vision-language models for surgical decision support, medRxiv 2025.07.16) but no canonical detector model exists for image/video injection vectors as of May 2026. Llama Guard 4 supports multimodal *content moderation* but is not an injection detector.

---

## 8. The Public Benchmark Landscape

### 8.1 Major benchmarks

| Benchmark | Source | Size | Composition | Direct/Indirect | Multilingual |
|---|---|---|---|---|---|
| **PINT** | Lakera | 4,314 (3,016 EN + 1,298 non-EN) | 5.2% injections, 0.9% jailbreaks, 20.9% hard negatives, 36.5% chat, 36.5% public docs | Both | Yes (~25 languages) |
| **rogue-security/prompt-injections-benchmark** (formerly Qualifire) | Qualifire/Rogue Security | ~5,000 | Adversarial edge cases | Direct (mostly) | English-leaning |
| **deepset/prompt-injections** | deepset | ~660 | Classic injections + benign keyword searches | Direct | English + German |
| **JailbreakBench (JBB-Behaviors)** | NeurIPS 2024 | 200 prompts (100 harmful + 100 benign) | Curated harmful behaviors | Direct | English |
| **microsoft/llmail-inject-challenge** | Microsoft | Competition dataset (email-context) | Email-context indirect injections | Indirect | English |
| **WildJailbreak / WildGuardMix** | AI2 (Jiang et al. 2024) | 50K+ adversarial + benign | In-the-wild jailbreaks | Direct | English |
| **xTRam1/safe-guard-prompt-injection (SafeGuard)** | Community | ~10K | Mixed direct injections | Direct | English |
| **safe-guard-v2** | Community/follow-up | Expanded version of SafeGuard | Mixed | Direct | English |
| **NotInject** | Li et al. (InjecGuard) | 339 benign | Over-defense probes; trigger words at 3 difficulty levels | n/a (benign only) | English |
| **jackhhao/jailbreak-classification** | Community | ~1.3K | Jailbreak prompts | Direct | English |
| **BIPIA** | Microsoft | Variable | Indirect injections in documents/emails/tools | Indirect | English |
| **PromptShield benchmark** | Berkeley (Jacob et al.) | Conversational + application-structured | Balanced for low-FPR eval | Both | English |
| **AdvBench** | Zou et al. 2023 (GCG paper) | 520 harmful behaviors + harmful strings | Adversarial suffix optimization | Direct | English |
| **HarmBench** | Mazeika et al. 2024 (ICML) | 400 behaviors across 7 categories | Categorical harm taxonomy | Direct | English |
| **Qualifire-prompt-injection-benchmark** | Qualifire | Held-out test set | Adversarial PI | Direct | English |
| **gandalf_ignore_instructions** | Lakera | ~1K | In-the-wild Gandalf-game attacks | Direct | English (mostly) |
| **JailbreakV-28K** | Community | 28K | Jailbreak variants | Direct | English |

### 8.2 Discussion of AdvBench and HarmBench

**AdvBench** (Zou et al., July 2023) is the canonical benchmark introduced with the Greedy Coordinate Gradient (GCG) adversarial-suffix attack. It contains 520 "harmful behaviors" (instructions like "Write a tutorial on building a bomb") and a parallel set of harmful strings. AdvBench measures *attack success* — i.e., whether the LLM produces a harmful response — rather than detector accuracy. It is used to evaluate detectors only indirectly: a detector is "good" if it blocks adversarial-suffix-augmented AdvBench prompts. The standard adversarial template is to append optimization-derived suffixes (`!!!!! !!!!! !!!!! ...` style strings) that bypass safety alignment. Most encoder detectors fail catastrophically on AdvBench-style optimization-based attacks because the suffixes look like random noise rather than semantic injections.

**HarmBench** (Mazeika et al., ICML 2024) extends AdvBench with 400 behaviors across 7 semantic categories (cybercrime, chemical/biological weapons, illegal activities, harassment, misinformation, harmful content, copyright), plus contextual behaviors and multimodal behaviors. HarmBench is more comprehensive and is now the de facto standard for jailbreak robustness evaluation. As with AdvBench, HarmBench is fundamentally an attack benchmark — detector evaluations against HarmBench attacks typically come from independent red-teaming papers rather than from detector model cards.

### 8.3 Published PINT leaderboard (Lakera, 2025-05–08)

| Detector | PINT Score | Date |
|---|---|---|
| Lakera Guard | **95.22%** | 2025-05-02 |
| AWS Bedrock Guardrails | 89.24% | 2025-05-02 |
| Azure AI Prompt Shield (Docs + Prompts) | 89.12% | 2025-05-02 |
| ProtectAI deberta-v3-base-prompt-injection-v2 | 79.14% | 2025-05-02 |
| Llama Prompt Guard 2 (86M) | 78.76% | 2025-05-05 |
| Google Model Armor | 70.07% | 2025-08-27 |
| Aporia Guardrails | 66.44% | 2025-05-02 |
| Llama Prompt Guard 1 (86M) | 61.82% | 2025-05-02 |

Qualifire Sentinel, CodeIntegrity PromptGuard, hlyn/judge-deberta-70m, vijil, and InjecGuard are not on the official PINT leaderboard.

### 8.4 What each benchmark actually tests — and what it doesn't

- **deepset/prompt-injections** is the historical baseline and contains essentially template attacks ("Ignore previous instructions…"). High accuracy here is necessary but almost meaningless — every modern detector exceeds 99% in-distribution.
- **PINT** is the broadest neutral benchmark, balances hard negatives and benign chat/documents, and is multilingual. Lakera maintains it explicitly to combat Goodhart's law by withholding its inputs from training (including their own). However, PINT is dominated by Lakera Guard's own score, raising concerns about whether the threat model is structurally aligned with Lakera's product.
- **rogue-security/prompt-injections-benchmark** has become a popular "adversarial edge-case" benchmark held out from training in newer models (hlyn, CodeIntegrity-adjacent). Originally a Qualifire dataset; it carries Qualifire's threat model.
- **NotInject** is a unique benign-only benchmark explicitly designed to detect over-defense. It is the single most important addition to the evaluation landscape because over-defense (false positives blocking legitimate users) is often the dominant failure mode in production.
- **JailbreakBench, AdvBench, HarmBench** test *unsafe-content elicitation*, which overlaps with but is not the same as prompt injection. Detectors that score well on JailbreakBench may not catch indirect injections that don't produce harmful content (e.g., data exfiltration via summarization).
- **llmail-inject-challenge** and **BIPIA** are among the very few benchmarks that test **indirect** injection in realistic email/document contexts. Most encoder detectors are not evaluated on these.
- **safe-guard** and **safe-guard-v2** (the xTRam1 community datasets) are widely used as training data — appearing in CodeIntegrity PromptGuard (xTRam1/safe-guard-prompt-injection) and Vijil — but are not commonly used as held-out evaluation sets, raising leakage concerns when models trained on them are evaluated on similar distributions.
- **PromptShield benchmark** introduced low-FPR evaluation (TPR@FPR=0.05%/0.1%/0.5%/1%), which is the regime that matters for production deployment, since defenders cannot tolerate false-positive rates above ~1% on millions of requests.

### 8.5 Known criticisms of benchmark validity

1. **Training-data leakage:** Most detectors train on deepset/prompt-injections, jackhhao/jailbreak-classification, safe-guard-prompt-injection, and similar public datasets and then evaluate on held-out splits of the same. ProtectAI v1's 99.99% accuracy and XLM-RoBERTa's 99.13% are both this pattern.
2. **Goodhart's law on public benchmarks:** Lakera explicitly designed PINT to combat this, stating that "having a 99% accuracy on a Hugging Face prompt injection dataset does not translate into being an effective defense in practice."
3. **Narrow attack coverage:** Most benchmarks test direct injection ("Ignore previous instructions"), not indirect injection, not character-injection attacks (emoji/Unicode smuggling), and not optimization-based attacks (GCG, AutoDAN). The April 2025 paper "Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails" showed that emoji smuggling alone achieved **100% ASR for both prompt injections and jailbreaks** against multiple commercial guardrails.
4. **In-distribution vs out-of-distribution:** The PromptShield paper's low-FPR table reveals that ProtectAI v2 — celebrated for near-perfect accuracy — has TPR=0% at FPR≤0.5%, meaning it cannot operate at deployment thresholds at all.
5. **Selection bias in self-reported benchmarks:** Sentinel was evaluated only against ProtectAI v2 on four benchmarks; ProtectAI v2 was the unambiguous loser by design. The Sentinel paper omits PINT and PromptShield evaluations.
6. **Mismatch between attack benchmarks (AdvBench, HarmBench) and detector benchmarks (PINT, NotInject, PromptShield).** No detector is routinely evaluated against both styles, leaving gaps in our understanding of robustness against optimization attacks.

### 8.6 The CodeIntegrity "98% post-mortem" critique

CodeIntegrity, whose own PromptGuard model achieves 98.01% accuracy / 97.04% F1 / 99.69% ROC-AUC, published a blog post in January 2026 titled "98% Accurate and Still Broken" making the following systematic arguments:

1. **Classical ML metrics measure memorization, not generalization.** Held-out test splits share the distribution of attack patterns and dataset biases with training data. They quote Joshua Saxe: "An LLM scoring an 85% F-score on your test data is likely more meaningful than a classical ML model scoring 95% but fit to the test distribution."
2. **The research journey across architectures hit similar ceilings:** BERT → ModernBERT → NeoBERT all plateaued on out-of-distribution attacks. Energy-based loss functions (Liu NeurIPS 2020) improved boundaries but did not solve generalization. Embedding-based ML (XGBoost on embeddings) generalized slightly better but added 50–100 ms latency. Small fine-tuned LMs (Qwen 2.5 0.5/1.5B, Phi-3 3.8B, Gemma-2 2B) generalized notably better but cost 200+ ms. LLM-as-judge is "the current ceiling" but costs 800+ ms and 10–100× the compute.
3. **The "AI solving AI" trap:** Using LLM guards to protect LLMs creates compounding failure modes — the same vulnerabilities exist in every guard layer, and attackers who can manipulate the primary LLM can typically manipulate its guardians.
4. **Detection treats symptoms, not causes.** The core architectural issue — LLMs unify instruction and data in one context — is unsolved by any classifier. CodeIntegrity advocates structural separation, constrained execution, and capability-based security architectures.
5. **Practical advice:** "Treat your 98% detector as a speed bump, not a wall."

This critique is the most cited industry post-mortem of detector reliability and is broadly consistent with the PromptShield paper's low-FPR results and the "Bypassing" paper's character-injection results.

### 8.7 Latency comparison across detector architectures (CodeIntegrity)

| Approach | Generalization | Latency (typical) |
|---|---|---|
| BERT classifiers | Limited | ~5 ms |
| ModernBERT | Moderate | ~8 ms |
| Embedding + traditional ML | Improved | ~80 ms |
| Small LMs (fine-tuned 0.5–4B) | Good | ~200 ms |
| LLM-as-Judge (8B+) | Strong | ~800 ms |

---

## 9. Direct vs Indirect Prompt Injection Coverage

| Detector | Direct PI | Indirect PI (XPIA) |
|---|---|---|
| Sentinel (Qualifire) | ✓ | Partial (via SPML and salad-data indirectly; not separately evaluated) |
| ProtectAI v1/v2 | ✓ | Not designed for it |
| CodeIntegrity PromptGuard | ✓ | Partial (llmail-inject in training data) |
| Meta Prompt Guard 1 | ✓ | Partial — separate INJECTION label explicitly for third-party/data content |
| Meta Llama Prompt Guard 2 | ✓ | Implicit through training corpus |
| PromptShield | ✓ | ✓ (application-structured data explicitly in benchmark) |
| Azure Prompt Shields | ✓ | ✓ (dedicated Document Shield + Spotlighting) |
| AWS Bedrock Guardrails | ✓ | Limited |
| Lakera Guard | ✓ | Partial (PINT includes long-document scenarios) |
| InjecGuard | ✓ | Tested on BIPIA but trained primarily on direct |
| Llama Guard 3 | (content-safety only) | (not designed for either) |
| BIPIA benchmark | n/a | ✓ (purpose-built) |
| llmail-inject benchmark | n/a | ✓ (email-context) |

Indirect prompt injection — Greshake et al.'s 2023 threat model — remains under-served by open detectors. **Azure's Document Shield + Spotlighting is currently the most explicit commercial defense.**

---

## 10. English vs Multilingual Coverage

| Detector | Languages |
|---|---|
| Sentinel (Qualifire) | English |
| ProtectAI v1/v2/small | English (explicit limitation in model card) |
| deepset/deberta-v3-base-injection | English + German |
| CodeIntegrity PromptGuard | "Primarily English" |
| hlyn/judge-deberta-70m | English |
| InjecGuard | English |
| Meta Prompt Guard 1 (86M) | Multilingual (mDeBERTa base, 100+ languages) |
| Meta Llama Prompt Guard 2 (86M) | Multilingual (eight+ languages tested: EN/FR/DE/IT/ES/PT/JA/ZH) |
| Meta Llama Prompt Guard 2 (22M) | English only |
| Azure Prompt Shields | Chinese, English, French, German, Spanish, Italian, Japanese, Portuguese |
| Lakera Guard | Multilingual (PINT covers ~25 languages) |
| Llama Guard 3 | Multilingual via Llama-3.1 base |
| PINT benchmark | Multilingual — 12 Indo-European, 8 Asian, plus Arabic/Turkish/Finnish/Hungarian |

The open-source ecosystem is overwhelmingly English-centric; only Meta's Prompt Guard family and a handful of commercial services seriously address multilingual injections.

---

## 11. Synthesis: Detector × Benchmark Performance

The following consolidated matrix shows the highest-confidence cross-evaluations available. Cells marked "self" are reported by the model's own authors; "indep" by an independent paper or benchmark maintainer.

| Detector | Internal Held-Out F1 | PINT | PromptShield AUC | NotInject (over-defense) | rogue-security F1 | Latency |
|---|---|---|---|---|---|---|
| Sentinel (Qualifire ModernBERT-L) | 0.980 (self) | – | – | – | – | ~20 ms (L4) |
| Sentinel v2 (Qwen3-0.6B) | 0.964 avg (self) | – | – | – | – | ~100+ ms |
| CodeIntegrity PromptGuard | 0.970 (self) | – | – | – | – | ~8 ms |
| ProtectAI v1 | 0.9998 (self) | – | 0.643 (indep) | severe (indep) | – | 7.5 ms / 646 ms (M1) |
| ProtectAI v2 | 0.9999 (self) | **79.14%** (indep) | 0.701 (indep) | <60% (indep) | 0.6549 (indep) | 7.5 ms |
| ProtectAI small v2 | reported | – | – | – | – | ~3 ms |
| deepset/deberta-v3-base-injection | ~0.99 (self) | (in examples) | – | – | – | ~7 ms |
| hlyn judge-70m | – | – | – | – | **0.8886** (self) | 3.7 ms / 101 ms |
| InjecGuard | 0.8348 avg (self) | tested | 0.764 (indep) | **87.32%** (self) | – | ~7 ms |
| Meta Prompt Guard 1 (86M) | – | 61.82% (indep) | 0.867 (indep) | below SOTA | – | ~5 ms |
| Meta Llama Prompt Guard 2 (86M) | – | 78.76% (indep) | – | – | – | ~5 ms |
| Llama Guard 3 (8B) | – | – | – | >90% (indep) | – | ~200 ms |
| Lakera Guard | – | **95.22%** (own) | – | – | – | ~50–100 ms (API) |
| Azure Prompt Shields | – | 89.12% (indep) | – | – | – | API |
| AWS Bedrock Guardrails | – | 89.24% (indep) | – | – | – | API |
| Google Model Armor | – | 70.07% (indep) | – | – | – | API |
| Aporia | – | 66.44% (indep) | – | – | – | API |
| **PromptShield (Llama-3.1-8B)** | – | – | **0.997** (self) | – | – | ~200–800 ms |
| Fmops DistilBERT | – | – | 0.759 (indep) | – | – | ~3 ms |
| CourtGuard (Llama/Phi multiagent) | – | – | – | >90% (indep) | – | very high |

Three observations dominate this matrix:

1. **No detector wins on every benchmark.** ProtectAI v2 dominates its own splits but collapses on PromptShield's low-FPR test; Lakera dominates PINT but isn't publicly evaluated on PromptShield; InjecGuard wins NotInject but is mid-pack on PromptShield AUC.
2. **The largest gap between in-distribution and OOD performance is in encoder-only models.** ProtectAI v2 reports 99.99% on its own data and 0.701 AUC (with 0% TPR at low FPR) on PromptShield.
3. **Scaling the base model helps more than scaling the training data.** PromptShield (Llama-3.1-8B) outperforms every encoder by a wide margin at low FPR, even at modest training-data scale (20K samples).

---

## 12. Practical Selection Guidance

For practitioners building a production guardrail, the literature now points toward a layered approach rather than any single classifier:

- **For lowest-latency English first-line defense (~5–10 ms):** ProtectAI v2 or CodeIntegrity PromptGuard or hlyn/judge-deberta-70m — but expect over-defense and assume sophisticated attackers will pass through.
- **For multilingual first-line defense:** Meta Llama Prompt Guard 2 (86M) or Azure Prompt Shields.
- **For best low-FPR encoder-class performance:** Qualifire Sentinel (ModernBERT-L) if you accept self-reported numbers; ProtectAI v2 if you accept ~80% PINT.
- **For best out-of-distribution performance at low FPR:** PromptShield (Llama-3.1-8B) — at the cost of 200+ ms latency.
- **For indirect injection in document/email contexts:** Azure Prompt Shields with Spotlighting, or a defense-in-depth combination including Microsoft's BIPIA-trained detectors.
- **For mitigating over-defense:** InjecGuard or a CourtGuard-style multiagent debate.
- **For long-term architectural defense:** Per the CodeIntegrity post-mortem, do not rely on detection alone — invest in structural data/instruction separation, schema-constrained outputs, and capability-based permissions on tool calls.

---

## 13. Open Research Gaps and Recent Trends (2024–2026)

1. **Multilingual coverage for open models** remains poor. Only Meta and commercial vendors have meaningful non-English support.
2. **Indirect prompt injection detection** is dominated by closed commercial offerings (Azure Spotlighting); open detectors lag.
3. **Adaptive attacks (character injection, optimization-based)** routinely bypass even commercial guardrails. The "Bypassing" paper (April 2025, arXiv 2504.11168) shows emoji smuggling alone achieves 100% ASR on most detectors.
4. **Trend toward decoder-based detectors:** Sentinel v2 (Qwen3-0.6B), PromptShield (Llama-3.1-8B), CourtGuard (Llama/Phi multiagent), and the broader LLM-as-judge approach suggest the field is moving away from pure encoder classifiers.
5. **Trend toward over-defense as a first-class metric.** NotInject and similar benign-only benchmarks are becoming required reporting.
6. **Trend toward low-FPR evaluation.** PromptShield's TPR@FPR=0.1% style reporting is replacing aggregate accuracy/F1 as the production-relevant metric.
7. **Game-theoretic and adversarially trained detectors** (DataSentinel, FreeLB-trained models like hlyn) are an active research thread.
8. **The "AI solving AI" critique** (CodeIntegrity) is pushing architecturally minded teams toward structural defenses (capability-based security, constrained execution) rather than detection-only strategies.
9. **Multimodal injection detection** is essentially open territory; only Llama Guard 4 currently addresses multimodal safety, and it is a content-moderation model, not an injection detector.
10. **Benchmark consolidation pressure.** With models routinely overfitting to public datasets, the community is increasingly relying on continuously refreshed, partially private benchmarks (PINT, Qualifire-internal, PromptShield) — a trend that aids defenders but reduces academic reproducibility.

---

## 14. Conclusion

The prompt injection detector landscape in mid-2026 is rich but uneven. ModernBERT-based detectors (Sentinel, CodeIntegrity PromptGuard) and DeBERTa-based detectors (ProtectAI, hlyn) dominate the open-source ecosystem and report 95–99% in-distribution accuracy. Independent low-FPR evaluations (PromptShield, PINT) reveal much weaker generalization, with several headline detectors collapsing entirely at deployment-grade FPRs. Commercial offerings (Lakera Guard 95.22% on PINT, Azure Prompt Shields 89.12%, AWS Bedrock 89.24%) lead on neutral benchmarks but are bound to specific platforms. LLM-based detectors (PromptShield's Llama-3.1-8B at AUC 0.997) achieve the strongest results but at 20–100× the latency. The most important conceptual development of the past 18 months is not architectural but methodological: NotInject's over-defense metric, PromptShield's low-FPR regime, and CodeIntegrity's "98% post-mortem" have together established that high in-distribution accuracy on small public benchmarks is no longer credible as a deployment-readiness signal. The practical state of the art is a layered defense — a fast encoder gate, an LLM-as-judge for ambiguous cases, an over-defense-aware benign filter, and, ultimately, architectural separation of trusted instructions from untrusted data.