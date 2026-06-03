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

### C5. nvidia/Aegis-AI-Content-Safety-Dataset-2.0 — NVIDIA (2025)
- **Source:** https://huggingface.co/datasets/nvidia/Aegis-AI-Content-Safety-Dataset-2.0
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt` + `prompt_label` (string {safe, unsafe}).
- **Size+License:** ~33.4K rows (binary safe/unsafe); CC-BY-4.0. (Corrected id 2026-06-03 — the handoff `nvidia/Aegis-2.0` 404s.)
- **Tasks:** Content-safety / toxicity moderation — `prompt_label` marks content harm (criminal / sexual / harassment categories), **NOT injection-presence**. EDA-gate verdict (2026-06-03): **off-axis for injection** (the label is a content-safety axis, not an attack-carrier axis); near-zero leakage (jackhhao 2). Research-role: **PARKED for injection** — catalogue as a toxicity / content-safety reference (an optional hard-negative source for guardrail co-training), not an injection set. Encoder-readiness: **derivable but off-axis** — a clean `(text, label)` via `prompt`+`prompt_label`{safe:0,unsafe:1}, but the target is content-safety not injection.
- **Status:** Verified.
- **Soft tags:** family=toxicity-safety-guard · encoder_readiness=derivable (off-axis) · study_relevance=parked

### C6. youbin2014/JailbreakDB — youbin2014 (2025)
- **Source:** https://huggingface.co/datasets/youbin2014/JailbreakDB
- **Access:** hf datasets; auth_required: N (HF Viewer 500s ⇒ pull files / raw-CSV adapter)
- **Schema:** `user_prompt` + `jailbreak` (0/1) + `source` (provenance); ships as 2 raw CSVs.
- **Size+License:** 1,539,874 records (445,752 + 1,094,122; the "12.2M" was a multi-line-quoted-field line-count artifact); CC-BY-4.0.
- **Tasks:** A 14-source aggregate of jailbreak / instruction-tuning corpora. EDA-gate verdict (2026-06-03): **PARK — not slate-eligible**, on two decisive findings. (1) **Severe contamination** — full 1.54M scan finds 19,458 exact overlaps with our universe: `shen_dan` 17,783 (almost all via its `DAN` source), `jackhhao` 1,387, `jbb` 288 (via JBB-Behaviors/AdvBench/HarmBench) ⇒ using it contaminates any split holding out shen_dan/jackhhao/jbb, plus a ~2.1% near-dup tail. (2) **Scrambled labels** — the classic `DAN` jailbreak sits in `text_regular` (jailbreak=0) while benign Safe-RLHF questions sit in `text_jailbreak` (jailbreak=1); provenance explains it (the set mixes instruction-tuning corpora — OpenHermes-2.5 494K, glaive-code 181K, metamath, alpaca, platypus — with jailbreak/harm sets, so `jailbreak` is not the intuitive label). Research-role: **PARKED** (contaminated + unreliable labels). Encoder-readiness: **derivable but parked**.
- **Status:** Verified (parked — contamination + scrambled labels).
- **Soft tags:** family=jailbreak · encoder_readiness=derivable but parked · study_relevance=parked

_6 entries._
