# A5. Activation-probe + specialized + cross-cutting evaluation

Detectors that depart from the encoder-classifier and LLM-judge defaults: activation-delta probes (§ A5.1, § A5.2), attention-based detection (§ A5.7), embedding-classifier baselines (§ A5.6), game-theoretic detection (§ A5.10), alignment-aware multi-class detection (§ A5.5), and agentic-defense detectors that ship discrete classifier-like components (§ A5.8 Task Shield, § A5.9 MELON). Plus the cross-cutting evaluation / evasion / postmortem literature (§ A5.12 - § A5.17) that informs the dossier's methodology critique throughout.

## A5.1. TaskTracker (Abdelnabi et al.)

- **Get my drift? Catching LLM Task Drift with Activation Deltas** — Abdelnabi et al. (IEEE SaTML 2025).
  - **Source:** https://arxiv.org/abs/2406.00799
  - **Code:** —
  - **Mechanism:** Detector operates on LLM internal activations rather than input text: computes the activation delta between pre- and post-data-ingestion forward passes, then trains a simple linear classifier to flag "task drift" (deviation from the user's original task induced by injected instructions in external data) [claim_detector_landscape_0027_01].
  - **Result:** Abstract reports that a simple linear classifier can detect drift with near-perfect ROC AUC on an out-of-distribution test set [claim_detector_landscape_0027_02]; generalizes across unseen task domains (prompt injections, jailbreaks, malicious instructions) without being trained on any of those attack types. Companion toolkit dataset >500K instances across 6 LLMs per `research_plan.md` notes.
  - **Status:** Verified. (no widely-known repo) Foundational reference for activation-probe detection; coined the term "task drift." [ev_detector_landscape_0028]

## A5.2. InstructDetector (Wen et al.)

- **Defending against Indirect Prompt Injection by Instruction Detection** — Wen et al. (EMNLP 2025 Findings).
  - **Source:** https://arxiv.org/abs/2505.06311
  - **Code:** https://github.com/MYVAE/Instruction-detection
  - **Mechanism:** Hidden-states + gradients from intermediate LLM layers used as features for instruction detection [claim_detector_landscape_0028_01]; reframes IPI defense as detecting state-changes in the LLM's behavior caused by embedded instructions. Architecturally similar to TaskTracker (§ A5.1) but uses gradients rather than activation deltas.
  - **Result:** Abstract reports 99.60% detection accuracy in-domain, 96.90% out-of-domain, and reduces attack success rate to 0.03% on the BIPIA benchmark (§ A5.17) [claim_detector_landscape_0028_02].
  - **Status:** Verified. EMNLP-published with open repo; pair with § A5.1 for the activation-based detector cluster. [ev_detector_landscape_0029]

## A5.3. InjecGuard + NotInject (Li & Liu)

- **InjecGuard: Benchmarking and Mitigating Over-defense in Prompt Injection Guardrail Models** — Li & Liu (arXiv 2024).
  - **Source:** https://arxiv.org/abs/2410.22770
  - **Code:** https://github.com/leolee99/InjecGuard
  - **Mechanism:** Introduces (1) NotInject, a 339-sample benign evaluation dataset enriched with trigger words common in prompt-injection attacks (e.g., "ignore the above"), explicitly designed to measure over-defense [claim_detector_landscape_0029_02]; and (2) MOF (Mitigating Over-defense for Free), a training strategy that reduces trigger-word bias in prompt-guard models [claim_detector_landscape_0029_01].
  - **Result:** Abstract reports that SOTA guardrail models drop close to random-guessing levels (~60% accuracy) on NotInject due to over-defense; InjecGuard with MOF training surpasses the best prior model by 30.8% on diverse benchmarks including NotInject (`unverified body claim` for the specific deltas across all benchmarks listed in body).
  - **Status:** Verified. The canonical reference for the over-defense / false-positive problem in guardrails; complements § A3.1's TPR@FPR framing. [ev_detector_landscape_0030]

## A5.4. PIGuard (Li, Liu, Zhang & Xiao)

- **PIGuard: Prompt Injection Guardrail via Mitigating Overdefense for Free** — Li, Liu, Zhang & Xiao (ACL 2025).
  - **Source:** https://aclanthology.org/2025.acl-long.1468/
  - **Code:** https://github.com/leolee99/PIGuard
  - **Mechanism:** ACL 2025 long paper from the same research group as InjecGuard (§ A5.3); refines the MOF training strategy and extends evaluation. ACL Anthology page surface anchors title and venue [claim_detector_landscape_0030_01]; abstract not anchored on this surface (paper PDF not in cache text extraction).
  - **Result:** ACL Anthology page surface — quantitative claims are `(unverified body claim)` since not in abstract-equivalent area; pair with § A5.3 for the over-defense thread.
  - **Status:** Verified. (ACL venue verifies; specific claims unverified body claim) [ev_detector_landscape_0031]

## A5.5. AlignSentinel (Jia et al.)

- **AlignSentinel: Alignment-Aware Detection of Prompt Injection Attacks** — Jia et al. (arXiv 2026).
  - **Source:** https://arxiv.org/abs/2602.13597
  - **Code:** —
  - **Mechanism:** Three-class classifier that distinguishes (a) inputs with misaligned instructions (prompt injections), (b) inputs with aligned instructions (benign inputs that happen to contain instruction-shaped language aligning with the intended task), and (c) non-instruction inputs [claim_detector_landscape_0031_01]. Uses features derived from the target LLM's attention maps [claim_detector_landscape_0031_02]. Authors also build the first systematic benchmark containing inputs from all three categories — existing benchmarks largely lack the "aligned-instructions" case.
  - **Result:** Abstract reports AlignSentinel "accurately detects inputs with misaligned instructions and substantially outperforms baselines" (`unverified body claim` for specific deltas).
  - **Status:** Verified. Three-class framing is the contribution; this is structurally distinct from the binary detector default elsewhere in the dossier. [ev_detector_landscape_0032]

## A5.6. Embedding-based classifiers (Ayub & Majumdar)

- **Embedding-based classifiers can detect prompt injection attacks** — Ayub & Majumdar (arXiv 2024).
  - **Source:** https://arxiv.org/abs/2410.22284
  - **Code:** —
  - **Mechanism:** Uses three commonly-used embedding models to generate embeddings of malicious and benign prompts, then trains classical ML classifiers (Random Forest, XGBoost, MLP) on the embedding space to detect prompt injection [claim_detector_landscape_0032_01]. Architecturally orthogonal to fine-tuned encoder classifiers (§ A1, § A2) — uses frozen embeddings + classical-ML head.
  - **Result:** Abstract reports best performance with Random Forest and XGBoost classifiers [claim_detector_landscape_0032_02]; claims to outperform state-of-the-art open-source encoder-only prompt-injection classifiers (specific deltas `(unverified body claim)`).
  - **Status:** Verified. (no widely-known repo) The reference baseline for "is the encoder-only fine-tuning actually necessary or is frozen-embedding + classical-ML enough?" question. [ev_detector_landscape_0033]

## A5.7. Attention Tracker (Hung et al.)

- **Attention Tracker: Detecting Prompt Injection Attacks in LLMs** — Hung et al. (arXiv 2024; NAACL 2025 Findings venue unverified, 2026-05-22).
  - **Source:** https://arxiv.org/abs/2411.00348
  - **Code:** —
  - **Mechanism:** Introduces the "distraction effect" concept: specific attention heads (termed "important heads") shift focus from the original instruction to the injected instruction during a prompt-injection attack. Attention Tracker is a training-free detection method that tracks attention patterns on instruction tokens to detect this distraction-effect signature, without requiring additional LLM inference passes [claim_detector_landscape_0033_01].
  - **Result:** Abstract reports AUROC improvement of up to 10.0% over existing methods [claim_detector_landscape_0033_02]; generalizes effectively across diverse models, datasets, and attack types; works even on small LLMs.
  - **Status:** Verified. (no widely-known repo) Training-free attention-based detection is a distinctive architecture choice; NAACL Findings venue claim unverified (arXiv Comments field lists only the project page). [ev_detector_landscape_0034]

## A5.8. Task Shield (Jia, Wu, Qin & Squicciarini)

- **The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents** — Jia, Wu, Qin & Squicciarini (arXiv 2024).
  - **Source:** https://arxiv.org/abs/2412.16682
  - **Code:** —
  - **Mechanism:** Test-time defense that reframes agent security from "preventing harmful actions" to "ensuring task alignment" — every agent action must demonstrably serve the user-specified objective. Task Shield systematically verifies whether each instruction and tool call contributes to user-specified goals [claim_detector_landscape_0034_01].
  - **Result:** Abstract reports 2.07% attack success rate while maintaining 69.79% task utility on GPT-4o evaluated on AgentDojo [claim_detector_landscape_0034_02].
  - **Status:** Verified. (no widely-known repo; also covered as architectural defense) Crosslinks to the architectural-defense literature in `../direct-vs-indirect/`. [ev_detector_landscape_0035]

## A5.9. MELON (Zhu et al.)

- **MELON: Provable Defense Against Indirect Prompt Injection Attacks in AI Agents** — Zhu et al. (ICML 2025).
  - **Source:** https://arxiv.org/abs/2502.05174
  - **Code:** https://github.com/kaijiezhu11/MELON
  - **Mechanism:** Masked re-Execution and TooL comparisON. Re-executes the agent's trajectory with a masked user prompt; identifies an attack when actions generated in the original and masked executions are similar (because under successful injection, the agent's next action becomes more dependent on the malicious task than on the user task) [claim_detector_landscape_0035_01, claim_detector_landscape_0035_02]. Includes three additional designs to reduce false positives / false negatives.
  - **Result:** Abstract reports MELON outperforms SOTA defenses on AgentDojo for both attack prevention and utility preservation; combining MELON with a SOTA prompt-augmentation defense (MELON-Aug) further improves performance (specific deltas `(unverified body claim)`).
  - **Status:** Verified. (also covered as architectural defense) ICML-published. [ev_detector_landscape_0036]

