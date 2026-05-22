# A1. ModernBERT-based encoder detectors

Open-source prompt-injection encoder classifiers built on the ModernBERT base / large architecture (released Dec 2024). ModernBERT's 8K-token native context is the practical differentiator over the DeBERTa-v3 generation (typically 512-token context); ModernBERT-large at 395M parameters sits at the upper end of viable single-GPU inference for low-latency guardrails. See A2 for the DeBERTa-v3 family side-by-side, and § A5.16 for the CodeIntegrity industry postmortem on why even SOTA encoder classifiers underperform against adaptive attacks despite high held-out accuracy.

## A1.1. Sentinel (Qualifire)

- **Sentinel: SOTA model to protect against prompt injections** — Ivry & Nahum (arXiv 2025).
  - **Source:** https://arxiv.org/abs/2506.05446
  - **Code:** https://huggingface.co/qualifire/prompt-injection-sentinel
  - **Mechanism:** ModernBERT-large (395M) fine-tuned on a curated dataset amalgamating open-source and Qualifire-private prompt-injection corpora (role-playing, instruction hijacking, biased-content generation attacks alongside benign instructions) [claim_detector_landscape_0000_01].
  - **Result:** Reports 0.987 average accuracy and 0.980 F1-score on an unseen internal test set; abstract claims consistent outperformance of `protectai/deberta-v3-base-prompt-injection-v2` on public benchmarks (`unverified body claim` for the specific delta sizes).
  - **Status:** Verified. Self-reported numbers; treat the SOTA claim with the usual self-reported skepticism — see § A5.16 for the broader industry critique of held-out accuracy. [ev_detector_landscape_0001]

## A1.2. CodeIntegrity PromptGuard (Jung)

- **codeintegrity-ai/promptguard (ModernBERT-base 149M, 955K-example prompt-injection classifier)** — Jung (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/codeintegrity-ai/promptguard
  - **Code:** https://huggingface.co/codeintegrity-ai/promptguard
  - **Mechanism:** ModernBERT-base (149M) sequence-classifier fine-tuned on a curated 955K-example prompt-injection corpus; positioned by CodeIntegrity as a "high-performance prompt injection and jailbreak detector for LLM applications" [claim_detector_landscape_0001_01]. Adopts a modified energy-based loss function inspired by Meta's Llama Prompt Guard 2 design (model-card cross-reference).
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. Companion industry postmortem from the same author (§ A5.16) provides the methodological critique of how held-out accuracy understates adversarial vulnerability.
  - **Status:** Verified. (model card surface) Self-published HF card; companion postmortem at § A5.16 contextualizes the detector's design tradeoffs. [ev_detector_landscape_0002]

## A1.3. Vijil mBERT Prompt Injection (Vijil AI)

- **vijil/mbert-prompt-injection (ModernBERT-base prompt-injection classifier)** — Vijil AI (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/vijil/mbert-prompt-injection
  - **Code:** https://huggingface.co/vijil/mbert-prompt-injection
  - **Mechanism:** Fine-tuned ModernBERT (base) classifier trained to flag prompt-injection inputs designed to manipulate language models into unintended outputs [claim_detector_landscape_0002_01].
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. Card positions the model as a Vijil-curated, deployment-ready guardrail; vendor-side context for Vijil Dome lives at § A4 references.
  - **Status:** Verified. (model card surface) [ev_detector_landscape_0003]

## A1.4. tihilya ModernBERT Prompt Injection Detection (tihilya)

- **tihilya/modernbert-base-prompt-injection-detection** — tihilya (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/tihilya/modernbert-base-prompt-injection-detection
  - **Code:** https://huggingface.co/tihilya/modernbert-base-prompt-injection-detection
  - **Mechanism:** Community-maintained ModernBERT-base prompt-injection sequence classifier; HF card metadata declares `answerdotai/ModernBERT-base` as base model and `ModernBertForSequenceClassification` architecture [claim_detector_landscape_0003_01]. Card surface offers no curated dataset description or training-method documentation.
  - **Result:** Model-card surface — no quantitative claim in abstract; treat as stub-quality / unverified community contribution.
  - **Status:** Unverified. (community model card, stub-quality) [ev_detector_landscape_0004]

## A1.5. Pangolin Guard Large (Carpintero)

- **dcarpintero/pangolin-guard-large (ModernBERT-large 395M, lightweight self-hosted prompt-injection guardrail)** — Carpintero (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/dcarpintero/pangolin-guard-large
  - **Code:** https://huggingface.co/dcarpintero/pangolin-guard-large
  - **Mechanism:** ModernBERT-large (395M) classifier positioned for self-hosted prompt-injection guardrailing; HF card surfaces Transformers usage instructions but no curated dataset description in abstract-equivalent area [claim_detector_landscape_0004_01].
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. At the same parameter scale as Sentinel (§ A1.1), so latency profile is comparable; positioning is a lightweight alternative to vendor-hosted guardrails (§ A4.x).
  - **Status:** Verified. (model card surface; no widely-known evaluation paper) [ev_detector_landscape_0005]
