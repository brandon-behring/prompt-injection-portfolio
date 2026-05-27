# Detection / classifier corpora

`(text, label)` injection/jailbreak sets — most are drop-in or near-drop-in for a
ModernBERT-style encoder. **License watch:** `xTRam1` and both `jayavibhav` sets are
license-undisclosed; clear before publishing any trained artifact.

### B1. deepset/prompt-injections — deepset (2023)
- **Source:** https://huggingface.co/datasets/deepset/prompt-injections
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 0/1).
- **Size+License:** 662 rows (546 train / 116 test); apache-2.0.
- **Tasks:** Canonical small bilingual (DE+EN) injection set; label 1 = injection. Encoder-readiness: **drop-in** with a predefined split — ideal smoke-test, too small to train alone. Lineage: JasperLS/prompt-injections.
- **Status:** Verified.

### B2. jackhhao/jailbreak-classification — jackhhao (2023)
- **Source:** https://huggingface.co/datasets/jackhhao/jailbreak-classification
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `type` (string {jailbreak, benign}).
- **Size+License:** 1,306 rows (1,040 / 262); apache-2.0.
- **Tasks:** Roughly-balanced jailbreak vs benign. Encoder-readiness: **drop-in after a trivial rename/label-map** (prompt→text, {benign:0, jailbreak:1}). Confirmed component of the ProtectAI deberta-v3-v2 training mixture (B8).
- **Status:** Verified.

### B3. xTRam1/safe-guard-prompt-injection — xTRam1 (2024)
- **Source:** https://huggingface.co/datasets/xTRam1/safe-guard-prompt-injection
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 0=safe / 1=injection).
- **Size+License:** 10,296 rows (8,240 / 2,056), ~70/30; **license: unknown**.
- **Tasks:** Good mid-size binary training set. Encoder-readiness: **drop-in** `(text,label)` with split. ⚠️ **Flagged mismatched**: license undisclosed AND the card cites arXiv:2402.13064, which is the unrelated "Generalized Instruction Tuning (GLAN)" paper — do not propagate that citation; verify provenance first.
- **Status:** Mismatched (citation/license).

### B4. reshabhs/SPML_Chatbot_Prompt_Injection — reshabhs (2024)
- **Source:** https://huggingface.co/datasets/reshabhs/SPML_Chatbot_Prompt_Injection
- **Access:** hf datasets; auth_required: N
- **Schema:** `System Prompt`, `User Prompt`, `Prompt injection` (0/1), `Degree`, `Source`.
- **Size+License:** 16,012 rows (single train split, no test); MIT.
- **Tasks:** Captures **system-vs-user** attack structure + injection severity (`Degree`). Encoder-readiness: **needs format work** — select/concatenate System+User as text, map `Prompt injection`→label, supply your own split. Assoc. arXiv:2402.11755.
- **Status:** Verified.

### B5. jayavibhav/prompt-injection — jayavibhav (2024)
- **Source:** https://huggingface.co/datasets/jayavibhav/prompt-injection
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 0/1).
- **Size+License:** 327,154 rows (262k / 65.4k); **license: unknown**.
- **Tasks:** Largest binary set surveyed; strong **primary training-corpus candidate**. Encoder-readiness: **drop-in** with split. ⚠️ License undisclosed; provenance undocumented (empty card, likely synthetic/aggregated) — clear licensing before publishing a trained model.
- **Status:** Verified (license unknown).

### B6. jayavibhav/prompt-injection-safety — jayavibhav (2024)
- **Source:** https://huggingface.co/datasets/jayavibhav/prompt-injection-safety
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (int64 multiclass {0,1,2}).
- **Size+License:** 60,000 rows (50k / 10k); **license: unknown**.
- **Tasks:** 3-class safety variant (classes not explicitly named on card — appears benign / injection / third). Encoder-readiness: **drop-in** with split, but confirm the 3-class meaning (collapse to binary for an injection head). ⚠️ License undisclosed.
- **Status:** Verified (license unknown).

### B7. GenTel-Bench (gentelbench-v1) — GenTelLab (2024)
- **Source:** https://huggingface.co/datasets/GenTelLab/gentelbench-v1
- **Access:** hf datasets; auth_required: N
- **Schema:** `id`, `text`, `label` (0/1), `domain`, `subdomain` (6-domain harm taxonomy).
- **Size+License:** 177,015 HF rows (vs paper's 84,812 attacks — likely bundles benign; confirm balance); apache-2.0.
- **Tasks:** From GenTel-Safe (arXiv:2409.19521); paper frames 3 attack categories (jailbreak / goal-hijacking / prompt-leaking) over 28 scenarios. Encoder-readiness: **drop-in** for binary; domain/subdomain enable multiclass. README empty — confirm benign/attack balance before quoting.
- **Status:** Verified (size caveat).

### B8. ProtectAI deberta-v3-base-prompt-injection-v2 (training mixture) — ProtectAI (2024)
- **Source:** https://huggingface.co/ProtectAI/deberta-v3-base-prompt-injection-v2
- **Access:** hf datasets; auth_required: N
- **Schema:** `text`, `label` (0=benign / 1=injection) — the model consumes this; the *data* is a mixture, not one set.
- **Size+License:** assembled mixture (per-source counts unpublished); apache-2.0.
- **Tasks:** Model card for the dossier's **SOTA reference detector (ProtectAI-v2)**. A **recipe**, not a unit: "assembled from various public open datasets" — components include jackhhao (B2), OpenSafetyLab/Salad-Data, natolambert/xstest-v2-copy, Harelix/Prompt-Injection-Mixed-Techniques-2024, VMware/open-instruct, alespalla/chatbot_instruction_prompts, HuggingFaceH4/grok-conversation-harmless. Encoder-readiness: **reproduce by concatenating** the listed sources.
- **Status:** Verified.

_8 entries._
