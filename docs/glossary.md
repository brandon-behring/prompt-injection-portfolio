# Glossary

Project-specific terms for `prompt-injection-portfolio`. Per plan §2
Tier-4 anti-pattern firewall: any new project-specific term introduced
in code or prose must land here in the same commit. Enforced by the
`glossary_complete` test-contract (tests/contracts/test_glossary_complete.py).

Terms are listed in alphabetical order (case-insensitive). For methodology
terms inherited from the submission predecessor
(`prompt-injection-detection-prototype`) see that repo's own
`docs/glossary.md` + canonical-terminology table (per submission ADR-064).

---

## ADR-NNN

**A**rchitecture **D**ecision **R**ecord. Michael Nygard format at
`decisions/ADR-NNN-<slug>.md`. Portfolio uses a lighter retrospective
ADR cadence than the submission (see [[sdd-calibration-by-audience]]
memory); ~35-37 ADRs anticipated at M7 close.

## Adversarial robustness matrix

Lane 1b's 12-technique × N-detector grid of character-injection bypass
results. Per Round 20 + Round 21: all 12 character_injection dataclasses
ship in `eval_toolkit.adversarial.ALL_TECHNIQUES` v0.47.0+.

## agentic_benchmarks

Dossier `claim_family` (per ADR-007). Indirect-injection benchmarks that
test prompt injection inside an agentic loop with tool calls + side
effects: BIPIA, InjecAgent, AgentDojo, LLMail-Inject, Agent Security
Bench (ASB), τ-Bench, and the 2026 adaptive-attacker benchmarks
(AgentDyn / AgentSentry / AgentVigil). Distinct from `detector_benchmarks`
which test classifier accuracy on single text inputs.

## ALL_TECHNIQUES

The 12-tuple of character-injection dataclass strategies exported by
`eval_toolkit.adversarial` v0.47.0+ — core-6
(ZeroWidthSpaceInjection, HomoglyphSubstitution, DiacriticInjection,
WhitespaceInjection, CaseRandomization, PunctuationInjection) +
advanced-6 (BidiRTLInjection, TagStrippingInjection, SynonymSubstitution,
TokenSplitting, UnicodeNormalization, InvisibleCharsInjection).

## APR

**A**ttack **P**revention **R**ate (Meta Prompt Guard 2 metric): % of
attacks blocked at ≤3% utility loss. Reported alongside ASR in Lane 4
agentic eval per ADR-037.

## architectural_defense_methods

Dossier `claim_family` (per ADR-007). Defenses that change LLM-application
architecture rather than classify text: Spotlighting (delimiting /
datamarking / encoding), StruQ, SecAlign + Meta SecAlign, Jatmo,
Instruction Hierarchy, CaMeL, IsolateGPT/SecGPT, LlamaFirewall, tool-call
constraints, output filtering. Distinct from `detector_architectures`
which classifies content; architectural defenses change *how the
system processes the content*.

## ASR

**A**ttack **S**uccess **R**ate: portion of adversarial transforms that
defeat the detector (defined as `transformed_score < threshold AND
original_score >= threshold`). Returned by `eval_toolkit.sweep(...,
attack_threshold=t)`.

## benchmark_validity

Dossier `claim_family` (per ADR-007). Methodology critiques challenging
the validity of detector benchmark numbers: CodeIntegrity's "98% post-mortem,"
"Are Firewalls All You Need?" (Bhagwatkar et al. NeurIPS 2025), "Bypassing
Prompt Injection and Jailbreak Detection in LLM Guardrails" (Hackett et al.
2025), Goodhart's law on public benchmarks, training-data leakage,
selection bias in self-reported numbers, weak-attack pathologies.

## claim_family

A `bib_ledger.yml` taxonomy key that groups dossier entries by topic
domain. Per ADR-007: domain-prefixed lowercase (e.g.,
`ood_evaluation_methodology`, `direct_injection`, `production_incidents`).
Each entry in `bib_ledger.yml` declares exactly one `claim_family`. Lane
experiment-records + ADRs + book chapters cite claim_families to resolve
to specific dossier entries via `experiments/MANIFEST.json`.

## commercial_detector_performance

Dossier `claim_family` (per ADR-007). Self-reported + independently
verified benchmark scores for proprietary/commercial detectors: Lakera
Guard, Azure AI Prompt Shields (User + Document + Spotlighting), AWS
Bedrock Guardrails, NVIDIA NeMo Guardrails, Google Model Armor, Aporia
Guardrails, plus vendors without published numbers (HiddenLayer, Robust
Intelligence, CalypsoAI, Vijil Dome, Guardrails AI, SafePrompt).

## detector_architectures

