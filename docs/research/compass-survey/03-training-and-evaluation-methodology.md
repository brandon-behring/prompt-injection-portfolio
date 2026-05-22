# How We Actually Know This Works: Training & Evaluation Methodology for Prompt Injection Detectors

## TL;DR

- **The field's headline numbers are largely meaningless.** Detectors routinely report 98–99% accuracy on held-out splits of the same mixture they trained on (ProtectAI's deberta-v3-base-prompt-injection-v1 reports F1 0.9998; CodeIntegrity's PromptGuard reports 98.01% accuracy), yet the same detectors are bypassed at up to 100% by simple character-injection or out-of-distribution evaluations. The PromptShield benchmark (Jacob et al., CODASPY 2025) and Lakera PINT have established that **TPR at low FPR (≤1%, ≤0.1%)** and **independent out-of-distribution test sets** are the only metrics that survive contact with production.
- **Three training paradigms dominate, with sharply different evaluation needs.** Encoder classifiers (ProtectAI, Meta Prompt Guard, Qualifire Sentinel, CodeIntegrity PromptGuard, InjecGuard) are trained with supervised cross-entropy plus increasingly elaborate tricks (energy loss, DoRA, SupCon, FreeLB, R-Drop); LLM-based detectors (PromptShield-8B, DataSentinel, Sentinel-v2 Qwen3-0.6B) are LoRA/QLoRA fine-tuned; and architectural defenses (StruQ, SecAlign, Meta SecAlign, Instruction Hierarchy, Jatmo, CaMeL) train the agent LLM itself with structured tokens, DPO preference pairs, or distillation. Detectors and architectural defenses are not interchangeable and require fundamentally different benchmarks.
- **The recommended evaluation stack for 2026 is now well-defined.** A credible 2026 evaluation must report (1) AUC-PR and TPR at 1%, 0.1%, 0.05% FPR on *out-of-distribution* benign data (PromptShield), (2) over-defense accuracy on NotInject's 339 trigger-word prompts (InjecGuard), (3) PINT score on Lakera's 4,314-input held-out benchmark, (4) end-to-end ASR/utility tradeoff on AgentDojo's 97 tasks × 629 security cases or BIPIA, and (5) adaptive-attack resilience à la LLMail-Inject (208,095 attacks from 839 participants). Anything short of that is essentially marketing.

---

## 1. Training Data Sources — Exhaustive Catalog

### 1.1 Foundational small datasets

| Dataset | Origin / Year | Size | Composition | Construction | License | Known issues |
|---|---|---|---|---|---|---|
| **deepset/prompt-injections** | deepset (Haystack), 2023 | 662 rows total (546 train + 116 test; 263 injections, 399 legitimate requests) | Binary (INJECTION/LEGIT); multilingual EN/DE/ES | Handwritten + sourced injections; legit prompts assumed to be Q&A or keyword search | Apache-2.0 | Tiny; trivially memorized; underlies 45+ HF detectors per HF index; "trigger-happy" per its own card |
| **jackhhao/jailbreak-classification** | Jack Hao, 2023 | 1,306 rows (640 benign / 666 jailbreak) | Jailbreaks scraped from `verazuo/jailbreak_llms` (Reddit/Discord) plus benign prompts | Scraped + handwritten | Apache-2.0 | Conflates jailbreaks with injections; balanced but small |
| **xTRam1/safe-guard-prompt-injection** (v1, v2) | xTRam1 (community), 2023–24 | 10,300 rows v1 (8,240 train / 2,060 test); v2 expanded | Binary; mixes deepset + scraped attacks | Aggregated | Apache-2.0 | Heavy overlap with deepset; train/test leakage when combined |
| **verazuo/jailbreak_llms** ("In the Wild" / DAN) | Shen, Chen, Backes, Shen, Zhang — CCS 2024 | 15,140 prompts (1,405 labeled jailbreaks) | Reddit, Discord, scraped jailbreak websites, open-source datasets, Dec 2022–Dec 2023 | Scraped real-world | MIT | English only; ChatGPT-centric; rapid drift |
| **TrustAIRLab/in-the-wild-jailbreak-prompts** | Same authors as above | 1,405 jailbreak prompts | Subset of jailbreak_llms | Scraped | MIT | Same as above |
| **lakera/gandalf_ignore_instructions** | Lakera, from Gandalf game (2023–) | ~1K public test split | Pure injections (no benign); "ignore instructions" sub-game | Crowd-sourced from real players | MIT (public slice) | Lakera has the *full* private telemetry — an acknowledged "unfair advantage" |
| **lmsys/toxic-chat** | LMSYS, 2023 | ~10K real chatbot conversations | Mostly benign with toxicity / jailbreak labels | Real LMSYS chatbot arena logs, human-labeled | CC-BY-NC | Toxicity ≠ injection; useful benign distractor |

