<!-- AGENT-INDEX: agentic-security-architecture; 25 entries; 2026-05-23 -->

# Agentic security architecture — Research Synthesis

**Purpose:** Lane 4 + Lane 5 dossier — agent harness security, capability-based isolation (CaMeL, IsolateGPT/SecGPT, dual-LLM patterns), score fusion + stacker theory, activation-probe methodology (TaskTracker + extensions), and agentic-bench critique. Designed primarily for future LLM agents picking up portfolio Lanes 4-5; secondarily for the user authoring Ch 11-12.

**Primary intended consumer:** future Claude Code / LLM agents grounding reasoning in this literature. Secondary: humans reading directly.

**Scope:** mid-2024 to mid-2026 agentic-security literature. 25 entries across 5 sub-areas.

**Coverage:** 25 entries (24 cross-classified from `direct-vs-indirect/` + `detector-landscape/` + `training-and-evaluation/` with `agentic_` bibkey prefix; 1 net-new: AgentArmor).

**Last updated:** 2026-05-23.

## ⚠️ Scope boundary

This folder is the *agentic-side* of architectural defenses. Companion topics:
- `../direct-vs-indirect/` — threat-model taxonomies (B1) + architectural defenses generally (B2) + production incidents (B3) + agentic-benchmark catalogue (B4). Spotlighting/StruQ/SecAlign/Jatmo live there as general architectural defenses.
- `../detector-landscape/` — encoder + LLM-judge + activation-probe-as-classifier detector landscape. Activation probes deployed as classifiers are there; this dossier focuses on the activation-delta signal class methodology (D4).
- `../training-and-evaluation/` — training data + eval methodology + benchmark validity + OOD methodology. Includes the inherited LODO + ADR-075 unified OOD-drop narrative.
- `../rag-injection-defenses/` — RAG-retrieval-boundary defenses. Sister Sprint-2 topic.

**Cross-classification convention:** entries here use `agentic_<original_bibkey>` prefix when re-citing sources from sibling topics. Each agentic entry has a topic-tailored excerpt focused on the agentic-architectural dimension.

## How this is organized

| File | Topic | Anchors |
|---|---|---|
| `01_agent_harness_architecture.md` | D1 — Agent harness security architecture | D1.1-D1.8 |
| `02_capability_based_isolation.md` | D2 — Capability-based isolation + dual-LLM patterns | D2.1-D2.3 |
| `03_score_fusion_stacker.md` | D3 — Score fusion + stacker theory | D3.1-D3.5 |
| `04_activation_probe_methodology.md` | D4 — Activation-probe methodology beyond TaskTracker | D4.1-D4.3 |
| `05_agentic_bench_critique.md` | D5 — Agentic-bench critique + adaptive evaluation | D5.1-D5.6 |

## Lookup recipes

