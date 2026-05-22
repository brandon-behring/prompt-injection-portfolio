<!-- AGENT-INDEX: training_and_evaluation v2.2 strict-live; covers 45 sources across C1-C5; OOD-wall thesis foundational dossier. -->

# Training data + evaluation methodology + benchmark validity + OOD generalization — Agent Index

**Purpose:** dual-audience reference covering how prompt-injection detectors are actually trained and evaluated: training-data catalogs, training recipes, evaluation metrics, benchmark-validity critiques, and out-of-distribution (OOD) generalization methodology.
**Primary intended consumer:** future LLM agents working in the prompt-injection-portfolio that need grounded context on detector training + evaluation methodology. Secondary consumers: humans reading the material directly.
**Self-containedness guarantee:** this folder is a self-contained synthesis. Move it elsewhere and the cross-links to sibling dossiers still describe what's where.
**Scope:** 2018–2026 (with one 2020 OOD-detection foundational paper). Five sub-areas — training data sources (C1), training methodologies (C2), evaluation metrics (C3), benchmark-validity critiques (C4), OOD methodology + reproducibility (C5).
**Coverage:** 45 primary-source entries across 5 topic files. 5-bullet schema (Source / Code / Mechanism / Result / Status) with inline atomic claim IDs.
**Last updated:** 2026-05-22.

## ⚠️ Scope boundary

This dossier covers **training + evaluation methodology** for prompt-injection detectors and adjacent guardrails. It does NOT cover:

- **Specific detector implementations** (vendor profiles, model architectures, benchmark leaderboard standings). Those live in [`../detector-landscape/`](../detector-landscape/) (added 2026-05-22). When this dossier cites a detector (ProtectAI, Meta Prompt Guard 2, Qualifire Sentinel, PromptShield, hlyn EDL), the citation is about its training recipe or evaluation result, not its product-surface taxonomy.
- **Architectural defenses** (Spotlighting, StruQ, SecAlign, CaMeL, Instruction Hierarchy as a training paradigm). Those live in [`../direct-vs-indirect/`](../direct-vs-indirect/) (added 2026-05-22). Instruction Hierarchy is cited here for its training data composition (Wallace et al. 2024) but the broader direct/indirect taxonomy belongs in the sibling dossier.
- **Multimodal training** — no widely-adopted PI multimodal detectors as of 2026-05-22. JailBreakV-28K (`luo2024jailbreakv28k`) is included only as a multimodal **attack corpus**, not as a multimodal detector training recipe.
- **Jailbreak-elicitation evaluation that isn't framed as detector evaluation** — AdvBench / HarmBench / JailbreakBench / WildJailbreak / SALAD-Bench appear here only as training-data corpora or as the attack benchmarks paired with detector evaluations; their full attack-benchmark methodology is out-of-scope.
- **General content moderation evaluation** (toxicity, hate, CSAM) — referenced only when WildGuard / Llama Guard family is cited for incidentally-high NotInject scores.
- **Pre-2023 NLP evaluation methodology** (GLUE/SuperGLUE) — out-of-scope; this dossier starts at 2020 (energy-OOD) and 2018 (Evidential Deep Learning) only because both methods are reused in PI detector recipes (Meta PG2, hlyn).

