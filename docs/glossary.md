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

## activation_probe_methodology

Dossier `claim_family` (per ADR-007). The hidden-state signal class for
prompt-injection detection: TaskTracker linear-probe recipe on activation
deltas (pre- vs post-untrusted-data injection), InstructDetector
activation-based detector, AttentionTracker / hung2025 family
attention-head-level signals, encoder-vs-decoder transfer questions,
methodology critiques (benign-text-distribution sharing in TaskTracker
eval). Distinct from `detector_architectures` which covers activation-probe
detectors as one architecture among many; this family is the activation-delta
signal class methodology specifically. Lane 5 dossier substrate.

## ADR-NNN

**A**rchitecture **D**ecision **R**ecord. Michael Nygard format at
`decisions/ADR-NNN-<slug>.md`. Portfolio uses a lighter retrospective
ADR cadence than the submission (see [[sdd-calibration-by-audience]]
memory); ~35-37 ADRs anticipated at M7 close.

## Adversarial robustness matrix

Lane 1b's 12-technique × N-detector grid of character-injection bypass
results. Per Round 20 + Round 21: all 12 character_injection dataclasses
ship in `eval_toolkit.adversarial.ALL_TECHNIQUES` v0.47.0+.

## agent_capability_isolation

Dossier `claim_family` (per ADR-007). Capability-based + dual-LLM-pattern
isolation specifically: CaMeL formalism (Debenedetti et al. DeepMind arXiv
2503.18813) — privileged-LLM/quarantined-LLM split with custom Python
interpreter + capability tags + provenance metadata; IsolateGPT / SecGPT
(Wu et al. NDSS 2025) — per-plugin sandboxing; Willison dual-LLM articulation;
information-flow control descended from SLam/Jif/HiStar lineage. Distinct
from broader `architectural_defense_methods` (Spotlighting / StruQ / SecAlign
live there); per validator, a single bib_ledger entry declares exactly one
`claim_family`, so CaMeL + IsolateGPT are classified here (more specific).

## agent_harness_architecture

Dossier `claim_family` (per ADR-007). The system-shape layer underlying
agentic deployment: tool-calling agents, multi-turn loops, side-effect
surfaces, sub-agent delegation, persistent memory. LlamaFirewall (Meta
arXiv 2505.03574), AgentArmor, ReAct/Function-calling/Toolformer lineage,
Anthropic Claude Code / Cursor / OpenAI Assistants harness designs. Key
claim: side effects make agentic injection categorically worse than chat
injection — same detection accuracy translates to vastly higher blast
radius. Distinct from `architectural_defense_methods` (what the LLM does
with text); this family is what the agent harness is shaped like.

## agentic_bench_critique

Dossier `claim_family` (per ADR-007). The critique layer on top of
`agentic_benchmarks`: Bhagwatkar "Are Firewalls All You Need?" (NeurIPS
2025 arXiv 2510.05244) saturation findings — AgentDojo / ASB / InjecAgent
/ τ-Bench saturated by two-firewall defenses; weak-attack pathologies;
LLMail-Inject as adaptive gold-standard (Abdelnabi et al. SaTML 2025
arXiv 2506.09956) — 208K attacks defeating SOTA defenses; Nasr "attacker
moves second" static-defense critique (arXiv 2510.09023); 2026 adaptive-
attacker benchmarks (AgentDyn / AgentSentry / AgentVigil) as critique
vehicles. The benchmarks themselves stay catalogued in `agentic_benchmarks`.

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

## attack-type-LODO

