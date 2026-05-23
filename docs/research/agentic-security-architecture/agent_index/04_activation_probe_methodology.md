# # D4 — Activation-probe methodology beyond TaskTracker

_3 entries covering hidden-state signal class; TaskTracker + InstructDetector + AttentionTracker._


## D4.1. Get my drift? Catching LLM Task Drift with Activation Deltas

- **Get my drift? Catching LLM Task Drift with Activation Deltas** — Abdelnabi et al. (2024).
  - **Source:** https://arxiv.org/abs/2406.00799
  - **Code:** —
  - **Mechanism:** TaskTracker trains linear probes on activation deltas (pre- vs post-untrusted-data injection) of decoder LLMs to detect task drift; reports near-perfect ROC…
  - **Result:** Releases a toolkit of >500K instances across six LLMs (encoder + decoder variants) to support downstream activation-probe reproductions;…
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0020


## D4.2. Defending against Indirect Prompt Injection by Instruction Detection

- **Defending against Indirect Prompt Injection by Instruction Detection** — Wen et al. (2025).
  - **Source:** https://arxiv.org/abs/2505.06311
  - **Code:** https://github.com/MYVAE/Instruction-detection
  - **Mechanism:** InstructDetector extends activation-based detection to indirect prompt injection; reports high OOD detection accuracy on BIPIA and very low ASR after…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0022


## D4.3. Attention Tracker: Detecting Prompt Injection Attacks in LLMs

- **Attention Tracker: Detecting Prompt Injection Attacks in LLMs** — Hung et al. (2025).
  - **Source:** https://arxiv.org/abs/2411.00348
  - **Code:** —
  - **Mechanism:** AttentionTracker proposes detection of prompt injection from attention-head-level patterns rather than hidden-state deltas; introduces a distinct signal class…
  - **Result:** See primary source for details.
  - **Status:** Verified
  - **Evidence:** ev_agentic_security_architecture_0023
