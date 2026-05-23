# Library imports registry

Per ADR-026 + Round-10 library-first invariant, every reusable primitive
consumed by `prompt-injection-portfolio` from one of the 4 load-bearing
libraries is logged here. This registry is the audit surface for the
no-hand-rolled-equivalents rule + the `library_imports_registered` test
contract (Tier-4, plan §2).

**Round 20 + Round 21 update (2026-05-21, commit `bc30c52`)**: pin floors
advanced (eval-toolkit `>=0.42` → `[probes,losses]>=0.47`; book-scaffold-astro
`^3.1.0` → `^3.5.0`); 5/7 portfolio eval-toolkit MRs + both scaffold MRs
shipped by upstream parallel agents over 2-day window. v0.47 API canonical
surface verified via Day 3a step 4 Python REPL smoke-test
(top-level imports per ADR 0002).

---

## eval-toolkit (PyPI; floor `[probes,losses]>=0.47`)

Per [ADR 0002](https://github.com/brandon-behring/eval-toolkit/blob/main/docs/source/adr/0002-scorecard-as-primary-metric-surface.md):
**top-level `from eval_toolkit import <Name>` is the canonical contract**;
submodule paths are implementation. Portfolio code uses top-level imports.

| Symbol (top-level) | Origin module | Min version | Used in | First commit | MR | Notes |
|--------------------|---------------|-------------|---------|--------------|----|-------|
| `scorecard` | `eval_toolkit._scorecard` | >=0.46 | `<pending lane work>` | bc30c52 (Day 3a smoke-test) | — | v1.0 canonical eval entry; `Mapping[str, MetricResult]` |
| `metric_specs` | `eval_toolkit.metric_specs` | >=0.46 | `<pending lane work>` | bc30c52 | — | `metric_specs.pr_auc` + `metric_specs.ece(n_bins=15)` etc. |
| `sweep` | `eval_toolkit._sweep` | >=0.47 | `<pending Lane 1b matrix>` | bc30c52 | MR-2+10 obsoleted | Top-level unified sweep; replaces v0.46 module-level sweeps |
| `TextTransform` | `eval_toolkit.protocols` | >=0.47 | `<pending Lane 1b + 3>` | bc30c52 | MR-12 (#69) | 9th Tier-2 Protocol; canonical strategy-shape |
| `Probe` | `eval_toolkit.probes` | >=0.43 | `<pending Lane 5>` | bc30c52 | MR-12 (#69) | TaskTracker probe Protocol; canonical surface top-level |
| `MetricSpec` | `eval_toolkit._scorecard` | >=0.46 | `<pending Lane 1 + 4>` | bc30c52 | MR-12 (#69) | Tier-2 Protocol; `name + compute(y,s) -> float` |
| `MetaLearner` | `eval_toolkit.stacking` | >=0.45 | `<pending Lane 4 stacker>` | bc30c52 | MR-12 (#69); MR-6 closed v0.45.0 | Stacker Protocol; canonical |
| `loaders.ood_dataset_from_manifest` | `eval_toolkit.loaders` | >=0.43 | `<pending Lane 1 baseline>` | bc30c52 | MR-1 (#48) closed v0.43.0 | OOD slate declarative loader |
| `loaders.OodManifestLoader` | `eval_toolkit.loaders` | >=0.43 | `<pending>` | bc30c52 | MR-1 (#48) | DatasetLoader Protocol wrapper |
| `adversarial.{12 dataclasses}` | `eval_toolkit.adversarial` | >=0.47 | `<pending Lane 1b 12-tech matrix>` | bc30c52 | MR-2 + MR-10 closed v0.43.0 + v0.47.0 | `ALL_TECHNIQUES` 12-tuple: ZeroWidthSpace, Homoglyph, Diacritic, Whitespace, CaseRandomization, Punctuation (core-6) + BidiRTL, TagStripping, Synonym, TokenSplitting, UnicodeNormalization, InvisibleChars (advanced-6) |
| `preprocessing.{3 dataclasses}` | `eval_toolkit.preprocessing` | >=0.47 | `<pending Lane 3>` | bc30c52 | MR-5 (#51) closed v0.44.0 | DelimitVariant, DatamarkVariant, EncodeVariant |
| `losses.RecallAtLowFPR` | `eval_toolkit.losses` | >=0.44 | `<pending Lane 2 retrain>` | bc30c52 | MR-4 (#50) closed v0.44.0 | Meta PG2 recipe; `[losses]` extra |
| `probes.ActivationDeltaProbe` | `eval_toolkit.probes` | >=0.43 | `<pending Lane 5>` | bc30c52 | MR-7 (#53) closed v0.43.0 | TaskTracker-style; `[probes]` extra |
| `stacking.LogisticStacker` | `eval_toolkit.stacking` | >=0.45 | `<pending Lane 4>` | bc30c52 | MR-6 (#52) closed v0.45.0 | Stacker reference impl |

Additional primitives expected (NOT yet consumed; populate at lane start):
- `eval_toolkit.metrics` submodule (per ADR 0002 implementation-side access
  for scalar functions; legacy submodule pattern)
- `eval_toolkit.io` (predictions parquet writer)
- `eval_toolkit.bootstrap.BootstrapCI` (returned by scorecard CI cells)
- `eval_toolkit.calibration.{fit_platt_binary, fit_beta_binary,
  fit_isotonic_binary, fit_temperature_binary}` — canonical 4-calibrator
  family per submission ADR-055/056/058

---

## runpod-deploy (PyPI; floor `>=0.8.4`)

Local orchestrator only. **Never imported by remote pods**; consumed at
session-launch boundary.

| Symbol | Min version | Used in | First commit | MR | Notes |
|--------|-------------|---------|--------------|----|-------|
| (none yet) | | | | | |

Expected populations:
- `runpod_deploy.Session` ← session-launch for Lane 2 retrain (M4) +
  Lane 1 / Lane 1b / Lane 5 evals (M1-M2) — `lifecycle.on_success: recycle`
  per submission ADR-059.

---

## research_toolkit (git URL pinned to `v1.9.1`)

| Symbol / skill | Min version | Used in | First commit | MR | Notes |
|----------------|-------------|---------|--------------|----|-------|
| `/research-plan` | v2.2.1 | M0 + Sprint 2 dossier sprint | `413284a` (Phase 1) + `f709f15` (Sprint 2 E1) | (none) | Used to scope 3 Sprint 1 topics + 2 Sprint 2 new topics |
| `/research-gather` | v2.2.1 | M0 + Sprint 2 E2 dossier sprint | `51785d9` (Phase 2) + `5bc9cf9` (Sprint 2 E2) | (none) | --cache-pdfs for ~124 arXiv PDFs across 5 topics |
| `/agent-index` | v2.2.1 | M0 + Sprint 2 E4 dossier sprint | `8b0fdb4` (Phase 3) + `16e9169` (Sprint 2 E4) | (none) | v2.2+ Attribute-First atomic decomposition; pre_selection_manifest |
| `/dossier-audit` | v2.2.1 | M0 + Sprint 2 E5 dossier sprint | `00d45c5` (Phase 4) + `b68329c` (Sprint 2 E5) | (none) | 6 Sprint 1 rounds + 3 Sprint 2 audit-trail rounds per topic |
| `/dataset-synthesize` | v0.8+ (upstream) | Lane 2 (~M3) | (pending MR-3) | MR-3 | STILL OPEN per Round 21 — research_toolkit#1 |

Expected populations:
- `/research-plan` ← M0 dossier sprint (week 1-3)
- `/research-gather` ← M0 dossier sprint
- `/dossier-build` ← M0 dossier sprint
- `/dossier-audit` ← M0 close (Day 19) + per-milestone re-runs
- `/dataset-synthesize` ← MR-3 (Lane 2 synthetic data gen, ~M3) — STILL OPEN per Round 21

Tracked as v0.8+ upstream feature request: publish research_toolkit
to PyPI for cleaner pinning (currently consumed via git URL).

---

## @brandon_m_behring/book-scaffold-astro (npm; floor `^3.5.0` per Round 21)

Per Round 21: scaffold pin advanced from `^3.1.0` → `^3.5.0`; MR-8 + MR-9 both
closed upstream. v3.5.0 ships `research-portfolio` preset (the Round 12 design
spec). v3.6.0 adds `katexMacros` consumer-defined macros option (not currently
needed but available).

| Component / API | Min version | Used in | First commit | MR | Notes |
|-----------------|-------------|---------|--------------|----|-------|
| `defineBookSchemas()` | ^3.1.0 (backfill-pinned-via Round 21 ^3.5.0) | `book/src/content.config.ts` | f011726 (M0 Day 2 scaffold bootstrap) | — | Stock scaffold |

Expected populations (post Day 14 chapter skeletons):
- `research-portfolio` preset (union schema academic ∪ tools) — MR-8 (#6) closed v3.5.0
- `PreReleaseBanner` component (state + dismissAt + message)
- `PolicyRef` component (generic cross-doc policy citation)
- `AICollaborationDisclosure` component (YAML-config disclosure paragraph)
- Generic frontmatter collection primitive — MR-9 (#7) closed v3.3+
- 18 callouts + 8 theorem family + KaTeX + BibTeX pipeline + `<Cite>`
  + `<MarginNote>` + 7-state status — already present in scaffold; consumed
  as portfolio chapter skeletons author per Day 14 M0 sequence (NOW UNBLOCKED
  per Round 21 Q2 — was previously gated on v3.2 wait).

---

## Test-contract attestation

The `tests/contracts/test_library_imports_registered.py` contract
(part of the 7 Tier-4 contracts; implemented at M0 Day 3) parses
this file + verifies that every primitive imported in `src/` or `scripts/`
appears in a row above. Adding a new upstream import without
registering it here fails CI.
