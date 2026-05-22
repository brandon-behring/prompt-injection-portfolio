# Research Plan: Prompt-injection detector landscape

Comprehensive landscape sweep of the prompt-injection detector ecosystem mid-2024 to mid-2026: open-source encoder classifiers, LLM-based judges, commercial guardrails, and activation-probe / architectural variants — with reconciled head-to-head benchmark numbers and methodology critique. Primary audience: future LLM agents picking up the prompt-injection-portfolio project; secondarily the user authoring the book. Target ~30-35 primary-source entries across 5 sub-areas.

## Sub-areas

- A1. ModernBERT-based encoder detectors
  - Source types: arXiv preprints, HuggingFace model cards, vendor blog posts, benchmark leaderboards
  - Notes: Qualifire Sentinel v1 (paper Ivry & Nahum 2025 arXiv 2506.05446), CodeIntegrity PromptGuard, vijil/mbert-prompt-injection, tihilya, ccss17 (stub). Reconcile self-reported vs. independent benchmark numbers. The 8K-token native context is a key differentiator from DeBERTa generation.

- A2. DeBERTa-based encoder detectors
  - Source types: HuggingFace model cards, vendor docs (ProtectAI, deepset), arXiv preprints
  - Notes: ProtectAI deberta-v3-base-prompt-injection v1 + v2 + small, deepset/deberta-v3-base-injection, hlyn/prompt-injection-judge-deberta-70m. Cover INT8 ONNX quantization + LoRA / DoRA variants. Track PromptShield-paper independent numbers vs. self-reported.

- A3. LLM-based detectors (decoder + LLM-as-judge)
  - Source types: arXiv, vendor blog posts, model cards
  - Notes: PromptShield Llama-3.1-8B (Jacob et al. arXiv 2501.15145), Qualifire Sentinel v2 (Qwen3-0.6B), Meta Llama Prompt Guard 1 + 2 (86M + 22M), Llama Guard 1/2/3/4 family, CourtGuard multi-agent (Sun arXiv 2510.19844), DataSentinel (Liu et al. arXiv 2504.11358). Capture the latency / quality tradeoff (5ms encoders → 200ms small LM → 800ms 8B judge).

- A4. Commercial / proprietary detectors
  - Source types: vendor docs, PINT leaderboard, independent benchmark papers
  - Notes: Lakera Guard, Azure AI Prompt Shields (User + Document + Spotlighting), AWS Bedrock Guardrails, NVIDIA NeMo Guardrails, Google Model Armor, Aporia Guardrails, Rebuff, HiddenLayer, Robust Intelligence, CalypsoAI, Vijil Dome, Guardrails AI, SafePrompt. PINT leaderboard scores 2025-05 through 2025-08. Flag the Lakera-designed-PINT structural alignment caveat.

- A5. Activation-probe + specialized detectors
  - Source types: arXiv, IEEE SaTML, GitHub repos
  - Notes: TaskTracker activation-delta probe (Abdelnabi et al. SaTML 2025 arXiv 2406.00799), InstructDetector (arXiv 2505.06311), InjecGuard MOF (Li et al. arXiv 2410.22770), Task Shield (arXiv 2412.16682), MELON (ICML 2025 arXiv 2502.05174), embedding-based detectors (Ayub & Majumdar arXiv 2410.22284). DataSentinel KAD signal is here too.

## Out-of-scope

- Multimodal injection detectors (no canonical detector exists as of mid-2026; Llama Guard 4 is content-moderation, not injection-detection)
- Pre-2023 BERT classifiers (foundational but obsolete relative to ModernBERT/DeBERTa generation)
- Privately-trained detectors with no published benchmark numbers (e.g., HiddenLayer's classifier internals)
- Adversarial-suffix optimization attacks (AdvBench/HarmBench) — they're attack benchmarks, not detector literature; covered as benchmark validity context in `training-and-evaluation/`
- Architectural defenses that aren't detectors (Spotlighting, StruQ, SecAlign, CaMeL) — they belong in `direct-vs-indirect/` because they're not classifier-shaped
- Content-moderation classifiers (toxicity, hate-speech) when not specifically positioned as prompt-injection detectors

## Claim family taxonomy

- detector_architectures — encoder vs. decoder vs. multi-agent shape, base-model choice, parameter count, context window
- detector_benchmarks — PINT, PromptShield benchmark, NotInject, BIPIA, deepset/prompt-injections, rogue-security/prompt-injections-benchmark, JailbreakBench, gandalf, etc.
- commercial_detector_performance — vendor-reported + independently-verified scores for Lakera / Azure / AWS / NVIDIA / Google / Aporia
- detector_latency_tradeoff — inference latency (ms) at the architecture-class level: encoder ~5-10ms, embedding-ML ~80ms, small LM ~200ms, 8B judge ~500-800ms
- architectural_defense_methods — referenced from `direct-vs-indirect/`; this dossier flags when a detector is *also* used as part of a multi-layer architectural defense (Llama Prompt Guard 2 + Spotlighting + tool-filter stack)

## Known landmark papers

These are pre-known canonical references; `/research-gather` populates bibkeys without spending discovery effort:

- jacob2025promptshield: PromptShield Berkeley (arXiv 2501.15145, ACM CODASPY 2025) — Llama-3.1-8B SOTA at low FPR; the source of the "TPR@FPR" reporting convention
- ivry2025sentinel: Qualifire Sentinel v1 paper (arXiv 2506.05446) — ModernBERT-large 395M
- sun2025courtguard: CourtGuard multi-agent debate (arXiv 2510.19844, Oct 2025) — NotInject >90%
- li2024injecguard: InjecGuard + NotInject benchmark (arXiv 2410.22770) — MOF over-defense mitigation
- liu2025datasentinel: DataSentinel game-theoretic detector (arXiv 2504.11358) — KAD secret-token signal
- abdelnabi2025tasktracker: TaskTracker activation probe (IEEE SaTML 2025; toolkit dataset >500K instances across 6 LLMs)
- ayub2024embedding: Embedding-based detectors (arXiv 2410.22284) — XGBoost / Random Forest / MLP on embedding space
- jung2026postmortem: CodeIntegrity "98% Accurate and Still Broken" (Jan 2026 blog) — the most-cited industry self-critique of held-out-split accuracy
- bhagwatkar2025firewalls: "Are Firewalls All You Need?" (NeurIPS 2025 arXiv 2510.05244) — two-firewall defense saturating AgentDojo / InjecAgent / ASB / τ-Bench
- hackett2025bypassing: "Bypassing Prompt Injection and Jailbreak Detection in LLM Guardrails" (arXiv 2504.11168, April 2025) — character-injection 100% ASR results