Dossier `claim_family` (per ADR-007). The model-architecture axis of the
detector landscape: encoder-only (BERT / DeBERTa / ModernBERT / NeoBERT),
decoder small (Qwen3-0.6B, Llama-3.2-1B), LLM-as-judge (Llama-3.1-8B,
Mistral, Phi), multi-agent (CourtGuard), activation-probe (TaskTracker,
InstructDetector), embedding+ML (XGBoost on OpenAI embeddings).

## detector_benchmarks

Dossier `claim_family` (per ADR-007). The text-classification benchmark
side of detector eval: PINT, PromptShield benchmark, NotInject, BIPIA,
deepset/prompt-injections, rogue-security/prompt-injections-benchmark,
JailbreakBench, gandalf_ignore_instructions, AdvBench/HarmBench (as
attack benchmarks). Distinct from `agentic_benchmarks` which test
end-to-end tool-using agents.

## detector_latency_tradeoff

Dossier `claim_family` (per ADR-007). The inference-latency axis of
detector deployability: BERT ~5ms / ModernBERT ~8ms / embedding+ML ~80ms
/ small-LM fine-tune ~200ms / LLM-as-judge ~800ms (per CodeIntegrity's
2026 measurements). Multi-agent (CourtGuard) sits above LLM-as-judge.
Quantization (INT8 ONNX) shifts encoder costs toward the lower end.

## direct_vs_indirect_split

Dossier `claim_family` (per ADR-007). The conceptual + empirical
distinction between direct prompt injection (user-supplied) and indirect
/ XPIA (retrieved-content) attacks. Covers Greshake's 4-flavor taxonomy
(passive / active / user-driven / hidden), OWASP LLM01:2025 codification,
MITRE ATLAS AML.T0051.000-.001 split, the trust-boundary problem,
Simon Willison's dual-LLM pattern, and information-theoretic arguments
for why indirect detection is fundamentally harder.

## evaluation_metrics

Dossier `claim_family` (per ADR-007). Metric definitions + what each
measures + what each misses: accuracy / F1 / AUC-ROC / AUC-PR /
TPR@LowFPR / APR / over-defense accuracy / ASR-utility tradeoff. Includes
PromptShield's TPR@LowFPR introduction as the deployment-relevant metric
shift, Meta PG2's APR, NotInject's over-defense, AgentDojo's coupled
benign-utility + utility-under-attack reporting.

## Fragment (book substrate)

Per Round 17 Q2 shared-substrate authoring pattern: each lane has
fragments at `book/src/content/fragments/lane-N/{methodology,
results,interpretation}.mdx` holding experiment data + dossier
citations (single source of truth). Each of the 3 guides' chapter
MDX imports + sequences fragments with guide-specific framing prose.

## Guide (3-guide architecture)

Per Round 17: portfolio's book ships THREE separate guides — textbook
(M7) + narrative ("Can we climb the wall?", v0.8.0) + academic IMRaD
(v0.9.0) — at three subsite folders inside one Astro project. Each
guide has its own TOC + nav + audience; shared substrate via fragments.

## injection_threat_model

Dossier `claim_family` (per ADR-007). Foundational threat-model framings:
Greshake et al. 2023 (arXiv 2302.12173) introduction of indirect
injection, OWASP LLM01:2025 direct + indirect codification, MITRE ATLAS
AML.T0051 split, Simon Willison's dual-LLM / privileged-vs-quarantined
pattern, Meta's instruction-hierarchy framing, the conceptual lineage
through SQL injection / XSS.

## Lane N

A self-contained experiment-extension to the submission's prototype.
Portfolio has 6 lanes (1, 1b, 2, 3, 4, 5) per plan §5; each has a 4-file
experiment record (hypothesis/protocol/results/decisions.md) per §18 +
a per-lane playbook in `portfolio-lane-execution-playbooks.md` companion.

## LODO

**L**eave-**O**ne-**D**ataset-**O**ut methodology. Cross-source disjoint
splits per submission ADR-016. Portfolio inherits + reuses this discipline.

## MR-N

Upstream **M**erge **R**equest filed by portfolio against one of the 4
load-bearing libraries (eval-toolkit / runpod-deploy / research_toolkit
/ book-scaffold-astro). Tracked in `decisions/upstream_issues.md`. Per
Round 21: 8 of 9 M0-batch MRs closed by upstream; only MR-3 + new MR-12
remain open.

## OOD wall

The bottom-line finding from the submission predecessor (per ADR-075):
fine-tuning on direct-injection-heavy training pool actively HURTS
generalization to indirect/agentic OOD slices (-0.071 AUPRC delta vs
frozen-probe with CI clearing zero). Portfolio asks whether the wall
is data-bound or structural across backbones + parameter budgets.

## ood_evaluation_methodology

