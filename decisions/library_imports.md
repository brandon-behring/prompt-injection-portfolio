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

## eval-toolkit (PyPI; floor `[probes,losses]>=1.8`)

**Reproduction audit (2026-06-04):** floor advanced `>=1.6` → `>=1.8` across two upstream contributions
this session, both consumed in the bootstrap **reproduction audit** (`experiments/REPRODUCTION_2026-06/`):
`>=1.7` added `bootstrap.cluster_bootstrap_ci` (DF-9, #90 — label-stratified single-block cluster
bootstrap) and `>=1.8` added `bootstrap.stratified_cluster_bootstrap_ci` (DF-10, #92 — the composite
**multi-stratum** generalisation that actually fits the seed-averaged LODO estimators; the single-block
one could not). Both v1.7.0/v1.8.0 published to PyPI via Trusted Publishing (OIDC; receipts verified).
**DOGFOODED:** the new primitive re-derived all 3 LODO verdicts (dialect/carrier/§6.5) — point EXACT, CI
within MC noise. Production `falsify_*` loops unchanged (optional parallel re-lock = future follow-up).

**Round 28 (2026-05-29, ADR-051 EDA / Phase 3):** floor advanced `>=1.5` → `[probes,losses]>=1.6` to
consume the **Tier-2 `eda` Job-2 + Job-3 modules**, both built upstream this session: `lexical_association`
(#86 — C1 weighted log-odds/PMI + C2 partial-input competency baselines → V5) and `distribution_shift`
(#87 — E1 proxy-A-distance + unbiased RBF MMD + kNN purity → V9). v1.6.0 published to PyPI 2026-05-29 via
Trusted Publishing (tag `v1.6.0`, OIDC; receipt independently verified at the per-version endpoint). These
back the Phase-3 **pre-modeling OOD-wall prediction** (`experiments/eda/OOD_WALL_PREDICTION/`); the
real-data **dogfood run is P3.6 (pending)** — so the rows below are tagged *consumed-by-P3.6*, promoted to
`DOGFOODED` once the run lands. New symbols in the table below.

**Round 27 (2026-05-29, ADR-051 EDA):** floor advanced `>=1.0` → `[probes,losses]>=1.5` to consume the
**Tier-2 `eda` layer** (upstream #83: `audit_dataset`/`DataAudit`/`SplitSummary` + 3 integrity gates +
obfuscation) and the **schema-aware `HFDatasetsLoader`** (#85: `feature_cols`/`feature_join`/`label_map`/
`revision`). **This is the first DOGFOODED consumption** — both were exercised on real data in the
pre-modeling EDA (`experiments/eda/`: the RC0 BIPIA attack-type-split adequacy gate + the 13-dataset
full-landscape survey), unlike the rows below still tagged `<pending lane work>`. v1.5.0 published to
PyPI 2026-05-29 via Trusted Publishing (tag `v1.5.0`, OIDC, no tokens). New symbols in the table below.

**Round 26 (2026-05-26, ADR-051):** floor advanced `>=0.47` → `>=1.0` to opt into the
upstream **v1.0 stability contract** (their ADR 0003: Tier-1 API + 9 Protocols frozen
for the 1.x line; lock resolves 1.2.0). No consumer code exists yet, so this is **not yet
dogfooded** — but **M1+ lane code must target the v1.0 surface**, which changed since v0.47:
- `scorecard().to_dict()` keys are now `point` / `(low, high)` (was `point_estimate` / `ci_95`) — v0.48.
- 3 adversarial classes renamed (see the `adversarial` row below) — v0.49.
- `rng=` replaces `seed=` / `random_state=` across the stats fns, incl. `LogisticStacker(rng=…)` — v0.50.

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
| `adversarial.{12 dataclasses}` | `eval_toolkit.adversarial` | >=0.47 | `<pending Lane 1b 12-tech matrix>` | bc30c52 | MR-2 + MR-10 closed v0.43.0 + v0.47.0 | `ALL_TECHNIQUES` 12-tuple: ZeroWidthSpace, Homoglyph, Diacritic, Whitespace, **CaseInjection**, Punctuation (core-6) + BidiRTL, TagStripping, Synonym, **TokenSplittingInjection**, **UnicodeNormalizationInjection**, InvisibleChars (advanced-6) — **3 bolded names renamed in v0.49** (ADR-051 forward-guidance; were CaseRandomization / TokenSplitting / UnicodeNormalization) |
| `preprocessing.{3 dataclasses}` | `eval_toolkit.preprocessing` | >=0.47 | `<pending Lane 3>` | bc30c52 | MR-5 (#51) closed v0.44.0 | DelimitVariant, DatamarkVariant, EncodeVariant |
| `losses.RecallAtLowFPR` | `eval_toolkit.losses` | >=0.44 | `<pending Lane 2 retrain>` | bc30c52 | MR-4 (#50) closed v0.44.0 | Meta PG2 recipe; `[losses]` extra |
| `probes.ActivationDeltaProbe` | `eval_toolkit.probes` | >=0.43 | `<pending Lane 5>` | bc30c52 | MR-7 (#53) closed v0.43.0 | TaskTracker-style; `[probes]` extra |
| `stacking.LogisticStacker` | `eval_toolkit.stacking` | >=0.45 | `<pending Lane 4>` | bc30c52 | MR-6 (#52) closed v0.45.0 | Stacker reference impl |
| `eda.audit_dataset` | `eval_toolkit.eda` | >=1.5 | `experiments/eda/` (RC0 + `survey_v2.py`) | R27 | #83 | **DOGFOODED.** Job-1 integrity engine; gates `class_balance` / `no_cross_split_leakage` / `context_window_fit` + obfuscation → returns `DataAudit` |
| `eda.DataAudit` / `eda.SplitSummary` | `eval_toolkit.eda` | >=1.5 | `experiments/eda/` | R27 | #83 | **DOGFOODED.** audit result dataclasses (`.gate_passed`, `.split_summaries`, `.write(path)`) |
| `loaders.HFDatasetsLoader` (extended) | `eval_toolkit.loaders` | >=1.5 | `experiments/eda/survey_v2.py` | R27 | #85 | **DOGFOODED.** added `feature_cols`/`feature_join` (multi-col text join), `label_map` (raw→0/1), `revision` (SHA pin); fail-fast lists OBSERVED cols on mismatch |
| `embeddings.make_minilm_embedder` | `eval_toolkit.embeddings` | >=1.0 | `experiments/eda/RC0_BIPIA/run_rc0.py` | R27 | — | **DOGFOODED.** within-type MiniLM cosine (BIPIA memorization-floor check) |
| `eda.class_lexical_association` / `eda.weighted_log_odds` | `eval_toolkit.eda` | >=1.6 | `experiments/eda/OOD_WALL_PREDICTION/` (P3.6 pending) | R28 | #86 | C1: Monroe-2008 informative-Dirichlet weighted log-odds z + smoothed PMI → `LexicalAssociationResult` (V5). *Consumed-by-P3.6.* |
| `eda.competency_baselines` | `eval_toolkit.eda` | >=1.6 | `experiments/eda/OOD_WALL_PREDICTION/` (P3.6 pending) | R28 | #86 | C2: partial-input shortcut floor (length / char-n-gram / BoW) → `CompetencyResult`; the per-type shortcut-exposure signal. *Consumed-by-P3.6.* |
| `eda.distribution_shift` / `eda.proxy_a_distance` / `eda.maximum_mean_discrepancy` / `eda.knn_purity` | `eval_toolkit.eda` | >=1.6 | `experiments/eda/OOD_WALL_PREDICTION/` (P3.6 pending) | R28 | #87 | E1: linear-CV PAD + unbiased RBF MMD (median bandwidth, permutation p) + kNN purity → `DistributionShiftResult` (V9). *Consumed-by-P3.6.* |
| `scorecard` / `MetricResult` | `eval_toolkit` | >=1.6 | `experiments/attack-type-lodo/{metrics,detectors}.py` | R29 | TBD | **DOGFOODED (M1 Lane-1 harness).** Primary v1.0 metric surface: `scorecard(y, s, *, metrics=, bootstrap=, n_resamples=, rng=) → Scorecard[str, MetricResult]`; CI via `m.ci.ci_low/.ci_high`, single-class → `status="skipped"`. Headline AUPRC/AUROC/Brier/ECE battery + per-type diagnostic AUPRC. |
| `metric_specs.pr_auc/roc_auc/brier/ece` | `eval_toolkit.metric_specs` | >=1.6 | `experiments/attack-type-lodo/{metrics,detectors}.py` | R29 | TBD | **DOGFOODED.** Threshold-free `MetricSpec` singletons + `ece(n_bins=15)` factory (key `ece_n_bins_15_strategy_uniform`) fed to `scorecard(metrics=…)`. |
| `thresholds.recall_at_fpr` | `eval_toolkit.thresholds` | >=1.6 | `experiments/attack-type-lodo/metrics.py` | R29 | TBD | **DOGFOODED.** TPR@{1,0.5,0.1}% FPR: `recall_at_fpr(y, s, target_fpr) → RecallAtFprResult.recall` (ADR-036). NB: `losses.RecallAtLowFPR` is a torch *training* loss, **not** this reporting metric. |
| `artifacts.write_json_strict` | `eval_toolkit.artifacts` | >=1.6 | `experiments/attack-type-lodo/harness.py` | R29 | TBD | **DOGFOODED.** Strict RFC-8259 JSON writer (`write_json_strict(payload, path)`; NaN-sanitizing) for the per-`(rung,fold,seed)` metrics records (spec §5 retention). |
| `provenance.capture_git_sha` | `eval_toolkit.provenance` | >=1.6 | `experiments/attack-type-lodo/harness.py` | R29 | TBD | **DOGFOODED.** Git-SHA capture for the harness `MANIFEST.yml` provenance (spec §6). |

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
| `runpod_deploy.load_job_spec` | 0.8.4 | `scripts/runpod_sweep.py` | (runpod-wiring) | — | loads the strict-v2 YAML job spec |
| `runpod_deploy.run_job` | 0.8.4 | `scripts/runpod_sweep.py` | (runpod-wiring) | — | provision→stage→run→pull→lifecycle; `offline_dry_run` validates w/o spend |
| `runpod_deploy.RunpodJobSpec` | 0.8.4 | `scripts/runpod_sweep.py` (type) | (runpod-wiring) | — | returned by `load_job_spec` |
| `runpod_deploy.pricing` | 0.8.4 | `scripts/cheap_gpu_monitor.py` | (cheap-gpu-monitor) | — | `fetch_gpu_prices` / `select_price_for_pod` for best-effort price labels (`{}` when GraphQL pricing unavailable) |
| `runpod_deploy.provider.select_gpu_across_datacenters` | 0.8.4 | `scripts/cheap_gpu_monitor.py` | (cheap-gpu-monitor) | — | zero-spend availability probe: resolves (gpu, datacenter) from a gpu_order without provisioning |

> **Correction (2026-05-30): there is no `runpod_deploy.Session`.** The earlier "expected
> population" (and submission ADR-059) named a phantom symbol; the real `runpod-deploy>=0.8.4` API is
> a strict YAML job spec (`experiments/attack-type-lodo/runpod_lane1_sweep.yaml`) loaded via
> `load_job_spec` → `run_job`. `lifecycle` values are `preserve|stop|delete|recycle` (the Lane-1
> sweep uses `on_success: delete`). Lane 2 / 1b / 5 launches reuse this same `run_job` glue with
> their own job specs. Wiring validated via `scripts/runpod_sweep.py --offline-dry-run` (zero spend).

---

## research_toolkit (TOOLING clone pinned to `v2.4.1` — NOT a pip dep)

**Round 26 (2026-05-26, ADR-051):** dropped as a Python dependency (nothing imports it;
its `docling`/`pdfplumber` deps are irrelevant to validation). Now consumed as a
**repo-local clone** bootstrapped by `make dossier-audit` at tag `v2.4.1`
(`.tooling/research_toolkit`, gitignored), validators run in an ephemeral `uv` env
(PyYAML only) — plus the Claude skills below. Hence research_toolkit is no longer scanned
by the `library_imports_registered` contract (it's tooling, not a Python import).

> **Bumped `v2.4.0` → `v2.4.1` (2026-05-26):** adopts upstream #15 (`cache_root` wired
> through the v3 excerpt-anchor callers) — the citation/anchor gate was 100% failing under
> `v2.4.0` due to a path-resolution bug, not missing cache. See the ADR-051 follow-up.

| Symbol / skill | Min version | Used in | First commit | MR | Notes |
|----------------|-------------|---------|--------------|----|-------|
| `/research-plan` | v2.2.1 | M0 + Sprint 2 dossier sprint | `413284a` (Phase 1) + `f709f15` (Sprint 2 E1) | (none) | Used to scope 3 Sprint 1 topics + 2 Sprint 2 new topics |
| `/research-gather` | v2.2.1 | M0 + Sprint 2 E2 dossier sprint | `51785d9` (Phase 2) + `5bc9cf9` (Sprint 2 E2) | (none) | --cache-pdfs for ~124 arXiv PDFs across 5 topics |
| `/agent-index` | v2.2.1 | M0 + Sprint 2 E4 dossier sprint | `8b0fdb4` (Phase 3) + `16e9169` (Sprint 2 E4) | (none) | v2.2+ Attribute-First atomic decomposition; pre_selection_manifest |
| `/dossier-audit` | v2.2.1 | M0 + Sprint 2 E5 dossier sprint | `00d45c5` (Phase 4) + `b68329c` (Sprint 2 E5) | (none) | 6 Sprint 1 rounds + 3 Sprint 2 audit-trail rounds per topic |
| `/dataset-synthesize` | v2.4.0 | Lane 2 (~M3) | MR-3 merged 2026-05-24 | MR-3 | **Designated primary, execution GATED** on #21/#22/#23 (silent-failure + install gaps) — see upstream_issues.md |

Expected populations:
- `/research-plan` ← M0 dossier sprint (week 1-3)
- `/research-gather` ← M0 dossier sprint
- `/dossier-build` ← M0 dossier sprint
- `/dossier-audit` ← M0 close (Day 19) + per-milestone re-runs
- `/dataset-synthesize` ← MR-3 (Lane 2 synthetic data gen, ~M3) — STILL OPEN per Round 21

Tracked as v0.8+ upstream feature request: publish research_toolkit
to PyPI for cleaner pinning (currently consumed via git URL).

---

## @brandon_m_behring/book-scaffold-astro (npm; floor `^4.4.0`, resolves 4.5.1)

**Round 26 (2026-05-26, ADR-051):** pin advanced `^3.6.5` → `^4.4.0` and the book
**switched from the academic profile to `research-portfolio`** (v4's `defineStyle`
architecture). `astro.config.mjs` uses `styles: [researchPortfolioStyle]`;
`content.config.ts` uses `defineBookSchemas({ preset: 'research-portfolio', chaptersBase:
'./src/content/textbook' })` (BOOK_PROFILE env is dead in v4). The 13 `textbook/` chapters
validate + build green. Consumer fixes forced: per-chapter `freshness` values, the
**required** `last_verified`, and HTML→MDX comment conversion (see ADR-051 + DF-1/DF-2).

| Component / API | Min version | Used in | First commit | MR | Notes |
|-----------------|-------------|---------|--------------|----|-------|
| `defineBookConfig({ styles })` | ^4.4.0 | `book/astro.config.mjs` | (R26) | — | `researchPortfolioStyle` (v4 defineStyle) |
| `defineBookSchemas({ preset, chaptersBase })` | ^4.4.0 | `book/src/content.config.ts` | f011726 → R26 | — | `preset: 'research-portfolio'`; `chaptersBase: './src/content/textbook'` wires the 13 real chapters |

Now active (research-portfolio adopted at v4.5.1, R26); components available, consumed as chapters author per Day 14+:
- `research-portfolio` preset (union schema academic ∪ tools) — **ADOPTED** (was MR-8 (#6), closed v3.5.0)
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
