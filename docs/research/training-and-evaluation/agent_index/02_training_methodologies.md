# C2. Training methodologies

_8 primary-source entries covering training recipes used by prompt-injection detectors and the architectural-training paradigm that prevents PI at the LLM layer rather than the detector layer. Encoder baseline recipes (AdamW LR 2e-5 to 5e-5, batch 8-32, 3 epochs, cross-entropy) are well-documented in dataset cards but are referenced rather than catalogued as separate entries here — this file focuses on the load-bearing methodology papers. Cross-cuts to C3 (evaluation metrics) and C5 (OOD methodology) are surfaced via lookup recipes in the README._

## C2.1. Liu et al. Energy-based OOD detection

- **Energy-based Out-of-distribution Detection** — Liu et al. (NeurIPS 2020).
  - **Source:** https://arxiv.org/abs/2010.03759
  - **Code:** —
  - **Mechanism:** Determining whether inputs are out-of-distribution (OOD) is an essential building block for safely deploying ML models; previous methods relying on the softmax confidence are critiqued [claim_training_and_evaluation_liu2020energyood_a1_headline]; energy-based loss derives free energy from softmax logits and fine-tunes to push in-distribution samples to low energy and OOD to high energy [claim_training_and_evaluation_liu2020energyood_a2_methodology].
  - **Result:** NeurIPS 2020 method; later adopted by Meta Prompt Guard 2 (§ C2.5) and CodeIntegrity PromptGuard recipes; foundational PI detector training building block [claim_training_and_evaluation_liu2020energyood_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: historical`. (no widely-known repo for this paper specifically; method is reimplemented in downstream detector codebases)

## C2.2. Hu et al. LoRA

- **LoRA: Low-Rank Adaptation of Large Language Models** — Hu et al. (ICLR 2022).
  - **Source:** https://arxiv.org/abs/2106.09685
  - **Code:** <https://github.com/microsoft/LoRA>
  - **Mechanism:** Pre-training-then-adaptation paradigm with full fine-tuning becomes increasingly expensive as models scale [claim_training_and_evaluation_hu2021lora_a1_headline]; freezes pre-trained weights and injects trainable rank-decomposition matrices into transformer layers, reducing trainable parameters by ~10000× [claim_training_and_evaluation_hu2021lora_a2_methodology].
  - **Result:** ICLR 2022; basis of HuggingFace PEFT library; adopted by PromptShield (§ C3.1), Sentinel-v2 (§ C2.8), and most PI detector LLM fine-tunes [claim_training_and_evaluation_hu2021lora_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: historical`.

## C2.3. Liu et al. DoRA

- **DoRA: Weight-Decomposed Low-Rank Adaptation** — Liu et al. (ICML 2024 Oral).
  - **Source:** https://arxiv.org/abs/2402.09353
  - **Code:** <https://github.com/NVlabs/DoRA>
  - **Mechanism:** LoRA and variants have gained popularity for avoiding additional inference costs, but an accuracy gap to full fine-tuning often remains [claim_training_and_evaluation_liu2024dora_a1_headline]; DoRA decomposes pre-trained weight into magnitude + direction components, achieving LoRA-rate convergence with full-FT-like capacity [claim_training_and_evaluation_liu2024dora_a2_methodology].
  - **Result:** ICML 2024 Oral; one component of hlyn's aggressive PEFT stack for `prompt-injection-judge-deberta-70m` (DoRA + SupCon + FreeLB + R-Drop + SWA + Mixout + EDL) [claim_training_and_evaluation_liu2024dora_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`.

## C2.4. Sensoy et al. Evidential Deep Learning

- **Evidential Deep Learning to Quantify Classification Uncertainty** — Sensoy, Kaplan, Kandemir (NeurIPS 2018).
  - **Source:** https://arxiv.org/abs/1806.01768
  - **Code:** —
  - **Mechanism:** Deterministic neural nets learn effective predictors but the standard prediction-error minimization yields point predictions without uncertainty [claim_training_and_evaluation_sensoy2018evidential_a1_headline]; treats softmax outputs as Dirichlet evidence and outputs predictive uncertainty alongside class probabilities [claim_training_and_evaluation_sensoy2018evidential_a2_methodology].
  - **Result:** NeurIPS 2018; reused by hlyn (`hlyn/prompt-injection-judge-deberta-*`) for PI judges with explicit uncertainty quantification [claim_training_and_evaluation_sensoy2018evidential_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: historical`. (no widely-known repo for this paper specifically; method is reimplemented in downstream codebases)

## C2.5. Meta Llama Prompt Guard 2 86M

- **Llama Prompt Guard 2 86M** — Meta Llama (2025).
  - **Source:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
  - **Code:** —
  - **Mechanism:** Meta's 2025 prompt-injection detector model card; successor to Prompt-Guard-86M; multilingual support [claim_training_and_evaluation_meta2025promptguard2_a1_existence].
  - **Result:** Official Meta model card on HuggingFace; documents energy-based loss (from § C2.1) + APR (Attack Prevention Rate) evaluation metric on private red-team data; training-data composition not fully disclosed [claim_training_and_evaluation_meta2025promptguard2_a2_provenance].
  - **Status:** Verified (HF model card, 2026-05-22). `freshness_tier: volatile`. **License red flag (Phase 2 report):** training-data composition undisclosed — limits independent reproducibility + LODO replay. APR metric is Meta's signature; see glossary.

## C2.6. Liu et al. DataSentinel

- **DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks** — Liu et al. (IEEE S&P 2025 Distinguished Paper).
  - **Source:** https://arxiv.org/abs/2504.11358
  - **Code:** —
  - **Mechanism:** LLM-integrated applications and agents are vulnerable to prompt injection attacks; a detection method aims to defend against them [claim_training_and_evaluation_liu2025datasentinel_a1_headline]; game-theoretic min-max fine-tuning where detector and attacker are jointly trained [claim_training_and_evaluation_liu2025datasentinel_a2_methodology].
  - **Result:** IEEE S&P 2025 Distinguished Paper; provides attack-aware detector training methodology; later shown to be bypassable by DataFlip (Choudhary 2025, see § C4.5) [claim_training_and_evaluation_liu2025datasentinel_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (no widely-known repo)

## C2.7. Wallace et al. Instruction Hierarchy (OpenAI)

- **The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions** — Wallace et al. (arXiv 2024).
  - **Source:** https://arxiv.org/abs/2404.13208
  - **Code:** —
  - **Mechanism:** LLMs are susceptible to prompt injections, jailbreaks, and attacks that overwrite the model's original instructions with adversary-controlled prompts [claim_training_and_evaluation_wallace2024instructionhierarchy_a1_headline]; synthesizes training data where system / developer / user / tool messages have ranked privilege, then trains the LLM to honor higher-privilege instructions [claim_training_and_evaluation_wallace2024instructionhierarchy_a2_methodology].
  - **Result:** OpenAI training recipe; reduces prompt-injection vulnerability via 'context-synthesis' training rather than post-hoc detection; cross-references the architectural-training paradigm covered in `../direct-vs-indirect/` [claim_training_and_evaluation_wallace2024instructionhierarchy_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. (no widely-known repo; OpenAI training recipe, internal)

## C2.8. Ivry & Nahum Sentinel

- **Sentinel: SOTA model to protect against prompt injections** — Ivry & Nahum (2025).
  - **Source:** https://arxiv.org/abs/2506.05446
  - **Code:** —
  - **Mechanism:** LLMs are increasingly powerful but remain vulnerable to prompt injection attacks where malicious inputs cause deviation from intended instructions [claim_training_and_evaluation_ivry2025sentinel_a1_headline]; Qwen3-0.6B-based PI detector with departure from encoder backbones, using LoRA + reflection-style training [claim_training_and_evaluation_ivry2025sentinel_a2_methodology].
  - **Result:** Qualifire / Rogue Security SOTA claim against ProtectAI-only comparison; raises selection-bias concerns flagged in C4 critiques and in C5 reproducibility analysis [claim_training_and_evaluation_ivry2025sentinel_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (uncertain venue — arXiv preprint, no peer-reviewed venue at retrieval time). **Selection-bias flag:** self-comparison vs ProtectAI-only.

8 entries.
