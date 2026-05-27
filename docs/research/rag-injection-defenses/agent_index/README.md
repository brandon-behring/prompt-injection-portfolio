<!-- AGENT-INDEX: rag-injection-defenses; 21 entries; 2026-05-27 -->

# RAG-injection defenses — Research Synthesis

**Purpose:** Lane 3 dossier — Spotlighting variants applied at the RAG document boundary, retrieval-side provenance + signed-document architectures, content-authentication for RAG, RAG-specific evaluation harnesses (BIPIA per-subset, Azure Document Shield, LLMail-Inject as RAG-email adaptive eval), production RAG-injection incidents analyzed at the RAG-pipeline layer, and the retrieval-mechanics substrate (context-positioning + embedding-space) that indirect injection exploits. Designed primarily for future LLM agents picking up portfolio Lane 3; secondarily for the user authoring Ch 8.

**Primary intended consumer:** future Claude Code / LLM agents grounding reasoning in RAG-injection literature. Secondary: humans.

**Scope:** mid-2019 to mid-2026 (foundational retrieval-mechanics substrate from 2019; injection-defense literature mid-2023 onward). 21 entries across 6 sub-areas. ETHICS-locked for production_rag_incidents per ADR-041.

**Coverage:** 21 entries (6 cross-classified from `direct-vs-indirect/` + `detector-landscape/` with `rag_` bibkey prefix; 7 net-new papers; 5 net-new production-incident entries; 3 net-new retrieval-dynamics substrate papers added 2026-05-27).

**Last updated:** 2026-05-27.

## ⚠️ Scope boundary

This folder is the *RAG-retrieval-boundary* layer of indirect-injection defenses. Companion topics:
- `../direct-vs-indirect/` — Spotlighting + StruQ + SecAlign as general architectural defenses (B2). BIPIA + LLMail-Inject as general agentic benchmarks (B4). EchoLeak + Slack AI as production incidents (B3). This dossier covers the *RAG-specific* application.
- `../agentic-security-architecture/` — Sprint 2 sister topic covering agent-harness defenses. Spotlighting at the agent harness is THERE; Spotlighting at the RAG retrieval boundary is HERE.
- `../detector-landscape/` — Azure Document Shield as a commercial detector entry (A4). This dossier covers it as a RAG-retrieval-boundary defense + benchmark target.
- `../training-and-evaluation/` — methodology critiques (Bhagwatkar saturation, Hackett bypass) apply but aren't re-derived here.

The E6 retrieval-dynamics entries (`06_retrieval_dynamics.md`) are the *retrieval-mechanics substrate* for the injection-defense families, NOT a general IR/RAG survey. They are foundational pre-injection-era papers (2019, 2023) cited only for the mechanism they describe (context-position attention, dense-retrieval similarity primitive, embedding anisotropy); each entry's injection reading is marked as synthesis (paraphrase). Pre-Greshake-2023 retrieval-augmentation literature (classical RAG without injection-threat awareness) and multimodal-RAG injection remain out-of-scope per `research_plan.md`.

**Cross-classification convention:** entries here use `rag_<original_bibkey>` prefix when re-citing sources from sibling topics. Topic-tailored excerpts highlight the retrieval-boundary application.

## How this is organized

| File | Topic | Anchors |
|---|---|---|
| `01_spotlighting_variants.md` | E1 — Spotlighting 3-variants deep-dive | E1.1-E1.4 |
| `02_retrieval_provenance.md` | E2 — Retrieval-side provenance + signed-document architectures | E2.1-E2.2 |
| `03_content_authentication_rag.md` | E3 — Content authentication for RAG | E3.1-E3.3 |
| `04_rag_evaluation_harness.md` | E4 — RAG-specific evaluation harnesses | E4.1-E4.2 |
| `05_production_rag_incidents.md` | E5 — Production RAG-injection incidents | E5.1-E5.7 |
| `06_retrieval_dynamics.md` | E6 — RAG retrieval dynamics (positioning + embedding-space substrate) | E6.1-E6.3 |

> Anchor-numbering note: agent-index file numbers are the folder's own sequential scheme. They diverge by one from `research_plan.md` sub-area numbers because `03_content_authentication_rag.md` was split out of plan sub-area E2. The retrieval-dynamics sub-area is **E5 in `research_plan.md`** (claim_family `rag_retrieval_dynamics`) but rendered as the **6th file / E6 anchors** here to keep the append-only file/anchor numbering stable.

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
- **"What's the 'lost in the middle' effect?"** → `06_retrieval_dynamics.md` § E6.1 (Liu et al. TACL 2024 arXiv 2307.03172; U-shaped positional-attention curve)
- **"Why does a retrieved chunk's rank/position matter for injection?"** → `06_retrieval_dynamics.md` § E6.1 (head/tail chunks more salient than middle; re-ranking alters injection efficacy)
- **"What's Sentence-BERT / SBERT?"** → `06_retrieval_dynamics.md` § E6.2 (Reimers & Gurevych EMNLP 2019 arXiv 1908.10084; the dense-retrieval cosine-similarity primitive)
- **"What is the dense-retrieval similarity primitive a payload exploits?"** → `06_retrieval_dynamics.md` § E6.2 (SBERT cosine embedding; poisoned chunk surfaces when its embedding lands near the query)
- **"What does it mean that contextual embeddings are anisotropic?"** → `06_retrieval_dynamics.md` § E6.3 (Ethayarajh EMNLP 2019 arXiv 1909.00512; narrow cone, high baseline cosine)
- **"Why do retrieval-side cosine detectors need calibration/whitening?"** → `06_retrieval_dynamics.md` § E6.3 (anisotropy compresses benign↔poisoned separation; bears on dedup + trust-signal separability)

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
- **Lost in the Middle**: U-shaped positional-attention finding (Liu et al. TACL 2024) — LM performance is highest when relevant info is at the beginning or end of the context and degrades in the middle. Injection-relevant because a retrieved chunk's rank changes its salience.
- **Sentence-BERT / SBERT**: siamese/triplet sentence-embedding model (Reimers & Gurevych EMNLP 2019) producing cosine-comparable embeddings — the dense-retrieval similarity primitive that surfaces a (possibly poisoned) chunk into context.
- **Anisotropy (embedding)**: contextual embeddings occupy a narrow cone rather than being isotropic (Ethayarajh EMNLP 2019), giving high baseline cosine similarity between arbitrary tokens; bears on retrieval dedup and on whether a trust/provenance signal is linearly separable in embedding space (motivates whitening / isotropy correction).