Dossier `claim_family` (per ADR-007). The out-of-distribution evaluation
discipline: LODO (held-out *datasets* not held-out *rows*), conversational
vs. application-structured tracks (PromptShield's design), held-out
benchmarks (PINT 4,314 inputs explicitly never-trained-on), low-FPR
operating points (TPR @ 1% / 0.5% / 0.1% / 0.05% FPR per PromptShield
2025), adaptive-attack OOD (LLMail-Inject's 208K-attack adaptive split).

## Pre-alpha banner

Visible across the entire portfolio (README + book frontmatter +
HF Hub model cards) until M7 v0.7.0 ratification per Round 3 Q2''
(ADR-024). Reminds readers that ADRs are not yet locked.

## production_incidents

Dossier `claim_family` (per ADR-007). Public CVEs + bug-bounty
disclosures documenting prompt-injection exploitation in production:
EchoLeak (CVE-2025-32711, Aim Labs June 2025) zero-click XPIA in
Microsoft 365 Copilot, Johann Rehberger's August 2025 "Month of AI
Bugs," Slack AI cross-channel exfiltration (PromptArmor 2024), ChatGPT
Markdown image exfil (2023), Bing Chat / Copilot manipulation, Gemini
long-term-memory poisoning, ShadowPrompt (Claude Chrome extension Dec
2025), Gemini Trifecta, Comet browser indirect injection. Per ADR-041
+ ETHICS.md §1: records existence + impact + remediation; does NOT
republish exploit content or step-by-step reproductions.

## reproducibility_practice

Dossier `claim_family` (per ADR-007). Disclosure-gap audit of winning
detectors: Qualifire Sentinel's private dataset slice undisclosed, Meta
Prompt Guard 2's red-team data undisclosed, ProtectAI's exact mixture
undisclosed, "winning" detectors mostly not reproducible end-to-end from
public artifacts. Includes dataset license + provenance hygiene practice.

## scorecard / metric_specs

v0.46+ canonical evaluation API: `scorecard(y_true, y_score,
metrics=[...])` returns `Mapping[str, MetricResult]`. Threshold-free
specs in `metric_specs.{pr_auc, roc_auc, brier, ece(n_bins=15)}`.
Replaces top-level scalar metric imports (REMOVED in v0.47.0).

## Single-class slice

A LODO/OOD eval slice where `y_true` contains only one class (all 0s
or all 1s). PR-AUC + ROC-AUC are undefined; eval-toolkit's scorecard
returns `status="skipped"` cells via existing `MetricState` vocabulary.
Per ADR-027 → upstream-enforced via eval-toolkit#39 + submission ADR-055.

## TextTransform Protocol

v0.47.0 canonical strategy contract per eval-toolkit ADR 0003. Top-level
`from eval_toolkit import TextTransform`. Adversarial attacks + defensive
spotlighting both satisfy structurally — same `name + transform(text)`
shape. Drives the unified top-level `sweep()`.

## TPR@LowFPR

True positive rate measured at constrained false-positive rates
(typically 1%, 0.5%, 0.1%, 0.05%). Methodologically load-bearing
detector metric per PromptShield 2025. Reported in all Lane 1+4
evals per ADR-036.

## training_data_sources

Dossier `claim_family` (per ADR-007). The training corpus axis: every
dataset cited as training input for prompt-injection detectors, with
license + size + composition + known leakage issues. Covers foundational
small (deepset, jackhhao, xTRam1/safe-guard, verazuo, lakera/gandalf),
mid-size aggregated (geekyrakshit 534K, SPML, alespalla, VMware,
microsoft/orca-agentinstruct), crowd-sourced (TensorTrust, HackAPrompt,
LLMail-Inject), safety/red-team reused (AdvBench, HarmBench,
JailbreakBench, WildJailbreak/WildGuardMix), and 2025-26 specialized
(DhruvTre, hendzh/PromptShield, hlyn dataset, protectai/validation).

## training_methodologies

Dossier `claim_family` (per ADR-007). Detector + architectural-defense
training recipes: encoder baseline (AdamW, LR 2e-5 to 5e-5, batch 8-32,
CE, 3 epochs); advanced loss functions (energy-based per Liu NeurIPS
2020, Recall@1%FPR custom loss per Meta PG2, Evidential Deep Learning
per hlyn); PEFT (LoRA, DoRA); regularization stacks (SupCon, FreeLB,
R-Drop, SWA, Mixout); LLM-detector fine-tuning (PromptShield's LoRA on
Llama-3.1-8B with `\n` augmentation); architectural training (StruQ
reserved delimiters, SecAlign DPO, Instruction Hierarchy context-synthesis,
Jatmo distillation, CaMeL capability-tagging); game-theoretic (DataSentinel
minimax).
