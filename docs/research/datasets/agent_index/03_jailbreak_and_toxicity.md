# Jailbreak & toxicity-safety-guard families

Two adjacent unsafe-input axes co-housed because both are user-turn safety signals (not injection-into-context). **Jailbreak** = user-text attempts to bypass system/safety policy. **Toxicity-safety-guard** = real-traffic / general-harm moderation corpora (often labeled with multiple harm axes; useful as co-training material for guardrail detectors). License watch: ToxicChat (CC-BY-NC-4.0; research-only) and WildGuardMix (ODC-BY, **gated**).

### C1. allenai/wildguardmix — Han et al. (NeurIPS 2024 D&B)
- **Source:** https://huggingface.co/datasets/allenai/wildguardmix
- **Access:** hf datasets; auth_required: Y
- **Schema:** `prompt`, `adversarial` (bool), `response`, `prompt_harm_label`, `response_harm_label`, `response_refusal_label`, `subcategory` (+ `*_agreement` in test).
- **Size+License:** `wildguardtrain` ~86,759 (48,783 prompt-only + 37,976 prompt-response); `wildguardtest` ~1,725; ~56 MB; odc-by.
- **Tasks:** Three label axes — `prompt_harm_label` (harmful/unharmful), `response_harm_label`, `response_refusal_label` (refusal/compliance) — plus an `adversarial` bool (jailbreak-style vs vanilla) + fine `subcategory`. Configs: `wildguardtrain` (~86,759 = 48,783 prompt-only + 37,976 pairs; synthetic + in-the-wild + adversarial) and `wildguardtest` (~1,725, w/ inter-annotator agreement); single train split. arXiv:2406.18495. Encoder-readiness: **derivable** — pick an axis (e.g. `prompt_harm_label` on `prompt`), supply own split. ⚠️ **Gated** — login + accept AI2 Responsible Use to download. The `adversarial` flag is a useful shortcut-vs-adversarial signal for our EDA.
- **Status:** Verified.
- **Soft tags:** family=toxicity-safety-guard · encoder_readiness=derivable · study_relevance=high

### C2. jackhhao/jailbreak-classification — jackhhao (2023)
- **Source:** https://huggingface.co/datasets/jackhhao/jailbreak-classification
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `type` (string {jailbreak, benign}).
- **Size+License:** 1,306 rows (train 1,040 / test 262), ~1.3k rows; apache-2.0.
- **Tasks:** Roughly-balanced jailbreak vs benign. Encoder-readiness: **drop-in after a trivial rename/label-map** (prompt→text, {benign:0, jailbreak:1}); has train/test split. Confirmed component of the ProtectAI deberta-v3-v2 training mixture (F3).
- **Status:** Verified.
- **Soft tags:** family=jailbreak · encoder_readiness=drop-in · study_relevance=high

### C3. lmsys/toxic-chat — Lin et al. (EMNLP 2023 Findings)
- **Source:** https://huggingface.co/datasets/lmsys/toxic-chat
- **Access:** hf datasets; auth_required: N
- **Schema:** `conv_id`, `user_input`, `model_output`, `human_annotation` (bool), `toxicity` (0/1), `jailbreaking` (0/1), `openai_moderation`.
- **Size+License:** toxicchat0124: 10,165 (train 5,080 / test 5,085); ~60.9 MB across both versions; cc-by-nc-4.0.
- **Tasks:** Real Vicuna-demo user-AI traffic (anonymized). Carries TWO independent binary int64 labels: `toxicity` (0/1) AND `jailbreaking` (0/1) — the latter directly relevant — plus `openai_moderation` raw output and a `human_annotation` bool. Config `toxicchat0124` (older `toxicchat1123` also present); predefined train(5,080) / test(5,085); heavily imbalanced toward non-toxic/non-jailbreak (real low base rate). arXiv:2310.17389. Encoder-readiness: **drop-in** `(text,label)` via `user_input` + toxicity|jailbreaking; predefined split. ⚠️ NC license ⇒ non-commercial research only.
- **Status:** Verified.
- **Soft tags:** family=toxicity-safety-guard · encoder_readiness=drop-in · study_relevance=high

### C4. TrustAIRLab/in-the-wild-jailbreak-prompts ("Do Anything Now") — Shen et al. (ACM CCS 2024)
- **Source:** https://huggingface.co/datasets/TrustAIRLab/in-the-wild-jailbreak-prompts
- **Access:** hf datasets; auth_required: N
- **Schema:** `platform`, `source`, `prompt`, `jailbreak` (bool), `created_at`, `date`, `community_id`, `community_name`.
- **Size+License:** 21,527 rows across 4 dated configs (jailbreak_2023_05_07 666 / jailbreak_2023_12_25 1.41k / regular_2023_05_07 5.72k / regular_2023_12_25 13.7k), ~18.4 MB; mit.
- **Tasks:** Boolean `jailbreak` column is the binary target (jailbreak vs regular); `prompt` is the text; rich metadata (platform/source/date/community). Ships in 4 DATED configs loaded by name: two `jailbreak_*` + two `regular_*` snapshots (2023_05_07, 2023_12_25). Ships BOTH classes: ~1,405 jailbreak + ~13,735 regular/benign (15,140 deduped prompts collected Dec-2022..Dec-2023; 21,527 rows across configs) ⇒ a benign-vs-jailbreak binary IS constructable. arXiv:2308.03825. Encoder-readiness: **derivable** — concatenate the `jailbreak_*` + `regular_*` configs, map `jailbreak`→label. **Jailbreak** family (direct user-vs-system), not indirect/RAG. Canonical CCS'24 corpus.
- **Status:** Verified.
- **Soft tags:** family=jailbreak · encoder_readiness=derivable · study_relevance=medium

_4 entries._
