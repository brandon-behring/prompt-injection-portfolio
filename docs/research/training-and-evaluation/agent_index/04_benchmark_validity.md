# C4. Benchmark validity + methodology critiques

_16 primary-source entries covering systematic critiques of prompt-injection detector benchmark validity. The CodeIntegrity '98% post-mortem' is the most-cited industry self-critique; Bhagwatkar's 'Are Firewalls All You Need?' is the load-bearing academic saturation finding for the portfolio's OOD-wall thesis. Four claims in this file are verbatim-anchored in `evidence_ledger.yml` (Saxe quote + 'speed bump' framing in § C4.1; 'all four public benchmarks' saturation phrase + 'weak attacks, hindering progress' in § C4.2). Sprint 2 adds OR-Bench (Cui et al. ICML 2025) as the canonical general over-refusal benchmark paired with NotInject (§ C3.3) for the over-defense regime._

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

## C4.7. Cui et al. OR-Bench

- **OR-Bench: An Over-Refusal Benchmark for Large Language Models** — Cui et al. (ICML 2025).
  - **Source:** https://arxiv.org/abs/2405.20947
  - **Code:** <https://github.com/justincui03/or-bench>
  - **Mechanism:** Large-scale over-refusal benchmark with 80,000 seemingly-toxic-but-benign prompts spanning 10 rejection categories, plus a harder OR-Bench-Hard-1K subset and an OR-Bench-Toxic comparison set; introduces an automatic over-refusal-prompt generation method [claim_training_and_evaluation_cui2025orbench_a1_abstract]; pairs naturally with InjecGuard NotInject (§ C3.3) — OR-Bench measures general LLM over-refusal regime, NotInject measures PI-detector-specific over-defense regime [claim_training_and_evaluation_cui2025orbench_a2_pairs_with_notinject].
  - **Result:** ICML 2025; evaluates 32 frontier models across 8 model families on the over-refusal regime; cited as the canonical general over-refusal benchmark, complementing the PI-detector-specific NotInject benchmark for the over-defense methodology gap discussed in C3.3 (Li et al. 2024 InjecGuard).
  - **Status:** Verified (webfetch, 2026-05-23). `freshness_tier: stable`. Cross-cut: pairs with `li2024injecguard` (§ C3.3) for the dual over-defense / over-refusal regime.

16 entries.

## C4.8. Benchmark Data Contamination of Large Language Models: A Survey

- **Benchmark Data Contamination of Large Language Models: A Survey** — Xu, Guan, Greene, Kechadi (2024).
  - **Source:** https://arxiv.org/abs/2406.04244
  - **Code:** —
  - **Mechanism:** Benchmark Data Contamination of Large Language Models: A Survey. Reviews how LLMs inadvertently incorporate evaluation benchmark information from training…
  - **Result:** OOD-wall narrative link: a "98% accuracy" on a public benchmark is indistinguishable from contamination-driven memorization absent independent decontamination…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0134

## C4.9. Investigating Data Contamination in Modern Benchmarks for Large Language Models