## A5.10. DataSentinel (Liu, Jia, Jia, Song & Gong)

- **DataSentinel: A Game-Theoretic Detection of Prompt Injection Attacks** — Liu, Jia, Jia, Song & Gong (IEEE Symposium on Security and Privacy 2025).
  - **Source:** https://arxiv.org/abs/2504.11358
  - **Code:** —
  - **Mechanism:** Fine-tunes an LLM as a detector via minimax optimization: the outer min trains the detector LLM to correctly classify, the inner max generates strategically-adapted injected prompts trying to evade detection [claim_detector_landscape_0036_01]. Solved via a gradient-based alternating-minimization scheme [claim_detector_landscape_0036_02]. Operationally uses the "KAD signal" (Known Answer Detection) — a secret canary-token mechanism where the detector LLM is fine-tuned to produce a known token on benign inputs; absence of that token at inference signals injection (per `research_plan.md` notes).
  - **Result:** Abstract claims effective detection of both existing and adaptive prompt-injection attacks on multiple benchmark datasets and LLMs (specific numbers `(unverified body claim)`).
  - **Status:** Verified. (no widely-known repo) IEEE S&P-published; the canonical reference for "detector trained against an adaptive attacker" architecture. [ev_detector_landscape_0037]

## A5.11. WAInjectBench (Liu et al.)