## Verification & limits

- 21/21 entries verified as of 2026-05-27 (3 retrieval-dynamics substrate entries added 2026-05-27).
- Body-quote anchors at PDF level for 6+ carriers (Spotlighting, BIPIA, LLMail-Inject, LLatrieval, D-RAG, SAG) — see `cache/body_text/`.
- E6 retrieval-dynamics entries: 5 verbatim spans anchored to cached arXiv-abstract snapshots (offsets + sha256 produced via `build_excerpt_anchor.py`, `--occurrence 1` to disambiguate the abstract's triple-duplication in the HTML page); 3 injection-relevance readings are synthesis (paraphrase, extraction_method `paraphrase`, link_confidence 0.60) per E-dossier scope — they interpret the papers' mechanics for indirect injection, not claims made by the original authors.
- ETHICS posture (ADR-041 + ETHICS.md §1): production_rag_incidents documented at vulnerability-class + impact + remediation level only. No exploit chains or attacker payloads in any excerpt or evidence span.
- Strict-live v2 evidence IDs preserved (see `../evidence_ledger.yml`, `../cache_manifest.yml`, `../claim_graph.jsonl`).

## Attribution

Synthesized from a research dossier maintained by `research_toolkit` (Sprint 2 build). Cross-classified from sibling topic dossiers under topic-prefixed bibkeys.


## Sprint 2 audit-trail (Round 1 + 2, 2026-05-23)

**Round 1 — New topic E fresh build verification.** Reviewed all 18 entries (6 cross-classified `rag_*` + 7 net-new papers + 5 production_rag_incidents). Findings: 0 DROP / 0 CORRECT / 1 FLAG (rag_aimlabs2025echoleak — Cato Networks blog returned 212 bytes; verified via NVD CVE-2025-32711 cross-reference instead) / 17 SPOT-CHECK PASSED. All entries except EchoLeak promoted to `status: verified`. EchoLeak retained at `verified` via CVE cross-reference per gather_trace note.

**Round 2 — Body-quote anchoring (6 carriers) + ETHICS posture audit.** Body-anchored carriers: rag_hines2024spotlighting (Spotlighting ASR-reduction abstract claim), rag_yi2025bipia (BIPIA universal-vulnerability + capability-correlation), rag_abdelnabi2025llmailinject (208K adaptive attacks), li2024llatrieval, lu2025drag, zhou2025sag. ETHICS posture maintained: 7 production_rag_incident entries use `extraction_method: paraphrase` or title-only verbatim_match with link_confidence ≤0.80; no exploit chains or attacker payloads in any excerpt or evidence span. 7 orphan evidence_ids stitched into correct bib entries at E3 recovery. Recommendation: Clean — stop here.


## Synthesis-extension log — E6 retrieval-dynamics sub-area (2026-05-27)

**Sub-area / file registered.** Added new agent-index file `06_retrieval_dynamics.md` (3 entries, anchors E6.1-E6.3) for claim_family `rag_retrieval_dynamics` (`research_plan.md` sub-area E5; rendered as the folder's 6th file to keep file/anchor numbering append-only). Entries: `rag_liu2023lostinmiddle` (Lost in the Middle, arXiv 2307.03172, TACL 2024), `rag_reimers2019sentencebert` (Sentence-BERT, arXiv 1908.10084, EMNLP 2019), `rag_ethayarajh2019anisotropy` (anisotropic contextual embeddings, arXiv 1909.00512, EMNLP 2019). Folder count 18 → 21.

**Span-anchoring.** 8 (bullet, atom) pairs added to `pre_selection_manifest.yml` (sel_E_033–sel_E_040), mapping evidence_ids ev_rag_injection_defenses_0033–0040. 5 verbatim spans anchored via `build_excerpt_anchor.py` (each `--occurrence 1`, to disambiguate the abstract's triple-duplication in the arXiv HTML snapshot); offsets + sha256 self-verified by the producer. 3 injection-relevance readings (`claim_rag_lostinmiddle_chunk_rank_salience`, `claim_rag_sbert_dense_retrieval_primitive`, `claim_rag_ethayarajh_provenance_separability`) are synthesis paraphrase (`[0,0]`/`unknown` sentinel, matching the existing sel_E_031/032 synthesis convention; extraction_method `paraphrase`, link_confidence 0.60). No exploit content — foundational mechanics papers read for the injection-defense substrate only. cross_stage 3-arxiv-ID WARN cleared.
