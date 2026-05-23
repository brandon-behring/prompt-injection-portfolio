# Dossier implications for the portfolio roadmap

**Status**: M0 close synthesis (Round 24, 2026-05-23)
**Audience zones**: Exec summary (build-in-public-ready) → per-lane
operational (LLM-agent-primary) → reflective margins (user-primary)
**Citation discipline**: bibkeys resolve to `book/bibliography.bib`
(157 entries) + ADR numbers (50 total entries post-Round 24) + public
URLs via `cache_manifest.yml` artifacts under
`docs/research/<topic>/cache_manifest.yml`. No local-only file paths.

---

## TL;DR — 5 bullets

1. **The OOD-evaluation-wall thesis carries**: 17 body-quote-anchored
   carriers + 28 abstract-level anchors converge across 5 topic
   dossiers (210 entries) on a single observation: detectors that
   report 95%+ AUPRC on held-out test sets degrade by 30-60pp under
   even mild OOD conditions (character-level perturbation, paraphrase,
   distribution drift). Book Ch 5/7/9/11/12/13 each find their primary
   evidence here.
2. **TPR@LowFPR is now a multi-paper convergence, not a single-paper
   advance**: three independent carriers (`jacob2025promptshield`
   Table 4; `li2024injecguard` over-defense quantification;
   `meta2025promptguard2-86m` vendor card) treat low-FPR operating
   points as the headline metric. ADR-036 is no longer a "novel
   methodology contribution" — it's a "ratify the emerging norm"
   contribution.