### 1.2 Mid-size aggregated datasets

| Dataset | Origin | Size | Composition | Use |
|---|---|---|---|---|
| **geekyrakshit/prompt-injection-dataset** | Community 2024 | 534,434 rows (271K train / 264K test) | Aggregate of deepset + xTRam1 + jayavibhav/prompt-injection | Used by CodeIntegrity PromptGuard, hlyn |
| **reshabhs/SPML-Chatbot-Prompt-Injection** | SPML/Reshabh, 2024 | ~16K rows | System-prompt + user-prompt structure | Application-structured |
| **Qualifire/Qualifire-prompt-injection-benchmark** | Qualifire 2024 | ~5K samples | Public test benchmark | One of Sentinel's eval datasets |
| **rogue-security/prompt-injections-benchmark** | rogue-security 2024 (Qualifire) | 5,000 samples | Adversarial edge cases | Used by hlyn as held-out (explicitly excluded from training) |
| **alespalla/chatbot-instruction-prompts** | alespalla | ~258K | All benign instructions | Negative class for Sentinel and others |
| **VMware/open-instruct** | VMware | ~50K | Benign instructions | Negative class for Sentinel, hlyn |
| **microsoft/orca-agentinstruct-1M-v1** | Microsoft 2024 | 1M rows | Synthetic benign agentic instructions | Source of benign in PromptShield, Sentinel |

### 1.3 Crowd-sourced & competition-derived datasets

| Dataset | Source | Size | Construction |
|---|---|---|---|
| **TensorTrust** | Toyer et al. (Berkeley/Georgia Tech/Harvard), ICLR 2024 (arXiv 2311.01011) | 126,000 attacks + 46,000 defenses (ICLR-published count); 563K/118K in later post-publication release | Crowd-sourced from "Tensor Trust" web game (simulated bank); 2 attack categories: prompt extraction and prompt hijacking |
| **HackAPrompt 1.0** | Schulhoff et al., EMNLP 2023 (2311.16119) | 600,000+ adversarial prompts | Global competition vs. GPT-3, FlanT5-XXL, ChatGPT; $37,500 prize pool; comprehensive taxonomical ontology |
| **microsoft/llmail-inject-challenge** | Abdelnabi et al. (Microsoft), SaTML 2025 (2506.09956) | 208,095 unique submissions (370,724 raw Phase 1 + 90,916 Phase 2) from 839 participants | Adaptive CTF: attacker emails an LLM email assistant; multiple defenses, LLMs (Phi-3, GPT-4o-mini), RAG configurations |
| **Gandalf data** | Lakera | Millions of private game plays | Real-world adversarial attempts; only ~1K public via `lakera/gandalf_ignore_instructions` |

### 1.4 Safety / red-team training corpora reused for injection

| Dataset | Authors | Size | Notes |
|---|---|---|---|
| **AdvBench** | Zou et al. (CMU) 2023, "Universal & Transferable…" | 520 harmful behaviors | Original GCG paper; often re-used as positives |
| **HarmBench** | Mazeika et al. 2024 | ~400 behaviors | Standardized red-team eval |
| **JailbreakBench / JBB-Behaviors** | Chao, Debenedetti, Robey et al. NeurIPS D&B 2024 (2404.01318) | 100 misuse + 100 matched benign behaviors; 45% original, 18% from AdvBench, 27% from TDC/HarmBench | 10 OpenAI-policy categories |
| **allenai/wildjailbreak** | Jiang et al. AI2, 2024 | 262K synthetic adversarial + 50K vanilla | GPT-4 generated; "Mining the Wild" pipeline |
| **allenai/wildguardmix** | AI2 2024 | ~92K rows | Prompt + response classification training set; used by Vijil |
| **OpenSafetyLab/Salad-Data** | OpenSafetyLab 2024 | ~21K filtered | Safety taxonomy |
| **JailbreakV-28K** | Multi-author 2024 | 28,000 | Multimodal jailbreaks; vision + text |
| **PurpleLlama / CyberSecEval** | Meta 2023–25 | Multiple subsets | Includes prompt-injection sub-suite |

