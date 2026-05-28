# Aggregated recipes / training-mixture corpora

Datasets that are themselves **aggregations** of multiple upstream sources — purpose-built guardrail training corpora and the training mixtures of SOTA reference detectors. Useful as starting points (or for reproducing a reported detector); requires verifying component composition because the leaves are often partially undisclosed.

### F1. GenTel-Bench (gentelbench-v1) — Li et al. (2024)
- **Source:** https://huggingface.co/datasets/GenTelLab/gentelbench-v1
- **Access:** hf datasets; auth_required: N
- **Schema:** `id`, `text`, `label` (0/1), `domain`, `subdomain` (6-domain harm taxonomy).
- **Size+License:** 177,015 rows (HF single split; **differs from paper headline 84,812 attacks** — likely bundles benign); ~tens of MB; apache-2.0.
- **Tasks:** From GenTel-Safe (arXiv:2409.19521); `label` int64 (0/1) with a harm taxonomy in domain/subdomain (6 domains; paper frames 3 attack categories: jailbreak / goal-hijacking / prompt-leaking over 28 scenarios). HF reports 177,015 rows, LARGER than the paper's 84,812 injection attacks ⇒ HF release likely bundles benign+attack; README empty, **confirm balance before quoting**. Encoder-readiness: **drop-in** `(text,label)` for binary; domain/subdomain enable multiclass. English. Project: gentellab.github.io/gentel-safe.github.io.
- **Status:** Verified (size caveat — HF count > paper count).
- **Soft tags:** family=aggregated-recipe · encoder_readiness=drop-in · study_relevance=high

### F2. InjecGuard / PIGuard training corpus — Li & Liu (ACL 2025)
- **Source:** https://github.com/SaFoLab-WISC/InjecGuard
- **Access:** direct; auth_required: N
- **Schema:** binary benign vs malicious-injection `(text, label)` (training).
- **Size+License:** training set aggregated from ~20 open-source datasets + LLM-augmented data; 144-sample val; training count not printed on README — count from `PIGuard/datasets` after clone; mit.
- **Tasks:** Purpose-built guardrail training corpus (arXiv:2410.22770) that **aggregates BIPIA (indirect) + Wildguard-Benign + PINT** among ~20 sources — so it carries some indirect content (unlike HackAPrompt/TensorTrust which are direct-only). Companion = NotInject (D2), the all-benign over-defense eval. Encoder-readiness: **drop-in** — purpose-built `(text,label)` guardrail corpus in `PIGuard/datasets`, MIT. Verify exact composition after clone.
- **Status:** Verified.
- **Soft tags:** family=aggregated-recipe · encoder_readiness=drop-in · study_relevance=high

### F3. ProtectAI deberta-v3-base-prompt-injection-v2 (training mixture) — ProtectAI.com (2024)
- **Source:** https://huggingface.co/ProtectAI/deberta-v3-base-prompt-injection-v2
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (0=benign / 1=injection) — the model consumes this; the *data* is a mixture, not one set.
- **Size+License:** assembled mixture; per-source counts not published; rows: unknown (recipe); apache-2.0.
- **Tasks:** **Model card** for the dossier's **SOTA reference detector** (ProtectAI-v2). **NOT one dataset** — a **recipe**: *"meticulously assembled from various public open datasets"* (8 MIT + 1 CC0 + 6 public-domain). Named components include jackhhao/jailbreak-classification (C2), OpenSafetyLab/Salad-Data, natolambert/xstest-v2-copy (D3), Harelix/Prompt-Injection-Mixed-Techniques-2024 (A7), VMware/open-instruct, alespalla/chatbot_instruction_prompts, HuggingFaceH4/grok-conversation-harmless. Encoder-readiness: **NOT encoder-ready as a unit** — reproduce by concatenating the listed sources (jackhhao is logged separately above). Listed as the pointer to the v2 training mixture the submission benchmarks against.
- **Status:** Verified.
- **Soft tags:** family=aggregated-recipe · encoder_readiness=pointer · study_relevance=high

_3 entries._