Leave-one-attack-type-out evaluation (M1, Lane 1): train on 13 of BIPIA's 14
injection task-types, test on the held-out one, rotate. The `attack-type`
sibling of `carrier-LODO`, with the carrier held constant (ADR-052) so the only
shift is the payload's intent. The §6.5 OOD-wall prediction is judged on these
folds. (Distinct from the submission's dataset-level `LODO`.)

**In plain terms:** hide one *kind* of attack during training, then check the
detector still catches it — repeated for each kind.

## AUPRC

Area under the precision–recall curve (AUC-PR / `pr_auc`; see
`evaluation_metrics`, `scorecard / metric_specs`). **Prevalence-inflated:** at
positive-rate p a no-skill classifier already scores AUPRC ≈ p — so on BIPIA
carriers (83–94% positive) chance AUPRC ≈ 0.92, and a scope-blind probe can look
like a "0.92 separator." Report with `AUROC` + class means, not AUPRC alone
(audit 2026-06; `reference_scorers.py`).

**In plain terms:** a score that rewards finding rare positives — but when
positives are *common* it flatters by default, so a high AUPRC can be meaningless.

## AUROC

Area under the ROC curve (`roc_auc`): the probability a random positive outscores
a random negative. **Prevalence-robust** — 0.5 = chance regardless of class
balance; < 0.5 = systematically worse than chance (ProtectAI 0.44 on
BIPIA-indirect = direct-trained, scope-blind). The honest headline where `AUPRC`
is inflated.

**In plain terms:** how well the detector *ranks* attacks above benign — and
unlike AUPRC it isn't fooled by lots of positives. Below 0.5 means it points the
wrong way.

## benchmark_validity

Dossier `claim_family` (per ADR-007). Methodology critiques challenging
the validity of detector benchmark numbers: CodeIntegrity's "98% post-mortem,"
"Are Firewalls All You Need?" (Bhagwatkar et al. NeurIPS 2025), "Bypassing
Prompt Injection and Jailbreak Detection in LLM Guardrails" (Hackett et al.
2025), Goodhart's law on public benchmarks, training-data leakage,
selection bias in self-reported numbers, weak-attack pathologies.

## capacity ladder (tfidf / frozen / LoRA / full_ft)

The four detector "rungs" of increasing model capacity used to read the OOD gap
at each level: **tfidf** (bag-of-words + logistic regression — lexical only),
**frozen** (a frozen pretrained encoder's embeddings + a logistic head — sees
meaning, doesn't learn the task), **LoRA** (small end-to-end fine-tune of
ModernBERT — M1's measured ceiling; see `training_methodologies`), **full_ft**
(full fine-tune — most capacity; deferred behind a `trigger-gate (§16)`). Reading
a result *across* rungs is what reveals `capacity-dependent` vs
`capacity-attenuated` walls.

**In plain terms:** four detectors from dumbest to smartest; watching the wall
shrink (or not) as you climb tells you whether the wall is about the *model* or
the *task*.

## capacity-dependent / capacity-attenuated / residual wall

Three readings of how an OOD gap behaves up the `capacity ladder`.
**Capacity-dependent:** real at tfidf/frozen but *vanishes* with capacity (the
attack-type wall — gone at LoRA). **Capacity-attenuated:** *shrinks but persists*
(the carrier wall — ~60% smaller at LoRA, not zero). **Residual wall:** the part
that remains at the ceiling (the +0.205 table-carrier gap at LoRA). See
`multi-axis OOD spine (capacity-dependent)`.

**In plain terms:** does a bigger model make the wall disappear
(capacity-dependent), only lower it (attenuated), or leave a stubborn chunk
(residual)?

## carrier (OOD axis)

The trust-boundary / content-format axis of an indirect-injection eval — the
email / code / table / qa / abstract scaffold the injected payload sits in
(BIPIA's per-subset structure; see `rag_evaluation_harness`). Per the M1 EDA, the
carrier **dominates the frozen-embedding geometry** (silhouette by-carrier 0.197
vs by-attack-type −0.023; KMeans→carrier ARI 0.98), so the Round-30 multi-axis
spine (ADR-055) named it the **standing wall** (the geometric prior) — distinct from
the *attack-type* axis, which M1 showed is capacity-dependent. M1 held the carrier
constant by design (ADR-052); the `carrier-LODO` M2 pre-flight (2026-06-01) then
refined the claim to **partially capacity-resistant — capacity-attenuated, residual
at the table carrier (provisional, n=3)**.

## carrier-LODO

Leave-one-carrier-out evaluation: train on a subset of carriers, test on a
held-out `carrier` (email/code/table available; qa/abstract license-gated). The
carrier-axis sibling of attack-type-LODO, reusing the M1 harness with the LODO
axis swapped and a **carrier-clustered** estimator (the held-out unit is the
carrier, n=3; the bootstrap resamples payload ids *within* the held-out carrier).
Registered by ADR-055 (Round 30) as the M1-exit → Lane-2-entry pre-flight gate:
does end-to-end LoRA dissolve the carrier OOD gap (spine revised) or does it
persist (spine validated)? Pre-registered at `experiments/carrier-lodo/criteria.md`.

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

## composition_audit

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). Methodology
literature on training-data contamination detection + composition disclosure:
Xu et al. contamination survey (arXiv 2406.04244), Deng et al. NAACL 2024
(2311.09783), Yang et al. rephrased-samples contamination (2311.04850),
Oren et al. proving black-box contamination (ICLR 2024 2310.17623), Shi
et al. Min-K% Prob detection (ICLR 2024 2310.16789), Sainz et al. NLP-eval
contamination call (EMNLP Findings 2023), Zawalski CoDeC (2510.27055),
M et al. six-frontier surface-pattern (2603.16197). Distinct from
`benchmark_validity` (which covers Goodhart + vendor-bias critiques);
this family is the methodology of contamination *detection* specifically.

## content_authentication_rag

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). mTLS-style
content authentication for AI retrieval, C2PA / content-credentials applied
to retrieved documents, retrieval-time cryptographic authentication.
Distinguished from `retrieval_provenance` (metadata-only trust signal)
by requiring cryptographic verification. Less-mature literature space;
mixed academic + vendor + standards-draft expected.

