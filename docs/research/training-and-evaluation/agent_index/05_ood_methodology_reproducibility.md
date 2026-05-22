# C5. OOD generalization methodology + reproducibility crisis

_4 primary-source entries covering Leave-One-Dataset-Out (LODO) methodology and disclosure gaps in 'winning' PI detectors. This file is foundational to the portfolio's OOD-wall thesis: it documents the canonical OOD-collapse example (ProtectAI v2's high in-distribution F1 → 1.34% TPR @ 0.5% FPR / 0.00% TPR @ 0.1% FPR on PromptShield Table 4) and the methodology that surfaces such collapses (LODO held-out-dataset evaluation rather than held-out-row from the same mixture). The portfolio inherits LODO discipline from submission ADR-016 + ADR-075 (see Verification & limits in the README)._

## C5.1. Fomin et al. When Benchmarks Lie

- **When Benchmarks Lie: Evaluating Malicious Prompt Classifiers Under True Distribution Shift** — Fomin et al. (arXiv 2026).
  - **Source:** https://arxiv.org/abs/2602.14161
  - **Code:** —
  - **Mechanism:** Detecting PI + jailbreak attacks is critical for deploying LLM-based agents safely; as agents process untrusted data from emails, documents, tool outputs, and external APIs, classifier reliability under true distribution shift becomes load-bearing [claim_training_and_evaluation_fomin2026benchmarkslie_a1_headline]; introduces LODO (Leave-One-Dataset-Out) evaluation for malicious-prompt classifiers and shows TPR collapses under true distribution shift compared to held-out-row evaluation [claim_training_and_evaluation_fomin2026benchmarkslie_a2_methodology].
  - **Result:** Provides empirical evidence for the OOD-wall hypothesis; the methodology is directly mirrored by portfolio ADR-016 + ADR-075 LODO discipline [claim_training_and_evaluation_fomin2026benchmarkslie_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (no widely-known repo at retrieval)

## C5.2. rogue-security/prompt-injections-benchmark (Qualifire)

- **rogue-security/prompt-injections-benchmark (Qualifire Benchmark)** — Rogue Security / Qualifire (2025).
  - **Source:** https://huggingface.co/datasets/rogue-security/prompt-injections-benchmark
  - **Code:** —
  - **Mechanism:** HuggingFace benchmark dataset used by Qualifire Sentinel evaluations (also known as `qualifire/prompt-injections-benchmark`) [claim_training_and_evaluation_rogue2025promptinjectionsbenchmark_a1_existence].
  - **Result:** Released by Rogue Security / Qualifire; reproducibility concern flagged: Qualifire Sentinel comparisons rely on this benchmark plus an undisclosed private subset, raising selection-bias risk for self-reported numbers [claim_training_and_evaluation_rogue2025promptinjectionsbenchmark_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. **License red flag (Phase 2 report):** undisclosed private subset used in companion Sentinel evaluations (§ C2.8); independent reproducibility limited.

## C5.3. hendzh/PromptShield benchmark dataset

- **hendzh/PromptShield benchmark dataset** — Alzahrani / Berkeley PromptShield team (2025).
  - **Source:** https://huggingface.co/datasets/hendzh/PromptShield
  - **Code:** —
  - **Mechanism:** HuggingFace mirror of the Berkeley PromptShield benchmark dataset (conversational + application-structured tracks) [claim_training_and_evaluation_hendzh2025promptshielddataset_a1_existence].
  - **Result:** Maintained by hendzh (Berkeley PromptShield team); released alongside the Jacob et al. CODASPY 2025 paper (§ C3.1); the standard third-party OOD benchmark used by the field for cross-detector comparison [claim_training_and_evaluation_hendzh2025promptshielddataset_a2_provenance].
  - **Status:** Verified (HF dataset card, 2026-05-22). `freshness_tier: volatile`. (recheck after 2026-06-22)

## C5.4. protectai/deberta-v3-base-prompt-injection-v2

- **protectai/deberta-v3-base-prompt-injection-v2** — ProtectAI (2024).
  - **Source:** https://huggingface.co/protectai/deberta-v3-base-prompt-injection-v2
  - **Code:** —
  - **Mechanism:** ProtectAI's encoder-based PI detector model card; widely-used baseline (DeBERTa-v3-base backbone) [claim_training_and_evaluation_protectai2024deberta_a1_existence].
  - **Result:** ProtectAI HuggingFace model card; documents Apache-2.0 license; training-data mixture details disclosed by license category (1 CC-BY-3.0, 8 MIT, 1 CC0, 6 public-domain, 5 Apache-2.0, 1 CC-BY-4.0) but no quantitative proportions (reproducibility gap flagged in C5). The canonical OOD-collapse example on PromptShield: per Jacob et al. Table 4 (§ C3.1), this detector reports 1.34% TPR @ 0.5% FPR and 0.00% TPR @ 0.1% FPR (annotated as no threshold achieves the desired FPR aside from 1.0) on the held-out PromptShield benchmark despite high in-distribution F1 [claim_training_and_evaluation_protectai2024deberta_a2_provenance].
  - **Status:** Verified (HF model card, 2026-05-22). `freshness_tier: volatile`. **License red flag (Phase 2 report):** exact training-data mixture undisclosed → independent reproducibility limited; cross-cuts to § C4.4 (Nasr 'attacker moves second' static-defense critique) and § C3.1 (PromptShield OOD-collapse evidence). (recheck after 2026-06-22)

4 entries.