3. **Vendor landscape is consolidating**: 6 commercial vendor entries
   in `detector-landscape/` (HiddenLayer, Robust Intelligence, Vijil
   Dome, Guardrails AI, CalypsoAI, SafePrompt) document two
   acquisitions in the past 12 months (Robust Intelligence → Cisco;
   CalypsoAI → F5) + two parked surfaces (CalypsoAI's calypso.ai;
   SafePrompt's safeprompt.com). The portfolio's value to readers
   shifts: detector cataloging is decreasingly novel; methodology
   critique increasingly so.
4. **Saturated benchmarks justify LLMail-Inject adaptive eval**: the
   `abdelnabi2025llmailinject` carrier (cross-classified across 4
   topics) operationalizes adaptive evaluation in a way that PINT +
   PromptShield + WildGuardMix cannot. Lane 4's protocol should
   declare a hard pivot to LLMail-Inject if M3 results suggest
   benchmark saturation per `jung2026postmortem`'s 98%-accurate-and-
   still-broken framing.
5. **Composition_audit methodology is mature**: 9-paper claim family
   (Xu/Deng/Yang/White/Oren/Shi/Sainz/Zawalski/M-2026) provides
   drop-in audit primitives (`shi2023minkprob` Min-K%-Prob;
   `zawalski2025codec` CoDeC). Lane 2's MR-3 synthetic-corpus +
   ADR-038 audit step can leverage these directly at M2 close
   pre-Tier-C unlock.

---

## Zone 1 — Cross-cutting findings

### 1.1 Methodology critique convergence (4 papers, 1 axis)

The dossier surfaces 4 carriers that converge on a single critique
of held-out-only evaluation:

- **`bhagwatkar2025firewalls`** (cross-classified to
  detector-landscape `detector_benchmarks` + direct-vs-indirect
  `production_incidents` + training-and-evaluation
  `benchmark_validity` + agentic-security-architecture
  `agentic_bench_critique`): firewalls/guardrails fail under character-
  level perturbations that don't appear in training distributions.
- **`hackett2025bypassing`** (cross-classified to detector-landscape
  + direct-vs-indirect + training-and-evaluation): 100% character-
  injection ASR against multiple detector backbones, including
  ProtectAI v1/v2.
- **`choudhary2025detect`** (training-and-evaluation `benchmark_validity`):
  "how not to detect" methodology critique paired with Choudhary's
  production_incidents carrier (`choudhary2025hownotdetect`).
- **`jung2026postmortem`** (training-and-evaluation `benchmark_validity`):
  industry post-mortem framing "98% accurate and still broken" — the
  thesis-statement-shaped carrier for the OOD-wall.

These 4 carriers don't merely agree; they converge through different
methodologies (character-perturbation, post-mortem, ASR-quantification,
how-not-to-detect critique) onto the same conclusion. The book's thesis
chapters can cite **the convergence pattern itself** as evidence —
not just any one paper.

**Why this matters**: a thesis that depends on one paper can be
attacked by attacking that paper. A thesis that depends on a 5-paper
convergence with methodological diversity has a much higher bar to
clear for adversarial reading.

### 1.2 OOD-wall thesis carriers (17 body-quote-anchored)

The body-quote anchoring discipline per ADR-049 prioritized the OOD-
wall thesis carriers. These ~17 entries carry verbatim_match anchors
with byte-offset + sha256_of_span precision (per
`research_toolkit/validators/evidence_ledger.py` span schema):

- 5 in `detector-landscape/`: `bhagwatkar2025firewalls`,
  `hackett2025bypassing`, `jacob2025promptshield`,
  `jung2026postmortem`, plus 1 carrier per body-anchored vendor URL.
- 6 in `training-and-evaluation/`: subset of the composition_audit
  9-paper family + `fomin2026benchmarkslie` + `choudhary2025detect`.
- 3 in `rag-injection-defenses/`: `production_rag_incidents`
  (EchoLeak/Comet/`greshake2023bingadvisory`).
- 3 in `agentic-security-architecture/`:
  `agentic_debenedetti2024agentdojo`, `agentic_abdelnabi2025tasktracker`,
  `agentic_li2024injecguard`.

These give chapter-by-chapter book authoring high-resolution evidence
anchors. The remaining ~193 entries (of 210) use abstract-level
cached HTML extraction, sufficient for status verification + general
literature anchoring without over-engineering.

### 1.3 Vendor landscape consolidation (2 acquisitions + 2 parked)

Per ADR-050 vendor cluster posture:
- **Robust Intelligence → Cisco** (verified Sprint 3 via Cisco
  announcement blog cached as
  `robustintelligence2025_cluster`).
- **CalypsoAI → F5** (calypso.ai parked at domainnames.com; product
  surface moved to f5.com/products/ai-guardrails per
  `detector-landscape/` cross-link in `calypsoai2025_cluster`).
- **HiddenLayer**: independent + verified
  (`hiddenlayer2025_cluster`).
- **Guardrails AI**: independent + verified
  (`guardrailsai2025_cluster`).
- **Vijil AI**: independent + verified
  (`vijildome2025_cluster` after URL correction Sprint 3).
- **SafePrompt**: parked surface (`safeprompt.com` for-sale on
  Spaceship.com); originating press release retained as
  `safeprompt2025_cluster`.

**Implication**: the portfolio's "detector survey" framing should
treat vendor cataloging as **lower-priority** (the market is
consolidating; vendor names rotate fast). The portfolio's
**methodology critique** framing should be **higher-priority** (the
critiques don't go stale with vendor rotation).

### 1.4 Saturated benchmark exhaustion (PINT/PromptShield/HackAPrompt)

The dossier surfaces 3 indicators that the headline benchmark suites
(PINT/PromptShield/WildGuardMix/HackAPrompt) are saturating:

- **`jung2026postmortem`** "98% accurate and still broken" frames
  high-AUPRC as a saturation indicator, not a quality indicator.
- **`fomin2026benchmarkslie`** (`ood_evaluation_methodology`)
  documents the gap between benchmark AUPRC and true-distribution
  shift behavior.
- **`abdelnabi2025llmailinject`** offers an adaptive-eval alternative
  that doesn't saturate (the challenge is structurally adversarial,
  not a fixed test set).

**Implication**: Lane 4's APR metric (per ADR-037) + LLMail-Inject
adaptive frame should be the primary headline in M6 reporting, with
saturated benchmarks reported only as legacy comparators.

### 1.5 Composition_audit methodology maturity (9 papers, drop-in)

The 9-paper `composition_audit` family (per Phase C ADR-038
cross-references) is mature enough to use as drop-in audit primitives.
Lane 2's MR-3 synthetic-corpus path + ADR-038 audit step can leverage:

- `shi2023minkprob` Min-K%-Prob — token-likelihood-tail detection
  primitive
- `zawalski2025codec` CoDeC — in-context-learning-based detection
- `oren2023provetestcontam` exchangeability hypothesis test

These are not novel methodology — they're field-validated tools the
portfolio can adopt without re-deriving.

---

## Zone 2 — Per-lane operational implications

### Lane 1 (M1) — Direct-injection baselines + reference scorers + classical floor

**Linked ADRs**: 036 + 038 + 043 + 045
**Dossier claim_families**: `detector_architectures`,
`detector_benchmarks`, `commercial_detector_performance`,
`detector_latency_tradeoff`, `encoder_backbone`

**Hypothesis state — STRENGTHENED**:

The Lane 1 hypothesis (a frozen-encoder-backbone classical detector
should establish a non-trivial floor against direct injections) is
strengthened by the dossier in two ways:

- The 13-entry `detector_benchmarks` claim family in
  detector-landscape provides a broader baseline-detector comparator
  set than M0 plan §5 anticipated. The classical floor can be
  reported alongside `protectai2024deberta` + `protectai2024debertav2`
  + `meta2025promptguard2-86m` + `meta2025promptguard2-22m` +
  `microsoft2025promptshields` + `li2025piguard` + 7 others.
- The 5-paper methodology critique convergence (Zone 1.1) provides
  the framing for why the classical floor matters: it's not a "weak
  baseline"; it's the operating-point baseline that adaptive attacks
  in the OOD-wall regime degrade most acutely.

**Methodology choices unlocked**:

- `agentic_ayub2024embedding` (cross-classified to
  agentic-security-architecture `score_fusion_stacker`) opens a
  parallel embedding-classifier baseline track that Lane 1 can
  include as a sub-baseline alongside the encoder-backbone primary.
- `bhagwatkar2025firewalls` provides character-level adversarial
  test cases Lane 1 can use as a sanity-check OOD shift before
  reporting headline metrics.

**Methodology choices constrained**:

- Per ADR-038 + the composition_audit family, Lane 1 MUST report
  whether its training pool overlaps with the held-out evals. The
  composition_audit primitive `shi2023minkprob` is a drop-in audit
  step.

**Risks newly visible**:

- The `jung2026postmortem` 98%-accurate-still-broken framing means
  Lane 1's headline AUPRC numbers may surface saturated. Mitigation:
  report TPR@LowFPR per ADR-036 + report OOD-shift slice per ADR-038
  as the actual claim, not raw AUPRC.

**General protocol-adjustment recommendations**:

- Add a sub-section in `experiments/lane-1/protocol.md` that explicitly
  documents the 13-entry detector_benchmarks comparator set with
  citations.
- Ensure the encoder-backbone choice (`deberta-v3-base` per ADR-043)
  is explicitly motivated against `agentic_ayub2024embedding` +
  alternatives.

**Cross-lane dependencies**:

- Lane 1's output (per-row predictions parquet per `predictions_persisted`
  contract) feeds Lane 4's score-fusion stacker. The
  `score_fusion_stacker` claim family (5 entries in
  agentic-security-architecture) constrains how Lane 1's score outputs
  must be formatted (e.g., calibrated logits, not raw probabilities,
  per `agentic_meta2025promptguard2_86m` PG2 PR card convention).

