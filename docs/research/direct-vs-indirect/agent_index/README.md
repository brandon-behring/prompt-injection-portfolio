# Direct vs Indirect (XPIA) Prompt Injection — Research Synthesis

<!-- AGENT-INDEX: this folder is a self-contained agent-ready reference for the direct-vs-indirect prompt-injection literature. Read this README first. -->

**Purpose:** indexed primary-source synthesis of the conceptual + practical split between direct (user-supplied) and indirect / XPIA (retrieved-content) prompt injection — threat taxonomies, architectural defenses, production incidents, and indirect-injection benchmarks. Designed for dual consumption: humans skim directly; future LLM agents ground reasoning in the cited primary sources.
**Primary intended consumer:** future LLM agents working on prompt-injection defenses, agentic-AI security audits, or AI-safety portfolio projects under `/Users/brandonbehring/Claude/prompt-injection-portfolio/`. Secondary consumers: human researchers and security practitioners.
**Self-containedness guarantee:** this folder has no hard dependence on sibling files outside the parent `direct-vs-indirect/` directory and its YAML ledgers.
**Scope:** 43 primary entries across 4 sub-areas (B1 threat-models / B2 architectural defenses / B3 production incidents / B4 indirect-injection benchmarks); date range 2022-11 (Perez & Ribeiro "Ignore Previous Prompt") through 2026-01 (ShadowPrompt fix). Strict-live freshness as of 2026-05-27.
**Coverage:** 4 topic files + this README; structured 5-bullet entries (Source / Code / Mechanism / Result / Status / Evidence) with inline atomic-claim IDs.
**Last updated:** 2026-05-27 (+1 B2 entry — ASIDE (Zverev et al. ICLR 2026), embedding-level instruction/data separation via orthogonal rotation of data-token embeddings). Prior: 2026-05-23 (Sprint 2: +9 B1 entries — Perez 2022, Liu 2024 formalizing, Liu 2023 LLM-apps, Shi 2024 JudgeDeceiver, Pasquini 2024 Neural Exec, Evertz 2024 Whispers, Wei 2023 Jailbroken, Rossi 2024 survey, MITRE ATLAS 2024; +4 B2 body-anchored evidence refs for CaMeL/SecAlign/Meta SecAlign/Instruction Hierarchy).

## ⚠️ Scope boundary

This folder covers the **direct-vs-indirect (XPIA) split** and its consequences: threat taxonomies, architectural defenses (Spotlighting, StruQ, SecAlign, ASIDE, CaMeL, Instruction Hierarchy, Jatmo, IsolateGPT, LlamaFirewall, design patterns), production incidents (EchoLeak, Slack AI, ChatGPT plugins, ShadowPrompt, Gemini Trifecta, Comet, Month-of-AI-Bugs), and indirect-injection benchmarks (BIPIA, InjecAgent, AgentDojo, LLMail-Inject, ASB, WASP). It is NOT a complete survey of all prompt-injection literature.

**For adjacent topics, look elsewhere:**

- **Direct-injection detectors** (Llama Guard, Prompt Guard, PromptShield, Lakera Guard, classifier-shaped defenses) — see [`../../detector-landscape/`](../../detector-landscape/) (Topic A sibling dossier). The direct-vs-indirect dossier here covers the **threat split** and **architectural** defenses; the detector-landscape dossier covers the **content-classifier** branch.
- **Training-time defenses and evaluation methodology** (defense-training datasets, evaluation rubrics, red-team training protocols for prompt-injection robustness) — see [`../../training-and-evaluation/`](../../training-and-evaluation/) (Topic C sibling dossier). Some defenses surveyed here (StruQ, SecAlign, Meta SecAlign, Instruction Hierarchy) are training-time interventions; the methodology of *evaluating* such training lives in Topic C.
- **Adversarial-suffix / jailbreak literature** (AdvBench, HarmBench, GCG, AutoDAN) — out of scope here; these are attack benchmarks against base LLMs, not direct-vs-indirect threats.
- **Multimodal indirect injection** (vision-language attacks etc.) — open research thread, no canonical taxonomy yet; omitted from this snapshot.
- **Pre-2023 conceptual ancestors** (SQL injection, XSS, instruction-data confusion in NLP) — referenced in Greshake 2023 but not surveyed here.