## d′ (d-prime)

Signal-detection separation between two distributions: the difference of means in
pooled-standard-deviation units. Lane 5's M3-entry gate — the activation probe
proceeds only if it separates injected vs clean activations at **d′ > 0.5** (else
pivot to the `agent_capability_isolation` surface-third-path).

**In plain terms:** a number for "how far apart are these two bell curves" — a
go/no-go threshold for whether the probe sees anything.

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

## dual_llm_pattern

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). The Willison
2023 dual-LLM articulation + its 2025 CaMeL formalization + descendants
specifically. Separated from `agent_capability_isolation` because the
dual-LLM pattern is a historical + conceptual claim (privileged-vs-
quarantined; trust-boundary as the original sin) while capability-isolation
is the engineering claim (tagging + interpreters). Keeps citation hygiene
clean: Willison informal blogs vs Debenedetti et al. formal paper.

## embedding-invisible

A signal *not* linearly present in a frozen final-layer embedding yet learnable
end-to-end. M1: the attack-type signal is embedding-invisible (frozen MiniLM
silhouette by-attack-type −0.023) but LoRA learns it directly (test AUPRC
0.98–0.999), sharpening Lane 5's hypothesis toward *intermediate* activations.
See `multi-axis OOD spine (capacity-dependent)`, `silhouette / ARI`.

**In plain terms:** the clue isn't visible in the model's frozen "snapshot" of
the text, but the model *can* learn to see it if you actually train it.