> **Reflective margin** — *user-primary*
>
> What I keep coming back to: Lane 1 is no longer the "lay the floor"
> work I imagined at M0 plan time. The dossier shows the floor is
> already laid by `meta2025promptguard2-86m` and friends; what's
> missing in the literature is the **operating-point-aware
> floor-laying that surfaces saturation** — that's the contribution
> Lane 1 actually makes. Reframe the lane's headline from "we trained
> a detector" to "we measured a detector's operating-point honesty."

---

### Lane 1b (M1) — Adversarial robustness matrix (12-technique character_injection sweep)

**Linked ADRs**: 036 + 045
**Dossier claim_families**: `adversarial_robustness_matrix`,
`detector_architectures`

**Hypothesis state — STRENGTHENED then PARTIALLY UNDERMINED**:

The Lane 1b hypothesis (a 12-technique character_injection sweep
will reveal robustness gaps in encoder-backbone detectors) is
STRENGTHENED by `bhagwatkar2025firewalls` +
`hackett2025bypassing`'s 100% character-injection ASR finding. But
the hypothesis is PARTIALLY UNDERMINED by the **same** finding: if
character-injection achieves 100% ASR against multiple backbones,
the lane's contribution shifts from "novel finding" to "methodology
demonstration." This is the rescope candidate flagged in Round 24.

**Methodology choices unlocked**:

- The `ALL_TECHNIQUES` 12-tuple in `eval_toolkit.adversarial`
  (per ADR-045) maps to the 12-technique character_injection sweep
  the dossier carriers describe. The lane can run a fast-iter
  proof-of-concept against `meta2025promptguard2-86m` to confirm
  Hackett's finding before committing to a full matrix.

**Methodology choices constrained**:

- The lane MUST report APR (per ADR-037) alongside ASR — the
  utility-aware metric distinguishes "detector is broken under
  character injection" from "all character-injected texts are flagged
  as benign garbage by the detector." These are different failure
  modes with different operational implications.

**Risks newly visible**:

- The `hackett2025bypassing` 100% ASR result, if reproduced, is the
  paper's finding being replicated. The lane's value-add then becomes
  "methodology + scope expansion" rather than "novel result." Decision
  criterion below.

**General protocol-adjustment recommendations**:

- Add a fast-iter ASR confirmation step at the start of Lane 1b:
  apply 3 of the 12 techniques (e.g., zero-width-space, combining-
  marks, mathematical-alphanumerics) against the detector set; if
  Hackett's 100% ASR reproduces, decision criterion below kicks in.
- The 12-technique matrix output should include APR per ADR-037 and
  TPR@LowFPR per ADR-036 (cross-metric consistency).

**Cross-lane dependencies**:

- Lane 1b's output may demote the priority of Lane 4's score-fusion
  stacker IF Hackett's result holds: stacking weak detectors that
  each have 100% ASR against simple character perturbations doesn't
  help. Decision criterion below.

**Roadmap-change proposal**:

- **Rescope Lane 1b IF M1 confirms Hackett 2025 100% character-
  injection ASR ±5pp on the primary detector set.** At that point,
  the lane's contribution shifts from "novel finding" to "methodology
  demonstration." Concrete rescope:
  - Cut from "full 12-technique matrix on 5 detector backbones" to
    "3 representative techniques on 5 detector backbones + per-
    technique severity ranking."
  - Reallocate freed budget (~$X) to Lane 4's adaptive-eval path
    (per Zone 1.4 saturated benchmark finding).
  - Document rescope in `experiments/lane-1b/decisions.md` with
    cross-ref to this synthesis doc + Hackett carrier.