- **"What's CaMeL?"** → `02_capability_based_isolation.md` § D2 (Debenedetti et al. arXiv 2503.18813)
- **"How does Meta Prompt Guard 2 achieve high Recall@1%FPR?"** → `03_score_fusion_stacker.md` § D3 (custom Recall@1%FPR loss + energy-based loss recipe)
- **"What's the canonical activation-probe paper?"** → `04_activation_probe_methodology.md` § D4 (TaskTracker — Abdelnabi et al. SaTML 2025)
- **"What benchmark saturation finding does Bhagwatkar 2025 establish?"** → `05_agentic_bench_critique.md` § D5 (AgentDojo + ASB + InjecAgent + τ-Bench saturated by 2-firewall defenses)
- **"What's the adaptive-attack gold standard for agent harnesses?"** → `05_agentic_bench_critique.md` § D5 (LLMail-Inject — 208K attacks, Microsoft IEEE SaTML 2025)
- **"What does Task Shield achieve on AgentDojo?"** → `05_agentic_bench_critique.md` § D5 (2.07% ASR / 69.79% utility on GPT-4o)
- **"What does MELON achieve?"** → `05_agentic_bench_critique.md` § D5 (0.24% ASR / 68.52% utility — current floor)
- **"What's the Instruction Hierarchy training recipe?"** → `01_agent_harness_architecture.md` § D1 (Wallace et al. OpenAI arXiv 2404.13208)
- **"What's the StruQ approach?"** → `01_agent_harness_architecture.md` § D1 (reserved-delimiter SFT; Chen et al. USENIX 2025)
- **"What's the SecAlign recipe?"** → `01_agent_harness_architecture.md` § D1 (DPO over secure/insecure response pairs; Chen et al. CCS 2025)
- **"What is dual-LLM pattern?"** → `02_capability_based_isolation.md` § D2 (Willison 2023 informal articulation; CaMeL formalization 2025)
- **"What's LlamaFirewall?"** → `01_agent_harness_architecture.md` § D1 (Meta arXiv 2505.03574; layered agent firewall)
- **"What's AgentArmor?"** → `01_agent_harness_architecture.md` § D1 (Wang et al. arXiv 2508.01249; agent-layer firewall pattern)
- **"What activation-probe extends TaskTracker?"** → `04_activation_probe_methodology.md` § D4 (InstructDetector arXiv 2505.06311; AttentionTracker)
- **"What's the Jatmo distillation approach?"** → `01_agent_harness_architecture.md` § D1 (task-specific distillation; <0.5% ASR)
- **"Why does encoder-only TaskTracker port test matter?"** → `04_activation_probe_methodology.md` § D4 (Lane 5 hypothesis — does activation-probe recipe transfer to ModernBERT encoder space?)
- **"What's the embedding-based detector approach?"** → `03_score_fusion_stacker.md` § D3 (Ayub & Majumdar 2024 arXiv 2410.22284 — XGBoost on OpenAI embeddings)
- **"What's InjecGuard MOF?"** → `03_score_fusion_stacker.md` § D3 (Mitigating Over-defense for Free; Li et al. 2024)

## Glossary

- **agent harness**: the system-shape layer underlying agentic deployment — tool-calling agents, multi-turn loops, side-effect surfaces, sub-agent delegation, persistent memory.
- **CaMeL**: capability-based isolation with custom Python interpreter + capability tags + provenance metadata (Debenedetti et al. DeepMind 2025).
- **dual-LLM pattern**: Willison's 2023 articulation of privileged-LLM/quarantined-LLM split. CaMeL is the engineering formalization.
- **TaskTracker**: linear-probe on activation deltas (pre- vs post-untrusted-data injection) on decoder LLMs; SaTML 2025.
- **APR**: Attack Prevention Rate (Meta PG2 metric) — % attacks blocked at ≤3% utility loss.
- **AgentDojo**: 97 user tasks × 629 security cases benchmark (Debenedetti et al. NeurIPS 2024) — the de facto agentic benchmark.
- **LLMail-Inject**: 208K adaptive attacks from 839 participants over a realistic RAG-email-assistant pipeline (Microsoft IEEE SaTML 2025).
- **Bhagwatkar saturation finding**: "Are Firewalls All You Need?" NeurIPS 2025 — AgentDojo/ASB/InjecAgent/τ-Bench saturated by 2-firewall defenses; weak-attack pathologies.
- **Instruction Hierarchy**: OpenAI training-time approach — system > developer > user > tool priority (Wallace et al. 2024).

## Verification & limits

- 25/25 entries verified as of 2026-05-23 (post-Sprint 2 Phase E3).
- Body-quote anchors at PDF level for 4 OOD-wall thesis carriers (CaMeL, SecAlign, Meta SecAlign Llama-3.3-70B, Instruction Hierarchy priority ordering) — see `direct-vs-indirect/cache/body_text/` for source PDFs + extractions.
- Cross-classifications carry topic-tailored excerpts; the same source may have different highlighted aspects in `direct-vs-indirect/B2` vs here in `D2`/`D5`.
- Strict-live v2 evidence IDs preserved across all entries (see `../evidence_ledger.yml`, `../cache_manifest.yml`, `../claim_graph.jsonl`).
- This dossier inherits the methodology critique posture from `training-and-evaluation/C4` (Bhagwatkar, Hackett, Nasr "attacker moves second"). Submission ADR-075 unified OOD-drop narrative is referenced via `agentic_bhagwatkar2025firewalls`.

## Attribution

Synthesized from a research dossier maintained by `research_toolkit` (Sprint 2 build, post-Phase E4). Cross-classified from sibling topic dossiers under topic-prefixed bibkeys per Sprint 2 cross-classification convention.