### 1.5 Indirect-injection benchmarks

| Benchmark | Authors | Size | Methodology |
|---|---|---|---|
| **BIPIA** | Yi et al. (Microsoft / USTC), 2312.14197 (KDD '25) | 626,250 train / 86,250 test prompts across 5 application scenarios (Email/Web/Table QA, Summarization, Code QA), 375 attack variants × 250 attacker goals; 25 LLMs evaluated | 6 attack subtypes (Task Automation, Business Promotion, Phishing, Information Dissemination, Marketing, Information Manipulation); GPT-4 + rule judges |
| **InjecAgent** | Zhan et al., 2403.02691 | 1,054 test cases, 17 user tools, 62 attacker tools | Two intent types: Direct Harm and Data Stealing (2-step S1/S2); ASR-valid + ASR-all |
| **AgentDojo** | Debenedetti, Zhang, Balunović et al. (ETH), NeurIPS D&B 2024 (2406.13352) | 97 user tasks, 629 security test cases across banking, Slack, travel, workspace | Dynamic, extensible; reports benign utility, utility under attack, targeted ASR |
| **NotInject** | Li, Liu, Xiao (InjecGuard, 2410.22770) | 339 benign prompts carefully constructed with trigger words ("ignore", "cancel", etc.) at 3 difficulty levels | Pure over-defense measurement |
| **PINT** | Lakera | 4,314 inputs (3,016 English + 1,298 non-English across 12 languages) blended public + proprietary | Categories: `internal_prompt_injection`, `jailbreak`, `hard_negatives`, `chat`, `documents`, `public_prompt_injection`; never trained on by Lakera Guard |
| **PromptShield benchmark** | Jacob, Alzahrani, Hu, Alomair, Wagner — CODASPY 2025 (2501.15145) | Released as `hendzh/PromptShield` on HF; conversational + application-structured | Train/test/eval; ablation at 1K, 5K, 10K, 20K |

### 1.6 Specialized / newer (2025–26)

- **DhruvTre/jailbreakbench-paraphrase-2025-08** — JBB-Behaviors paraphrased augmentation; used by CodeIntegrity.
- **hendzh/PromptShield** — Berkeley's open release of the PromptShield training/eval mixture.
- **hlyn/prompt-injection-judge-deberta-dataset** — 12 source datasets merged, MD5-deduplicated, 6 label-contradiction samples purged, empty-string-filtered.
- **protectai/prompt-injection-validation** — 3,227 rows across 7 splits (InjecGuard_valid 144, spikee 986, bipia_code 50, bipia_text 75, not_inject 339, wildguard 971, deepset 662).

---

## 2. Training Methodologies

### 2.1 Encoder Classifiers

**Baseline recipe (BERT/DeBERTa/ModernBERT):** AdamW, LR 2e-5 to 5e-5, batch 8–32, 3 epochs, weight decay 0.01, cross-entropy. The original `deepset/deberta-v3-base-injection` model card lists `lr=2e-5, batch=8, AdamW (β=0.9,0.999, ε=1e-8), linear scheduler, 3 epochs`.

**Advanced techniques used by leading detectors:**

| Technique | Used by | What it does |
|---|---|---|
| **Energy-based loss** (Liu NeurIPS 2020, arXiv 2010.03759) | Meta Llama Prompt Guard 2, CodeIntegrity PromptGuard | Pushes benign → low-energy, malicious → high-energy; improves OOD; CodeIntegrity uses energy thresholds (<-25 benign, >-7 malicious) |
| **Custom Recall@1%FPR loss** | Meta Llama Prompt Guard 2 | Reweights training to maximize recall at fixed low FPR; per Meta's card: "*the dramatic increase in Recall @ 1% FPR is due to the custom loss function used for the new model*" |
| **EDL (Evidential Deep Learning)** | hlyn/prompt-injection-judge-deberta-70m | Parameterizes Dirichlet distribution for epistemic uncertainty; enables 95.8% precision ceiling |
| **DoRA** (Weight-Decomposed LoRA) | hlyn | Magnitude + direction decomposition |
| **SupCon** | hlyn | Pulls attack embeddings apart from benign |
| **FreeLB** | hlyn | Embedding-space adversarial perturbations |
| **R-Drop** | hlyn | Bidirectional KL between dropout passes |
| **SWA + Mixout** | hlyn (full stack) | Weight averaging + parameter regularization |
| **LoRA/PEFT** | ccss17, Sentinel-v2 | Parameter-efficient |
| **INT8 ONNX quantization** | hlyn (83 MB → ~101ms on M1), ProtectAI | Deployment |

**Multilingual base models:** Meta Prompt Guard 2 86M uses `mDeBERTa-base`; Prompt Guard 2 22M uses `DeBERTa-xsmall`. Both are MIT-licensed Microsoft models.

### 2.2 LLM-Based Detectors

**PromptShield (Berkeley):** LoRA fine-tune of Llama-3.1-8B-Instruct; LR 2e-4, 3 epochs. Data augmentation: "*Before training our detector we augment training datapoints by randomly inserting 1–3 newline delimiters (i.e., \n) at three locations.*" Ablation at 1K/5K/10K/20K training samples: at 0.1% FPR, TPR rises from 20.9% (1K) to 47.5% (20K); AUC from 0.981 to 0.998. Six base models compared (DeBERTa-v3-base 184M, FLAN-T5 small/base/large, Llama-3.2-1B, Llama-3.1-8B).

**DataSentinel (Liu et al., 2504.11358):** Fine-tunes a small LLM via game-theoretic minimax — alternating between (inner-max) optimizing contaminated inputs to evade detection while misleading the backend LLM, and (outer-min) fine-tuning the detector. Uses a "known-answer" probe: ask the detector to repeat a secret key like "DGDSGNH"; if the secret is absent in the output, the input is flagged contaminated.

**Sentinel v2 (Qualifire):** Moved from ModernBERT-large (v1) to Qwen3-0.6B decoder; context extended 8K → 32K; size reduced 1.6 GB → 1.2 GB (FP16); 3× more training data; average F1 across five benchmarks rose from 0.936 (v1) to **0.964** (v2).

**Llama Guard family:** Llama-3-8B fine-tuned on a Meta-curated safety taxonomy (not specifically injection).

### 2.3 Architectural Defenses (training the agent, not a separate detector)

| Defense | Authors | Recipe |
|---|---|---|
| **StruQ** | Chen, Piet, Sitawarin, Wagner — arXiv 2402.06363 | SFT on data with reserved delimiter tokens marking instruction vs. data; trained on clean + simulated-injection samples; LLM learns to follow only the instruction part |
| **SecAlign** | Chen, Zharmagambetov, Mahloujifar, Chaudhuri, Guo (Meta + Berkeley) — 2410.05451 | DPO on (intended-instruction, secure-response, insecure-response) triples constructed by simulating injections; preference-optimizes a much larger margin between secure/insecure outputs than StruQ |
| **Jatmo** | Piet, Alrashed, Sitawarin, Wagner — arXiv 2312.17673 | Distills from a teacher instruction-tuned model into a task-specific model that follows only the original task |
| **Meta SecAlign** | Chen et al. 2507.02735 | Applies SecAlign to Llama-3.3-70B; introduces an "input" role in the chat template |
| **Instruction Hierarchy** | Wallace et al. (OpenAI), arXiv 2404.13208 | Trains GPT-3.5/4 with "context synthesis": synthesizes (system, user, tool) conversations with conflicting instructions and trains the model to prefer the higher-priority source |
| **TaskTracker** | Abdelnabi, Fay, Cherubin, Salem, Fritz, Paverd (Microsoft) — SaTML 2025 (arXiv 2406.00799) | Extracts activations before and after external data is processed; trains a **linear probe** on the activation deltas; toolkit releases >500K instances across 6 LLMs (Mistral 7B, Llama-3 8B/70B, Mixtral 8x7B, Phi-3); reports >0.99 ROC AUC OOD with no model fine-tuning |
| **CaMeL** | Debenedetti et al. 2503.18813 | Capability-based isolation; evaluated on AgentDojo |

### 2.4 Game-Theoretic / Adversarial Training

- **DataSentinel** minimax (above).
- **GCG-suffix adversarial training** used to harden some detectors.
- **Red-team pipelines:** Meta's Prompt Guard 2 training includes a private red-team dataset distinct from training sources.

---

## 3. Evaluation Methodologies

### 3.1 Metrics and what they mean

| Metric | When it matters | Failure mode |
|---|---|---|
| Accuracy | Almost never useful with imbalanced production data (typical: 1:10,000 attack:benign) | Inflated by majority class |
| F1, precision, recall | Standard but threshold-dependent | Picking threshold post-hoc |
| AUC-ROC | Threshold-free ranking | Insensitive at low-FPR tail |
| **AUC-PR** | Better under class imbalance | Still summary number |
| **TPR @ low FPR** (PromptShield's signature contribution) | Production threshold reality | Even 1% FPR is unacceptable at scale; PromptShield reports 1%, 0.5%, 0.1%, 0.05% |
| ASR (Attack Success Rate) | For evaluating *attacks on LLMs*, not detectors | Doesn't capture utility cost |
| **APR (Attack Prevention Rate)** | Meta Prompt Guard 2's metric: % of attacks blocked at ≤3% utility loss | Combines security + utility |
| Utility score (AgentDojo) | Tradeoff with security | Easy to game |
| Over-defense accuracy (NotInject) | False-positives on injection-flavored benign | Penalizes trigger-word reliance |

PromptShield's specific finding: ProtectAI's deberta-v3-base-prompt-injection-v2, despite a 99.99% reported in-distribution F1, collapses at low-FPR on out-of-distribution data. Lakera's PINT scoreboard shows Lakera Guard itself at only **92.55%**, confirming Goodhart's law has hit public benchmarks.

### 3.2 Evaluation protocols

1. **Held-out test from same mixture** — what most HF model cards report; near-meaningless because training and test share distribution.
2. **OOD evaluation** — PromptShield's contribution: holding out entire datasets, not just rows.
3. **Independent third-party benchmarks** — PINT (4,314 inputs, never trained on by any evaluated system).
4. **Adaptive-attack evaluation** — LLMail-Inject is the gold standard: 839 participants over 3 months adaptively attacking known defenses, generating 208K submissions.
5. **End-to-end agentic evaluation** — AgentDojo's 97 tasks × 629 security cases measure both utility *and* security in dynamic tool-calling.
6. **Production telemetry** — Lakera's Gandalf logs, OpenAI moderation logs; gives an "unfair advantage" but not reproducible.

### 3.3 Specific evaluation pathologies

- **Goodhart's law on public benchmarks.** Lakera explicitly states PINT was designed to fight this: "*having a 99% accuracy on a Hugging Face prompt injection dataset does not translate into being an effective defense in practice.*"
- **Training-data leakage into benchmarks.** Models trained on `deepset/prompt-injections` are then evaluated on overlapping subsets.
- **CodeIntegrity "98% accurate and still broken" critique** (Steven Jung, Jan 3 2026): "*Classical ML metrics evaluate performance on held-out slices of historical data. The model and test set share the same distribution… This measures memorization, not generalization.*" Cites Joshua Saxe: "*An LLM scoring an 85% F-score on your test data is likely more meaningful than a classical ML model scoring 95% but fit to the test distribution.*"
- **"Are Firewalls All You Need?"** (Bhagwatkar et al., arXiv 2510.05244, NeurIPS 2025): "*Critical limitations including flawed success metrics, implementation bugs, and most importantly, weak attacks, hindering progress.*" The paper shows AgentDojo, Agent Security Bench, InjecAgent, and τ-Bench are saturated by a simple two-firewall defense (Tool-Input Minimizer + Tool-Output Sanitizer) achieving 0% ASR with high utility.
- **"Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails"** (Hackett et al., arXiv 2504.11168): Character-injection and adversarial-ML evasion achieve "*up to 100% evasion success*" against Azure Prompt Shield, ProtectAI v1/v2, Meta Prompt Guard, NVIDIA NeMo Guard, and Vijil — using 12 character techniques (zero-width, homoglyph, bidi, emoji smuggling, Unicode tags, etc.) and 8 TextAttack methods.

---

## 4. Detector-Specific Training & Eval Recipes

### 4.1 ProtectAI deberta-v3-base-prompt-injection-v2

- **Base:** `microsoft/deberta-v3-base` (184M).
- **Data:** "*meticulously assembled from various public open datasets… prompt injections crafted using insights gathered from academic research papers, articles, security competitions, and valuable LLM Guard's community feedback*" — undisclosed exact composition. V1's card states ~30% injection / ~70% benign.
- **Tuning:** Over 20 hyperparameter configurations tested.
- **Reported results:** 99.99% accuracy / F1 0.9998 on internal test (v1); 95.25% on untrained external sets.
- **Why it fails PromptShield:** evaluated on PromptShield's OOD benign distribution, ProtectAI's TPR collapses at <1% FPR; its 99.99% is a memorization artifact.
- **Bypassability:** 100% character-injection bypass per arXiv 2504.11168.

### 4.2 Qualifire Sentinel v1 / v2

- **v1:** `qualifire/prompt-injection-sentinel`. Base: `answerdotai/ModernBERT-large` (~395M). Data: aggregation of "*a few open-source and private collections*" amalgamating role-playing, instruction hijacking, biased-content attacks, plus benign instructions; private subset for nuanced misclassifications. Composition: **70% benign / 30% injection**, **90/10 train/test**.
- **Eval:** Two fronts — (a) 10% internal held-out reporting 0.987 accuracy / 0.980 F1; (b) **four public benchmarks** with average F1 0.938 vs. ProtectAI's 0.709.
- **Comparison choice:** Only against ProtectAI deberta-v3-base — the easiest baseline available.
- **v2 (Qwen3-0.6B):** 3× more training data, F1 0.964 across 5 benchmarks, 32K context, 1.2 GB FP16.

### 4.3 Meta Llama Prompt Guard 2 (86M & 22M)

- **Bases:** mDeBERTa-base (86M); DeBERTa-xsmall (22M) — both MIT.
- **Training corpus:** Open-source benign + open-source injections + synthetic + Meta red-team (private).
- **Loss:** Custom Recall@1% FPR. Verbatim from model card: "*the dramatic increase in Recall @ 1% FPR is due to the custom loss function used for the new model, which results in prompts similar to known injection payloads reliably generating the highest scores even in out-of-distribution settings.*"
- **Why v2 dropped JAILBREAK/INJECTION distinction:** Both v1 labels collapse into one "attack" binary; rationale is that the operational decision is the same.
- **Eval:** Private benchmark + AgentDojo APR ("% of attacks blocked at ≤3% utility loss").

### 4.4 PromptShield (Berkeley)

- **Base model winners:** Llama-3.1-8B-Instruct (LoRA, LR 2e-4, 3 epochs); also evaluated DeBERTa-v3-base, FLAN-T5 small/base/large, Llama-3.2-1B.
- **Augmentation:** Random insertion of 1–3 `\n` delimiters at three locations before training datapoints.
- **Benchmark construction:** Conversational data (chatbots) + application-structured data (LLM-integrated apps) — two-track design specifically chosen so memorizing one doesn't transfer to the other.
- **Results table (verbatim from paper):**

| Base | Params | AUC | TPR@1%FPR | TPR@0.5%FPR | TPR@0.1%FPR | TPR@0.05%FPR |
|---|---|---|---|---|---|---|
| DeBERTa-v3-base | 184M | 0.976 | 43.22% | 40.50% | 31.45% | 0.00% |
| FLAN-T5-small | 61M | 0.942 | 7.56% | 4.66% | 3.05% | 2.57% |
| FLAN-T5-base | 223M | 0.971 | 70.69% | 62.94% | 34.69% | 20.77% |
| FLAN-T5-large | 751M | 0.985 | 55.60% | 46.30% | 40.56% | 35.72% |
| Llama-3.2-1B | 1B | 0.960 | 67.32% | 44.51% | 30.76% | 22.29% |
| **Llama-3.1-8B** | 8B | **0.998** | **94.80%** | **87.80%** | **65.33%** | **47.53%** |

- **Ablation (Llama-3.1-8B):** At 0.1% FPR, TPR rises 20.9% (1K samples) → 47.5% (20K); AUC 0.981 → 0.998.

### 4.5 CodeIntegrity PromptGuard

- **Base:** `answerdotai/ModernBERT-base`.
- **Training corpus:** 955K+ samples, exhaustive composition from model card: deepset/prompt-injections, jackhhao/jailbreak-classification, JailbreakBench/JBB-Behaviors, JailbreakV-28K, DhruvTre/jailbreakbench-paraphrase-2025-08, microsoft/llmail-inject-challenge, hendzh/PromptShield, geekyrakshit/prompt-injection-dataset, xTRam1/safe-guard-prompt-injection.
- **Loss:** Modified energy-based loss (inspired by Meta Prompt Guard 2 + Liu NeurIPS 2020). Energy thresholds: <-25 benign, >-7 malicious.
- **Self-reported metrics:** Accuracy 98.01%, Precision 98.54%, Recall 95.60%, F1 97.04%.
- **Self-critique** (the "98% post-mortem", Jan 2026): "*98% on historical data ≠ 98% on tomorrow's attacks… Treat your 98% detector as a speed bump, not a wall.*"

### 4.6 InjecGuard (Li, Liu, Xiao — 2410.22770)

- **Training data:** Open-source datasets + augmented benign sets.
- **Key technique:** **MOF (Mitigating Over-defense for Free)** — retraining from scratch with curated benign augmentation that includes trigger words ("ignore", "cancel", "override") in benign contexts.
- **Result:** Combining MOF + retrain-from-scratch yields average accuracy 83.48%, over-defense 87.32%, benign 85.74%, malicious 77.39%.
- **NotInject:** 339 benign prompts × 3 difficulty levels by number of trigger words.
- **Eval suite:** NotInject + PINT + WildGuard-Benign + BIPIA.
- **Headline finding:** Pre-MOF ProtectAI v2 over-defense accuracy <60% (close to random); MOF achieves >85%.

### 4.7 hlyn/prompt-injection-judge-deberta-70m

- **Base:** DeBERTa-v3-xsmall (70M).
- **Training data:** Custom 12-source aggregation, MD5-deduplicated, label-contradiction-purged (6 samples removed), empty-string filtered.
- **Training stack:** EDL + DoRA + SupCon + FreeLB + R-Drop + SWA + Mixout — likely the most aggressive published recipe.
- **Deployment:** INT8 ONNX, 83 MB, ~101 ms on Apple M1 CPU.
- **Eval:** rogue-security/prompt-injections-benchmark (5,000 samples, **explicitly excluded from training**) vs. ProtectAI v2.
- **Claimed improvement:** Drastically higher precision (vs. ProtectAI's ~65% on that set) and ~6× lower CPU latency.

### 4.8 Architectural defenses summary

- **StruQ:** SFT on `Alpaca`-derived data with reserved delimiters; per the BAIR blog (April 2025): "*StruQ, with an ASR 45%, significantly mitigates prompt injections compared to prompting-based defenses. SecAlign further reduces the ASR from StruQ to 8%.*" StruQ effectively blocks optimization-free attacks but remains vulnerable to optimization-based ones (27% / 45% ASR on Mistral-7B / Llama-3-8B Instruct respectively).
- **SecAlign:** DPO with simulated injection prompts; ASR drops to 1% and 8% on Mistral-7B-Instruct and Llama-3-8B-Instruct respectively under the strongest attacks; **no AlpacaEval2 WinRate drop**.
- **Meta SecAlign on Llama-3.3-70B:** generalizes to a new "input" chat role.
- **CaMeL:** evaluated on AgentDojo; capability-based isolation.

---

## 5. Cross-Cutting Analysis

### 5.1 The training–eval distribution gap

ProtectAI v1's 99.99% F1 on its own test set → 65% precision on Qualifire's rogue benchmark → up to 100% bypass under character injection. CodeIntegrity's 98.01% accuracy → admitted memorization. The pattern is universal.

### 5.2 Choice of baselines

A consistent pattern: vendors compare against the weakest publicly available competitor.
- Qualifire Sentinel paper compares only to ProtectAI v2.
- hlyn compares only to ProtectAI v2.
- Meta Prompt Guard 2 compares against Prompt Guard v1.
- Almost no vendor compares against PromptShield-Llama-8B or DataSentinel.

### 5.3 PromptShield's TPR@0.1%FPR as a forcing function

The shift from accuracy/F1 reporting to TPR@LowFPR has revealed that most encoder classifiers under 200M params collapse below 35% TPR at production-realistic operating points. This is the single most important methodological advance in 2024–25.

### 5.4 NotInject's revelation

Over-defense is now a first-class failure mode. ProtectAI v2 over-defense accuracy <60% means roughly 4 of every 10 legitimate users with trigger words get blocked.

### 5.5 AgentDojo's utility-aware framing

In agentic settings, raw ASR is misleading because models that fail tasks have artificially low ASR. AgentDojo's coupled "benign utility" and "utility under attack" metrics reveal the "*inverse scaling law*": more capable models like Claude 3.5 Sonnet (78.22% utility) and GPT-4o (47.69% targeted ASR) are simultaneously more useful and more attackable.

### 5.6 The Goodhart problem

Lakera explicitly designed PINT to be unhackable by training: "*all evaluated solutions (including Lakera Guard) are not directly trained on any of the inputs in this dataset.*" Even so, Lakera Guard scores only 92.55% on it — implying every detector has nontrivial residual error in the wild.

### 5.7 Production telemetry vs. academic benchmarks

Lakera's Gandalf game generates millions of real adversarial attempts; only ~1K are public. This is an explicit, acknowledged unfair advantage that academic baselines cannot replicate.

### 5.8 Reproducibility crisis

- Qualifire Sentinel's private dataset slice is undisclosed.
- Meta Prompt Guard 2's red-team data is undisclosed.
- ProtectAI's exact mixture proportions are undisclosed.
- Most "winning" detectors are not reproducible end-to-end from public artifacts.

---

## 6. Dataset Construction Methodology

| Method | Examples | Strengths | Weaknesses |
|---|---|---|---|
| Manual red-teaming | Meta Prompt Guard 2 private data, Lakera Gandalf | High-quality, targeted | Doesn't scale |
| LLM-generated synthetic | allenai/wildjailbreak (GPT-4), CodeIntegrity augmentation | Scales | Distributional bias from generator model's safety training |
| Crowd-sourced attacks | TensorTrust (126K attacks / 46K defenses per ICLR), HackAPrompt (600K), LLMail-Inject (208K) | Real adversarial creativity | Competition incentives skew distribution |
| Adversarial optimization | GCG, PAIR, AutoDAN suffix generation | Strong attacks | Token-level patterns may not generalize |
| Real-world bug bounty | Embrace The Red, HackerOne disclosures | Realistic | Sparse |
| Translation augmentation | Lakera multilingual PINT (12 languages), Meta multilingual training | Multilingual coverage | Translation drift |
| Paraphrase augmentation | DhruvTre/jailbreakbench-paraphrase-2025-08 | Distribution expansion | Surface variance only |
| Character-injection augmentation | Defenders mostly *don't* do this; attackers (per 2504.11168) exploit the gap | — | — |
| Template-based generation | BIPIA fills 125 attack instructions into 3 positions × 5 tasks | Systematic | Easy to memorize |

---

## 7. Recommendations & Best Practices for 2026 Evaluation

### What a rigorous 2026 detector evaluation must include

1. **Multiple independent benchmarks**, with PINT and PromptShield as mandatory.
2. **TPR at 1%, 0.5%, 0.1%, 0.05% FPR** — not just accuracy or F1.
3. **OOD evaluation:** held-out *datasets*, not held-out rows of the same mixture.
4. **Over-defense (NotInject) score** at all 3 difficulty levels.
5. **Adaptive-attack resilience** — minimum bar: pass arXiv 2504.11168's character-injection suite; gold standard: an LLMail-Inject-style adaptive competition.
6. **Per-attack-category breakdown** — direct vs. indirect; goal-hijacking vs. extraction; English vs. multilingual.
7. **Multilingual coverage** (PINT's 12 non-English languages or Meta Prompt Guard 2's multilingual base).
8. **Utility/security tradeoff** on AgentDojo or BIPIA — security in isolation is meaningless.
9. **Independent reproducibility:** open training data, hyperparameters, seeds.
10. **Living benchmarks > static**: PINT and AgentDojo are explicitly designed to evolve.

### Staged recommendations

- **If you must ship today**, use Llama Prompt Guard 2 86M plus PromptShield-8B (or DataSentinel) as a two-tier filter; instrument every false-positive; treat detection as a speed bump (per CodeIntegrity).
- **For high-stakes agentic systems**, prefer architectural defenses (SecAlign, Instruction Hierarchy, CaMeL) over detectors; detection alone is bypassed at near-100% under character-injection.
- **For benchmark-trustworthy claims**, require: PINT + NotInject + AgentDojo + PromptShield, with TPR@0.1%FPR reported.
- **Trigger to reconsider:** any new vendor claiming >95% on a single public benchmark without low-FPR or OOD numbers should be treated as a marketing claim, not a security claim.

---

## Caveats

- LoRA rank for PromptShield's Llama-3.1-8B training is not explicit in retrieved snippets; the paper's Appendix B should be consulted directly.
- Many vendor "private dataset" composition figures are self-reported and unverifiable.
- "Up to 100% evasion" headlines from arXiv 2504.11168 hide per-system variance reported only in figures; specific numbers per guardrail require fetching the paper's Appendix A.1.
- BIPIA v1 and v4 report slightly different numbers; the v4 KDD '25 figures (250 attacker goals, 25 LLMs) are cited here.
- The CodeIntegrity blog is a vendor self-critique; its accuracy figures (98.01%) are self-reported.
- TensorTrust's ICLR 2024 paper reports 126,000 attacks + 46,000 defenses; subsequent post-publication dataset releases have grown to 563K/118K — choose the version corresponding to the dataset release you actually consume.