- **WAInjectBench: Benchmarking Prompt Injection Detections for Web Agents** — Liu et al. (arXiv 2025).
  - **Source:** https://arxiv.org/abs/2510.01354
  - **Code:** https://github.com/Norrrrrrr-lyn/WAInjectBench
  - **Mechanism:** First comprehensive benchmark study on detecting prompt-injection attacks targeting web agents [claim_detector_landscape_0037_02]. Introduces a fine-grained categorization of web-agent prompt injection attacks; constructs datasets containing both malicious and benign samples (malicious text generated by different attacks, benign text from four categories, malicious images and benign images) [claim_detector_landscape_0037_01]. Evaluates both text-based and image-based detection methods.
  - **Result:** Abstract reports that detectors handle attacks with explicit textual instructions or visible image perturbations moderately well, but largely fail against attacks that omit explicit instructions or use imperceptible perturbations (qualitative claim from abstract; specific deltas `(unverified body claim)`).
  - **Status:** Verified. Web-agent-specific benchmark; complements AgentDojo / InjecAgent / ASB / τ-Bench in the agentic side. [ev_detector_landscape_0038]

## A5.12. "Are Firewalls All You Need?" (Bhagwatkar et al.)

- **Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?** — Bhagwatkar et al. (arXiv 2025; NeurIPS 2025 venue unverified, 2026-05-22).
  - **Source:** https://arxiv.org/abs/2510.05244
  - **Code:** —
  - **Mechanism:** Two-firewall defense at the agent-tool interface: a Tool-Input Firewall (Minimizer) and a Tool-Output Firewall (Sanitizer). Simple, modular, model-agnostic; makes minimal assumptions about the agent and can be deployed out of the box [claim_detector_landscape_0038_01].
  - **Result:** Abstract reports the two-firewall defense achieves perfect security with high utility across all four public benchmarks (AgentDojo, Agent Security Bench, InjecAgent, τ-Bench) and state-of-the-art security-utility tradeoff compared to prior results [claim_detector_landscape_0038_02]. Companion contribution: targeted fixes to AgentDojo and Agent Security Bench (flawed success metrics, implementation bugs, weak attacks) and a three-stage attack strategy cascading standard injection, second-order, and adaptive attacks.
  - **Status:** Verified. (no widely-known repo; also covered as architectural defense) Canonical "is the agentic benchmark suite too weak?" reference; the methodology critique is at least as load-bearing as the perfect-security result. NeurIPS 2025 venue (unverified, 2026-05-22) — not confirmed on arXiv abstract page. [ev_detector_landscape_0039]