## encoder_backbone

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). Encoder backbone
alternatives + comparisons for injection-detection: ModernBERT (answerdotai
2024), NeoBERT 250M (Le Breton 2025 arXiv 2502.19587 — "evaluated but no
public injection detector"), DeBERTa-v3 (He 2020), DistilBERT, XLM-RoBERTa
multilingual variants. The compass §4 "backbone landscape" axis. Distinct
from `detector_architectures` which covers detectors-as-deployed; this
family is the backbone-choice methodology layer.

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

## kappa (κ — Cohen's kappa)

Chance-corrected inter-annotator agreement (0 = chance, 1 = perfect). Lane 2's
synthetic-corpus quality gate: an Opus N=50 audit must reach **κ ≥ 0.5** before
the generated corpus is trusted for training (ADR-027 / ADR-040); below that,
re-spec the synthesis recipe.

**In plain terms:** do two reviewers agree the synthetic examples are labeled
right (beyond lucky guessing)? If not, don't train on them.

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

## multi-axis OOD spine (capacity-dependent)

The Round-30 reframe (ADR-055) of the portfolio's thesis: the `OOD wall` is not
one wall but several **axes**, each with its own capacity regime. The
*attack-type* axis is **capacity-dependent** — M1's pre-registered §6.5 prediction
SURVIVES on tfidf/frozen but is FALSIFIED at the LoRA ceiling (T 0.135 → 0.082 →
−0.003): end-to-end LoRA dissolves the per-type gap. The *carrier* axis dominates
the representation geometry; the `carrier-LODO` M2 pre-flight (2026-06-01) refined it
from "standing wall" to **partially capacity-resistant — capacity-attenuated, residual
at the table carrier (provisional, n=3)**. Reconciles with the submission's "backbone-invariant"
null — backbone-invariant ≠ capacity-invariant, and the submission measured the
carrier axis while M1 measured attack-type-within-indirect.

## OOD wall

The bottom-line finding from the submission predecessor (per ADR-075):
fine-tuning on direct-injection-heavy training pool actively HURTS
generalization to indirect/agentic OOD slices (-0.071 AUPRC delta vs
frozen-probe with CI clearing zero). Portfolio asks whether the wall
is data-bound or structural across backbones + parameter budgets.
**Round 30 (ADR-055) re-axis:** now understood as multi-axis — the *attack-type*
axis is capacity-dependent (M1 dissolved it with end-to-end LoRA), the *carrier*
axis is **partially capacity-resistant** (capacity-attenuated, residual at the table
carrier; provisional n=3 — 2026-06-01 carrier-LODO verdict; see `multi-axis OOD spine
(capacity-dependent)`).

## ood_evaluation_methodology

Dossier `claim_family` (per ADR-007). The out-of-distribution evaluation
discipline: LODO (held-out *datasets* not held-out *rows*), conversational
vs. application-structured tracks (PromptShield's design), held-out
benchmarks (PINT 4,314 inputs explicitly never-trained-on), low-FPR
operating points (TPR @ 1% / 0.5% / 0.1% / 0.05% FPR per PromptShield
2025), adaptive-attack OOD (LLMail-Inject's 208K-attack adaptive split).

## PAD (proxy-A-distance) / MMD

Two train↔test distribution-shift magnitudes used in the EDA (`shift`): **PAD** =
how separable two slices are to a simple classifier (a proxy for divergence);
**MMD** = maximum mean discrepancy, a kernel distance between distributions. Used
to *quantify* a fold's shift pre-modeling — necessary-not-sufficient for a wall
(separability ≠ collapse).

**In plain terms:** two rulers for "how different is the test set from training" —
a big gap is a warning sign, not a guarantee, of failure.

## payload-clustered bootstrap

A resampling scheme that resamples *payload groups* (not individual rows) when
computing a `bootstrap CI`, because the ~5 strings per attack-type/carrier are
correlated. The §6.5 estimator is payload-clustered; `carrier-LODO` nests it
*within* the held-out carrier. Avoids the pseudo-replication that would fake a
tight interval.

**In plain terms:** when rows come in correlated clumps, resample whole clumps —
otherwise the confidence interval lies by pretending you have more independent
data than you do.

## permutation test (p) / bootstrap CI (CI-low)

The two §6.5 significance tools. **Permutation p:** reshuffle labels many times;
p = fraction of shuffles whose statistic beats the observed one (p < 0.05 ⇒
unlikely by chance). **Bootstrap CI-low:** the lower bound of a resampled
confidence interval; CI-low > 0 ⇒ the gap is reliably positive. The verdict rule
needs *both* (see `SURVIVES / FALSIFIED / SMALL-THROUGHOUT`).

**In plain terms:** "could this gap be a fluke?" (permutation) and "is it reliably
above zero?" (bootstrap) — a result has to pass both.

## Pre-alpha banner

Visible across the entire portfolio (README + book frontmatter +
HF Hub model cards) until M7 v0.7.0 ratification per Round 3 Q2''
(ADR-024). Reminds readers that ADRs are not yet locked.

## pre-registration

Writing the hypothesis, decision rule, thresholds, and held-out tail sets to a
dated file *before* any result exists, so a verdict can't be reverse-engineered
from the data. The §6.5 prediction (`experiments/eda/OOD_WALL_PREDICTION/
criteria.md`) and the carrier-LODO criteria are pre-registered; the `write-gate`
enforces the order operationally.

**In plain terms:** call your shot before you see the data — that's what makes a
falsification credible rather than hindsight.

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

## production_rag_incidents

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). Production
RAG-injection incidents analyzed at the RAG-pipeline layer specifically
(narrower than `production_incidents` which covers all PI incidents).
Each entry analyzes the retrieval-boundary mechanism (where malicious
content entered the RAG pipeline) and the defense-layer-bypassed: EchoLeak
M365 Copilot RAG (CVE-2025-32711), Slack AI cross-channel RAG-exfil,
Comet browser RAG-style ingestion (Brave 2025), Gemini long-term memory
poisoning RAG-vector (Rehberger 2024), ChatGPT Markdown image exfil
(pre-RAG-fix era), Bing Chat webpage manipulation (Greshake 2023). Per
ADR-041 + ETHICS.md §1: vulnerability-class + impact + remediation only.

## rag_evaluation_harness

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). RAG-specific
evaluation harnesses: BIPIA per-subset (Email QA / Web QA / Table QA /
Summarization / Code QA) — Yi et al. Microsoft/USTC KDD 2025 arXiv
2312.14197; Azure Document Shield benchmark + `documentsAnalysis` API;
LLMail-Inject as RAG-email adaptive eval (Abdelnabi et al. SaTML 2025).
Distinct from broader `agentic_benchmarks` (which covers BIPIA's
agentic-eval framing); this family captures the RAG-specific subset
+ retrieval-boundary evaluation.

## rag_retrieval_dynamics

Dossier `claim_family` (per ADR-007, 2026-05-27 scope expansion). The
retrieval-mechanics substrate that indirect injection exploits and that
retrieval-side defenses must account for: context-window position effects
on whether an injected span is attended (Lost in the Middle, Liu et al.
arXiv 2307.03172); the dense-retrieval embedding-similarity primitive that
surfaces a possibly-poisoned chunk (Sentence-BERT, Reimers & Gurevych arXiv
1908.10084); contextual-embedding geometry/anisotropy bearing on retrieval
dedup + trust-signal separability (Ethayarajh arXiv 1909.00512). Scoped to
the injection-relevant reading of retrieval mechanics — not a general IR/RAG
survey; substrate for `retrieval_provenance`.

## reproducibility_practice

Dossier `claim_family` (per ADR-007). Disclosure-gap audit of winning
detectors: Qualifire Sentinel's private dataset slice undisclosed, Meta
Prompt Guard 2's red-team data undisclosed, ProtectAI's exact mixture
undisclosed, "winning" detectors mostly not reproducible end-to-end from
public artifacts. Includes dataset license + provenance hygiene practice.

## retrieval_provenance

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). Verifiable
retrieval + signed-document architectures + document-class trust tier
+ retrieval-time provenance metadata as trust signal. The newer / less-
mature complement to text-only detection — concept: give detectors a
trustworthy source signal rather than text alone. Includes source-
attribution-preserving prompt templates (OpenAI `tool`/`input` role,
Anthropic `tool_result`) as closest production-deployed approximation.
Distinct from `content_authentication_rag` (cryptographic verification)
by being metadata-only.

