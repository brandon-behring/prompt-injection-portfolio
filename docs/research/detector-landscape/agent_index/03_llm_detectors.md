# A3. LLM-based detectors (decoder + LLM-as-judge)

Detectors that use a decoder LLM (small-LM judge, multi-agent debate, or full 8B-class judge) rather than an encoder classifier. The latency cost is materially higher (typically 200ms-800ms vs. 5-100ms for encoder classifiers per § A2.4 and the postmortem latency table at § A5.16), but expressive power scales accordingly. PromptShield (§ A3.1) is the most-cited research-grade detector in this family; the Meta Llama Prompt Guard line (§ A3.3 - § A3.5) and Llama Guard (§ A3.6) provide the canonical vendor-side stack. PromptArmor (§ A3.7) is the canonical "off-the-shelf LLM-as-judge" baseline.

## A3.1. PromptShield (Berkeley)

- **PromptShield: Deployable Detection for Prompt Injection Attacks** — Jacob et al. (ACM CODASPY 2025).
  - **Source:** https://arxiv.org/abs/2501.15145
  - **Code:** —
  - **Mechanism:** Curated benchmark of conversational and application-structured prompt-injection inputs + a Llama-3.1-8B detector fine-tuned on insights from the curation process [claim_detector_landscape_0010_01]. The paper introduces the TPR@FPR (True Positive Rate at fixed False Positive Rate) reporting convention as the lens for surfacing the low-FPR collapse pattern that uniform accuracy hides [claim_detector_landscape_0010_02].
  - **Result:** Abstract claims the fine-tuned detector achieves significantly higher performance in the low false positive rate regime compared to prior schemes; positioned as a deployable benchmark for the broader community.
  - **Status:** Verified. (no widely-known repo) Source of the "encoder classifiers collapse at low FPR" pattern that informs the synthesis evidence in § A5.16 and the head-to-head methodology critique throughout the dossier. [ev_detector_landscape_0011]

## A3.2. CourtGuard (Wu & Maslowski)

- **CourtGuard: A Local, Multiagent Prompt Injection Classifier** — Wu & Maslowski (arXiv 2025).
  - **Source:** https://arxiv.org/abs/2510.19844
  - **Code:** https://github.com/isaacwu2000/CourtGuard
  - **Mechanism:** Multi-agent debate architecture: a "defense attorney" LLM argues the input is benign, a "prosecution attorney" LLM argues it's an injection, and a "judge" LLM produces the final classification [claim_detector_landscape_0011_01]. Implementations span Gemma-3-12b-it, Llama-3.3-8B, and Phi-4-mini-instruct (per abstract and code repo).
  - **Result:** Abstract reports lower false positive rate than the "Direct Detector" (a single-LLM-as-judge baseline) [claim_detector_landscape_0011_02], but acknowledges CourtGuard is generally a worse prompt-injection detector than the Direct Detector overall — the contribution is the lower FPR rather than higher TPR.
  - **Status:** Verified. arXiv preprint; first systematic evidence that multi-agent debate trades raw detection for adversarial robustness on benign-input scenarios. [ev_detector_landscape_0012]

## A3.3. Llama Prompt Guard 2 86M (Meta)

