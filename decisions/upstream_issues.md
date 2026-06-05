# Upstream issues — state machine

Tracks all upstream issues filed against the 4 load-bearing libraries
(`eval-toolkit`, `runpod-deploy`, `research_toolkit`,
`@brandon_m_behring/book-scaffold-astro`).

Per Round 10 library-first invariant: **no local workarounds.** Missing
primitives become upstream issues + MRs; portfolio's `pyproject.toml`
(or `book/package.json`) pins the new version once released, then the
dependent lane proceeds. The standing GH-issue-filing permission lets
portfolio file issues during execution (not only the M0 batch) when
friction is encountered.

## State machine (per row)

```
issue-filed → pr-opened → pr-merged → released-vX.Y.Z → pinned-in-portfolio
```

`needs-redesign` is a side state when an issue is open but needs more
upstream discussion before a PR can be opened.

---

## M0 batch — filed 2026-05-19 (week 1 of M0) + Round 20/21 closures (2026-05-21)

Per plan §10 (Library-first audit). State machine advanced for 8 of 9
M0-batch MRs after Round 20 + Round 21 cascade: 5 eval-toolkit MRs
shipped (v0.43.0-v0.47.0) + 2 book-scaffold-astro MRs shipped (v3.3+ + v3.5.0).
**ALL M0-batch MRs now closed**: MR-3 merged 2026-05-24 (research_toolkit
PR #16). See "Filed during execution" table below for MR-12/-13/-14
(all also closed by 2026-05-24).

| # | Repo | Issue | Primitive | Blocks | State (Round 20/21 update) | Notes |
|---|------|-------|-----------|--------|----------------------------|-------|
| ~~MR-1~~ | brandon-behring/eval-toolkit | [#48](https://github.com/brandon-behring/eval-toolkit/issues/48) | `loaders.ood_dataset_from_manifest(yaml_path)` | M1 Lane 1 | **released-v0.43.0; closed 2026-05-19T19:30:20Z; pinned-in-portfolio via bc30c52 (Round 20)** | shipped by upstream parallel-Codex |
| ~~MR-2~~ | brandon-behring/eval-toolkit | [#49](https://github.com/brandon-behring/eval-toolkit/issues/49) | `adversarial.character_injection` (12-technique suite + Scorer-Protocol wrapper) | M1 Lane 1b | **released-v0.43.0 (core-6); v0.47.0 (advanced-6 via sweep unification); closed 2026-05-19; pinned-in-portfolio via bc30c52** | 12 dataclasses; `ALL_TECHNIQUES` 12-tuple |
| ~~MR-3~~ | brandon-behring/research_toolkit | [#1](https://github.com/brandon-behring/research_toolkit/issues/1) | `/dataset-synthesize` skill (prompt-caching template) | M3 Lane 2 data (~week 7) | **released; merged 2026-05-24 via research_toolkit PR #16 (squash 4d5b420); skill at `.claude/skills/dataset-synthesize.md`** | Recipe YAML + Anthropic prompt-caching + `--bail-at-cost` + idempotent resume + exit-code-3 on API error. UNBLOCKS Lane 2 primary path. |
| ~~MR-4~~ | brandon-behring/eval-toolkit | [#50](https://github.com/brandon-behring/eval-toolkit/issues/50) | `losses.RecallAtLowFPR` (Meta PG2 recipe) | M4 Lane 2 train | **released-v0.44.0; closed 2026-05-19; pinned-in-portfolio via bc30c52** | `[losses]` extra |
| ~~MR-5~~ | brandon-behring/eval-toolkit | [#51](https://github.com/brandon-behring/eval-toolkit/issues/51) | `preprocessing.spotlighting` (delimit + datamark + encode variants) | M5 Lane 3 | **released-v0.44.0; closed via upstream housekeeping; pinned-in-portfolio via bc30c52** | 3 dataclasses |
| ~~MR-6~~ | brandon-behring/eval-toolkit | [#52](https://github.com/brandon-behring/eval-toolkit/issues/52) | `stacking.MetaLearner` Protocol + `LogisticStacker` reference impl | M6 Lane 4 | **released-v0.45.0; closed 2026-05-21T18:22:48Z; pinned-in-portfolio via bc30c52 (Round 20)** | shipped same week |
| ~~MR-7~~ | brandon-behring/eval-toolkit | [#53](https://github.com/brandon-behring/eval-toolkit/issues/53) | `probes.ActivationDeltaProbe` (TaskTracker-style linear probe) | M2 Lane 5 | **released-v0.43.0; closed 2026-05-19; pinned-in-portfolio via bc30c52** | `[probes]` extra |
| ~~MR-8~~ | brandon-behring/book-scaffold-astro | [#6](https://github.com/brandon-behring/book-scaffold-astro/issues/6) | v3.2 `research-portfolio` profile (union academic ∪ tools schema + 3 new components + recipe + template) | M1 book authoring | **released-v3.5.0; closed 2026-05-19T19:29:53Z; pinned-in-portfolio via bc30c52 (Round 21 `^3.5.0`)** | UNBLOCKS Day 14 chapter skeletons |
| ~~MR-9~~ | brandon-behring/book-scaffold-astro | [#7](https://github.com/brandon-behring/book-scaffold-astro/issues/7) | Generic frontmatter collection + dynamic route helper | NOT blocking | **released-v3.3+; closed 2026-05-19T19:04:30Z; pinned-in-portfolio via bc30c52 (Round 21)** | Shipped earlier than expected |
| ~~MR-10~~ (Round 14 Q3) | brandon-behring/eval-toolkit | (NOT FILED — obsoleted before filing) | Advanced-6 character_injection techniques (bidi RTL + tag stripping + synonym + token splitting + Unicode normalization + invisible chars) | M1 Lane 1b full-12 matrix | **OBSOLETED via Round 20**: shipped in v0.47.0 as part of MR-2 12-technique consolidation BEFORE portfolio could file. `ALL_TECHNIQUES` 12-tuple exports the full set. Day 4 MR-10 filing step CANCELED. | Plan §10 row supersedes filing intent |

---

## Filed during execution

Per Round 10 ongoing-issue-filing discipline (user grant 2026-05-19):
when friction is encountered during execution (e.g., upstream primitive
doesn't compose ergonomically, scaffold callout missing for a chapter,
runpod-deploy validate flag missing), capture friction here + open the
issue + reference its `#N` here + continue execution.

Workflow:
1. Encounter friction
2. Add row below under "Filed during execution"
3. `gh issue create --repo brandon-behring/<lib> --label enhancement`
4. Reference issue number in the row
5. Continue execution — don't block unless friction has no clean
   compose-around using existing primitives. If genuinely blocking,
   escalate to "lane blocked until upstream ships" per
   no-local-workarounds rule.

| # | Repo | Issue | Friction | Workaround taken | State |
|---|------|-------|----------|------------------|-------|
| ~~MR-12~~ | brandon-behring/eval-toolkit | [#69](https://github.com/brandon-behring/eval-toolkit/issues/69) | 4 of 9 Tier-2 Protocols (`TextTransform`, `Probe`, `MetricSpec`, `MetaLearner`) live in different submodules; `eval_toolkit.protocols.__all__` only exports 6/9. Day 3a smoke-test `from eval_toolkit.protocols import Probe` failed with ImportError; canonical top-level `from eval_toolkit import Probe` works (per ADR 0002). | Portfolio uses top-level canonical imports — no code workaround needed; doc/discoverability issue. | **CLOSED 2026-05-24 (wontfix-with-docs)**: upstream chose NOT to expand `__all__` (would pull pandas/sklearn/matplotlib into the lightweight-Protocols module, breaking its design intent). Resolved via new ADR 0004 naming-conventions doc + cross-link from `docs/source/api/protocols.md`. Tier-1 top-level imports already intact. |
| ~~MR-13~~ | brandon-behring/book-scaffold-astro | [#54](https://github.com/brandon-behring/book-scaffold-astro/issues/54) | `npm run build:bib` (citation-js plugin-bibtex) fails when the canonical `bibliography.bib` template ships with a commented-out `% @article{example-key2024, ...}` example block. citation-js's lexer treats `@TYPE` tokens inside `%`-comments as real entry starts. | Portfolio's `book/bibliography.bib` header was edited to remove the `% @article{...}` template block (prose-only header preserved). | **CLOSED: resolved in book-scaffold-astro v4.0.0**. Template no longer ships the parser-tripping comment block. Portfolio's local workaround remains compatible; bump pin to ^4.0.0 at next book-authoring milestone (note: v4.0.0 is a BREAKING `defineStyle` architecture change — review migration before bumping past ^3.6.5). |
| ~~MR-14~~ | brandon-behring/research_toolkit | [#14](https://github.com/brandon-behring/research_toolkit/issues/14) | v2.3.0-candidate `cache_manifest.py` REJECTS absolute / `~`-prefixed paths; after migration, `v2_common.py` resolved relative `text_path` via `manifest_path.parent` instead of `cache_root`. Both validators inconsistent — no intermediate state passed both. `make dossier-audit` broke under v2.3-candidate. | At filing time: reverted migration; accepted pre-v2.3 baseline. | **CLOSED 2026-05-24 via research_toolkit PR #15 (squash 33f07f9)**: shared `resolve_cache_path()` helper added with cache_root → manifest-local fallback. Portfolio cache_manifest.yml migrated to relative paths (commit 5da5fd4); `make dossier-audit` PASSES (5 topics). Mixed-cache-location dossiers (218 canonical + 15 dossier-local body-anchored) now validate cleanly. |

---

## Dogfooding findings — Round 26 upstream adoption (2026-05-26, ADR-051)

Adopting the newer versions by *using* them surfaced the following. Posture this
pass: **file issues only** (clear repros; no upstream PRs). Lane 2 reliance is
gated on the research_toolkit items below.

| # | Repo | Friction surfaced by dogfooding | State |
|---|------|---------------------------------|-------|
| DF-1 | book-scaffold-astro | research-portfolio schema requires `last_verified` (`z.date()`), but recipe 13 / examples imply it's optional; all 13 portfolio chapters failed the astro build until it was added. | [#74](https://github.com/brandon-behring/book-scaffold-astro/issues/74) |
| DF-2 | book-scaffold-astro | `book-scaffold validate` CLI ignores `defineBookSchemas({preset, chaptersBase})` from content.config.ts — reports `profile=minimal` + only checks the default `src/content/chapters/`, diverging from Astro's content layer (which correctly used research-portfolio + `textbook/`). | [#75](https://github.com/brandon-behring/book-scaffold-astro/issues/75) |
| DF-3 | research_toolkit | `docling`/`pdfplumber` are *hard* deps, forcing validator-only consumers to install heavy ML deps they never use. Propose a `[validators]` extras split. (Motivated dropping the pip dep — ADR-051.) | [#26](https://github.com/brandon-behring/research_toolkit/issues/26) |
| DF-4 | research_toolkit | `evidence_ledger` validator hard-fails on absent `excerpt_anchor.text_path` body-text with no distinction between "cache not populated (re-fetchable)" and a genuinely broken anchor. A structural-only / `--allow-missing-cache` mode would let clean-checkout consumers validate ledger structure without the heavy cache. | [#27](https://github.com/brandon-behring/research_toolkit/issues/27) |

**Lane 2 `/dataset-synthesize` — readiness gate** (tracks EXISTING upstream issues; no dupes):

| Repo | Issue | Why it gates Lane 2 |
|------|-------|---------------------|
| research_toolkit | [#22](https://github.com/brandon-behring/research_toolkit/issues/22) | P1: candidate/dogfood-pending; silent-failure path (`_extract_text` drops non-text blocks, returns "") would silently corrupt a training corpus. |
| research_toolkit | [#23](https://github.com/brandon-behring/research_toolkit/issues/23) | P2: skill not installed by default (absent from Makefile SKILLS / quickstart / `~/.claude/skills`) → not reproducible. |
| research_toolkit | [#21](https://github.com/brandon-behring/research_toolkit/issues/21) | Post-merge polish (pricing staleness, API-key check location, cost-invariant test). |

Lane 2 keeps `/dataset-synthesize` as its **designated** primary data path (ADR-051),
but **execution is gated** on #22/#23 closing — no reliance until then; the 3-tier
fallback ladder remains the documented contingency.

**Pin-state updates (this round):**
- eval-toolkit: `>=0.47` → `>=1.0` (lock 1.2.0); v1.0 stability contract. Cannot be
  dogfooded until M1 (no consumer code yet) — pin + forward-guidance only.
- research_toolkit: git-pinned `@v1.9.1` dep → **dropped as a dep**; consumed as a
  repo-local tooling clone pinned `v2.4.1` via `make dossier-audit` (ADR-051; bumped
  `v2.4.0` → `v2.4.1` on 2026-05-26 to adopt the merged-but-untagged #15 `cache_root`
  resolution fix — see the ADR-051 follow-up).
- book-scaffold-astro: `^3.6.5` → `^4.4.0` (resolves 4.5.1) + research-portfolio profile.
- runpod-deploy: unchanged (`>=0.8.4` == PyPI latest 0.8.4; the GitHub Releases lag was a false alarm).

---

## Dogfooding findings — RunPod LoRA launch readiness (2026-06-01, ADR-054)

Surfaced while preparing the paid Lane-1 LoRA launch (`scripts/runpod_sweep.py --dry-run`).

| # | Repo | Friction surfaced by dogfooding | State |
|---|------|---------------------------------|-------|
| DF-6 | runpod-deploy | The RunPod pytorch base image (`runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04`) does not include `rsync`. `_push_workspace` invokes `rsync` locally to push to `root@<host>:<dest>`, which requires rsync on BOTH ends (the local client and the remote server). Without it, the rsync sub-process fails with `bash: line 1: rsync: command not found` and exit code 12, halting the run before any GPU time is consumed. **Workaround taken**: added a `setup` block to the YAML spec (`apt-get install -y -qq rsync`, ~10 s) which runs before staging. This works but is noise in every spec and will recur for any user using a lean base image. The library should either: (a) document the rsync requirement prominently in the quickstart, or (b) auto-install rsync as part of the SSH-ready validation step, or (c) offer a `scp`/`tar`-over-SSH fallback transfer mode when rsync is absent on the remote. **NON-BLOCKING** after the YAML workaround. | **issue-filed** — [#116](https://github.com/brandon-behring/runpod-deploy/issues/116) (2026-06-01). Workaround in place: `setup: [{command: "apt-get update -qq && apt-get install -y -qq rsync"}]` in the YAML spec. |
| DF-5 | runpod-deploy | `pricing.fetch_gpu_prices` returns **0 cards**. `_post_graphql` (`pricing.py:139-146`) authenticates the RunPod GraphQL `gpuTypes` query (`GRAPHQL_ENDPOINT = https://api.runpod.io/graphql`, `pricing.py:50`) with an `Authorization: Bearer <key>` header → **HTTP 403 Forbidden**. RunPod's GraphQL API classically expects the key as a `?api_key=<key>` query param, not a Bearer header. Reproduced with a valid 50-char key that authenticates `runpodctl` fine (the dry-run provisions normally). **NON-BLOCKING**: provisioning uses `runpodctl`; the budget guard falls back to `assumed_hourly_rate_usd`. Cost: the live-price display is empty and the `--max-gpu-price-usd` filter is inert (no prices to compare). | **issue-filed** — [#117](https://github.com/brandon-behring/runpod-deploy/issues/117) (2026-06-01). No workaround needed; rely on `assumed_hourly_rate_usd` + `cost_cap_usd` + `max_runtime_minutes`. |

---

## Dogfooding findings — Phase-2 dataset-universe EDA (2026-06-03) — DRAFT, NOT YET FILED (user-led)

Surfaced while EDA-gating the Phase-2 new datasets. Per the present-first discipline, public issue filing is
**user-led** — these are **drafted repros awaiting your go to file** (`gh issue create --repo
brandon-behring/eval-toolkit --label enhancement`). Both are genuine missing primitives that forced a local
one-off in the (ruff-excluded) `experiments/eda/` drivers; neither belongs in portfolio long-term.

| # | Repo | Friction surfaced by dogfooding | Proposed primitive | State |
|---|------|---------------------------------|--------------------|-------|
| DF-7 | eval-toolkit | `loaders.HFDatasetsLoader` assumes the HF Dataset Viewer / `load_dataset` works. `youbin2014/JailbreakDB` has a **broken Viewer** (500 "generation failed"; parquet-export job failed) → `load_dataset` cannot read it; it ships as two raw multi-line CSVs (~1.54M records). Also `perplexity-ai/browsesafe-bench` rows are ~46–140 KB HTML (34K tokens) and the in-scope corpora include multi-GB sets — loading full into memory to then sample is wasteful. Had to hand-roll a local `custom_csv_loader` (+ the pre-existing local `custom_parquet_loader`) in `experiments/eda/survey_v2.py` that reads via the HF `resolve/` URL **or** a local snapshot, with **memory-bounded per-chunk Bernoulli sampling**. | `eval_toolkit.loaders.RawFileLoader` (or a `streaming=`/`sample_rows=` mode on a CSV/parquet loader): Viewer-independent raw-file read (resolve-URL or local path), with an optional memory-bounded representative sample for multi-GB / multi-M-row corpora. | **DRAFT — not filed** |
| DF-8 | eval-toolkit | `eval_toolkit.leakage` checks (`CrossSplitLeakageCheck`) and `text_dedup.cross_dedup_pairs` are **in-memory** (both sides as `list[str]`). To leakage-gate JailbreakDB (~1.54M records) vs a ~68K probe (our jackhhao/shen/jbb), neither side composition fits the in-memory pair-finder at scale. Had to hand-roll `experiments/eda/jailbreakdb_leakage_scan.py`: **exact normalized-hash membership over a stream** + `MinHashLSHStrategy` near-dup on a bounded sample, asymmetric (index the small probe, stream the big corpus). | `eval_toolkit.leakage` streaming/asymmetric variant: index a small reference set, **stream** a large corpus, report exact + MinHash-near overlap **per reference corpus**. Reuses the existing `MinHashLSHStrategy` + `normalize_text_for_dedup` + `sha256_text` (so it's an orchestration layer, not new core). | **DRAFT — not filed** |

*(Cleanup companion, not an upstream gap: portfolio's `experiments/eda/cross_dataset_geometry.py` had local re-implementations of `proxy_a_distance` (as `pad()`) and a cross-source near-dup (`cross_dataset_neardup()`) that DUPLICATE existing upstream — `eval_toolkit.eda.proxy_a_distance` + `eval_toolkit.text_dedup.audit_source_label_similarity`. Resolved in-portfolio by consuming the upstream primitives — no issue needed.)*

---

## Dogfooding findings — B2.3 cluster-bootstrap parallelism (2026-06-04)

Surfaced while running the cross-family **dialect-LODO** cheap-rung sweep (`experiments/cross-family-transfer/`).
The label-stratified **cluster** bootstrap for the transfer-gap CI (`Gx = val_roc − test_roc`, positive- and
negative-clusters resampled separately) was **hand-rolled as a serial Python loop** in
`falsify_dialect_lodo.per_dialect_gap` — and the same shape was previously hand-rolled in
`falsify_carrier_lodo` (§6.5) and the attack-type LODO. Three call sites, one missing primitive ⇒ Rule of Three.
Per the user directive (2026-06-04) this is filed upstream, not worked around locally.

| # | Repo | Friction surfaced by dogfooding | Proposed primitive | State |
|---|------|---------------------------------|--------------------|-------|
| DF-9 | eval-toolkit | `eval_toolkit.bootstrap` ships **row-level** (`bootstrap_ci`), **fold-level** (`block_bootstrap_on_folds`), and **paired** (`paired_bootstrap_diff`, already `n_jobs`-parallel) bootstraps + analytic DeLong (`delong_roc_variance`) — but **no label-stratified cluster/group bootstrap**, the "missing middle" for clustered eval data (prompts sharing a payload; a doc contributing a poisoned + a benign row). DeLong assumes row-independence ⇒ under-covers clustered test sets. So portfolio hand-rolled a **serial** 10k-iter cluster bootstrap (using none of the upstream `parallel_map` + `spawn_seed_sequences` infra) in 3 LODO call sites — single-threaded on a 128-core box. | `eval_toolkit.bootstrap.cluster_bootstrap_ci(y_true, y_score, groups, statistic, *, resample_labels=(0,1), n_resamples, confidence, rng, n_jobs)` — resamples whole `groups` with replacement, unit = `(label, group)` (mixed-label groups split by label; `resample_labels=(1,)` = positives-only, negatives fixed = the carrier convention); percentile `BootstrapCI`; parallel via `parallel_map` + `spawn_seed_sequences` ⇒ **bit-identical across `n_jobs`**. | **issue-filed [#89](https://github.com/brandon-behring/eval-toolkit/issues/89) → pr-merged [#90](https://github.com/brandon-behring/eval-toolkit/pull/90) → released-v1.7.0** ([release](https://github.com/brandon-behring/eval-toolkit/releases/tag/v1.7.0); **PyPI 1.7.0 live**, 2026-06-04; + benchmark fix [#91](https://github.com/brandon-behring/eval-toolkit/pull/91)): fn + tests (unit/n_jobs-reproducibility/cluster-CI-wider-than-row/edge/doctest) + `__all__`/`_EXPORTS` + CHANGELOG; ruff + mypy-strict + tests + doctests green, coverage 92.6%. **Consumption: pin-bump-pending** — portfolio `pyproject` `>=1.6` → `>=1.7`, then consume in `falsify_dialect_lodo` + retrofit `falsify_carrier_lodo` (§6.5) + re-lock method (RNG-stream note + reproduction cross-check) **before B3** (Phase 3, separate go). |

*Side finding (separate, pre-existing — not in PR #90):* `tests/benchmarks/test_kernel_benchmarks.py` calls `bootstrap_ci(..., seed=…)` / `paired_bootstrap_diff(..., seed=…)` but those migrated to `rng=` (SPEC 7) → 2 bootstrap benchmark tests `TypeError` on the nightly-benchmarks workflow (excluded from PR CI). Trivial `seed=`→`rng=` fix; noted in #89, separate one-line PR offered.

**DF-10 (follow-on to DF-9, surfaced 2026-06-04 during the reproduction audit).** Consuming
`cluster_bootstrap_ci` (DF-9, v1.7.0) revealed it is **single-block** and cannot express the
**seed-averaging** all three LODO estimators do *inside* the bootstrap (`Gx = val − mean_seed(test_roc)`;
carrier additionally means over carriers; §6.5 a composite top−bottom `T`). So the single-block primitive
fits **none** of the three sites — an honest mis-scope on the DF-9 PR. The DF-9 "consumption" plan is
**superseded**: the correct primitive is the multi-stratum generalisation below.

| # | Repo | Friction surfaced by dogfooding | Proposed primitive | State |
|---|------|---------------------------------|--------------------|-------|
| DF-10 | eval-toolkit | `cluster_bootstrap_ci` (v1.7.0) is **single-block** → cannot express the seed-averaged / multi-group composite statistics the real LODO estimators bootstrap (dialect `val − mean_seed`; carrier mean-over-carriers; §6.5 top−bottom `T`). | `eval_toolkit.bootstrap.stratified_cluster_bootstrap_ci(strata, per_stratum_metric, combine, *, resample_labels, …)` — a composite statistic reduced over independently-resampled cluster **strata** (`strata={key:(y,score,groups)}`); `cluster_bootstrap_ci` = single-stratum identity-reduce special case; parallel + `n_jobs`-reproducible. | **released-v1.8.0 + consumed + reproduced** ([#92](https://github.com/brandon-behring/eval-toolkit/pull/92) merged `7284365`; [release v1.8.0](https://github.com/brandon-behring/eval-toolkit/releases/tag/v1.8.0); **PyPI 1.8.0 live**, 2026-06-04; pin `>=1.8`): fn + 11 tests (single-stratum-equivalence / seed-averaged / composite-`T` / n_jobs-reproducibility / validation) + `__all__`/`_EXPORTS`/CHANGELOG/golden; ruff + mypy-strict + doctests green. **Consumed in the reproduction audit** (`experiments/REPRODUCTION_2026-06/`): all 3 LODO verdicts (dialect 8/8 · carrier 3/3 incl. lora · §6.5 lora FALSIFIED) **re-derived — point EXACT, CI within MC noise (Δ ≤ 0.001)**. Production `falsify_*` loops unchanged (optional parallel re-lock = a future follow-up). |
| DF-11 | eval-toolkit | `stratified_cluster_bootstrap_ci` (v1.8.0) returns only `point_estimate` / `ci_low` / `ci_high` — **not** the bootstrap resample distribution. The production §6.5 + carrier estimators (`falsify_clustered.cluster_bootstrap`, `falsify_carrier_lodo._rung_gap`) persist a **`frac_gt0`** field (fraction of resampled stats > 0) into committed verdicts (`carrier-lodo/verdict.json`, the §6.5 verdict), which is structurally **unrecoverable** from the primitive's output → those two sites cannot migrate without dropping a committed field or retaining the serial loop. (The dialect site has no `frac_gt0` → **migrated cleanly 2026-06-04**, point EXACT / CI Δ ≤ 0.0023.) | An opt-in `return_samples=True` (expose the resample array) **or** a `frac_gt(threshold)` summary on `stratified_cluster_bootstrap_ci`, so consumers persisting `frac_gt0` can migrate (ADR-026 library-first completion of the re-lock). | **DRAFT — not filed (user-led).** Workaround: `falsify_carrier_lodo` + `falsify_clustered` stay on the hand-rolled serial bootstrap (reproduction audit already proved equivalence; zero verdict-impact). |

---

## Library-first invariant — restatement

- 4 load-bearing libraries are infrastructure for multiple consumers; portfolio
  is one consumer.
- Reusable primitives belong upstream, never hand-rolled in portfolio.
- Project-specific glue (lane orchestration scripts, data loaders composing
  eval-toolkit primitives, project-named CLI wrappers) is allowed in portfolio's
  `src/`.
- Missing upstream primitive + no clean compose-around → lane is blocked
  until upstream ships. No `# TODO(upstream #N)` markers; no transition
  commits with both paths live.

See also: `library_imports.md` (registry of primitives consumed by portfolio).