## ROC-gap (G)

The carrier-LODO test statistic: the mean over held-out carriers of (validation
ROC-AUC − held-out-carrier test ROC-AUC). G > 0 = detection drops on an unseen
carrier. Used on the ROC basis (not AUPRC) because carriers are 83–94% positive.
Frozen G = +0.167 → LoRA G = +0.067 (residual +0.205 at table). The carrier-axis
analogue of `transfer-gap (T)`.

**In plain terms:** how much worse the detector does on a carrier it never trained
on — the height of the carrier wall.

## S2 (encoder-transfer caveat)

The pre-registered Lane-1 limitation that the §6.5 prediction's *prediction-encoder
choice* (MiniLM → frozen ModernBERT) might not transfer — empirically mitigated,
since the ranking SURVIVED at the frozen rung (Kendall τ-b 0.58). **Not** the same
as the LoRA capacity dissolution: S2 concerns frozen-encoder choice and argued the
ordering *transfers*; the LoRA falsification is the broader `capacity-dependent`
finding S2 did not pre-commit (clarified 2026-06).

**In plain terms:** a hedge written in advance about using one embedding model to
predict another's behavior — often confused with, but distinct from, the separate
finding that *fine-tuning* erases the attack-type wall.

## score_fusion_stacker

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). The meta-
learning layer on top of per-detector scores: Meta Prompt Guard 2's
custom Recall@1%FPR loss; energy-based loss (Liu NeurIPS 2020 arXiv
2010.03759) as Meta + CodeIntegrity foundation; embedding-based detectors
(Ayub & Majumdar arXiv 2410.22284) as stacker-eligible signal; LogisticStacker
per eval-toolkit v0.47.0+; APR metric (Meta PG2) for score-fusion-relevant
reporting; ensemble methods for low-FPR operation. Lane 4 dossier
substrate.

## scorecard / metric_specs

v0.46+ canonical evaluation API: `scorecard(y_true, y_score,
metrics=[...])` returns `Mapping[str, MetricResult]`. Threshold-free
specs in `metric_specs.{pr_auc, roc_auc, brier, ece(n_bins=15)}`.
Replaces top-level scalar metric imports (REMOVED in v0.47.0).

## silhouette / ARI

Two clustering-geometry metrics over embeddings. **Silhouette:** how cleanly
points group by a label (−1…1); by-carrier 0.197 vs by-attack-type −0.023 ⇒ the
embedding is carrier-shaped, attack-type-`embedding-invisible`. **ARI** (adjusted
Rand index): how well *unsupervised* clusters match a label; KMeans→carrier ARI
0.98 vs →attack-type −0.001. The EDA's geometric evidence for the carrier axis
(`a1_v4_metrics.json`).

**In plain terms:** do the data naturally clump by *carrier* or by *attack-type*?
Strongly by carrier — which is why the carrier became the spine.