> **Reflective margin** — *user-primary*
>
> Open question: if Hackett's 100% ASR is correct, does Lane 1b have
> a contribution at all? Possibly: the per-technique severity ranking
> + APR-aware reporting + open-source replication artifacts (the
> sweep code) are still useful even if the finding itself is not
> novel. But the framing changes from "we discovered" to "we
> verified + extended." That's a significant book chapter change.

---

### Lane 2 (M2-M4) — Indirect-injection LoRA retrain (2-variant loss ablation)

**Linked ADRs**: 038 + 041 + 043
**Dossier claim_families**: `training_data_sources`,
`training_methodologies`, `ood_evaluation_methodology`,
`composition_audit`, `reproducibility_practice`

**Hypothesis state — STRENGTHENED**:

The Lane 2 hypothesis (a LoRA retrain on indirect-injection
synthetic data, using a 2-variant loss ablation per ADR-043, will
produce a detector that outperforms direct-injection-only baselines
on indirect benchmarks) is STRENGTHENED by:

- `agentic_meta2025promptguard2_86m` cross-classified evidence
  showing PG2's training mix includes both direct + indirect.
- `liu2020energyood` (training_methodologies) provides the energy-
  based-loss precedent the 2-variant ablation cites.
- `protectai2024_validation_dataset` (auth-required HF dataset; per
  ADR-050 + Phase B notes) is a candidate sanity-check eval set if
  HF auth is resolved post-v0.1.0.

**Methodology choices unlocked**:

- The 9-paper composition_audit family (Zone 1.5) provides drop-in
  audit primitives. Lane 2's MR-3 synthetic-corpus + ADR-038 audit
  step can use `shi2023minkprob` (Min-K%-Prob) + `zawalski2025codec`
  (CoDeC) as confirmatory audit primitives.
- `fomin2026benchmarkslie` (`ood_evaluation_methodology`) provides
  the true-distribution-shift eval frame Lane 2 should target.

**Methodology choices constrained**:

- Per ADR-041 + WildGuardMix-style full-specificity disclosure norm,
  Lane 2's synthetic-corpus generation MUST use only documented
  attack techniques (Greshake + OWASP LLM01:2025 + dossier
  `production_rag_incidents` carriers — EchoLeak/Slack/Comet/etc.) —
  no novel attack vectors.

**Risks newly visible**:

- MR-3 is STILL OPEN (per `decisions/upstream_issues.md`). Lane 2's
  M2-M4 work depends on the `/dataset-synthesize` skill landing in
  `brandon-behring/research_toolkit`. If MR-3 doesn't ship by M2
  start, Lane 2 may need a temporary in-portfolio dataset-synthesis
  helper, BUT this conflicts with the no-local-workarounds rule
  (ADR-026). Decision criterion below.

**General protocol-adjustment recommendations**:

- Add an MR-3-blocking-status check at M2 entry: if MR-3 still open,
  trigger a brief escalation conversation with the user about
  whether to (a) wait, (b) propose a portfolio-local synthesis
  helper as a clearly-marked exception to ADR-026, or (c) pivot
  Lane 2's data source to an existing dataset (`harelix2024_mixed`
  if HF auth resolved by then, or `lakeraai2025pintbenchmark`).

**Cross-lane dependencies**:

- Lane 2's output (the retrained encoder weights + per-row predictions)
  feeds Lane 4's stacker. The `score_fusion_stacker` claim family
  expectation is that Lane 2's outputs are formatted consistently
  with Lane 1's outputs.
- Lane 2's composition_audit work informs Lane 3's spotlighting
  variant choices (does spotlighting help OOD or only IID?).

**Roadmap-change proposal**:

- **Lane 2 budget reservation for composition_audit work at M2 close
  IF Tier C PromptShield Llama-3.1-8B unlocks at M2+.** At that
  point, the portfolio MAY run `shi2023minkprob` +
  `zawalski2025codec` as a confirmatory audit step before reporting
  comparative results against PromptShield's evals (per ADR-038
  Phase C cross-references).