**Cross-vol overlap convention:** every entry has exactly one canonical location. When a paper supports both training methodology (C2) and OOD evaluation methodology (C5) — e.g., `liu2020energyood`, `wallace2024instructionhierarchy`, `liu2025datasentinel`, `meta2025promptguard2` — it lives in its primary claim_family file and is cross-referenced from lookup recipes. **Do NOT duplicate entries across files.** Cross-cuts (e.g., Bhagwatkar's saturation finding affecting both C3 and C4) are surfaced in lookup recipes, not by duplicating the entry.

## How this is organized

Section anchors use a per-file letter prefix matching the research_plan's `C1–C5` numbering. Each topic file uses `## C1.`, `## C2.`, etc., matching the sub-area letter.

| File | Topic | Sources |
|---|---|---|
| `01_training_data_sources.md` | C1 — Training data sources (datasets used to train PI detectors) | 19 |
| `02_training_methodologies.md` | C2 — Training methodologies (LoRA, DoRA, energy loss, EDL, game-theoretic, Instruction Hierarchy) | 8 |
| `03_evaluation_metrics.md` | C3 — Evaluation metrics + methodology (TPR@LowFPR, APR, NotInject over-defense, agentic benchmarks) | 8 |
| `04_benchmark_validity.md` | C4 — Benchmark validity + methodology critiques (98% post-mortem, Are Firewalls All You Need?, bypassing, DataFlip) | 6 |
| `05_ood_methodology_reproducibility.md` | C5 — OOD generalization methodology + reproducibility crisis (LODO, conversational vs application-structured, ProtectAI collapse, disclosure gaps) | 4 |

(Total: 45 entries.)

## Lookup recipes

Routes by question type. Each recipe points to a file and a section anchor.

- **"What datasets do public PI detectors train on?"** → `01_training_data_sources.md` § C1.1–C1.19 (the canonical catalog).
- **"What's the largest aggregated open PI dataset?"** → `01_training_data_sources.md` § C1.8 (`geekyrakshit2024promptinjectiondataset`, ~534K rows — license red flag, see Status field).
- **"What's the canonical crowd-sourced PI attack dataset?"** → `01_training_data_sources.md` § C1.9 (`toyer2023tensortrust`).
- **"What's HackAPrompt?"** → `01_training_data_sources.md` § C1.10 (`schulhoff2023hackaprompt`, EMNLP 2023 competition).
- **"What's LLMail-Inject?"** → `01_training_data_sources.md` § C1.11 (`abdelnabi2025llmailinject`, Microsoft IEEE SaTML 2025 adaptive-attack corpus).
- **"What datasets have attack content I should handle carefully (ADR-041)?"** → `01_training_data_sources.md` § C1.9 (TensorTrust), § C1.10 (HackAPrompt), § C1.12 (AdvBench/GCG), § C1.13 (HarmBench), § C1.15 (WildJailbreak), § C1.18 (JailBreakV-28K). Status field flags these explicitly.
- **"What datasets have license red flags?"** → see glossary "License red flags"; flagged entries: C1.8 (geekyrakshit aggregator provenance), C1.15 (WildJailbreak ETHICS), `02_training_methodologies.md` § C2.5 (Meta PG2 undisclosed training data), `05_ood_methodology_reproducibility.md` § C5.2 (Qualifire benchmark private subset), § C5.4 (ProtectAI mixture undisclosed).
- **"What's the foundational PEFT method for PI detector fine-tuning?"** → `02_training_methodologies.md` § C2.2 (`hu2021lora`, LoRA, ICLR 2022).
- **"What's DoRA and where is it used in PI?"** → `02_training_methodologies.md` § C2.3 (`liu2024dora`, ICML 2024 Oral; one component of hlyn's aggressive PEFT stack).
- **"Why energy-based loss in Meta Prompt Guard 2?"** → `02_training_methodologies.md` § C2.1 (`liu2020energyood`, NeurIPS 2020) → § C2.5 (`meta2025promptguard2` adoption).
- **"What's a game-theoretic PI detector?"** → `02_training_methodologies.md` § C2.6 (`liu2025datasentinel`, IEEE S&P 2025 Distinguished Paper); see also `04_benchmark_validity.md` § C4.5 (`choudhary2025detect`, DataFlip bypass).
- **"What's the canonical OOD-collapse example?"** → `05_ood_methodology_reproducibility.md` § C5.4 (`protectai2024deberta`) cross-cuts to `03_evaluation_metrics.md` § C3.1 (`jacob2025promptshield` reports the 0.00% TPR @ 0.5% FPR).
- **"What's TPR@LowFPR and why does it matter?"** → `03_evaluation_metrics.md` § C3.1 (`jacob2025promptshield`).
- **"What's APR (Attack Prevention Rate)?"** → `02_training_methodologies.md` § C2.5 (`meta2025promptguard2`).
- **"What's NotInject?"** → `03_evaluation_metrics.md` § C3.3 (`li2024injecguard`).
- **"What's PINT?"** → `03_evaluation_metrics.md` § C3.4 (`lakera2024pint`, vendor benchmark, designed against Goodhart's law).
- **"What's AgentDojo's 'inverse scaling law'?"** → `03_evaluation_metrics.md` § C3.2 (`debenedetti2024agentdojo`).
- **"What's the 'Are Firewalls All You Need?' saturation finding?"** → `04_benchmark_validity.md` § C4.2 (`bhagwatkar2025firewalls`, NeurIPS 2025).
- **"What's the '98% post-mortem'?"** → `04_benchmark_validity.md` § C4.1 (`jung2026postmortem`, CodeIntegrity Jan 2026); see Saxe quote + 'speed bump' framing.
- **"How can character-injection bypass PI guardrails?"** → `04_benchmark_validity.md` § C4.3 (`hackett2025bypassing`).
- **"What's the 'attacker moves second' critique?"** → `04_benchmark_validity.md` § C4.4 (`nasr2025attackersecond`).
- **"What's DataFlip / 'How Not to Detect Prompt Injections with an LLM'?"** → `04_benchmark_validity.md` § C4.5 (`choudhary2025detect`).
- **"What's LODO and why does the portfolio inherit it from submission ADR-016?"** → `05_ood_methodology_reproducibility.md` § C5.1 (`fomin2026benchmarkslie`); see also Verification & limits below for the ADR-016 / ADR-075 inheritance note.
- **"What's the PromptShield two-track conversational/application-structured split?"** → `03_evaluation_metrics.md` § C3.1 (paper) + `05_ood_methodology_reproducibility.md` § C5.3 (`hendzh2025promptshielddataset` HF mirror).

## Glossary

- **APR** (Attack Prevention Rate): Meta Prompt Guard 2's headline metric — fraction of attacks blocked at ≤3% utility loss. See `meta2025promptguard2` (§ C2.5).
- **Attribute-First**: methodology where the model commits to evidence spans BEFORE generating prose, so post-hoc rationalization is structurally impossible. Used in this dossier's `pre_selection_manifest.yml` (Phase 2b of `/agent-index`). Reference: Slobodkin et al. (2024 ACL).
- **AUC-PR** (Area Under Precision-Recall curve): preferred over AUC-ROC under class imbalance.
- **AUC-ROC** (Area Under Receiver Operating Characteristic curve): insensitive at low-FPR deployment regime; PromptShield critique. See § C3.1.
- **BIPIA**: Benchmarking Indirect Prompt Injection Attacks (Yi et al. 2023, Microsoft, KDD 2025). See § C3.5.
- **DataFlip**: instruction-inversion bypass of LLM-based PI detectors (Choudhary et al. 2025, ACM AISec 2025). See § C4.5.
- **DoRA**: Weight-Decomposed Low-Rank Adaptation (Liu et al. 2024, ICML 2024 Oral). PEFT variant adopting magnitude + direction decomposition. See § C2.3.
- **EDL** (Evidential Deep Learning): Sensoy et al. 2018 NeurIPS uncertainty-quantification method; reused in hlyn's PI detector. See § C2.4.
- **F1 / Precision / Recall**: threshold-dependent metrics; less informative than TPR@LowFPR under heavy class imbalance.
- **FPR** (False Positive Rate): in PI context, fraction of benign inputs flagged as injections; deployment-grade FPRs are typically 0.05–1%.
- **GCG** (Greedy Coordinate Gradient): adversarial-suffix attack (Zou et al. 2023 arXiv 2307.15043); foundational AdvBench attack benchmark. See § C1.12.
- **Goodhart's law**: explicit design rationale of Lakera PINT (`lakera2024pint`, § C3.4) — public benchmarks become training data, distorting their measurement value.
- **HackAPrompt**: global-scale PI competition (Schulhoff et al. 2023, EMNLP 2023). See § C1.10.
- **License red flags**: dataset entries with attack content (ADR-041 ETHICS constraint) and/or mixed/undisclosed license + provenance. Flagged in Status fields. The 5 entries surfaced in the Phase 2 final report: `jiang2024wildjailbreak` (§ C1.15), `geekyrakshit2024promptinjectiondataset` (§ C1.8, aggregator), `rogue2025promptinjectionsbenchmark` (§ C5.2, private subset), `meta2025promptguard2` (§ C2.5, training data undisclosed), `protectai2024deberta` (§ C5.4, exact mixture undisclosed).
- **LLMail-Inject**: ~208K adaptive-attack corpus (Abdelnabi et al. 2025, IEEE SaTML 2025). See § C1.11.
- **LODO** (Leave-One-Dataset-Out): OOD-evaluation discipline of training on N-1 datasets and testing on the held-out Nth dataset (not held-out rows from the same mixture). Introduced for PI in `fomin2026benchmarkslie` (§ C5.1); inherited by submission ADR-016 + ADR-075, this portfolio extends that discipline.
- **LoRA** (Low-Rank Adaptation): foundational PEFT method (Hu et al. 2021, ICLR 2022). See § C2.2.
- **MOF** (Mitigating Over-defense for Free): training scheme proposed by InjecGuard (Li et al. 2024). See § C3.3.
- **NotInject**: benign-prompts-with-trigger-words over-defense benchmark (~339 prompts) bundled with InjecGuard. See § C3.3.
- **OOD wall**: portfolio-internal name for the empirical observation that PI detectors collapse from near-perfect in-distribution F1 to near-zero TPR at deployment FPRs when evaluated on truly held-out data. Cross-referenced from: `jacob2025promptshield` (§ C3.1), `protectai2024deberta` (§ C5.4), `fomin2026benchmarkslie` (§ C5.1), `bhagwatkar2025firewalls` (§ C4.2 saturation finding).
- **PEFT** (Parameter-Efficient Fine-Tuning): LoRA + DoRA + adapter family; HuggingFace PEFT library is the standard impl.
- **PINT** (Prompt Injection Test): Lakera 2024 third-party benchmark (~4,314 inputs deliberately not used as training data); see § C3.4.
- **PromptShield**: Berkeley benchmark + detector (Jacob et al. CODASPY 2025) with TPR@LowFPR reporting convention and conversational + application-structured two-track design. See § C3.1.
- **TPR @ low FPR** (1% / 0.5% / 0.1% / 0.05%): PromptShield's signature reporting convention; reveals encoder PI detector collapse at deployment-grade FPRs. See § C3.1.
- **τ-bench** (tau-bench): Yao et al. 2024 tool-agent-user-interaction benchmark; included in Bhagwatkar's saturation analysis. See § C3.7.

## Verification & limits

- Citations resolved as of **2026-05-22**.
- Strict-live v2 evidence IDs: **present**. See `../evidence_ledger.yml` (123 evidence entries, supporting 123 atomic claim_ids), `../cache_manifest.yml` (45 cached sources), `../claim_graph.jsonl` (381 records), and `pre_selection_manifest.yml` (92 Attribute-First span selections committed in Phase 2b BEFORE bullet prose generation).
- Per the Attribute-First contract, every claim_id rendered inline in topic files (`[claim_training_and_evaluation_<bibkey>_aN_<descriptor>]`) is a subset of the atom_ids declared in `pre_selection_manifest.yml`. Validator-enforced.
- **Inherited LODO discipline:** this dossier inherits the submission's `ADR-016` (cross-source disjoint splits) and `ADR-075` (unified full-FT OOD drop narrative, supersedes ADR-050 R2 + ADR-052). The LODO methodology in § C5.1 (`fomin2026benchmarkslie`) is the published academic articulation of the same discipline; the portfolio's v1.1.2 DeBERTa-v3-base null result is the backbone-invariant verdict mirroring the inherited submission narrative.
- **Volatility:** vendor blog and HF model/dataset card entries (`(vendor blog)`, `freshness_tier: volatile`, 30-day window) need re-verification after 2026-06-22 at the latest. Entries: `lakera2024pint` (§ C3.4), `jung2026postmortem` (§ C4.1), `meta2025promptguard2` (§ C2.5), `protectai2024deberta` (§ C5.4), all HF dataset cards in C1, `rogue2025promptinjectionsbenchmark` (§ C5.2), `hendzh2025promptshielddataset` (§ C5.3).
- **ETHICS constraint (ADR-041):** datasets containing attack content (TensorTrust, HackAPrompt, AdvBench/HarmBench/JailbreakBench, WildJailbreak/WildGuardMix, JailBreakV-28K, LLMail-Inject, ToxicChat) — this dossier documents existence + composition + license but does NOT excerpt attack examples into the 5-bullet bodies.
- **Verbatim-anchored quotes:** four key claims have substring + sha256 + bytes-equality anchors in `evidence_ledger.yml`: Saxe's F-score critique + CodeIntegrity 'speed bump, not a wall' framing (both in § C4.1); Bhagwatkar's 'all four public benchmarks' saturation phrasing + 'weak attacks, hindering progress' (both in § C4.2). The other 119 evidence entries use `extraction_method: paraphrase` from cached abstracts/dataset descriptions.

## Attribution

Synthesized from primary sources cached locally (45 cached pages, 123 evidence supports, 381 claim_graph records). URLs link to canonical primary sources (arXiv abs pages, HuggingFace dataset/model cards, vendor blog posts, conference proceedings). No local file paths are referenced. Maintained by the research_toolkit pipeline (`~/Claude/research_toolkit/`). Topic C of a 3-topic sprint (paired with `../detector-landscape/` and `../direct-vs-indirect/`).