- **Investigating Data Contamination in Modern Benchmarks for Large Language Models** — Deng, Zhao, Tang, Gerstein, Cohan (2023).
  - **Source:** https://arxiv.org/abs/2311.09783
  - **Code:** —
  - **Mechanism:** Deng et al. NAACL 2024 propose retrieval-based overlap detection + a novel "Testset Slot Guessing" method (mask correct answers; ask model to predict missing…
  - **Result:** Testset Slot Guessing: black-box contamination detection that works on proprietary models (no weights or training-data access required) by exploiting that…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0136

## C4.10. Rethinking Benchmark and Contamination for Language Models with Rephrased Sample

- **Rethinking Benchmark and Contamination for Language Models with Rephrased Samples** — Yang, Chiang, Zheng, Gonzalez, Stoica (2023).
  - **Source:** https://arxiv.org/abs/2311.04850
  - **Code:** —
  - **Mechanism:** Yang et al. 2023 show simple paraphrasing or translation bypasses string-match decontamination; 8-18% of HumanEval benchmark overlaps with pre-training sets…
  - **Result:** Cross-paper claim: paraphrasing-based contamination bypass (Yang 2023) + slot-guessing detection (Deng 2024) jointly imply that PI-detector training corpora…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0138

## C4.11. LiveBench: A Challenging, Contamination-Limited LLM Benchmark

- **LiveBench: A Challenging, Contamination-Limited LLM Benchmark** — White, Dooley, Roberts et al. (2024).
  - **Source:** https://arxiv.org/abs/2406.19314
  - **Code:** —
  - **Mechanism:** LiveBench (White et al. ICLR 2025 Spotlight): a contamination-limited LLM benchmark with frequently-updated questions sourced from recent…
  - **Result:** Methodology: frequent benchmark refresh from recent-only sources mitigates contamination via temporal cutoff rather than detection — a design lesson the…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0140

## C4.12. Proving Test Set Contamination in Black Box Language Models

- **Proving Test Set Contamination in Black Box Language Models** — Oren, Meister, Chatterji, Ladhak, Hashimoto (2023).
  - **Source:** https://arxiv.org/abs/2310.17623
  - **Code:** —
  - **Mechanism:** Oren et al. ICLR 2024 prove black-box contamination by exploiting that all orderings of an exchangeable benchmark should be equally likely under a clean model;…
  - **Result:** Exchangeability proof technique: the test statistic compares model log-likelihoods of the canonical ordering vs. random permutations; statistically significant…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0142

## C4.13. Detecting Pretraining Data from Large Language Models

- **Detecting Pretraining Data from Large Language Models** — Shi, Ajith, Xia, Huang, Liu, Blevins, Chen, Zettlemoyer (2023).
  - **Source:** https://arxiv.org/abs/2310.16789
  - **Code:** —
  - **Mechanism:** Shi et al. ICLR 2024 introduce Min-K% Prob, identifying unseen examples by detecting outlier words with low probabilities; WIKIMIA benchmark (pre/post-training…
  - **Result:** Min-K% Prob: average log-probability of the K% lowest-likelihood tokens in a sequence; contaminated sequences have systematically higher Min-K% than unseen…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0144

## C4.14. NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for eac

- **NLP Evaluation in trouble: On the Need to Measure LLM Data Contamination for each Benchmark** — Sainz, Campos, García-Ferrero, Etxaniz, Lopez de Lacalle, Agirre (2023).
  - **Source:** https://arxiv.org/abs/2310.18018
  - **Code:** —
  - **Mechanism:** Sainz et al. EMNLP 2023 Findings: data contamination causes overestimation of model performance and can lead to flawed scientific conclusions. Propose defining…
  - **Result:** Disclosure norm: every benchmark should publish a contamination assessment for the models evaluated on it; this is the methodological basis for the portfolio's…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0146

## C4.15. Detecting Data Contamination in LLMs via In-Context Learning

- **Detecting Data Contamination in LLMs via In-Context Learning** — Zawalski, Boubdir, Bałazy, Nushi, Ribalta (2025).
  - **Source:** https://arxiv.org/abs/2510.27055
  - **Code:** —
  - **Mechanism:** Zawalski et al. 2025 CoDeC: contamination detection via in-context-learning signal — ICL examples enhance confidence on unknown datasets but diminish it for…
  - **Result:** CoDeC ICL-signal mechanism: contaminated samples are memorized as joint distributions; ICL examples introduce distributional noise that disrupts the memorized…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0148

## C4.16. Are Large Language Models Truly Smarter Than Humans?

- **Are Large Language Models Truly Smarter Than Humans?** — Reddy M, Karmakar (2026).
  - **Source:** https://arxiv.org/abs/2603.16197
  - **Code:** —
  - **Mechanism:** "Are Large Language Models Truly Smarter Than Humans?" (Reddy M & Karmakar 2026) audit six frontier models (GPT-4o, GPT-4o-mini, DeepSeek-R1, DeepSeek-V3,…
  - **Result:** Field-skewed contamination: rates rank from STEM downward through humanities, suggesting that benchmark contamination patterns reflect web-text composition…
  - **Status:** Verified
  - **Evidence:** ev_training_and_evaluation_0150
