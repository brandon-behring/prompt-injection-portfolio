---
adr_id: "045"
slug: eval-toolkit-v047-pin-and-api-pivot
title: "eval-toolkit v0.47 pin + canonical-surface API pivot"
date: 2026-05-21
status: Accepted
linked_round: "R20"
plan_section: "Context + §3 + §21"
---

# ADR-045: eval-toolkit v0.47 pin + API pivot

## Status

Accepted (Round 20 lock; commit `bc30c52` Day 3a/c1).

## Context

Per user directive on 2026-05-21: "make sure we are using the most recent
version of eval toolkit and we look on my computer for it's roadmap so we
have it in mind." Reading eval-toolkit's roadmap at
`~/.claude/plans/evaluate-all-the-work-twinkly-kite.md` revealed
eval-toolkit shipped 4 additional releases (v0.45.0 → v0.46.0 → v0.46.1
→ v0.47.0) closing portfolio's MR-6 + obsoleting planned MR-10 via
upstream parallel-Codex implementation.

Critical BREAKING changes in v0.47.0:
- Top-level scalar metric names REMOVED (`pr_auc`, `roc_auc`, `brier_score`,
  `expected_calibration_*`). Use `scorecard()` + `metric_specs.*`.
- Module-level `adversarial.sweep` + `preprocessing.sweep` REMOVED.
  Consolidated into top-level `sweep()`.
- SimpleNamespace shortcuts (`character_injection.zero_width_space`,
  `spotlighting.delimit`) REMOVED. Use 12 dataclasses + `TextTransform`
  Protocol.

## Decision

**Q1 (pin floor)**: advance pyproject.toml `eval-toolkit>=0.44` →
`eval-toolkit[probes,losses]>=0.47`. Range-floor auto-bumps to v0.48+ as
upstream releases ship.

**Q2 (roadmap awareness)**: document v0.48 + v1.0 in Round 20 narrative;
portfolio code acts on SHIPPED APIs only. No code references
v0.48-unreleased APIs.

**API contract pivot** (load-bearing for all Lane work): portfolio code
uses v0.47 canonical surfaces exclusively —
- `scorecard()` + `metric_specs.*` for evaluation
- Top-level `sweep(strategies, texts, scorer, attack_threshold)` for transforms
- `TextTransform` + `Probe` + `MetricSpec` + `MetaLearner` Protocols (canonical
  top-level access per ADR 0002)
- 12 dataclass strategies in `eval_toolkit.adversarial` (`ALL_TECHNIQUES`)
- 3 dataclass strategies in `eval_toolkit.preprocessing` (DelimitVariant etc.)

**REMOVED from portfolio plan references**: SimpleNamespace patterns;
per-module Protocols (`CharacterInjectionStrategy`); module-level sweeps;
top-level scalar metric imports.

## Consequences

- MR-6 (eval-toolkit#52) state → `released-v0.45.0`; auto-pinned.
- MR-10 OBSOLETED — advanced-6 shipped in v0.47.0 sweep unification.
- Day 4 MR-10 filing step CANCELED; Lane 1b matrix uses full 12 from M1 start.
- API smoke-tests overhauled per Day 3a step 4 (top-level canonical imports).
- Forward-look: v0.48 ships strategy_id disambiguation + scorer-output
  shape validation; v1.0 ships stability commitment. Portfolio re-runs
  Day-3a-style consume + smoke-test per minor.
- Day 3a smoke-test surfaced MR-12 (eval-toolkit#69) — Tier-2 Protocol
  consolidation discoverability improvement; NOT blocking.

## Sprint 2 dossier evidence (added M0 close, Round 24)

The Sprint 2 literature dossier validates that v0.47's canonical
surfaces directly map to recurring detection-methodology patterns
across the dossier, supporting the API-pivot decision:

**`ALL_TECHNIQUES` 12-tuple (Lane 1b adversarial sweep):**

The 12-dataclass strategies in `eval_toolkit.adversarial.ALL_TECHNIQUES`
correspond to character-injection + delimiter-perturbation +
prompt-rewrite techniques benchmarked in:

- **`bhagwatkar2025firewalls`** (detector_benchmarks claim family) —
  firewall/guardrail bypass via character-level perturbations.
  Lane 1b uses ALL_TECHNIQUES to reproduce + extend.
- **`hackett2025bypassing`** (detector_benchmarks claim family) — 100%
  character-injection ASR against multiple detector backbones.
  Operationalized via `eval_toolkit.adversarial.zero_width_space` +
  `combining_marks` + `mathematical_alphanumerics` dataclasses.
- **`zizzo2025adversarialprompt`** + **`nasr2025attackermovessecond`**
  — adaptive-attack systematic benchmarking. The sweep API enables the
  combinatorial coverage these papers call for.

**LogisticStacker / score_fusion_stacker (Lane 4):**

The dossier's `agentic-security-architecture/` topic surfaces a
5-entry **`score_fusion_stacker`** claim family that operationalizes
the Lane 4 stacker approach:

- **`agentic_meta2025promptguard2_86m`** + **`agentic_meta2025promptguard2_22m`**
  — base detector scores fed into the stacker.
- **`agentic_liu2020energyloss`** — energy-based OOD scoring; one of
  the stacker's complementary signals.
- **`agentic_ayub2024embedding`** — embedding-classifier detection;
  fusion-compatible per the topic README.
- **`agentic_li2024injecguard`** — InjecGuard cross-classified into
  agentic topic; surfaces over-defense as a fusion-design constraint.

These map cleanly onto v0.47's `MetaLearner` Protocol + `Probe`
Protocol contracts.

Claim families anchored: `detector_benchmarks` (3 referenced) +
`score_fusion_stacker` (5 entries). See
`docs/research/agentic-security-architecture/bib_ledger.yml` +
`docs/research/detector-landscape/bib_ledger.yml`.

## Cross-references

- eval-toolkit roadmap: `~/.claude/plans/evaluate-all-the-work-twinkly-kite.md`
- ADR-042 (Round 14; supersedes Round 14 Q2 v0.44 pin)
- ADR 0002 (eval-toolkit; top-level canonical surface)
- Round 20 Q1-Q2 lock + Day 3a smoke-test results
- Plan §3 dependency policy
- `decisions/library_imports.md` (14 v0.47 primitives registered)
- ADR-048 (Round 24, cross-classification policy — explains the
  `agentic_li2024injecguard` topic-prefixed bibkey form)
- `docs/research/agentic-security-architecture/bib_ledger.yml`
  (claim_family: `score_fusion_stacker`)
