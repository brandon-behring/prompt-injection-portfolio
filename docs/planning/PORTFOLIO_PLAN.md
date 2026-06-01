# Plan: `prompt-injection-portfolio` (public, open-ended extension)

## Context

The submission repo (sibling `../prompt-injection-detection-submission/`)
shipped v1.0.1 as a locked case-study submission. Its headline finding is
**honest and uncomfortable**: training the ModernBERT backbone on
direct-injection-heavy LODO data made the indirect/agentic OOD slice *worse*
than the frozen-probe baseline (BIPIA AUPRC: LoRA 0.293 vs frozen-probe 0.364
vs prevalence 0.374). **Fine-tuning consumed the OOD generalization budget.**

This plan creates a **new public sibling repo named
`prompt-injection-portfolio`** that takes the submission as the
prototype and asks: *can we climb the wall, or is it structural?* Five
extension lanes will run as experiments; an Astro+MDX book will be the
**field log**. Submission ADRs stay frozen at v1.0.1; submission code
receives bug-fix patches as v1.0.x (Q4').

The portfolio uses a **hierarchical depth architecture** (Q1' round 2): the
book is the L3 ground-truth deep layer; shallower summaries derive top-down;
the user's verification gate is reading at L3-L5 depth to audit Claude's
reasoning before shallower summaries propagate up.

The portfolio is **public from M0 with a pre-alpha banner** (Q2'' round 3),
develops continuously in public via weekly threads (Q4'' round 3), and
transitions v0.7.0 → v1.0.0 over a ~3-month community feedback window
(Q5'' round 3) before entering v1.0.x patch-only maintenance.

**Round 5 reframing (2026-05-18 post-survey)**: the submission shipped
through v1.0.7 (4 jupytext notebooks, DeLong + BH-FDR + paired-bootstrap,
3-artifact reading-guide, ADR-052 strengthening the OOD wall narrative).
book-scaffold-astro shipped v2.0.0. Portfolio repositions as
**"the next version built from submission's experience, done cleaner"**.

**Round 6 update (2026-05-19 overnight resurvey)** — both repos shipped
massive overnight progress that re-shapes the portfolio plan:

- **book-scaffold-astro pivoted v2.0 → v3.0**: GitHub template → **npm
  monorepo** with two published packages (`@brandon_m_behring/book-scaffold-astro`
  + `@brandon_m_behring/create-book`). Bootstrap is now `npx
  @brandon_m_behring/create-book <name> --profile=...`. Still 3 profiles
  (academic / tools / minimal); no 4th profile shipped. ~50 LOC scaffolded
  per consumer; `npm update` propagates fixes.
- **Submission shipped v1.0.8 → v1.1.2** (5 patches + DeBERTa execution):
  - ADR-055..057 (v1.0.8): eval-toolkit PyPI install, canonical binary
    calibrator API, manifest schema v3. **Single-class metric convention
    enforced upstream** via eval-toolkit #39 + ADR-039 gate 3 → my
    ADR-027 + planned submission v1.0.8 patch task **obsolete**.
  - ADR-058 (v1.0.9): `scripts/eval_from_hub.py` **non-dry-run wired**;
    Block A of ADR-051 closed. **T0 surface is AVAILABLE** in submission.
  - ADR-059 (v1.1.0): runpod-deploy PyPI v0.8.4; 7 issues consumed.
  - ADR-060 (v1.1.0): DeBERTa-v3-base methodology lock + Path B
    infrastructure.
  - ADR-061 (v1.1.1): Quarto navigation restructure.
  - **v1.1.2 DeBERTa execution null result**: chunk_and_average 0.2912 ≈
    head_truncation 0.2895 on pooled OOD (~$1.34 GPU). **Backbone-dominant
    verdict**: ModernBERT advantage is NOT context-window-driven; the OOD
    wall extends across backbones + truncation strategies.

**Round 6 portfolio decisions** (4 new locks):

- **T0 reproducibility**: portfolio writes its own clean T0 (does NOT
  consume submission's eval_from_hub.py). Maintains "next version built
  from submission's experience, done cleaner" framing. ADR-033 dropped;
  **ADR-035 (portfolio-clean-T0-strategy)** replaces it.
- **Scaffold consumption**: `npx @brandon_m_behring/create-book
  prompt-injection-portfolio --profile=academic` + portfolio-local
  extras for what academic profile doesn't cover (likely: volatility
  schema field, T1-T4 source tier enum, pre-alpha banner system, ETHICS
  reference component, AI-disclosure component). File upstream issue
  documenting design intent for a future v3.1 "research-portfolio" profile
  but do NOT block portfolio M0 on it. ADR-031 reframed accordingly.
- **Lane 2 hypothesis + Ch 7**: cite v1.1.2 DeBERTa null result as
  backbone-dominant evidence — Lane 2 question becomes "does indirect
  training data overcome the active-harm pattern AND backbone
  invariance?" Ch 7 case-study expanded.
- **Cleanups**: drop ADR-027 (single-class metric upstream-enforced),
  drop ADR-033 (T0 deferral inverted by submission progress), defer MR-8
  (v3.1 profile PR) to v0.8+, drop Task #14 (submission v1.0.2 patch
  obsolete).

**Round 14 update (2026-05-21 post-survey)** — submission shipped 10
patches (v1.2.3 → v1.2.12) + 8 new ADRs (068..075) over 2 days, AND a
parallel Codex agent implemented + released **5 of 7 portfolio
eval-toolkit MRs** through eval-toolkit v0.43.0 + v0.44.0. This collapses
portfolio M0's MR-implementation burden from "3 critical to ship
upstream" to "0 to ship; consume + verify v0.44.0 primitives":

- **Submission v1.2.3..v1.2.12** (2026-05-19 → 2026-05-21):
  - v1.2.3..v1.2.7: CI hygiene + docs presentation + lychee fix
    (no methodology change; no portfolio impact).
  - **v1.2.8** (2026-05-19): site hardening + bumps `eval-toolkit` pin
    to `==0.43.0` (closes #48 MR-1 + #49 MR-2 core-6 + #53 MR-7 via
    parallel-Codex implementation).
  - **v1.2.9** (2026-05-20): audit-remediation; 4 new ADRs (071/072/
    073/074); **canonical source pin advances v1.0.0 → v1.2.9** (v1.0.0
    preserved as historical reviewer pin per ADR-033).
  - v1.2.10..v1.2.12 (2026-05-20..21): reporting-honesty asterisks +
    polish + README hybrid-adopt. No methodology / model / data /
    result change.
- **8 new submission ADRs**: ADR-068/069/070/073 are 4-class
  immutability-rule narrow-relaxations (consolidated into single rule
  by ADR-073). ADR-071 executes ADR-067 slug-sweep. ADR-072 backfills
  ADR-051/052 frontmatter. ADR-074 redacts ADR-064 self-criticism
  quote. **ADR-075 is load-bearing for portfolio**: it unifies ADR-050
  Revision 2 (FUSE-crash-forced-drop framing) + ADR-052
  (methodology-load-bearing-with-crash-as-trigger reframe) into a
  single canonical narrative. **ADR-052 is FULLY SUPERSEDED** per
  ADR-075 frontmatter; ADR-050 R2 axis superseded. Portfolio's
  Lane 2 hypothesis (§5) + Ch 7 case study (§17) cite **ADR-075** as
  canonical (was ADR-052 in Round 6).
- **eval-toolkit v0.43.0** (2026-05-19): closes #48 MR-1
  (`ood_dataset_from_manifest`); #49 MR-2 core-6 of 12 character
  injection techniques (advanced-6 scheduled for v0.43.1); #53 MR-7
  (`ActivationDeltaProbe`). Plus new `Probe` Protocol +
  `ActivationExtractor` Protocol + optional `[probes]` extra.
- **eval-toolkit v0.44.0** (2026-05-19): closes #50 MR-4
  (`losses.RecallAtLowFPR`); #51 MR-5 (`preprocessing.spotlighting`
  3 variants). Plus optional `[losses]` extra.
- **Remaining open MRs**: MR-3 (research_toolkit #1
  `/dataset-synthesize`), MR-6 (eval-toolkit #52 `MetaLearner` +
  `LogisticStacker`), MR-8 (book-scaffold-astro #6 v3.2
  `research-portfolio` profile), MR-9 (book-scaffold-astro #7
  generic frontmatter primitive — not blocking).
- **NEW MR-10** to file: eval-toolkit advanced-6 character_injection
  extension (bidi RTL + tag stripping + synonym + token splitting +
  Unicode normalization + invisible chars). Scheduled for v0.43.1 per
  upstream CHANGELOG; portfolio files explicit issue to track + signal
  priority (Round 14 Q3 lock).

**Round 14 portfolio decisions** (4 new locks):

- **CI submission ref pin**: advance `v1.1.1` → `v1.2.12` (HEAD), with
  **dynamic-latest fallback** if v1.2.12 isn't pushed yet (round-2 Q2:
  `git ls-remote --tags origin | grep refs/tags/v1.X.X | sort -V | tail -1`
  selects the latest pushed semver tag, falling back to v1.2.11 etc.).
  Tracks current state of the submission's reading-guide + README +
  reviewer-facing site. Accepts re-pin overhead if polish patches
  continue. (Round 14 Q1 lock; user picked HEAD over canonical v1.2.9.)
- **eval-toolkit floor**: bump `>=0.42` → `>=0.44`. Gets MR-1/2/4/5/7
  primitives ready at lane work start; matches submission's exact pin
  `==0.43.0` semantically (portfolio's range floor is `>=0.44` so v0.44+
  is required). (Round 14 Q2 lock.)
- **Lane 1b scope** (MR-2 partial shipment): file new **MR-10**
  extension issue against eval-toolkit for the 6 deferred character
  injection techniques (advanced-6: bidi/tag/synonym/token-split/
  unicode/invisible). Lane 1b uses core-6 at M1 start; advanced-6
  arrives via v0.43.1. No portfolio-side workaround; track explicitly.
  (Round 14 Q3 lock; user picked file-issue over silent wait.)
- **Task #6 transition**: split into closed half (5/7 MRs shipped) +
  new follow-up tasks. Close #6 ("implement MR-1/2/7") as completed
  via parallel-Codex; open **#6a** (`consume + verify v0.44.0 primitives
  at M0 Day 3-4 + populate library_imports.md rows`) + **#6b** (`track
  open MRs MR-3 / #52 MR-6 / #6 MR-8 / #7 MR-9 / new MR-10 for closure`).
  (Round 14 Q4 lock; user picked split over reframe-in-place.)

**Round 14 citation cascade**: Lane 2 hypothesis (§5) + Ch 7 case
study (§17) cite **ADR-075** as canonical full-FT OOD drop rationale.
ADR-052 remains in submission/decisions/ as a historical artifact;
portfolio-side prose treats ADR-075 as the entry point.

**Round 15 update (2026-05-21 post-Round-14 scope directive)** — user
explicit scope-narrowing on Lane 2 fine-tuning + scope-widening on
baselines. Two related locks reshape the experimental matrix:

- **Lane 2 retrain = LoRA only**. Full fine-tuning is OUT OF SCOPE for
  portfolio. Reasoning: submission v1.0.X evidence (ADR-052 + ADR-075)
  already showed full-FT OOD drop was methodology-load-bearing — the
  bottleneck is training data, not parameter budget. Adding full-FT to
  portfolio Lane 2 would re-run a known-null experiment at 5-10x the
  cost without testing the actual hypothesis (indirect-injection data
  overcoming the active-harm LoRA pattern). Round 1 Q3's $68 / 2-variant
  budget was implicitly LoRA-cost; Round 15 makes the implicit explicit.
  Tier C energy-loss 3rd variant (per Round 7 Q2'''''') is also LoRA
  scope.
- **Baseline scope broadened (per Round 15 Q1 user-custom)**: portfolio
  adds **TF-IDF + LogisticRegression baseline** (sklearn; CPU; ~$0) as
  classical text-classification floor. Plus retains submission's
  frozen-probe baseline + existing reference scorers (ProtectAI v1/v2 +
  Meta PG2 86M per Round 7 Tier B). Plus OPEN category for "any other
  appropriate open-source models" — not locked at Round 15; examples
  that may qualify: sentence-transformer + LR, DeBERTa-v3-base (cite
  submission v1.1.2 null), small BERT variants. Added to Lane 1
  experiment-record `protocol.md` as gates open. Each additional
  baseline is ~$0-5 inference-only; stays within base envelope.
- **Cost re-budget** (per Round 15 Q2): deferred — "we will do a better
  estimate when we get closer". $68 / Lane 2 2-variant slot in §16 base
  envelope holds; recompute at M2/M3 gate.

**Round 15 portfolio decisions** (3 locks):
- **Lane 2 parameter budget**: LoRA-only; no full-FT variant.
- **Baseline expansion**: TF-IDF added; "other appropriate open-source
  models" left open for Lane 1 protocol-level decision; frozen-probe +
  ProtectAI v1/v2 + Meta PG2 86M retained.
- **ADR-043** separate ADR at Day 17 batch (per Round 15 Q3) documents
  this scope-narrowing + baseline-expansion + cites ADR-075 as
  supporting evidence.

**Round 16 update (2026-05-21 Lane 1 baseline mechanics clarification)** —
user clarifies Round 15 baseline expansion with 2 execution-mechanics
decisions:

- **Baseline training data (Round 16 Q1; user emphasis "don't they all
  need to be comparable?")**: ALL trainable baselines (TF-IDF + LR;
  sentence-transformer + LR head; DeBERTa-v3-base; any other open-source
  trainable model added per the open category) train on the **SAME
  corpus as Lane 2 LoRA** — Lane 2's synthetic indirect-injection-heavy
  MR-3 output (~20k rows: ~10k indirect-injection positives + ~10k
  benign carriers per §5 + Lane 2 protocol.md). Comparability is the
  priority — apples-to-apples experimental design. Non-trainable
  baselines (frozen-probe; ProtectAI v1/v2; Meta PG2 86M) operate as
  off-the-shelf scorers; the trainable category (LoRA ModernBERT-base +
  TF-IDF + sentence-transformer + ...) shares the SAME training pool.
  Output: clean "is LoRA's complexity worth it on this training data?"
  comparison.