- **meta-llama/Llama-Prompt-Guard-2-86M (mDeBERTa-base 86M multilingual prompt-injection + jailbreak classifier)** — Meta Llama Team (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
  - **Code:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
  - **Mechanism:** mDeBERTa-base 86M-parameter classifier; positioned by Meta as the multilingual prompt-injection + jailbreak detection layer for Llama-deployment safety stacks. Card surface anchors Transformers-loading instructions [claim_detector_landscape_0012_01]; full mechanism / training-corpus description lives in the companion product doc (§ A4.10).
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. CodeIntegrity PromptGuard (§ A1.2) explicitly cites this model's energy-based loss function in its design.
  - **Status:** Verified. (model card surface; substantive product doc at § A4.10) [ev_detector_landscape_0013]

## A3.4. Llama Prompt Guard 2 22M (Meta)

- **meta-llama/Llama-Prompt-Guard-2-22M (DeBERTa-xsmall 22M, 75% latency reduction)** — Meta Llama Team (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-22M
  - **Code:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-22M
  - **Mechanism:** DeBERTa-xsmall 22M-parameter classifier; positioned by Meta as the latency-optimized variant of the Prompt Guard 2 line. Card surface anchors Transformers-loading instructions [claim_detector_landscape_0013_01].
  - **Result:** Model-card surface — quantitative latency claim ("75% latency reduction" per bib_ledger title field, retrieved 2026-05-22) is `(unverified body claim)` since not in abstract-equivalent area; treat as Meta-reported headline relative to the 86M sibling.
  - **Status:** Verified. (model card surface; vendor-reported latency) Tier choice when latency budget < 22M params allows. [ev_detector_landscape_0014]

## A3.5. Prompt Guard 86M (Meta — original)

- **meta-llama/Prompt-Guard-86M (original mDeBERTa-base prompt-injection + jailbreak classifier)** — Meta Llama Team (Hugging Face model card, 2024).
  - **Source:** https://huggingface.co/meta-llama/Prompt-Guard-86M
  - **Code:** https://huggingface.co/meta-llama/Prompt-Guard-86M
  - **Mechanism:** The original (v1) Meta Prompt Guard mDeBERTa-base 86M classifier, predecessor to the Prompt Guard 2 line (§ A3.3 - § A3.4). Card surface anchors the Llama 3.1 Acceptable Use Policy and Transformers-loading instructions [claim_detector_landscape_0014_01]; full training-corpus details not in abstract-equivalent area.
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. Superseded by Prompt Guard 2 (§ A3.3, § A3.4); retained as the reference baseline for older deployments.
  - **Status:** Unverified. (model card surface; superseded by Prompt Guard 2) [ev_detector_landscape_0015]

## A3.6. Llama Guard 3 8B (Meta)

- **meta-llama/Llama-Guard-3-8B (Llama-3.1-8B content-safety classifier; 14 MLCommons hazard categories)** — Meta Llama Team (Hugging Face model card, 2024).
  - **Source:** https://huggingface.co/meta-llama/Llama-Guard-3-8B
  - **Code:** https://huggingface.co/meta-llama/Llama-Guard-3-8B
  - **Mechanism:** Llama-3.1-8B fine-tuned as a content-safety classifier; positioned by Meta to cover 14 MLCommons hazard categories rather than prompt-injection-specific detection. Card surface anchors Docker Model Runner / Transformers usage [claim_detector_landscape_0015_01]; positioned as an LLM-as-judge for safety-content moderation.
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract for this surface; multiple Llama Guard 3 evaluation papers exist (out of scope here — see `../training-and-evaluation/`).
  - **Status:** Verified. (model card surface; edge-of-scope — covers content-moderation hazards, not injection-specific detection, but listed because of practitioner overlap and frequent inclusion in detector benchmarks) [ev_detector_landscape_0016]

## A3.7. PromptArmor (Shi et al.)

- **PromptArmor: Simple yet Effective Prompt Injection Defenses** — Shi et al. (arXiv 2025).
  - **Source:** https://arxiv.org/abs/2507.15219
  - **Code:** —
  - **Mechanism:** Prompts an off-the-shelf LLM (no fine-tuning) to detect and remove potential injected prompts from agent inputs before the agent processes them — the canonical "LLM-as-judge baseline" pattern [claim_detector_landscape_0016_01]. Evaluated against adaptive attacks and across different judge-prompting strategies.
  - **Result:** Abstract reports both false positive rate and false negative rate below 1% on the AgentDojo benchmark using GPT-4o, GPT-4.1, or o4-mini as the judge LLM [claim_detector_landscape_0016_02]; attack success rate drops to below 1% after removing injected prompts. Authors recommend PromptArmor as a "standard baseline" for evaluating new defenses.
  - **Status:** Verified. (no widely-known repo) The canonical off-the-shelf LLM-as-judge benchmark configuration. Latency cost is the GPT-class judge inference time per input. [ev_detector_landscape_0017]