## Single-class slice

A LODO/OOD eval slice where `y_true` contains only one class (all 0s
or all 1s). PR-AUC + ROC-AUC are undefined; eval-toolkit's scorecard
returns `status="skipped"` cells via existing `MetricState` vocabulary.
Per ADR-027 → upstream-enforced via eval-toolkit#39 + submission ADR-055.

## spotlighting_variants

Dossier `claim_family` (per ADR-007, Sprint 2 expansion). Per-variant
deep-dive of Microsoft Spotlighting (Hines et al. CAMLIS 2024 arXiv
2403.14720; GA Microsoft Build 2025): *delimiting* (tag-wrap; minimal
overhead; bypassable by tag-mimicry), *datamarking* (whitespace → marker
token; near-zero task-degradation per Hines abstract), *encoding* (base-64
prepend; most effective in paper; requires GPT-4-class decoder; primary
GA variant in Azure Document Shield). Headline claim: GPT-3.5/4 ASR >
50% → < 2% per Hines abstract. Distinct from broader
`architectural_defense_methods`; this family is the Spotlighting-
variant-specific axis.

## SURVIVES / FALSIFIED / SMALL-THROUGHOUT (pre-registered verdicts)

The three outcomes the OOD-wall pre-registration can return, judged on the LoRA
rung. **SURVIVES:** the gap is real *and* capacity-resistant (passes both
`permutation test` p < 0.05 and `bootstrap CI` lower-bound > 0, and — for carrier —
clears ½·G(frozen)). **FALSIFIED:** the gap is statistically gone (CI-low ≤ 0;
attack-type at LoRA, T −0.003). **SMALL-THROUGHOUT:** the pre-registered
else-branch — real but capacity-attenuated, neither resistant nor dissolved
(carrier at LoRA, G +0.067).

**In plain terms:** the wall either stands, falls, or partly-stands — and which one
was decided by a rule fixed in advance.

## TextTransform Protocol

v0.47.0 canonical strategy contract per eval-toolkit ADR 0003. Top-level
`from eval_toolkit import TextTransform`. Adversarial attacks + defensive
spotlighting both satisfy structurally — same `name + transform(text)`
shape. Drives the unified top-level `sweep()`.

## Tier A / B / C (reference-scorer + experiment tiers)

Cost/effort tiers for baselines and add-ons: **A** = free/local (tfidf, frozen
probe, ProtectAI on CPU); **B** = cheap-paid (Meta PG2 86M, embedding-scorer,
CourtGuard — ~$5–15); **C** = expensive, *contingency-gated* (PromptShield
Llama-3.1-8B ~$40–50; the Lane-2 energy-loss variant ~$34) — unlocked only if a
stated signal fires (see `trigger-gate (§16)`, ADR-013/014).

**In plain terms:** a budget ladder — free stuff always runs, cheap stuff runs by
default, expensive stuff only if the cheaper results say it's worth it.

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

## transfer-gap (T)

The §6.5 attack-type test statistic: the difference in per-type detection drop
between the predicted-worst top-k and predicted-best bottom-k held-out types.
T > 0 = the predicted collapse-ordering holds. tfidf +0.135 / frozen +0.082
(SURVIVE) → LoRA −0.003 (FALSIFIED): T collapses as capacity rises. The
attack-type analogue of `ROC-gap (G)`.

**In plain terms:** did the attack-types we predicted would be hardest actually
turn out hardest? Yes for weak detectors, no once you fine-tune.

## trigger-gate (§16)

A pre-registered *conditional* follow-up (catalogued in PORTFOLIO_PLAN §16): a
costed action that fires only if a stated condition is met — e.g. run `full_ft`
*iff* the LoRA verdict is borderline (resolved: does-not-fire); re-run
`carrier-LODO` at n=5 *iff* the qa/abstract license unlocks; the Lane-4
saturation pivot *iff* 2-of-3 benchmarks exceed 95% AUPRC. Keeps deferred work
honest — registered, not forgotten.

**In plain terms:** an "if X happens, then do Y" promise written down in advance,
so deferring something isn't the same as dropping it.

## write-gate

The operational lock that enforces `pre-registration`: the §6.5 verdict cannot be
computed until the *complete* sweep (all required rungs × all seeds) is present on
disk (`manifest_complete`), so no one can peek at partial results and adjust.
Opening the gate is what makes the recorded verdict trustworthy.

**In plain terms:** you can't look at the answer until every experiment has
finished running — no peeking, no nudging.