**Cross-pipeline overlap convention:** an entry that is methodologically relevant to multiple research dossiers (e.g., SecAlign as a training-time defense vs. an architectural defense) is placed once in its **primary** location and cross-linked from the sibling scope boundary. **Do NOT duplicate entries.** This dossier owns the architectural-defense and incident framings; the detector-landscape and training-and-evaluation dossiers own the classifier and training-methodology framings respectively.

**ETHICS posture (per ADR-041 + ETHICS.md §1):** production-incident entries record vulnerability class, vendor, impact, CVE/CVSS identifier, and remediation status. They do NOT republish attacker payloads, step-by-step exploit chains, or code excerpts that could enable reproduction. Academic critique papers (Bypassing, Are Firewalls, How Not to Detect) are summarized at abstract-and-conclusion level. Readers seeking attack mechanics should consult the linked primary sources directly.

## How this is organized

Section anchors per file use the letter prefix from `../research_plan.md`: `## B1.` in `01_threat_models.md`, `## B2.` in `02_architectural_defenses.md`, `## B3.` in `03_production_incidents.md`, `## B4.` in `04_indirect_benchmarks.md`.

| File | Topic | When to read |
|---|---|---|
| `README.md` (this file) | Hub: scope, lookup recipes, glossary, attribution | Always read first |
| `01_threat_models.md` | B1 — Threat-model taxonomies + foundational framings (Greshake, OWASP LLM01:2025, Willison Dual-LLM, Willison Lethal Trifecta) | You need the conceptual split or want canonical taxonomy references |
| `02_architectural_defenses.md` | B2 — Architectural defenses (Spotlighting, StruQ, SecAlign, Meta SecAlign, ASIDE, CaMeL, Instruction Hierarchy, Jatmo, IsolateGPT, LlamaFirewall, Design Patterns) | You're evaluating defenses beyond content classifiers |
| `03_production_incidents.md` | B3 — Production incidents + adversarial-bypass research (EchoLeak, Month-of-AI-Bugs, ChatGPT image-exfil, Slack AI, ShadowPrompt, Gemini Trifecta, Comet, Hackett bypassing, Bhagwatkar firewalls, Nasr adaptive, Choudhary KAD) | You need real-world impact evidence or want to know what got patched in 2025 |
| `04_indirect_benchmarks.md` | B4 — Indirect-injection benchmarks (BIPIA, InjecAgent, AgentDojo, LLMail-Inject, ASB, WASP) | You're evaluating a defense and need a benchmark |
| `pre_selection_manifest.yml` | Phase 2b Attribute-First contract: span anchors that gate every bullet's evidence ID | You're an auditor verifying claim → source provenance |

The parent `direct-vs-indirect/` directory also holds the upstream YAML artifacts: `bib_ledger.yml`, `evidence_ledger.yml`, `cache_manifest.yml`, `claim_graph.jsonl`, `gather_trace.yml`.

## Lookup recipes

Routes by question type. Each points to a specific file and section anchor.