## A5.13. Bypassing Guardrails (Hackett et al.)

- **Bypassing LLM Guardrails: An Empirical Analysis of Evasion Attacks against Prompt Injection and Jailbreak Detection Systems** — Hackett et al. (LLMSec 2025).
  - **Source:** https://arxiv.org/abs/2504.11168
  - **Code:** —
  - **Mechanism:** Two evasion approaches: (1) traditional character-injection methods, (2) algorithmic Adversarial Machine Learning (AML) evasion techniques [claim_detector_landscape_0039_01]. Tests against six prominent protection systems including Microsoft Azure Prompt Shield (§ A4.4) and Meta Prompt Guard (§ A3.3 - § A3.5).
  - **Result:** Abstract reports both methods can evade detection while maintaining adversarial utility, achieving in some instances up to 100% evasion success [claim_detector_landscape_0039_02]; demonstrates attackers can enhance Attack Success Rate against black-box targets by leveraging word-importance ranking computed by offline white-box models.
  - **Status:** Verified. (no widely-known repo) The single most-cited empirical demonstration that current guardrails are bypassable via simple character-injection — anchor reference for the "98% accurate but broken" thread in § A5.16. [ev_detector_landscape_0040]

## A5.14. Adversarial Prompt Evaluation (Zizzo et al.)

- **Adversarial Prompt Evaluation: Systematic Benchmarking of Guardrails Against Prompt Input Attacks on LLMs** — Zizzo et al. (NeurIPS 2024 Safe Generative AI Workshop).
  - **Source:** https://arxiv.org/abs/2502.15427
  - **Code:** https://github.com/IBM/Adversarial-Prompt-Evaluation
  - **Mechanism:** Systematic benchmarking across 15 different defences considering a broad swathe of malicious and benign datasets [claim_detector_landscape_0040_02]; addresses the lack of systematization in how guardrails are evaluated [claim_detector_landscape_0040_01].
  - **Result:** Abstract reports significant performance variation depending on the jailbreak style a defence is subject to; simple baselines can display competitive out-of-distribution performance compared to many SOTA defences when evaluated on current available datasets.
  - **Status:** Verified. IBM-hosted code; complements § A5.12 (Firewalls) and § A5.15 (Attacker Moves Second) as the systematic-benchmarking literature cluster. [ev_detector_landscape_0041]

