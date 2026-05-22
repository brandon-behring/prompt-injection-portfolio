# C1. Training data sources

_19 primary-source entries cataloging public datasets used to train prompt-injection detectors and adjacent guardrails. Each entry documents existence + provenance + size where in-abstract; license + composition + known leakage issues are surfaced in Status fields where the dataset card or paper makes them explicit. Per ADR-041 / ETHICS §1, datasets with attack content document existence + composition + license; attack examples are NOT excerpted into bullet bodies._

## C1.1. deepset/prompt-injections

- **deepset/prompt-injections** — deepset (2024).
  - **Source:** https://huggingface.co/datasets/deepset/prompt-injections
  - **Code:** —
  - **Mechanism:** HuggingFace community dataset for prompt-injection classification, hosted by deepset [claim_training_and_evaluation_deepset2024promptinjections_a1_existence].
  - **Result:** One of the earliest small baseline PI training corpora; widely re-used in encoder-detector training mixtures with known overlap across downstream models [claim_training_and_evaluation_deepset2024promptinjections_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile` (30-day window). Training-data-leakage signal: appears in many downstream detector training mixtures (memorization risk).

## C1.2. jackhhao/jailbreak-classification

- **jackhhao/jailbreak-classification** — jackhhao (2023).
  - **Source:** https://huggingface.co/datasets/jackhhao/jailbreak-classification
  - **Code:** —
  - **Mechanism:** HuggingFace community dataset of labeled jailbreak vs. benign prompts [claim_training_and_evaluation_jackhhao2023jailbreakclassification_a1_existence].
  - **Result:** Early small training corpus reused in several jailbreak/PI classifiers; no associated paper [claim_training_and_evaluation_jackhhao2023jailbreakclassification_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. (no widely-known paper)

## C1.3. xTRam1/safe-guard-prompt-injection

- **xTRam1/safe-guard-prompt-injection** — Erdogan, Shang, Goyal, Ijju (2024).
  - **Source:** https://huggingface.co/datasets/xTRam1/safe-guard-prompt-injection
  - **Code:** —
  - **Mechanism:** Community-uploaded HuggingFace dataset for PI classification [claim_training_and_evaluation_xtram2024safeguard_a1_existence].
  - **Result:** One of many mid-2024 small PI training corpora; treated as a community-mixture component in detector landscape [claim_training_and_evaluation_xtram2024safeguard_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. **Naming gotcha:** distinct from `xTRam1/safe-guard-v2` — verify maintainer + name in downstream citations (gotcha flagged in Phase 2 final report).

## C1.4. Shen et al. "Do Anything Now"

- **"Do Anything Now": Characterizing and Evaluating In-The-Wild Jailbreak Prompts on Large Language Models** — Shen et al. (ACM CCS 2024).
  - **Source:** https://arxiv.org/abs/2308.03825
  - **Code:** <https://github.com/verazuo/jailbreak_llms>
  - **Mechanism:** First large-scale measurement of in-the-wild jailbreak prompts collected from Reddit / Discord / dedicated websites [claim_training_and_evaluation_shen2023doanythingnow_a1_headline]; characterizes attack patterns and releases the verazuo/jailbreak_llms dataset [claim_training_and_evaluation_shen2023doanythingnow_a2_methodology].
  - **Result:** Releases the verazuo/jailbreak_llms dataset of real-world jailbreak prompts; used as evaluation/training corpus by downstream detector teams [claim_training_and_evaluation_shen2023doanythingnow_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: contains attack prompts; existence documented, examples not excerpted.

## C1.5. Lakera/gandalf_ignore_instructions

- **Lakera/gandalf_ignore_instructions** — Lakera (2023).
  - **Source:** https://huggingface.co/datasets/Lakera/gandalf_ignore_instructions
  - **Code:** —
  - **Mechanism:** HuggingFace dataset of prompts attempting to make the LLM ignore system instructions, derived from the public Lakera Gandalf challenge [claim_training_and_evaluation_lakera2023gandalfignore_a1_existence].
  - **Result:** Widely re-used as a training/evaluation subset in encoder PI detectors; Lakera-curated and -released [claim_training_and_evaluation_lakera2023gandalfignore_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. ETHICS: attack-content; existence documented.

## C1.6. Lin et al. ToxicChat

- **ToxicChat: Unveiling Hidden Challenges of Toxicity Detection in Real-World User-AI Conversation** — Lin et al. (EMNLP 2023 Findings).
  - **Source:** https://arxiv.org/abs/2310.17389
  - **Code:** —
  - **Mechanism:** Constructs ToxicChat from real Vicuna-online user-AI conversations with human-annotated toxicity + jailbreak labels [claim_training_and_evaluation_lin2023toxicchat_a1_headline]; analyzes how real-conversation toxicity differs from social-media benchmarks [claim_training_and_evaluation_lin2023toxicchat_a2_methodology].
  - **Result:** Provides the `lmsys/toxic-chat` dataset reused as a PI training subset and as a benign-conversation source [claim_training_and_evaluation_lin2023toxicchat_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. Out-of-domain note: cross-references content-moderation evaluation (cited only because LMSYS toxic-chat appears in PI training mixtures).

## C1.7. Sharma et al. SPML

- **SPML Chatbot Prompt Injection Dataset (reshabhs/SPML_Chatbot_Prompt_Injection)** — Sharma et al. (2024).
  - **Source:** https://huggingface.co/datasets/reshabhs/SPML_Chatbot_Prompt_Injection
  - **Code:** —
  - **Mechanism:** ~16K system-prompt vs user-prompt pairs designed for chatbot-style PI evaluation; SPML = System Prompt Meta Language [claim_training_and_evaluation_reshabh2024spml_a1_existence].
  - **Result:** Released alongside Sharma et al. SPML paper (arXiv 2402.11755); used in several detector training mixtures [claim_training_and_evaluation_reshabh2024spml_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. (uncertain venue) — companion paper exists at arXiv 2402.11755 but the dataset card is the canonical resource.

## C1.8. geekyrakshit/prompt-injection-dataset

- **geekyrakshit/prompt-injection-dataset** — Pal (2024).
  - **Source:** https://huggingface.co/datasets/geekyrakshit/prompt-injection-dataset
  - **Code:** —
  - **Mechanism:** Aggregated HuggingFace dataset combining multiple smaller PI corpora; one of the largest publicly-available PI training mixtures [claim_training_and_evaluation_geekyrakshit2024promptinjectiondataset_a1_existence].
  - **Result:** Aggregator-style provenance; individual-row provenance mixed (de-duplicated rollup of public PI sources); license of underlying components varies [claim_training_and_evaluation_geekyrakshit2024promptinjectiondataset_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. **License red flag (Phase 2 report):** aggregator provenance + mixed underlying licenses → downstream use requires per-row license tracing. (no widely-known paper)

## C1.9. Toyer et al. Tensor Trust

- **Tensor Trust: Interpretable Prompt Injection Attacks from an Online Game** — Toyer et al. (ICLR 2024).
  - **Source:** https://arxiv.org/abs/2311.01011
  - **Code:** <https://tensortrust.ai/paper>
  - **Mechanism:** Crowd-sourced PI attacks via the Tensor Trust online game in a defender-vs-attacker setting [claim_training_and_evaluation_toyer2023tensortrust_a1_headline]; analyzes interpretability of crowd-sourced attack patterns [claim_training_and_evaluation_toyer2023tensortrust_a2_methodology].
  - **Result:** Releases the TensorTrust dataset of diverse crowd-sourced adversarial prompts; ICLR 2024 publication [claim_training_and_evaluation_toyer2023tensortrust_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: attack-content; existence documented, examples not excerpted.

## C1.10. Schulhoff et al. HackAPrompt

- **Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities of LLMs through a Global Scale Prompt Hacking Competition** — Schulhoff et al. (EMNLP 2023).
  - **Source:** https://arxiv.org/abs/2311.16119
  - **Code:** <https://github.com/PromptLabs/hackaprompt>
  - **Mechanism:** Global-scale prompt-hacking competition eliciting 600K+ adversarial prompts against three state-of-the-art LLMs [claim_training_and_evaluation_schulhoff2023hackaprompt_a1_headline]; proposes a systematic ontology of attack categories [claim_training_and_evaluation_schulhoff2023hackaprompt_a2_methodology].
  - **Result:** Releases the HackAPrompt dataset and the first systematic ontology of prompt-injection techniques used by downstream training-data work [claim_training_and_evaluation_schulhoff2023hackaprompt_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: attack-content; existence documented, examples not excerpted.

## C1.11. Abdelnabi et al. LLMail-Inject

- **LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge** — Abdelnabi et al. (IEEE SaTML 2025; arXiv preprint).
  - **Source:** https://arxiv.org/abs/2506.09956
  - **Code:** <https://github.com/microsoft/llmail-inject-challenge>
  - **Mechanism:** Microsoft adaptive-PI challenge collecting ~208K adaptive attacks against email-LLM-agent variants from both attacker and defender perspectives [claim_training_and_evaluation_abdelnabi2025llmailinject_a1_headline]; releases adaptive-attack corpus paired with defender configurations [claim_training_and_evaluation_abdelnabi2025llmailinject_a2_methodology].
  - **Result:** Provides one of the largest adaptive-attack corpora in 2025 for PI detector benchmarking; IEEE SaTML 2025 challenge [claim_training_and_evaluation_abdelnabi2025llmailinject_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. ETHICS: attack-content; adaptive-attack corpus, existence documented.

## C1.12. Zou et al. GCG / AdvBench

- **Universal and Transferable Adversarial Attacks on Aligned Language Models** — Zou et al. (arXiv 2023).
  - **Source:** https://arxiv.org/abs/2307.15043
  - **Code:** <https://github.com/llm-attacks/llm-attacks>
  - **Mechanism:** Introduces the Greedy Coordinate Gradient (GCG) attack that optimizes adversarial suffixes transferring across aligned LLMs to bypass refusal [claim_training_and_evaluation_zou2023universal_a1_headline]; demonstrates transferable adversarial-suffix attack methodology [claim_training_and_evaluation_zou2023universal_a2_methodology].
  - **Result:** Releases AdvBench (the walledai/AdvBench HF mirror lists 500 harmful behaviors as of 2026-05-22; the original Zou et al. paper body discusses 520 (unverified body claim)); foundational attack benchmark used by HarmBench, JBB-Behaviors, and downstream detector evaluations [claim_training_and_evaluation_zou2023universal_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: attack-content + adversarial-suffix; documented as attack benchmark not training-positive corpus.

## C1.13. Mazeika et al. HarmBench

- **HarmBench: A Standardized Evaluation Framework for Automated Red Teaming and Robust Refusal** — Mazeika et al. (ICML 2024).
  - **Source:** https://arxiv.org/abs/2402.04249
  - **Code:** <https://github.com/centerforaisafety/HarmBench>
  - **Mechanism:** Standardized evaluation framework for automated red-teaming + robust refusal [claim_training_and_evaluation_mazeika2024harmbench_a1_headline]; large-scale comparison of 18 red-teaming methods and 33 target LLMs and defenses; 400 behaviors × 7 categories specifics (unverified body claim, not in abstract) [claim_training_and_evaluation_mazeika2024harmbench_a2_methodology].
  - **Result:** ICML 2024; canonical benchmark for adversarial robustness + jailbreak attack benchmarking [claim_training_and_evaluation_mazeika2024harmbench_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: attack-content benchmark; existence documented, examples not excerpted.

## C1.14. Chao et al. JailbreakBench

- **JailbreakBench: An Open Robustness Benchmark for Jailbreaking Large Language Models** — Chao et al. (NeurIPS 2024 D&B).
  - **Source:** https://arxiv.org/abs/2404.01318
  - **Code:** <https://github.com/JailbreakBench/jailbreakbench>
  - **Mechanism:** Argues current jailbreak evaluation lacks standardized comparison and addresses it with a reproducible benchmark [claim_training_and_evaluation_chao2024jailbreakbench_a1_headline]; JBB-Behaviors benchmark with 100 misuse behaviors and an evolving repository plus open leaderboard tracking attacks/defenses across multiple LLMs [claim_training_and_evaluation_chao2024jailbreakbench_a2_methodology].
  - **Result:** NeurIPS 2024 D&B; provides reproducible jailbreak evaluation harness with a versioned behavior set [claim_training_and_evaluation_chao2024jailbreakbench_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: attack-content; existence documented.

## C1.15. Jiang et al. WildJailbreak / WildTeaming

- **WildTeaming at Scale: From In-the-Wild Jailbreaks to (Adversarially) Safer Language Models** — Jiang et al. (NeurIPS 2024).
  - **Source:** https://arxiv.org/abs/2406.18510
  - **Code:** —
  - **Mechanism:** WildTeaming is an automatic LLM safety red-teaming framework that mines in-the-wild user-chatbot interactions to discover ~5.7K unique clusters of novel jailbreak tactics [claim_training_and_evaluation_jiang2024wildjailbreak_a1_headline]; synthesizes diverse in-the-wild jailbreak training prompts from LMSYS-Chat to produce WildJailbreak (262K vanilla + adversarial prompt-response pairs) [claim_training_and_evaluation_jiang2024wildjailbreak_a2_methodology].
  - **Result:** Releases AllenAI WildJailbreak (large attack-content dataset); per ADR-041 ETHICS §1, this dossier documents existence + license but does NOT excerpt attack examples [claim_training_and_evaluation_jiang2024wildjailbreak_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. **License red flag (Phase 2 report):** WildJailbreak ETHICS — attack-content dataset requiring careful downstream use; existence documented per ADR-041.

## C1.16. Han et al. WildGuard

- **WildGuard: Open One-Stop Moderation Tools for Safety Risks, Jailbreaks, and Refusals of LLMs** — Han et al. (NeurIPS 2024).
  - **Source:** https://arxiv.org/abs/2406.18495
  - **Code:** <https://github.com/allenai/wildguard>
  - **Mechanism:** Open lightweight moderation tool identifying malicious intent in user prompts, detecting safety risks of model responses, and refusal classification [claim_training_and_evaluation_han2024wildguard_a1_headline]; trains WildGuard moderation model on WildGuardMix (~92K combined prompts + responses) [claim_training_and_evaluation_han2024wildguard_a2_methodology].
  - **Result:** Open one-stop moderation model; NeurIPS 2024; reused as a PI/jailbreak baseline detector [claim_training_and_evaluation_han2024wildguard_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: paired with WildJailbreak attack corpus.

## C1.17. Li et al. SALAD-Bench

- **SALAD-Bench: A Hierarchical and Comprehensive Safety Benchmark for Large Language Models** — Li et al. (ACL 2024 Findings).
  - **Source:** https://arxiv.org/abs/2402.05044
  - **Code:** <https://github.com/OpenSafetyLab/SALAD-BENCH>
  - **Mechanism:** Safety benchmark specifically targeting LLM safety risk landscape [claim_training_and_evaluation_li2024saladbench_a1_headline]; hierarchical taxonomy (6 domains × 16 tasks × 65 categories) with ~30K test items [claim_training_and_evaluation_li2024saladbench_a2_methodology].
  - **Result:** Releases OpenSafetyLab/Salad-Data; ACL 2024 Findings; provides hierarchical safety evaluation [claim_training_and_evaluation_li2024saladbench_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: contains attack content; existence documented.

## C1.18. Luo et al. JailBreakV-28K

- **JailBreakV-28K: A Benchmark for Assessing the Robustness of MultiModal Large Language Models against Jailbreak Attacks** — Luo et al. (COLM 2024).
  - **Source:** https://arxiv.org/abs/2404.03027
  - **Code:** <https://github.com/EddyLuo1232/JailBreakV_28K>
  - **Mechanism:** Securing multimodal LLMs against malicious inputs while aligning with human values [claim_training_and_evaluation_luo2024jailbreakv28k_a1_headline]; 28K cross-modal jailbreak attempts targeting MLLMs (text + image attack vectors) [claim_training_and_evaluation_luo2024jailbreakv28k_a2_methodology].
  - **Result:** Releases the JailBreakV-28K dataset; COLM 2024; multimodal jailbreak corpus referenced as a multimodal attack benchmark [claim_training_and_evaluation_luo2024jailbreakv28k_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. ETHICS: multimodal attack content; out-of-scope as a detector training source but in-scope as an attack-benchmark reference.

## C1.19. microsoft/orca-agentinstruct-1M-v1

- **microsoft/orca-agentinstruct-1M-v1** — Microsoft Orca Team (2024).
  - **Source:** https://huggingface.co/datasets/microsoft/orca-agentinstruct-1M-v1
  - **Code:** —
  - **Mechanism:** ~1M-row instruction-following synthetic dataset from Microsoft Orca team; cited in PI detector training as a benign-instruction source [claim_training_and_evaluation_microsoft2024orcaagentinstruct_a1_existence].
  - **Result:** Released by Microsoft Research; CC license per HuggingFace card; used as benign-instruction balance in mixed PI training corpora [claim_training_and_evaluation_microsoft2024orcaagentinstruct_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`.

19 entries.
