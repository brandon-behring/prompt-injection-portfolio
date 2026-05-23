<!-- AGENT-INDEX: rag-injection-defenses; 18 entries; 2026-05-23 -->

# RAG-injection defenses — Research Synthesis

**Purpose:** Lane 3 dossier — Spotlighting variants applied at the RAG document boundary, retrieval-side provenance + signed-document architectures, content-authentication for RAG, RAG-specific evaluation harnesses (BIPIA per-subset, Azure Document Shield, LLMail-Inject as RAG-email adaptive eval), and production RAG-injection incidents analyzed at the RAG-pipeline layer. Designed primarily for future LLM agents picking up portfolio Lane 3; secondarily for the user authoring Ch 8.

**Primary intended consumer:** future Claude Code / LLM agents grounding reasoning in RAG-injection literature. Secondary: humans.

**Scope:** mid-2023 to mid-2026. 18 entries across 5 sub-areas. ETHICS-locked for production_rag_incidents per ADR-041.

**Coverage:** 18 entries (6 cross-classified from `direct-vs-indirect/` + `detector-landscape/` with `rag_` bibkey prefix; 7 net-new papers; 5 net-new production-incident entries).

**Last updated:** 2026-05-23.

## ⚠️ Scope boundary

This folder is the *RAG-retrieval-boundary* layer of indirect-injection defenses. Companion topics:
- `../direct-vs-indirect/` — Spotlighting + StruQ + SecAlign as general architectural defenses (B2). BIPIA + LLMail-Inject as general agentic benchmarks (B4). EchoLeak + Slack AI as production incidents (B3). This dossier covers the *RAG-specific* application.
- `../agentic-security-architecture/` — Sprint 2 sister topic covering agent-harness defenses. Spotlighting at the agent harness is THERE; Spotlighting at the RAG retrieval boundary is HERE.
- `../detector-landscape/` — Azure Document Shield as a commercial detector entry (A4). This dossier covers it as a RAG-retrieval-boundary defense + benchmark target.
- `../training-and-evaluation/` — methodology critiques (Bhagwatkar saturation, Hackett bypass) apply but aren't re-derived here.

**Cross-classification convention:** entries here use `rag_<original_bibkey>` prefix when re-citing sources from sibling topics. Topic-tailored excerpts highlight the retrieval-boundary application.

## How this is organized

| File | Topic | Anchors |
|---|---|---|
| `01_spotlighting_variants.md` | E1 — Spotlighting 3-variants deep-dive | E1.1-E1.4 |
| `02_retrieval_provenance.md` | E2 — Retrieval-side provenance + signed-document architectures | E2.1-E2.2 |
| `03_content_authentication_rag.md` | E3 — Content authentication for RAG | E3.1-E3.3 |
| `04_rag_evaluation_harness.md` | E4 — RAG-specific evaluation harnesses | E4.1-E4.2 |
| `05_production_rag_incidents.md` | E5 — Production RAG-injection incidents | E5.1-E5.7 |

## Lookup recipes