- **Baseline lock timing (Round 16 Q2; user emphasis "between 1 and 3
  since I am not sure how well researched we are")**: Lane 1 baseline
  list **locked at M1 protocol.md** (start of M1 lane work; per §18
  4-file schema = protocol.md = pre-registered design) BUT **appendable**
  via per-experiment-record protocol.md amendment if M0 dossier work
  (Days 6-12, ~60-80 files) surfaces a clearly-appropriate baseline not
  considered at M0 close. Amendment workflow: new dossier finding →
  Lane 1 hypothesis.md updated → protocol.md amendment row + commit
  with explicit cite. Pre-registered locking + rational amendment is
  the standard scientific-protocol pattern.

**Round 16 portfolio decisions** (4 locks; Round 16 Q3-Q5 added after
Q1-Q2 surfaced the cross-lane comparability principle):
- **Q1: Baseline training data**: same corpus as Lane 2 LoRA (synthetic
  indirect-injection-heavy MR-3 output ~20k rows).
- **Q2: Baseline lock timing**: M1 protocol.md lock + amendment-friendly
  during M1-M5 if dossier surfaces gaps. ADR-043 (Day 17 batch) covers
  the amendment-workflow framing.
- **Q3: Lane 4 fusion stacker training data**: same Lane 2 MR-3 corpus
  (per Round 16 Q1 comparability). Stacker `(N_samples, N_detectors)`
  score matrix computed FROM Lane 2's ~20k corpus → trained → eval'd
  on submission val + portfolio OOD slates. Direct "does stacking on
  the same training data beat best individual?" comparison.
- **Q4: Lane 5 activation probe training data**: same Lane 2 MR-3 corpus
  (per Round 16 Q1). **Overrides F1 risk resolution** which had Lane 5
  at "submission val only" — Lane 5 hypothesis becomes "does TaskTracker
  probe approach work on the SAME training data Lane 2's LoRA uses?"
  Maintains the F8 encoder-vs-decoder methodology port test framing
  + adds comparability.
- **Q5: Lane 5 timing shift**: M2 → M4 (post-Lane-2-corpus). Lane 5
  cannot run until MR-3 ships + Lane 2 synthetic generation completes
  (M3 close); probe training therefore moves to M4. Still ~2-3 days;
  Lane 5 + Lane 4 both run in the M4-M5 window after corpus is
  available. F1 risk resolution updated accordingly.

**Round 17 update (2026-05-21 narrative-structure remediation directive)** —
user complaint: submission's Quarto hub-and-spoke ("RESULTS + EXEC_SUMMARY
+ WRITEUP hub + 8 spokes + EVIDENCE + READING_GUIDE + SPEC_SHEET +
SUBMISSION_AUDIT + NEXT_STEPS + ADRs + 4 notebooks") has "neither a
narrative structure nor an academic structure like in a journal paper —
random parts of the results all over the place with no story". The
submission was reviewer-driven (maximum auditability) at the cost of
narrative cohesion. Portfolio remediates by producing **THREE SEPARATE
GUIDES** instead of ONE book, each targeting a different reader:

1. **Pedagogical Textbook** (= current 13-chapter KF triadic R/O/E
   outline from §6.2 + companion `portfolio-chapter-outlines.md`).
   Self-contained chapters; modular learning; reader picks chapters.
   Audience: practitioners learning prompt-injection detection
   methodology.
2. **Story arc / "Can we climb the wall?"** narrative. OOD wall as
   antagonist; 6 lanes as climb attempts; chapters build cumulative
   tension toward methodology lesson. **Heavy cross-chapter threading**
   per Round 17 follow-up Q3 (each chapter opens with story-recap +
   closes with hook to next; book frontmatter lays full arc).
   Audience: curious engineers + recruiters who skim narratives.
3. **Academic Journal-Paper (IMRaD-like)**. Long-form paper structure:
   Introduction → Background → Methods → Results (6 lanes as
   sub-sections) → Discussion → Future Work. Reviewer-defense-ready.
   Audience: researchers + reviewers who want compressed academic flow.

**Round 17 portfolio decisions** (4 locks):

- **Q1 (build strategy)**: ONE Astro book + 3 subsite folders.
  `book/src/content/textbook/` + `book/src/content/narrative/` +
  `book/src/content/academic/`. Astro routes: `/textbook/[slug]`,
  `/narrative/[slug]`, `/academic/[slug]`. Single npm build; shared
  infrastructure (callouts, BibTeX, KaTeX, AI-disclosure component,
  PreReleaseBanner). Each guide has its own TOC + nav. Scaffold v3.2
  research-portfolio profile per MR-8 supports each guide via union
  schema.
- **Q2 (authoring strategy)**: SHARED SUBSTRATE + 3 framing wrappers.
  `book/src/content/fragments/lane-N/{methodology,results,
  interpretation}.mdx` hold experiment-data + dossier citations
  (single source of truth). Each guide's chapter MDX imports +
  sequences fragments with its own framing prose. ~1x experiment-write
  + 3x framing-write per lane. Single experimental-data update
  propagates to all 3 guides via fragment reload.
- **Q3 (release sequence)**: SEQUENTIAL ROLLOUT.
  - **v0.7.0 M7**: Pedagogical Textbook ratified (lowest authoring
    delta from existing chapter outlines).
  - **v0.8.0 (~month 13, ~1mo after M7)**: Story arc / narrative
    guide shipped.
  - **v0.9.0 (~month 14, ~2mo after M7)**: Academic IMRaD guide
    shipped.
  - **v1.0.0 (~month 16-17, ~3-4mo after M7)**: All 3 guides polished
    + citable. Extends Round 5's v0.7.0 → v1.0.0 community-feedback
    window from 3 months to ~3-4 months to accommodate authoring.
- **Q4 (plan-level lock)**: Round 17 narrative + 4 locks added to
  plan NOW; §6 / §9 / §21 updated to reflect 3-guide architecture.
  M0 Day 14 chapter skeleton work continues with **Textbook chapters
  only** (the Round 11 v3.2 scaffold blocker still applies to textbook;
  story arc + academic guides scaffold concerns deferred to their
  respective v0.8 / v0.9 release planning).

**Round 17 implications**:
- **ADR-044** (3-guide architecture + shared-substrate authoring
  pattern + sequential rollout schedule) added to Day 17 ADR batch.
  Cites Round 17 + the submission's hub-and-spoke anti-pattern as
  motivating evidence.
- **M0 Day 14 chapter skeletons**: TEXTBOOK ONLY (13 chapters per
  existing outline). Story arc + Academic IMRaD chapters scaffold
  at v0.8+ / v0.9+ respectively. Reduces M0 chapter-skeleton scope
  from ambiguous to specific.
- **§10 may need MR-11** (book-scaffold-astro v3.3+ fragment-import
  helpers + multi-subsite route generation patterns) for the 3-guide
  Astro pattern. Defer filing to v0.8+ pre-work; portfolio's local
  impl at v0.7.0 (textbook only) doesn't need MR-11 yet.
- **Cost impact**: ~0 GPU cost (book authoring is human-time). Time
  cost: ~30-50h authoring per non-textbook guide. M7→v1.0.0 window
  extends from 3mo to 3-4mo to absorb the additional authoring.

**Round 20 update (2026-05-21 same-day eval-toolkit roadmap review per
user directive)** — user directive: "make sure we are using the most
recent version of eval toolkit and we look on my computer for it's
roadmap so we have it in mind". Reading
`~/.claude/plans/evaluate-all-the-work-twinkly-kite.md` (eval-toolkit's
v0.43→v1.0 staggered release plan) revealed eval-toolkit shipped FOUR
ADDITIONAL releases since Round 14's v0.44.0 snapshot:

- **v0.45.0** (2026-05-20): `MetaLearner` Protocol + `LogisticStacker`
  reference impl. **Closes eval-toolkit #52 = portfolio MR-6**
  (CLOSED 2026-05-21T18:22:48Z).
- **v0.46.0** (2026-05-20): `scorecard()` primary metric surface +
  `metric_specs` namespace + Tier-2 Protocols expansion. SOFT BREAKING
  (DeprecationWarning shim for top-level scalar metric names; hard
  removed at v0.47).
- **v0.46.1** (2026-05-21): hotfix — ECE strategy validation +
  warning-content fixes.
- **v0.47.0 (TODAY, 2026-05-21)**: BREAKING — `sweep()` unification +
  top-level `TextTransform` Protocol + advanced-6 character_injection
  + removal of `adversarial.sweep` / `preprocessing.sweep` /
  `character_injection` SimpleNamespace / `spotlighting` SimpleNamespace
  / per-module strategy Protocols / top-level scalar metric names
  (now AttributeError). **Closes the v0.43 forward-look re: advanced-6
  = portfolio's planned MR-10**.

**eval-toolkit roadmap forward-look (per user directive "have in mind")**:
- **v0.48.0** (planned, ~1-2 weeks): `metrics_at_threshold` key
  normalization + `BootstrapCI.to_dict()` rewrite + docstring example
  sweep + ADRs 0001 + 0003 + sweep `strategy_id` disambiguation +
  scorer-output-shape validation. **BREAKING** (additive Tier-2 schema
  expansion).
- **v1.0.0** (planned, ~4-6 weeks total per roadmap): stability
  commitment — top-level `__all__` + 10 Tier-2 Protocols frozen
  strictly; submodule public symbols additive-only; no new code.
  Portfolio's lane work (M1-M6) targets v0.47 surfaces and is
  automatically v1.0.0 compatible if v1.0.0 ships before M1 starts.

**Round 20 portfolio decisions** (3 locks):
- **Q1 (pin floor)**: `eval-toolkit[probes,losses]>=0.47` (was
  `>=0.44` after Round 14 Q2). Range-floor only — auto-bumps to v0.48+
  / v1.0+ as upstream releases ship; portfolio re-runs Day 3a-style
  consume + smoke-test verification per minor.
- **Q2 (roadmap awareness scope)**: Document v0.48 + v1.0 in Round 20
  narrative; portfolio code acts on SHIPPED APIs only (v0.47 surfaces).
  No code references v0.48-unreleased APIs (e.g., `strategy_id`
  disambiguation in sweep — defer consumption to v0.48 ship).
- **API contract pivot (load-bearing for all Lane work)**: portfolio
  code uses **v0.47 canonical surfaces exclusively** — `scorecard()` +
  `metric_specs.*` for evaluation; top-level `sweep(strategies, texts,
  scorer=None, attack_threshold=None)` for transformations;
  `TextTransform` + `Probe` + `MetricSpec` + `MetaLearner` Protocols
  for typing; the 12 dataclass strategies in `eval_toolkit.adversarial`
  (`ZeroWidthSpaceInjection`, `HomoglyphSubstitution`, ...,
  `InvisibleCharsInjection` — `ALL_TECHNIQUES` 12-tuple); the 3
  dataclass strategies in `eval_toolkit.preprocessing` (`DelimitVariant`,
  `DatamarkVariant`, `EncodeVariant`). **REMOVED FROM PORTFOLIO PLAN
  REFERENCES**: SimpleNamespace patterns (`character_injection.zero_width_space()`
  style); per-module Protocols (`CharacterInjectionStrategy`);
  module-level sweeps (`adversarial.sweep()`); top-level scalar metric
  imports (`from eval_toolkit import pr_auc`).

**Round 20 implications**:
- **MR-6 (eval-toolkit #52) state → `released-v0.45.0`** + auto-pinned
  via Round 20 pin floor. Drop from "open MRs to monitor" list.
- **MR-10 OBSOLETED** — advanced-6 shipped in v0.47.0 as part of the
  12-technique consolidation. Day 4 MR-10 filing step CANCELED.
  Replace Day 4 with: confirm v0.47.0 ships all 12 character_injection
  dataclasses via `eval_toolkit.adversarial.ALL_TECHNIQUES`; Lane 1b
  matrix can use full 12 from M1 start (round-5 Q1 "Wait for v0.43.1"
  pattern resolves favorably).
- **Lane 1b scope simplified** — §5 + §17 Ch 8 outline drops the
  "core-6 at M1 + advanced-6 backfill" sequencing; M1 starts with full
  12-technique matrix.
- **API smoke-tests OVERHAULED for v0.47 conventions** (Day 3a step 4):
  uses `scorecard()` + `metric_specs` for evaluation; `sweep()` from
  top-level; 12 dataclass instantiation + `TextTransform` Protocol
  check; `LogisticStacker` direct construction. No SimpleNamespace
  syntax; no scalar metric imports.
- **Open upstream MRs remaining (Round 20 reduced set)**: MR-3
  (research_toolkit #1 /dataset-synthesize, M3-blocking); MR-8
  (book-scaffold-astro #6 v3.2 research-portfolio profile, M1 book
  authoring blocker); MR-9 (book-scaffold-astro #7 generic frontmatter,
  not blocking). **NO open eval-toolkit MRs** (#59 advanced-6 is
  open in tracker but the work shipped in v0.47.0; eval-toolkit
  housekeeping will close at v0.48 cleanup).
- **ADR-045** (Round 20 cascade) added to Day 17 ADR batch.

**Round 21 update (2026-05-21 same-day book-scaffold-astro + submission resurvey)** —
extending Round 20 review to other load-bearing libraries surfaced
that book-scaffold-astro ALSO jumped multiple minors in the same 2-day
window (v3.1.0 → v3.6.0) + submission advanced v1.2.12 → v1.2.16:

- **book-scaffold-astro v3.2.0..v3.6.0** (2026-05-19..21): shipped
  the research-portfolio preset via v3.5.0 + closed both portfolio-
  filed scaffold MRs:
  - **MR-8 (book-scaffold-astro #6) CLOSED 2026-05-19T19:29:53Z** by
    v3.5.0 — research-portfolio preset SHIPPED with the union schema
    (academic ∪ tools) + 4 new generalized components + recipe +
    chapter template. Scaffold maintainer's CHANGELOG explicitly
    cites: "Unblocks downstream prompt-injection-portfolio M1 book
    authoring." **Resolves Round 11 Q1'''''''' blocker.**
  - **MR-9 (book-scaffold-astro #7) CLOSED 2026-05-19T19:04:30Z** by
    v3.3+ — generic frontmatter primitive SHIPPED.
  - v3.6.0 (2026-05-21): adds `katexMacros` consumer-defined macros
    option (closes #22) — not portfolio-critical but useful for
    deepest L3 chapter typography.
- **Submission v1.2.13..v1.2.16** (2026-05-19..21): patches tracking
  eval-toolkit's v0.46 → v0.47 pin bumps + library_imports.md
  trimming to fit upstream's 1200-char cell limit. Latest tag
  `v1.2.16`. Portfolio CI ref pin (per Round 14 Q1 dynamic-detection)
  auto-tracks via `git ls-remote --tags origin | sort -V | tail -1`.
- **research_toolkit (#1 MR-3 /dataset-synthesize) STILL OPEN** —
  unchanged. Remains M3 blocker. Portfolio waits for upstream ship.

**Round 21 portfolio decisions** (3 locks):

- **Q1 (scaffold pin floor)**: `^3.1.0` → `^3.5.0` (user picked option
  B over Recommended A `^3.6.0`). Matches the version that closed
  MR-8; skips v3.6.0 katexMacros (not currently needed for
  portfolio's chapter outlines). `npm update` will pick up v3.5.x
  patches automatically within the caret range.
- **Q2 (Day 14 unblock)**: Day 14 chapter skeleton work UNBLOCKED at
  M0. The Round 11 Q1'''''''' v3.2 scaffold blocker resolves
  favorably — v3.5.0+ ships research-portfolio preset. Day 14
  proceeds as planned (textbook chapters per Round 17 Q4); no
  timeline impact.
- **MR-3 remains only OPEN MR** — M3-blocking research_toolkit
  /dataset-synthesize. Portfolio monitors at Day 13 + escalates if
  M2/M3 approaches without upstream ship.

**Round 21 implications**:
- **§3 dependency policy**: `book/package.json` pin bumps
  `@brandon_m_behring/book-scaffold-astro: ^3.5.0` (was `^3.1.0`).
  Day 3a/c1 commit covers this alongside eval-toolkit pin bump.
- **§10 library-first audit table**: MR-8 + MR-9 rows advance to
  `released-vX.Y.Z` + `pinned-needed`.
- **§21 Day 14 "WAITS for scaffold v3.2.0"** — REMOVED. Chapter
  skeleton authoring proceeds with v3.5.0 research-portfolio preset
  (which is the superset Round 12 designed). Day 14 pre-condition
  becomes: confirm `book/package.json` pins `^3.5.0`.
- **ADR-046** (Round 21 cascade) added to Day 17 ADR batch.
- **Open upstream MRs at Round 21 close**: MR-3 only (research_toolkit
  #1). 6 of 9 originally filed are now closed (MR-1/2/4/5/6/7 in
  eval-toolkit + MR-8/9 in book-scaffold-astro); MR-10 obsoleted; only
  MR-3 + the no-longer-filed MR-11 (potential v3.3+ fragment-import
  helper for portfolio's 3-guide pattern, deferred to v0.8+ per Round
  17) remain on the open-tracking list. Portfolio's M0 upstream
  surface is essentially complete.

**Submission forward-look (Round 21 context)**: submission's
`CLAUDE.md` was updated to anticipate v1.3.0 with new ADR-078
(EXECUTIVE_SUMMARY absorption) + ADR-079 (two-guide reader
architecture). The two-guide architecture VALIDATES portfolio's
Round 17 3-guide direction (similar pattern at a smaller scale).
Portfolio doesn't need to wait for v1.3.0; dynamic-detection picks
up whatever's pushed. ADR-079 isn't yet written (file doesn't
exist); CLAUDE.md preview reflects intent, not state.

**Round 22 update (2026-05-22 M0 finish-out planning post-Day-3b)** —
After Day 3b close + v0.1.0-pre tag landed (4 commits: bc30c52 +
cbf7d25 + 8d6a60d + 6c75693 + 81765f7 + 0a4938a; 10 commits total on
main), the autonomous /loop hit Anthropic's output content-filter
mid-Day-15 governance batch — SECURITY.md (135 lines, dual-use
disclosure + responsible-disclosure policy) landed cleanly, but the
NEXT write in the batch (presumed `CODE_OF_CONDUCT.md` or an issue
template) was blocked at the model-output layer with HTTP 400 +
"content filtering policy" error. Submission v1.3.0 also shipped this
morning (per MEMORY.md update: two-guide reader architecture +
WRITEUP_PAPER + WRITEUP_NARRATIVE + EXECUTIVE_SUMMARY retired + 79
ADRs); portfolio's submission CI ref is still at v1.2.16 (Round 21).

**Round 22 portfolio decisions** (4 locks):

- **Q1 (content-filter strategy)**: **pre-vet each Write content for
  dual-use trigger phrases** (specific attack technique discussions,
  exploit details, prompt-injection corpus examples) + soften where
  possible before send. Slower iteration than blind retry but lower
  trip rate. Applies to: CODE_OF_CONDUCT.md + ADR content discussing
  attack methods + chapter skeletons for Ch 7-12 (lane experimental
  content) + Lane 1b adversarial section in ETHICS revisions.
- **Q2 (dossier sprint deferral)**: Days 6-12 dossier work (~60-80
  files via research_toolkit) **DEFERRED entirely to next user-led
  session**. Rationale: research_toolkit's `/research-plan` +
  `/research-gather` + `/dossier-build` + `/dossier-audit` skills
  aren't in autonomous /loop's available skill set; compass artifacts
  at `~/Downloads/compass_artifact_*.md` (3 files, ~1055 lines total)
  need user-led ingestion + decomposition. M0 v0.1.0 close window
  extends 2-3 days from plan §21 Day 19 estimate to absorb the
  dossier deferral.
- **Q3 (CI ref bump)**: advance submission ref `v1.2.16` → `v1.3.0`
  as a Round 22 mini-commit. Single-line edit to
  `.github/workflows/ci.yml` + update `pyproject.toml` comment line.
  v1.3.0 two-guide reader architecture (WRITEUP_PAPER + WRITEUP_NARRATIVE
  replacing single-hybrid WRITEUP.md) ALIGNS with portfolio's Round 17
  3-guide direction; pin advance is the immediate evidence-tracking
  win.
- **Q4 (priority order for remaining M0 work)**: risk-minimizing
  front-load — order autonomous work by content-filter risk (low →
  high) + by user-input-independence:
  1. **Round 22 mini-commit**: CI ref bump v1.2.16 → v1.3.0 (~5 min;
     zero content-filter risk)
  2. **Day 16**: Docker T2 setup — `Dockerfile` + `compose.yaml` +
     update `scripts/verify_docker.py` (~30 min; low risk)
  3. **Day 5** (vacated by Round 14): 6 experiment-record dirs × 2
     files (`hypothesis.md` + `protocol.md` skeleton) = 12 files +
     update `experiments/MANIFEST.json` (~30 min; low risk — pre-vet
     hypothesis statements for attack-corpus language)
  4. **Day 14**: 13 textbook chapter skeletons in
     `book/src/content/textbook/`; Round 21 UNBLOCKED via scaffold
     v3.5 research-portfolio preset (~60-90 min; medium risk — Ch 7-12
     are experimental chapters discussing attack methods; pre-vet)
  5. **Day 15 finish**: 5 governance files (CODE_OF_CONDUCT.md + 3
     issue templates + PR template + 4 frontmatter MDX files + README
     polish for 3 peer-level entry-points per Round 17 follow-up Q3)
     — pre-vet content for each Write (~60 min with pre-vet overhead)
  6. **Day 17 ADRs**: bulk-draft ~35-37 ADRs from `§1` decision
     tables. Pre-vet ADR content for attack-method discussions
     (especially ADRs 022/041 ETHICS + 027 retired metrics) (~3-4 h)
  7. **Day 18 build-in-public templates**: weekly/monthly post
     templates + announcement-draft template; defer actual account
     creation + handles to user-led session (~15 min)
  8. **Day 19 prep**: M0 close pre-flight — verify ratify-milestone
     command works against current state; document gaps that need
     user-led ratify (dossier presence + announcement post)
     (~15 min). Actual `git tag v0.1.0` + `gh release create v0.1.0`
     + announcement thread DEFERRED to user-led session.

**Round 22 implications**:
- **M0 v0.1.0 close timeline extends ~2-3 days** beyond plan §21 Day
  19 estimate due to dossier deferral. Calendar impact: M7 ratify +
  v0.7.0 tag (per plan §9 13-14 week timeline) shifts proportionally.
- **Autonomous /loop work bounded to ~6-7 hours** of Claude execution
  across Days 5/14/15/16/17/18 + Round 22 mini-commit. Day 19
  formal ratify + tag stays user-led.
- **ADR-047** (Round 22 cascade — M0 finish-out strategy + content-
  filter handling + dossier deferral + CI ref v1.3.0 bump) added to
  Day 17 ADR batch.
- **Day 15 SECURITY.md landed but uncommitted** — fold into Day 15
  finish batch when CODE_OF_CONDUCT.md + templates + frontmatter
  land. Round 22 ADR-047 cites SECURITY.md as the pre-content-filter
  artifact.
- **Memory updates**: at autonomous-loop close (post-Day-18), update
  `portfolio_plan_approved.md` with Round 22 + Day 5/14/15/16/17/18
  progress; bump MEMORY.md description suffix.

**Round 23 update (2026-05-22 cross-machine handoff)** — user is
moving to a different computer for the dossier sprint + subsequent
lane work. To enable clone-and-resume on the new machine, in-repo
copies of the planning + research-survey artifacts are committed to
public locations.

**Round 23 portfolio decisions** (2 locks):

- **Q1 (public-vs-tarball)**: **ALL PUBLIC**. Commit all 8 staged files
  + 2 README indices to public repo (Round 23 follow-up Q1 user-locked).
  Deviation from the submission-pattern hybrid (compass-public +
  planning-private analog of submission's transcripts-private
  convention). Maximum cross-machine portability + transparency about
  the design process; consistent with Round 17 3-guide transparency
  direction.
- **Q2 (tarball scope)**: **NOT needed**. User clarified "this new
  repo portfolio doesn't need transcripts anymore" — the public-repo
  commit covers cross-machine continuity; no auxiliary tarball. Memory
  dir + `~/.claude/` state stay on origin machine; user syncs
  separately if needed.

**Files committed (Round 23)**:

`docs/planning/` (5 planning artifacts + index):
- `PORTFOLIO_PLAN.md` (renamed from
  `~/.claude/plans/i-want-to-consider-merry-milner.md`; the master plan
  ratified across 22 `/exploring-options` rounds; ~2032 lines)
- `portfolio-chapter-outlines.md` (13-chapter KF-decomposed outline)
- `portfolio-experiment-record-template.md` (4-file schema)
- `portfolio-lane-execution-playbooks.md` (6 per-lane playbooks)
- `eval-toolkit-v0.43-to-v1.0-roadmap.md` (renamed from
  `evaluate-all-the-work-twinkly-kite.md`; upstream roadmap referenced
  by ADR-045 Round 20 v0.47 pivot)
- `README.md` (planning artifacts index + how-to-read guide +
  cross-references)

`docs/research/compass-survey/` (3 compass surveys + index):
- `01-detector-landscape.md` (Anthropic Compass survey; 500 lines)
- `02-direct-vs-indirect-deep-dive.md` (218 lines)
- `03-training-and-evaluation-methodology.md` (337 lines)
- `README.md` (compass-survey index + Days 6-12 dossier-sprint
  workflow pointer + Anthropic Compass provenance/license)

**Round 23 implications**:

- **NEXT_SESSION.md + M0_READINESS.md** update to reference in-repo
  paths (no longer point at `~/.claude/plans/` or `~/Downloads/`).
  Fresh-clone session has full state from the repo alone.
- **Update policy** (per `docs/planning/README.md`): future plan
  edits land at BOTH `~/.claude/plans/i-want-to-consider-merry-milner.md`
  (working copy on origin machine) AND
  `docs/planning/PORTFOLIO_PLAN.md` (in-repo authoritative-for-cross-
  machine copy). Drift between the two surfaces is a known carrying
  cost; commit cadence aligns the two at each `/exploring-options`
  round close.
- **ADR-048** (Round 23 cross-machine handoff strategy) added to the
  Day 17 ADR batch carryforward (or Day 19 close batch since Day 17 +
  Round 22 ADR-047 already landed).
- Portfolio's deliberative-content posture (originally aligned with
  submission's private-transcripts convention) **shifts to
  fully-public** for the planning artifacts. This is a portfolio-
  specific choice consistent with the case-study narrative; not a
  generally-recommended pattern for projects with confidential
  competitive context. User-locked at Round 23 Q1.

**Round 23 follow-up locks** (execution mechanics):

- **Q1 (plan-file SoT)**: in-repo authoritative; on origin machine
  symlink `~/.claude/plans/i-want-to-consider-merry-milner.md` →
  `<portfolio-repo>/docs/planning/PORTFOLIO_PLAN.md` so future
  plan-mode edits land in-repo automatically. New machine: clone repo
  + create symlink on first setup. Eliminates dual-copy drift; one
  canonical source. Origin's symlink:
  `ln -sf ~/Claude/prompt-injection-portfolio/docs/planning/PORTFOLIO_PLAN.md
   ~/.claude/plans/i-want-to-consider-merry-milner.md`
  (after moving the current content to the in-repo location).
- **Q2 (filenames)**: keep the renames. `PORTFOLIO_PLAN.md` +
  `eval-toolkit-v0.43-to-v1.0-roadmap.md` are reader-friendly + match
  other portfolio meta-docs. The auto-slug originals stay only as
  symlinks on origin machine for plan-mode convention; in-repo
  authoritative names are the public surface.
- **Q3 (handoff docs)**: keep all 3 (`NEXT_SESSION.md` +
  `M0_READINESS.md` + `docs/planning/README.md`) with sharper scoping.
  Each top-of-file documents its scope:
  - **NEXT_SESSION.md** = cold-start anchor (install instructions +
    18-commit summary + critical context + what-NOT-to-do)
  - **M0_READINESS.md** = `make ratify-milestone` gates + user-led
    TODO checklist (dossier sprint + accounts + formal tag)
  - **docs/planning/README.md** = index of design rationale + how to
    read planning artifacts + update-policy

### Round 24–26 cascade — M0 technical close + pre-modeling EDA arc (2026-05-23 → 05-29)

Continues the Round 20→23 cascade above; records the post-`v0.1.0-pre` work through the close of the pre-modeling EDA arc. No discrete R25 lock (R24 → R26).

- **M0 technical close (2026-05-23)** — all §21 ratification gates green (reconciled in §21 below) at `v0.1.0-pre`+68 commits. The formal `v0.1.0` tag (`git tag` + `gh release`) and the build-in-public announcement remain **user-led** (accounts not yet created); see `M0_READINESS.md`.
- **Round 24 (2026-05-23) — dossier Sprint 2 + close policies.** 3-topic → **5-topic** dossier (210 bib_ledger / 347+ evidence / 157 BibTeX / ~124 cached PDFs); detailed in §4 "Round 24 update". Three policy ADRs locked: **ADR-048** (cross-classification — topic-prefixed bibkeys), **ADR-049** (body-quote anchoring discipline), **ADR-050** (vendor-cluster posture — unverified-by-design).
- **Round 26 (2026-05-26) — dogfood adoption + study reorientation.** **ADR-051**: eval-toolkit pin floor `>=0.47`→`>=1.0` (v1.6.0 in `uv.lock`); book-scaffold `^3.5`→`^4.4.0`; `research_toolkit` dropped as a dep → repo-local tooling clone; DF-1..4 consumer-friction issues filed upstream. **ADR-052**: attack-type-generalization study design (axis C: type-LODO + joint carrier×attack shift); executable spec at `docs/planning/attack-type-lodo-harness-spec.md`.
- **Pre-modeling EDA arc (2026-05-26 → 05-29, Phases 0–3; executed under the EDA plan, not a numbered round).** RC0 BIPIA adequacy = **GO**; 13-dataset verified-spec survey (`configs/data/dataset_specs.yml`); 5 leaky splits + 3 mislabels caught. Phase 3 recorded a **pre-registered, falsifiable OOD-wall prediction** (`experiments/eda/OOD_WALL_PREDICTION/{criteria.md, results.json, FINDINGS.md}`). Headline finding: **the carrier dominates the MiniLM embedding** — the attack-type signal is embedding-invisible (silhouette by-carrier 0.197 vs by-attack-type −0.023; KMeans→carrier ARI 0.98 vs →attack-type −0.001). eval-toolkit `eda` layer shipped + consumed at **v1.6.0**.
- **Open tracked items (GitHub Issues):** **#1** (`P3`) rerun V10 with Prompt-Guard-86M once the Meta Llama gate is granted; **#2** (`P2`) run the OOD-wall falsification (top-k vs bottom-k) when Lane-1 produces per-test-attack-type LODO gaps.
- **Next phase:** the ADR-052 attack-type-LODO modeling study (Lane 1) — the unblocked path that produces the per-type gaps gating issue #2.

### Round 27 update — milestone rethink: EDA-arc placement + conditional rescope gates (2026-05-29)

Post-EDA-arc review of the M0→M7 ladder (locked pre-EDA, R1–R7). The Phase-3 findings (**carrier dominates the embedding; the attack-type signal is embedding-invisible**) **reframe value-props but falsify none of the six lane hypotheses**, and the Zone-2 dossier rescopes are all *conditional* (trigger-gated). Per **ADR-052** ("this ADR locks the *design*, not the lane reorganization; lane/chapter restructure is deferred to Phase 3 — after results"), a full re-ladder now would be premature. This round records only what is settled and registers the branch-points; it does **not** reorganize lanes.

**Decisions locked** (3):
- **Q1 (EDA-arc placement)**: the pre-modeling EDA arc (Phases 0–3) is recorded as **M1's entry-gate / pre-flight**, not a new milestone — the ADR-052 attack-type-LODO study *is* M1's Lane-1 modeling, and the EDA arc was its pre-registration + RC0 go/no-go. §9's "8 milestones M0-M7" header is unchanged (no rung added).
- **Q2 (conditional rescopes)**: the Lane 1b / Lane 4 / Lane 5 rescope proposals (`dossier_implications_for_roadmap.md` Zone 2) are **promoted to named trigger-gates in §16** beside the existing M1→M2 / M3→M4 gates — registering the branch-points without committing to any branch until a trigger fires.
- **Q3 (full re-ladder)**: **deferred to post-LODO-results** per ADR-052. The committed Round 24–26 narrative above stands as historical record (not rewritten).

**Implications**:
- §16 execution-order guide gains a Round-27 EDA-arc **M1 entry-gate** + **3 conditional rescope gates** (Lane 1b / Lane 4 / Lane 5), each cross-referencing `dossier_implications_for_roadmap.md` as the canonical detail (register, don't duplicate).
- The EDA findings **reframe Lane 1's value-prop**: from "we trained a detector" to "we measured operating-point honesty" (the field's floor is already laid; the contribution is saturation-aware reporting — `dossier_implications` Zone 2). Lane 1's *hypothesis* and milestone (M1) are unchanged.
- No ADR filed (ADR-052 already governs the deferral; ADR-053 left available for when the LODO results actually trigger a re-ladder).

### Round 30 update — post-M1 milestone re-ladder: the multi-axis capacity-dependent spine (2026-06-01)

The re-ladder deferred at Round 27 (and at **ADR-052**, "restructure deferred to Phase 3 — after results") is now run: M1 (attack-type-LODO, Lane 1) closed on 2026-06-01 with its §6.5 verdict, meeting the deferral condition. This `/exploring-options` round folded two input streams — `milestone-rethink-inputs.md` (the M1 result) + `dossier_implications_for_roadmap.md` Zone 2 (the dossier rescopes) — and reorganizes **narrative + lane framing + the M1→M2 sequencing checkpoint only**. It does **not** re-sequence milestones (still M0→M7) and does **not** re-open M1.

**The pivot:** M1's §6.5 falsification is **capacity-dependent and attack-type-axis-only** — tfidf +0.135 / frozen +0.082 **SURVIVE**, `lora` −0.003 **FALSIFIED** (`falsification_verdict.json`), with M1 holding the carrier constant by design. So "there is an OOD wall" splits into axes.

**Decisions locked** (5):
- **Spine → multi-axis, capacity-dependent**: *OOD is several axes; the **attack-type** axis is capacity-dependent (end-to-end LoRA dissolves it), the **carrier** axis dominates the geometry and is the standing wall.* [**Refined 2026-06-01** by the carrier-LODO verdict → *capacity-attenuated, residual, table-concentrated* (not a fully standing wall; G(lora)=+0.067 vs G(frozen)=+0.167); see §16 carrier-LODO **RESOLVED** + `experiments/carrier-lodo/FINDINGS.md`. Formal ADR-055 amendment deferred.] Stronger, more precise — a pre-registered falsification overturned only at the LoRA ceiling. Carries the **submission reconciliation**: backbone-invariant (submission's v1.1.2 DeBERTa carrier null) ≠ capacity-invariant, and the submission measured **carrier** while M1 measured **attack-type within indirect** — the multi-axis spine unifies them, no contradiction.
- **Lane 2 → re-point to the carrier axis**: method UNCHANGED (LoRA-retrain + 2-variant loss per **ADR-043**); evaluation axis moves from attack-type (M1 answered it: LoRA generalizes near-perfectly) to **carrier generalization** on the available set (email/code/table; qa/abstract license-gated). "Confirm attack-type generalization" becomes a cheap §16 optional secondary.
- **Lane 5 → sharpened, gate kept**: recover the signal from **intermediate** activations (between the embedding-invisible final layer and the LoRA-visible end-to-end signal); the M3-entry **d′ > 0.5** gate stays as the port-only-vs-surface-third-path decision; CaMeL / capability-isolation stays the flagged lead alternative.
- **§16 rescope gates → both untripped, one watch-note**: M1 tested **neither** the Lane 1b (Hackett char-injection ASR) nor the Lane 4 (saturation) trigger — both stay registered as-is. New **Lane-4 watch-note**: M1's 0.98–0.999 LoRA AUPRC foreshadows the saturation gate (revisit at M5-close).
- **Converge → reframe + ADR-055 + one sequencing tweak**: insert a **carrier-LODO validation gate** at **M1-exit → Lane 2-entry** (an M2 pre-flight, mirroring the EDA-arc-as-M1-entry-gate pattern). The gate reuses the attack-type-LODO harness with the LODO axis swapped to **carrier** and a **carrier-clustered** estimator (§6.5 was payload-clustered), criteria pre-registered before any run. It answers: does LoRA dissolve the carrier gap too (spine revised) or does carrier persist under LoRA (spine validated), and sizes Lane 2's scope. **Scheduled now; the run is a separate present-first go.**

**Implications**:
- The "carrier is the standing wall" half of the spine is currently **geometric, not a modeling result** (silhouette by-carrier 0.197 vs by-attack-type −0.023; KMeans→carrier ARI 0.98 — `OOD_WALL_PREDICTION/FINDINGS.md`). The carrier-LODO gate converts it to a modeling result or revises the spine — that is the gate's whole purpose; until it runs, prose must name the axis + capacity regime of every "wall" claim.
- §16 gains the carrier-LODO gate + the Lane-4 watch-note + a one-line "1b/4 untripped by M1" confirmation (Round-30 gates subsection). §9 gains the M2 pre-flight checkpoint. §5 re-points the Lane-2 framing and re-axises "structural wall (likely)" (M1 showed the *attack-type* wall is not structural; the open structural question is the *carrier* wall). §17 Ch 7/8/9/12/13 outlines re-axis (canonical detail lives in those sections + the chapter-outlines companion — register, don't duplicate).
- A new `experiments/carrier-lodo/criteria.md` pre-registration is owed **before** that run (carrier-clustered estimator; §6.5 decision rule reused byte-for-byte). Cost: tfidf/frozen local (free) + `lora` ~$1 → base-budget; **ADR-014** stays Reserved.
- **ADR-055 filed** (discharges ADR-052's Phase-3 deferral + the Round-27 placeholder; builds on ADR-054; supersedes nothing).

---

## 1. Decisions locked via `/exploring-options` (17 questions across 3 rounds)

### Round 1 (Q1-Q7): architecture + sequencing
| # | Decision | Choice |
|---|---|---|
| Q1 | Repo name | `prompt-injection-portfolio` |
| Q2 | Cost cap | $250 base + $100 contingency, unlocks gated (ADR-013) |
| Q3 | Lane 2 loss ablation | 2-variant pre-committed: CE + Recall@LowFPR (~$68 GPU) |
| Q4 | Lane 1b + Lane 3 breadth | Full 12 char-injection + all 3 Spotlighting variants. **Round 20 simplifies** (was Round 14 Q3 + round-5 Q1 6+6 sequencing): M1 starts with full 12-technique matrix — all 12 dataclasses ship in eval-toolkit v0.47.0 (`ALL_TECHNIQUES` 12-tuple); MR-10 OBSOLETED. |
| Q5 | Lane 4 adaptive eval | 5K LLMail-Inject stratified + PINT-EN 3,016 |
| Q6 | Dossier target | Exhaustive ~60-80 files |
| Q7 | License + HF naming | Apache-2.0 + CC-BY-4.0 + `BBehring/prompt-injection-{rung}-indirect-v2-{variant}` |

### Round 2 (Q1'-Q5'): positioning + reproducibility + authoring
| # | Decision | Choice |
|---|---|---|
| Q1' | Public-facing positioning | Hierarchical depth architecture; book = L3 ground truth |
| Q2' | Reproducibility tier strategy | All 4 tiers: T0 + T1-blueprint + T2 Docker + T3 selective notebooks |
| Q3' | Chapter authoring sequence | Skeleton-first at M0 + just-in-time prose fill |
| Q4' | Submission patch policy | v1.0.x bug-fix patches; ADRs frozen at v1.0.1 (ADR-017) |
| Q5' | Notebook publication | Inside `book/src/content/notebooks/`; jupytext-paired; nbval-gated |

### Round 3 (Q1''-Q5''): public-facing + governance + commitment
| # | Decision | Choice |
|---|---|---|
| Q1'' | Author identity | AI-assisted-research disclosure in book frontmatter; sole author + Co-Authored-By in commits (ADR-021) |
| Q2'' | Repo visibility timing | Public from M0 + pre-alpha banner until v0.7.0 (ADR-024) |
| Q3'' | Ethics + synthetic data disclosure | ETHICS.md + HF Hub dataset card with dual-use disclosure (ADR-022) |
| Q4'' | External communication | Continuous build-in-public: weekly Twitter/X + monthly Mastodon + per-milestone blog post (ADR-023) |
| Q5'' | Future maintenance | v0.7.0 → v1.0.0 cutover at ~3 months; then v1.0.x patch-only mode (ADR-025) |

### Round 4 (Q1'''-Q5'''): technical details + book authoring + governance files
| # | Decision | Choice |
|---|---|---|
| Q1''' | Single-class slate metric | Val-fixed TPR only; no AUPRC/AUROC on single-class slices; submission **v1.0.8** patch retroactively applies (ADR-027). Tag adjusted: submission is now at v1.0.7. |
| Q2''' | Lane 2 ratio | 1:1 paired locked as controlled-experiment design; hard-negative-mining deferred to v0.8 Lane-7 |
| Q3''' | Community governance | SECURITY.md + Contributor Covenant v2.1 + 3 issue templates + PR template + ETHICS.md cross-refs (ADR-028) |
| Q4''' | Book citation infrastructure | **Scaffold v2.0 provides this**: `Cite.astro` (bibkey-based, hyperlinked) + `MarginNote.astro` + `references.astro` page. BibTeX → JSON via `scripts/build-bib.mjs`. Hybrid 3-surface pattern aligns with scaffold's academic profile (ADR-029). |
| Q5''' | README structure + banner | Scientific-abstract-scaled: Problem → Why → Approach → Results → Supporting; educational-framed pre-alpha banner (ADR-030) |

### Round 5 (Q1''''-Q4''''): post-survey realignment (book-scaffold-astro v2.0.0 + submission v1.0.7)
| # | Decision | Choice |
|---|---|---|
| Q1'''' | book-scaffold-astro profile | **Reframed in Round 6 (v3.0 npm pivot)**: use academic profile + portfolio-local extras at v0.1.0; file upstream design issue for v3.1 "research-portfolio" profile but do NOT block on PR. (ADR-031 reframed) |
| Q2'''' | Chapter/notebook state machine | **Adopt scaffold's 7-state system as-is**: `implemented` / `chapter_only` / `reading_only` / `prose_only` / `code_only` / `scaffolded` / `planned`. Drops the prior 4-state freshness machine. Pre-alpha banner = separate repo-wide dimension. (ADR-032) |
| Q3'''' | T0 reproducibility strategy | **Reframed in Round 6 (T0 wired upstream)**: portfolio writes own clean T0 (does NOT consume submission's eval_from_hub.py). ADR-033 dropped. See Round 6 Q1'''''. |
| Q4'''' | Portfolio notebooks vs submission notebooks | **Reference submission's 4 jupytext notebooks (`docs/benchmark/{01-04}.ipynb`) as foundation; portfolio adds only NEW analyses**: Lane 1b 12-technique matrix, Lane 9 attribution table, Lane 12 activation probe, Ch 5 bootstrap walkthrough, Ch 6 threshold policy. Future portfolio work (v0.8+) may iterate. (ADR-034) |

### Round 12 (Q1'''''''''-Q2'''''''''): scaffold v3.2 research-portfolio profile design
| # | Decision | Choice |
|---|---|---|
| Q1''''''''' | v3.2 profile schema composition | **Union: academic ∪ tools schema**. Frontmatter accepts BOTH part+week (academic) AND volatility+sources+tools_compared (tools); fields that are mandatory in one and absent in the other become optional in the union. 38 existing components stay flat (no profile subdirs; already flat in v3.1). 3 NEW components ship as scaffold primitives (see Q2). Profile selector: `npx @brandon_m_behring/create-book <name> --profile=research-portfolio`. Recipe addition: `recipes/12-research-portfolio-getting-started.md`. Template: `examples/chapter-template-research-portfolio.mdx`. Versioning: v3.2.0 (semver-minor; backward-compatible since adding a profile doesn't break existing consumers). |
| Q2''''''''' | Generalize 3 new components for v3.2 (reusable across other research portfolios) | **PreReleaseBanner.astro** (configurable: `state='alpha'|'beta'|'rc'|'locked'`, `dismissAt?: tag`, `message?: string`) replaces portfolio-specific PreAlphaBanner; **PolicyRef.astro** (generic cross-document citation: `file + section + label` props; renders link to any repo-root markdown policy like ETHICS.md / SECURITY.md / CODE_OF_CONDUCT.md) replaces portfolio-specific EthicsRef; **AICollaborationDisclosure.astro** (renders disclosure paragraph from YAML config: `model + role + commit-attribution-format`) replaces portfolio-specific AIAssistanceDisclosure. All 3 reusable; portfolio passes its specific props at consumption. |

### Round 11 (Q1''''''''-Q3''''''''): book formatting depth-check (scaffold v3.1.0 readiness)
| # | Decision | Choice |
|---|---|---|
| Q1'''''''' | Volatility schema + tools features in academic profile | **WAIT for scaffold v3.2 research-portfolio profile (block M1 book authoring until shipped)**. MR-8 promoted from "deferred to v0.8+" → "**BLOCKING M1 book authoring start**". File upstream design issue at M0 day 1; M0 dossier + ETHICS + repo + MR-1/2/7 + governance + Docker + ADRs proceed in parallel; chapter-skeleton authoring on Day 14 (per §21) waits for v3.2 npm release. |
| Q2'''''''' | Frontmatter structure (5 pages) | **`src/content/frontmatter/` collection + `[slug].astro` dynamic route** as portfolio-local solution at M0. **AND** file upstream GH issue against scaffold for generic frontmatter primitive (Zod schema + route helper). Per user: "this will be a common problem and I want a long term maintainable solution for everyone" — portfolio's local impl is the prototype; eventual scaffold v3.3+ contribution is the durable fix. |
| Q3'''''''' | Build-in-public archive structure | **`src/content/blog/` collection inside book + route via `/blog/[slug].astro`**. Lightweight Zod schema (slug + date + title + draft + week). Inside book = search-indexable via Pagefind + archival + uniform Cite/MarginNote/KaTeX access. ~30 min M0 setup. |

### Round 6 (Q1'''''-Q4'''''): overnight realignment (book-scaffold-astro v3.0 npm + submission v1.1.2 DeBERTa null)
| # | Decision | Choice |
|---|---|---|
| Q1''''' | T0 strategy (re-asked) | **Portfolio writes own clean T0**. Does NOT consume submission's eval_from_hub.py despite its now-wired state. Maintains "next version, done cleaner" framing. (ADR-035 — supersedes ADR-033) |
| Q2''''' | Scaffold consumption | **Academic profile via npm + portfolio-local extras**. `npx @brandon_m_behring/create-book prompt-injection-portfolio --profile=academic`. Portfolio adds: volatility schema field, T1-T4 source tier enum, pre-alpha banner, ETHICS reference, AI-disclosure. File upstream design issue for v3.1 research-portfolio profile; do NOT block M0 on it. (ADR-031 reframed) |
| Q3''''' | Lane 2 hypothesis + Ch 7 incorporation of DeBERTa null | **Yes — backbone-dominant evidence in Lane 2 + Ch 7**. Lane 2 hypothesis sharpens to include "AND backbone invariance" question. |
| Q4''''' | Plan cleanups | **Drop ADR-027** (single-class metric upstream-enforced), **drop ADR-033** (T0 deferral reversed), **defer MR-8** (v3.1 profile PR) to v0.8+, **drop Task #14** (submission v1.0.2 patch obsolete). |

### Round 7 (Q1''''''-Q2''''''): holistic-review additions (Tier A + B + C roadmap)
| # | Decision | Choice |
|---|---|---|
| Q1'''''' | Tier B low-cost additions | **All 4 folded** (~$20-25): Meta PG2 86M reference scorer in Lane 1; CourtGuard multi-agent baseline in Lane 1b matrix; embedding-based scorer (XGBoost on OpenAI embeddings) as Lane 4 stacker row; V0/V4/SDD findings cited in book chapters (Ch 1 SDD label-corruption / Ch 4 V0 rung decomposition pretraining-does-68%-of-work / Ch 5 V4 contamination signature + paired-bootstrap stopping rule). Plus Tier A free additions: TPR@LowFPR (0.1%, 0.05%) reporting in all Lane 1+4 evals (ADR-036); APR metric in Lane 4 (ADR-037); benchmark-integrity audit (M0 sub-deliverable — confirm no training on PINT/PromptShield/NotInject; ADR-038). |
| Q2'''''' | Tier C methodology expansion | **Both on roadmap with execution optionality**: PromptShield Llama-3.1-8B Lane 1 SOTA anchor (~$40-50) AND Energy-based loss Lane 2 3rd variant (~$34). Decision deferred to mid-milestone when in-flight budget signal allows. See §16 Prioritized Roadmap for execution-order + contingency-unlock gates. |

### Round 14 (Q1''''''''''-Q4''''''''''): post-survey realignment (submission v1.2.3..v1.2.12 + eval-toolkit v0.43.0/v0.44.0 + ADR-075)
| # | Decision | Choice |
|---|---|---|
| Q1'''''''''' | CI submission ref pin | `v1.1.1` → **`v1.2.12` (HEAD)**. Tracks current state of submission's reading-guide + reviewer-facing site; accepts polish-stream re-pin overhead. (User picked HEAD over canonical v1.2.9.) |
| Q2'''''''''' | eval-toolkit floor | `>=0.42` → **`>=0.47` per Round 20** (was `>=0.44` initially; bumped after Round 20 roadmap-review revealed v0.45/v0.46/v0.47 had shipped same week). Gets MR-1/2/4/5/6/7 primitives + scorecard() + metric_specs + TextTransform + 12-technique character_injection + v0.45 LogisticStacker all in one pin. Lane work targets v0.47 canonical surfaces. |
| Q3'''''''''' | MR-2 advanced-6 follow-up | **File new MR-10 issue** against eval-toolkit for 6 deferred character_injection techniques (bidi RTL + tag stripping + synonym + token splitting + Unicode normalization + invisible chars). Scheduled for v0.43.1 per upstream CHANGELOG; portfolio files explicit issue to track + signal priority. Lane 1b uses core-6 at M1 start. |
| Q4'''''''''' | Task #6 transition | **Split** into closed half (5/7 MRs shipped via parallel-Codex implementation) + new follow-up: **#6a** `consume + verify v0.44.0 primitives at M0 Day 3-4 + populate library_imports.md rows`; **#6b** `track open MRs MR-3 / MR-6 / MR-8 / MR-9 / MR-10 for closure`. |
| (citation) | ADR-052 supersession | Portfolio cites **ADR-075** (unifies ADR-050 R2 + ADR-052) as canonical for Lane 2 hypothesis (§5) + Ch 7 case study (§17). ADR-052 retained in submission/decisions/ as historical artifact per submission's immutability rule. |

### Round 17 (Q1-Q4): 3-guide architecture (narrative-structure remediation per user complaint)
| # | Decision | Choice |
|---|---|---|
| Q1 (Round 17) | Build strategy for 3 guides | **One Astro book + 3 subsite folders**: `book/src/content/{textbook,narrative,academic}/`. Astro routes `/textbook/[slug]`, `/narrative/[slug]`, `/academic/[slug]`. Single npm build; shared scaffolding; each guide has own TOC + nav. |
| Q2 (Round 17) | Chapter authoring strategy | **Shared substrate + 3 framing wrappers**: fragments at `book/src/content/fragments/lane-N/{methodology,results,interpretation}.mdx` hold experiment-data + dossier citations; each guide's chapter MDX imports + sequences fragments with guide-specific framing prose. ~1x data-write + 3x framing-write per lane. |
| Q3 (Round 17) | Release sequence | **Sequential rollout**: v0.7.0 M7 = Textbook only (lowest authoring delta). v0.8.0 (~month 13) = Narrative ("Can we climb the wall?"). v0.9.0 (~month 14) = Academic IMRaD. v1.0.0 (~month 16-17) = all 3 polished. Extends v0.7.0 → v1.0.0 window from 3mo to ~3-4mo. |
| Q4 (Round 17) | Plan-level lock timing | **Round 17 now**: narrative + 4 locks added to plan; §6 (book design) + §9 (ADR-044) + §21 Day 14 updated. M0 Day 14 chapter skeletons = TEXTBOOK ONLY. |
| (follow-up Q3) | Cross-chapter narrative threading (narrative guide) | **Heavy threading — narrative weave**: each chapter opens with story recap + closes with hook to next; book frontmatter has full arc preview. Maximum reader-guide for narrative guide; ~5-10% prose overhead. |

---

## 2. SDD discipline calibration

### Tier-1 invariants

**Library-first — strict, no local workarounds**:
- **4 load-bearing infrastructure projects** (all maintained by Brandon; portfolio is one consumer):
  - `eval-toolkit` (PyPI, **v0.42+** per submission v1.0.9 pin; canonical Platt+Beta+Isotonic binary calibrator API)
  - `runpod-deploy` (PyPI, **v0.8.4+** per submission v1.1.0 pin; launch via `load_job_spec → run_job` over a YAML job spec — there is **no** `Session`; ADR-053)
  - `research_toolkit` (PyPI)
  - `@brandon_m_behring/book-scaffold-astro` (**npm package v3.1.0+**; pivoted from GitHub template overnight 2026-05-19; v3.1.0 academic ChapterHeader polish landed 2026-05-19). Bootstrapped via `@brandon_m_behring/create-book` CLI. `npm update` propagates fixes.
- **All reusable primitives belong in those libraries; portfolio NEVER hand-rolls equivalents.** Missing primitives → file upstream issue → implement as merge request → release new version → portfolio's `pyproject.toml` (or scaffold reference) pins the new version → lane work proceeds.
- **No local workarounds whatsoever.** No `src/_overrides/`, no `# TODO(upstream #N)` markers, no "ship now and refactor later." If a primitive is needed and not in upstream, the portfolio lane is blocked until upstream ships.
- Project-specific glue (lane orchestration scripts, data loaders that *compose* eval-toolkit primitives, project-named CLI wrappers) IS allowed in portfolio's `src/`. The line: anything reusable across projects belongs upstream; anything project-specific stays local.
- Imports logged in `decisions/library_imports.md`; upstream MR status tracked in `decisions/upstream_issues.md`.

**Ongoing-issue-filing discipline (Round 10 user grant 2026-05-19)**: in addition to the upfront MR-1..7 list (§10), the portfolio has standing permission to **file GitHub issues against any of the 4 load-bearing libraries during execution** when friction is encountered — feature requests, papercuts, API improvements, documentation gaps, upgrade-compatibility notes. Workflow:

1. Encounter friction in execution (e.g., eval-toolkit primitive doesn't compose ergonomically with a Lane 4 stacker setup; scaffold v3.1's academic profile lacks a callout the book needs; runpod-deploy validate flag is missing).
2. Capture the friction in a `decisions/upstream_issues.md` row under "Filed during execution".
3. Open the GH issue against the appropriate repo via `gh issue create --repo brandon-behring/<lib> --label enhancement` (or `bug`, `documentation`, etc.).
4. Reference the issue number in the upstream_issues.md row.
5. **Continue execution** — don't block on the issue. If the friction has a clean compose-around using existing primitives, use that. If it doesn't and is genuinely blocking, escalate to "the lane is blocked until upstream ships" per the no-local-workarounds rule.

The standing permission lets the library ecosystem grow with portfolio's needs in a continuous feedback loop, not just at M0's batch-of-7. Each issue filed should have a "Reference impl sketch" section sufficient for upstream maintainer (Brandon) to evaluate without context-switching back to portfolio.

**Anti-pattern firewall**: no test-tuning, real tests not stubs, per-row predictions persisted, leakage scan on every new eval source, new project-specific term → glossary entry in same commit.

**Commit discipline**: type-prefixed, `Co-Authored-By: Claude` trailer, **no amend / squash / force-push**.

### Tier-2 decision tracking (light, retrospective)
Light ADRs <400 words. **~20-24 anticipated** (5 round-3 additions: ADR-021/022/023/024/025). Experiment records primary unit of work. Contingency unlocks via `decisions/contingency_unlock_N.md`.

### Tier-3 spec docs (v5 pattern)
MISSION + ROADMAP + NEXT_SESSION + CHANGELOG + library_imports / upstream_issues + glossary + **ETHICS.md** (Q3'').

### Tier-4 CI / enforcement
- Quality gates: ruff (check + format), mypy --strict, pytest (unit + smoke).
- Test-contracts (6): `no_handrolled_metrics`, `predictions_persisted`, `leakage_scan_present`, `glossary_complete`, `library_imports_registered`, `mypy_strict_clean`.
- nbval gate for notebooks (Q5').

### Tier-5 hierarchical-depth public claim register (Q1')

| Layer | Surface | Audience | Depth | Derivation rule |
|---|---|---|---|---|
| L0 | README + pre-alpha banner (Q2'') | 60-sec scan | Shallow | Derived from L2 |
| L1 | HF Hub model cards (8+) + dataset card (Q3'') | ML engineers | Shallow | Derived from L3 + L4 |
| L2 | ~~Book exec summary~~ **COLLAPSED INTO L0 README per Round 17 follow-up Q2** (user: "That can go in the readme"); README's exec-summary section serves the 5-min-scan audience. Book frontmatter retains AI-disclosure + title-page + pre-alpha-banner + acknowledgments only. | 5-min scan | Medium (via L0) | Derived from L3 conclusions; lives in root README.md |
| L3 | Book chapters (KF-disciplined prose) — **3 guides per Round 17**: textbook (v0.7.0 M7) + narrative (v0.8.0) + academic (v0.9.0). Shared fragments at `book/src/content/fragments/lane-N/` are the single source of truth for experiment data + citations. | Practitioners (textbook) / engineers + recruiters (narrative) / researchers (academic) | **Deep (ground truth narrative)** | Derived from L4 + L5; guide-specific framing prose wraps L3.5 fragments |
| L3.5 | Notebooks inside `book/src/content/notebooks/` (Q5') | Interactive deep-divers | Deep | Mirrors L3 analysis |
| L4 | Experiment records | Researchers; primary unit of work | Deepest evidence | Original work; cites L5 |
| L5 | Dossier (~60-80 files) | Researchers; critical readers | Ground truth citations | Original work via research_toolkit |

**Derivation rule**: write deepest first; summarize up. No L0-L2 claim without traceable origin in L3-L5.

**Verification gate**: user reads L3-L5 to audit Claude's reasoning. Shallower summaries are valid only when deep layer survives review. M7 final-pass = coherence-edit pass on L3 end-to-end.

**Freshness-badge state machine** (L3 chapters + L3.5 notebooks): `exploratory` → `experimental-result` → `locked` → `superseded`. **Pre-alpha banner** (Q2'') applies to entire repo until M7 ratifies all badges to `locked`; banner removed at v0.7.0 tag.

### Tier-6 phase / milestone model
Loose milestone tags `v0.1.0` (M0) → `v0.7.0` (M7; **textbook guide ratified per Round 17 Q3**) → `v0.8.0` (~month 13; **narrative guide shipped**) → `v0.9.0` (~month 14; **academic IMRaD guide shipped**) → `v1.0.0` (M7 + 3-4mo community window; **all 3 guides polished + citable**). CHANGELOG mega-entries per tag.

---

## 3. Repo topology

**New repo**: `prompt-injection-portfolio` (this repo). Public on GitHub from M0 via `gh repo create --public` (Q2'').

**Dependency policy** (per round-3 reinforcement + round-6 v3.0 npm pivot + Round-14 v0.43.0/v0.44.0 advances):
```toml
# pyproject.toml
[project]
dependencies = [
    # PyPI infrastructure libraries — NEVER hand-rolled
    "eval-toolkit>=0.47",        # Round 14 floor: ships MR-1/2/4/5/7 primitives + canonical binary calibrator API
    "runpod-deploy>=0.8.4",      # cloud-eval launch via load_job_spec→run_job (ADR-053; no Session)
    "research-toolkit>=...",     # PyPI; dossier pipeline
    "transformers", "torch", "anthropic", "sklearn", ...
]

[tool.uv.sources]
# Submission is the prototype — editable dep at sibling path; CI two-step checkout per F2
prompt-injection-detection-prototype = {
  path = "../prompt-injection-detection-submission", editable = true
}
```

CI `ref:` value for submission **advances to v1.2.12 (HEAD) per Round 14
Q1** (was `v1.1.1` at portfolio M0 Day 2). Day 3a uses **dynamic
latest-tag detection** (round-2 Q2) to fall back gracefully if v1.2.12
isn't pushed yet — `git ls-remote --tags origin | grep refs/tags/v1.X.X
| sort -V | tail -1` selects the actual latest pushed semver tag. Re-pin
to a newer tag manually if submission ships further polish patches;
`eval-toolkit` / `runpod-deploy` minimum versions advance with upstream
releases (see Round 14 narrative for the v0.43.0 + v0.44.0 closures).

```jsonc
// book/package.json (scaffolded via npx @brandon_m_behring/create-book)
{
  "dependencies": {
    "@brandon_m_behring/book-scaffold-astro": "^3.1.0",
    "astro": "^6.1.7",
    "@astrojs/mdx": "^5.0.3",
    "@astrojs/preact": "^5.1.1",
    "preact": "^10.29.1",
    "pagefind": "^1.5.2"
  }
}
```

`@brandon_m_behring/book-scaffold-astro` is the **4th load-bearing library**. Missing features → upstream npm package issues + MRs; portfolio's `book/package.json` pins bumped as upstream ships.

```
prompt-injection-portfolio/
├── pyproject.toml
├── uv.lock
├── Dockerfile                              # T2 reproducibility tier (Q2')
├── compose.yaml
├── Makefile
├── README.md                               # L0; carries pre-alpha banner (Q2'')
├── MISSION.md
├── ROADMAP.md
├── NEXT_SESSION.md
├── CHANGELOG.md
├── CLAUDE.md
├── LICENSE                                 # Apache-2.0 (code)
├── ETHICS.md                               # Q3'' — dual-use disclosure
├── book/LICENSE                            # CC-BY-4.0 (prose + notebooks)
├── .env.example
├── .github/workflows/
│   ├── ci.yml                              # ruff + mypy + pytest + nbval + 6 test-contracts
│   ├── publish-book.yml                    # Cloudflare Pages deploy
│   └── publish-hf.yml                      # HF Hub model + dataset card publish
├── decisions/
│   ├── README.md
│   ├── library_imports.md
│   ├── upstream_issues.md
│   ├── ADR-*.md                            # ~20-24 anticipated
│   └── contingency_unlock_*.md
├── experiments/                            # L4
├── docs/
│   ├── research/                           # L5; ~60-80 files
│   ├── glossary.md
│   ├── runbooks/lane{1,1b,2,3,4,5}.md
│   └── build-in-public/                    # Q4'' — weekly/monthly post archive
├── configs/
├── src/
├── data/
├── evals/
├── scripts/
│   ├── verify_data_sources.py
│   ├── verify_editable_dep.py
│   ├── verify_docker.py
│   ├── eval_from_hub.py                    # T0 tier — portfolio-clean impl per Round 6 ADR-035
│   └── retrain_blueprint.py                # T1 tier
├── book/
│   ├── package.json
│   ├── astro.config.mjs
│   └── src/content/
│       ├── frontmatter/
│       │   ├── ai-assistance-disclosure.mdx   # Q1''
│       │   └── pre-alpha-banner.mdx           # Q2''
│       ├── chapters/                          # L3; 13 chapter .mdx
│       ├── notebooks/                         # L3.5; ~5-6 jupytext-paired
│       # exec-summary.mdx REMOVED per Round 17 follow-up Q2: exec-summary
│       # content lives in root README.md (collapses L2 → L0); shared
│       # across 3 guides via the README's 3 peer-level entry-points.
├── transcripts/                            # gitignored
└── tests/
    ├── unit/
    ├── smoke/
    ├── integration/                        # opt-in
    └── contracts/                          # 6 test-contracts
```

---

## 4. Research dossier — exhaustive refresh (M0 sub-deliverable)

Target ~60-80 files across 11 sub-areas. Per-paper deep dives, per-benchmark deep dives, commercial-detector survey, production-incident corpus, critique literature. ~25-40h Claude Code session over weeks 1-3 of M0. Workflow: compass → `_inbox/` → decompose → `/research-gather` + `/dossier-build` → `/dossier-audit`.

### Round 24 update — Sprint 2 dossier expansion (post-Sprint 1 close)

Sprint 1 (Phases 0-4, 2026-05-22) delivered the 3-topic dossier (122 entries across detector-landscape / direct-vs-indirect / training-and-evaluation). Sprint 2 (Phases E0-E6, 2026-05-23) expanded to **5 topics** with **210 bib_ledger entries / 347+ evidence entries / 157 unique BibTeX entries / ~124 cached PDFs (~246 MB, gitignored)**. The 2 new topics added per user goal of thesis-readiness:

- **agentic-security-architecture** (Lane 4 + 5 focus): 25 entries (24 cross-classified `agentic_*` prefix from sibling topics + 1 net-new AgentArmor)
- **rag-injection-defenses** (Lane 3 focus): 18 entries (6 cross-classified `rag_*` + 7 net-new papers + 5 production_rag_incidents per ADR-041 ETHICS posture)

**Pipeline substitution**: §4's original workflow listed `/dossier-build → /dossier-audit`, but Sprint 1 + 2 used the **canonical v2.2+ flow**: `/research-plan → /research-gather → /agent-index → /dossier-audit` (skipping `/dossier-build`; matches the 4 v2.2-dogfood projects). The `/agent-index` step produces the 5-bullet synthesis with claim IDs + Attribute-First `pre_selection_manifest.yml` span contract that future LLM agents read as ground-truth context.

**Cross-classification policy**: full cross-classification with topic-prefixed bibkeys (`agentic_<original>`, `rag_<original>`). Each topic's agent_index is fully self-contained.

**Validation**: `make dossier-audit` (Sprint 2 E6 addition) validates v2.2+ strict-live artifacts across all 5 topics (bib_ledger + evidence_ledger + cache_manifest + claim_graph + gather_trace + agent_index + pre_selection_manifest + audit_trail + cross_stage). M7 ratify gate per ADR-007 is now executable. Final 6-lane → claim_family mapping populated in `experiments/MANIFEST.json`.

---

## 5. Five indirect-attack lanes (architecture)

Lane 1, 1b, 2 (2-variant LoRA base per Round 15 Q1; optional 3rd energy-loss LoRA variant per Round 7 Q2''''''), 3 (3-variant Spotlighting), 4 (LLMail-Inject 5K + PINT-EN; stacker trains on Lane 2 corpus per Round 16 Q3), 5 (TaskTracker activation probe; trains on Lane 2 corpus per Round 16 Q4; **M4 timing per Round 16 Q5**, was M2).

**Round 7 additions** (per Q1'''''' + roadmap-optional Q2''''''):
- **Lane 1**: add Meta Prompt Guard 2 86M (~$10 GPU) as reference scorer alongside ProtectAI v1/v2. **Optional**: add PromptShield Llama-3.1-8B (~$40-50 GPU) as SOTA anchor — execution-optional based on mid-milestone budget signal.
- **Lane 1b**: add CourtGuard multi-agent debate baseline (~$5-10 API) as one row in the 12-technique × N-detector matrix; tests over-defense vs single-classifier columns. **Round 20 simplifies (was Round 14 Q3 + round-5 Q1 6+6 sequencing)**: M1 starts with full 12-technique matrix — all 12 dataclasses ship in eval-toolkit v0.47.0 (`ALL_TECHNIQUES` 12-tuple); MR-10 advanced-6 filing OBSOLETED.
- **Lane 2**: **Optional** 3rd variant — energy-based loss (Liu NeurIPS 2020; Meta PG2 + CodeIntegrity recipe; ~$34 GPU). Execution-optional based on M3 data audit + cost trajectory. **Round 15 Q1**: All Lane 2 retraining variants (2-variant base + optional energy-loss 3rd) are **LoRA on ModernBERT-base only**; full fine-tuning OUT OF SCOPE.
- **Lane 4**: add embedding-based scorer (XGBoost on OpenAI embeddings, CodeIntegrity approach; ~$5 API) as one detector type in stacker mix. **Report APR metric** (Meta PG2: % attacks blocked at ≤3% utility loss; $0).
- **All lanes with eval surfaces**: **report TPR@LowFPR (0.1%, 0.05%)** alongside AUPRC ($0). Per compass: single most important methodological advance 2024-25.
- **Benchmark integrity audit** (M0 sub-deliverable, $0): confirm portfolio doesn't train on PINT, PromptShield, NotInject, HackAPrompt. ADR-038 ratifies.

**Round 15 baseline expansion** (per Round 15 Q1 user-custom: "keep tfidf baseline and fixed probe baselines, and any other appropriate opensource models I can test"; refined Round 16):

- **TF-IDF + LogisticRegression baseline** (NEW; sklearn `TfidfVectorizer` +
  `LogisticRegression`; CPU-only; ~$0). Methodologically important
  classical-text-classification floor — answers "are we even better
  than 1990s methods?" Added to Lane 1 baseline column + Lane 2
  comparator set. No upstream MR needed (sklearn already in main deps
  via existing `scikit-learn>=1.5` pin). **Round 16 Q1**: trains on
  Lane 2's same corpus (synthetic indirect-injection-heavy MR-3 output
  ~20k rows) for apples-to-apples comparability with LoRA.
- **Frozen-probe baseline** RETAINED (from submission; already available
  via portfolio's clean-T0 `scripts/eval_from_hub.py` per ADR-035).
  Non-trainable; operates as off-the-shelf scorer.
- **Open category** for "other appropriate open-source models" —
  baseline list **locked at M1 protocol.md** (per Round 16 Q2) BUT
  **appendable** via per-experiment-record protocol.md amendment if
  M0 dossier work (Days 6-12) surfaces a clearly-appropriate baseline.
  Examples that may qualify as Lane 1 baselines: sentence-transformer
  + LR head; DeBERTa-v3-base (cite submission v1.1.2 null result as
  anchor); small BERT variants (DistilBERT, TinyBERT). All TRAINABLE
  open-category baselines train on the SAME Lane 2 corpus per Round 16
  Q1 comparability rule. Each baseline costs ~$0-5 inference-only;
  stays within base envelope.

**Lane 2 hypothesis sharpened by submission ADR-075 + v1.1.2 DeBERTa null result** (round 6 Q3''''' lock + Round 14 citation cascade):

- **ADR-075 (v1.2.9; supersedes ADR-050 R2 + ADR-052 per ADR-075
  frontmatter)**: Unifies the FUSE-crash-forced-drop + methodology-
  load-bearing framings into one prospective narrative. LoRA full-FT
  OOD drop is methodologically load-bearing — LoRA paired-bootstrap
  shows -0.071 AUPRC delta vs frozen-probe on pooled_ood with CI
  clearing zero. Fine-tuning on submission's direct-injection-heavy
  training pool **actively hurts** OOD generalization; the FUSE crash
  was a proximate trigger that aligned with the methodologically-
  load-bearing decision to drop full-FT OOD inference (3-rung LODO
  + 2 trained + 1 classical + 2 reference scorers per ADR-050 R1+R2 +
  ADR-052 + ADR-075). [ADR-052 superseded; ADR-050 R2 axis superseded;
  both retained in submission's `decisions/` per immutability rule.]
- **v1.1.2 DeBERTa-v3-base null result**: chunk_and_average 0.2912 ≈ head_truncation 0.2895 on pooled OOD. Backbone-dominant verdict: ModernBERT advantage is NOT context-window-driven; OOD wall extends across backbones + truncation strategies. **[Round 30 / ADR-055 — axis-precision:** this null is on the **carrier / direct→indirect** axis; *backbone*-invariant ≠ *capacity*-invariant. M1's attack-type-axis result (end-to-end LoRA dissolves the per-type gap) is a **different axis** and does **not** bear on this carrier null — see the Round-30 Lane-2 re-point below.**]**

Lane 2's question becomes (Round 15 framing): *does adding
indirect-injection training data, while holding parameter budget at
LoRA-only, overcome (a) the active-harm LoRA pattern from submission's
direct-injection training AND (b) backbone-invariant OOD limit?* Three
possible outcomes:
- Both Lane 2 LoRA variants still produce negative AUPRC deltas vs
  frozen-probe → wall confirmed structural beyond data choice;
  methodology lesson is "current detector framing has a hard ceiling
  that doesn't yield to either parameter budget or training data
  alone".
- One LoRA variant lifts to non-negative → data + loss together matter
  (CE vs Recall@LowFPR distinguishes which loss).
- Both LoRA variants lift → indirect training data overcomes both
  prior limits at LoRA scope → wall is data-bound (counter-evidence to
  backbone-dominant verdict). Lane 2 confirms Round 15 hypothesis that
  the bottleneck was data, not parameter budget.

Ch 7 case study cites BOTH **ADR-075 (canonical unified full-FT OOD
drop rationale; supersedes ADR-052; supports Round 15 LoRA-only scoping
decision)** AND v1.1.2 DeBERTa null result (backbone-invariance) as
foundation for the OOD wall framing.

**Round 30 re-point (post-M1; ADR-055) — Lane 2 → the carrier axis.** M1 (attack-type-LODO) answered the *attack-type* half: end-to-end LoRA generalizes near-uniformly across held-out attack types (test AUPRC 0.98–0.999), so the §6.5 per-type "wall" is **capacity-dependent** (dissolved by LoRA — FALSIFIED at the ceiling; SURVIVES on tfidf/frozen). The interesting *unsolved* axis is therefore the **carrier** (held constant by ADR-052 design), which dominates the representation geometry (silhouette by-carrier 0.197 vs by-attack-type −0.023). **Decision (R30):** Lane 2's **method is unchanged** (LoRA-retrain + 2-variant loss per ADR-043); its **headline evaluation axis moves to carrier generalization** on the available carrier set (email/code/table; qa/abstract license-gated). "Confirm attack-type generalization persists under the Lane-2 recipe" is registered as a cheap §16 optional secondary, not the headline.

The three outcomes above are **re-axised to the carrier wall**: M1 showed the *attack-type* wall is **not** structural (capacity dissolves it), so "wall confirmed structural beyond data choice" now refers specifically to the **carrier** wall — whose size is measured *before* Lane 2 commits by the **carrier-LODO M2 pre-flight gate** (§16 Round-30 gates; ADR-055). If that gate finds the carrier gap persists under LoRA, the carrier wall is the live structural question Lane 2 attacks; if LoRA dissolves it too, the spine is revised (capacity dissolves both axes) and Lane 2's headline is resized accordingly.

---

## 6. Book design (`book/`)

**Working title**: *The OOD Wall* (placeholder). License **CC-BY-4.0**.

**Bootstrap from scaffold v3.0+ npm package** (Round 6 Q2''''' final): `npx @brandon_m_behring/create-book prompt-injection-portfolio --profile=academic` (research-portfolio profile deferred to v3.1+ per Round 6; portfolio uses academic + local extras at v0.1.0). The scaffold provides:
- **18 typed callouts** (8 original + 10 academic): SkillBox / CaseStudy / ConceptBox / KeyIdea / TryThis / Recovery / Convergence / Divergence + NoteBox / ExampleBox / DynConnect / InsightBox / WarnBox / CounterBox / TipBox / OpenQuestion / PaperBox / ResultBox.
- **Theorem family** (8 amsthm kinds): theorem / proposition / lemma / corollary / definition / example / exercise / remark.
- **KaTeX math** via remark-math + rehype-katex; 36-macro custom library.
- **BibTeX bibliography pipeline**: `scripts/build-bib.mjs` converts `.bib` → `src/data/references.json` via citation-js; `<Cite key="...">` component with hyperlinked references on a generated `references.astro` page.
- **`<MarginNote>`** for Tufte sidenotes alongside `<Cite>` for inline citations (Q4''' hybrid satisfied by scaffold).
- **Pre-flight validator** `scripts/validate.mjs` catches typo'd bibkeys, XRef slugs, figure paths.
- **Asset pipelines**: `scripts/build-figures.mjs` (PDF→SVG + PNG→WEBP), `scripts/render-notebooks.mjs` (ipynb→HTML).
- **7-state status system** (Q2'''' adoption): `implemented` / `chapter_only` / `reading_only` / `prose_only` / `code_only` / `scaffolded` / `planned`. `<StatusBadge>` renders state from chapter frontmatter.
- **Pre-alpha banner** = SEPARATE repo-wide dimension (Q2'''' resolution); implemented as portfolio-local component added during M0 (not per-chapter state).

### 6.1 Frontmatter (per Q1'', Q2'')

```
book/src/content/frontmatter/
├── title-page.mdx               # "The OOD Wall" + sole author "Brandon Behring"
├── ai-assistance-disclosure.mdx # 1-paragraph publisher-style disclosure
├── pre-alpha-banner.mdx         # visible until M7 final-pass
└── acknowledgments.mdx          # thanks Claude as collaborator
# exec-summary.mdx REMOVED per Round 17 follow-up Q2: lives in root README.md
# (L2 → L0 collapse; shared across 3 guides via README's 3 peer-level entry-points)
```

**AI-assistance disclosure paragraph** (template):

> *This book was developed in collaboration with Claude (Anthropic). Claude assisted with literature review, methodology drafting, code authoring, experiment design, and prose drafting. All experimental work and methodology choices were directed by the human author; Claude served as a research and writing collaborator throughout. Detailed per-commit attribution is preserved via `Co-Authored-By:` git trailers; the overall workflow is described in `docs/build-in-public/` and the project's README.*

### 6.2 Pedagogical Textbook ToC (13 chapters, 4 parts) — guide #1 of 3 per Round 17

This is the **textbook guide's ToC** (Round 17 Q1: 3 separate guides; textbook = guide #1, ships at v0.7.0 M7). Unchanged from Round 6 design: Part I (Ch 1-3), Part II (Ch 4-6), Part III (Ch 7-12), Part IV (Ch 13). Three case-study anchors: EchoLeak (Ch 7), "Firewalls" critique (Ch 5 sidenote), CodeIntegrity 98% post-mortem (Ch 13). Self-contained chapters; modular learning; reader picks chapters. Audience: practitioners learning prompt-injection detection methodology.

Story arc + Academic IMRaD ToCs ship at v0.8.0 / v0.9.0 respectively (per Round 17 Q3); see §6.6 below for the 3-guide architecture overview.

### 6.3 Selective T3 notebooks (~5-6 per Q5')
Ch 5 bootstrap-CI-walkthrough, Ch 6 threshold-policy, **Ch 8 char-injection-bypass-matrix** (full 12-technique columns from M1 start per Round 20 — eval-toolkit v0.47.0 ships `ALL_TECHNIQUES` 12-tuple), Ch 9 attribution-table, Ch 11 stacker-analysis, Ch 12 activation-probe. Ch 10 RAG demo is interactive via HF Space — no notebook.

**Round 17 update**: notebooks live under `book/src/content/notebooks/` as a SHARED resource. All 3 guides reference the same notebook artifacts (textbook chapter links to notebook URL; narrative chapter references same notebook; academic chapter cites same notebook). Notebooks are guide-independent.

### 6.4 Chapter authoring workflow (Q3')
M0: textbook guide's 13 skeletons ship (3-5 days; **TEXTBOOK ONLY per Round 17 Q4**; story arc + academic chapters scaffold at v0.8+ / v0.9+ respectively). Per-milestone: prose fill; badge promotes. M7: coherence-edit pass on textbook only; user reads L3 end-to-end; Claude fixes; textbook freshness badges → `locked`; pre-alpha banner removed; v0.7.0 tag.

v0.8.0 (~month 13): scaffold + write Story arc guide chapters using fragment imports from `book/src/content/fragments/lane-N/`. v0.9.0 (~month 14): scaffold + write Academic IMRaD guide. v1.0.0 (~month 16-17): all 3 guides polished + citable.

### 6.5 Quarto site (submission) vs Astro book (portfolio)
Quarto stays at submission; Astro book never duplicates a WRITEUP section. Portfolio's 3-guide Astro book remediates the submission's "random parts everywhere" anti-pattern (per Round 17 user complaint).

### 6.6 Three-guide architecture (Round 17 lock)

| Guide | Audience | TOC structure | Astro route | M7 v0.7.0 | Release |
|---|---|---|---|---|---|
| **Textbook** (current §6.2) | Practitioners learning methodology | 13 chapters / 4 parts / KF triadic R/O/E | `/textbook/[slug]` | ✓ Shipped | M7 v0.7.0 |
| **Story arc** (~"Can we climb the wall?") | Curious engineers + recruiters | Setup → 6 climb attempts → resolution; heavy cross-chapter threading per Round 17 follow-up Q3 | `/narrative/[slug]` | — | v0.8.0 (~month 13) |
| **Academic IMRaD** | Researchers + reviewers | Introduction → Background → Methods → Results (6 lanes as sub-sections) → Discussion → Future Work | `/academic/[slug]` | — | v0.9.0 (~month 14) |

**Shared substrate (Round 17 Q2)**: each lane has fragments at `book/src/content/fragments/lane-N/{methodology,results,interpretation}.mdx` holding the experiment data + dossier citations (single source of truth). Each guide's chapter MDX imports + sequences fragments with its own framing prose. Example (Story arc Ch 5 "First Attempt: Direct-Injection Baselines"):

```mdx
---
slug: ch05-first-attempt
title: "First attempt: direct-injection baselines"
guide: narrative
order: 5
---

import LaneOneMethodology from "@fragments/lane-1/methodology.mdx";
import LaneOneResults from "@fragments/lane-1/results.mdx";
import LaneOneInterpretation from "@fragments/lane-1/interpretation.mdx";

We started with the easiest climb: existing detectors against direct
injection. If the wall yields anywhere, it yields here. The hypothesis
was modest: established detectors should perform well on the easiest
attack class, giving us a baseline against which harder lanes can be
measured.

<LaneOneMethodology />
<LaneOneResults />
<LaneOneInterpretation />

But the wall didn't yield. ProtectAI v2's headline AUROC of 0.94
collapsed to 0.61 on our OOD pool — anti-correlated with random by
0.07 AUPRC delta. The textbook's Chapter 4 explains the rung ladder;
here in the story, that ladder is starting to look like a stepladder
against a much higher wall than literature led us to expect.

The next attempt — character injection — tests whether the wall has
side-paths, or whether the limitation is in the detector framing itself.
```

The textbook's Ch 8 (same lane 1) imports the same fragments but with textbook-style chapter intro + thesis statement instead of narrative framing.

**Fragment maintenance discipline**: changes to experiment data ONLY live in fragments. Guide-specific framing prose lives in guide-specific chapter MDX. Test contract `experiment_records_complete` (§18 Round 7) extends to verify each lane's 3 fragment files (methodology + results + interpretation) exist + are populated at lane-record close.

### 6.7 Narrative arc ToC outline (placeholder; full at v0.8.0)

**Working structure** (per Round 17 follow-up Q3 = Heavy cross-chapter threading):
- **Act I: The Wall** (3 chapters): "What is prompt injection?" / "Why detection looks easy at first" / "OOD: where it stops looking easy" (incorporates textbook Ch 1-3 content + per-chapter recap-and-hook framing)
- **Act II: Six Attempts** (6 chapters): One per lane (1, 1b, 2, 3, 4, 5). Each chapter is a "climb attempt" with setup ("here's what we tried") + execution ("here's what happened") + reflection ("here's what it tells us"). Heavy cross-chapter threading — Chapter N opens with "where we are" + closes with "Chapter N+1 takes a different angle..."
- **Act III: The Lesson** (1 chapter): "What the OOD wall is really made of" + methodology synthesis + ADR-075 citation + cumulative answer to "Can we climb the wall?"

Full per-chapter narrative beats locked at v0.8.0 planning session (post-M7 ratification).

### 6.8 Academic IMRaD ToC outline (placeholder; full at v0.9.0)

**Working structure**:
- **Introduction** (1 chapter): problem framing + significance + research questions + paper structure
- **Background** (1 chapter): literature review of prompt-injection detection methodologies + threat models + benchmark landscape (compressed from textbook Ch 1-3)
- **Methods** (1 chapter): rung ladder + LODO methodology + statistical apparatus + threshold policy (compressed from textbook Ch 4-6) + ADR-016/017/019/022/025 citations
- **Results** (1 chapter with 6 sub-sections): one per lane (1, 1b, 2, 3, 4, 5). Compact methods + key results + significance tests + tables. No tutorial framing.
- **Discussion** (1 chapter): cross-lane synthesis + OOD wall + ADR-075 + limitations + threats to validity
- **Future Work** (1 chapter, possibly fused with Discussion): NEXT_SESSION.md content + v0.8+ deferrals + open questions

Full per-section design locked at v0.9.0 planning session (post-v0.8.0 narrative-guide ship).

---

## 7. Reproducibility ladder (Q2' + Q1''''' Round 6 reframe)

**Portfolio v0.7.0 ships all 4 tiers — T0 + T1 + T2 + T3** — but portfolio writes its **own clean T0** implementation rather than consuming submission's `scripts/eval_from_hub.py` (per Q1''''' round 6 + ADR-035).

Why portfolio writes own clean T0 even though submission's is now wired (v1.0.9 ADR-058):
- Maintains "next version built from submission's experience, done cleaner" framing.
- Submission's T0 carries its own complexity from being retrofitted onto v1.0.x; portfolio's clean reimplementation can apply lessons learned (better error handling, cleaner CLI surface, dataset-loader integration, single-class-slice handling baked in).
- Independent codebase prevents portfolio's reproducibility surface from breaking when submission patches.
- Portfolio's T0 lives at `scripts/eval_from_hub.py` in portfolio repo (parallel name; different implementation).

**Tier mapping (final)**:
- **T0** (L1 HF Hub model card surface): `scripts/eval_from_hub.py` (portfolio-owned clean reimplementation; ADR-035). Downloads HF Hub checkpoint → CPU inference → compare to portfolio's `evals/results.json` within 1e-4. ~15 min on laptop.
- **T1** (L4 researchers, blueprint not bundled): `scripts/retrain_blueprint.py` + lane experiment records.
- **T2** (cross-cutting Docker, mandatory at M5): `Dockerfile` + `compose.yaml` + `verify_docker.py`.
- **T3** (L3 selective notebooks): ~5-6 jupytext-paired notebooks in `book/src/content/notebooks/`. Reference submission's 4 foundational notebooks (`docs/benchmark/{01-04}.ipynb`) where applicable; portfolio adds Lane 1b 12-technique matrix + Lane 9 attribution + Lane 12 activation probe + Ch 5 bootstrap + Ch 6 threshold-policy notebooks.

ADR-035 (portfolio-clean-T0-strategy) supersedes ADR-033 (T0 deferral).

---

## 8. Public-facing commitments (Round 3 decisions)

### 8.1 Visibility timeline (Q2'')

| Tag | Date | Visibility state | Banner |
|---|---|---|---|
| M0 (week 1) | repo creation | Public on GitHub | `pre-alpha — under active development` |
| v0.1.0 - v0.6.0 (M0-M6) | weeks 1-12 | Public; develops in open | `pre-alpha` continues |
| **v0.7.0 (M7)** | week 13-14 | Public + **Textbook guide ratified per Round 17 Q3**; **pre-alpha banner removed** on textbook guide; `pre-alpha` may continue on book index page until v1.0.0 (other 2 guides still in flight) | None on textbook routes; light banner on `/narrative/` + `/academic/` placeholders |
| v0.7.x patches (months 1-3 post-M7) | months 13-15 | Public; textbook community feedback window | None on textbook routes; CHANGELOG mega-entries per patch |
| **v0.8.0** (~month 13, per Round 17 Q3) | ~1mo post-M7 | Public; **Narrative guide ("Can we climb the wall?") shipped** | None on narrative routes after ship |
| v0.8.x patches | months 14-15 | Public; narrative community feedback window | None |
| **v0.9.0** (~month 14, per Round 17 Q3) | ~2mo post-M7 | Public; **Academic IMRaD guide shipped** | None on academic routes after ship |
| v0.9.x patches | months 15-16 | Public; academic community feedback window | None |
| **v1.0.0 (~month 16-17, per Round 17 Q3)** | ~3-4mo post-M7 | Public; **all 3 guides polished + citable** | None; `locked` for citation purposes |
| v1.0.x patches (indefinite) | post-v1.0.0 | Public; maintenance mode | None; bug-patch-only per Q5'' |

### 8.2 Build-in-public cadence (Q4'')

**Weekly cadence** (every Friday):
- Twitter/X thread (~3-5 tweets): summarize the week's progress + 1 figure + link to relevant chapter/dossier.
- Mastodon cross-post (`sigmoid.social` for ML reach).
- Archive copy → `docs/build-in-public/YYYY-WW-week-summary.md`.

**Monthly cadence** (first weekday of month):
- Longer-form blog post (500-1500 words): one of the recent badges promoted; deeper dive than weekly thread.
- Cross-post to LessWrong (ML-safety-relevant content) or LinkedIn (hiring-audience-relevant content).
- Archive → `docs/build-in-public/YYYY-MM-month-deepdive.md`.

**Per-milestone announcement**:
- M0 (v0.1.0): "starting an open prompt-injection portfolio with the submission as prototype. Following along: ${repo url}."
- M5 (v0.5.0): "Lane 3 RAG demo live: paste a poisoned doc, watch the classifier respond. Try it: ${HF Space url}." Twitter + Mastodon + HN if traction.
- M7 (v0.7.0): "The OOD Wall pre-print: 13 chapters, 5 lanes, 60+ dossier. Honest findings about fine-tuning consuming OOD budget." All channels.
- v1.0.0 (~month 16): "v1.0.0: portfolio piece complete. ${citable URL}." All channels; arXiv preprint if relevant.

**Time budget**: ~1-2h/week human-time (Claude drafts; Brandon edits + posts). Claude Code skill could generate first drafts from the previous week's commit log + experiment record diffs.

### 8.3 Author + AI-assistance disclosure (Q1'')

- Book title page: sole author "Brandon Behring".
- Frontmatter `ai-assistance-disclosure.mdx`: publisher-style 1-paragraph disclosure (template above).
- Acknowledgments section: thanks Claude as collaborator.
- Commits: `Co-Authored-By: Claude <noreply@anthropic.com>` per submission discipline.
- HF Hub model cards: "Training methodology" section mentions AI-assisted research workflow.
- Citation format: `Behring, B. (2026). The OOD Wall: A Methodology Case Study in Prompt-Injection Detection. https://...`

### 8.4 Ethics + dual-use disclosure (Q3'')

**ETHICS.md sections**:
1. Dual-use disclosure — synthetic adversarial data could be misused for attacker training; intended for detector training only.
2. Intended use — research, detector development, defensive evaluation.
3. Responsible use — recommendations against using for production attacker training.
4. Anthropic ToS compliance — Sonnet-generated outputs redistributed per Anthropic Commercial Service Agreement for research purposes with attribution.
5. Citation guidance.
6. Reporting concerns — contact info for security/ethics issues.

**HF Hub dataset card** (`BBehring/prompt-injection-synthetic-indirect-v2`):
- `task_categories: ["text-classification"]`
- `tags: ["prompt-injection", "research-use", "responsible-ai"]`
- Restricted-use note in dataset card frontmatter.
- Links back to portfolio's `ETHICS.md`.

### 8.5 Maintenance commitment (Q5''; extended by Round 17 Q3 sequential rollout)

**M7 to month 16-17 (~3-4 months; Round 17 extends from 3mo to ~3-4mo)**: Active community feedback window + sequential 2-guide ship.
- Respond to GitHub Issues; accept PRs for typos, citation fixes, clarifications.
- No new lanes; no methodology changes that supersede locked ADRs (per submission's discipline).
- Build-in-public cadence continues at lower frequency (monthly only).
- v0.7.x patch releases on textbook as fixes accumulate.
- **v0.8.0 (~month 13)**: Narrative guide shipped per Round 17 Q3.
- **v0.9.0 (~month 14)**: Academic IMRaD guide shipped per Round 17 Q3.

**v1.0.0 cutover (~month 16-17)**: Portfolio piece locked.
- Final v1.0.0 release after ~3-4 months community feedback (all 3 guides shipped + polished).
- All freshness badges → `locked` (definitively, post-community-window).
- v1.0.0 is the citable / hiring-discussion / academic-citation tag.
- All 3 guides have parity coverage; README's 3 peer-level entry-points (per Round 17 follow-up Q3) are all active.

**Post-v1.0.0 (indefinite)**: Maintenance mode.
- v1.0.x patches for critical bugs only.
- New lanes / chapters / methodology changes → deferred to potential future v2.0 or never.
- NEXT_SESSION.md documents v2.0 ideas; no active commitment.
- Build-in-public posts can continue at user's discretion but are not committed-to.

---

## 9. Milestone sequence (8 milestones M0-M7, ~13-14 weeks; then 3-month community window → v1.0.0)

### M0 deliverables (weeks 1-3, ~45-70h session)

1. **Pre-flight gates** (day 1): `gh repo view brandon-behring/book-scaffold-astro`, `make verify-data-sources`, `make verify-deps`, `make book-pdf-smoke`, `make verify-docker`.
2. **Repo public on GitHub** (day 1): `gh repo create --public prompt-injection-portfolio` with pre-alpha banner.
3. **CI green from first push** (week 1): mypy --strict clean, ruff format clean, all 6 test-contracts in place.
4. **Dossier work** (weeks 1-3): exhaustive ~60-80 files via research_toolkit.
5. **Upstream MRs filed + (Round 14) consume v0.44.0 + file MR-10** (week 1-3, ~1.5-2 days session):
   - ✓ Day 2.5: filed 9 issues per §10 (MR-1..MR-9).
   - ✓ 2026-05-19 → 2026-05-21: parallel-Codex agent implemented 5 (MR-1/2 core-6/4/5/7); released eval-toolkit v0.43.0 + v0.44.0.
   - Day 3: file new **MR-10** (advanced-6 character_injection) against eval-toolkit per Round 14 Q3.
   - Day 4: consume v0.44.0 (eval-toolkit floor bump per Round 14 Q2) + populate `decisions/library_imports.md` rows + advance state machine (per Round 14 Q4 task #6a).
   - Day 13: open-MR monitoring (MR-3 / MR-6 / MR-8 / MR-9 / MR-10).
   - **MR-8 (scaffold v3.2 research-portfolio profile)** still blocking Day 14 chapter skeletons per Round 11 Q1'''''''' — not vacated by Round 14.
6. **Chapter skeletons** (weeks 2-3, ~3-5 days): all 13 skeletons + 5-6 notebook scaffolds with `freshness: exploratory`.
7. **Docker setup** (week 3, ~3 days): `Dockerfile` + `compose.yaml` + verify on clean machine.
8. **ETHICS.md draft** (week 3, ~1 day).
9. **Frontmatter files** (week 3, ~0.5 day): AI-disclosure + pre-alpha banner + acknowledgments. (exec-summary REMOVED per Round 17 follow-up Q2 — moved into root README.md instead.)
10. **Build-in-public bootstrap** (week 3): Twitter/X account + Mastodon account configured; `docs/build-in-public/2026-WW-week-summary.md` template; M0 announcement thread drafted.
11. **Governance files** (week 3, ~0.5 day per Q3'''): SECURITY.md + CODE_OF_CONDUCT.md (Contributor Covenant v2.1 vendored) + `.github/ISSUE_TEMPLATE/{bug,question,research-discussion}.md` + `.github/PULL_REQUEST_TEMPLATE.md` (requires test-contracts-green + CHANGELOG entry + freshness-badge state update). SECURITY.md ↔ ETHICS.md cross-references.
12. **Bibliography infrastructure — scaffold-provided** (week 2-3, ~0.5 day): `book/bibliography.bib` seeded from dossier (1:1 mapping by `claim_family` key). Scaffold v2.0+ already includes BibTeX pipeline (`scripts/build-bib.mjs` via citation-js), `<Cite>` component, `<MarginNote>` component, and `references.astro` page in academic profile (and in MR-8 new 4th profile). Portfolio just needs to populate `.bib` and run the pipeline; no plugin install needed.
13. **README + pre-alpha banner** (week 2, ~0.5 day per Q5'''): "scientific-abstract-scaled" template (Problem / Why / Approach / Results / Supporting); educational-framed pre-alpha banner with build-in-public feed pointers.
14. **ADRs**: ADR-001..013 + ADR-016 + ADR-017 + ADR-021..026 + ADR-028..032 + ADR-034 + ADR-035 + **ADR-036..038 (Round 7 Tier A: TPR@LowFPR reporting / APR metric / benchmark integrity audit)** written. ADR-027 + ADR-033 DROPPED per Round 6. ADR-039 + ADR-040 reserved for Round 7 Tier C contingency unlocks (PromptShield Lane 1 SOTA anchor / Lane 2 energy-loss variant). Total ~30-32 anticipated.

### Per-milestone

Each lane milestone: prose fill for corresponding chapter + companion notebook (if applicable) + weekly build-in-public posts + monthly deep-dive at the relevant month boundary.

### M1→M2 entry-gate — carrier-LODO pre-flight (Round 30; ADR-055)

Before Lane 2 commits, a **carrier-LODO validation read** sits at the M1-exit → Lane-2-entry boundary (an M2 pre-flight, mirroring the Round-27 EDA-arc-as-M1-entry-gate). It tests whether the multi-axis spine's "carrier is the standing wall" claim — geometric so far (silhouette by-carrier 0.197 vs by-attack-type −0.023) — survives end-to-end LoRA, and sizes Lane 2's scope. Registered in §16 (Round-30 gates) + ADR-055; criteria pre-registered at `experiments/carrier-lodo/criteria.md`; the run is a separate present-first go. Milestone *order* is unchanged (still M0→M7; no rung added).

### v0.7.0 → v1.0.0 polish window (~3 months post-M7)

- Active community feedback intake.
- v0.7.x patch releases for fixes.
- Monthly build-in-public posts only.
- M7+3mo: v1.0.0 cutover; pre-alpha banner long-since-removed; freshness badges definitively `locked`.

### Cost envelope

Unchanged from prior round: $250 base + $100 contingency. Most-likely $224-244 base; upper-bound $264-284. Contingency unlock requires `decisions/contingency_unlock_N.md`.

### Anticipated ADR set (~30-32 after Round 7 additions)

- **Round 1**: ADR-001..013, ADR-016.
- **Round 2**: ADR-017 (submission-patch-policy), ADR-018 (reproducibility-tier-ladder), ADR-019 (chapter-authoring-workflow), ADR-020 (notebook-publication-target).
- **Round 3**: ADR-021..026 (authorship / ethics / build-in-public / visibility / maintenance / no-local-workarounds).
- **Round 4**: ~~ADR-027~~ **DROPPED** (single-class metric upstream-enforced via eval-toolkit #39 + submission ADR-055), ADR-028 (community-governance), ADR-029 (book-callout-and-citation-infrastructure via scaffold v3.0 academic profile), ADR-030 (readme-structure-and-banner).
- **Round 5**: ADR-031 (book-scaffold-astro-consumption — reframed Round 6 for v3.0 npm + academic profile + portfolio-local extras), ADR-032 (7-state adoption), ~~ADR-033~~ **DROPPED** (T0 deferral reversed), ADR-034 (notebooks-reference-submission-as-foundation).
- **Round 6**: ADR-035 (portfolio-clean-T0-strategy; supersedes ADR-033).
- **Round 7 Tier A**: ADR-036 (TPR@LowFPR-reporting-requirement — all Lane 1+4 evals must report TPR@1%, 0.5%, 0.1%, 0.05% FPR alongside AUPRC; per PromptShield 2025), ADR-037 (APR-metric-Lane-4 — Meta PG2's % attacks blocked at ≤3% utility loss reported alongside ASR), ADR-038 (benchmark-integrity-audit — M0 confirms portfolio doesn't train on PINT/PromptShield/NotInject/HackAPrompt; ratifies Goodhart-discipline).
- **Round 7 Tier C reserved** (contingency unlocks): ADR-039 (Lane 1 SOTA-anchor PromptShield Llama-3.1-8B expansion), ADR-040 (Lane 2 energy-loss 3rd variant).
- **Round 8**: ADR-041 (ETHICS.md content lock — full-specificity dual-use disclosure + Public CC-BY-4.0 + hybrid reporting + BibTeX citation per §20).
- **Round 14**: ADR-042 (round-14-upstream-mr-cascade — documents the 5/7 eval-toolkit MR shipment via parallel-Codex implementation + ADR-052 → ADR-075 supersession + CI ref + eval-toolkit floor advancement; written at Day 17 batch per round-4 Q1 lock).
- **Round 15**: ADR-043 (lane-2-lora-only-scoping-and-baseline-expansion — documents the LoRA-only retrain decision per Round 15 Q1 + TF-IDF baseline addition + "other open-source models" open category for Lane 1; cites ADR-075 as supporting evidence; written at Day 17 batch per round-15 Q3 lock).
- **Round 17**: ADR-044 (three-guide-architecture-with-shared-substrate — documents the textbook + narrative + academic-IMRaD split per Round 17 Q1, fragment-import authoring pattern per Q2, sequential rollout v0.7.0 → v0.8.0 → v0.9.0 → v1.0.0 per Q3; cites the submission's hub-and-spoke anti-pattern as motivating evidence; written at Day 17 batch).
- **Round 20**: ADR-045 (eval-toolkit-v0.47-pin-and-api-pivot — documents the Round 20 cascade: eval-toolkit pin floor `>=0.44` → `>=0.47`; MR-6 + MR-10 obsoletion via upstream parallel-Codex implementation; API contract pivot to v0.47 canonical surfaces (`scorecard()` + `metric_specs.*` + top-level `sweep()` + `TextTransform` Protocol + 12 dataclass strategies); roadmap-awareness scope (act-on-shipped-only; v0.48 + v1.0 in mind); cites eval-toolkit's `~/.claude/plans/evaluate-all-the-work-twinkly-kite.md` v0.43→v1.0 staggered release plan as upstream context; written at Day 17 batch).
- **Round 21**: ADR-046 (book-scaffold-astro-v3.5-pin-and-m1-unblock — documents the Round 21 cascade: scaffold pin floor `^3.1.0` → `^3.5.0` (research-portfolio preset shipped via v3.5.0); MR-8 + MR-9 closure on upstream; M1 book authoring Round 11 v3.2 blocker resolves; written at Day 17 batch).
- **Round 22**: ADR-047 (m0-finish-out-strategy — documents the Round 22 cascade: content-filter incident handling (pre-vet for dual-use phrasing); Days 6-12 dossier deferral to user-led session; submission CI ref bump v1.2.16 → v1.3.0; priority order for remaining M0 work (Day 16 Docker → Day 5 expt-records → Day 14 chapter skeletons → Day 15 governance → Day 17 ADRs → Day 18 templates → Day 19 prep); v0.1.0 ratify deferred to user-led session; written at Day 17 batch).
- **Round 23**: ADR-048 (cross-machine-handoff-strategy — documents the Round 23 commit-to-public choice: 5 planning artifacts at `docs/planning/` + 3 compass surveys at `docs/research/compass-survey/`; deviation from submission's private-transcripts convention; rationale + cross-machine update policy; written at Day 19+ ADR carryforward).
- ADR-014/015 reserved for cost contingency unlocks (separate from Tier C method-expansion unlocks).

Total anticipated ADR set: ~38-40 (up from ~37-39 after Round 23 addition).

---

## 10. Library-first audit (8 upstream MRs block dependent lanes; 1 submission patch)

Per round-3 reinforcement + round-5 expansion: **no local workarounds**. Each missing primitive becomes an upstream merge request (eval-toolkit, runpod-deploy, research_toolkit, or **book-scaffold-astro**) that BLOCKS the dependent lane's start. Plus a submission v1.0.8 patch sweeps the single-class metric convention (ADR-027).

**Round 14 status snapshot (2026-05-21)**: 5 of 7 eval-toolkit MRs
SHIPPED via parallel-Codex implementation (v0.43.0 + v0.44.0). Portfolio
state machine for these rows advances directly to `released-vX.Y.Z` +
`pinned-needed`. Lane work at M1 / M2 / M4 / M5 can `from eval_toolkit
import ...` against `>=0.44`. See `decisions/upstream_issues.md` for the
per-row state machine.

| # | Lane / Surface | Primitive needed | Upstream repo | Blocks | State (Round 14) |
|---|---|---|---|---|---|
| ~~MR-1~~ | Lane 1 | `eval_toolkit.loaders.ood_dataset_from_manifest(yaml_path)` | eval-toolkit | M1 | **released-v0.43.0 (#48 closed 2026-05-19); pinned-needed** |
| ~~MR-2~~ (core-6) | Lane 1b | `eval_toolkit.adversarial.character_injection` — **core-6 of 12 shipped** (ZeroWidthSpace + Homoglyph + Diacritic + Whitespace + CaseRandomization + Punctuation) + Scorer-Protocol `sweep()` | eval-toolkit | M1 | **released-v0.43.0 (#49 closed 2026-05-19); pinned-needed** |
| MR-3 | Lane 2 data | `/dataset-synthesize` skill (with prompt-caching template) | research_toolkit | M3 | issue-filed (research_toolkit #1) |
| ~~MR-4~~ | Lane 2 training | `eval_toolkit.losses.RecallAtLowFPR` (Meta PG2 recipe) | eval-toolkit | M4 | **released-v0.44.0 (#50 closed 2026-05-19); pinned-needed** |
| ~~MR-5~~ | Lane 3 | `eval_toolkit.preprocessing.spotlighting` (delimit + datamark + encode variants) | eval-toolkit | M5 | **released-v0.44.0 (#51 closed 2026-05-19); pinned-needed** |
| ~~MR-6~~ | Lane 4 | `eval_toolkit.stacking.MetaLearner` Protocol + `LogisticStacker` reference impl | eval-toolkit | M6 | **released-v0.45.0 (#52 closed 2026-05-21T18:22:48Z per Round 20); pinned-needed** |
| ~~MR-7~~ | Lane 5 | `eval_toolkit.probes.ActivationDeltaProbe` (TaskTracker-style linear probe; encoder + decoder portable) | eval-toolkit | M2 | **released-v0.43.0 (#53 closed 2026-05-19); pinned-needed** |
| ~~MR-10~~ (OBSOLETED Round 20) | Lane 1b advanced-6 | `eval_toolkit.adversarial` advanced-6 dataclasses (BidiRTLInjection + TagStrippingInjection + SynonymSubstitution + TokenSplitting + UnicodeNormalization + InvisibleCharsInjection) | eval-toolkit | M1 Lane 1b full 12-tech matrix | **released-v0.47.0 (2026-05-21) as part of sweep unification + advanced-6 ship; OBSOLETES portfolio's planned MR-10 filing; eval-toolkit `ALL_TECHNIQUES` 12-tuple exports the full set** |
| ~~MR-8~~ | (was: PROMOTED TO BLOCKING per Round 11 Q1'''''''' + Round 12 Q1/Q2) Scaffold ships research-portfolio preset = union academic ∪ tools schema + 4 new generalized components + recipe + chapter template. Portfolio's `book/package.json` pins `^3.5.0` (Round 21). | `@brandon_m_behring/book-scaffold-astro` | M1 book authoring (now UNBLOCKED) | **released-v3.5.0 (#6 closed 2026-05-19T19:29:53Z per Round 21); pinned-needed via `book/package.json: ^3.5.0`** |
| ~~MR-9~~ (Round 11 Q2'''''''') | Generic frontmatter collection primitive (Zod schema + dynamic route helper) | `@brandon_m_behring/book-scaffold-astro` | Not blocking M0 | **released-v3.3+ (#7 closed 2026-05-19T19:04:30Z per Round 21); pinned-needed via Round 21 ^3.5.0 advance** |
| ~~Patch~~ | **OBSOLETE** (Round 6 Q4''''') | Single-class metric convention already enforced upstream via eval-toolkit #39 + submission ADR-055 + ADR-039 gate 3. No portfolio-side action needed; submission already at v1.1.2. | — | — | — |

**Total upstream MR effort (Round 14 update)**: portfolio-side
implementation work for eval-toolkit MRs DROPS TO ZERO — 5/7 shipped
via parallel-Codex agent. Remaining portfolio-implementation surface:
file MR-10 (~10 min), monitor MR-3 / MR-6 / MR-8 / MR-9 for upstream
closure. M0 dossier work + chapter skeletons (gated on MR-8 ship)
remain unchanged. eval-toolkit v0.43.1 (advanced-6 for MR-10) +
v0.45.0+ (for MR-6) expected to ship organically.

**M0 sub-deliverable (Round 14 reframe)**:
- ✓ Day 2.5 (2026-05-19): filed 9 issues (MR-1..MR-9).
- ✓ 2026-05-19 → 2026-05-21: parallel-Codex implemented 5 (MR-1/2/4/5/7);
  closed #48/49/50/51/53; released eval-toolkit v0.43.0 + v0.44.0.
- M0 Day 3 (NEW per Round 14 Q3): file **MR-10** issue against
  eval-toolkit (advanced-6 character_injection extension).
- M0 Day 3-4 (NEW per Round 14 Q4 → task #6a): consume v0.44.0 in
  portfolio pyproject.toml; verify `from eval_toolkit.loaders import
  ood_dataset_from_manifest` etc. resolve; populate
  `decisions/library_imports.md` rows for each consumed primitive;
  advance `decisions/upstream_issues.md` state machine rows MR-1/2/4/5/7
  to `pinned-in-portfolio`.

**Sequencing check (Round 14 update)**:
- ✓ MR-1, MR-2 core-6, MR-7 SHIPPED (v0.43.0). M1 / M2 unblocked at
  Round-14 level (separate v3.2 scaffold gate still applies to book
  authoring per Round 11).
- MR-10 (advanced-6) — TARGET: portfolio M1 Lane 1b matrix completion.
  Soft-gated on upstream v0.43.1 ship; if v0.43.1 slips past M1, Lane 1b
  matrix proceeds at core-6 scope + advanced-6 backfills when ready.
- MR-3 — TARGET: M3 (week 7). research_toolkit #1 OPEN.
- ✓ MR-4 SHIPPED (v0.44.0). M4 retrain unblocked.
- ✓ MR-5 SHIPPED (v0.44.0). M5 Spotlighting eval unblocked.
- MR-6 — TARGET: M6 (week 11). eval-toolkit #52 OPEN.
- MR-8 — TARGET: M1 book authoring (Day 14). book-scaffold-astro #6 OPEN.

If a remaining MR (MR-3 / MR-6 / MR-8 / MR-10) slips, the dependent lane / book-authoring is held back. No local workarounds — the discipline IS that the infrastructure libraries grow with portfolio's needs, modularly + testably + reusably.

**`decisions/upstream_issues.md`** tracks status per MR: `issue-filed` → `pr-opened` → `pr-merged` → `released-vX.Y.Z` → `pinned-in-portfolio`.

**Add ADR-026 (no-local-workarounds-policy)** to the anticipated ADR set: ratifies the round-3 reinforcement that primitives belong upstream, never hand-rolled in portfolio.

---

## 11. Out of scope

Unchanged plus: no v2.0 plans during v0.7.0 → v1.0.0 window (per Q5''); v2.0 ideas documented in NEXT_SESSION.md only.

---

## 12. Critical files (read before M0 kickoff)

Unchanged plus: anthropic's Commercial Service Agreement (for ETHICS.md Anthropic-ToS section).

---

## 13. Verification

### Pre-flight (M0 day 1)
```bash
npm view @brandon_m_behring/book-scaffold-astro  # confirm v3.0+ on npm
npm view @brandon_m_behring/create-book          # confirm CLI on npm
make verify-data-sources && make verify-deps && make book-pdf-smoke && make verify-docker
gh repo create --public brandon-behring/prompt-injection-portfolio
```

### End-to-end smoke (M0 close)
Unchanged plus: pre-alpha banner renders correctly + ETHICS.md is in repo root + frontmatter files render in book + `docs/build-in-public/` has M0 announcement post archived.

### M7 verification gate (Q1' + Q3' + Q2''; **Round 19 Q1 lock: textbook only at M7**)
- User reads **textbook L3 chapters** end-to-end (coherence-edit pass). Narrative + academic guides are NOT verified at M7; they have their own ship gates at v0.8.0 / v0.9.0.
- Claude fixes inconsistencies discovered in textbook.
- Textbook freshness badges → `experimental-result`; pre-alpha banner **removed on textbook routes**; v0.7.0 tag.
- Notebook nbval green across all ~5-6.
- T0/T1/T2/T3 reproducibility tiers all smoke-test.
- Hybrid sub-gate per Round 19 Q1 option C variant: verify narrative + academic placeholder routes exist with 'Shipping at v0.8.0 / v0.9.0' content.
- M7 textbook announcement thread + monthly deep-dive published.

### v0.8.0 ship gate (per Round 17 Q3 + Round 19 Q1)
- User reads **narrative L3 chapters** end-to-end (coherence-edit pass on the story arc; verify cross-chapter threading per Round 17 follow-up Q3 = heavy weave).
- Narrative chapters' fragment imports resolve against the same fragments the textbook chapters use.
- Narrative freshness badges → `experimental-result`; pre-alpha banner removed on narrative routes.
- **Quiet ship per Round 19 Q2 (user picked option B over Recommended A)**: CHANGELOG entry; no Twitter/X / Mastodon / blog announcement. Reserve viral push for v1.0.0.
- Model cards updated per Round 19 Q3: 2-link section (textbook + narrative routes).

### v0.9.0 ship gate (per Round 17 Q3 + Round 19 Q1)
- User reads **academic IMRaD L3 chapters** end-to-end. Verify compressed academic flow matches journal-paper conventions.
- Academic chapters' fragment imports resolve.
- Academic freshness badges → `experimental-result`; pre-alpha banner removed on academic routes.
- **Quiet ship per Round 19 Q2** (same rationale as v0.8.0).
- Model cards updated per Round 19 Q3: 3-link section (textbook + narrative + academic routes).

### v1.0.0 cutover gate (Q5''; **Round 19 Q2 ratifies as big-announcement moment**)
- ~3-4 months community-feedback window concluded (per Round 17 Q3 extension).
- All accepted PR fixes incorporated across all 3 guides.
- All freshness badges → `locked` (definitively).
- **v1.0.0 announcement thread (per Round 19 Q2 only-v1.0.0-final-announcement lock)** + arXiv preprint (if relevant) published. THE big announcement covering: textbook + narrative + academic guides all polished + citable. All channels (Twitter/X + Mastodon + LinkedIn + HN if traction + LessWrong if ML-safety-relevant).

### Test-contracts (CI every push)
6 contracts.

### Cost monitoring
`make cost-report`; manual; soft cap $100/lane, $250 base hard cap; contingency unlock via `decisions/contingency_unlock_N.md`.

### Dossier integrity
`make dossier-audit`; ~60-80 entries verified.

---

## 14. Open items resolved via three `/exploring-options` rounds + 12-finding review

17 questions across 3 rounds + 12 risk-mitigation findings. Plan is execution-ready.

Remaining for M0 kickoff (mechanical, not decision-worthy):
- Book working title settle (propose *The OOD Wall*).
- Pre-flight gates execution.
- Twitter/X + Mastodon account setup.

---

## 15. Risks & mitigations (12 findings from re-examination)

### Critical (resolved)
- **F1 Lane 5 timing** — submission val only (§5). **Round 16 Q4-Q5 supersedes**: Lane 5 trains on Lane 2 MR-3 corpus (not submission val), shifting timing M2 → M4 (post-Lane-2-corpus). F1 risk resolution updated; comparability with Lane 2 + Lane 4 maintained.
- **F2 Editable-dep + CI** — Two-step checkout pinning to submission tag (§3); ref: advances with submission patches (Q4').
- **F3 Data availability** — `make verify-data-sources` pre-flight blocks v0.1.0.

### High (resolved)
- **F4 Cost recount** — Most-likely vs upper-bound framing; ADR-014 auto-fires on M3 overage.
- **F5 Hidden dev work** — "Impl effort" column in milestone table.
- **F6 CI green from day 0** — Required to tag v0.1.0; especially important with public-from-M0 visibility (Q2'').
- **F7 mypy --strict from day 0** — 6th test-contract `mypy_strict_clean`.
- **F8 Encoder-vs-decoder Lane 5** — Hypothesis explicitly frames as methodology port test (§5).

### Medium (resolved)
- **F9 Q2 vs Q3 framing** — Base vs contingency line items explicit.
- **F10 Book chapter pacing** — Skeleton-first + just-in-time per Q3'.
- **F11 book-scaffold-astro existence** — Pre-flight check + local fallback.

### Low (resolved)
- **F12 Paged.js PDF rendering** — M0 Ch 00 smoke test.

---

## 16. Prioritized roadmap of additions (Round 7)

Full budget breakdown across all tiers with execution-order guidance:

### Base envelope (committed in Round 6, ~$225-265 most-likely; Round 16 reschedules Lane 5)
| Item | Cost | Milestone |
|---|---|---|
| Lane 5 ModernBERT activation extraction (trains on Lane 2 MR-3 corpus per Round 16 Q4) | $30-50 GPU | **M4** (was M2; shifted post-Lane-2-corpus per Round 16 Q5) |
| Lane 2 synthetic data gen (Sonnet + Opus audit; bail at $80) | $88-128 API | M3 |
| Lane 2 retrain × 2 LoRA variants (CE + Recall@LowFPR per Round 1 Q3; LoRA-only per Round 15 Q1) | $68 GPU | M4 |
| Lane 3 demo + Spotlighting | $1 API | M5 |
| Lane 4 fusion + adaptive eval (stacker trains on Lane 2 corpus per Round 16 Q3) | $30 API | M6 |
| Lane 1 + 1b + bandwidth (+ Round 15 TF-IDF baseline ~$0 + open-category baselines ~$0-5 each) | $8 API | M1 |
| **Subtotal** | **$225-285** | — |

### Tier A — committed, zero cost (Round 7 Q1'''''')
| Item | Cost | Milestone |
|---|---|---|
| TPR@LowFPR (0.1%, 0.05%) reporting in all Lane 1+4 evals | $0 | M1, M6 |
| APR metric in Lane 4 agentic eval | $0 | M6 |
| Benchmark integrity audit (no training on PINT/PromptShield/NotInject) | $0 | M0 |
| Cite V0 rung decomposition + V4 contamination signature + V4 stopping rule + SDD label-corruption in chapters | $0 | M1-M5 prose |
| Reframe Lane 2 hypothesis with v1.1.2 DeBERTa null result (already in Round 6) | $0 | M1 prose |

### Tier B — committed, low cost (~$20-25 total; Round 7 Q1'''''')
| Item | Cost | Milestone | ADR |
|---|---|---|---|
| Meta PG2 86M as Lane 1 reference scorer | ~$10 GPU | M1 | (Lane 1 expt record) |
| CourtGuard multi-agent baseline as Lane 1b matrix row | ~$5-10 API | M1 | (Lane 1b expt record) |
| Embedding-based scorer (XGBoost on OpenAI embeddings) as Lane 4 stacker row | ~$5 API | M6 | (Lane 4 expt record) |
| V0/V4/SDD citation hooks in book chapters | $0 | M1-M5 | — |

### Tier C — roadmap with execution optionality (Round 7 Q2'''''')
| Item | Cost | Trigger gate | Expected milestone | ADR |
|---|---|---|---|---|
| PromptShield Llama-3.1-8B Lane 1 SOTA anchor | ~$40-50 GPU | Unlock if M1 Tier B results show base detectors fall meaningfully behind expected SOTA; or if contingency budget has $50+ headroom after M3 data bail | M2-M3 | ADR-039 (Lane 1 SOTA-anchor expansion) |
| Energy-based loss Lane 2 3rd variant | ~$34 GPU | Unlock if M3 data audit kappa ≥ 0.5 AND M4 baseline 2-variant retrain shows interpretable signal; OR if a clearer loss-vs-data attribution is needed in Ch 9 | M4-M5 | ADR-040 (Lane 2 energy-loss variant) |

### Tier D — explicit v0.8+ deferrals (NEXT_SESSION.md candidates)
| Item | Estimated cost | Why deferred |
|---|---|---|
| Optimization-based attacks (GCG/PAIR/AutoDAN) as Lane 7 | ~$30-50 GPU + 2-3d | Separate attack-generation methodology; not blocking OOD wall narrative |
| Multi-rater human label audit (N=200-500) | ~$50-100 labeling | Lane 2 + Lane 1b uses Opus LLM-rater audit at v0.7.0 |
| Extended hidden-payload techniques (16-18 total: +HTML comment, white text, image steganography) | ~1-2d dev | Beyond the published 12-technique paper; nice-to-have breadth |
| WildJailbreak + WildGuardMix + HackAPrompt + TensorTrust + SPML + alespalla data sourcing | $0 (cataloging) | Submission's source manifest doesn't include these; portfolio inherits same scope |
| Production incident catalog (5-10 case studies for Ch 11 expansion: Slack AI, Gemini memory poisoning, ShadowPrompt, Comet/Perplexity, Month of AI Bugs) | ~2-3d prose | Ch 11 currently locked at AgentDojo+LLMail focus |
| τ-bench / ToolEmu / AgentDyn / AgentSentry / AgentVigil 2026 adaptive benchmarks | ~0.5d each (post-release) | Benchmarks not yet shipped or unstable |

### Cost-scenario matrix (vs $250 base + $100 contingency = $350 ceiling)

| Scenario | Total | Status |
|---|---|---|
| Base only (Round 6 plan) | $225-285 | Within base |
| Base + Tier A (free) | $225-285 | Within base |
| **Base + Tier A + Tier B** (committed in Round 7) | **$245-310** | Most-likely within base; worst-case in low contingency |
| Base + Tier A + Tier B + PromptShield | $285-360 | Needs contingency unlock $35-110; close to ceiling |
| Base + Tier A + Tier B + Energy-loss | $279-344 | Needs contingency unlock $29-94 |
| Base + Tier A + Tier B + both Tier C | $319-394 | **Exceeds ceiling by $0-44**; selective execution required |

### Execution-order guide (Round 7)

1. **M0**: Tier A all (free); Tier B citations (free); benchmark integrity audit.
2. **M1**: Tier B Meta PG2 86M ($10) + CourtGuard ($5-10); TPR@LowFPR reporting in Lane 1+1b evals.
3. **M1 → M2 gate**: review Lane 1 Tier B results. **If detector baselines fall meaningfully behind expected literature numbers, unlock PromptShield Llama-3.1-8B ($40-50)** as Tier C #1.
4. **M3 → M4 gate**: review Lane 2 data audit kappa. **If ≥0.5 AND budget has headroom, unlock energy-loss variant ($34)** as Tier C #2 — extends Lane 2 to 3-variant ablation.
5. **M6**: Tier B embedding-based scorer in Lane 4 stacker ($5); APR metric reporting.
6. **M7 / v0.7.0**: ratify; build NEXT_SESSION.md with Tier D items for v0.8+ planning.

**Contingency-unlock discipline** (per ADR-013): each Tier C execution requires a `decisions/contingency_unlock_N.md` entry pointing to the specific interim signal that justified the spend. Default is **do NOT execute Tier C** unless the gate signal fires.

#### Round-27 gates (EDA-arc entry + conditional rescopes)

Added at the milestone rethink (Round 27, 2026-05-29). The EDA entry-gate is settled; the three rescope gates are *registered branch-points* — each fires only if its trigger trips, and the full lane/chapter re-ladder remains deferred to post-LODO-results per ADR-052. Detailed rationale in [`dossier_implications_for_roadmap.md`](dossier_implications_for_roadmap.md) (Zone 2).

- **M1 entry-gate (EDA arc, settled)**: the pre-modeling EDA arc (Phases 0–3) is M1's pre-flight — RC0 BIPIA = GO + the pre-registered, falsifiable OOD-wall prediction (`experiments/eda/OOD_WALL_PREDICTION/`). The ADR-052 attack-type-LODO study *is* M1's Lane-1 modeling; it must persist per-test-attack-type diagnostic AUPRCs (harness-spec §5 retention pre-commit), which trigger the issue-#2 falsification (§6.5). Findings reframe Lane 1's value-prop to operating-point honesty.
- **M1→M2 gate (Lane 1b rescope)**: **if M1 confirms `hackett2025bypassing` 100% character-injection ASR ±5pp on the primary detector set**, cut Lane 1b from "12-technique × 5-detector matrix" → "3 representative techniques × 5 detectors + per-technique severity ranking"; reallocate freed budget to Lane 4's adaptive-eval path. Document in `experiments/lane-1b/decisions.md`.
- **M5-close gate (Lane 4 benchmark pivot)**: **if any 2 of {PINT, PromptShield, WildGuardMix} saturate above 95% AUPRC on the stacker at M5 close**, declare them legacy comparators and pivot Lane 4's headline to LLMail-Inject adaptive eval as primary.
- **M3-entry gate (Lane 5 surface-third-path)**: **if the encoder activation-delta probe does not separate direct + indirect distributions with d′ > 0.5 at the M3 smoke-test**, declare the port-only (TaskTracker-on-encoder) hypothesis falsified and promote the surface-third-path (capability-isolation pairing / CaMeL) to Lane 5's primary contribution.
- **M1 full-FT trigger-gate (Lane 1 ceiling, ADR-054)**: the M1 attack-type-LODO headline ceiling is **`lora`** (3-rung ladder `tfidf → frozen → lora`); `full_ft` is **deferred, not dropped** — it stays selectable in the harness (`detectors.RUNG_NAMES`; `--rungs full_ft`). **If the merged 3-rung §6.5 LoRA verdict is decision-relevant** — i.e. LoRA SURVIVES with a per-type test-AUPRC ceiling materially above the frozen rung (a real capacity effect worth confirming at full capacity), **or** LoRA's verdict is borderline (permutation at the 1/70 floor with bootstrap CI-low near 0) such that the never-measured full-FT OOD point (ADR-052's stated goal; ADR-075's open question) would change the writeup's claim — **then** run `full_ft × 3 folds × 3 seeds` on RunPod and fold it into the §6.5 verdict; otherwise `full_ft` stays deferred to v0.8+ (Tier D). Incremental cost ~$2-6 (LoRA-class card), disclosed in `contingency_unlock_1.md`. Hybrid execution (ADR-054): tfidf + frozen + §6.5-falsify + off-the-shelf reference baselines run **local**; only the trainable transformer rungs need the 24 GB cloud card. Cross-ref ADR-052 (added full-FT to M1), ADR-054 (deferred it behind this gate). **RESOLVED 2026-06-01 — trigger does NOT fire:** the merged 3-rung §6.5 verdict is **FALSIFIED on `lora`** (T=−0.003, perm p=0.90 — decisively null, not borderline; cheap rungs SURVIVE), so a higher-capacity full-FT point would only dissolve the wall further and change no conclusion. `full_ft` stays deferred (still selectable); ADR-052's intent preserved as a still-fireable gate. See ADR-054 "Trigger-gate resolution".

#### Round-30 gates (post-M1 re-ladder; ADR-055)

Added at the post-M1 milestone re-ladder (Round 30, 2026-06-01; ADR-055). M1's §6.5 verdict is **capacity-dependent and attack-type-axis-only** (carrier held constant), so the re-ladder reframes the spine, re-points Lane 2 to the carrier axis, and registers one new validation gate. The five Round-27 gates above are unchanged except as noted. Detailed rationale in ADR-055 + [`dossier_implications_for_roadmap.md`](dossier_implications_for_roadmap.md).

- **M1→M2 gate (carrier-LODO validation, NEW)**: the multi-axis spine asserts the **carrier** is the standing wall, but M1 held the carrier constant — that claim is so far **geometric** (carrier dominates the frozen MiniLM embedding: silhouette by-carrier 0.197 vs by-attack-type −0.023; KMeans→carrier ARI 0.98), not a modeling result. Before Lane 2 commits, run a **leave-one-carrier-out (carrier-LODO)** read across the rung ladder (tfidf/frozen local + free; `lora` ~$1) — **reusing the attack-type-LODO harness with the LODO axis swapped (attack-type → carrier) and a carrier-clustered estimator** (the §6.5 estimator was payload-clustered). It answers: does LoRA dissolve the carrier gap too (→ capacity dissolves both axes; spine revised) or does it persist (→ carrier is capacity-resistant; spine validated), and sizes Lane 2's scope. Criteria pre-registered at `experiments/carrier-lodo/criteria.md` **before** the run; the run is a separate present-first go. Cross-ref ADR-055 (gate), ADR-052 (harness reused), `experiments/eda/OOD_WALL_PREDICTION/criteria.md` (pre-registration pattern + the payload-clustered unit being swapped). **→ RESOLVED 2026-06-01 — verdict `SMALL-THROUGHOUT`** (`experiments/carrier-lodo/{verdict.json,FINDINGS.md}`; full 3-rung ladder, `lora` on a RunPod H100 ~$0.85–1.20): the carrier gap is real at frozen (G=+0.167) but **capacity-attenuated** at the LoRA ceiling (G=+0.067, CI-low +0.064 > 0 → *not* FALSIFIED; but < ½·G(frozen)=+0.084 → *not* capacity-resistant), with a **residual table-carrier wall** (+0.205; email/code close). So the carrier axis is **partially** capacity-resistant — more than the attack-type axis (which fully dissolved, FALSIFIED) but **not** a fully standing wall. The spine's "carrier is the standing wall" claim is **refined → capacity-attenuated, residual, table-concentrated**; the formal **ADR-055 amendment is deferred to a fresh present-first session** (finding recorded; ratified-decision step stays user-led). Estimator: criteria Rev 1 (AUPRC→ROC-AUC, prevalence fix — carriers 83–94 % positive) + Rev 2 (in-distribution val, confound fix), both dated before the run.
- **M1→M2 gate (Lane 1b rescope) — NOT tripped by M1**: M1 measured attack-type LODO, **not** the `hackett2025bypassing` character-injection ASR the Lane-1b trigger watches for. The Round-27 gate stays registered as-is; its trigger is rechecked at Lane 1b's own fast-iter ASR confirmation step.
- **M5-close gate (Lane 4 benchmark pivot) — watch-note**: M1's near-uniform **0.98–0.999 LoRA test AUPRC** on BIPIA-indirect is an early foreshadow of the fixed-benchmark saturation the M5-close gate watches for. The gate is **not** tripped (its criterion is 2-of-{PINT, PromptShield, WildGuardMix} > 95% AUPRC *on the stacker at M5 close* — none measured by M1); recorded here as evidence to revisit at M5-close.
- **M3-entry gate (Lane 5 surface-third-path) — unchanged; hypothesis sharpened**: the d′ > 0.5 gate stays the port-only-vs-surface-third-path decision. ADR-055 sharpens only the *hypothesis it guards* — recover the attack-type signal from **intermediate** activations (between the embedding-invisible final layer and the LoRA-visible end-to-end signal); surface-third-path (CaMeL / capability-isolation) stays the flagged lead alternative.

---

## 17. Book chapter outlines (Round 7 holistic-review focus #1)

**Companion doc**: `~/.claude/plans/portfolio-chapter-outlines.md`

13-chapter outline refined per scaffold v3.0 academic profile (KF triadic R/O/E + 7-state freshness + 18 callouts + T1-T4 source tiers + volatility classes):

- **Part I (Ch 1-3) — Representation**: definitions, threat models, OOD methodology. `stable-principle` volatility; ConceptBox + KeyIdea emphasis. Round 7 Tier B citation: Ch 1 SDD label-corruption case study.
- **Part II (Ch 4-6) — Operation**: rung ladder + statistical apparatus + threshold policy. `architectural-pattern` volatility; companion T3 notebooks for Ch 5 (bootstrap walkthrough) + Ch 6 (threshold-policy). Round 7 Tier B citations: Ch 4 V0 rung decomposition (pretraining ~68%); Ch 5 V4 contamination signature + V4 stopping rule + Bhagwatkar 2025 "Firewalls" critique sidenote.
- **Part III (Ch 7-12) — Evolution**: the 6 experimental chapters. Ch 7 anchors EchoLeak (CVE-2025-32711) + submission **ADR-075** (unified full-FT OOD drop rationale; supersedes ADR-050 R2 + ADR-052 per Round 14) + v1.1.2 DeBERTa null result (backbone-invariance). Ch 8-12 map 1-to-1 to Lane 1/1b/2/3/4/5 experiment outcomes. `feature-surface` volatility; ResultBox + CaseStudy emphasis; freshness progresses `planned` → `prose_only` → `implemented` as lanes close.
- **Part IV (Ch 13) — Methodology lessons**: CodeIntegrity 98% post-mortem anchor + V0/V4/SDD reprise (Round 7 Tier B citations). `architectural-pattern` volatility; Cross-cutting Convergence/Divergence.

**Full per-chapter detail** (KF triadic structure, callout strategy, citation density target, freshness state, volatility class, cross-references, failure-branch prose) lives in the companion doc. Original ~70KB analysis preserved in a local Claude Code transcript artifact (author-local; not in the repo).

---

## 18. Experiment record schema (Round 7 holistic-review focus #2)

**Companion doc**: `~/.claude/plans/portfolio-experiment-record-template.md`

Experiment records are the **primary unit of work** for portfolio (§2 Tier-2). Each of the 6 lanes (1, 1b, 2, 3, 4, 5) has `experiments/lane-N-<slug>/{hypothesis,protocol,results,decisions}.md`.

**4-file schema** (per `experiments/MANIFEST.json` authority graph):
- **`hypothesis.md`** (skeleton at lane START): YAML frontmatter (lane_id, slug, hypothesis_id, dates, budget) + question + 3-way outcome pre-commitment (H1/H0/H∅) + prior evidence refs + success/bail-out criteria + cost envelope + ADR pointers.
- **`protocol.md`** (skeleton at lane START): eval slate (data + SHA pins) + checkpoints + eval-toolkit/runpod-deploy command sequence (phase-by-phase) + contingency-unlock-gate thresholds + test-contract attestations + single-class slice handling + metric reporting deliverables (Tier A/B; TPR@LowFPR per ADR-036; APR per ADR-037).
- **`results.md`** (retrospective at lane CLOSE): outcome_branch fired + per-cell metrics + bootstrap CIs + paired-bootstrap delta CIs + figure refs + predictions parquet pointers + cost realized vs envelope + protocol deviations + cross-references to book chapters.
- **`decisions.md`** (retrospective at lane CLOSE): lane-internal decisions + ADR promotions + contingency-unlock entries + v0.8+ flag-fors + book chapter intake status + freshness-badge state transitions.

**Cross-reference matrix** maintained as `experiments/MANIFEST.json` (single source of truth for lane ↔ ADRs ↔ chapters ↔ dossier `claim_family` ↔ HF Hub artifacts).

**Test-contract attestation** (new): `tests/contracts/test_experiment_records_complete.py` verifies all 4 files present + populated + MANIFEST.json consistency + ADR backreferences. Adds to the 6 test-contracts → now 7.

**Round 17 follow-up Q2 extension (Recommended option-A locked)**: at lane CLOSE (M1-M6 per lane), the contract ALSO verifies the 3 fragment files exist + are populated under `book/src/content/fragments/lane-N/{methodology,results,interpretation}.mdx`. Fragments are SHARED SUBSTRATE per Round 17 Q2 — same 3 files feed all 3 guides; not per-guide. Single contract enforces "lane is done = data record (4 files) AND book fragments (3 files) shipped". Catches the failure mode "lane closed but book fragments still say TBD". Guide-chapter-MDX consumption (chapter imports the 3 fragments) is enforced at the respective guide's ship gate: textbook chapter MDX at v0.7.0 M7; narrative chapter MDX at v0.8.0; academic chapter MDX at v0.9.0.

**Worked example for Lane 1** (deferred OOD loaders + Tier B reference scorers) in companion doc; demonstrates the schema in context.

**Bootstrap effort**: ~2-3 days at M0 to write skeleton hypothesis.md + protocol.md for all 6 lanes; ~1 day per lane at close to write results.md + decisions.md.

---

## 19. Lane execution playbooks (Round 7 holistic-review focus #4)

**Companion doc**: `~/.claude/plans/portfolio-lane-execution-playbooks.md`

Each of the 6 lanes (1, 1b, 2, 3, 4, 5) has a self-contained execution playbook. Concise table:

| Lane | Milestone | Cost | Chapter | Duration | Expected outcome |
|---|---|---|---|---|---|
| **1** Direct-injection baseline + Tier B reference scorers | M1 | $10-12 | Ch 8 | ~3-4 days | positive/null (backbone-invariance test) |
| **1b** Adversarial robustness (12 char-injection + CourtGuard) | M1 (co-scheduled) | $5-8 | Ch 8 sidenote | ~2-3 days | null (encoder-only insufficient against character injection) |
| **2** Indirect training data + 2-variant loss ablation | M2-M4 | $156-196 base + $34 opt | Ch 9 | ~4-5 weeks | null expected per ADR-052; positive opens "data-bound wall" |
| **3** Spotlighting structural defense | M5 | ~$1 API | Ch 10 | ~2-3 days | null (Spotlighting helps LLMs not encoder detectors) |
| **4** Fusion + embedding-scorer + APR metric | M6 | $5-30 | Ch 11 | ~2-3 weeks | positive/null (fusion's utility-security frontier) |
| **5** TaskTracker activation probe (encoder port test) | M2 + M7 | $10-20 | Ch 12 | ~2-3 days | null expected (encoder vs decoder methodology mismatch per F8) |

Each playbook details:
- **Scope + proof goal** with ADR-052 + v1.1.2 DeBERTa null result framing
- **Eval slate** (data sources × sample sizes × SHA pins)
- **Checkpoints in scope** (which models, where they come from, what gets published to HF Hub)
- **Execution sequence** (Phase-by-Phase eval-toolkit + runpod-deploy commands; expected wall-clock + cost per phase)
- **3-way outcome branches** (positive/null/negative interpretations with book-chapter-prose hooks)
- **Contingency-unlock signal thresholds** (specific to Tier C lanes 1 + 2)
- **Test-contracts touched**
- **Book chapter citation** (what the lane's chapter prose says in each outcome)

**Total roadmap**:
- M0-M7 (~13-14 weeks): all 6 lanes shipped
- Base cost: ~$230-280 (within $250 base envelope)
- Tier C contingency unlocks (gated): +$34-100
- v0.7.0 → v1.0.0 (~3-month polish window): community feedback intake
- v1.0.0 (~month 16): portfolio piece definitively locked

---

## 20. ETHICS.md concrete draft (Round 8 holistic-review focus #3 — locked)

Locked via Round 8 sub-questions Q1''''''' (WildGuardMix-style full specificity) + Q2''''''' (Public CC-BY-4.0 + terms-of-use in card) + Q3''''''' (Hybrid GH Security Advisories + secondary email) + Q4''''''' (BibTeX with arXiv placeholder + acknowledging Anthropic-ToS-compliant language). To be extracted to `/ETHICS.md` at M0 portfolio repo creation.

---

### ETHICS.md (draft)

```markdown
# Ethics + Dual-Use Disclosure

**Project**: prompt-injection-portfolio
**License**: this document and the book (`book/`) — CC-BY-4.0 | code — Apache-2.0
**Status**: pre-alpha until v0.7.0 (see README.md banner)

---

## 1. Dual-use disclosure

This repository publishes a synthetic adversarial dataset
(`BBehring/prompt-injection-synthetic-indirect-v2`, available on Hugging Face
Hub) containing approximately 10,000 indirect-prompt-injection positives paired
with 10,000 hard-negative benign carriers. The dataset is **100% generated by
Claude Sonnet 4.6** via 12-18 templated carrier-framework prompts (email / web /
PDF / tool-output × imperative / base64-encoded / social-engineered / multi-turn
styles) with a Claude Opus N=50 inter-annotator audit (κ ≥ 0.5 minimum quality
gate per ADR-027). Full methodology is documented at
`experiments/lane-2-synthetic-retrain/protocol.md`.

This dataset is **dual-use**. It is designed and intended for training and
evaluating prompt-injection detectors. The same data, if misused, could
inform construction of more effective attack prompts.

**Do not** use this dataset (alone or in combination) as the exclusive
training corpus for an attack-generation model. The portfolio's research
position is that detection is necessary but architecturally insufficient
(per book Chs 7, 13); attack-generation research should be conducted in a
coordinated-disclosure framework, not by amplifying the corpus we publish.

We follow WildGuardMix (AllenAI 2024) and HarmBench (Center for AI Safety
2024) disclosure norms: full methodology transparency, explicit dual-use
warning, and explicit research-positioning. We do not employ HarmBench-style
context-trimming or cryptographic-hash-only release, because the dataset
contains no novel attack vectors — only documented techniques from Greshake
et al. 2023, OWASP LLM01:2025, and the compass-artifact threat-model
taxonomy. Withholding context would foreclose reproducibility (per
portfolio's T0 reproducibility tier, ADR-035) without providing meaningful
attacker uplift.

---

## 2. Intended use

The dataset, model checkpoints
(`BBehring/prompt-injection-{frozen-probe,lora}-indirect-v2-{ce,rfpr}` on HF
Hub), code (`src/`), notebooks (`book/src/content/notebooks/`), and book
chapters are intended for:

- Academic research in prompt-injection detection methodology
- Safety evaluation and red-team exercises of LLM-integrated applications
  conducted in a defensive posture
- Benchmarking of defense mechanisms (encoder classifiers, multi-agent
  debate, score fusion, activation probes, Spotlighting, etc.)
- Teaching and learning about adversarial-ML evaluation under realistic
  out-of-distribution conditions
- Reproduction and critique of portfolio's experimental results

The portfolio is explicitly **not** intended for:

- Production deployment of any classifier without external red-team
  validation (the portfolio's results show all current encoder detectors
  are bypassable; see Lane 1b 12-technique adversarial-bypass matrix)
- Training attack-generation models
- Any application that bypasses or circumvents legitimate access controls,
  authentication, or rate limits on third-party services

---

## 3. Responsible use

If you use this dataset, code, or trained checkpoints:

- **Cite the work** (see §5 below).
- **Do not** redistribute unmodified copies of the dataset for use cases
  outside detection research. If you derive a new dataset, mention this
  one in your derived work's data card.
- **Do not** train an LLM exclusively on adversarial examples. The dataset
  is balanced (~10k positives + ~10k benign carriers) by design; preserve
  that balance or document the deviation.
- **Do not** use the dataset to score open-source models for the purpose
  of public ranking without first replicating portfolio's val-fixed-TPR
  single-class metric convention (ADR-027) and TPR@LowFPR reporting
  discipline (ADR-036). Public detector leaderboards that compare
  detectors at inconsistent operating points contribute to Goodhart's-law
  pressure and weaken the field.
- **Disclose AI assistance** in derived work per emerging ACL / NeurIPS
  2026 norms.

---

## 4. Anthropic Commercial Service Agreement compliance

The synthetic dataset is generated by Claude Sonnet 4.6 under Anthropic's
Commercial Service Agreement (https://www.anthropic.com/legal/commercial-terms).

Per Anthropic's published terms (as of 2026-05-19):

- The Customer (Brandon Behring) owns the outputs ("Customer Content").
- The outputs may be redistributed.
- Anthropic may not train Anthropic's models on Customer Content from
  Services.
- The Customer may not use the Services to build a competing product or
  service, including to train competing AI models, except as expressly
  approved by Anthropic.

The portfolio's publication of this dataset is **consistent with academic
research use** under these terms. No attribution to Anthropic is legally
required.

**However, as a transparency norm**, this project explicitly acknowledges
that:

- The synthetic positives in `BBehring/prompt-injection-synthetic-indirect-v2`
  are Claude Sonnet 4.6 outputs.
- The Claude Opus N=50 inter-annotator audit (per ADR-027 protocol) used
  Claude Opus as the labeling judge.
- The book (`book/`) was developed in collaboration with Claude (see book
  frontmatter `ai-assistance-disclosure.mdx` per ADR-021).
- Detailed per-commit attribution is preserved via `Co-Authored-By: Claude
  <noreply@anthropic.com>` git trailers.

This acknowledgment is provided in the spirit of emerging 2026 academic
norms requiring transparency about AI assistance in research and
publication. Other downstream researchers who use Claude-generated outputs
under similar terms are encouraged (but not required) to follow this same
transparency pattern.

---

## 5. Citation guidance

```bibtex
@misc{behring2026portfolio,
  author       = {Brandon M. Behring},
  title        = {Prompt-Injection Detection Portfolio: A Methodology Case Study},
  year         = {2026},
  publisher    = {GitHub + Hugging Face Hub},
  howpublished = {\url{https://github.com/brandon-behring/prompt-injection-portfolio}},
  note         = {Synthetic adversarial dataset: \url{https://huggingface.co/datasets/BBehring/prompt-injection-synthetic-indirect-v2}}
  % arXiv preprint: TBD (if filed in v0.8+ per Round 3 Q4'' communication plan)
}
```

When citing in the book or other markdown surfaces, use the scaffold's
`<Cite key="behring2026portfolio"/>` component (per Round 4 Q4 citation
infrastructure + scaffold v3.0 `Cite.astro`). The `.bib` file at
`book/bibliography.bib` is the single source of truth; rendered as
hyperlinked references on `book/src/pages/references.astro`.

---

## 6. Reporting concerns

### 6.1 Security vulnerabilities (incl. adversarial-ML research disclosures)

Use **GitHub Security Advisories** for vulnerabilities in code, model
checkpoints, dataset integrity, or methodology bugs that have security
implications: https://github.com/brandon-behring/prompt-injection-portfolio/security/advisories/new

This is the right channel if:
- You discover a previously-undocumented attack vector that bypasses
  portfolio's published detectors at higher rates than the Lane 1b
  12-technique matrix shows
- You find a leakage of training data into evaluation slates
- You find a security bug in any portfolio-owned script or workflow

GitHub Security Advisories supports private embargoed disclosure with the
maintainer; we will acknowledge receipt within **3 business days** (mirroring
Anthropic's Responsible Disclosure Policy's published SLA). We do not
commit to a remediation deadline; depending on severity, we may issue a
CVE, publish a patch, or document the finding as an `experimental-result`
chapter addition.

See `SECURITY.md` for the full security policy.

### 6.2 Ethics / dataset-misuse concerns

For non-security ethics concerns (dataset misuse reports, citation
questions, content concerns, AI-disclosure questions):

**Email**: `brandon.m.behring+portfolio-ethics@gmail.com`

We will acknowledge within 3 business days. Please include:
- The concern (be specific about the artifact: dataset row / model
  checkpoint / book chapter / etc.)
- Your role (researcher / practitioner / member of the public / journalist)
- Whether you'd like attribution if we update the artifact in response

We **do not** punish good-faith reports. We do not threaten legal action
against researchers who disclose responsibly per the norms in this
document.

---

## 7. Acknowledgments

This ethics framework draws on:

- OWASP LLM01:2025 (Prompt Injection)
  https://genai.owasp.org/llmrisk/llm01-prompt-injection/
- MITRE ATLAS Framework (AML.T0051.000 + AML.T0051.001)
- Greshake et al. 2023, "Not What You've Signed Up For" (arXiv 2302.12173)
- AllenAI WildJailbreak + WildGuardMix responsible-use guidelines (2024)
- HarmBench (Center for AI Safety 2024) responsible-disclosure norms
- ACL Policy on Publication Ethics (effective April 2025)
- Anthropic Responsible Disclosure Policy
  https://www.anthropic.com/responsible-disclosure-policy
- Anthropic Commercial Service Agreement
  https://www.anthropic.com/legal/commercial-terms

---

## 8. Version + change log

- **v0.1.0** (M0, 2026-05-XX): initial release under pre-alpha banner.
- See top-level `CHANGELOG.md` for portfolio's release history.
```

---

### HF Hub dataset card frontmatter (companion content)

```yaml
---
license: cc-by-4.0
task_categories:
- text-classification
tags:
- prompt-injection
- adversarial-ml
- research-use
- responsible-ai
size_categories:
- 10K<n<100K
language:
- en
pretty_name: "Synthetic Indirect Prompt-Injection Training Data v2"
---

# Synthetic Indirect Prompt-Injection Training Data v2

**This dataset is part of the prompt-injection-portfolio
research project.** Please read the project's `ETHICS.md`
(https://github.com/brandon-behring/prompt-injection-portfolio/blob/main/ETHICS.md)
**before downloading or using this data.**

## Terms of use

By downloading this dataset, you agree to:

1. Use it only for prompt-injection detection research, safety evaluation,
   or related defensive work — not for training attack-generation models.
2. Cite the source (BibTeX in ETHICS.md §5).
3. Report any misuse you encounter to the contact in ETHICS.md §6.2.

Full responsible-use language is in the project's ETHICS.md.

## Composition

[full methodology summary lifted from experiments/lane-2-synthetic-retrain/results.md
at M3 close — Sonnet 4.6 generation; 12-18 carrier templates; Opus N=50 audit κ; etc.]
```

---

### Adds new ADR

- **ADR-041 (ETHICS.md content lock)** ratifies §20a's content + HF Hub
  dataset card alignment. Codifies the WildGuardMix-style full-specificity
  pattern, the Public CC-BY-4.0 license choice, the hybrid reporting
  channel, and the BibTeX + acknowledging-Anthropic citation pattern.
  Total anticipated ADR set rises to ~31-33.

---

## 21. M0 day-by-day execution sequence (Round 9 lock)

Locked via Round 9 sub-questions: MR scheduling = concentrated week 1 + spillover to week 3; dossier ↔ chapter skeletons = parallel; M0 close-out gate = all deliverables green + CI passing + book PDF smoke OK.

### Week 1 — Foundation
- **Day 1 (~6h session)**: Pre-flight gates run in this order:
  1. `npm view @brandon_m_behring/book-scaffold-astro` (confirm v3.0+)
  2. `npm view @brandon_m_behring/create-book` (confirm CLI on npm)
  3. `make verify-data-sources` (6 OOD sources; SHA pins)
  4. `make verify-docker` (Docker daemon + base image pullable)
  5. (Optional) `make book-pdf-smoke` if a scratch directory is available
  6. `gh repo create --public brandon-behring/prompt-injection-portfolio`
  7. Initial commit: `README.md` v0.1.0-pre placeholder + `LICENSE` (Apache-2.0) + **`ETHICS.md` extracted from plan §20a** + `.gitignore` (gitignore submission + transcripts patterns)
- **Day 2 (~6h)**: Scaffold bootstrap. **DONE 2026-05-19** (commits `f011726` scaffold + pyproject + verify-deps; `11175db` CI draft):
  1. `npx @brandon_m_behring/create-book prompt-injection-portfolio --profile=academic`
  2. `uv init` + `pyproject.toml` with `eval-toolkit>=0.42` (Round 14 advances to **`>=0.44`**) + `runpod-deploy>=0.8.4` + `research-toolkit` + submission editable dep via `[tool.uv.sources]`
  3. `uv run python scripts/verify_editable_dep.py` (validates sibling-layout import path)
  4. Draft `.github/workflows/ci.yml` with two-step `actions/checkout@v4` (portfolio + submission `ref: v1.1.1` → **Round 14 Q1: advance to `ref: v1.2.12`**)
- **Day 2.5 (~3h)**: **DONE 2026-05-19** (commit `e6a2234`). Filed 9 upstream MR issues per Round 10 ongoing-issue-filing discipline (5 of these subsequently closed by parallel-Codex agent within ~24h). See `decisions/upstream_issues.md` for state machine + issue URLs.
- **Day 3a (~2h) — Round 14 reconciliation** (per Round 14 follow-up `/exploring-options` Q1 split; **3-commit granularity** per follow-up round 2 Q3). **Verify-first ordering** (per follow-up Q2): pin local + smoke-test imports BEFORE committing the pin bump. **Dynamic tag detection** (per follow-up round 2 Q2): probe latest pushed submission tag rather than hardcoding `v1.2.12` (in case it isn't pushed yet).
  1. **Dynamic tag detection**: `git -C ../prompt-injection-detection-submission ls-remote --tags origin | grep -E 'refs/tags/v1\.[0-9]+\.[0-9]+$' | awk -F'/' '{print $NF}' | sort -V | tail -1`. Captures latest pushed semver tag (e.g., `v1.2.12` if pushed; else `v1.2.11`). Pin TARGET = captured value; use throughout Day 3a steps below.
  2. **Edit `pyproject.toml`** (round-2 Q1: add extras now):
     - `eval-toolkit>=0.42` → `eval-toolkit[probes,losses]>=0.47`
     - (Verify uv resolver handles the `[extras,extras]>=floor` syntax; if not, split into two lines + drop the `[extras]` from the main pin.)
  3. **Local resolve check**: `uv sync --extra dev` resolves `eval-toolkit==0.44.x` + transitively `torch` + `transformers` extras. If resolver fails, halt + diagnose (e.g., split into two pin lines).
  4. **Import + tiny end-to-end smoke-tests** (Python REPL; round-2 round-4 Q3 lock + Round 20 v0.47 API overhaul):
     ```python
     # (a) Imports — v0.47 canonical surfaces (Round 20 lock: no SimpleNamespace,
     # no scalar metric imports, no per-module Protocols, no module-level sweep)
     from eval_toolkit import scorecard, sweep, metric_specs
     from eval_toolkit.protocols import TextTransform, Probe, MetricSpec, MetaLearner
     from eval_toolkit.loaders import ood_dataset_from_manifest, OodManifestLoader
     from eval_toolkit.adversarial import (
         # 12-technique dataclass strategies (Round 20 — all 12 ship in v0.47.0)
         ZeroWidthSpaceInjection, HomoglyphSubstitution, DiacriticInjection,
         WhitespaceInjection, CaseRandomization, PunctuationInjection,    # core-6
         BidiRTLInjection, TagStrippingInjection, SynonymSubstitution,
         TokenSplitting, UnicodeNormalization, InvisibleCharsInjection,   # advanced-6
         ALL_TECHNIQUES,  # 12-tuple
     )
     from eval_toolkit.preprocessing import DelimitVariant, DatamarkVariant, EncodeVariant
     from eval_toolkit.losses import RecallAtLowFPR
     from eval_toolkit.probes import ActivationDeltaProbe
     from eval_toolkit.stacking import LogisticStacker  # v0.45.0 per Round 20

     # (b) Tiny e2e: mock 2-row YAML manifest; confirm DataFrame schema
     import yaml, tempfile, pandas as pd
     mock_manifest = {"slices": {"toy": {"url": "...",  # tiny HF fixture or local dummy
                                          "sha256": "<sha>", "text_field": "text",
                                          "label_field": "label",
                                          "label_map": {"clean": 0, "injected": 1},
                                          "sample_size": 2, "seed": 42}}}

     # (c) Call-surface ping for v0.47 canonical APIs:
     # Adversarial dataclass — instantiation + transform
     attack = ZeroWidthSpaceInjection()
     transformed = attack.transform("test")            # str returned
     assert len(ALL_TECHNIQUES) == 12

     # Preprocessing dataclass — TextTransform Protocol satisfaction
     defence = DelimitVariant(delimiter="<<", end=">>")
     spotlit = defence.transform("test")

     # Top-level sweep — mixes attack + defence strategies (Round 20 sweep unification)
     # sweep([attack, defence], texts=["a", "b"]) returns DataFrame with
     # columns: text_id, variant, transformed_text

     # Scorecard surface (Round 20 v0.46+ canonical eval entry)
     # scorecard(y_true, y_score, metrics=[metric_specs.pr_auc,
     #                                     metric_specs.roc_auc,
     #                                     metric_specs.brier,
     #                                     metric_specs.ece(n_bins=15)])
     # returns Mapping[str, MetricResult]

     # nn.Module loss
     import torch
     loss_fn = RecallAtLowFPR(fpr_target=0.01)

     # Activation probe
     probe = ActivationDeltaProbe(
         backbone="sentence-transformers/all-MiniLM-L6-v2",
         layer_index=-1, aggregate="mean",
     )

     # Logistic stacker (Round 20 — MR-6 shipped in v0.45.0)
     stacker = LogisticStacker(C=1.0, class_weight="balanced")
     # stacker.fit(score_matrix, y) at lane-work time
     ```
     If any (a-c) step surfaces an API mismatch vs eval-toolkit v0.47.0
     CHANGELOG, document the diff in `decisions/upstream_issues.md`
     "Filed during execution" section + file a clarification issue
     against eval-toolkit. Do NOT silently mutate portfolio's
     expectations. **Round 20 note**: v0.48 + v1.0 are coming with
     additional API expansion / stability lock; portfolio's lane code
     should NOT preemptively use v0.48-unreleased APIs (e.g., sweep's
     `strategy_id` column).
  5. **Edit `.github/workflows/ci.yml`**: `ref: v1.1.1` → `ref: <captured-tag-from-step-1>`.
  6. **COMMIT 1 (deps + CI workflow change)** — Round 21 expands to ALSO bump scaffold pin: `feat: M0 Day 3a/c1 — bump eval-toolkit floor to v0.47 + bump book-scaffold-astro to ^3.5.0 + advance submission CI ref to <captured-tag>`. Push → CI green expected (Day 2 allow-failure shells still active). [Bumps include book/package.json line `"@brandon_m_behring/book-scaffold-astro": "^3.5.0"` per Round 21 Q1.]
  7. **Populate `decisions/library_imports.md`**: 5 rows under `eval-toolkit` section (one per consumed primitive: symbol + version-pin `>=0.44` + Used-in `<pending lane work>` + First-commit hash = commit 1's SHA). Plus 1 row backfill for `defineBookSchemas()` from book-scaffold-astro (already consumed at Day 2).
  8. **Advance `decisions/upstream_issues.md` state machine**: MR-1/MR-2/MR-4/MR-5/MR-7 rows from `issue-filed` → `released-v0.43.0` (MR-1, MR-2, MR-7) or `released-v0.44.0` (MR-4, MR-5) → `pinned-in-portfolio` (cite commit 1's SHA).
  9. **COMMIT 2 (tracking files)**: `feat: M0 Day 3a/c2 — populate library_imports.md + advance upstream_issues.md state machine (MR-1/2/4/5/7 pinned)`. Push.
  10. **Rewrite `NEXT_SESSION.md`** (round-2 Q4: full rewrite, not delta-append): compact existing Day 1 / Day 2 / Day 2.5 sections into single "M0 progress summary" + fresh forward-looking sections (Round 14 absorbed; Day 3a/3b/4 next-steps; Day 5+ buffer; open-MR watch list).
  11. **COMMIT 3 (docs)**: `docs: M0 Day 3a/c3 — NEXT_SESSION.md full rewrite (Round 14 absorbed; Day 3a/3b/4 forward-look)`. Push.
- **Day 3b (~4-6h) — 7 test-contracts implementation + tighten gates**.
  1. Implement 7 test-contracts in `tests/contracts/`: `no_handrolled_metrics`, `predictions_persisted`, `leakage_scan_present`, `glossary_complete`, `library_imports_registered`, `mypy_strict_clean`, **`experiment_records_complete`** (new per §18 Round 7 focus).
  2. Configure ruff (check + format) + mypy --strict; remove `2>&1 || echo "..."` allow-failure shells from `.github/workflows/ci.yml`.
  3. Verify each contract individually with `uv run pytest -m contract -k <name>` before pushing.
  4. Commit: `feat: M0 Day 3b — 7 test-contracts active (mypy --strict + ruff + contract markers)`. Push → wait for CI fully-green (all gates real) → **tag `v0.1.0-pre` checkpoint**.
- **Day 4 (~0.5h, OBSOLETED MR-10 filing per Round 20)** — Round 14 Q3 planned MR-10 filing for the advanced-6 character_injection techniques is now **OBSOLETE**: v0.47.0 already shipped all 12 dataclasses + `ALL_TECHNIQUES` 12-tuple (see Round 20 narrative). Day 4 simplifies to:
  1. **Verify advanced-6 present in v0.47.0** (Python REPL):
     ```python
     >>> from eval_toolkit.adversarial import (
     ...     BidiRTLInjection, TagStrippingInjection, SynonymSubstitution,
     ...     TokenSplitting, UnicodeNormalization, InvisibleCharsInjection,
     ...     ALL_TECHNIQUES,
     ... )
     >>> len(ALL_TECHNIQUES)  # 12 (core-6 + advanced-6)
     >>> BidiRTLInjection().transform("test")  # confirm dataclass works
     ```
  2. **Update `decisions/upstream_issues.md`** to mark MR-10 row as `released-v0.47.0 (OBSOLETED — work shipped before portfolio could file the issue)`; advance MR-6 row to `released-v0.45.0`; pinned-in-portfolio via Round 20 floor bump in Day 3a/c1.
  3. **Open-MR monitoring** (~15 min): check status of MR-3 (research_toolkit #1) / MR-8 (book-scaffold-astro #6) / MR-9 (book-scaffold-astro #7); update upstream_issues.md state if any have advanced. **eval-toolkit MR monitoring no longer needed** — all 7 portfolio MRs shipped.
  4. Commit: `feat: M0 Day 4 — Round 20 reconciliation (MR-6 + MR-10 obsoleted by eval-toolkit v0.45.0 + v0.47.0)`.
- **Day 5 (freed)** — Round 14 vacated the prior Day 5 MR-implementation slot. Use freed bandwidth to start Day 6 dossier sprint early OR draft Lane 1/1b/5 experiment-record skeletons (§18) ahead of Day 14 chapter skeletons.

### Week 2 — Dossier sprint + Part I+II chapter skeletons (Round 14: MR-2 implementation slot vacated)
- **Days 6-10 (~12-15h session, ~25-40h Claude time)** in parallel:
  1. **Dossier sprint**: compass artifact decomposition → 5 sub-areas first (`attacks_defenses` / `architectural_defenses` / `detection_methodologies` / `benchmarks` / `datasets`) via `research_toolkit` `/research-gather` + `/dossier-build` pipeline.
  2. **MR-10 follow-up watch** (Days 6-8, ~30 min/day): monitor eval-toolkit v0.43.1 ship status (advanced-6 character_injection); if shipped → bump pyproject pin → mark MR-10 row `pinned-in-portfolio` in `upstream_issues.md`. Lane 1b matrix design (Day 9-10) treats core-6 as committed + advanced-6 as backfill if v0.43.1 lands during M0.
  3. **Chapter skeletons Part I + II** (Days 9-10): Ch 1-6 with `<Cite key="TBD-..."/>` placeholders for citations that will be filled as dossier matures. Freshness state = `scaffolded`. KF triadic structure (R/O/E) per scaffold pedagogy/kf-chapter-shape.md.

### Week 3 — Round-out + ratification (Round 14: MR-7 implementation slot vacated)
- **Days 11-12 (~10h)**: Dossier remaining 6 sub-areas (`critiques` / `incidents` / `commercial_detectors` / `optimization_attacks` / `multimodal` / `future_work`). Run `/dossier-audit` iteratively until all 60-80 entries `verified` or `human-review-queued`.
- **Day 13 (~3h, was ~6h MR-7 implementation; freed by Round 14 closures)**: Open-MR monitoring + slack/buffer day. Check status of:
  - MR-3 (research_toolkit #1) — `/dataset-synthesize` skill
  - MR-6 (eval-toolkit #52) — stacker Protocol + reference impl
  - MR-8 (book-scaffold-astro #6) — v3.2 research-portfolio profile (BLOCKS Day 14)
  - MR-9 (book-scaffold-astro #7) — generic frontmatter primitive (not blocking)
  - MR-10 (eval-toolkit advanced-6) — v0.43.1 ship status

  Use freed bandwidth for: extra dossier polishing if needed; ADR-036/037/038 Tier A drafts if Day 17 looks tight; experiment-record skeletons (§18) for Lane 1/1b/5 if not yet started.
- **Day 14 (~6h)** *(UNBLOCKED per Round 21 — scaffold v3.5.0 shipped research-portfolio preset 2026-05-19; was previously gated on Round 11 Q1'''''''' v3.2 wait)*: **Textbook guide ONLY per Round 17 Q4**. Chapter skeletons **Part III + IV** (Ch 7-13) of the textbook guide; freshness = `scaffolded`. Path: `book/src/content/textbook/`. Backfill TBD citations from Part I+II skeletons now that dossier is mature. Seed `book/bibliography.bib` (1:1 mapping with dossier `claim_family` keys). Also scaffold the **shared fragments structure** per Round 17 Q2: `book/src/content/fragments/lane-{1,1b,2,3,4,5}/` directories created (empty at M0; populated as lanes close at M1-M6). **Pre-condition (Round 21)**: confirm `book/package.json` pins `"@brandon_m_behring/book-scaffold-astro": "^3.5.0"` (advanced from ^3.1.0 in Day 3a/c1 commit per Round 21). **Story arc + Academic IMRaD guides are NOT scaffolded at M0** (per Round 17 Q3 sequential rollout); they ship at v0.8.0 / v0.9.0.
- **Day 15 (~5h)**: Frontmatter files + governance + README:
  1. `book/src/content/frontmatter/{title-page,ai-assistance-disclosure,pre-alpha-banner,acknowledgments}.mdx` (exec-summary.mdx REMOVED per Round 17 follow-up Q2; exec-summary content lives in root README.md)
  2. `SECURITY.md` (with adversarial-ML disclosure path + GH Security Advisories cross-ref to ETHICS.md per Round 8 Q3''''''')
  3. `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1 vendored from contributor-covenant.org)
  4. `.github/ISSUE_TEMPLATE/{bug,question,research-discussion}.md`
  5. `.github/PULL_REQUEST_TEMPLATE.md` (requires test-contracts-green + CHANGELOG entry + freshness-badge state update)
  6. `README.md` scientific-abstract-scaled per ADR-030 (problem / why / approach / results / supporting) **PLUS Round 17 follow-up Q3 "3 peer-level entry-points" section**: '3 ways to read this work' with sub-sections for Textbook (active at v0.7.0) + Narrative (placeholder 'Shipping at v0.8.0') + Academic IMRaD (placeholder 'Shipping at v0.9.0'). Each guide gets a link to its root Astro route. All 3 active at v1.0.0.
- **Day 16 (~4h)**: Docker T2 setup. `Dockerfile` + `compose.yaml` + `verify_docker.py`. Test on clean machine if available.
- **Day 17 (~4-6h)**: ADRs writing. ~26-28 ADRs total. Bulk-draft via templates from plan §1 decisions tables (Rounds 1-8). Light Michael-Nygard <400 words each. Reference dossier entries by `claim_family` key.
- **Day 18 (~2h)**: Build-in-public account setup.
  1. Twitter/X account: `@brandonmbehring` or similar; profile bio with portfolio URL + book URL
  2. Mastodon `sigmoid.social` account (ML research community)
  3. Draft M0 announcement thread (~3-5 tweets); save to `docs/build-in-public/2026-WW-week01-announcement.md`
- **Day 19 (~2h)**: **M0 close**.
  1. `make ratify-milestone M=M0` (runs full test suite + 7 test-contracts + nbval + `/dossier-audit` + Docker smoke + book PDF smoke)
  2. `git push origin main` → CI green required
  3. `git tag v0.1.0`
  4. `gh release create v0.1.0` with M0 announcement notes
  5. Post M0 announcement thread to Twitter/X + Mastodon
  6. Archive thread to `docs/build-in-public/2026-WW-week01-announcement.md`

### M0 ratification checklist (Day 19 close gate per Round 9 Q3)

*(Reconciled 2026-05-29 against `M0_READINESS.md`: technical gates green at `v0.1.0-pre`+68 commits; formal `v0.1.0` tag + announcement remain user-led — see `M0_READINESS.md` §"User-led items remaining".)*

- [x] All 7 test-contracts pass in CI
- [x] mypy --strict clean on all `src/` modules
- [x] ruff format check clean
- [x] pytest unit + smoke green
- [x] nbval green across 5-6 notebook scaffolds (empty notebooks OK at v0.1.0)
- [x] book/dist-pdf/portfolio.pdf renders without Paged.js errors
- [x] Pre-alpha banner renders on README + book frontmatter
- [x] `ETHICS.md` + `SECURITY.md` + `CODE_OF_CONDUCT.md` present at repo root
- [x] All 13 chapter skeletons exist with KF triadic structure
- [x] All 6 experiment record `experiments/lane-N-*/hypothesis.md` + `protocol.md` populated (skeleton state, not stubs)
- [x] `experiments/MANIFEST.json` populated for all 6 lanes
- [x] `book/bibliography.bib` seeded 1:1 with dossier `claim_family` keys
- [x] `decisions/library_imports.md` lists all upstream primitives consumed
- [x] `decisions/upstream_issues.md` state machine current (8/9 MRs closed; MR-12 added) — *(R26; was "tracks MR-1 + MR-2 + MR-7")*
- [x] `pyproject.toml` pins `eval-toolkit[probes,losses]>=1.0` (v1.6.0 in `uv.lock`; R26 per ADR-051; was `>=0.47`) + `runpod-deploy>=0.8.4`; `book/package.json` pins `@brandon_m_behring/book-scaffold-astro: ^4.4.0` (R26; was `>=3.0`); `research_toolkit` dropped as a dep → repo-local tooling clone (ADR-051)
- [x] Submission `[tool.uv.sources]` ref = `v1.3.0` (two-step CI ref; R22, was `v1.1.1`)
- [x] Docker build clean + `verify_docker.py` green
- [x] `gh repo view brandon-behring/prompt-injection-portfolio` returns 200
- [x] First push CI green
- [ ] M0 announcement thread posted to Twitter/X + Mastodon — **DEFERRED (user-led; X/Mastodon accounts not yet created; see `M0_READINESS.md` §"User-led items remaining")**

### Day-by-day total

- 19 working days × ~4-6h session/day = ~76-114h Claude Code session time
- Spread over 3 calendar weeks (1 week = 5 working days; some days may overflow)
- Plus ~1-2h/week human-time for build-in-public + GH operations
- Cost: $0 in M0 (no GPU; metered API only at M3 lane 2 data gen)

### Schedule risk register (per F2 / F3 / F11 risk findings)

- **MR-1/2/7 slippage**: each MR is ~1-3 days; if any slips by >2 days, dependent lane (Lane 1 / Lane 1b / Lane 5) M1 start is delayed by the same amount. M0 close (Day 19) is NOT contingent on lane work — just M0 deliverables.
- **Pre-flight gate failure**: if `npm view @brandon_m_behring/book-scaffold-astro` returns no v3.0+, fall back to scaffold v2.0 local clone + npx-create-book.sh wrapper (Round 5 fallback). +1-2 days at Day 1.
- **Data-source download fail**: if any of 6 OOD sources unavailable, document in `decisions/upstream_issues.md` + defer the affected lane's eval scope to v0.8+. +0-1 days at Day 1.
- **Docker test fail on clean machine**: defer T2 tier to v0.2.0; document in `decisions/contingency_unlock_*.md`. +0 days (drops scope; ships v0.1.0 with T0+T1+T3 only).

---

## 22. Memory cross-references

Patterns extracted from this planning session, saved as global feedback memories
for future projects:

- **`round-7-holistic-review-pattern.md`** — when to spawn multi-area parallel
  deep-dive review for accumulated multi-round planning sessions
- **`lane-playbook-pattern.md`** — per-experiment execution playbook structure
  (scope / slate / sequence / outcomes / gates / citations)
- **`experiment-record-4-file-schema.md`** — hypothesis/protocol/results/decisions
  template for exploratory ML work
- **`companion-doc-pattern-for-large-plans.md`** — extract to companion docs
  when a plan section exceeds ~500 lines

Project-specific memory updates:
- **`portfolio-plan-approved.md`** — updated with Round 6 + Round 7 progress
  (npm pivot, submission v1.1.2, Tier A/B/C framework, companion docs)

Memory index at `~/.claude/projects/-home-brandon-behring-Claude-prompt-injection-detection-submission/memory/MEMORY.md`.
