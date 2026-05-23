# # E4 — RAG-specific evaluation harnesses

_2 entries covering BIPIA per-subset; Azure Document Shield; LLMail-Inject as RAG-email adaptive eval._


## E4.1. Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large La

- **Benchmarking and Defending Against Indirect Prompt Injection Attacks on Large Language Models** — Yi et al. (2023).
  - **Source:** https://arxiv.org/abs/2312.14197
  - **Code:** —
  - **Mechanism:** we introduce the first benchmark for indirect prompt injection attacks, named BIPIA
  - **Result:** Using BIPIA, we evaluate existing LLMs and find them universally vulnerable
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0003


## E4.2. LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge

- **LLMail-Inject: A Dataset from a Realistic Adaptive Prompt Injection Challenge** — Abdelnabi et al. (2025).
  - **Source:** https://arxiv.org/abs/2506.09956
  - **Code:** —
  - **Mechanism:** 208,095 unique attack submissions from 839 participants
  - **Result:** resulting in a dataset of 208,095 unique attack
  - **Status:** Verified
  - **Evidence:** ev_rag_injection_defenses_0005
