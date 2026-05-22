# A2. DeBERTa-based encoder detectors

Open-source prompt-injection encoder classifiers built on DeBERTa-v3 (Microsoft, 2021) and related smaller variants. The DeBERTa-v3 generation has been the practitioner default since 2023; ProtectAI's v1 / v2 / small lineage and deepset's earlier 2023 release together account for the majority of downloads on Hugging Face's "prompt-injection-classifier" family. Smaller xsmall (70M) and INT8 ONNX quantized variants (§ A2.4) sit at the lower end of the latency tradeoff curve. See § A5.16 for the CodeIntegrity industry postmortem on why even mature DeBERTa-v3 detectors collapse against adaptive evasion, and § A3.1 (PromptShield) for the independent benchmark that surfaces the "low FPR collapse" pattern that uniform accuracy hides.

## A2.1. ProtectAI DeBERTa v3 Prompt Injection v1 (Protect AI)

- **protectai/deberta-v3-base-prompt-injection (DeBERTa-v3-base prompt-injection classifier, v1)** — Protect AI (Hugging Face model card, 2024).
  - **Source:** https://huggingface.co/protectai/deberta-v3-base-prompt-injection
  - **Code:** https://huggingface.co/protectai/deberta-v3-base-prompt-injection
  - **Mechanism:** DeBERTa-v3-base sequence classifier fine-tuned for prompt-injection detection; the v1 release is the deprecated predecessor to v2 (see § A2.2). Card surface anchors transformer-loading instructions but no curated training-corpus description [claim_detector_landscape_0005_01].
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. Superseded by v2 (§ A2.2) which Protect AI positions as the production-grade English-only release.
  - **Status:** Unverified. (model card surface; v1 retained for reproducibility, v2 is the current product) [ev_detector_landscape_0006]

## A2.2. ProtectAI DeBERTa v3 Prompt Injection v2 (Protect AI)

- **protectai/deberta-v3-base-prompt-injection-v2 (DeBERTa-v3-base 184M English-only prompt-injection classifier)** — Protect AI (Hugging Face model card, 2024).
  - **Source:** https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2
  - **Code:** https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2
  - **Mechanism:** DeBERTa-v3-base 184M-parameter sequence classifier; English-only as positioned by Protect AI. Card surface anchors transformer-loading instructions and class labels [claim_detector_landscape_0006_01]; specific training-corpus composition not in abstract-equivalent area.
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. Sentinel (§ A1.1) explicitly benchmarks against this model and reports outperforming it on public benchmarks (Sentinel-side claim, treat per § A1.1 Status note).
  - **Status:** Verified. (model card surface; benchmarked by Sentinel and PromptShield families) [ev_detector_landscape_0007]

## A2.3. deepset DeBERTa v3 Injection (deepset)

- **deepset/deberta-v3-base-injection (DeBERTa-v3-base prompt-injection classifier)** — deepset (Hugging Face model card, 2023).
  - **Source:** https://huggingface.co/deepset/deberta-v3-base-injection
  - **Code:** https://huggingface.co/deepset/deberta-v3-base-injection
  - **Mechanism:** DeBERTa-v3-base sequence classifier for prompt-injection detection; one of the earliest widely-used open-source detectors (2023). Card surface anchors transformer-loading instructions and class labels [claim_detector_landscape_0007_01]; deepset operationally maintains this as a community-grade rather than production-grade artifact.
  - **Result:** Model-card surface — no quantitative claim is anchored in the abstract. Frequently cited as a baseline in independent benchmark comparisons (PINT-leaderboard included, § A4.2).
  - **Status:** Verified. (model card surface; widely cited baseline) [ev_detector_landscape_0008]

## A2.4. hlyn-labs Prompt Injection Judge DeBERTa 70M (Hlyn Labs)

- **hlyn-labs/prompt-injection-judge-deberta-70m (DeBERTa-v3-xsmall 70M, INT8 ONNX, ~101ms M1 CPU)** — Hlyn Labs (Hugging Face model card, 2025).
  - **Source:** https://huggingface.co/hlyn-labs/prompt-injection-judge-deberta-70m
  - **Code:** https://huggingface.co/hlyn-labs/prompt-injection-judge-deberta-70m
  - **Mechanism:** DeBERTa-v3-xsmall 70M-parameter prompt-injection classifier, INT8 ONNX quantized for CPU inference; the smallest viable detector in the DeBERTa family. Card positions it as a "Prompt Injection Detector: DeBERTa Frontend" within a broader Qualifire-framework evaluation harness [claim_detector_landscape_0008_01].
  - **Result:** Model-card surface — quantitative latency claim ("~101ms M1 CPU" per bib_ledger title field, retrieved 2026-05-22) is `(unverified body claim)` since not in abstract-equivalent area; treat the latency as a vendor-reported headline.
  - **Status:** Verified. (model card surface; vendor-reported latency) Tier choice for sub-200ms CPU guardrails. [ev_detector_landscape_0009]

## A2.5. DMPI-PMHFE (Ji, Li & Mao)

- **Detection Method for Prompt Injection by Integrating Pre-trained Model and Heuristic Feature Engineering** — Ji, Li & Mao (KSEM 2025 AI & Security Workshop).
  - **Source:** https://arxiv.org/abs/2506.06384
  - **Code:** —
  - **Mechanism:** DMPI-PMHFE dual-channel architecture: DeBERTa-v3-base extracts semantic features in parallel with heuristic rules based on known attack patterns; the two feature channels are fused and passed through a fully-connected classifier head [claim_detector_landscape_0009_01]. Hybrid encoder + heuristic-feature pattern motivated by limitations of relying only on DeBERTa-extracted features [claim_detector_landscape_0009_02].
  - **Result:** Abstract claims DMPI-PMHFE outperforms existing methods on accuracy, recall, and F1-score across diverse benchmark datasets, and reduces attack success rates across GLM-4, LLaMA 3, Qwen 2.5, and GPT-4o when deployed in-line (specific deltas are `(unverified body claim)`).
  - **Status:** Verified. (no widely-known repo) Workshop venue; treat the magnitude of improvement claims with caution pending independent reproduction. [ev_detector_landscape_0010]
