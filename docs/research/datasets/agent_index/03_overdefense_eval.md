# Over-defense / held-out eval (NOT for the training split)

Benign-heavy or withheld sets used to measure **false positives / over-defense** and to
provide a contamination-free benchmark. Keep these out of any training split.

### C1. NotInject — Li & Liu / InjecGuard·PIGuard (2024)
- **Source:** https://huggingface.co/datasets/leolee99/NotInject
- **Access:** hf datasets; auth_required: N
- **Schema:** `prompt`, `word_list` (embedded injection-trigger words), `category` (topic, **not** an attack-type label).
- **Size+License:** 339 rows (3 subsets × 113, by trigger-word count); MIT.
- **Tasks:** **All-benign by construction** — measures over-defense / false-positive rate: score a detector by how few of these benign-but-triggery prompts it flags. Pairs with the [harness spec](../../planning/attack-type-lodo-harness-spec.md)'s benign-FPR metric. Multilingual. arXiv:2410.22770 (ACL 2025). Encoder-readiness: **eval-only**, never a training split.
- **Status:** Verified.

### C2. Prompt Injection Test (PINT) Benchmark — Lakera AI (2024)
- **Source:** https://github.com/lakeraai/pint-benchmark
- **Access:** credentialed (request from Lakera); auth_required: Y
- **Schema:** `text`, `label`, `category` (YAML schema the harness expects; the **real data is withheld** — repo ships only the scorer + an example yaml).
- **Size+License:** ~4,314 inputs (3,016 EN / 1,298 non-EN); MIT (harness) **+ data not publicly distributed** (anti-contamination).
- **Tasks:** Neutral held-out injection/jailbreak benchmark. Verbatim: *"The PINT Benchmark dataset is not publicly available in order to prevent the dilution of the PINT Benchmark from overfitting due to training on the inputs."* Categories: public/internal injection, jailbreak, hard_negatives, chat, documents (mostly benign by design). Encoder-readiness: **not for training**; eval-only and not freely downloadable.
- **Status:** Unverified (data deliberately withheld; harness verified).

_2 entries._