- **"What's the foundational paper for indirect prompt injection?"** → `01_threat_models.md` § B1 (Greshake et al. 2023, *Not what you've signed up for*).
- **"What's OWASP LLM01:2025?"** → `01_threat_models.md` § B1 (OWASP Gen AI Security Project 2025).
- **"What's the dual-LLM pattern?"** → `01_threat_models.md` § B1 (Willison 2023).
- **"What's the 'lethal trifecta'?"** → `01_threat_models.md` § B1 (Willison 2025).
- **"What's the pre-Greshake canonical reference for direct prompt injection?"** → `01_threat_models.md` § B1 (Perez & Ribeiro 2022, *Ignore Previous Prompt*, NeurIPS ML Safety Workshop).
- **"What's the standard formalization for prompt-injection attack/defense matrices?"** → `01_threat_models.md` § B1 (Liu et al. USENIX Security 2024, *Formalizing and Benchmarking*).
- **"What's HouYi?"** → `01_threat_models.md` § B1 (Liu et al. 2023, black-box attack against 36 LLM-integrated apps, 31 vulnerable).
- **"What's JudgeDeceiver?"** → `01_threat_models.md` § B1 (Shi et al. CCS 2024, optimization-based attack against LLM-as-a-Judge).
- **"What's Neural Exec?"** → `01_threat_models.md` § B1 (Pasquini et al. 2024, learning-based prompt-injection-trigger family).
- **"What's the 'Whispers in the Machine' paper?"** → `01_threat_models.md` § B1 (Evertz et al. DIMVA 2026, confidentiality in agentic systems, 10 agents × 20 tool scenarios × 14 attacks).
- **"What's the Wei et al. jailbreak failure-mode paper?"** → `01_threat_models.md` § B1 (Wei et al. NeurIPS 2023, competing objectives + mismatched generalization).
- **"What's an early survey of prompt-injection attack categories?"** → `01_threat_models.md` § B1 (Rossi et al. 2024, *Early Categorization*).
- **"What's MITRE ATLAS / AML.T0051?"** → `01_threat_models.md` § B1 (MITRE Corporation 2024, adversarial-tactic taxonomy for AI systems).
- **"What's Spotlighting?"** → `02_architectural_defenses.md` § B2 (Hines et al. 2024, Microsoft).
- **"What's StruQ?"** → `02_architectural_defenses.md` § B2 (Chen et al. USENIX 2025, reserved-delimiter SFT).
- **"What's SecAlign?"** → `02_architectural_defenses.md` § B2 (Chen et al. CCS 2025, DPO over secure/insecure pairs).
- **"What's Meta SecAlign / open-source secure LLM?"** → `02_architectural_defenses.md` § B2 (Chen et al. 2025, Llama-3.3-70B).
- **"What's ASIDE / embedding-level instruction-data separation?"** → `02_architectural_defenses.md` § B2 (Zverev et al. ICLR 2026, orthogonal rotation of data-token embeddings).
- **"What's CaMeL?"** → `02_architectural_defenses.md` § B2 (Debenedetti et al. Google DeepMind 2025).
- **"What's the Instruction Hierarchy?"** → `02_architectural_defenses.md` § B2 (Wallace et al. OpenAI 2024).
- **"What's Jatmo?"** → `02_architectural_defenses.md` § B2 (Piet et al. ESORICS 2024, task-specific distillation).
- **"What's IsolateGPT / SecGPT?"** → `02_architectural_defenses.md` § B2 (Wu et al. NDSS 2025).
- **"What's LlamaFirewall?"** → `02_architectural_defenses.md` § B2 (Chennabasappa et al. Meta 2025).
- **"What's the EchoLeak CVE?"** → `03_production_incidents.md` § B3 (Aim Labs / NVD 2025, CVE-2025-32711).
- **"What's the Month of AI Bugs?"** → `03_production_incidents.md` § B3 (Rehberger 2025 announcement + wrap-up).
- **"What was the Slack AI vulnerability?"** → `03_production_incidents.md` § B3 (PromptArmor Aug 2024).
- **"What's ShadowPrompt?"** → `03_production_incidents.md` § B3 (Koi Security 2025-2026 Claude Chrome extension disclosure).
- **"What's the Gemini Trifecta?"** → `03_production_incidents.md` § B3 (Tenable 2025).
- **"What's the Comet indirect-injection vulnerability?"** → `03_production_incidents.md` § B3 (Brave 2025).
- **"What's the 100% guardrail-bypass paper?"** → `03_production_incidents.md` § B3 (Hackett et al. 2025).
- **"What's the 'Are Firewalls All You Need' critique?"** → `03_production_incidents.md` § B3 (Bhagwatkar et al. NeurIPS 2025, benchmark-saturation critique).
- **"Why do we need adaptive-attacker evaluation?"** → `03_production_incidents.md` § B3 (Nasr et al. 2025, *Attacker Moves Second*).
- **"What's BIPIA?"** → `04_indirect_benchmarks.md` § B4 (Yi et al. KDD 2025, first indirect-injection benchmark).
- **"What's InjecAgent?"** → `04_indirect_benchmarks.md` § B4 (Zhan et al. ACL 2024).
- **"What's AgentDojo?"** → `04_indirect_benchmarks.md` § B4 (Debenedetti et al. NeurIPS 2024, de facto agentic IPI benchmark).
- **"What's LLMail-Inject?"** → `04_indirect_benchmarks.md` § B4 (Abdelnabi et al. IEEE SaTML 2025, adaptive-challenge dataset).
- **"What's the largest comprehensive agentic-security benchmark?"** → `04_indirect_benchmarks.md` § B4 (Zhang et al. ICLR 2025, ASB / Agent Security Bench).
- **"What's WASP?"** → `04_indirect_benchmarks.md` § B4 (Evtimov et al. 2025, web-agent benchmark).
- **"What's XPIA?"** → see Glossary below.
- **"What's the canonical defense for an agentic stack in 2026?"** → start with `02_architectural_defenses.md` § B2 (CaMeL or LlamaFirewall), cross-check on `04_indirect_benchmarks.md` § B4 (AgentDojo, ASB), then audit known-bypass evidence in `03_production_incidents.md` § B3.

## Glossary

Canonical term + aliases + one-line definition. Resolves ambiguous lookups without forcing the reader to search.

- **Direct prompt injection (DPI)**: instruction-bearing content supplied via the user-facing prompt channel that attempts to override the system's intended behavior. Compare *Indirect prompt injection*. Greshake et al. 2023 contrast.
- **Indirect prompt injection (IPI, XPIA)**: instruction-bearing content supplied via a non-prompt input channel (retrieved web page, RAG document, email, browser DOM, tool result) that the LLM processes and may follow. Sometimes "Cross-Prompt Injection Attack" (XPIA). Greshake et al. 2023 originating reference.
- **Lethal trifecta**: Willison 2025's shorthand for the three properties that together enable indirect-injection exfiltration: (1) access to private data, (2) exposure to untrusted content, (3) ability to communicate externally.
- **XPIA**: Cross-Prompt Injection Attack — Microsoft's preferred term for indirect prompt injection (used in EchoLeak / Aim Labs disclosure, Spotlighting paper).
- **Spotlighting**: Microsoft's family of prompt-engineering defenses (delimiting / datamarking / encoding) that mark untrusted input so the LLM treats it as data, not instructions. Hines et al. 2024.
- **StruQ**: Reserved-delimiter SFT defense — fine-tunes the LLM so instruction text and data text occupy non-overlapping token spaces. Chen et al. USENIX 2025.
- **SecAlign**: DPO-based prompt-injection defense — trains on (secure, insecure) response pairs. Chen et al. CCS 2025. **Meta SecAlign** extends this to a fully open-source Llama-3.3-70B variant.
- **ASIDE**: Embedding-level instruction/data-separation architecture — applies an orthogonal rotation to data-token embeddings so instructions and data get distinct representations, with no added parameters; improves instruction-data separation and prompt-injection robustness. Zverev et al. ICLR 2026.
- **CaMeL**: Google DeepMind's capability-based isolation defense — extracts control and data flow from the trusted query so untrusted data cannot impact program flow. Debenedetti et al. 2025.
- **Instruction Hierarchy**: OpenAI's training-time defense that explicitly orders system > developer > user > tool instructions; the model learns to honor that priority. Wallace et al. 2024.
- **Jatmo**: Task-specific distillation defense — distills the base instruction-tuned LLM into a narrower task model that never sees free-form instructions at inference. Piet et al. ESORICS 2024.
- **IsolateGPT / SecGPT**: Execution-isolation architecture for LLM-based agentic systems — sandboxes each app/extension and mediates inter-app communication. Wu et al. NDSS 2025.
- **LlamaFirewall**: Meta's open-source guardrail framework bundling input/output classifiers, tool-call constraints, and policy enforcement at the agent layer. Chennabasappa et al. 2025.
- **Dual-LLM pattern**: Privileged LLM (sees trusted inputs, emits tool calls) plus quarantined LLM(s) (process untrusted content but cannot directly trigger tool calls). Willison 2023.
- **EchoLeak / CVE-2025-32711**: First publicly documented zero-click XPIA in production GenAI (Microsoft 365 Copilot, June 2025, Aim Labs disclosure, CVSS 9.3).
- **Month of AI Bugs**: Rehberger's August 2025 daily-disclosure campaign of indirect-injection and related agentic-AI vulnerabilities across major coding assistants. embracethered.com.
- **ShadowPrompt**: Koi Security's DOM-XSS-class indirect-injection disclosure against the Anthropic Claude Chrome extension (fixed v1.0.41).
- **Gemini Trifecta**: Tenable's 2025 disclosure of three indirect-injection vulnerabilities across Gemini Cloud Assist, Search Model, and Browsing.
- **BIPIA**: First standardized indirect-injection benchmark; 5 application scenarios × 6 attack subtypes. Yi et al. KDD 2025.
- **InjecAgent**: Tool-use-focused IPI benchmark; 1,054 cases × 17 user tools × 62 attacker tools per research_plan. Zhan et al. ACL 2024.
- **AgentDojo**: Dynamic agent benchmark; 97 user tasks × 629 security cases across banking/Slack/travel/workspace scenarios; extensible environment design. Debenedetti et al. NeurIPS 2024.
- **LLMail-Inject**: Adaptive-attacker challenge benchmark; 208K attacks from 839 participants per research_plan. Abdelnabi et al. IEEE SaTML 2025.
- **ASB / Agent Security Bench**: Comprehensive agentic-security benchmark; 10 scenarios × 10 agents × 400+ tools × 27 attack/defense types × 7 metrics. Zhang et al. ICLR 2025.
- **WASP**: Benchmark for web-agent security against prompt injection (Perplexity Comet, Claude Chrome extension, etc.). Evtimov et al. 2025.
- **KAD (known-answer detection)**: Class of LLM-based content-classifier detectors that observe an LLM's output to a benign question to classify input as clean or contaminated; shown structurally bypassable by Choudhary et al. 2025.
- **Adaptive attacker**: Evaluation methodology (Nasr et al. 2025) where the attacker explicitly modifies their attack strategy to counter a known defense, in contrast to fixed-attack benchmarks. The 2025-2026 community consensus is that adaptive evaluation is the new methodological standard.

## Verification & limits

- Citations resolved as of 2026-05-22.
- Strict-live v2.2 evidence IDs: **present**. See `../evidence_ledger.yml`, `../cache_manifest.yml`, `../claim_graph.jsonl`, and `pre_selection_manifest.yml` in this folder.
- Every claim-bearing bullet cites at least one `claim_<descriptor>` atom whose span anchor is committed in `pre_selection_manifest.yml`. Validator (`validators/pre_selection_manifest.py`) rejects any cited claim_id whose anchor isn't in the manifest — post-hoc rationalization is structurally impossible.
- Quantitative claims in 5-bullet prose are either (a) verified against the primary source's abstract (most cases) or (b) sourced from the research plan's `Notes:` line with the qualifier "per the research plan" or "per ADR-041" (when the number is not directly verifiable from the cached source).
- Production-incident entries follow the ETHICS posture documented in the scope-boundary callout: vulnerability class + impact + remediation status only; no attacker payload reproduction. Re-check vendor advisories and CVE entries directly for current patch status.
- Active-tier entries (90-day freshness) carry an explicit `recheck after 2026-08-20` flag — re-verify before relying on a vendor disclosure or 2025-2026 paper claim past that date.
- This synthesis is a snapshot. The agentic-security field is moving rapidly; expect new disclosures and benchmarks monthly. Schedule a freshness-audit pass every quarter for active-tier entries.
- Audit-trail placeholder for `/dossier-audit` results: see audit notes below.

**Independent audit, round 1 (2026-05-22):** Complementary-scope review pass focused on 2025-26 arXiv entries + EchoLeak / Month-of-AI-Bugs / production-incident disclosure freshness (B3 + recent B1/B2/B4 papers). Findings: 0 dropped, 1 corrected, 2 flagged. Typical discrepancies: ShadowPrompt author affiliation + publication date drift ("December 2025–January 2026" → "March 2026, Koi Research"); Wallace 2024 instruction-priority ordering (system > developer > user > tool) is a paper-body claim not in the abstract; Meta SecAlign abstract names Meta-SecAlign-70B / Meta-SecAlign-8B but does NOT name Llama-3.3-70B as the base model. CVSS 9.3 for EchoLeak is the MSRC-assigned score (NVD adjudicated 7.5); the dossier's "CVSS 9.3" matches the widely-cited MSRC + Aim Labs primary disclosure. Disclosure-level review only per ADR-041; operational details intentionally not cross-referenced. Recommendation: re-run with focus on GitHub code links + reproducibility claims for B2 architectural defenses.

**Independent audit, round 2 (2026-05-22):** Complementary-scope review pass focused on GitHub code links + reproducibility claims for B2 architectural defenses. Prior rounds covered: B3 production_incidents + B1/B4 paper freshness (round 1). Findings: 0 dropped, 3 corrected, 0 flagged. Typical discrepancy: three B2 entries (Jatmo, IsolateGPT/SecGPT, LlamaFirewall) carried `Code: —` despite official public repos existing — repos verified to resolve and correspond to the cited paper: `github.com/wagner-group/prompt-injection-defense` (Jatmo), `github.com/llm-platform-security/SecGPT` (IsolateGPT, NDSS 2025), `github.com/meta-llama/PurpleLlama/tree/main/LlamaFirewall` (LlamaFirewall). All 7 originally-cited code URLs (StruQ, SecAlign, CaMeL, InjecAgent, AgentDojo, ASB, WASP) HEAD-resolve and correspond to the official paper implementations. CaMeL's "77% provably-secure on AgentDojo (vs. 84% undefended)" reproducibility claim verified in the abstract. Recommendation: clean — stop here, or if a round 3 is desired, focus on stable-tier (2024) entry freshness (Greshake / dual-LLM blog) or pre_selection_manifest span-anchor integrity.

## Attribution

Synthesized from a research dossier maintained by `research_toolkit` v2.2 (`~/Claude/research_toolkit/`). URLs link to primary sources (arXiv abstracts, vendor security advisories, NIST NVD, conference proceedings). Cached source-text blobs live at `~/Claude/research_cache/` and are not republished here. Phase 2 evidence_ledger paraphrased 7 entries for ETHICS content-lock; this agent-index extends that posture into the 5-bullet prose (see `03_production_incidents.md` for the affected entries).


## Sprint 2 audit-trail (Round 3 + 4, 2026-05-23)

**Round 3 — Sprint 2 new-entry verification.** Verified the 9 new threat-model + foundational direct-injection entries (Perez & Ribeiro, Liu USENIX 2024, Liu LLM-apps, Shi LLM-judge, Pasquini Neural Exec, Evertz Whispers, Wei Jailbroken, Rossi survey, MITRE ATLAS). Findings: 0 DROP / 0 CORRECT / 0 FLAG / 9 SPOT-CHECK PASSED. All 9 verified via WebFetch + abstract anchor.

**Round 4 — Body-quote anchor integrity.** Verified 4 body-quote anchors added at E3 against cached PDF text + sha256 spans. Carriers: debenedetti2025camel (CaMeL 77% provable security on AgentDojo v2), chen2025secalign (SecAlign DPO ASR reduction), chen2025metasecalign (Llama-3.3-70B input-role separation — resolves Sprint 1 Round 1 FLAG), wallace2024instructionhierarchy (system > developer > user > tool priority — resolves Sprint 1 Round 1 FLAG). Findings: 0 DROP / 0 CORRECT / 0 FLAG / 4 SPOT-CHECK PASSED. Body sha256 spans recompute clean. Recommendation: Clean — stop here.