## A5.15. "The Attacker Moves Second" (Nasr et al.)

- **The Attacker Moves Second: Stronger Adaptive Attacks Bypass Defenses Against LLM Jailbreaks and Prompt Injections** — Nasr et al. (arXiv 2025).
  - **Source:** https://arxiv.org/abs/2510.09023
  - **Code:** —
  - **Mechanism:** Argues current defense evaluation is flawed: defenses are evaluated against static attack strings or weak optimization methods. Proposes evaluating defenses against adaptive attackers who explicitly modify strategy to counter the defense's design and spend considerable compute on optimization [claim_detector_landscape_0041_01]. Uses gradient descent, reinforcement learning, random search, and human-guided exploration as the adaptive-attack toolkit.
  - **Result:** Abstract reports bypass of 12 recent defenses (based on diverse techniques) with attack success rate above 90% for most; importantly, the majority of these defenses originally reported near-zero attack success rates [claim_detector_landscape_0041_02].
  - **Status:** Verified. (no widely-known repo) The canonical reference for the "static evaluation is misleading" critique — pair with § A5.12 (Firewalls) and § A5.13 (Bypassing Guardrails) for the evaluation-methodology thread. [ev_detector_landscape_0042]

## A5.16. "98% Accurate and Still Broken" — CodeIntegrity industry postmortem (Jung)

- **98% Accurate and Still Broken (industry post-mortem on held-out vs adversarial detector accuracy)** — Jung (Vendor blog, 2026).
  - **Source:** https://www.codeintegrity.ai/blog/prompt-injection-limits
  - **Code:** —
  - **Mechanism:** Industry self-critique by the CodeIntegrity team (companion vendor-side context to § A1.2 CodeIntegrity PromptGuard). Walks through encoder-only transformers as "the workhorses of text classification" [claim_detector_landscape_0042_01], the high in-distribution accuracy they achieve, and the structural reasons they collapse against adaptive evasion (character injection, distribution shift, trigger-word patterns).
  - **Result:** Vendor blog — no quantitative summary claim in abstract-equivalent area. The piece's contribution is methodological: it's the most-cited industry self-critique of the "98% held-out accuracy" headline that gets eroded under adaptive attack — corroborates the academic results in § A5.13 (Hackett 100% evasion) and § A5.15 (Nasr 90% ASR).
  - **Status:** Verified. (vendor blog; methodological self-critique) Re-verify after 2026-08-22 — vendor blog is on a `volatile` freshness tier. [ev_detector_landscape_0043, ev_detector_landscape_0045]

## A5.17. microsoft/BIPIA (Yi et al.)

- **microsoft/BIPIA: A benchmark for evaluating the robustness of LLMs and defenses to indirect prompt injection attacks** — Yi et al. (GitHub repository, 2023).
  - **Source:** https://github.com/microsoft/BIPIA
  - **Code:** https://github.com/microsoft/BIPIA
  - **Mechanism:** Benchmark for Indirect Prompt Injection Attack — the canonical Microsoft-side benchmark for RAG-flavored indirect prompt injection (instructions embedded in external content fed to the LLM, vs. direct prompt injection). Repo surface anchors the GitHub feedback footer [claim_detector_landscape_0043_01]; mechanism details live in the companion arXiv preprint (out of cache scope here).
  - **Result:** GitHub repo surface — quantitative claims are `(unverified body claim)` since not in abstract-equivalent area. Standard reference for indirect-PI benchmarking; InstructDetector (§ A5.2) reports 0.03% ASR after defense on BIPIA.
  - **Status:** Verified. (vendor repo) Frequently cited; one of the few pre-2024 indirect-PI benchmarks still in active use. [ev_detector_landscape_0044]