> **Reflective margin** — *user-primary*
>
> Why I'm worried about MR-3: it's the only remaining open MR from the
> M0 batch, and it's M3-blocking. The dossier work has surfaced rich
> production_rag_incidents data we could now use directly as
> synthesis seeds — but we still need the skill to do the
> prompt-caching template work. Possible mitigation I'm chewing on:
> file a follow-up MR with a more specific scope (e.g., "support 5
> seed-document patterns extracted from the dossier") rather than
> waiting on the more general skill.

---

### Lane 3 (M5) — Spotlighting structural defense (3 variants)

**Linked ADRs**: 045
**Dossier claim_families**: `spotlighting_variants`,
`rag_evaluation_harness`, `architectural_defense_methods`

**Hypothesis state — STRENGTHENED**:

The Lane 3 hypothesis (3 spotlighting variants — delimit + datamark +
encode — applied at the input layer will provide an architectural
defense complementary to the encoder-backbone detector) is
STRENGTHENED by:

- `rag_hines2024spotlighting` (rag-injection-defenses
  `spotlighting_variants`) — the foundational paper. Body-quote
  anchored.
- `microsoft2025spotlightingfoundry` — Microsoft's commercial
  spotlighting product launch (Azure AI Foundry); validates the
  architectural-defense framing at the vendor level.
- `rag_microsoft_azure_doc_shield` — Prompt Shields in Azure AI
  Content Safety (User Prompt + Document Shield).
- `shone2025promptshields` — enhanced AI security with Azure Prompt
  Shields integration narrative.

**Methodology choices unlocked**:

- The 4-entry `spotlighting_variants` family + the 3-entry
  `architectural_defense_methods` family (`hines2024spotlighting`,
  `debenedetti2025camel`, `beurerkellner2025designpatterns`) provide
  a broader design-space comparison set than the M0 plan §5 lane
  description anticipated.
- The 3-dataclass preprocessing module in eval-toolkit (per ADR-045
  Q1 v0.47.0 pin) maps directly to the 3 variants (delimit + datamark
  + encode).

**Methodology choices constrained**:

- `agentic_debenedetti2025camel` (cross-classified to
  agentic-security-architecture `agent_capability_isolation`)
  introduces a capability-isolation pattern that overlaps with
  spotlighting's framing. Lane 3 should explicitly distinguish
  spotlighting (input-layer marker) from CaMeL (capability-isolation
  layer) in the lane's hypothesis statement.

**Risks newly visible**:

- The cross-classification of `rag_hines2024spotlighting` to
  rag-injection-defenses indicates the spotlighting frame is
  predominantly evaluated in the RAG-injection setting, not the
  direct-injection setting. If Lane 3 evaluates on a direct-injection
  corpus only, the external validity of the result is
  weaker than the dossier suggests.

**General protocol-adjustment recommendations**:

- Lane 3's eval set should include both direct + indirect splits
  (per the existing `agentdojo` carrier from
  `debenedetti2024agentdojo`).
- The 3-variant ablation should include a baseline (no spotlighting)
  + a hypothesis-rejection control (random-token marker) to
  separate "spotlighting works" from "any input-layer perturbation
  works."

**Cross-lane dependencies**:

- Lane 3's output (the spotlight-defended detector scores) feeds
  Lane 4's stacker as an additional input stream.
- Lane 3's spotlighting helpers (the `eval_toolkit.preprocessing`
  3-dataclass module) are reused in Lane 4's pre-processing pipeline.

> **Reflective margin** — *user-primary*
>
> What I keep coming back to: Lane 3 felt under-motivated at M0 plan
> time. The dossier strengthens it considerably — particularly the
> Microsoft commercial spotlighting product (Azure AI Foundry) +
> Hines' paper as the foundational evidence. The lane's value-add is
> now clearer: open replication + 3-variant ablation on an open
> backbone, which Microsoft's commercial product doesn't make
> visible.

---

### Lane 4 (M6) — Score-fusion stacker (LogisticStacker + XGBoost) + APR metric

**Linked ADRs**: 036 + 037 + 045
**Dossier claim_families**: `score_fusion_stacker`,
`agentic_benchmarks`, `agentic_bench_critique`,
`agent_harness_architecture`

**Hypothesis state — STRENGTHENED + REFRAMED**:

The Lane 4 hypothesis (a score-fusion stacker over Lane 1 + Lane 2 +
Lane 3 + Lane 5 + reference scorer outputs will produce a
detector ensemble that outperforms any single backbone) is
STRENGTHENED by the 5-entry `score_fusion_stacker` claim family. But
the hypothesis is REFRAMED by the dossier's `agentic_bench_critique`
work:

- `agentic_bhagwatkar2025firewalls` + `agentic_debenedetti2024agentdojo`
  + `agentic_abdelnabi2025llmailinject` together argue that **fixed
  agentic benchmarks are saturating** — the stacker should be
  evaluated on adaptive evals (`abdelnabi2025llmailinject`'s
  LLMail-Inject competition) as the primary headline, with fixed
  benchmarks as legacy comparators.

**Methodology choices unlocked**:

- The `agentic_meta2025promptguard2_86m` + `agentic_meta2025promptguard2_22m`
  cross-classified evidence shows PG2's output-format conventions
  that the stacker should consume (calibrated logits).
- `agentic_liu2020energyloss` provides energy-based scoring as one
  of the stacker's complementary signals.
- `agentic_ayub2024embedding` provides embedding-classifier scoring
  as another complementary signal (per Lane 1 unlocked methodology).
- `agent_harness_architecture` carriers (e.g.,
  `agentic_beurerkellner2025designpatterns`) inform the harness
  architecture the stacker plugs into.

**Methodology choices constrained**:

- Per ADR-037 + Lane 4's APR metric, the stacker's outputs must be
  APR-aware: a stacker that flags everything to maximize TPR fails
  the APR metric. The dossier's `evaluation_metrics` family
  (8 entries) reinforces this.

**Risks newly visible**:

- Per `jung2026postmortem`'s 98%-accurate-still-broken framing, a
  stacker reporting 95% AUPRC on `lakeraai2025pintbenchmark` may be
  trivially saturated. Lane 4 MUST report against LLMail-Inject as
  primary + PINT/PromptShield/WildGuardMix as legacy.

**General protocol-adjustment recommendations**:

- Lane 4's reporting deliverables should include:
  - LLMail-Inject competition results (adaptive eval primary)
  - PINT + PromptShield + WildGuardMix results (legacy)
  - APR metric per ADR-037
  - TPR@LowFPR per ADR-036
  - Per-input-stream attribution (which stack component contributed
    most to which detection)

**Cross-lane dependencies**:

- Lane 4's input streams: Lane 1 + Lane 2 + Lane 3 + Lane 5 + reference
  scorers (`protectai2024deberta`, `meta2025promptguard2-86m`, `meta2025promptguard2-22m`).
- Lane 4's stacker output is the portfolio's headline detector for
  M6+ deliverables.

**Roadmap-change proposal**:

- **Lane 4 evaluation pivot to LLMail-Inject as primary at M5 close
  IF M5 results suggest fixed-benchmark saturation across Lane 1 + 2
  + 3.** Decision criterion: if any 2 of (PINT, PromptShield,
  WildGuardMix) saturate above 95% AUPRC on the stacker at M5
  close, declare them legacy comparators and pivot Lane 4's headline
  to LLMail-Inject.

> **Reflective margin** — *user-primary*
>
> This is the lane I'm most worried about over-engineering. The 5-
> input-stream stacker + 4-benchmark comparison + 4-metric reporting
> is a lot to keep tractable. Possible simplification I keep
> chewing on: pick 3 input streams + 2 benchmarks + 2 metrics at
> M5-end-of-lane assessment, defer the rest to M6+ if the simpler
> design is informative enough.

---

### Lane 5 (M4) — TaskTracker activation probe port on encoder backbone

**Linked ADRs**: (none currently)
**Dossier claim_families**: `activation_probe_methodology`,
`dual_llm_pattern`, `agent_capability_isolation`

**Hypothesis state — STRENGTHENED + SURFACE-THIRD-PATH**:

The Lane 5 hypothesis (port TaskTracker's activation-delta probe
methodology from decoder LLMs to encoder backbones) is STRENGTHENED
by the dossier in two ways + a third unexpected path:

- **Strengthened by**: `agentic_abdelnabi2025tasktracker` provides
  the upstream methodology + the activation-probe primitive that
  ADR 0002's `Probe` Protocol formalizes.
- **Strengthened by**: `activation_probe_methodology` claim family in
  agentic-security-architecture provides multi-paper context for the
  port.
- **SURFACE-THIRD-PATH**: `agentic_debenedetti2025camel` +
  `agent_capability_isolation` cross-classification surfaces an
  alternative framing — that activation probes can be **paired with
  capability-isolation** patterns rather than competing with them.
  This is a hypothesis-richening direction Lane 5 wasn't originally
  scoped to explore.

**Methodology choices unlocked**:

- The `eval_toolkit.probes.ActivationDeltaProbe` (per MR-7 shipped
  v0.43.0) maps to the TaskTracker port. The lane can use the
  upstream primitive directly.
- The `Probe` Protocol from eval-toolkit v0.47 (per ADR-045)
  formalizes the probe contract.

**Methodology choices constrained**:

- The encoder-backbone choice (probably `deberta-v3-base` per
  ADR-043) constrains the activation-delta extraction shape. If the
  port doesn't yield positive results on encoder, the lane's null
  finding is itself a contribution.

**Risks newly visible**:

- The TaskTracker methodology is decoder-LLM-native. Porting to an
  encoder backbone may have null result; the lane should plan for
  null-finding write-up.
- The `dual_llm_pattern` family includes `agentic_debenedetti2025camel`
  which raises the bar: the dual-LLM frame has design alternatives
  Lane 5 should consider before committing to a port-only design.

**General protocol-adjustment recommendations**:

- Lane 5 should declare a hypothesis-rejection control at M3 entry:
  if the encoder-backbone activation-delta probe doesn't show
  separable distributions on direct + indirect injections at M3
  smoke-test, the lane writes up the null finding + pivots to a
  capability-isolation-paired hypothesis (per surface-third-path).

**Cross-lane dependencies**:

- Lane 5's output (probe weights + per-row predictions) feeds Lane 4's
  stacker as a 5th input stream.

**Roadmap-change proposal**:

- **Promote Lane 5's surface-third-path (capability-isolation pairing)
  to a sub-hypothesis at M3 entry IF M3 smoke-test indicates null
  result on the port-only design.** Decision criterion: at M3
  smoke-test, if the encoder probe doesn't separate direct +
  indirect distributions with d-prime > 0.5, declare the port-only
  hypothesis falsified + pivot to surface-third-path hypothesis as
  the lane's primary contribution.

