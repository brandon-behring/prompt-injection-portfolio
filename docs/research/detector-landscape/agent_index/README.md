# Prompt-injection Detector Landscape — Research Synthesis

<!-- AGENT-INDEX: this folder is a self-contained reference for the prompt-injection detector landscape (mid-2024 → mid-2026). Read this README first. -->

**Purpose:** Map the prompt-injection detector ecosystem across encoder classifiers, LLM judges, commercial guardrails, and activation-probe / specialized variants — with reconciled benchmark numbers and head-to-head methodology critique. Designed for dual consumption — humans (reading directly) and future LLM agents (grounding reasoning in this literature).
**Primary intended consumer:** future Claude Code / LLM agents working in the `prompt-injection-portfolio` project (and adjacent AI-safety projects) who need detailed context on detector architectures, benchmarks, and known evasion findings. Secondary consumers: human readers researching the prompt-injection defense literature.
**Self-containedness guarantee:** this folder has no hard dependence on sibling files outside itself. Move it elsewhere and it still works (URLs link to primary sources).
**Scope:** Prompt-injection detector literature from mid-2024 to mid-2026. Includes ModernBERT- and DeBERTa-family encoder classifiers, decoder/LLM-judge detectors (PromptShield, CourtGuard, Llama Prompt Guard), commercial / vendor-hosted detection products (Lakera, Azure Prompt Shields, AWS Bedrock Guardrails, NVIDIA NeMo, Google Model Armor, Cisco AI Defense), and activation-probe / specialized detectors (TaskTracker, InstructDetector, InjecGuard, Attention Tracker, Task Shield, MELON, DataSentinel, AlignSentinel, embedding-classifier baselines). Also covers cross-cutting evaluation / evasion / postmortem literature (PromptShield benchmark, NotInject, PINT, WAInjectBench, the Firewalls-NeurIPS paper, the Bypassing Guardrails evasion paper, and "Attacker Moves Second" adaptive-attack systematization).
**Coverage:** 67 entries across 5 topic files (A1-A5); structured 5-bullet entries (Source / Code / Mechanism / Result / Status). Every claim-bearing bullet is traceable to `evidence_ledger.yml` via Evidence IDs; Attribute-First pre-selection commitments live in `pre_selection_manifest.yml`.
**Last updated:** 2026-05-22.

## ⚠️ Scope boundary

This folder covers the **detector landscape only** — classifiers, judges, and guardrail products whose primary function is binary or multi-class classification of inputs into "prompt injection" vs. "benign." It does NOT cover:

- **Direct-vs-indirect prompt injection threat models and architectural defenses** (Spotlighting, StruQ, SecAlign, CaMeL, agent-side input segregation, the dual-LLM pattern) — see [`../../direct-vs-indirect/`](../../direct-vs-indirect/) for that material. Note: MELON, Task Shield, and the Firewalls-NeurIPS paper appear here because they ship discrete detector-like components even though they're architectural defenses; flagged in their Status fields with `(also covered as defense)`.
- **Training-time hardening and evaluation methodology beyond detector benchmarks** (instruction-tuning techniques, RLHF for safety, red-teaming pipelines, AdvBench / HarmBench attack benchmarks themselves) — see [`../../training-and-evaluation/`](../../training-and-evaluation/) for that material.
- **Pre-2023 BERT classifiers** (foundational but obsolete relative to the ModernBERT / DeBERTa-v3 generation that dominates the encoder bucket here).
- **Multimodal injection detectors as a category** — no canonical multimodal detector exists as of mid-2026. Llama Guard 4 is content-moderation, not injection-detection, and is excluded here. (The WAInjectBench entry does cover image-based attacks within the broader web-agent detection benchmark.)
- **Content-moderation classifiers** (toxicity, hate-speech, refusal classifiers) when not specifically positioned as prompt-injection detectors. Llama Guard 3 is included here because it covers MLCommons hazard categories that materially overlap with prompt-injection threat models, and because it's the canonical reference for "LLM-as-judge content classifier"; treat as edge-of-scope.
- **Privately-trained vendor detectors without published benchmark numbers** (HiddenLayer's internal classifier, Robust Intelligence's pre-acquisition stack details, CalypsoAI's full architecture) — referenced in passing under A4 but not given a primary entry.

**Cross-vol overlap convention:** when an entry is methodologically relevant to multiple dossiers (e.g., MELON and Task Shield touch both detector and architectural-defense), the primary location is chosen by claim_family. Architectural-defense methods that *also* ship a detector are flagged in Status with `(also covered as architectural defense)`. **No duplicate primary entries across dossiers** — the duplicate-detection rule lives here.

## How this is organized

Sub-section anchors use the per-file letter prefix from `research_plan.md`: `## A1.` ... `## A5.`. Each entry's anchor is stable; lookup recipes below reference these anchors.

| File | Topic | When to read |
|---|---|---|
| `00_overview.md` | Threat model, landscape map, glossary cross-reference | Start here if new to the prompt-injection detector ecosystem |
| `01_modernbert_detectors.md` | A1: ModernBERT-based encoder detectors (anchors A1.1 - A1.5) | Picking an open-source ModernBERT-family encoder classifier |
| `02_deberta_detectors.md` | A2: DeBERTa-based encoder detectors (anchors A2.1 - A2.5) | Picking an open-source DeBERTa-family encoder classifier or comparing ProtectAI v1 vs v2 |
| `03_llm_detectors.md` | A3: LLM-based detectors — decoder and LLM-as-judge (anchors A3.1 - A3.7) | Picking a small-LM / 8B-judge detector or evaluating the latency vs. accuracy tradeoff |
| `04_commercial_detectors.md` | A4: Commercial / proprietary detectors (anchors A4.1 - A4.10) | Comparing vendor-hosted guardrails (Lakera, Azure, AWS, NVIDIA, Google, Cisco, Meta) and PINT leaderboard methodology |
| `05_specialized_detectors.md` | A5: Activation-probe + specialized + cross-cutting evaluation (anchors A5.1 - A5.20) | Activation-delta probes (TaskTracker, InstructDetector), attention-based (Attention Tracker), embedding-classifier baselines, agentic-defense detectors (Task Shield, MELON, DataSentinel), lightweight char-ngram SVM (Mirror), prompt-injection localization (PromptLocate), and the cross-cutting evaluation / evasion / postmortem literature |

## Lookup recipes

Routes by question type. Each points to a specific file and section anchor.

- **"What's the SOTA encoder-only detector?"** → `01_modernbert_detectors.md` § A1.1 (Sentinel, Ivry & Nahum 2025).
- **"What's the most-cited deployable LLM-judge detector?"** → `03_llm_detectors.md` § A3.1 (PromptShield, Jacob et al. 2025 CODASPY).
- **"What's the foundational activation-probe detector paper?"** → `05_specialized_detectors.md` § A5.1 (TaskTracker, Abdelnabi et al. 2024 / SaTML 2025).
- **"Which encoder model is best for low-latency on M1 / CPU?"** → `02_deberta_detectors.md` § A2.4 (hlyn-labs prompt-injection-judge-deberta-70m, INT8 ONNX).
- **"Which detector handles the over-defense / false-positive problem most explicitly?"** → `05_specialized_detectors.md` § A5.3 (InjecGuard + NotInject benchmark) and A5.4 (PIGuard, ACL 2025).
- **"Where's the canonical PINT leaderboard?"** → `04_commercial_detectors.md` § A4.1 (Lakera PINT blog) and § A4.2 (lakeraai/pint-benchmark GitHub).
- **"Which paper documents the 'detectors are bypassable' empirical finding?"** → `05_specialized_detectors.md` § A5.13 (Hackett et al. 2025, character injection + AML evasion).
- **"What's the most recent systematic adaptive-attack bypass result?"** → `05_specialized_detectors.md` § A5.15 (Nasr et al. 2025, "The Attacker Moves Second").
- **"Which paper covers the 98%-accurate-yet-broken postmortem on encoder classifiers?"** → `05_specialized_detectors.md` § A5.16 (CodeIntegrity Jung 2026 vendor postmortem).
- **"What's the Meta / Llama-side detector stack?"** → `03_llm_detectors.md` § A3.3 (Prompt Guard 2 86M), § A3.4 (Prompt Guard 2 22M), § A3.5 (original Prompt Guard 86M), § A3.6 (Llama Guard 3 8B); product docs at `04_commercial_detectors.md` § A4.10.
- **"What's Lakera Guard's relationship to Cisco?"** → `04_commercial_detectors.md` § A4.3 (Lakera Guard product page) and § A4.8 (Cisco AI Defense post-acquisition).
- **"Which detector achieves perfect security on AgentDojo / InjecAgent / ASB / τ-Bench?"** → `05_specialized_detectors.md` § A5.12 (Bhagwatkar et al. 2025 NeurIPS Firewalls paper).
- **"Which detector explicitly uses game-theoretic / minimax training?"** → `05_specialized_detectors.md` § A5.10 (DataSentinel, Liu et al. 2025 IEEE S&P).
- **"Which detector uses attention-map features without extra LLM inference?"** → `05_specialized_detectors.md` § A5.7 (Attention Tracker, Hung et al. 2025 NAACL Findings).
- **"What benchmark covers web-agent prompt injection detection specifically?"** → `05_specialized_detectors.md` § A5.11 (WAInjectBench, Liu et al. 2025).
- **"What benchmark covers indirect prompt injection on RAG / external content?"** → `05_specialized_detectors.md` § A5.17 (BIPIA, Yi et al. 2023).
- **"Which detector covers AlignSentinel-style 'aligned vs misaligned vs no instruction' three-class problem?"** → `05_specialized_detectors.md` § A5.5 (AlignSentinel, Jia et al. 2026).
- **"Which detector is a lightweight char-ngram linear SVM that beats a small neural detector at sub-ms latency?"** → `05_specialized_detectors.md` § A5.19 (The Mirror Design Pattern, Corll 2026; 95.97% recall / 92.07% F1 vs. 22M Prompt Guard 2).
- **"Which method localizes WHERE the injected prompt is inside contaminated data (not just whether an attack occurred)?"** → `05_specialized_detectors.md` § A5.20 (PromptLocate, Jia et al. IEEE S&P 2026; first prompt-injection localization method).
- **"How do I find the latency vs. accuracy tradeoff curve?"** → glossary entry below ("Latency tradeoff classes") and entries A1.5, A2.4, A3.3, A3.4, A3.7.
- **"Which encoder detector is multilingual?"** → `03_llm_detectors.md` § A3.3 (Llama Prompt Guard 2 86M mDeBERTa-base) and § A3.5 (original Prompt Guard 86M mDeBERTa-base).
- **"What's the canonical industry critique of held-out-split accuracy?"** → `05_specialized_detectors.md` § A5.16 (CodeIntegrity "98% Accurate and Still Broken").
- **"What's NotInject?"** → glossary below; primary reference at `05_specialized_detectors.md` § A5.3.
- **"What's PINT?"** → glossary below; primary references at `04_commercial_detectors.md` § A4.1, A4.2.
- **"What's the difference between Llama Guard and Prompt Guard?"** → `03_llm_detectors.md` § A3.5 vs § A3.6 (Prompt Guard = injection/jailbreak classifier; Llama Guard = content-safety classifier across MLCommons hazard categories).

## Glossary

Canonical term + aliases + one-line definition + primary citation.

- **PINT** (Prompt Injection Test): Lakera's vendor-hosted prompt-injection detection benchmark; serves as the de facto leaderboard for commercial detectors despite the Lakera-designed-and-Lakera-evaluated structural alignment caveat. Primary references: § A4.1, § A4.2.
- **NotInject**: 339-sample benign evaluation dataset enriched with trigger words that commonly cause guardrail over-defense; introduced alongside InjecGuard. Primary reference: § A5.3.
- **MOF** (Mitigating Over-defense for Free): training strategy from InjecGuard that reduces trigger-word bias in prompt guards. Primary reference: § A5.3.
- **Over-defense**: false-positive failure mode where a detector flags benign inputs as malicious due to trigger-word bias (e.g., flagging legitimate instructions that contain phrases like "ignore the above"). Per InjecGuard, SOTA detectors drop close to 60% accuracy (random-guess) on NotInject. Primary reference: § A5.3.
- **Task drift**: deviation from a user's original task caused by injected instructions in external data (RAG / tool outputs); coined in TaskTracker. Detectable via activation deltas between pre- and post-data-ingestion forward passes. Primary reference: § A5.1.
- **TPR@FPR** (True Positive Rate at fixed False Positive Rate): the dominant reporting convention introduced by the PromptShield Berkeley paper; surfaces the "encoder classifiers collapse at low FPR" pattern that uniform accuracy hides. Primary reference: § A3.1.
- **KAD signal** (Known Answer Detection): DataSentinel's secret-canary-token mechanism; the detector LLM is fine-tuned to produce a known token on benign inputs, and absence of that token at inference signals injection. Primary reference: § A5.10.
- **AgentDojo** (Debenedetti et al. 2024, NeurIPS 2024): indirect-prompt-injection agentic benchmark; the canonical evaluation for agentic injection defenses. Referenced from § A5.8, § A5.9, § A5.12.
- **InjecAgent** / **Agent Security Bench** / **τ-Bench**: other indirect-prompt-injection agentic benchmarks alongside AgentDojo, used together in the Firewalls paper. Primary reference: § A5.12.
- **BIPIA** (Benchmark for Indirect Prompt Injection Attack): Microsoft's RAG-flavored indirect-prompt-injection benchmark; one of the standard evaluation datasets. Primary reference: § A5.17.
- **Latency tradeoff classes**: rough latency bands for the detector ecosystem (encoder classifiers ≈ 5-10 ms, INT8-quantized small encoders ≈ 100 ms on M1 CPU per § A2.4, mid-size LM judges ≈ 200-500 ms, 8B-class judges ≈ 500-800 ms per the latency-table in the CodeIntegrity postmortem). Treat these as practitioner rules of thumb; verify on your hardware.
- **Spotlighting**: a non-classifier architectural defense that delimits trusted vs. untrusted text in the prompt; referenced from Azure Prompt Shields (§ A4.4) and called out in the scope boundary as belonging to `../direct-vs-indirect/`.
- **Adaptive attack**: an attack that explicitly modifies its strategy to counter a specific defense's design (vs. evaluating defenses against a static attack set). Primary reference for systematic study: § A5.15 (Nasr et al. "The Attacker Moves Second").
- **LLM-as-judge**: detection pattern where an LLM is prompted to classify another LLM's input as benign vs. injected. CourtGuard (§ A3.2) explicitly contrasts itself against the "Direct Detector" LLM-as-judge baseline. PromptArmor (§ A3.7) is a prominent off-the-shelf LLM-as-judge baseline. Cross-referenced from § A3.7 (PromptArmor) and § A3.2 (CourtGuard).
- **Multiagent debate**: detection via multiple LLM roles arguing in opposition; CourtGuard is the canonical instance (defense-attorney + prosecution + judge). Primary reference: § A3.2.

## Verification & limits

- Citations resolved as of **2026-05-22**. Strict-live v2.2 evidence IDs are present — see `../evidence_ledger.yml`, `../cache_manifest.yml`, `../claim_graph.jsonl`, and `pre_selection_manifest.yml` (Attribute-First spans committed Phase 2b).
- The detector ecosystem is **highly volatile**: vendor pages can shift quarterly, model cards get version-bumped, leaderboard entries change. Verified-at dates and freshness tiers are tracked in `bib_ledger.yml`. Entries with `freshness_tier: volatile` (HF model cards, vendor docs, leaderboards) have a 30-day stale-after window.
- **Vendor-reported numbers should be treated with skepticism.** PINT scores in the Lakera repo are self-evaluated; the only independent reconciliations come from PromptShield's benchmark paper (§ A3.1), the Firewalls NeurIPS paper (§ A5.12), and the "Attacker Moves Second" study (§ A5.15). Vendor `(vendor blog)` Status flags are inline on the affected entries.
- **Lakera-designed-and-Lakera-evaluated PINT structural alignment caveat**: PINT was designed by Lakera (§ A4.1) and is used to rank Lakera Guard alongside competitors (§ A4.2). The benchmark methodology is sound, but the train/eval split alignment between Lakera Guard's training corpus and PINT's evaluation set is a documented concern in the broader literature. The PromptShield Berkeley paper (§ A3.1) is the most-cited independent counter-benchmark.
- **No memory-based attribution.** Every Mechanism / Result claim traces to a primary-source span recorded in `pre_selection_manifest.yml`. Any quantitative claim in the body without an abstract anchor is marked `(unverified body claim)`. Multiple entries (§ A1.2, A1.4, A2.4, A4.3, A4.10, A5.4) use HuggingFace / vendor model cards / ACL Anthology pages whose primary content is interface/UI rather than a quotable substantive claim; those entries have abbreviated Mechanism prose with explicit `(model card surface)` annotation in Status.
- Six entries have un-anchored authorship metadata (paraphrase-only `extraction_method` in `evidence_ledger.yml`): § A1.4 (tihilya), § A2.4 (hlyn-labs), § A4.3 (Lakera Guard product page), § A4.10 (Llama Prompt Guard product doc), § A5.4 (PIGuard ACL paper), § A4.9 (rebuff GitHub). For these, the Mechanism bullet uses the title-anchored or surface span; quantitative claims about parameter counts (e.g., "70M", "395M", "149M") draw from `bib_ledger.title` field which was webfetch-verified at gather time.
- This synthesis is a snapshot. Re-verify against primary sources before relying on time-sensitive vendor numbers; flag `(recheck after 2026-08-22)` is implicit on all `volatile` entries.

**Independent audit, round 1 (2026-05-22):** A complementary-scope review pass focused on recent 2025-26 arXiv entries + vendor model card freshness. Prior rounds: none on agent_index/. Findings: 0 dropped, 1 corrected, 4 flagged. 36 of 40 in-scope entries SPOT-CHECK PASSED (titles / authors / dates / claims all verified against primary sources; AlignSentinel arXiv ID 2602.13597 confirmed as a real Feb 2026 paper). FLAGs centered on venue claims not anchored on arXiv abstract pages (A5.7 Attention Tracker NAACL 2025 Findings; A5.12 Firewalls NeurIPS 2025) and vendor-page cross-references that the dossier paraphrased rather than anchored (A4.3 Lakera Guard → Cisco AI Defense; A4.4 Azure → Spotlighting). The 1 CORRECT was A3.2 CourtGuard's implementation-model list (in code-repo availability statement, not abstract). Recommendation: re-run with focus "GitHub code links + reproducibility claims" (Round 2 below).

**Independent audit, round 2 (2026-05-22):** A complementary-scope review pass focused on GitHub code links + reproducibility claims. Prior rounds covered: recent 2025-26 arXiv entries + vendor model card freshness (Round 1). Findings: 0 dropped, 0 corrected, 0 flagged. All 10 GitHub URLs in the 5 sub-area files resolve (isaacwu2000/CourtGuard, lakeraai/pint-benchmark, protectai/rebuff [archived 2025-05-16 confirmed], MYVAE/Instruction-detection, leolee99/InjecGuard [aliased to PIGuard], leolee99/PIGuard, kaijiezhu11/MELON, Norrrrrrr-lyn/WAInjectBench, IBM/Adversarial-Prompt-Evaluation, microsoft/BIPIA). Reproducibility-claim spot-checks (InstructDetector 99.60%/96.90%/0.03%, Task Shield 2.07%/69.79%, PromptArmor <1% FPR/FNR, Attention Tracker AUROC +10%, Attacker Moves Second 12 defenses / 90% ASR, Sentinel 0.987 accuracy / 0.980 F1, CodeIntegrity PromptGuard 955K examples / ModernBERT-base 149M, hlyn-labs 70M / INT8 / ~101ms M1, LPG2-22M 75% latency reduction, ProtectAI v2 184M, ModernBERT-large 395M) all match primary sources. Recommendation: Clean — stop here.

## Attribution

Synthesized from a research dossier maintained by the research_toolkit (`~/Claude/research_toolkit/`). URLs link to primary sources (arXiv, GitHub, HuggingFace, vendor blogs, conference proceedings). No local file paths are referenced. v2.2 strict-live Attribute-First pipeline: every Mechanism / Result bullet's evidence_id has a matching atom in `pre_selection_manifest.yml` (Phase 2b commitment) verified by the cross-stage validator.


## Sprint 2 audit-trail (Round 3, 2026-05-23)

**Round 3 — Sprint 2 entries verification + body-quote anchoring.** Complementary-scope review covering the 21 entries added in Sprint 2 E2 (compass-mentioned-but-missing sources + thin-sub-area expansion). Findings: 0 DROP / 0 CORRECT / 6 entries kept `status: unverified` (vendor cluster posture — HiddenLayer/RobustIntel/CalypsoAI/Vijil/Guardrails/SafePrompt) / 15 entries promoted to `status: verified` (arXiv + HF model cards + Anthropic + Microsoft + Lakera vendor pages). 8 URL fallbacks resolved at E2 (Lakera year-of-agent path correction, Anthropic browser-PI → Claude-for-Chrome, Microsoft GA → azure-ai-foundry-blog, Robust Intelligence → Cisco acquisition page, CalypsoAI → F5, vijilAI org slug, safeprompt parked → NatLawReview). 1 GitHub URL guess removed (hung2025attentiontracker) per anti-pattern firewall. Recommendation: Clean — stop here (vendor clusters intentionally remain unverified per posture).
