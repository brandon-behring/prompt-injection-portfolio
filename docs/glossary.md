# Glossary

Project-specific terms for `prompt-injection-portfolio`. Per plan §2
Tier-4 anti-pattern firewall: any new project-specific term introduced
in code or prose must land here in the same commit. Enforced by the
`glossary_complete` test-contract (tests/contracts/test_glossary_complete.py).

Terms are listed in alphabetical order. For methodology terms inherited
from the submission predecessor (`prompt-injection-detection-prototype`)
see that repo's own `docs/glossary.md` + canonical-terminology table
(per submission ADR-064).

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

## ASR

**A**ttack **S**uccess **R**ate: portion of adversarial transforms that
defeat the detector (defined as `transformed_score < threshold AND
original_score >= threshold`). Returned by `eval_toolkit.sweep(...,
attack_threshold=t)`.

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

## Pre-alpha banner

Visible across the entire portfolio (README + book frontmatter +
HF Hub model cards) until M7 v0.7.0 ratification per Round 3 Q2''
(ADR-024). Reminds readers that ADRs are not yet locked.

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