> **Reflective margin** — *user-primary*
>
> The surface-third-path direction is the most interesting Lane 5
> implication I see. CaMeL + capability-isolation is a different
> design ontology than detector-as-input-classifier — and the
> dossier's cross-classification suggests they may be
> complementary rather than competing.

---

## Zone 2.5 — Cross-cutting action list

Items applicable to multiple lanes:

1. **TPR@LowFPR reporting per ADR-036 across Lanes 1 + 1b + 4** —
   all 3 lanes report at FPR {1%, 0.5%, 0.1%, 0.05%}. Per ADR-036
   Phase C cross-references (jacob2025promptshield Table 4 +
   li2024injecguard + meta2025promptguard2-86m).
2. **Composition_audit step per ADR-038 at M2 close** — Lane 2's
   MR-3 synthetic-corpus + ADR-038 audit step uses
   `shi2023minkprob` + `zawalski2025codec` as confirmatory audit
   primitives.
3. **APR metric per ADR-037 in Lanes 1b + 4** — utility-aware
   metric complements TPR@LowFPR.
4. **ETHICS.md §1 full-specificity citation enabled by ADR-041 +
   the production_rag_incidents 7-entry family** — Lanes 2 + 3 may
   cite EchoLeak/Slack/Comet/Gemini/ChatGPT/screenshot incidents in
   protocol.md sections without re-justifying the disclosure norm.
5. **LLMail-Inject adaptive eval primary at M5 close pivot** — Lanes
   1 + 4 reporting prepared for the pivot per `abdelnabi2025llmailinject`
   carrier; gated on saturation criterion per Zone 1.4 + Lane 4
   roadmap proposal.

---

## Zone 3 — Reflective margins (consolidated)

These are user-primary observations the lane sections embed inline.
Restated here as a quick reference:

- **Lane 1 reframe**: from "we trained a detector" to "we measured a
  detector's operating-point honesty." The floor work is already
  done in the field; the operating-point-aware floor-laying is the
  contribution.
- **Lane 1b open question**: if `hackett2025bypassing`'s 100% ASR
  holds, does Lane 1b have a novel contribution? Probably: per-
  technique severity ranking + APR-aware reporting + open-source
  replication artifacts.
- **Lane 2 MR-3 worry**: it's the only remaining open MR from M0
  batch, and it's M3-blocking. Possible mitigation: file a follow-
  up MR with narrower scope (5 seed-document patterns from dossier
  production_rag_incidents).
- **Lane 3 stronger than I thought**: the spotlighting frame is well-
  established (Microsoft + Hines + 3 vendor evidences). The lane's
  value-add is open replication + 3-variant ablation on open
  backbone.
- **Lane 4 over-engineering risk**: 5 input streams + 4 benchmarks +
  4 metrics is a lot. Simplify at M5-end-of-lane assessment if
  necessary.
- **Lane 5 surface-third-path**: CaMeL + capability-isolation
  pairing is the most interesting direction. Different design
  ontology than detector-as-classifier.

---

## What additional information would help

### Immediate (post-v0.1.0, Sprint 4 candidates, ~1 week)

1. **Post-M1 dossier refresh**: at M1 close (Lane 1 + 1b deliver), re-
   run `/research-gather` against the 5 topics with a 7-day freshness
   window. Specifically:
   - Watch for new entries in `detector_benchmarks` claim family
     (post-2026-05 publications).
   - Watch for new entries in `composition_audit` claim family (the
     methodology is mature; new tools may surface).
   - Watch for new EchoLeak/Slack-style production incidents that
     extend the `production_rag_incidents` family.
2. **MR-3 monitoring** (per Round 24 Phase E sub-task): set a watch
   on `brandon-behring/research_toolkit#1` for `/dataset-synthesize`
   skill landing. If shipped by M2 entry, Lane 2 unblocks; if not,
   trigger MR-3-blocking-status conversation per Lane 2 risk above.
3. **submission v1.4+ CI ref repin**: the submission's CI workflow
   currently pins to a specific commit; if v1.4 ships before M2, the
   portfolio's repin step (per ADR-046) needs re-evaluation against
   any new submission ADRs.
4. **Cross-vol synthesis layer**: if the portfolio + submission ship
   together at v1.0 (post-M7), a cross-vol synthesis chapter
   comparing dossier findings across both volumes' chapter sets
   may be valuable. Deferred candidate — depends on the 3-guide
   architecture decision at M5 (per ADR-044).

### Medium-term (lane-execution feedback loops, ~M2-M5)

5. **Per-milestone dossier refresh cadence**: at each milestone
   close, allocate ~2 days for a topical refresh of the lane-relevant
   dossier topic. Cadence:
   - M1 close → refresh detector-landscape + direct-vs-indirect
   - M2 close → refresh training-and-evaluation
   - M3 close → refresh agentic-security-architecture
   - M4 close → refresh rag-injection-defenses
   - M5 close → refresh spotlighting_variants subset of
     rag-injection-defenses
   - M6 close → refresh agentic_benchmarks + adaptive-eval
