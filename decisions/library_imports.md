# Library imports registry

Per ADR-026 + Round-10 library-first invariant, every reusable primitive
consumed by `prompt-injection-portfolio` from one of the 4 load-bearing
libraries is logged here. This registry is the audit surface for the
no-hand-rolled-equivalents rule + the `library_imports_registered` test
contract (Tier-4, plan §2).

State at v0.1.0-pre (M0 Day 2): no upstream primitives consumed yet.
Imports populate as MR-1..7 + MR-8 ship and lane work begins.

---

## eval-toolkit (PyPI; floor `>=0.42`)

| Symbol | Min version | Used in | First commit | MR | Notes |
|--------|-------------|---------|--------------|----|-------|
| (none yet) | | | | | |

Expected populations (per plan §10):
- `loaders.ood_dataset_from_manifest` ← MR-1 (Lane 1 baseline eval, ~M1)
- `adversarial.character_injection` ← MR-2 (Lane 1b 12-tech matrix, ~M1)
- `losses.RecallAtLowFPR` ← MR-4 (Lane 2 retrain variant, ~M4)
- `preprocessing.spotlighting` ← MR-5 (Lane 3 demo, ~M5)
- `stacking.MetaLearner` + `LogisticStacker` ← MR-6 (Lane 4 fusion, ~M6)
- `probes.ActivationDeltaProbe` ← MR-7 (Lane 5 probe, ~M2)
- Existing primitives expected to be consumed in portfolio's
  composition layer: `eval_toolkit.metrics` (binary classification +
  bootstrap CIs + paired-bootstrap; canonical Platt+Beta+Isotonic
  binary calibrators per submission ADR-058), `eval_toolkit.scorers`
  (Scorer Protocol), `eval_toolkit.io` (predictions parquet writer).

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
| (none yet) | | | | | |

Expected populations:
- `/research-plan` ← M0 dossier sprint (week 1-3)
- `/research-gather` ← M0 dossier sprint
- `/dossier-build` ← M0 dossier sprint
- `/dossier-audit` ← M0 close (Day 19) + per-milestone re-runs
- `/dataset-synthesize` ← MR-3 (Lane 2 synthetic data gen, ~M3)

Tracked as v0.8+ upstream feature request: publish research_toolkit
to PyPI for cleaner pinning (currently consumed via git URL).

---

## @brandon_m_behring/book-scaffold-astro (npm; floor `^3.1.0`, blocks-on `^3.2.0` for chapter skeletons)

| Component / API | Min version | Used in | First commit | MR | Notes |
|-----------------|-------------|---------|--------------|----|-------|
| `defineBookSchemas()` | ^3.1.0 | `book/src/content.config.ts` | f011726 (M0 Day 2 scaffold bootstrap) | — | Stock scaffold |

Expected populations (post MR-8 v3.2.0 ship):
- `research-portfolio` profile (union schema academic ∪ tools)
- `PreReleaseBanner` component (state + dismissAt + message)
- `PolicyRef` component (generic cross-doc policy citation)
- `AICollaborationDisclosure` component (YAML-config disclosure paragraph)
- 18 callouts + 8 theorem family + KaTeX + BibTeX pipeline + `<Cite>`
  + `<MarginNote>` + 7-state status — already present in scaffold v3.1;
  consumed as portfolio chapter skeletons author per Day 14 M0
  sequence (gated on v3.2 ship per Round 11 Q1'''''''').

---

## Test-contract attestation

The `tests/contracts/test_library_imports_registered.py` contract
(part of the 7 Tier-4 contracts; implemented at M0 Day 3) parses
this file + verifies that every primitive imported in `src/` or `scripts/`
appears in a row above. Adding a new upstream import without
registering it here fails CI.

