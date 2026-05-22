# Research Plan: Training data + evaluation methodology + benchmark validity + OOD generalization

How prompt-injection detectors are actually trained and evaluated: training data catalogs, training methodologies (LoRA + energy-loss + DoRA + Recall@LowFPR + game-theoretic), evaluation methodologies (TPR@LowFPR, NotInject over-defense, LODO, adaptive-attack resilience), benchmark-validity critiques (Goodhart, CodeIntegrity "98% post-mortem", "Are Firewalls All You Need?"). Foundational to the portfolio's OOD-wall thesis. Target ~25-30 primary-source entries across 5 sub-areas.

## Sub-areas

- C1. Training data sources
  - Source types: HuggingFace dataset cards, arXiv preprints, competition GitHub repos, vendor blog posts
  - Notes: Foundational small datasets (deepset/prompt-injections, jackhhao/jailbreak-classification, xTRam1/safe-guard, verazuo/jailbreak_llms, TrustAIRLab/in-the-wild-jailbreak-prompts, lakera/gandalf_ignore_instructions, lmsys/toxic-chat); mid-size aggregated (geekyrakshit/prompt-injection-dataset 534K, reshabhs/SPML 16K, Qualifire / rogue-security benchmark, alespalla / VMware open-instruct, microsoft/orca-agentinstruct-1M); crowd-sourced / competition (TensorTrust Toyer et al. ICLR 2024 arXiv 2311.01011, HackAPrompt 1.0 Schulhoff et al. EMNLP 2023 arXiv 2311.16119, microsoft/llmail-inject-challenge); safety/red-team reuse (AdvBench, HarmBench, JailbreakBench, allenai/wildjailbreak, wildguardmix, OpenSafetyLab/Salad-Data, JailbreakV-28K, PurpleLlama/CyberSecEval); 2025-26 specialized (DhruvTre/jailbreakbench-paraphrase, hendzh/PromptShield, hlyn/prompt-injection-judge-deberta-dataset, protectai/prompt-injection-validation). License + size + composition + known issues per dataset.

- C2. Training methodologies
  - Source types: model cards, arXiv methodology papers, vendor engineering posts
  - Notes: Encoder baseline recipe (AdamW LR 2e-5 to 5e-5, batch 8-32, 3 epochs, CE). Advanced techniques: energy-based loss (Liu NeurIPS 2020 arXiv 2010.03759, used by Meta PG2 + CodeIntegrity); custom Recall@1%FPR loss (Meta PG2); Evidential Deep Learning (hlyn); DoRA / SupCon / FreeLB / R-Drop / SWA / Mixout (hlyn aggressive stack); LoRA/PEFT (ccss17, Sentinel-v2); INT8 ONNX quantization (hlyn). LLM-based: PromptShield LoRA on Llama-3.1-8B, LR 2e-4, 3 epochs, with `\n` augmentation. DataSentinel minimax fine-tune. Sentinel v2 Qwen3-0.6B departure from encoder.