6. **Lane-specific dossier follow-up questions** (post-M0):
   - Lane 1: "What's the operating-point convention in newer
     detector cards (post-2026-05)?" — informs ADR-036 follow-up.
   - Lane 2: "What's the composition_audit field state at M2 entry?"
     — informs ADR-038 follow-up.
   - Lane 4: "Has the LLMail-Inject leaderboard's adaptive-eval
     methodology been replicated/critiqued?" — informs Lane 4
     headline pivot decision.
7. **MR-13 follow-up** (book-scaffold-astro#54): once upstream
   ships, validate that the canonical create-book template no
   longer trips the `@TYPE` lexer. Bump pin if necessary.

### Long-term (open research gaps, post-M7)

8. **Retrieval provenance**: the dossier surfaces `retrieval_provenance`
   claim family (in rag-injection-defenses) with NASCENT literature —
   ~3 entries total, mostly position papers. If the portfolio's M6+
   Lane 4 work has bandwidth, a small lane-bonus contribution on
   retrieval-provenance methodology could be 2026-2027's "OOD-wall
   thesis" successor.
9. **Content authentication**: `content_authentication_rag`
   (rag-injection-defenses) claim family is similarly nascent. Open
   territory.
10. **Multimodal injection**: the dossier has roughly 2-3 entries
    touching multimodal injection (`sahib2025unseeable` screenshot
    injections; `tenable2025geminitrifecta` Gemini trifecta).
    Multimodal is a clear Sprint 4+ direction. Lane 6 candidate at
    M6+ if budget allows.

### Information sources to monitor (long-running)

11. **Embrace The Red blog** (Rehberger 2023 + 2025): high-quality
    indirect-injection disclosures continue to appear.
12. **Cisco Outshift blog**: post-Robust-Intelligence-acquisition,
    Cisco's product announcements may surface relevant landscape
    shifts (per ADR-050 vendor cluster posture).
13. **F5 AI Guardrails docs**: post-CalypsoAI-acquisition F5 product
    docs (vendor cluster posture cross-link).
14. **arXiv cs.CR + cs.CL** new submissions tagged with `prompt
    injection` keyword — bi-weekly review cadence.
15. **HuggingFace Hub** new datasets in the `prompt-injection` +
    `jailbreak` + `adversarial-prompts` tags — bi-weekly review
    cadence.

---

## Citation discipline (cache-stays-local)

Per Round 24 lock + ADR-049 body-quote anchoring discipline + ADR-050
vendor cluster posture:

- **Bibkey citations** resolve to `book/bibliography.bib` (157
  entries; the 5-topic dossier bib_ledgers concatenated + dedupe'd
  per ADR-048 cross-classification policy).
- **ADR citations** resolve to `decisions/ADR-NNN-*.md` (50 total
  entries post-Round 24).
- **URL citations** resolve to public URLs documented in
  `docs/research/<topic>/cache_manifest.yml` entries (sha256-keyed
  cache blobs; the cache stays local per public-repo licensing
  posture).
- **NO local-only file path references** in this document. Cached
  PDFs + body_text + body_meta directories are gitignored per
  `.gitignore` line 47 + 53. Readers can re-fetch via cache_manifest's
  source_url.

**Validator-equivalent check**: a grep for `cache/` in this document
should return zero hits in zones 1+2; zone 3 reflective margins may
reference cache artifacts conceptually but mark them as local-only.

---

## Cross-references

- ADR-007 (claim_family naming convention)
- ADR-010 (anti-pattern firewall — no URL guessing)
- ADR-011 (immutability discipline)
- ADR-026 (no-local-workarounds policy — applies to Lane 2 MR-3
  risk discussion)
- ADR-036 + ADR-037 + ADR-038 + ADR-041 + ADR-045 (inline Round 24
  Sprint 2 dossier cross-references per Phase C)
- ADR-048 + ADR-049 + ADR-050 (Round 24 Sprint 3 fold-in policy
  ADRs per Phase D)
- `experiments/MANIFEST.json` (6-lane experiment authority graph
  with `dossier_claim_family` cross-references per Sprint 2 E6)
- `docs/planning/PORTFOLIO_PLAN.md` §5 + §17 + §21 (full lane
  descriptions + roadmap + workstream surface)
- `docs/planning/portfolio-lane-execution-playbooks.md` (per-lane
  execution details)
- `docs/planning/portfolio-chapter-outlines.md` (book chapter outlines)
- 5 dossier topic READMEs in
  `docs/research/<topic>/agent_index/README.md`
- `decisions/upstream_issues.md` MR-3 (research_toolkit#1) + MR-13
  (book-scaffold-astro#54)
- `book/bibliography.bib` (157 entries; the cited bibkeys resolve
  there)
