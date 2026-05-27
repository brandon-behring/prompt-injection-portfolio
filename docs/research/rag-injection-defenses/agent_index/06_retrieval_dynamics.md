# # E6 — RAG retrieval dynamics (positioning + embedding-space substrate)

_3 entries covering the retrieval-mechanics substrate that indirect injection exploits and that retrieval-side defenses (esp. E2 provenance) must account for: context-position attention effects, the dense-retrieval similarity primitive, and contextual-embedding geometry/anisotropy. Each entry is read through an explicit **injection-relevance** lens — NOT as a general IR/RAG survey._

_Sub-area maps to `research_plan.md` claim_family `rag_retrieval_dynamics` (plan sub-area E5; rendered here as the 6th agent-index file to preserve the existing append-only file/anchor numbering). Scope-expansion added 2026-05-27. Foundational pre-injection-era mechanics — these papers predate the indirect-injection threat model and are cited for the substrate they describe, with the injection reading marked as synthesis (paraphrase) per E-dossier scope._


## E6.1. Lost in the Middle: How Language Models Use Long Contexts

- **Lost in the Middle: How Language Models Use Long Contexts** — Liu et al. (TACL 2024).
  - **Source:** https://arxiv.org/abs/2307.03172
  - **Code:** —
  - **Mechanism:** Measures how language-model performance varies with the position of relevant information in a long input context; reports that "performance can degrade significantly when changing the position of relevant information" [claim_rag_lostinmiddle_position_sensitivity].
  - **Result:** Performance follows a U-shaped curve over context position — "performance is often highest when relevant information occurs at the beginning or end of the input context, and significantly degrades when models must access relevant information in the middle of long contexts" [claim_rag_lostinmiddle_positional_attention].
  - **Injection relevance:** Because attention is U-shaped over context position, a retrieved chunk's *rank* in the assembled prompt changes how strongly it is attended — an injected/poisoned chunk surfaced at the head or tail of the context is more salient (more likely to drive output) than the same chunk buried in the middle. Retrieval-side defenses that re-rank or reposition retrieved spans therefore alter injection efficacy independent of the chunk's content; *where* provenance gating is applied in the context is a defense-design variable, not a detail. (Synthesis / paraphrase reading per E-dossier scope.) [claim_rag_lostinmiddle_chunk_rank_salience]
  - **Status:** Verified. (no widely-known repo)
  - **Evidence:** ev_rag_injection_defenses_0033, ev_rag_injection_defenses_0034, ev_rag_injection_defenses_0035


## E6.2. Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks

- **Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks** — Reimers & Gurevych (EMNLP 2019).
  - **Source:** https://arxiv.org/abs/1908.10084
  - **Code:** —
  - **Mechanism:** Modifies BERT with "siamese and triplet network structures to derive semantically meaningful sentence embeddings that can be compared using cosine-similarity" [claim_rag_sbert_siamese_embeddings].
  - **Result:** Establishes the cosine-comparable sentence-embedding (SBERT) that underlies dense-retrieval similarity scoring — the function a RAG retriever uses to decide which chunk is relevant to a query.
  - **Injection relevance:** SBERT's cosine-comparable embedding is the dense-retrieval similarity primitive. An indirect-injection payload is surfaced into context precisely when its embedding lands near the query embedding under this primitive, so an attacker who optimizes a poisoned chunk's embedding similarity — or a defender who filters / re-ranks on it — operates directly on this mechanism. A retrieval-time trust/provenance signal (E2) is a layer *on top of* this similarity channel, not a replacement for it. (Synthesis / paraphrase reading per E-dossier scope.) [claim_rag_sbert_dense_retrieval_primitive]
  - **Status:** Verified. (no widely-known repo)
  - **Evidence:** ev_rag_injection_defenses_0036, ev_rag_injection_defenses_0037


## E6.3. How Contextual are Contextualized Word Representations? Comparing the Geometry of BERT, ELMo, and GPT-2 Embeddings

- **How Contextual are Contextualized Word Representations? Comparing the Geometry of BERT, ELMo, and GPT-2 Embeddings** — Ethayarajh (EMNLP 2019).
  - **Source:** https://arxiv.org/abs/1909.00512
  - **Code:** —
  - **Mechanism:** Analyzes the geometry of contextual embeddings across model layers and finds that "the contextualized representations of all words are not isotropic in any layer of the contextualizing model" [claim_rag_ethayarajh_anisotropy].
  - **Result:** Contextual embeddings occupy an anisotropic narrow cone, and "upper layers of contextualizing models produce more context-specific representations" [claim_rag_ethayarajh_context_specificity].
  - **Injection relevance:** Because contextual embeddings occupy an anisotropic narrow cone (high baseline cosine similarity between arbitrary tokens), naive cosine thresholds compress the separation between benign and poisoned chunks — bearing on retrieval dedup and on whether a provenance / document-trust-tier signal is even linearly separable in embedding space. Anisotropy is why retrieval-side detectors that rely on raw cosine geometry need calibration (whitening / isotropy correction) before they can distinguish an injected chunk from a legitimately-similar one. (Synthesis / paraphrase reading per E-dossier scope.) [claim_rag_ethayarajh_provenance_separability]
  - **Status:** Verified. (no widely-known repo)
  - **Evidence:** ev_rag_injection_defenses_0038, ev_rag_injection_defenses_0039, ev_rag_injection_defenses_0040