- C3. Evaluation metrics + methodology
  - Source types: arXiv methodology papers, benchmark documentation, vendor benchmark blog posts
  - Notes: Metric hierarchy: accuracy (almost never useful at production imbalance) → F1 / precision / recall (threshold-dependent) → AUC-ROC (insensitive at low-FPR tail) → AUC-PR (better under imbalance) → **TPR @ low FPR** (PromptShield's signature: 1% / 0.5% / 0.1% / 0.05%) → APR (Meta PG2: % attacks blocked at ≤3% utility loss) → over-defense accuracy (NotInject). PromptShield's TPR@LowFPR table reveals encoder collapse at deployment-grade FPRs. AgentDojo's coupled benign-utility + utility-under-attack reveals "inverse scaling law" (more capable models more attackable). Methodology stack: held-out test from same mixture (memorization), OOD evaluation (held-out datasets not rows), independent third-party benchmarks (PINT 4,314 inputs never-trained-on), adaptive-attack evaluation (LLMail-Inject), end-to-end agentic (AgentDojo 97×629), production telemetry (Lakera Gandalf — unreproducible).

- C4. Benchmark validity + methodology critiques
  - Source types: arXiv critique papers, industry blog post-mortems
  - Notes: CodeIntegrity "98% Accurate and Still Broken" (Steven Jung Jan 2026, the most-cited industry post-mortem) — "measures memorization, not generalization"; Joshua Saxe F-score critique ("85% F-score on test data likely more meaningful than 95% fit to test distribution"). "Are Firewalls All You Need?" (Bhagwatkar et al. arXiv 2510.05244 NeurIPS 2025) — AgentDojo / ASB / InjecAgent / τ-Bench saturated by 2-firewall defenses, weak attacks hindering progress. "Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails" (Hackett et al. arXiv 2504.11168) — 12 character-injection techniques + 8 TextAttack methods achieve up to 100% bypass. "When Benchmarks Lie" (arXiv 2602.14161). Goodhart's law on public benchmarks (Lakera explicit PINT design rationale). Training-data leakage (deepset overlap across many models). Vendor self-comparison patterns (Sentinel vs ProtectAI-only, hlyn vs ProtectAI-only). Selection bias in self-reported numbers. Mismatch between attack benchmarks (AdvBench / HarmBench) and detector benchmarks (PINT / NotInject / PromptShield).

- C5. OOD generalization methodology + reproducibility crisis
  - Source types: arXiv, vendor model cards (for what is/isn't disclosed), submission's own ADR-016/-075
  - Notes: LODO methodology (Leave-One-Dataset-Out per submission ADR-016) — held-out datasets, not held-out rows. PromptShield's training/test split: conversational vs. application-structured as two-track design. ProtectAI v1's 99.99% F1 → 0.00% TPR @ 0.5% FPR on PromptShield (the canonical OOD-collapse example). XLM-RoBERTa 99.13% on deepset → memorization signal. Reproducibility crisis: Qualifire Sentinel's private subset undisclosed; Meta Prompt Guard 2 red-team data undisclosed; ProtectAI's exact mixture undisclosed; "winning" detectors mostly not reproducible end-to-end from public artifacts. Submission's ADR-075 unified narrative: LoRA full-FT OOD drop is methodologically load-bearing; fine-tuning consumed OOD generalization budget. v1.1.2 DeBERTa null result: backbone-invariant verdict. Per ADR-016 + ADR-075 the portfolio inherits + extends this discipline.

## Out-of-scope

- Specific detector implementations — covered in `detector-landscape/`
- Architectural defenses (Spotlighting, StruQ, SecAlign, CaMeL, Instruction Hierarchy) — covered in `direct-vs-indirect/`, only cited here when they bear on training methodology (e.g., SecAlign's DPO recipe, Instruction Hierarchy's "context synthesis" training)
- Multimodal training (no widely-adopted models; covered as a 1-paragraph open-area note)
- Jailbreak elicitation evaluation that isn't framed as detector evaluation (AdvBench / HarmBench are referenced only as attack benchmarks for context)
- Content moderation eval (toxicity, hate-speech, CSAM) — referenced only when Llama Guard family is cited for incidentally-high NotInject scores
- Pre-2023 evaluation methodology (foundational benchmarks like GLUE/SuperGLUE belong to NLP methodology, not prompt-injection-specific)

## Claim family taxonomy

- training_data_sources — every dataset cited, with license + size + composition + known leakage issues
- training_methodologies — recipes (encoder + LLM + game-theoretic); specific loss-function variants (energy, Recall@FPR, EDL); PEFT variants; quantization
- evaluation_metrics — accuracy / F1 / AUC-ROC / AUC-PR / TPR@LowFPR / APR / over-defense / ASR-utility tradeoff; what each measures, what it misses
- benchmark_validity — Goodhart on public benchmarks, training-data leakage, selection bias in self-reported numbers, adaptive-attack resilience, methodology critiques
- ood_evaluation_methodology — LODO, held-out datasets vs. rows, conversational vs. application-structured tracks; the portfolio's inherited LODO discipline from submission ADR-016
- reproducibility_practice — disclosure gaps in winning detectors, vendor private-data slices, dataset license + provenance hygiene

## Known landmark papers

- jacob2025promptshield: PromptShield (Berkeley CODASPY 2025 arXiv 2501.15145) — TPR@LowFPR reporting convention, conversational + application-structured benchmark
- liu2020energyloss: Energy-based loss (NeurIPS 2020 arXiv 2010.03759) — basis of Meta PG2 + CodeIntegrity recipe
- toyer2024tensortrust: TensorTrust crowd-sourced attacks (ICLR 2024 arXiv 2311.01011)
- schulhoff2023hackaprompt: HackAPrompt competition + ontology (EMNLP 2023 arXiv 2311.16119)
- abdelnabi2025llmailinject: LLMail-Inject 208K adaptive attacks (Microsoft IEEE SaTML 2025 arXiv 2506.09956)
- zou2023advbench: GCG paper (arXiv 2307.15043) — adversarial-suffix attack benchmark
- mazeika2024harmbench: HarmBench (ICML 2024) — 400 behaviors × 7 categories
- chao2024jailbreakbench: JBB-Behaviors (NeurIPS 2024 D&B arXiv 2404.01318)
- jiang2024wildjailbreak: AllenAI WildJailbreak / WildGuardMix
- jung2026postmortem: CodeIntegrity "98% Accurate and Still Broken" (Jan 2026) — most-cited industry self-critique
- bhagwatkar2025firewalls: "Are Firewalls All You Need?" (NeurIPS 2025 arXiv 2510.05244) — benchmark-saturation critique
- hackett2025bypassing: "Bypassing Prompt Injection" (arXiv 2504.11168) — character-injection 100% ASR
- wallace2024instructionhierarchy: OpenAI Instruction Hierarchy training (arXiv 2404.13208) — context-synthesis training recipe
- saxe2023fscore: Joshua Saxe F-score-over-85 thesis (industry blog) — referenced in CodeIntegrity post-mortem
- nasr2025attackersecond: "Attacker moves second" (arXiv 2510.09023) — static-defense critique
- howNotToDetect2025: "How Not to Detect Prompt Injections with an LLM" (arXiv 2507.05630) — DataSentinel DataFlip bypass

## Cross-references to submission (inherited methodology)

- Submission ADR-016: LODO methodology (cross-source disjoint splits) — portfolio inherits via ADR-016 in this repo
- Submission ADR-075: unified full-FT OOD drop narrative (supersedes ADR-050 R2 + ADR-052) — load-bearing for the OOD-wall thesis
- Submission v1.1.2: DeBERTa-v3-base null result (backbone-invariant verdict)