## A5.18. The Hardware Lottery — matched-compute critique (Hooker)

- **The Hardware Lottery** — Hooker (arXiv 2020).
  - **Source:** https://arxiv.org/abs/2009.06489
  - **Code:** —
  - **Mechanism:** Foundational essay arguing that the dominance of certain ML architectures reflects co-evolution with available hardware rather than intrinsic superiority — arXiv title anchors the contribution [claim_detector_landscape_0065_01]. Methodological lens for the detector-landscape: encoder-vs-decoder vs activation-probe latency comparisons (§ A2.4, § A3.3, § A5.1) need matched-compute framing to avoid mis-attributing wins to architecture when they're really hardware-fit wins.
  - **Result:** Position paper — no detector-specific benchmark numbers; cited here as the canonical "matched compute" caveat that should accompany cross-architecture latency / accuracy comparisons across the detector ecosystem.
  - **Status:** Verified. (arXiv essay; matched-compute framing reference) [ev_detector_landscape_0066]

## A5.19. The Mirror Design Pattern (Corll)

- **The Mirror Design Pattern: Strict Data Geometry over Model Scale for Prompt Injection Detection** — Corll (arXiv 2026).
  - **Source:** https://arxiv.org/abs/2603.11875
  - **Code:** —
  - **Mechanism:** Data-curation design pattern that organizes prompt-injection corpora into matched positive/negative cells so a classifier learns control-plane attack mechanics rather than incidental corpus shortcuts; from 5,000 strictly curated open-source samples it defines a 32-cell mirror topology (31 cells filled with public data), trains a sparse character n-gram linear SVM, and compiles the weights into a static Rust artifact with no external model runtime dependencies [claim_detector_landscape_0066_01]. Positions the first-screening detector as needing to be "fast, deterministic, non-promptable, and auditable" rather than a large semantic model [claim_detector_landscape_0066_02].
  - **Result:** Abstract reports 95.97% recall and 92.07% F1 on a 524-case holdout at sub-millisecond latency; on the same holdout a 22-million-parameter Prompt Guard 2 model reaches only 44.35% recall and 59.14% F1 at 49 ms median / 324 ms p95 latency — the lightweight linear SVM beats the neural detector on both quality and latency (`unverified body claim` for the specific Prompt Guard 2 deltas; abstract states them but framing is the paper's).
  - **Status:** Verified. (no widely-known repo) The reference case for "strict data geometry beats model scale" — a lightweight, sub-ms first-screening detector contrasting the encoder/decoder defaults (§ A1, § A3); pair with § A5.6 (embedding + classical-ML) and § A5.18 (matched-compute caveat). [ev_detector_landscape_0073]

## A5.20. PromptLocate (Jia, Liu, Shao, Jia & Gong)

- **PromptLocate: Localizing Prompt Injection Attacks** — Jia, Liu, Shao, Jia & Gong (IEEE Symposium on Security and Privacy 2026).
  - **Source:** https://arxiv.org/abs/2510.12252
  - **Code:** —
  - **Mechanism:** Localizes the injected prompt within contaminated input data (rather than only flagging that an attack occurred) via three sequential steps: segmenting contaminated data into semantically coherent units, identifying which segments contain injected instructions, and pinpointing which segments contain injected data [claim_detector_landscape_0067_01]. Motivated by post-attack forensic analysis and data recovery, a use-case distinct from the binary detect/block default elsewhere in the dossier.
  - **Result:** Abstract reports PromptLocate is the first method for localizing injected prompts [claim_detector_landscape_0067_02]; evaluated across 16 attack scenarios (eight existing and eight adaptive variants) with accurate localization (specific deltas `(unverified body claim)`).
  - **Status:** Verified. (no widely-known repo) The first prompt-injection localization method — structurally distinct from the detect-only detectors (§ A5.1 - § A5.18); IEEE S&P 2026 venue. [ev_detector_landscape_0074]