- **"What's Spotlighting?"** → `01_spotlighting_variants.md` § E1 (Hines et al. Microsoft arXiv 2403.14720 CAMLIS 2024)
- **"What are the 3 Spotlighting variants?"** → `01_spotlighting_variants.md` § E1 (delimiting / datamarking / encoding)
- **"What's the canonical RAG-injection benchmark?"** → `04_rag_evaluation_harness.md` § E4 (BIPIA — Yi et al. Microsoft/USTC arXiv 2312.14197 KDD 2025)
- **"What is LLMail-Inject?"** → `04_rag_evaluation_harness.md` § E4 (208K adaptive attacks in RAG-email pipeline)
- **"What's verifiable retrieval (LLatrieval)?"** → `02_retrieval_provenance.md` § E2 (Li et al. NAACL 2024)
- **"What's the EchoLeak vulnerability?"** → `05_production_rag_incidents.md` § E5 (CVE-2025-32711, M365 Copilot RAG, Aim Labs June 2025)
- **"What's Azure Document Shield?"** → `01_spotlighting_variants.md` § E1 (Microsoft commercial RAG-injection defense; userPromptAnalysis + documentsAnalysis API)
- **"What is D-RAG?"** → `03_content_authentication_rag.md` § E3 (blockchain provenance for RAG sources; Lu et al. 2025)
- **"What is C2PA in the AI context?"** → `03_content_authentication_rag.md` § E3 (Content Credentials standard applied to RAG retrieval)
- **"How did the Slack AI exfiltration work?"** → `05_production_rag_incidents.md` § E5 (PromptArmor Aug 2024; cross-channel RAG-indexed message + Markdown link exfil)
- **"What's the Comet browser indirect injection?"** → `05_production_rag_incidents.md` § E5 (Brave Aug 2025; RAG-style cross-tab content ingestion)
- **"How did Gemini long-term memory poisoning work?"** → `05_production_rag_incidents.md` § E5 (Rehberger Sept 2024; document → memory write → cross-session exfil)
- **"What's Provably Secure RAG (SAG)?"** → `03_content_authentication_rag.md` § E3 (Zhou et al. arXiv 2025)
- **"What's the original ChatGPT Markdown image exfil?"** → `05_production_rag_incidents.md` § E5 (Rehberger / Samoilenko April 2023)
- **"What was the Bing Chat/Copilot webpage manipulation?"** → `05_production_rag_incidents.md` § E5 (Greshake et al. 2023 companion advisory)
- **"How does Spotlighting datamarking differ from encoding?"** → `01_spotlighting_variants.md` § E1 (datamarking near-zero degradation; encoding requires GPT-4-class decoder)
- **"What's the NLI fact-checker for retrieval (Provenance)?"** → `02_retrieval_provenance.md` § E2 (Sankararaman et al. EMNLP 2024 Industry)

## Glossary

- **Spotlighting**: Microsoft's RAG-retrieval-boundary defense (Hines 2024) — 3 variants (delimiting, datamarking, encoding). ASR > 50% → < 2% per abstract.
- **BIPIA**: Benchmark for Indirect Prompt Injection Attacks; 5 application scenarios (Email QA / Web QA / Table QA / Summarization / Code QA) × 6 attack types × 50 goals.
- **LLMail-Inject**: 208K adaptive attacks competition (Abdelnabi et al. Microsoft IEEE SaTML 2025) — RAG-email-assistant pipeline gold standard.
- **EchoLeak**: CVE-2025-32711, CVSS 9.3 — first publicly documented zero-click XPIA in M365 Copilot RAG. Aim Labs disclosure June 2025.
- **C2PA**: Coalition for Content Provenance and Authenticity standard — content credentials applied to RAG sources for retrieval-time trust signal.
- **LLatrieval**: LLM-verified retrieval for verifiable generation; Li et al. NAACL 2024.
- **D-RAG**: blockchain provenance for RAG sources (Lu et al. 2025).
- **Azure Document Shield**: Microsoft's commercial RAG-retrieval-boundary defense, paired with Spotlighting.
- **userPromptAnalysis / documentsAnalysis**: Azure Prompt Shields API split for direct (user) vs indirect (document) injection.

## Verification & limits

- 18/18 entries verified as of 2026-05-23 (Sprint 2 Phase E3).
- Body-quote anchors at PDF level for 6+ carriers (Spotlighting, BIPIA, LLMail-Inject, LLatrieval, D-RAG, SAG) — see `cache/body_text/`.
- ETHICS posture (ADR-041 + ETHICS.md §1): production_rag_incidents documented at vulnerability-class + impact + remediation level only. No exploit chains or attacker payloads in any excerpt or evidence span.
- Strict-live v2 evidence IDs preserved (see `../evidence_ledger.yml`, `../cache_manifest.yml`, `../claim_graph.jsonl`).

## Attribution

Synthesized from a research dossier maintained by `research_toolkit` (Sprint 2 build). Cross-classified from sibling topic dossiers under topic-prefixed bibkeys.
