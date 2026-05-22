# C3. Evaluation metrics + methodology

_8 primary-source entries covering the metric hierarchy used to evaluate prompt-injection detectors and agentic guardrails: accuracy → F1 → AUC-ROC → AUC-PR → TPR@LowFPR → APR → over-defense (NotInject) → ASR-utility coupling (AgentDojo). Each entry's Mechanism field describes what the metric or methodology measures; the Result field describes what it reveals or misses. PromptShield's TPR@LowFPR convention is the load-bearing methodology for the OOD-wall thesis._

## C3.1. Jacob et al. PromptShield (Berkeley)

- **PromptShield: Deployable Detection for Prompt Injection Attacks** — Jacob, Alzahrani, Hu, Alomair, Wagner (ACM CODASPY 2025).
  - **Source:** https://arxiv.org/abs/2501.15145
  - **Code:** —
  - **Mechanism:** Application designers integrate LLMs into products but many LLM-integrated applications are vulnerable to prompt injections; the paper introduces a benchmark for training + evaluating deployable PI detectors [claim_training_and_evaluation_jacob2025promptshield_a1_headline]; two-track benchmark (conversational + application-structured) with TPR@LowFPR reporting convention at 1% / 0.5% / 0.1% / 0.05% FPR [claim_training_and_evaluation_jacob2025promptshield_a2_methodology].
  - **Result:** ACM CODASPY 2025; reveals encoder PI detectors collapse at deployment-grade FPRs (e.g., ProtectAI v2 reports 1.34% TPR @ 0.5% FPR and 0.00% TPR @ 0.1% FPR per the paper's Table 4, where 0.00% is annotated as no threshold achieves the desired FPR aside from 1.0); canonical OOD-collapse evidence for the portfolio's OOD-wall thesis [claim_training_and_evaluation_jacob2025promptshield_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. (no widely-known repo; the paper-side artifact is the HF dataset `hendzh/PromptShield`, § C5.3)

## C3.2. Debenedetti et al. AgentDojo

- **AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents** — Debenedetti et al. (NeurIPS 2024 D&B).
  - **Source:** https://arxiv.org/abs/2406.13352
  - **Code:** <https://github.com/ethz-spylab/agentdojo>
  - **Mechanism:** AI agents combine text-based reasoning with external tool calls; they are vulnerable to PI attacks where data from external tools subverts the agent's intent [claim_training_and_evaluation_debenedetti2024agentdojo_a1_headline]; extensible dynamic environment populated with 97 realistic tasks and 629 security test cases, with attack and defense paradigms instantiated atop the same task set [claim_training_and_evaluation_debenedetti2024agentdojo_a2_methodology].
  - **Result:** NeurIPS 2024 D&B (per project records; not stated in arXiv comments); canonical agentic PI benchmark and one of the four benchmarks Bhagwatkar 2025 (§ C4.2) shows can be saturated by simple firewalls; the 'inverse scaling law' framing (more capable models more attackable) is widely attributed to AgentDojo's findings (unverified body claim, not in abstract) [claim_training_and_evaluation_debenedetti2024agentdojo_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`.

## C3.3. Li et al. InjecGuard / NotInject

- **InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardrail Models** — Li et al. (arXiv 2024).
  - **Source:** https://arxiv.org/abs/2410.22770
  - **Code:** <https://github.com/SaFoLab-WISC/InjecGuard>
  - **Mechanism:** PI attacks pose a critical threat to LLMs; prompt guard models are effective in defense but suffer from over-defense — flagging benign prompts that contain trigger words [claim_training_and_evaluation_li2024injecguard_a1_headline]; InjecGuard + NotInject benchmark explicitly measure over-defense on benign-but-trigger-word prompts; introduces MOF (Mitigating Over-defense for Free) training scheme [claim_training_and_evaluation_li2024injecguard_a2_methodology].
  - **Result:** Releases NotInject benchmark of ~339 benign prompts containing trigger words; over-defense measurement is now a standard component of PI evaluation methodology alongside TPR@LowFPR and APR [claim_training_and_evaluation_li2024injecguard_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`.

## C3.4. Lakera PINT benchmark

- **Lakera's Prompt Injection Test (PINT) — A New Benchmark for Evaluating Prompt Injection Solutions** — Lakera Team (vendor blog, 2024).
  - **Source:** https://www.lakera.ai/product-updates/lakera-pint-benchmark
  - **Code:** <https://github.com/lakeraai/pint-benchmark>
  - **Mechanism:** Third-party PI benchmark deliberately not used as training data, designed against Goodhart's law on public benchmarks [claim_training_and_evaluation_lakera2024pint_a1_announcement].
  - **Result:** Vendor blog announcing PINT; design rationale explicitly cites avoidance of training-data overlap; reusable open-source evaluation harness (PINT GitHub repo) [claim_training_and_evaluation_lakera2024pint_a2_contribution].
  - **Status:** Unverified — title field cross-checked but verification flag not set on retrieval. (vendor blog) — treat numeric claims (e.g., specific input counts) with skepticism unless re-verified. `freshness_tier: volatile`. (recheck after 2026-06-22)

## C3.5. Yi et al. BIPIA

- **Benchmarking and Defending against Indirect Prompt Injection Attacks on Large Language Models** — Yi et al. (KDD 2025).
  - **Source:** https://arxiv.org/abs/2312.14197
  - **Code:** <https://github.com/microsoft/BIPIA>
  - **Mechanism:** Integration of LLMs with external content enables Microsoft Copilot-style apps but introduces vulnerabilities to indirect PI attacks where external content carries malicious instructions [claim_training_and_evaluation_yi2023bipia_a1_headline]; BIPIA — Benchmarking Indirect Prompt Injection — covers 26 attack methods × diverse downstream tasks with both text-and-code attack injections [claim_training_and_evaluation_yi2023bipia_a2_methodology].
  - **Result:** Microsoft KDD 2025; one of the first dedicated indirect-PI benchmarks; appears in firewall benchmarks (Bhagwatkar 2025, § C4.2) [claim_training_and_evaluation_yi2023bipia_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`.

## C3.6. Zhan et al. InjecAgent

- **InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents** — Zhan et al. (ACL 2024 Findings).
  - **Source:** https://arxiv.org/abs/2403.02691
  - **Code:** <https://github.com/uiuc-kang-lab/InjecAgent>
  - **Mechanism:** Recent work has embodied LLMs as agents with tools; external content introduces the risk of indirect prompt injection [claim_training_and_evaluation_zhan2024injecagent_a1_headline]; 1,054 test cases of indirect PI into tool-integrated LLM agents (ReAct-style) with attack outcomes classified as benign / harmful tool-use [claim_training_and_evaluation_zhan2024injecagent_a2_methodology].
  - **Result:** ACL 2024 Findings; canonical agentic indirect-PI benchmark; included in Bhagwatkar's 'Are Firewalls All You Need?' saturation evidence (§ C4.2) [claim_training_and_evaluation_zhan2024injecagent_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`.

## C3.7. Yao et al. τ-bench (tau-bench)

- **τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains** — Yao, Shinn, Razavi, Narasimhan (arXiv 2024).
  - **Source:** https://arxiv.org/abs/2406.12045
  - **Code:** <https://github.com/sierra-research/tau-bench>
  - **Mechanism:** Existing benchmarks do not test language agents on their interaction with human users or ability to follow domain-specific rules, both of which are vital for real-world deployment [claim_training_and_evaluation_yao2024taubench_a1_headline]; realistic tool-agent-user-interaction benchmark in retail and airline domains with multi-turn rollouts and rule-based reward [claim_training_and_evaluation_yao2024taubench_a2_methodology].
  - **Result:** Tests agent capability under realistic constraints; included as one of the four benchmarks in Bhagwatkar 2025 (§ C4.2) saturation analysis [claim_training_and_evaluation_yao2024taubench_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. (uncertain venue — arXiv preprint at retrieval, included as agent benchmark)

## C3.8. Zhang et al. Agent Security Bench (ASB)

- **Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents** — Zhang et al. (ICLR 2025).
  - **Source:** https://arxiv.org/abs/2410.02644
  - **Code:** —
  - **Mechanism:** LLM-based agents using tools + memory mechanisms introduce critical security vulnerabilities [claim_training_and_evaluation_zhang2025asb_a1_headline]; formalizes attack/defense taxonomy for LLM agents with 10 agent scenarios × multiple attack/defense methods [claim_training_and_evaluation_zhang2025asb_a2_methodology].
  - **Result:** ICLR 2025; together with AgentDojo (§ C3.2), InjecAgent (§ C3.6), and τ-Bench (§ C3.7), forms the four benchmarks Bhagwatkar 2025 (§ C4.2) shows can be saturated by simple firewalls [claim_training_and_evaluation_zhang2025asb_a3_contribution].
  - **Status:** Verified (webfetch, 2026-05-22). `freshness_tier: stable`. (no widely-known repo at retrieval; the code repo associated with ASB is not publicized in the arXiv abstract)

8 entries.
