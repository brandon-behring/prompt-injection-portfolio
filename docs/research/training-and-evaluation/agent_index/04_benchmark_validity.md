# C4. Benchmark validity + methodology critiques

_6 primary-source entries covering systematic critiques of prompt-injection detector benchmark validity. The CodeIntegrity '98% post-mortem' is the most-cited industry self-critique; Bhagwatkar's 'Are Firewalls All You Need?' is the load-bearing academic saturation finding for the portfolio's OOD-wall thesis. Four claims in this file are verbatim-anchored in `evidence_ledger.yml` (Saxe quote + 'speed bump' framing in § C4.1; 'all four public benchmarks' saturation phrase + 'weak attacks, hindering progress' in § C4.2)._

## C4.1. Jung CodeIntegrity 98% post-mortem

- **98% Accurate and Still Broken (Prompt Injection Classifier Limits for AI Agents)** — Jung (CodeIntegrity blog, Jan 2026).
  - **Source:** https://www.codeintegrity.ai/blog/prompt-injection-limits
  - **Code:** —
  - **Mechanism:** Industry post-mortem on why 98%-accurate PI detectors fail in production — measuring memorization, not generalization [claim_training_and_evaluation_jung2026postmortem_a1_summary]; cites Joshua Saxe's F-score critique verbatim: "85% F-score on your test data is likely more meaningful than a classical ML model scoring 95% but fit to the test distribution" [claim_training_and_evaluation_jung2026postmortem_a2_saxe_fscore].
  - **Result:** Frames the resilience-not-coverage thesis as "speed bump, not a wall" — a verbatim phrasing used by the post-mortem to advocate treating high-F1 PI detectors as defense-in-depth components, not standalone walls [claim_training_and_evaluation_jung2026postmortem_a3_speed_bump]; the most-cited industry self-critique of detector training methodology as of 2026.
  - **Status:** Unverified — title field cross-checked but verification flag not set on retrieval. (vendor blog) — narrative claims sourced from CodeIntegrity blog; Saxe quote + 'speed bump' phrasing are verbatim-anchored in `evidence_ledger.yml` (extraction_method: verbatim_match with sha256 substring + byte-offset anchors). `freshness_tier: volatile`. (recheck after 2026-06-22)

## C4.2. Bhagwatkar et al. Are Firewalls All You Need?

- **Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** — Bhagwatkar et al. (NeurIPS 2025).
  - **Source:** https://arxiv.org/abs/2510.05244
  - **Code:** —
  - **Mechanism:** AI agents are vulnerable to indirect prompt injection attacks; the paper investigates whether existing benchmarks accurately measure detector capability or instead reward narrow saturation [claim_training_and_evaluation_bhagwatkar2025firewalls_a1_abstract]; evaluates simple two-firewall defenses across all four canonical agentic PI benchmarks — verbatim: "across all four public benchmarks: AgentDojo, Agent Security Bench, InjecAgent and tau-Bench" [claim_training_and_evaluation_bhagwatkar2025firewalls_a2_saturation].
  - **Result:** Finds that the four benchmarks are saturable by simple firewall defenses combined with weak attacks; the paper's framing is verbatim: "weak attacks, hindering progress" [claim_training_and_evaluation_bhagwatkar2025firewalls_a3_weak_attacks]; load-bearing for the portfolio's OOD-wall thesis — when 'wins' come from saturation rather than methodological strength, OOD generalization claims become unsound.
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (no widely-known repo) — verbatim_match anchors confirmed in evidence_ledger.yml.

## C4.3. Hackett et al. Bypassing LLM Guardrails

- **Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems** — Hackett et al. (LLMSec 2025).
  - **Source:** https://arxiv.org/abs/2504.11168
  - **Code:** —
  - **Mechanism:** LLM guardrail systems are designed to protect against PI and jailbreak attacks but remain vulnerable to evasion techniques [claim_training_and_evaluation_hackett2025bypassing_a1_headline]; empirical evaluation of 12 character-injection techniques + 8 TextAttack methods against PI / jailbreak guardrails, reporting up to 100% bypass on some commercial systems [claim_training_and_evaluation_hackett2025bypassing_a2_methodology].
  - **Result:** LLMSec 2025; demonstrates near-trivial evasion via Unicode / character-level perturbations on multiple commercial guardrails; the methodology critique is that PI benchmarks measuring 'clean attack' robustness ignore the bypass surface [claim_training_and_evaluation_hackett2025bypassing_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (no widely-known repo at retrieval)

## C4.4. Nasr et al. The Attacker Moves Second

- **The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections** — Nasr et al. (arXiv 2025).
  - **Source:** https://arxiv.org/abs/2510.09023
  - **Code:** —
  - **Mechanism:** How should robustness of LM defenses be evaluated when current defenses against jailbreaks + PI aim to prevent harmful elicitation but the threat model assumes static defenses [claim_training_and_evaluation_nasr2025attackersecond_a1_headline]; argues current PI / jailbreak defenses are static and adaptive attackers with white-box access can bypass them after the fact [claim_training_and_evaluation_nasr2025attackersecond_a2_methodology].
  - **Result:** Critique of evaluation methodology that doesn't model adversarial adaptation; calls for dynamic-attack budgets in evaluation; complements Carlini 2023's (§ C4.6) 'alignment ≠ adversarial robustness' framing [claim_training_and_evaluation_nasr2025attackersecond_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (no widely-known repo) (uncertain venue — arXiv preprint at retrieval)

## C4.5. Choudhary et al. How Not to Detect Prompt Injections / DataFlip

- **How Not to Detect Prompt Injections with an LLM** — Choudhary et al. (ACM AISec 2025).
  - **Source:** https://arxiv.org/abs/2507.05630
  - **Code:** —
  - **Mechanism:** LLM-integrated applications and agents are vulnerable to PI attacks where adversaries embed malicious instructions within seemingly benign input data [claim_training_and_evaluation_choudhary2025detect_a1_headline]; DataFlip = LLM-based PI detection bypass via instruction inversion; demonstrates that DataSentinel-style minimax-trained detectors (§ C2.6) are bypassable despite the game-theoretic training [claim_training_and_evaluation_choudhary2025detect_a2_methodology].
  - **Result:** ACM AISec 2025; companion critique to DataSentinel; methodology lesson — minimax training does not imply attack invariance [claim_training_and_evaluation_choudhary2025detect_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: active`. (no widely-known repo at retrieval)

## C4.6. Carlini et al. Are aligned neural networks adversarially aligned?

- **Are aligned neural networks adversarially aligned?** — Carlini et al. (NeurIPS 2023).
  - **Source:** https://arxiv.org/abs/2306.15447
  - **Code:** —
  - **Mechanism:** Large language models are tuned to be 'helpful and harmless' — to respond helpfully to questions but refuse to answer harmful ones [claim_training_and_evaluation_carlini2023aligned_a1_headline]; demonstrates aligned neural networks (LLMs + multimodal models) remain adversarially exploitable via gradient-based attacks [claim_training_and_evaluation_carlini2023aligned_a2_methodology].
  - **Result:** NeurIPS 2023; foundational reference that alignment ≠ adversarial robustness; cited in PI / jailbreak threat-model framings throughout the portfolio [claim_training_and_evaluation_carlini2023aligned_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. (no widely-known repo at retrieval)

6 entries.
