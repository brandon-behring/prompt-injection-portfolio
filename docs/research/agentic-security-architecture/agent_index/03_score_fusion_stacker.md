# # D3 — Score fusion + stacker theory

_5 entries covering meta-learning on per-detector scores; Recall@1%FPR loss; embedding+ML; LogisticStacker._


## D3.1. meta-llama/Llama-Prompt-Guard-2-86M (mDeBERTa-base 86M multilingual prompt-injec

- **meta-llama/Llama-Prompt-Guard-2-86M (mDeBERTa-base 86M multilingual prompt-injection + jailbreak classifier)** — Meta Llama Team (2025).
  - **Source:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
  - **Code:** —
  - **Mechanism:** Llama-Prompt-Guard-2-86M is Meta's mDeBERTa-base multilingual prompt-injection + jailbreak classifier; the model card describes training with a custom…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0015


## D3.2. meta-llama/Llama-Prompt-Guard-2-22M (DeBERTa-xsmall 22M, 75% latency reduction)

- **meta-llama/Llama-Prompt-Guard-2-22M (DeBERTa-xsmall 22M, 75% latency reduction)** — Meta Llama Team (2025).
  - **Source:** https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-22M
  - **Code:** —
  - **Mechanism:** Llama-Prompt-Guard-2-22M is a DeBERTa-xsmall 22M-parameter classifier reporting a substantial latency reduction (~75%) relative to the 86M; relevant to…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0016


## D3.3. Energy-based Out-of-distribution Detection

- **Energy-based Out-of-distribution Detection** — Liu, Wang, Owens & Li (2020).
  - **Source:** https://arxiv.org/abs/2010.03759
  - **Code:** —
  - **Mechanism:** Energy-based Out-of-distribution Detection (NeurIPS 2020) introduces energy scores that better distinguish in- and out-of-distribution samples than softmax…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0017


## D3.4. Embedding-based classifiers can detect prompt injection attacks

- **Embedding-based classifiers can detect prompt injection attacks** — Ayub & Majumdar (2024).
  - **Source:** https://arxiv.org/abs/2410.22284
  - **Code:** —
  - **Mechanism:** Embedding-based classifiers (XGBoost, Random Forest, MLP) operating on OpenAI text-embedding-3-small can detect prompt injection at high accuracy; treated here…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0018


## D3.5. InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardra

- **InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardrail Models** — Li & Liu (2024).
  - **Source:** https://arxiv.org/abs/2410.22770
  - **Code:** https://github.com/leolee99/InjecGuard
  - **Mechanism:** InjecGuard introduces the Mitigating Overdefense Framework (MOF) and the NotInject benchmark, addressing the over-defense pathology where guardrail models flag…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0019
