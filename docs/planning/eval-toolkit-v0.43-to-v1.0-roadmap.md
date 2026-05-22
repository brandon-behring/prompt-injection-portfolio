# eval-toolkit holistic backlog → v1.0 (post-v0.44 state, staggered v1.0 path)

## Context

The original v0.43→v1.0 plan ([[i-want-to-systmetatically-piped-feigenbaum]]) executed on schedule through v0.44.0 (released 2026-05-19). Two things changed at this planning round:

1. **User stance: breaking API changes are OK at v1.0** — single active downstream consumer makes them cheap. The earlier plan kept #36 backward-compat (`with_ci=False` default); with breaking allowed, v1.0 can collapse the per-metric kwarg debate, return-shape sprawl, and four related warts into a coordinated multi-release sweep.
2. **Risk-reduction preference** — the user chose the most conservative bundling (three-phase staggered minors, not one big rc). Future major-version planning should default to staggering, not bundling.

A targeted audit ([[evaluate-all-the-work-twinkly-kite]] /exploring-options session) surfaced five v1.0 cleanup candidates and locked five design decisions. Tracking debt was reconciled in parallel: #51 shipped in v0.44.0 but the issue is still OPEN (manual close skipped); #49 advanced-6 was deferred but never filed; `mutants/` and `.env.local` slipped past `.gitignore`.

**Round 5 (2026-05-21): Gate 3 audit feedback integration.** Independent reads from Codex + Gemini surfaced 7 verified-real findings against the plan + shipped state. The most consequential:

- **F1 (Codex, blocker before v0.46):** scorecard()'s `MetricSpec.compute(y, s) -> float` signature can't carry F1/accuracy/precision/recall, which need a threshold. The library already separates these via `metrics_at_threshold` + `ThresholdSelector`. → Decision R: drop threshold-dependent metrics from v0.46 first-party specs.
- **F2 (Codex, blocker before v0.46):** Scorecard result type `MetricResult(point: float, ci: BootstrapCI | None)` has no contract for single-class slices, tiny inputs, per-metric bootstrap failures. `MetricState` already exists with `ok/skipped/error` vocabulary. → Decision S: reuse `MetricState` shape.
- **F3 (Codex, blocker before v0.47):** Plan assumes `DelimitVariant`/`DatamarkVariant` classes exist; `preprocessing.py:__all__` exports only functions (`delimit`, `datamark`, `encode`). Sweep consolidation must include creating these dataclasses or restructuring around callables.
- **F4 (Codex, plan-instruction error):** `__init__.py:302-312` is THE lazy export resolver for all root symbols. Plan's "add a `__getattr__` shim then delete the block at v0.47" would break every root import. The deprecation must EXTEND the existing resolver with a deprecated-names branch, then remove only that branch at v0.47.
- **F5 (Codex, blocker before v1.0):** `DeLongResult` + `delong_roc_variance` are publicly exported but methodology + roadmap say "out of scope". → Decision U: keep public; align docs.
- **F6 (Codex, packet drift):** `parallelism.md`, `testing.md`, `calibration.md` lag shipped state; `cv_clt_ci` docstring claims a "correction factor" the code doesn't apply; `bootstrap.md` two-level example is vulnerable to caller passing same array for val + test (~63.2% overlap).
- **F7 (Codex, governance honesty):** Multi-LLM cross-review is useful but not the same evidence class as external academic peer review. ADR 0003 must say so plainly.
- **Plan internal inconsistency:** v0.46 smoke imports `TextTransform`, but Decision K introduces it at v0.47.

These all map to plan edits below. The shape stays the same (staggered v0.45→v0.46→v0.47→v0.48→v1.0); the contents and ordering tighten.

**Round 6 (2026-05-21, post-v0.46 ship): Gate 3 STOP-GATE per Decision Y.2.** Codex + Gemini independent reads against the v0.46.0 state. 11 verified-real findings (Codex 6 + Gemini 5; 2 overlap on `seed=None` contract + ECE deprecation snippets). The most consequential:

- **Codex R6-F1 (BLOCKER before v0.47 opens):** `metric_specs.ece(strategy="typo")` silently dispatches to quantile ECE and returns a scorecard cell with `status="ok"` under the wrong key (`ece_n_bins_15_strategy_typo`). Wrong-by-design data correctness. → v0.46.1 hotfix.
- **Codex R6-F2 + Gemini R6-F2 (HIGH before v0.47 scalar hard-removal):** The 8 ECE deprecation warnings emit migration snippets that are wrong for every ECE variant — wrong scorecard keys (factory-call expression instead of encoded name) and 3 of the 5 ECE variants don't exist in `metric_specs` at all (`expected_calibration_error_debiased` / `_l2` / `_l2_debiased`). → v0.47 fix.
- **Codex R6-F3 (HIGH before scorecard freeze):** Duplicate `MetricSpec.name` in the same scorecard call silently overwrites the earlier cell. Not a documented contract. → **Decision R6-B**: raise `ValueError` at scorecard boundary.
- **Codex R6-F4 = Gemini R6-F1 (HIGH before v1.0):** `scorecard(seed=None)` documented as non-deterministic but coerced to `seed=0`. → **Decision R6-A**: deterministic-by-default; fix docs only (no behavior change).
- **Codex R6-F5 (contract-enforcement gap before v1.0):** ADR 0003 promises strict Tier-2 Protocol method-shape stability, but the public-API drift guard only snapshots `(*args, **kwargs)` for Protocol classes, not method signatures. → **Decision R6-D**: extend the snapshot test to capture Protocol method signatures.
- **Gemini R6-F3 (schema lock-in before v1.0):** `Scorecard.to_pandas()` MultiIndex columns drop `n_resamples` + `method` from `BootstrapCI`, breaking trace provenance compared to `to_dict()`. → **Decision R6-C**: add the two columns at v0.47 (additive).
- **Codex R6-F6 (packet drift):** v1.0 plan + roadmap still describe pre-v0.46 scorecard shapes that didn't ship (no-strategy ECE keys, `ece_quantile()` factory, `MetricUndefinedError`, `n_resamples >= 100` validation). → v0.47 plan refresh + v0.48 §5E-prep roadmap update.
- **Gemini R6-F4 (low):** No name-canonicalization helper for custom user specs — they may produce non-canonical keys. → Add `make_spec_name(prefix, **kwargs)` helper at v0.47.
- **Gemini R6-F5 (low):** Broad `except Exception` in `_evaluate_spec()` swallows `MemoryError` / `RecursionError` / `KeyboardInterrupt` / `SystemExit`. → Narrow the catch at v0.47.

**v0.46.1 hotfix packaging** (per Decision Q — wrong-API-shape / data-correctness regressions ship as hotfixes): Codex R6-F1 (ECE strategy validation) + Codex R6-F2 (deprecation warning snippet fixes) + Decision R6-A docstring fix. Small, urgent. Everything else folds into v0.47.

## Style invariants (read from what we've shipped through v0.47.0)

The audit findings below are SYMPTOMS of where code or docs drifted from these invariants — not items to point-fix individually. The invariants drive disposition choices when an audit finding has multiple plausible fixes:

1. **No silent failures.** Raise explicit `ValueError` / `TypeError` with context (CLAUDE.md python-standards). Drove R6-B (reject duplicate `MetricSpec.name`) + R6-F5 (re-raise system-exit-class exceptions).
2. **Methodology-honest defaults — the natural call pattern is the right one.** No magic numbers; required kwargs when there's ambiguity. v0.47's `attack_threshold` required-for-asr + v0.46.1's ECE strategy validation are the canonical examples.
3. **API-level errors with context; never low-level exceptions through the boundary.** Wrap numpy/list errors with `ValueError` tying failure to the offending call/spec/strategy. `_validate_scorecard_inputs` is the reference pattern.
4. **Mapping containers reject duplicate keys; row containers carry a stable disambiguator AND reject duplicates IN THAT disambiguator.** Different shape, same anti-silent-merge rule (R6-B Scorecard; R7-B sweep `strategy_id`).
5. **Docs that execute must execute correctly, on every execution surface.** Three surfaces with different collection scopes: Sybil (`testpaths` `.md` fences), MyST-NB (example notebooks during sphinx-build), pytest `--doctest-modules` (in-source docstrings). The pre-push gate covers ALL THREE simultaneously (see `[[feedback_sybil_python_blocks]]`, `[[feedback_degradation_layer_removal_hazard]]`).
6. **Public-API drift is tested via golden snapshot.** Every kwarg / signature / Protocol-method-shape change requires snapshot regen in the same commit (R6-D).
7. **Internal-vs-public distinction (ADR 0002).** Top-level `eval_toolkit.<name>` is contract; submodules are implementation. Pedagogical content reaches for the primary surface (scorecard, sweep, metric_specs) by default; submodule path is the escape hatch for callers needing scalar primitives.
8. **Additive-only at Tier-2 (ADR 0003).** Tier-2 Protocols + submodule public surfaces grow by addition. Removals require SemVer-major.

**Round 7 (2026-05-21, post-v0.47.0 ship): Gate 3 STOP-GATE per Decision Y.2.** Codex + Gemini independent reads against the shipped v0.47.0 state. Codex produced 3 verified-real substantive findings ("I would not close this as no findings"); Gemini's verdict was "highly stable; release/v0.48.0 is safe to open" — 6 minor observations / validations, no critical issues. Overlap was zero between the two reports. The most consequential finding (R7-F1 doc-migration boundary gap) was Codex-only and matches the v0.47 Sub-PR 7 incident class: removing the v0.46 `__getattr__` shim activated latent failures in another execution surface that the pre-push gate didn't cover. The three Codex findings:

- **Codex R7-F1 (HIGH before v0.48):** v0.47 doc migration only fixed Sybil-collected fences (`docs/source/methodology/*.md` + `README.md`). MyST-NB example notebooks under `docs/source/examples/*.md` are a SEPARATE executable surface — `conftest.py:51-54` explicitly excludes them from Sybil because they run during sphinx-build via `nb_execution_mode = "cache"`. Six example pages still import removed v0.47 APIs (top-level scalars, `character_injection` namespace, module-level `adversarial.sweep`, old `sweep(texts, scorer, threshold=...)` positional shape, `character_injection_sweep.md:132-139` still claims advanced-6 are "future v0.43.1 work"). The docs CI workflow runs `sphinx-build -b html` WITHOUT `-W`, so notebook execution failures only land as warnings — the build still reports success. Round 7 verification confirmed via runtime probe: all 6 pages report execution failures under the docs build. Additionally, `docs/source/api/protocols.md:6-15` autosummary omits `TextTransform` (the 9th Tier-2 Protocol); `src/eval_toolkit/__init__.py:3-6` module docstring still demonstrates a removed top-level `pr_auc` import; `src/eval_toolkit/__init__.py:210-215` still describes the v0.46 shim as active; `src/eval_toolkit/adversarial.py:18-36` module docstring still describes the removed adversarial sweep + namespace + claims advanced-6 are "scheduled for v0.43.1". → **Decision R7-A**: docs build fails on notebook execution errors at v0.48 (via `nb_execution_raise_on_error = True` in `conf.py`); 6 example notebooks + 4 module-level docstrings + `api/protocols.md` migration are part of the v0.48 release scope.
- **Codex R7-F2 (HIGH before sweep freezes):** `sweep()` records only `strategy.name` in each output row (`_sweep.py:165`), so two configured instances of the SAME shipped dataclass collapse to the same `variant` label. Runtime probe confirmed: `sweep([DelimitVariant(delimiter="<<"), DelimitVariant(delimiter="[["])], texts)` produces two rows both labeled `variant="delimit"`; `groupby("variant")` silently merges them. The DataFrame keeps both rows (no overwrite), but the analysis label cannot distinguish two configured strategy instances unless the caller manually overrides the public `name` field. This is the SAME defect class as Round 6 R6-F3 (scorecard duplicate `MetricSpec.name`) but with different semantics: scorecard returns a `Mapping[str, ...]` so silent overwrite is data loss → rejection. Sweep returns a row-major DataFrame so silent merge is an analysis-label issue → additive disambiguation column more appropriate than rejection (rejection breaks the natural "sweep over ratios" pattern). → **Decision R7-B**: add a `strategy_id` column to `sweep()` output at v0.48 (additive; per-row stable identifier carrying the strategy's configured kwargs).
- **Codex R7-F3 (worth fixing before v1.0):** `sweep()` doesn't validate scorer output shape/cardinality before building rows (`_sweep.py:151-176`). Runtime probe confirmed three different failure modes for common bad adapters: too many 1-D scores → silently accepted, extra score dropped (worst class — plausible output, wrong result); too few → `IndexError` later; `(n, 2)` matrix → `TypeError` later when `float(...)` is applied. None of these is an API-level shape error. → **Decision R7-C**: validate both score arrays against `(len(texts),)` at v0.48 with contextual `ValueError`.

The 9 other Round 6 follow-on items integrated into v0.47 (R6-A through R6-H minus the v0.46.1 hotfix scope) read as real fixes rather than ledger-only dispositions per Codex's §5 — no Round 7 finding in those paths.

**Gemini's 6 minor observations + validations** map to: R6-C `to_pandas()` int→float64 coercion (already an accepted tradeoff per Decision R6-C; will add a docs note in v0.48), `SynonymSubstitution` whitelist docstring sharpening (v0.48), Makefile pre-push target hardening to prevent the `pytest tests/` path-override trap that surfaced 40 Sybil failures in Sub-PR 7 (v0.48). Everything else in Gemini's report is a validation of the v0.47 shipped state.

The goal: take 2 remaining tracked issues (#52, #36) + 1 untracked carryover (#49 advanced-6) + 4 audit-driven API cleanups, ship them as a staggered v0.45 → v0.46 → v0.46.1 → v0.47 → v0.48 → v1.0.0 sequence.

## Locked decisions (this planning round)

| # | Decision | Choice |
|---|---|---|
| A | `scorecard()` metric specification | **Metric-spec objects** (`metric_specs.pr_auc`, `metric_specs.ece(n_bins=15)`) — type-safe; matches Protocol+frozen-dataclass house style |
| B | `bootstrap` default in `scorecard()` | **`bootstrap=True` default**; explicit `bootstrap=False` opt-out; `n_resamples=1000`, `confidence=0.95` baked in |
| C | Scalar metric function fate | **Top-level removed; submodule preserved as internal** — `from eval_toolkit.metrics import pr_auc` still works (subject to refactor in major versions, per ADR 0002) |
| D | Sweep API shape | **Free function `sweep(strategies, texts, scorer=None)`** — single public symbol; `CharacterInjectionSweep` / `SpotlightingSweep` classes removed from public API |
| E | Release bundling | **Three-phase staggered**: v0.46 scorecard → v0.47 sweep → v0.48 polish → v1.0 stability |
| F | Gate 3 (peer review) timing | **Kick off NOW** in parallel with v0.45 |
| G | #49 advanced-6 character_injection | **Bundle into v0.47.0** (revised — Decision Q12-11.3) — file issue in housekeeping; ship alongside sweep consolidation; eliminates the v0.45.1 release |
| H | Per-issue execution discipline | Reuse template from [[i-want-to-systmetatically-piped-feigenbaum]] §73–104; this plan only documents what's NEW or DIFFERENT |
| I | `Scorecard` container shape | **Read-only `Mapping[str, MetricResult]`** — dict subscript access only (`r["pr_auc"].point`); no `__getattr__`. Type-safe under `mypy --strict`. |
| J | `metric_specs` invocation style | **Mixed**: singletons for unparameterized (`ms.pr_auc`, no call); factories for parameterized (`ms.ece(n_bins=15)`). Factories LRU-cached for identity stability. |
| K | Strategy Protocol unification | **Single top-level `TextTransform` Protocol** at v0.47. Per-module Protocols (`CharacterInjectionStrategy`, spotlighting Protocol) removed from public API at v0.47. Concrete classes satisfy structurally — no code changes. |
| L | Scalar metric removal policy | **DeprecationWarning at v0.46, hard removal at v0.47.** `eval_toolkit.__init__.py __getattr__` shim emits warning for removed names; bounded transitional code deleted in v0.47 cleanup commit. |
| M | v1.0 stability contract scope | **Tiered**: top-level `__all__` + Tier-2 Protocols (9 strict + 1 opt-in) frozen strictly; submodule public symbols additive-only; docstring first lines NOT frozen (snapshot test adjusted at v1.0). Documented in new **ADR 0003**. |
| N | SimpleNamespace removal | **Remove both `character_injection` and `spotlighting` SimpleNamespaces at v0.47.** Concrete classes + top-level `sweep()` are the only public path; eliminates duplication tier. |
| O | Gate 3 methodology review | **Internal model-assisted cross-review** (user-directed; honesty-framing per Audit F7 — Codex): manual review by author + independent Codex report + independent Gemini report. **Explicitly NOT equivalent to external academic peer review** — the author shaped the packet, both model reviews are model-mediated, no third-party accountability for methodological judgment. Documented in ADR 0003 with that framing intact. Useful for catching contradictions and unstated assumptions (Round 5 demonstrated this); not a substitute for human external review on highest-risk methodology claims. |
| P | PR granularity per release | **Sub-PRs into `release/vX.Y` branch + single release commit** (matches v0.43 pattern of #54/#55/#56 → final release commit). Per-release branch isolates intermediate states from main; consumer can dry-run against the branch BEFORE main merge. |
| Q | Hotfix vs roll-forward policy | **Severity-tiered**: blockers (pipeline breakage, wrong API shape, data corruption, security/correctness regression) → hotfix as vX.Y.1 immediately. Non-blockers (cosmetic, docstring, message wording, perf without correctness impact, unhit edge cases) → roll forward into next minor's CHANGELOG. |
| R | Threshold-dependent metrics in scorecard | **DROP from v0.46 first-party specs.** Ship only threshold-free `metric_specs`: `pr_auc`, `roc_auc`, `brier`, `ece(n_bins)`, `ece_quantile(n_bins)`. F1/accuracy/precision/recall stay reachable via `metrics_at_threshold(y, s, threshold)` + `ThresholdSelector` Protocol — the existing operating-point machinery. Methodology-honest; smallest v1.0 contract. Revisit in v1.x if user demand surfaces. (Audit F1 — Codex.) |
| S | Scorecard cell-state contract | **Reuse existing `MetricState` vocabulary** (`artifacts.py:30-61`: `ok/skipped/error` + reason). `MetricResult` becomes: `value: float \| None`, `status: Literal['ok','skipped','error']`, `reason: str = ''`, `ci: BootstrapCI \| None = None`. Single-class slices, tiny slices, per-metric bootstrap failures yield `skipped`/`error` states with reasons — never raise out of the whole scorecard. (Audit F2 — Codex.) |
| U | DeLong v1.0 disposition | **Keep public; update methodology + roadmap docs to match code.** `DeLongResult` + `delong_roc_variance` stay in `_EXPORTS`. `methodology/comparison.md`, `methodology/reading_list.md`, and `roadmap.md` "Out of scope" updated to reframe: bootstrap is the preferred general comparison path, DeLong is a public ROC-AUC-specific closed-form variance primitive. Smallest delta; aligns docs to shipped state. (Audit F5 — Codex.) |
| W | Packet-drift fix timing | **All 7 fixes bundle into v0.48** (current plan) — single release coordination preferred over earlier docs accuracy. Trade-off accepted: methodology drift visible on PyPI until v0.48 ships. Mitigation: audit prompt updated with "known issues to skip" section so re-runs don't waste cycles re-flagging items already in the v0.48 backlog. |
| X | Skipped-status detection in scorecard | **Reuse existing `is_metric_defined_for_slice` from v0.39.0.** Scorecard calls it before invoking `spec.compute()`. Specs the primitive doesn't recognize fall through to attempt-compute → status='error' as fallback. No new public exception class; no new Protocol method. Consistent with `headline_metrics()` flow. **Implementation precondition**: verify `is_metric_defined_for_slice` accepts every v0.46 spec name (`pr_auc`, `roc_auc`, `brier`, `ece(*)` variants); extend the primitive if not. |
| Y | Audit re-runs as stop-gates | **Formal stop-gates after every breaking minor; 7-day timeout per gate.** Three audit gates: post-v0.46, post-v0.47, post-v0.48. After a minor ships, the Codex + Gemini re-run must complete (≤ 7 days) before the next minor's release branch can open. Blocker findings either fix-as-vX.Y.1-hotfix or fold into next minor's design. v0.45 (non-breaking, additive) does not gate. |
| Z | Audit findings ledger | **Public `docs/source/audit_findings.md` ledger + GitHub issues for blocker-severity findings only.** Single markdown file tracks each round's findings + disposition columns; high-severity items also get a `p1-gate3`-labelled issue for fix-tracking. Cross-referenced both directions. Created in Step 0 (housekeeping) with Round 5 entries; appended after each subsequent round. |
| R6-A | `seed=None` contract direction (Round 6 — Codex F4 + Gemini F1) | **Deterministic-by-default; fix docs only.** Keep the current `seed=0` behavior; rewrite the `scorecard()` docstring's `seed` description from "non-deterministic" to "default seed=0 for reproducibility; pass an explicit integer for control." No behavior change. Reproducibility-by-default is the right behavior for an evaluation toolkit; the v0.46 doc/impl contradiction was a docstring bug. |
| R6-B | Duplicate `MetricSpec.name` handling (Round 6 — Codex F3) | **Reject in `scorecard()` (raise `ValueError`).** When two specs in the `metrics` list share a `name`, raise: `ValueError("Duplicate MetricSpec name 'X' at index N; each spec must have a unique name for the Scorecard Mapping contract.")`. Forces caller to disambiguate; no silent data loss on user error. |
| R6-C | `Scorecard.to_pandas()` schema (Round 6 — Gemini F3) | **Add `n_resamples` + `method` columns at v0.47.** Schema becomes lossless against `BootstrapCI.to_dict()`. Additive expansion (callers indexing the MultiIndex by name keep working; callers indexing by position break — they shouldn't be doing that). v0.46 is the cheap moment because v1.0 is about to lock the schema. |
| R6-D | Protocol method-shape drift guard (Round 6 — Codex F5) | **Extend `tests/test_public_api.py` snapshot to capture Protocol method signatures.** Actually enforce what ADR 0003 promises about Tier-2 method-shape stability. Introspect each Protocol's methods + return types via `typing.get_type_hints` + `inspect.signature`; snapshot covers the 9 Tier-2 Protocols. Any change to `MetricSpec.compute`, `MetaLearner.fit`, etc., triggers the drift guard. Lands in v0.47 alongside the sweep work. |
| R6-E | v0.46.1 hotfix scope | **R6-F1 (strategy validation) + R6-F2 (warning content) only.** R6-A (docstring contradiction for `seed=None`) is NON-BLOCKER per Decision Q (docstring / message wording category) and rolls forward to v0.47. R6-F2 gets time-sensitivity exception because the shim only exists at v0.46 — the warning content has a 1–2 week shelf life that matters for consumer migration accuracy. |
| R6-F | ECE deprecation warning `n_bins` value | **Preserve pre-v0.46 default (`n_bins=10`).** Pre-v0.46 `expected_calibration_error` defaulted to `n_bins=10` (code at `metrics.py:730-734`); v0.46 `metric_specs.ece()` factory defaults to `n_bins=15` (matching Hines et al.). Warning snippets use `n_bins=10` to preserve bit-identical math for blind migrators + add migration note: "the v0.46+ metric_specs.ece() factory defaults to n_bins=15 (matching Hines et al.); pass n_bins=15 if you want the new convention." Gemini R6-F2 got the pre-v0.46 default wrong (claimed it was 15); plan corrected per ground truth. |
| R6-G | 3 ECE variants not in `metric_specs` | **Route deprecation warnings to submodule path; do NOT add to `metric_specs` at v0.47.** `expected_calibration_error_debiased`, `_l2`, `_l2_debiased` are research-completeness primitives with minimal consumer demand. Their deprecation warnings instruct: "use `from eval_toolkit.metrics import expected_calibration_error_debiased` (internal API per ADR 0002 — stable across v1.x, subject to refactor in major versions)." If consumer demand surfaces in v1.x, add as additive-only minor (Tier-2 commitment per Decision M allows this). |
| R6-H | `make_spec_name()` helper placement | **`metric_specs` submodule `__all__` only; NOT top-level `_EXPORTS`.** Users access via `from eval_toolkit.metric_specs import make_spec_name` OR `from eval_toolkit import metric_specs as ms; ms.make_spec_name(...)`. Tier-2 additive-only contract per Decision M allows the helper to evolve (e.g., gain a `formatter` kwarg in v1.x) without SemVer-major. Avoids top-level namespace bloat for utility code. |
| R7-A | Docs-execution CI gate (Round 7 — Codex F1) | **Enable `nb_execution_raise_on_error = True` in `docs/source/conf.py` at v0.48.** Notebook execution failures already surface as warnings during `sphinx-build`, but the docs.yml workflow runs without `-W` (intentional — ~56 advisory warnings predate v0.47 polish per `.github/workflows/docs.yml:51-58`). The MyST-NB setting specifically fails the build on notebook execution errors while leaving the unrelated xref/duplicate-label warnings as advisory. Narrower + cleaner than `-W`. v0.48 §5G covers the 6 stale example notebooks + 4 module-level docstrings + `api/protocols.md` `TextTransform` autosummary entry; v0.48 §5H wires the gate. |
| R7-B | `sweep()` identity disambiguation (Round 7 — Codex F2) | **Add `strategy_id` column AND reject duplicate `strategy_id` at sweep boundary (option C — style-coherent with R6-B).** Reading style invariants 1 (no silent failures) + 2 (natural call pattern is the right one) + 4 (canonical-identifier + reject-duplicates) together: emit `strategy_id` as the canonical per-row identifier built from configured kwargs (e.g., `"delimit/delimiter='<<',end='>>'"`); `variant` keeps current shape for backward-compat readers (e.g., `groupby("variant")` for "all delimits"). At the sweep boundary, raise `ValueError` if two strategies produce the same `strategy_id` — mirrors R6-B's rejection of duplicate `MetricSpec.name` in scorecard. The "cost" (intentional duplicate-instance sweeps would fail) is a non-cost: no methodology-honest reason to put the same configured strategy twice in one sweep; cache-warming + reproducibility re-runs use `.transform()` directly outside sweep. Additive schema expansion at v0.48 (Tier-2 contract); column gain of 1 + new ValueError class for the boundary check. |
| R7-C | `sweep()` scorer output shape validation (Round 7 — Codex F3) | **Validate `score.shape == (len(texts),)` after each batched `predict_proba` call; raise `ValueError` with strategy + call-site context.** Closes three failure modes Codex confirmed via runtime probe: overlong 1-D (silent truncation — worst, plausible output), short 1-D (`IndexError` later — low-level), `(n, 2)` matrix (`TypeError` later — low-level). All three become a single API-level shape error with context. Lands in v0.48 alongside the strategy_id change (R7-B). |

## Reconciled state (one-table summary)

| Item | Tracked | Actual | Action |
|---|---|---|---|
| #36 inline CI | OPEN | unshipped — redirected to `scorecard()` | v0.46.0 |
| #51 spotlighting | OPEN | **shipped in v0.44.0** | Close issue (housekeeping) |
| #52 LogisticStacker | OPEN | unshipped | v0.45.0 |
| #49 advanced-6 charinj | no issue (v0.43.1 forward-look in CHANGELOG, never tagged) | unshipped | **File issue, ship v0.45.1** |
| Gate 1 (consumer cycle) | in-progress | consumer pinned to v0.43.0 | Rolling-bump to v0.44 → v0.45 → v0.46 → v0.47 → v0.48 |
| Gate 2 (Protocol stability) | MET (per roadmap v0.41 entry) | MET — additive only through v0.42/v0.43/v0.44 | Reverify pre-v1.0 |
| Gate 3 (peer review) | not started | not started | **Start NOW** (long lead time) |
| Gate 4 (Croissant e2e) | MET | MET (v0.41) | — |
| `.gitignore` | missing `mutants/`, `.env.local` | both untracked | One-line gitignore patch |
| roadmap.md | "shipped as of v0.36.0" header, stale tracked-candidates | repo is at v0.44.0; most candidates closed | **Refresh in housekeeping** |
| `docs/source/adr/` directory | doesn't exist | doesn't exist | **Create in housekeeping** |
| `docs/source/migration/` | has v0.7/v0.8/v0.9 guides | pattern in use | Add v0.46/v0.47/v0.48/v1.0 guides per release |
| `PairedBootstrapCI` location | audit reported `preprocessing.py:187` | actually in `bootstrap.py` (per `_EXPORTS`) | No move needed; audit was wrong |
| SimpleNamespaces `character_injection` / `spotlighting` | exported, duplicates class/function API | duplication tier | Remove at v0.47 (§4E); flag for consumer dry-run verification |
| Module sizes vs ADR 0001 trigger | "800 LOC trigger" assumed | 9 modules already exceed 800 LOC | **Revise ADR trigger** (size alone not a signal) |
| v1-prelude evidence core | listed in roadmap as "next step" | shipped (visible in `_EXPORTS`) | Pre-v1.0: verify additive-only diff |
| JSON schemas | `schemas/*.v1.json` per roadmap | `manifest.v1/v2/v3.json` already exist | Pre-v1.0: document canonical per artifact type |

## Release sequence

| Step | Tag | Closes | Theme | Breaking? |
|---|---|---|---|---|
| 0 | (no tag) | — | Housekeeping: close #51, file advanced-6 issue (target v0.47), `.gitignore` patch, roadmap refresh, ADR directory, consumer → v0.44 | no |
| 1 | **v0.45.0** | #52 | LogisticStacker + `MetaLearner` Protocol | no |
| 1a | (no tag) | — | Consumer bump → v0.45 | — |
| 2 | **v0.46.0** | #36 | `scorecard()` + `Scorecard` (`Mapping[str, MetricResult]`) + `metric_specs`; top-level scalar functions emit DeprecationWarning via `__getattr__` shim; ADR 0002 | **YES** (soft — deprecation, not removal) |
| 2a | (no tag) | — | Consumer bump → v0.46 | — |
| 2b | **v0.46.1** | — | **HOTFIX (Round 6 findings; Decision R6-E scope)**: ECE strategy validation in `metric_specs.ece()` factory + `_EceSpec.compute()` (Codex R6-F1); deprecation-warning snippet fixes for all 5 ECE variants in `__init__.py:_scorecard_spec_for()` with `n_bins=10` per Decision R6-F + submodule-path template for 3 variants per Decision R6-G (Codex+Gemini R6-F2). R6-A (docstring) and all other Round-6 items roll forward to v0.47. | no (correctness fixes) |
| 2c | (no tag) | — | Consumer bump → v0.46.1 | — |
| 3 | **v0.47.0** | (advanced-6 issue) | `sweep()` unification + new top-level `TextTransform` Protocol; advanced-6 character_injection added; hard-remove v0.46 `__getattr__` shim; remove per-module strategy Protocols; remove `character_injection` + `spotlighting` SimpleNamespaces. **PLUS Round-6 follow-on**: `scorecard()` docstring fix for `seed=None` (Decision R6-A, bumped from v0.46.1 per R6-E); duplicate `MetricSpec.name` rejection in `scorecard()` (Decision R6-B); `Scorecard.to_pandas()` schema expansion with `n_resamples` + `method` columns (Decision R6-C); Protocol method-shape drift guard in `tests/test_public_api.py` (Decision R6-D); `make_spec_name(prefix, **kwargs)` helper in `metric_specs` submodule per Decision R6-H (Gemini R6-F4); narrow `_evaluate_spec()` exception catch (Gemini R6-F5); plan + roadmap state-drift refresh (Codex R6-F6). | **YES** |
| 3a | (no tag) | — | Consumer bump → v0.47 | — |
| 4 | **v0.48.0** | — | `metrics_at_threshold` key normalization, `BootstrapCI.to_dict()` rewrite, lazy-extras message audit, docstring example sweep, ADRs 0001 + 0003 | **YES** |
| 4a | (no tag) | — | Consumer bump → v0.48 | — |
| 5 | **v1.0.0** | — | Stability commitment; no new code; ADRs 0001 (flat-module), 0002 (scorecard-primary), 0003 (stability contract + Gate 3 methodology) finalized; roadmap gates MET | no |

Estimated calendar: ~4–6 weeks of release work (one fewer release after Q11 → 11.3 bundling) + Gate 3 multi-model cross-review (days, in parallel).

---

## Step 0 — Housekeeping (this week, no release)

Do all as a single small PR (or absorb into v0.45.0 prep commit). Order does not matter:

1. **Close #51** with comment pointing at v0.44.0 CHANGELOG + commit `005dd1a` (v0.44.0 entry confirms `preprocessing` module + spotlighting variants shipped; issue just never auto-closed).
2. **File new issue** `feat(adversarial): character_injection advanced-6` covering bidi-RTL, tag-strip, synonym, token-split, Unicode-normalize, invisible-chars. Note in the issue body: "v0.43.0 CHANGELOG entry referenced these as 'scheduled for v0.43.1' — that version never shipped; this issue picks up the deferred work." Tag `enhancement` + `P3`. Target milestone v0.45.1.
3. **`.gitignore` patch**: add `mutants/` and `.env.local`. Verify locally: `git status` clean after.
4. **Refresh `docs/source/roadmap.md`** — currently says "Currently shipped (as of v0.36.0)"; update to v0.44.0. Refresh "Tracked candidates" list (most items now closed: #31, #35, #37, #38 all closed 2026-05-18; #42/#43/#44/#48/#49/#50/#53 closed 2026-05-19). Remaining open: #36, #51 (pending close per step 1), #52. Update Gate 2 narrative to reflect continued stability through v0.42 + v0.43 + v0.44 (all additive). Clarify Gate 3 NOT-STARTED.
5. **Consumer rolling-bump v0.43.0 → v0.44.0** in `prompt-injection-detection-submission/pyproject.toml`. `uv lock --upgrade-package eval-toolkit`; run full consumer suite; observe 1 cycle. Finishes the v0.44 leg of Gate 1.
6. **Gate 3 kickoff** — see §Gate 3 parallel track below. Owner: user.
7. **Create `docs/source/adr/` directory** — placeholder with a stub `README.md` so ADRs 0001/0002 have a home in v0.46 (currently doesn't exist).
8. **Create `docs/source/audit_findings.md` ledger** (Decision Z) — single markdown file with one section per audit round. Round 5 (2026-05-21, Codex + Gemini) populated with the ~9 verified findings from this planning loop + their dispositions + links to plan sections / GitHub issues. Future rounds appended after each post-minor audit re-run (Y.2). Cross-referenced from ADR 0003 (Gate 3 governance).
9. **Update `~/.claude/plans/gate3-audit-prompt.md`** — add a "Known issues in current packet (skip re-reporting)" section listing the items deferred to v0.48 polish (§5E-prep) so future Codex + Gemini rounds don't waste cycles re-flagging them. Currently: `cv_clt_ci` docstring "correction factor" phrasing, `parallelism.md` lag, `testing.md` "PR 1.5" wording, `calibration.md` calibrator-family omission, `bootstrap.md` two-level example, DeLong methodology-vs-code contradiction, `CostSensitiveSelector` framing.

---

## Step 1 — v0.45.0 (Stacking, no breaking)

### #52 `MetaLearner` Protocol + `LogisticStacker`

Original plan ([[i-want-to-systmetatically-piped-feigenbaum]] §175–187) stands unchanged:

- **Module**: new `src/eval_toolkit/stacking.py` (flat, per Decision 2 in original plan).
- **No new deps** — sklearn already core.
- **Public API**: `MetaLearner` Protocol (`fit(score_matrix, y) -> Self`, `predict_proba(score_matrix) -> np.ndarray`); `LogisticStacker` frozen-dataclass reference impl. Pattern mirrors `Scorer` at `src/eval_toolkit/protocols.py:28`.
- **Tests**: shape contracts (N detectors × M samples), regularization handling, calibration chaining into `fit_platt_binary` (v0.40).
- **Docs**: `docs/source/stacking.md` myst-nb page; stack 2–3 detectors including `ActivationDeltaProbe` (v0.43).
- **Snapshot**: regen public API golden ([[feedback_public_api_snapshot_drift]]).
- **Release**: `make release-prep VERSION=0.45.0`; CHANGELOG `feat: MetaLearner Protocol + LogisticStacker (closes #52)`.

---

(v0.45.1 release eliminated by Decision Q11 → 11.3 — advanced-6 character_injection moved to v0.47.0 alongside sweep consolidation. See Step 3 §4F below.)

---

## Step 2 — v0.46.0 (Scorecard surface; FIRST BREAKING RELEASE)

### 3A. New `scorecard()` primary metric surface — closes #36

**New module**: `src/eval_toolkit/scorecard.py` (flat).

**Public surface** (revised per Decisions R + S):

```python
from eval_toolkit import scorecard, metric_specs as ms

r = scorecard(
    y_true, y_score,
    metrics=[ms.pr_auc, ms.roc_auc, ms.brier, ms.ece(n_bins=15)],
    bootstrap=True,           # default
    n_resamples=1000,         # default
    confidence=0.95,          # default
    seed=None,
)
r["pr_auc"].value             # 0.873  (None when status != "ok")
r["pr_auc"].status            # "ok" | "skipped" | "error"
r["pr_auc"].ci                # BootstrapCI(low=0.84, high=0.90, confidence=0.95) — None when skipped/error
r["pr_auc"].reason            # "" when ok; populated when skipped/error
r["ece_n_bins_15"].value      # parameterized metrics: deterministic string key
r.to_dict()                   # JSON-ready, deterministic key order

# Single-class slice example — scorecard does NOT raise; it records skipped state:
r2 = scorecard(np.zeros(100), y_score, metrics=[ms.pr_auc, ms.brier])
r2["pr_auc"].status   # "skipped"
r2["pr_auc"].reason   # "PR-AUC is not defined on a single-class slice"
r2["pr_auc"].value    # None
r2["brier"].status    # "ok"  (Brier IS defined on single-class)
r2["brier"].value     # float
```

**Public types** (all frozen, slots where applicable):
- `MetricSpec` Protocol: `name: str`, `compute(y_true, y_score) -> float` (raises `MetricUndefinedError` from inside if the slice/spec combination is undefined; scorecard catches and converts to `skipped` status).
- `metric_specs` namespace (Decision J + revised by Decision R):
  - Unparameterized **singletons** (threshold-free only): `pr_auc`, `roc_auc`, `brier`.
  - Parameterized **factory callables**: `ece(n_bins=int, strategy='uniform')`, `ece_quantile(n_bins=int)`. LRU-cached by kwargs so `ms.ece(n_bins=15) is ms.ece(n_bins=15)` holds.
  - **NOT in v0.46 scorecard**: `f1`, `accuracy`, `precision`, `recall` — these are threshold-dependent and reachable via the existing `metrics_at_threshold(y, s, threshold)` + `ThresholdSelector` Protocol. Adding an operating-point spec family is deferred to v1.x if user demand surfaces (Decision R).
- `MetricResult` (Decision S — reuses `MetricState` vocabulary at `artifacts.py:30-61`):
  ```python
  @dataclass(frozen=True, slots=True)
  class MetricResult:
      value: float | None                              # point estimate; None when status != "ok"
      status: Literal["ok", "skipped", "error"]
      reason: str = ""                                 # human-readable explanation
      ci: BootstrapCI | None = None                    # populated only when status == "ok" and bootstrap=True
  ```
  Aligns with existing `MetricState` (artifacts.py) used by `headline_metrics()` and the harness for single-class slices.
- `Scorecard` container (Decision I): subclass of `Mapping[str, MetricResult]`; read-only; exposes `__getitem__`, `__iter__`, `__len__`, `__contains__`, `.keys()`, `.values()`, `.items()`, `.to_dict()`, `.to_pandas()` (one row). **No `__getattr__`** — type-safe under `mypy --strict`.

**Per-cell failure isolation:** when one metric in the list fails (or is undefined), other metrics still compute. The whole scorecard never raises out of an individual metric's domain error; it records `status="error"` / `status="skipped"` for that cell. The wrapping function only raises for ABSOLUTE input validation failures (length mismatch, all-non-finite, empty input, bootstrap config out of bounds).

**Key-naming rule** for parameterized specs: `ece(n_bins=15)` → key `"ece_n_bins_15"` (alphabetized kwargs joined by underscore, snake-cased). Document explicitly so callers can predict keys without round-tripping through `.to_dict()`.

**Reuse**: `bootstrap_ci` and `BootstrapCI` from `src/eval_toolkit/bootstrap.py`; existing scalar metric implementations in `metrics.py` and `calibration.py` (scorecard dispatches by spec; doesn't reimplement). Parallel bootstrap via `_parallel.py` when `len(metrics)` is large — transparent to caller.

**Validation**: helper checks `len(y_true) == len(y_score)`, both finite, non-empty; `bootstrap=True` requires `n_resamples >= 100`; `confidence in (0, 1)`. Reuse `_check_inputs`-style patterns from `metrics.py`.

**Skipped-status detection** (Decision X.2): scorecard calls `is_metric_defined_for_slice(spec.name, y_true)` (existing primitive shipped v0.39.0, closes #39) BEFORE invoking `spec.compute()`. Flow:

```python
from eval_toolkit.metrics import is_metric_defined_for_slice

def _evaluate_spec(spec, y, s, bootstrap, n_resamples, confidence, seed):
    if not is_metric_defined_for_slice(spec.name, y):
        return MetricResult(value=None, status="skipped",
                            reason=f"{spec.name} not defined on slice")
    try:
        v = spec.compute(y, s)
    except Exception as e:
        return MetricResult(value=None, status="error", reason=str(e))
    ci = None
    if bootstrap:
        try:
            ci = bootstrap_ci(lambda yi, si: spec.compute(yi, si),
                              y, s, n_resamples=n_resamples,
                              confidence=confidence, seed=seed)
        except Exception as e:
            # Point estimate succeeded but bootstrap couldn't run
            # (e.g., n < 10 floor from bootstrap.py:198).
            return MetricResult(value=v, status="ok",
                                reason=f"bootstrap unavailable: {e}", ci=None)
    return MetricResult(value=v, status="ok", ci=ci)
```

**Implementation precondition** (Decision X.2 follow-up): before v0.46 release branch starts, verify `is_metric_defined_for_slice` accepts every v0.46 spec name (`pr_auc`, `roc_auc`, `brier`, every ECE variant in the namespace). If any are missing, extend the primitive to recognize them — this is a small additive change, not a new public surface.

**Tests** (revised — explicit per-cell-state coverage required by Decision S):
- Every threshold-free spec × `bootstrap={True,False}` produces a `MetricResult` with `status="ok"`, finite `value`, and (when `bootstrap=True`) a `BootstrapCI` whose bounds bracket the point.
- **Single-class slice**: `scorecard(np.zeros(100), s, metrics=[ms.pr_auc, ms.roc_auc, ms.brier])` returns `status="skipped"` for `pr_auc` + `roc_auc` (both undefined on single-class) and `status="ok"` for `brier`. Same for all-positive slice. Reason strings cite the existing methodology language ("single-class slice"). Cross-reference: harness uses the same language at `harness.py:347-349`.
- **Tiny slice with default bootstrap**: `scorecard(rng.integers(0,2,5), rng.random(5))` — n=5 is below `bootstrap_ci`'s `n>=10` floor (`bootstrap.py:198`). Expected: `value` is `ok`, `ci` is `None`, `reason` mentions "too few samples for bootstrap" — but the point estimate still computes.
- **Per-metric error isolation**: one custom spec raises `ZeroDivisionError` deep inside `compute()`; other specs still complete; the failing cell gets `status="error"`, `reason=str(exc)`.
- **JSON round-trip with mixed states**: `Scorecard.to_dict()` produces JSON-serializable output for ok/skipped/error cells; `to_pandas()` flattens consistently with NaN for skipped/error `value`.
- **Static contract**: `KeyError` on unknown metric key access (`r["pr_uac"]`); `ValueError` on unknown spec passed in; `Scorecard` is `Mapping[str, MetricResult]` (covariance + read-only verified); identity holds for spec singletons (`ms.pr_auc is ms.pr_auc`).
- **Point-agreement**: `scorecard(...)["pr_auc"].value == metrics.pr_auc(y, s)` when both succeed; locks scalar agreement with the submodule path.
- **Custom user spec**: implementing the `MetricSpec` Protocol satisfies the type-check + passes through scorecard with full state handling.

### 3B. Soft-deprecate scalar metric functions at top level (Decision L: WARN now, REMOVE in v0.47)

**Implementation correction per Audit F4 (Codex, VERIFIED):** `src/eval_toolkit/__init__.py:302-312` is THE lazy resolver for every root symbol in `_EXPORTS`. The earlier "add a shim / delete the block" framing was wrong — it would shatter ALL root imports. The correct shape is to *extend* the existing resolver with a deprecation branch, then *remove only that branch* at v0.47.

**v0.46 steps:**

1. **Remove deprecated scalar names from `_EXPORTS`**: drop `pr_auc`, `roc_auc`, `brier_score`, and the 5 ECE variants from the `_EXPORTS` dict. After this edit, `__all__` (derived from `_EXPORTS.keys()`) no longer advertises them.
2. **Add a deprecated-names set + extend the existing `__getattr__` resolver**:
   ```python
   # In src/eval_toolkit/__init__.py — kept verbatim through v0.46.
   # The lazy resolver below is the load-bearing public-API mechanism; this
   # block adds a deprecation branch in front of it (do NOT replace the
   # whole resolver — the existing branch resolves every other root symbol).

   _DEPRECATED_SCALARS: frozenset[str] = frozenset({
       "pr_auc", "roc_auc", "brier_score",
       "expected_calibration_error",  # + actual ECE variant names: enumerate
       # at implementation time by reading metrics.py + calibration.py
   })  # TRANSITIONAL — REMOVE AT v0.47 along with the branch below

   def __getattr__(name: str) -> Any:
       """Resolve public symbols lazily."""
       if name == "__version__":
           return __version__
       # ── BEGIN TRANSITIONAL DEPRECATION BRANCH (remove at v0.47) ──
       if name in _DEPRECATED_SCALARS:
           import warnings
           warnings.warn(
               f"eval_toolkit.{name} is deprecated and will be removed in "
               f"v0.47. Use `scorecard(y, s, metrics=[metric_specs.{name}])"
               f"[\"{name}\"].value` instead.",
               DeprecationWarning,
               stacklevel=2,
           )
           # Fall through to the normal resolver, which finds the function
           # via the metrics / calibration submodule.
           module_name = "eval_toolkit.metrics" if name != "expected_calibration_error" else "eval_toolkit.calibration"
           module = import_module(module_name)
           value = getattr(module, name)
           globals()[name] = value
           return value
       # ── END TRANSITIONAL DEPRECATION BRANCH ──
       module_name = _EXPORTS.get(name)
       if module_name is None:
           raise AttributeError(f"module 'eval_toolkit' has no attribute {name!r}")
       module = import_module(module_name)
       value = getattr(module, name)
       globals()[name] = value
       return value
   ```

3. **v0.47 cleanup is narrow:** remove the `_DEPRECATED_SCALARS` frozenset and the deprecation branch between the `BEGIN`/`END TRANSITIONAL` comments. The base resolver, `__all__` derivation, and `__dir__` stay exactly as they are today.

4. **Tests cover both behaviors:**
   - Remaining root exports continue to resolve lazily under v0.46 (`tests/test_public_api.py` already exercises every name in `__all__` via `getattr(eval_toolkit, name)`; that test must keep passing).
   - Deprecated names emit `DeprecationWarning` exactly once per first lookup; the function returned is the metrics/calibration submodule's scalar.
   - At v0.47, the same deprecated names raise `AttributeError` cleanly.

5. **Submodule path still works without warning** in both v0.46 and v0.47: `from eval_toolkit.metrics import pr_auc` is the internal-API escape hatch. ADR 0002 demotes the submodule to "implementation, subject to refactor in major versions" (per Decision C).

6. **Migration story:** consumer's `marginal_bootstrap.py:31-32,42-43,110` and `calibration_battery.py:47-52` refactor to `scorecard(...)` calls. Can ship across two consumer cycles — bump pin to v0.46 immediately (logs warnings), migrate at consumer's pace, then bump to v0.47 cleanly.

7. **CHANGELOG / snapshot:**
   - v0.46 CHANGELOG: `**DEPRECATIONS**` section listing every soft-removed symbol + migration snippet; explicit "will be hard-removed in v0.47".
   - v0.46 snapshot: deprecated names are gone from `_EXPORTS` → gone from `__all__` → gone from the golden snapshot. The deprecation shim adds runtime-only behavior; `tests/test_public_api.py` (which iterates `__all__`) doesn't see the deprecated names. The deprecation is purely runtime-discoverable.
   - v0.47 CHANGELOG: `**BREAKING CHANGES**` section noting the shim removal + final cleanup.
   - v0.47 snapshot: unchanged from v0.46 in this dimension (the snapshot already lacked the deprecated names since v0.46).

Net result: `Scorecard`, `MetricResult`, `MetricSpec`, `scorecard`, `metric_specs` (and their constituent singletons / factories per Decisions I/J) added to `_EXPORTS` at v0.46. Deprecated scalar names removed from `_EXPORTS` at v0.46 but still importable at top level with warnings; importable at top level fails at v0.47. ([[feedback_public_api_snapshot_drift]])

### 3C. ADR `0002-scorecard-as-primary-metric-surface.md`

Documents the v0.46 decision:
- Single-consumer / breaking-OK framing.
- Why `scorecard()` won over per-metric `with_ci=True` (single return shape; type-safe parameterized metrics; extensibility via Protocol).
- `eval_toolkit.metrics` submodule status (implementation, not contract).
- Future override condition: second consumer with materially different metric-surface needs → reconsider at v2.0.

### v0.46.0 release

- `make release-prep VERSION=0.46.0`.
- CHANGELOG opens with **DEPRECATIONS** section (per Decision L: warnings now, hard removal at v0.47) — not yet `**BREAKING CHANGES**`.
- **Add `docs/source/migration/v0.46.md`** per existing pattern (`migration/v0.7.md`, `v0.8.md`, `v0.9.md`). Document the `scorecard()` migration with side-by-side examples (`pr_auc(y, s)` → `scorecard(y, s, metrics=[ms.pr_auc])["pr_auc"].point`); reference the `__getattr__` shim and the v0.47 hard-removal date.
- Tag `v0.46.0`. Publish.
- **Rolling-bump consumer → v0.46**: consumer can bump pin BEFORE migration (warnings spam logs but code runs). Migrate callsites at consumer's pace; must be clean before bumping to v0.47. **Observe ≥1 full consumer review cycle** before proceeding to v0.47.

---

## Step 2.5 — v0.46.1 hotfix (Round 6 audit findings; correctness + time-sensitive warning)

Per Decision R6-E (locked): hotfix scope is R6-F1 (strategy validation) + R6-F2 (deprecation warning content). R6-A (`seed=None` docstring) is non-blocker per Decision Q (docstring category) and rolls forward to v0.47.

R6-F2 gets a time-sensitivity exception to Decision Q's "message wording → roll-forward" rule because the `__getattr__` deprecation shim **only exists at v0.46** (deleted at v0.47). Broken migration guidance has a 1–2 week shelf life that matters for consumer migration accuracy.

Ship as `v0.46.1` BEFORE opening `release/v0.47.0`. Small, urgent.

### 2.5A. ECE strategy validation (Codex R6-F1)

**Bug**: `metric_specs.ece(strategy="typo")` silently dispatches to quantile ECE and returns a scorecard cell with `status="ok"` under the wrong-by-design key `ece_n_bins_15_strategy_typo`. Verified by Codex via runtime probe.

**Fix**:

- `src/eval_toolkit/metric_specs.py` — validate `strategy` in two places:
  1. The `ece()` factory function (eager validation before LRU cache hit).
  2. `_EceSpec.compute()` (defence-in-depth for custom `_EceSpec` construction paths that bypass the factory).
- Raise `ValueError` with the message: `f"ECE strategy must be 'uniform' or 'quantile'; got {strategy!r}"`.
- Add a regression test in `tests/test_scorecard.py` covering: factory-level validation (`ms.ece(strategy="typo")` raises), and a parametrized check that valid strategies (`"uniform"`, `"quantile"`) still work.

### 2.5B. ECE deprecation warning snippet fixes (Codex R6-F2 + Gemini R6-F2)

**Bug**: All 5 ECE-variant deprecation warnings in `__init__.py:_scorecard_spec_for()` produce broken migration snippets:
- For `expected_calibration_error` / `expected_calibration_error_equal_mass`: the suggested scorecard lookup key is the factory-call expression (e.g., `"ece(n_bins=10)"`) instead of the actual encoded spec name (e.g., `"ece_n_bins_10_strategy_uniform"`).
- For `expected_calibration_error_debiased` / `_l2` / `_l2_debiased`: these variants don't exist in `metric_specs` at all; `_scorecard_spec_for` falls through to the original deprecated name, which is a non-functional snippet.

**Pre-v0.46 default verification**: Gemini R6-F2 claimed pre-v0.46 `expected_calibration_error` defaulted to `n_bins=15`; verified against `src/eval_toolkit/metrics.py:730-734` that the actual default is **`n_bins=10`**. Plan corrected per Decision R6-F.

**Fix**:

- Restructure `_scorecard_spec_for()` to return a `(spec_factory_expr, scorecard_key, has_first_party_replacement)` tuple.
- For `expected_calibration_error` → factory `ece(n_bins=10)` → key `"ece_n_bins_10_strategy_uniform"` (preserves pre-v0.46 math per Decision R6-F).
- For `expected_calibration_error_equal_mass` → factory `ece(n_bins=10, strategy="quantile")` → key `"ece_n_bins_10_strategy_quantile"`.
- For the 3 ECE variants NOT in `metric_specs` (Decision R6-G): emit a different warning template pointing at the submodule path:

  ```
  eval_toolkit.expected_calibration_error_debiased is deprecated and
  will be removed in v0.47. This variant is NOT in v0.46+
  metric_specs. Use:
      from eval_toolkit.metrics import expected_calibration_error_debiased
  (internal API per ADR 0002 — stable across v1.x, subject to
  refactor in major versions). Or contribute the variant to
  metric_specs if you use it regularly.
  ```

- Migration note in the warning (per Decision R6-F): append to the `expected_calibration_error` / `_equal_mass` warnings:

  ```
  Note: the v0.46+ metric_specs.ece() factory defaults to n_bins=15
  (matching Hines et al.); the n_bins=10 in this snippet preserves
  the pre-v0.46 math. Pass n_bins=15 to use the new convention.
  ```

- Extend `tests/test_deprecated_scalars_shim.py` with assertions that each warning's suggested snippet is executable: parse the snippet, attempt to evaluate it (in a safe eval context), verify it produces a usable `MetricResult` for the 2 variants with first-party replacements; for the 3 variants without, assert the submodule path is importable.

### v0.46.1 release

- Branch `release/v0.46.1` off main (post-v0.46.0 tag).
- Sub-PRs feed in per Decision P pattern; final release commit on the branch.
- `make release-prep VERSION=0.46.1`. CHANGELOG entry under `## [0.46.1]` with two fixes attributed (Round 6 audit, Codex + Gemini).
- **Public-API snapshot drift**: 2.5A adds validation behavior but no new symbols (no signature change); 2.5B is internal helper rewrite (no signature change but the helper docstring may shift). Verify snapshot stays clean; regen only if `_scorecard_spec_for` ends up in `__all__` (it shouldn't — it's underscore-prefixed).
- Tag `v0.46.1`. Push. publish.yml → PyPI.
- Consumer rolling-bump → v0.46.1. Observe 1 cycle.
- Update `docs/source/audit_findings.md` Round 6 entries: mark R6-F1, R6-F2 as RESOLVED with disposition pointing at v0.46.1.

**R6-A (docstring) and all other Round-6 items roll forward to v0.47** per Decision R6-E.

---

## Step 3 — v0.47.0 (Sweep unification + advanced-6 + cleanup + Round 6 follow-on; SECOND BREAKING RELEASE)

### 4A. New top-level `sweep(strategies, texts, scorer=None, attack_threshold=None) -> pd.DataFrame` — REVISED for Audit F3

**Module**: `src/eval_toolkit/sweep.py` (flat).

**Audit F3 critique (Codex, VERIFIED):** the original `sweep(strategies, texts, scorer=None)` design conflated two operations: (a) neutral text-transform enumeration (current `preprocessing.sweep` behavior), and (b) attack scoring with ASR (current `adversarial.sweep` behavior — requires a threshold). The earlier `TextTransform` Protocol only had `name + transform`, with no threshold attribute — but the `scorer=None` branch claimed to compute ASR. That's underspecified.

**Revised behavior — neutral transform by default; attack scoring is opt-in with explicit threshold:**

- `sweep(strategies, texts)` → DataFrame columns `text_id, variant, transformed_text`. Pure text-transform enumeration. Works for defenses, attacks, anything implementing `TextTransform`. Replaces both current sweeps' neutral subset.
- `sweep(strategies, texts, scorer=scorer, attack_threshold=0.5)` → adds columns `original_score, transformed_score, asr` per row. **`attack_threshold` is now a required kwarg** when `scorer` is provided — no default-0.5 magic (which the methodology docs explicitly warn against, per `methodology/thresholds.md:234-242`).
- `sweep(strategies, texts, scorer=scorer)` without `attack_threshold` → returns `original_score, transformed_score` columns but NOT `asr`. ASR requires an explicit threshold contract.
- Composes: same call can mix attack strategies (`adversarial`) and defense strategies (`preprocessing`).

**Migration parity (per Codex F3 recommendation):** before deleting the existing `preprocessing.sweep` and `adversarial.sweep`, the v0.47 PR sequence must include a parity test that demonstrates the replacement path produces equivalent transformed text rows for every existing variant + kwargs combination. Test fixture: build the same N×K input pairs, run through both old + new paths, assert DataFrame equivalence on the neutral columns.

### 4B. New top-level `TextTransform` Protocol (Decision K) — REVISED for Audit F3

**Audit F3 finding (Codex, VERIFIED):** `src/eval_toolkit/preprocessing.py:__all__` exports only functions (`delimit`, `datamark`, `encode`, `sweep`) and a `spotlighting` SimpleNamespace — **NO defense-strategy classes**. The plan's previous claim that "concrete classes (`DelimitVariant`, `DatamarkVariant`) satisfy this Protocol structurally — no code changes" was correct on the adversarial side (`adversarial.py` has 6 strategy dataclasses) but wrong on the preprocessing side. Two viable shapes:

```python
# eval_toolkit.__init__.py
from typing import Protocol, runtime_checkable

@runtime_checkable
class TextTransform(Protocol):
    name: str
    def transform(self, text: str) -> str: ...
```

**Implementation: create the preprocessing dataclasses at v0.47.** Three new frozen-dataclass strategies in `preprocessing.py` so the structural-satisfaction story holds across both modules:

```python
# In src/eval_toolkit/preprocessing.py — added at v0.47
@dataclass(frozen=True, slots=True)
class DelimitVariant:
    name: str = "delimit"
    delimiter: str = "<<"
    end: str | None = None

    def transform(self, text: str) -> str:
        return delimit(text, delimiter=self.delimiter, end=self.end)

@dataclass(frozen=True, slots=True)
class DatamarkVariant:
    name: str = "datamark"
    marker: str = "^"

    def transform(self, text: str) -> str:
        return datamark(text, marker=self.marker)

@dataclass(frozen=True, slots=True)
class EncodeVariant:
    name: str = "encode"
    encoding: Literal["base64"] = "base64"

    def transform(self, text: str) -> str:
        return encode(text, encoding=self.encoding)
```

- Existing functional API (`delimit(text)`, `datamark(text)`, `encode(text)`) stays at the module level. The dataclasses are thin wrappers preserving the functional layer's behavior + adding the `name + transform()` shape `TextTransform` requires.
- Adversarial side already has the shape: `ZeroWidthSpaceInjection`, `HomoglyphSubstitution`, etc. (`adversarial.py:139-397`) satisfy `TextTransform` structurally without changes.
- Per-module Protocols (`CharacterInjectionStrategy` in `adversarial.py`) **removed from public API** at v0.47: dropped from `__all__` and `_EXPORTS`. They may remain as internal documentation if useful but are not part of the contract.
- Domain clarity comes from module location (`from eval_toolkit.adversarial import ...`) and concrete class names — not from Protocol-level taxonomy.

**Snapshot at v0.47:** preprocessing.py `__all__` grows by 3 (`DelimitVariant`, `DatamarkVariant`, `EncodeVariant`); also adds `TextTransform` at top level. Removes `CharacterInjectionStrategy`, removes the SimpleNamespaces (per §4E).

### 4C. Consolidate two module-level `sweep` functions into one top-level (BREAKING)

**Current shape** (verified via `_EXPORTS` + CHANGELOG v0.43/v0.44):
- `eval_toolkit.adversarial.sweep(texts, scorer, techniques="all", threshold=0.5)` — module-level function (NOT a class — earlier audit miscategorized).
- `eval_toolkit.preprocessing.sweep(texts, variants=..., kwargs=...)` — module-level function with divergent signature.
- `character_injection` and `spotlighting` SimpleNamespaces ALSO expose `.sweep(...)` shortcuts.

**Target shape**:
- New top-level `eval_toolkit.sweep(strategies, texts, scorer=None)` is the only public sweep entry point.
- Module-level `adversarial.sweep` and `preprocessing.sweep` removed.
- `character_injection.sweep` and `spotlighting.sweep` SimpleNamespace shortcuts: see §4E (separate decision).

### 4D. Hard-remove v0.46 `__getattr__` deprecation shim (Decision L cleanup)

- Delete the entire `__getattr__` block from `src/eval_toolkit/__init__.py` (the `# TRANSITIONAL — DELETE AT v0.47` section).
- Delete `_DEPRECATED_SCALARS` frozenset.
- Update CHANGELOG v0.47 `**BREAKING CHANGES**:` section listing the now-removed names.
- After this commit, `from eval_toolkit import pr_auc` raises `AttributeError` cleanly — no transitional code in the codebase.

### 4E. Remove `character_injection` and `spotlighting` SimpleNamespaces (BREAKING; flag for confirmation)

The current `_EXPORTS` exposes two `SimpleNamespace` objects (`character_injection`, `spotlighting`) that mirror the function-style API from the original issues — providing duplication tier with the canonical classes/functions. At v0.47 (now consolidating around `sweep()`), this duplication becomes load-bearing tech debt: three ways to spell the same thing (class, module function, SimpleNamespace).

**Plan**: remove both from `_EXPORTS` at v0.47. Consumer doesn't use the SimpleNamespace style today (verified by the original audit). If discovered to be load-bearing during consumer dry-run, fall back to keeping them with a soft-deprecation note in CHANGELOG v0.47 + hard-remove at v0.48.

**Why this matters**: the user's "no legacy design" stance applies here too. Three surfaces for one operation IS the tech debt; v1.0 is the moment to collapse it.

### 4F. Advanced-6 character_injection (additive — Decision Q11 → 11.3)

Six new technique dataclasses behind the new top-level `TextTransform` Protocol — no Protocol changes (confirms Gate 2 reverification holds through v0.47).

- **Module touch**: extend `src/eval_toolkit/adversarial.py` — `BidiRTLInjection`, `TagStrippingInjection`, `SynonymSubstitution`, `TokenSplitting`, `UnicodeNormalization`, `InvisibleCharsInjection`.
- All structurally satisfy `TextTransform` (from §4B). No Protocol-level changes.
- **Tests** per technique: idempotence where applicable, round-trip, Unicode safety, determinism under seed.
- **Docs**: append 6 to `docs/source/adversarial.md` (no new page).
- **Snapshot**: regen — adversarial.py `__all__` grows by 6.
- **Issue tracking**: closes the advanced-6 issue filed in housekeeping (Step 0 #2).
- **Bundling rationale**: shipping additive techniques alongside the breaking sweep consolidation lets the consumer absorb "complete 12-technique suite + new sweep API" in one migration step rather than two.

### 4G-prep. `scorecard()` docstring fix for `seed=None` (Decision R6-A; bumped from v0.46.1 per R6-E)

**Bug**: `scorecard()` docstring at `src/eval_toolkit/_scorecard.py:343-344` says `seed=None` is non-deterministic; implementation at `:463-471` coerces `None → 0`. Doc/impl contradiction (Codex R6-F4 + Gemini R6-F1).

**Decision (R6-A — locked)**: deterministic-by-default is the right behavior; fix the docs. No behavior change.

**Fix**: rewrite the `seed` paragraph in `scorecard()` docstring:

```text
seed : int or None, optional
    Bootstrap RNG seed. Default ``None``, which is treated as
    ``seed=0`` for reproducibility — eval-toolkit's evaluation pipelines
    are deterministic by default. Pass an explicit integer to control
    the bootstrap RNG; pass a value derived from
    ``np.random.SeedSequence().entropy`` for non-deterministic
    sampling.
```

**Snapshot regen**: required since `tests/test_public_api.py` captures the first line of each public docstring. The first line of `scorecard()` is unchanged by this edit (only the body changes), so the snapshot diff is likely empty. Verify before commit.

### 4G. Duplicate `MetricSpec.name` rejection (Decision R6-B — Round 6 Codex F3)

**Fix**: validate the `metrics` list at the entry of `scorecard()`. Build a `seen: set[str]` while iterating; on duplicate, raise:

```python
raise ValueError(
    f"Duplicate MetricSpec name {spec.name!r} at index {i}; "
    f"each spec must have a unique name for the Scorecard "
    f"Mapping[str, MetricResult] contract."
)
```

**Tests**: add a regression test in `tests/test_scorecard.py` — `test_scorecard_rejects_duplicate_spec_names` exercising the raise. Add a positive test that two distinct specs (`ms.ece(n_bins=10)`, `ms.ece(n_bins=15)`) coexist (their names differ even though both are ECE).

**Public-API impact**: signature unchanged; only behavior tightens. Documented in v0.47 CHANGELOG under `### Fixed`.

### 4H. `Scorecard.to_pandas()` schema expansion (Decision R6-C — Round 6 Gemini F3)

**Fix**: extend the MultiIndex column list in `Scorecard.to_pandas()` to include `n_resamples` and `method` (from `BootstrapCI`):

```python
cols.extend([
    (name, "value"), (name, "status"), (name, "reason"),
    (name, "ci_low"), (name, "ci_high"), (name, "confidence"),
    (name, "n_resamples"),  # NEW per R6-C
    (name, "method"),       # NEW per R6-C
])
```

For cells where `ci is None` (skipped, error, bootstrap-unavailable), the two new columns get sentinel values (`NaN` for `n_resamples`, `""` for `method`) — matches the existing handling of `ci_low` / `ci_high` / `confidence` in those cases.

**Public-API impact**: additive schema expansion. Callers indexing the MultiIndex by name keep working; callers indexing by position break (but that's not a supported pattern). Documented in v0.47 CHANGELOG under `### Changed`.

**Tests**: extend `tests/test_scorecard.py::test_to_pandas_one_row` to assert both new columns exist and carry expected values for ok / skipped cells.

### 4I. Protocol method-shape drift guard (Decision R6-D — Round 6 Codex F5)

**Fix**: extend `tests/test_public_api.py` to capture each Tier-2 Protocol's method signatures + return types in the snapshot. The 9 Protocols to cover:

`Scorer`, `LeakageCheck`, `Splitter`, `ThresholdSelector`, `DatasetLoader`, `MetricSpec`, `TextTransform` (NEW at v0.47), `MetaLearner`, `Probe`.

Implementation sketch:

```python
def _protocol_methods_snapshot(cls: type) -> dict[str, Any]:
    """For a Protocol class, capture method signatures + return types."""
    methods: dict[str, str] = {}
    for name, member in inspect.getmembers(cls):
        if name.startswith("_"):
            continue
        if inspect.isfunction(member) or callable(member):
            try:
                methods[name] = str(inspect.signature(member))
            except (TypeError, ValueError):
                continue
    # Capture @property attributes too (read-only contract):
    properties = {
        name: str(getattr(cls, name).fget.__annotations__.get('return', '?'))
        for name in dir(cls)
        if isinstance(getattr(cls, name, None), property)
    }
    return {"methods": methods, "properties": properties}
```

The Protocol entries in `tests/golden/public_api/snapshot.json` grow from a thin `(*args, **kwargs)` signature to include the method shapes. Any change to `MetricSpec.compute`, `MetaLearner.fit`, etc., now triggers the public-API drift guard.

**Snapshot regen**: required in this commit. Each affected Protocol gets a new `methods` + `properties` sub-entry.

**Tests**: existing test_public_api.py drift guard now covers Protocol method shapes; no new test file needed.

### 4J. `make_spec_name(prefix, **kwargs)` helper (Round 6 Gemini F4 — placement per Decision R6-H)

**Placement** (Decision R6-H — locked): `metric_specs` submodule `__all__` only. NOT in top-level `eval_toolkit._EXPORTS`. Users access via `from eval_toolkit.metric_specs import make_spec_name` OR `from eval_toolkit import metric_specs as ms; ms.make_spec_name(...)`. Tier-2 additive-only contract per Decision M allows the helper to evolve (e.g., add a `formatter` kwarg, support custom value-rendering, etc.) without SemVer-major.

**Add** to `src/eval_toolkit/metric_specs.py`:

```python
def make_spec_name(prefix: str, **kwargs: object) -> str:
    """Canonicalize a parameterized MetricSpec name.

    Convention: alphabetized kwargs joined by underscore, snake-cased.
    Mirrors the v0.46 ECE encoding rule (`ece(n_bins=15, strategy="uniform")`
    → `"ece_n_bins_15_strategy_uniform"`).

    Use in custom MetricSpec implementations to avoid silent key drift
    when constructor argument order changes:

    >>> make_spec_name("custom_metric", alpha=0.1, beta=2)
    'custom_metric_alpha_0.1_beta_2'

    Parameters
    ----------
    prefix : str
        Base name (e.g., the metric family).
    **kwargs : object
        Spec parameters. Keys are alphabetized; values rendered via repr-stable
        str() conversion. Only finite, hashable values supported.
    """
    if not kwargs:
        return prefix
    parts = [prefix]
    for key in sorted(kwargs):
        parts.append(key)
        parts.append(str(kwargs[key]))
    return "_".join(parts)
```

Add to `metric_specs.__all__`. Tests in `tests/test_scorecard.py`: round-trip ordering invariance (`make_spec_name("ece", n_bins=15, strategy="uniform")` == `make_spec_name("ece", strategy="uniform", n_bins=15)`), positive examples for ECE encoding.

### 4K. Narrow `_evaluate_spec()` exception catch (Round 6 Gemini F5)

**Fix**: in `src/eval_toolkit/_scorecard.py:_evaluate_spec()`, narrow the two `except Exception:` catches to exclude system-exit-class exceptions:

```python
# Replace:
except Exception as exc:
# With:
except (MemoryError, RecursionError, KeyboardInterrupt, SystemExit):
    raise  # never silence these
except Exception as exc:
    ...  # existing handling
```

Two sites: spec.compute() catch and bootstrap_ci catch. Both follow the same pattern.

**Tests**: extend `tests/test_scorecard.py` with a parametrized test that confirms a spec raising `MemoryError` (mocked) propagates out of `scorecard()` rather than becoming `status="error"`.

### 4L. Plan + roadmap state-drift refresh (Round 6 Codex F6 — non-code)

The v1.0 plan file (this file) + `docs/source/roadmap.md` still describe pre-v0.46 scorecard shapes that didn't ship:

- Plan §3A scorecard example uses `r["ece_n_bins_15"]` — shipped key is `"ece_n_bins_15_strategy_uniform"`.
- Plan lists an `ece_quantile(n_bins)` factory — shipped is `ece(n_bins, strategy="quantile")` (one factory with the strategy kwarg).
- Plan mentions a `MetricUndefinedError` exception type — ADR 0002 + Decision X.2 explicitly chose no new public exception.
- Plan §validation describes `n_resamples >= 100` floor — shipped validator is `n_resamples >= 1` only (the >=100 floor isn't in the code).
- Roadmap "Currently shipped" header still says v0.44; v0.45 + v0.46 entries in CHANGELOG describe issues #52 + #36 as shipped.

**Fix**: update the plan's §3A example + Decision narratives to reflect shipped shapes. Refresh `docs/source/roadmap.md` "Currently shipped" header to v0.47.0 once that ships (or v0.46.1 if dispositioning happens then). Already-shipped issues (#36, #52) move to the changelog references; tracked-candidates list shows only `#59` (advanced-6) at v0.47.

**Where**: this is a doc-only commit on the v0.47 release branch (or a separate housekeeping PR). No code touch.

### v0.47.0 release

- `make release-prep VERSION=0.47.0`.
- CHANGELOG structure: separate **BREAKING CHANGES** + **ADDED** + **CHANGED** + **FIXED** sections.
  - **BREAKING**: (a) module-level `adversarial.sweep` + `preprocessing.sweep` removed (consolidated into top-level `sweep()`), (b) `__getattr__` deprecation shim removed (top-level scalar metrics now `AttributeError`), (c) per-module strategy Protocols (`CharacterInjectionStrategy`, spotlighting Protocol) removed, (d) `character_injection` + `spotlighting` SimpleNamespaces removed, (e) `scorecard()` now raises `ValueError` on duplicate `MetricSpec.name` (was silent last-wins).
  - **ADDED**: (a) new top-level `sweep()` function, (b) new top-level `TextTransform` Protocol, (c) advanced-6 character_injection techniques, (d) `metric_specs.make_spec_name()` helper for custom spec name canonicalization (Round 6 Gemini F4).
  - **CHANGED**: (a) `Scorecard.to_pandas()` schema gains `n_resamples` + `method` columns per `BootstrapCI` provenance (Round 6 Gemini F3); (b) `_evaluate_spec()` exception catch narrowed to exclude `MemoryError` / `RecursionError` / `KeyboardInterrupt` / `SystemExit` (Round 6 Gemini F5); (c) `tests/test_public_api.py` snapshot now captures Tier-2 Protocol method signatures (Round 6 Codex F5 / Decision R6-D).
  - **FIXED**: plan + roadmap state-drift items per Round 6 Codex F6 (already-shipped issues moved to changelog references; tracked-candidates list updated).
- Add `docs/source/migration/v0.47.md` per existing pattern (`migration/v0.7.md`, `v0.8.md`, `v0.9.md`). Document Round 6 follow-on impact: duplicate-name rejection, to_pandas schema expansion.
- Tag, publish, rolling-bump consumer → v0.47. Observe ≥1 cycle. **Round 7 audit STOP-GATE** (Decision Y.2, 7-day timeout) before `release/v0.48.0` can open.

---

## Step 4 — v0.48.0 (Polish sweep; THIRD BREAKING RELEASE, sets up v1.0)

### 5A. `metrics_at_threshold` key normalization (BREAKING)

- Standardize on abbreviated keys: `fpr`, `fnr`, `tn`, `fp`, `fn`, `tp`, `threshold`, `f1`, `precision`, `recall`, `accuracy`.
- Most keys already use this style; audit candidate #4 is mainly about confirming no spelled-out variants leak elsewhere.
- Sweep `metrics.py` and `calibration.py` for any other functions emitting dicts with mixed-style keys; align all in one pass.
- Tests: pin every returned key in a regression-guard test that asserts exact dict-key membership.

### 5B. `BootstrapCI.to_dict()` rewrite (BREAKING)

- **Current** (`src/eval_toolkit/bootstrap.py:122–130`): hard-coded `"ci_95"` regardless of `confidence` field.
- **New**: emit `{"point": p, "low": l, "high": h, "confidence": 0.95}` — generic, self-describing.
- Apply same fix to `PairedBootstrapCI` (audit suggests `preprocessing.py:187–195`; **verify location during implementation** — if misplaced, move to `bootstrap.py` as part of this work).
- Any caller parsing `"ci_95"` breaks; documented in CHANGELOG migration snippet.

### 5C. Lazy-extras error message audit (non-breaking)

- Sweep every `ImportError` raised in `src/eval_toolkit/**.py`.
- Standardize message: `f"<feature> requires <pkg>. Install with: pip install eval-toolkit[<extra>]"`.
- Files to check: `losses.py` ✅ (conformant), `probes.py` ✅, `calibration.py` (sklearn — core, may not need extras), `embeddings.py`, `loaders.py` (HF datasets).
- Add unit test importing each `[losses]` / `[probes]` symbol with extra missing; assert canonical error string.

### 5D. Docstring example sweep (non-breaking)

- Run `pytest --doctest-modules src/eval_toolkit/` and fix every failure.
- Audit candidate #10 noted stale examples (e.g., `mde_from_ci(paired=x)` after v0.34.0 renamed `paired` → `ci`).
- Rewrite metric-related doctest examples to use `scorecard()` shape (since the top-level scalar API no longer exists post-v0.46).

### 5E-prep. Packet-drift fixes for Gate 3 audit (Round 5 audit findings F6 + Gemini)

Documentation fixes flagged by the round-5 Codex + Gemini audits. None are breaking; all are correctness/honesty fixes to the methodology packet that Gate 3 will read. Bundle into v0.48 since polish releases naturally collect docs work.

1. **`cv_clt_ci` docstring** (`bootstrap.py:1156-1163`) — remove the phrase "with a correction factor". Replace with: "Bayle et al. 2020 prove that the naive sample-variance estimator (with `ddof=1`) gives valid asymptotic coverage under stability conditions, resolving the historical concern that fold correlation makes it anti-conservative. No additional correction factor is applied." Aligns docstring to the code's actual computation (verified at `bootstrap.py:1235-1241`).

2. **`docs/source/methodology/parallelism.md:143-181`** — replace the "as of v0.34, harness scoring and `evaluate_folded` are not yet parallelized" + "once #29/#30 land" language with the post-v0.36 reality: `evaluate(n_jobs=)` and `evaluate_folded(n_jobs=)` wire the unified parallelism pattern (verified at `harness.py:872-936`, `:1268-1321`). Also clarify in the parallelism table that `bootstrap_ci`'s `n_jobs` is effective ONLY for `method="studentized"` and raises for BCa / percentile (verified at `bootstrap.py:198-286`). Note: BCa is the default method per `methodology/comparison.md`; the table currently makes `bootstrap_ci` look uniformly parallel.

3. **`docs/source/methodology/testing.md:108-136`** — remove the "reference-equivalence gap is closing in PR 1.5" sentence. Roadmap state (verified at `roadmap.md:56-77`) lists existing reference-equivalence tests against sklearn / scipy for `pr_auc`, `roc_auc`, `brier_score`, `reliability_curve`, `bootstrap_ci`, `fit_isotonic_calibrator`, `fit_platt_calibrator`. The historical audit can stay; the "still pending" framing must go.

4. **`docs/source/methodology/calibration.md:15-18`** — the chapter intro lists fixes by temperature, isotonic, and Platt. Expand to include Beta (v0.40) and the 4-binary-adapter family (`fit_temperature_binary` v0.35 + `fit_isotonic_binary` v0.42 + `fit_platt_binary` v0.40 + `fit_beta_binary` v0.40), all uniformly returning `(params, apply)`. Cross-reference: roadmap.md:37-43 captures this baseline; methodology curriculum should mirror it.

5. **`docs/source/methodology/bootstrap.md`** two-level example — verified at `bootstrap.py:744-745` that `_paired_bootstrap_op_point_diff_step` draws `val_idx` and `test_idx` independently with replacement. The docs example MUST partition the y array before passing val + test arrays — passing `val_y=y, test_y=y` causes ~63.2% overlap and violates the two-level bootstrap's independence assumption. Two fixes:
   - **Docs:** rewrite the example to use a disjoint split (e.g., `val_y = y[:n//2]; test_y = y[n//2:]`).
   - **Code (defensive):** in `paired_bootstrap_op_point_diff()`, raise `ValueError` if `val_y is test_y` and the array length is the same — explicit refuse-to-shoot-the-foot guard. Methodology-honest. The function signature already takes them as separate arguments; this just adds the assertion.

6. **`docs/source/methodology/comparison.md:160-190` + `methodology/reading_list.md:156-177` + `roadmap.md` "Out of scope"** — DeLong docs update per **Decision U**:
   - `comparison.md`: change the "DeLong's test... not in eval-toolkit" framing to: "Bootstrap is the preferred general-purpose comparison path (works for arbitrary metrics, paired-sample-aware, supports any operating point). DeLong is publicly available as a ROC-AUC-specific closed-form variance primitive (`delong_roc_variance`, `DeLongResult`) for callers who specifically need it — typically when bootstrap cost dominates and the metric is exactly ROC-AUC."
   - `reading_list.md`: remove DeLong from "future work"; cite it as a shipped public API with the closed-form variance derivation reference (Sun & Xu 2014).
   - `roadmap.md` "Out of scope": remove the "McNemar / DeLong tests" bullet. Add a new note in "Currently shipped" or similar: "DeLong's closed-form ROC-AUC variance is exported as `delong_roc_variance` + `DeLongResult` since v0.x (predates the comparison-curriculum write-up); bootstrap remains the documented default for general-purpose comparison."
   - McNemar stays out of scope.

7. **`CostSensitiveSelector` docstring sharpening** (Gemini claim 1, partial) — verified at `calibration.py:354-412` that the existing docstring already explicitly contrasts the prior-corrected formula (implemented) with Elkan's prior-independent form (cited). The math is intentional, documented. But the framing could still mislead users who calibrate to deployment prior and apply the formula. Add a `Warning:` admonition block at the top of the docstring saying: "This formula assumes `y_score` is a calibrated probability with respect to a **balanced prior** (or equivalently, a raw likelihood ratio). If your scores are calibrated to the deployment prior (e.g., via `fit_platt_binary` on a representative validation set), the prior is already incorporated and applying this formula will double-count it. For deployment-prior-calibrated scores, use the simpler `t* = c_FP / (c_FP + c_FN)` form (no `prior` kwarg)." Add a doctest example showing both correct usages.

### 5E. ADR `0001-flat-module-layout.md`

- Documents flat-module decision per existing plan §222–227.
- **Trigger criteria for v2.0 subpackage restructure** (revised after auditing actual module sizes — 9 modules already exceed 800 LOC including `metrics.py` at 1819 lines, `bootstrap.py` at 1796 lines, `calibration.py` at 1477 lines):
  - (a) **Second production consumer** with materially different surface needs (the original "this consumer doesn't need it" justification stops holding).
  - (b) **Clear functional grouping** that the codebase asks for — e.g., `attacks/` for adversarial + preprocessing combined; `calibration/` for the 4-calibrator family + isotonic + Platt + beta.
  - (c) **Discoverability complaint** from real users (not internal tooling concern) — e.g., "I can't find where X is" issues filed twice.
  - **NOT a trigger**: per-module line count. Existing modules thrive at 1500+ LOC because they're cohesive (all metrics in `metrics.py`, all bootstrap in `bootstrap.py`). Size alone is not a signal.

### 5F. ADR `0003-stability-contract-and-gate3-methodology.md` (NEW — Decisions M + O)

Documents two interlinked v1.0 decisions:

1. **Tiered stability contract** (Decision M / Q10 → 10.3):
   - **STRICT (SemVer-major to change)**: symbols in `eval_toolkit.__all__`, their signatures, the 9 Tier-2 Protocols (`Scorer`, `LeakageCheck`, `Splitter`, `ThresholdSelector`, `DatasetLoader`, `MetricSpec`, `TextTransform`, `MetaLearner`, `Probe`) + 1 opt-in (`Versioned`), and current JSON schema versions per artifact type.
   - **ADDITIVE-ONLY (SemVer-minor)**: submodule public symbols (`eval_toolkit.metrics.*`, etc.); Tier-2 Protocols can gain optional methods via subprotocols.
   - **FREE (SemVer-patch)**: docstring first lines (snapshot test updated to skip at v1.0), implementation internals, error message wording.
   - `tests/test_public_api.py` modified at v1.0 to drop docstring-first-line capture from the golden, OR gate it behind `STRICT_DOCSTRINGS=1` env var so the strict mode remains available for local verification.

2. **Gate 3 methodology cross-review** (Decision O / user-directed):
   - The original "external academic peer reviewer" approach is replaced with a multi-model cross-review process.
   - Three independent reviews: (a) manual review by user (author), (b) Codex independent report, (c) Gemini independent report.
   - All three reviewers receive the same packet: `docs/source/methodology/` (16 chapters) + feature pages (`scorecard.md`, `sweep.md`, `stacking.md`) + ADRs 0001/0002/0003 + this plan file.
   - Any reviewer-flagged blocker becomes a `p1-gate3`-labelled issue; must close before v1.0 tag.
   - Predictable cycle time (days, not weeks); no calendar uncertainty from reviewer-availability.

### 5G. Migrate 6 MyST-NB example notebooks to v0.47 API (Round 7 — Codex R7-F1)

Six pages under `docs/source/examples/` still import removed v0.47 surface; verified via runtime probe (`sphinx-build` reports execution failures on each but the build still passes because `-W` is off — Codex R7-F1). Migrate each in v0.47-vocabulary per `docs/source/migration/v0.47.md` recipes:

- **`metrics_and_bootstrap.md:23-29`** — `from eval_toolkit import pr_auc, roc_auc, brier_score` → `from eval_toolkit.metrics import pr_auc, roc_auc, brier_score`. Where pedagogically appropriate, demonstrate the v1.0-primary `scorecard()` surface (ADR 0002); use the scalar-submodule path only when illustrating the underlying math.
- **`calibration.md:22-31`** — same pattern; the chapter is about calibrator families, not the metric surface, so submodule path is acceptable.
- **`paired_comparison.md:36-40`** — same pattern.
- **`stacking.md:38-47`** — same pattern.
- **`character_injection_sweep.md:26-35,57-75,77-113,132-139`** — REMOVE `character_injection` namespace + module-level `sweep` imports; rewrite to use top-level `sweep(strategies, texts, scorer=detector, attack_threshold=0.5)` with concrete dataclasses. ALSO: lines 132-139 incorrectly claim advanced-6 is "scheduled for v0.43.1" — update to reflect v0.47 shipped state + demonstrate the full 12-technique surface via `ALL_TECHNIQUES`.
- **`spotlighting.md:23-33,69-93,121-128`** — REMOVE `spotlighting` namespace + module-level `sweep` imports; rewrite to use top-level `sweep(strategies, texts)` with the 3 Variant dataclasses.

**Module-level docstring sweep** (audit-as-seed extension — broader than the 4 Codex listed). Per style invariant 5 (docs must execute correctly on every surface) + 7 (pedagogical content reaches for primary surface), audit EVERY module-level docstring in `src/eval_toolkit/` for v0.47 accuracy, not just the ones Codex flagged. Known stale + plausible additional candidates:

- **Known stale (Codex R7-F1 + sub-PR 6 partial cleanup):**
  - `src/eval_toolkit/__init__.py:3-6` still demonstrates removed `pr_auc` top-level import. Rewrite to show the v0.47 primary surface.
  - `src/eval_toolkit/__init__.py:210-215` still describes the v0.46 shim as routing top-level scalars. Update to "removed at v0.47; submodule path remains" wording.
  - `src/eval_toolkit/adversarial.py:18-36` still describes the removed adversarial `sweep` + `character_injection` SimpleNamespace, and claims advanced-6 are "scheduled for v0.43.1". Rewrite to v0.47 state + the full 12-technique surface via `ALL_TECHNIQUES`.
  - `src/eval_toolkit/preprocessing.py:15-23` was only partly cleaned in Sub-PR 6 — still mentions `spotlighting` namespace by name (the post-Sub-PR-6 wording says it was "removed at v0.47" but the line still describes it as the function-style API). Sharpen.

- **Plausible additional drift (verify each):**
  - `src/eval_toolkit/_scorecard.py` module docstring — describe the v0.46 surface + R6-A/R6-B/R6-C/R6-F5 additions at v0.47.
  - `src/eval_toolkit/metric_specs.py` module docstring — describe the v0.46 surface + v0.46.1 strategy validation + v0.47 `make_spec_name` helper.
  - `src/eval_toolkit/protocols.py` module docstring — the file's docstring may still list only 5 Protocols; v0.47 added `TextTransform` (now 9 strict Tier-2 + 1 opt-in).
  - `src/eval_toolkit/_sweep.py` module docstring — written at v0.47 so likely accurate; verify.
  - `src/eval_toolkit/_deprecated.py` — was deprecation infrastructure; may still describe v0.46 shim mechanics that no longer apply.

- **Doc-reference pages:**
  - `docs/source/api/protocols.md:6-15` autosummary list omits `TextTransform`. Add it (alphabetized between `Scorer`/`SliceAwareScorer` and `Versioned`).
  - Verify `docs/source/api/*.md` covers every v0.46/v0.47 addition (scorecard family, sweep, advanced-6 dataclasses).
  - `docs/source/roadmap.md:108-110` says examples are "Sybil-validated" — that's true for the methodology + migration pages but NOT for `docs/source/examples/*.md` (those are MyST-NB-executed during sphinx-build per `conftest.py:51-54`). Reword to distinguish the two execution surfaces.

### 5H. Wire `nb_execution_raise_on_error` so docs CI fails on broken notebooks (Decision R7-A)

Edit `docs/source/conf.py` near the existing `nb_execution_mode = "cache"` setting:

```python
nb_execution_mode = "cache"
nb_execution_timeout = 90
nb_execution_show_tb = True
nb_execution_raise_on_error = True   # v0.48 (Decision R7-A): docs CI fails on notebook execution errors
nb_merge_streams = True
```

This is the narrower-than-`-W` fix Codex recommended. It does NOT enable strict-warnings mode globally, so the ~56 advisory MyST xref + duplicate-label warnings remain advisory (preserving the v0.31.0 migration concession in `.github/workflows/docs.yml:51-58`). It DOES fail the build on the specific class of failure Sub-PR 7's incident class produces.

Verification: in CI, intentionally introduce a broken `{code-cell}` (e.g., `import eval_toolkit; eval_toolkit.nonexistent_name`) on a branch and confirm the docs job goes red.

### 5I. `sweep()` `strategy_id` column + duplicate rejection (Decision R7-B option C — Round 7 Codex R7-F2)

Style-coherent with R6-B (scorecard duplicate `MetricSpec.name`): emit a canonical identifier AND reject duplicates at the boundary. Two parts in one sub-PR.

**Part 1: emit `strategy_id`.** Extend `src/eval_toolkit/_sweep.py:163-177` row construction with a new `strategy_id` column that's a stable per-row identifier built from the strategy's configured kwargs. Approach (mirrors `metric_specs.make_spec_name`):

```python
def _strategy_id_for(strategy: TextTransform) -> str:
    """Stable identifier carrying configured kwargs.

    For dataclass strategies: ``name + "/" + alphabetized kwargs joined``.
    For plain-Protocol-implementing objects without a ``__dict__`` we can
    introspect, fall back to ``name``.
    """
    fields = getattr(strategy, "__dataclass_fields__", None)
    if fields is None:
        return strategy.name
    kw_pairs = sorted(
        (f, getattr(strategy, f))
        for f in fields
        if f != "name"
    )
    if not kw_pairs:
        return strategy.name
    return f"{strategy.name}/" + ",".join(f"{k}={v!r}" for k, v in kw_pairs)
```

Add to the per-row dict ahead of `variant`:

```python
row: dict[str, object] = {
    "text_id": text_id,
    "strategy_id": _strategy_id_for(strategy),
    "variant": strategy.name,
    "transformed_text": transformed,
}
```

`base_cols` gains `"strategy_id"` ahead of `"variant"`.

**Tests** (`tests/test_sweep.py`):

- Two `DelimitVariant` instances with different `delimiter` kwargs share `variant == "delimit"` but have distinct `strategy_id` (e.g., `"delimit/delimiter='<<',end='>>'"` vs `"delimit/delimiter='[[',end=']]'"`).
- Same for `ZeroWidthSpaceInjection(ratio=0.0)` vs `ZeroWidthSpaceInjection(ratio=1.0)`.
- A plain-Protocol-implementing user class (no `__dataclass_fields__`) → `strategy_id == name`.
- `make_spec_name`-style argument-order invariance (alphabetized kwargs).
- A regression test using `df.groupby("strategy_id")` to confirm the column distinguishes configurations.

**Part 2: reject duplicate `strategy_id`.** Before building rows, walk the `strategies` list once and assert no two strategies produce the same `strategy_id`. If a duplicate is found, raise:

```python
raise ValueError(
    f"sweep(): duplicate strategy_id {dup_id!r} at index {i} "
    f"(previously at index {seen[dup_id]}); each strategy must produce a "
    f"unique strategy_id. If you want two configurations of the same "
    f"dataclass in the same sweep, vary their kwargs so the canonical "
    f"identifier differs."
)
```

This mirrors `_validate_unique_spec_names` in `_scorecard.py` (per R6-B). Style invariant 4 (Mapping containers reject duplicate keys; row containers carry a stable disambiguator AND reject duplicates IN THAT disambiguator).

**Tests** (`tests/test_sweep.py`):

- Two `DelimitVariant` instances with different `delimiter` kwargs share `variant == "delimit"` but have distinct `strategy_id` → sweep succeeds; `df.groupby("strategy_id")` distinguishes them.
- Two `DelimitVariant` instances with IDENTICAL kwargs → `ValueError("duplicate strategy_id 'delimit/...' at index 1")`.
- Two `ZeroWidthSpaceInjection(ratio=0.0)` vs `ZeroWidthSpaceInjection(ratio=1.0)` → distinct `strategy_id` (regression test for ratio differentiation).
- A plain-Protocol-implementing user class (no `__dataclass_fields__`) → `strategy_id == name`; two such instances with the same name → ValueError (correct rejection).
- `make_spec_name`-style argument-order invariance verified.
- Regression test using `df.groupby("strategy_id")` to confirm the column distinguishes configurations cleanly.

**Public-API impact**: additive schema expansion + new ValueError raise. Callers indexing by name keep working; callers indexing by position must re-check column offsets. Callers passing the same configured dataclass instance twice break (which is the right behavior — no methodology-honest reason to do that).

### 5J. `sweep()` scorer output shape validation (Decision R7-C — Round 7 Codex R7-F3)

Edit `src/eval_toolkit/_sweep.py:151-176`. After each `np.asarray(scorer.predict_proba(...))` call, validate shape:

```python
def _validate_scorer_output(scores: np.ndarray, expected_n: int, *, label: str) -> None:
    if scores.shape != (expected_n,):
        raise ValueError(
            f"sweep(): scorer.predict_proba({label}) returned shape "
            f"{scores.shape}; expected ({expected_n},). The Scorer Protocol "
            f"requires one float per input row."
        )
```

Two call sites: the `original_scores` batch and each per-strategy `transformed_scores` batch. Per-strategy label includes the `strategy.name` so the failure message tells the caller which strategy's scorer call misfired.

**Tests** (`tests/test_sweep.py`):

- Overlong 1-D (`scorer returns len(texts)+1` scores) → `ValueError` matching expected shape message.
- Short 1-D → `ValueError`.
- `(n, 2)` matrix → `ValueError`.
- Existing scorer-cardinality-OK tests still pass (regression-guard).

### 5K. Documentation polish (Round 7 Gemini observations)

Single small commit; non-breaking. Includes:

- **`SynonymSubstitution` docstring** (`src/eval_toolkit/adversarial.py`) — add a `Notes` section calling out the hardcoded `_SYNONYMS` whitelist (6 entries: `ignore`, `instructions`, `system`, `secret`, `send`, `all`). Note that the transform is a no-op on inputs without whitelist words; this is intentional (preserves semantics) but easy to be surprised by.
- **`Scorecard.to_pandas()` docstring** — add a `Notes` section documenting the pandas dtype coercion behavior (int + NaN → `float64` for the `n_resamples` column) per Decision R6-C tradeoff. Downstream consumers expecting strict `Int64` dtype will need to cast explicitly.

### 5L. Makefile pre-push target hardening (Round 7 Gemini §4 + v0.47 Sub-PR 7 incident + style invariant 5)

Add a `make pre-push` (or `make ci-mirror`) target that runs ALL THREE executable doc surfaces per style invariant 5 — preventing the silent path-override that surfaced 40 Sybil failures on v0.47 Sub-PR 7 (see `[[feedback_sybil_python_blocks]]` + `[[feedback_degradation_layer_removal_hazard]]` memories).

```makefile
.PHONY: pre-push
pre-push:
	# Surface 1: Sybil + tests/. NO positional path arg — testpaths includes
	# tests/ + README.md + docs/source/.
	uv run pytest --no-cov -q --ignore=tests/benchmarks
	# Surface 2: MyST-NB example notebooks via sphinx-build. After R7-A lands
	# (nb_execution_raise_on_error = True in conf.py), this exits non-zero on
	# notebook execution errors.
	uv run sphinx-build -b html -n docs/source/ docs/build/html/
	# Surface 3: in-source docstring examples. These are NOT covered by the
	# Sybil collection (different pattern) and have a separate failure mode
	# (stale docstring examples drift from API changes — see §5M postmortem).
	uv run pytest --doctest-modules src/eval_toolkit/ --no-cov -q
```

The three surfaces have non-overlapping coverage. Sybil tests `.md` fences in `tests`/`README.md`/`docs/source/{methodology,migration,extending,...}`. MyST-NB tests `docs/source/examples/*.md` `{code-cell}` blocks. `--doctest-modules` tests `>>> ...` examples inside Python docstrings in `src/`. Round 7 R7-F1 caught surface 2; the v0.47 incident caught surface 1; surface 3 is currently unaudited (§5M audits it).

### 5M. In-source docstring drift audit (audit-as-seed extension of R7-F1)

Style invariant 5 demands all three doc-execution surfaces stay green. Sub-PR 7 + §5G cover surfaces 1 + 2; this is the surface-3 audit.

**Procedure:**

1. Run `pytest --doctest-modules src/eval_toolkit/ --no-cov -q` against the v0.47.0 state (current `main`).
2. For each failure, classify:
   - **Stale top-level-scalar usage** (`>>> from eval_toolkit import pr_auc` in a docstring) → migrate to `from eval_toolkit.metrics import pr_auc` OR rewrite the example to use `scorecard()` if the docstring is on a high-level surface (invariant 7).
   - **Stale module-level-sweep usage** (`>>> from eval_toolkit.adversarial import sweep`) → migrate to the top-level `sweep()`.
   - **Stale namespace usage** (`>>> spotlighting.delimit(...)` / `>>> character_injection.zero_width_space(...)`) → rewrite to dataclass + functional API.
   - **Other drift** (e.g., examples that reference the old `paired=True` kwarg removed in v0.34) → fix to current state.
3. After every fix, re-run the doctest collection until it exits clean.

**Hypothesis:** the same mechanism that left 40 stale Sybil fences + 6 stale MyST-NB notebooks pre-v0.47-removal will have left N stale in-source docstring examples. N is unknown until the audit runs; rough expectation 5–20 based on the size of the corpus and the fact that the v0.46 shim was hiding the failures.

**Output:** one migration commit (`docs(src): migrate in-source docstring examples to v0.47 API`) sized by what the audit surfaces.

### 5N. Cross-API shape-validation consistency sweep (style invariants 1 + 3)

R7-F3 surfaced that `sweep()` skipped a shape check `scorecard()` would have done (via `_validate_scorecard_inputs`). Style invariants 1 (no silent failures) + 3 (API-level errors, not low-level exceptions) demand consistency across every public-API surface.

**Audit targets** (each gets a quick verification + a tightening commit if needed):

- **`metrics_at_threshold(y, s, threshold)`** — already on v0.48 §5A polish list for key normalization; while there, verify the input-validation pattern matches `_validate_scorecard_inputs`.
- **`paired_bootstrap_op_point_diff(val_y, val_s, test_y, test_s, ...)`** — Round 5 F6e flagged the `val_y is test_y` silent overlap; §5E-prep already schedules the defensive guard. Verify the rest of the input-validation matches scorecard.
- **`bootstrap_metric_from_predictions`** — analysis-layer public API; reuses bootstrap_ci internals; verify no low-level numpy errors escape.
- **`metrics.py` public functions called via submodule path** (`pr_auc`, `roc_auc`, `brier_score`, `expected_calibration_error*`) — internal API per ADR 0002 but still consumer-callable; verify each validates input shape rather than relying on sklearn's lower-level errors.
- **`fit_*_binary` / `fit_*_calibrator`** (calibration submodule) — the v0.40+ calibrator family. Verify input validation + return-shape contract.

**Style-coherence target:** every public API surface that accepts array-typed inputs (a) validates `.shape` + finite-ness + non-emptiness at the boundary, (b) raises `ValueError` with a message that names the offending kwarg + the expected/actual shapes, (c) never lets a low-level numpy/sklearn/list-index error escape to the caller. The `_validate_scorecard_inputs` function is the reference pattern.

**Output:** zero or more small tightening commits per audit target. Likely shape: each commit adds a `_validate_*_inputs` helper + a regression test that pins the new boundary error. None of these should be design changes — they're closing inconsistencies the v0.46/v0.47 surface evolution surfaced.

### v0.48.0 release

**Scope confirmation** (Q6 exploring-options round, 2026-05-21): single v0.48 release covering all 8 sub-PRs (§5A–§5N inclusive — see structure below). Per `[[feedback_staggered_breaking_releases]]` the default is one cleanup per minor; v0.48 is the "polish + audit-driven tightening before v1.0" thematic release. Estimated calendar: ~3–4 weeks of release work (was 2–3 weeks pre-Round-7; the audit-as-seed extensions §5M + §5N add ~1 week). Round 8 audit STOP-GATE catches anything missed.

**Sub-PR structure** (v0.48 release branch will collect these in roughly this order, then a single release commit):
- §5A — `metrics_at_threshold` key normalization (BREAKING — original v0.48 scope)
- §5B — `BootstrapCI.to_dict()` rewrite (BREAKING — original v0.48 scope)
- §5C — Lazy-extras error message audit (non-breaking — original v0.48 scope)
- §5D — Docstring example sweep (non-breaking — original v0.48 scope; ALSO see §5M which extends this)
- §5E + §5E-prep — ADR 0001 (flat-module) + Round 5 packet-drift fixes (cv_clt_ci docstring, parallelism.md, testing.md, calibration.md, bootstrap.md `val_y is test_y` + defensive guard, DeLong docs, CostSensitiveSelector framing)
- §5F — ADR 0003 finalized
- §5G — MyST-NB notebooks + full module-docstring sweep + protocols.md autosummary + roadmap wording (Round 7 R7-F1; Q2 locked full scope)
- §5H — `nb_execution_raise_on_error = True` wired into `docs/source/conf.py` (Decision R7-A)
- §5I — `sweep()` `strategy_id` column + reject duplicate `strategy_id` (Decision R7-B option C; Q1 locked)
- §5J — `sweep()` scorer output shape validation (Decision R7-C)
- §5K — Documentation polish (SynonymSubstitution whitelist + R6-C dtype note)
- §5L — `make pre-push` target running all 3 doc execution surfaces (Sub-PR 7 incident + style invariant 5)
- §5M — In-source docstring drift audit (audit-as-seed; Q5 locked separate sub-PR)
- §5N — Cross-API shape-validation consistency sweep (audit-as-seed; Q4 locked comprehensive scope)

**Release coordination**:
- `make release-prep VERSION=0.48.0`.
- CHANGELOG with **BREAKING CHANGES** for key renames + `BootstrapCI.to_dict()` + `sweep()` schema (now carries `strategy_id` + raises on bad scorer shape per R7-B/R7-C). Treat R7-B's `strategy_id` addition as ADDITIVE in the strict sense (no removal; column count grows by 1) but call it out in **CHANGED** since callers indexing the DataFrame by column position must re-check offsets. Reject-duplicate-strategy_id is the new BREAKING contract; document in BREAKING CHANGES.
- **Add `docs/source/migration/v0.48.md`** per existing pattern; document the `metrics_at_threshold` key renames + `BootstrapCI.to_dict()` shape change + `sweep()` `strategy_id` column addition + reject-duplicate-strategy_id contract + `sweep()` scorer-shape `ValueError` with before/after examples.
- **Update `docs/source/audit_findings.md`** Round 7 entries: mark R7-F1 / R7-F2 / R7-F3 as RESOLVED in v0.48 with disposition pointing at §5G–§5J. Update §1 (Decision Y references) to record that Round 7 STOP-GATE closed via this release.
- Tag, publish, rolling-bump consumer → v0.48. Observe ≥1 cycle. **This is the last consumer cycle before v1.0.** **Round 8 audit STOP-GATE** (Decision Y.2; 7-day timeout) before `v1.0.0` tag opens.

---

## Gate 3 parallel track — internal model-assisted cross-review (runs throughout)

**Decision O + Audit F7 honesty framing** (user-directed): Gate 3 is satisfied by **three independent reviews from the author's environment** — manual review by the author + Codex independent report + Gemini independent report. This is **NOT** equivalent to external academic peer review. ADR 0003 documents the framing plainly so future maintainers understand exactly what evidence Gate 3 actually produced.

**What this process catches and does not catch** (from Round 5 evidence):
- **Catches well**: plan/code contradictions; unstated assumptions; references to symbols that don't exist; doc-code drift; load-bearing instruction errors in implementation directives; mathematical claims that don't match implementation; public-API status contradictions. Round 5 demonstrated all of these — Codex + Gemini together surfaced 7+ verified-real findings before any v0.46 code shipped.
- **Catches less reliably**: methodological judgments that depend on domain expertise outside the model's training corpus; deep statistical correctness on novel methods; whether the chosen methodology serves the practitioner's actual decision-making need. For these, the consumer ledger (`decisions/upstream_issues.md` in `prompt-injection-detection-submission`) + the 16-chapter methodology curriculum carry the load — and even those are author-authored.
- **Does NOT substitute for**: external accountability. There is no third party who will be embarrassed if v1.0 turns out to have a methodology bug.

**Three reviewers:**

1. **Manual review by author** — the author reads `docs/source/methodology/` (16 chapters) + new feature pages (`scorecard.md`, `sweep.md`, `stacking.md`, ADRs 0001/0002/0003) with a critic's eye. Author is NOT external; this is the weakest of the three reviewers but is still the highest-context one.
2. **Codex independent report** — provide methodology docs + plan + relevant source files; ask for a methodology-focused review identifying gaps, contradictions, unstated assumptions, calibration / bootstrap / CI issues. OpenAI-trained reasoning surfaces things Anthropic-trained reasoning may miss.
3. **Gemini independent report** — same packet, different model. Google-trained reasoning surfaces things both Anthropic and OpenAI training may miss.

**Process** (formal stop-gates per Decision Y.2 — three audit gates between minors, 7-day timeout each):

1. **Round 5 (done, 2026-05-21)**: Codex + Gemini ran first reports against v0.44 state + the v1.0 plan. Findings integrated into this plan (see Round 5 overview near top). Ledger entries at `docs/source/audit_findings.md` (per Decision Z).
2. **Round 6 (post-v0.46 ship) — STOP-GATE before v0.47 release branch opens**: re-run Codex + Gemini against the v0.46 state. **7-day timeout**: if the audit doesn't complete within 7 days of v0.46 tag, work on v0.47 may begin; findings that land later are triaged as roll-forward or v0.46.1 hotfix per Decision Q.
3. **Round 7 (post-v0.47 ship) — STOP-GATE before v0.48 release branch opens**: re-run for the v0.47 sweep + Protocol consolidation. Same 7-day timeout.
4. **Round 8 (post-v0.48 ship) — STOP-GATE before v1.0 tag**: final Codex + Gemini pass against the complete pre-v1.0 packet. All packet-drift fixes (§5E-prep) merged before this read. Same 7-day timeout. **This is the gate the v1.0 release waits on**.
5. **Triage convention**: any reviewer-flagged blocker (any of the three) becomes a `p1-gate3`-labelled GitHub issue + a row in `audit_findings.md`. Must close (or be explicitly accepted with rationale in the ledger) before the next minor begins.
6. **Round-N "skip" hints**: each new audit prompt cites the open items already in the v0.48 backlog so reviewers don't waste cycles re-flagging known drift (§5E-prep, see `gate3-audit-prompt.md` "Known issues" section).

**Escalation path** (if Round 5–7 produce findings that require domain judgment beyond model capability): consult a human reviewer for the specific narrow question. Don't require a full-curriculum external read; do require a human signoff on any methodology claim that surfaces as "models disagree" or "models flag uncertainty."

**ADR 0003 (drafted at v0.48)** documents this redefinition explicitly per **Decision O** (revised). Future maintainers can read the ADR and understand: Gate 3 at v1.0 was internal model-assisted cross-review with documented limitations, not external academic review.

---

## Step 5 — v1.0.0 (Stability commitment, no new code)

Prerequisites — all must be GREEN:

- **Gate 1**: consumer running v0.48 for ≥1 review cycle without breakage.
- **Gate 2**: Protocol shapes survived v0.43–v0.48 without method-signature changes. Reverify: `git diff v0.42.0..HEAD -- src/eval_toolkit/protocols.py` shows only additions.
- **Gate 3**: peer review complete (or fallback ADR accepted).
- **Gate 4**: already MET (v0.41).
- **Post-bump audit**: `tests/golden/public_api/snapshot.json` reviewed.

### Pre-tag work

1. **Finalize ADRs**: 0001 (flat-module) and 0002 (scorecard-primary) — both already drafted in v0.48 / v0.46 prep; this is a content-review pass.
2. **Update `docs/source/roadmap.md`**: mark all 4 gates MET; refresh "Currently shipped" header to v1.0.0; clear tracked-candidates list (all closed at v1.0); populate v1.x candidate list (seed with deferred audit items: `_EXPORTS` curation, Protocol mutability docs, docstring example freshness; plus any new items surfaced in Gate 3 review).
3. **Verify v1-prelude evidence Protocol stability**: `git diff v0.42.0..HEAD -- src/eval_toolkit/{evidence,claims,operating_points,manifest}.py` shows only additive changes. If any Protocol shape changed, document in ADR or address pre-tag.
4. **Document canonical schema versions**: in roadmap or new ADR 0003, list the canonical schema version per artifact type (e.g., "v1.0 ships with `manifest.v3.json`, `ood_manifest.v1.json`, `results.v1.json`, `results_full.v1.json` as canonical"). Schema-version-frozen at v1.0; schema bumps require v2.0 of the package.
5. **Add `docs/source/migration/v1.0.md`** — a meta-migration guide that summarizes the v0.46/v0.47/v0.48 changes for any consumer jumping directly from v0.45 → v1.0.
6. `make release-prep VERSION=1.0.0`.
7. **CHANGELOG entry**: `release: v1.0.0 — stability commitment; all v1.0 gates closed; API surface frozen modulo SemVer-major bumps`. No code-content entries (v1.0 is content-identical to v0.48 modulo the version bump + roadmap edits + ADR finalization).
8. Tag `v1.0.0`. Publish. Final consumer rolling-bump → v1.0.0.

---

## Critical files

Reuse the full list from [[i-want-to-systmetatically-piped-feigenbaum]] §234–248. **New entries specific to this plan**:

- `src/eval_toolkit/scorecard.py` — new module (Step 3A).
- `src/eval_toolkit/sweep.py` — new module (Step 4A).
- `src/eval_toolkit/metrics.py:415–470` — `metrics_at_threshold` key normalization (Step 5A).
- `src/eval_toolkit/bootstrap.py:122–130` — `BootstrapCI.to_dict()` rewrite (Step 5B).
- `src/eval_toolkit/preprocessing.py:187–195` — `PairedBootstrapCI.to_dict()` + likely relocation to `bootstrap.py` (Step 5B).
- `src/eval_toolkit/adversarial.py:118–137` + `:458` — Protocol unification + `CharacterInjectionSweep` removal (Step 4).
- `src/eval_toolkit/preprocessing.py:175–195` — `SpotlightingSweep` removal (Step 4).
- `src/eval_toolkit/__init__.py:_EXPORTS` — scalar removal (Step 3B), `scorecard` family additions (Step 3A), `sweep` addition (Step 4A), sweep-class removals (Step 4B).
- `tests/golden/public_api/snapshot.json` — large diffs in v0.46, v0.47, v0.48; review each carefully.
- `docs/source/scorecard.md`, `docs/source/sweep.md` — new myst-nb pages.
- `docs/source/methodology/` — Gate 3 reviewer packet.
- `docs/source/adr/0001-flat-module-layout.md` — Step 5E.
- `docs/source/adr/0002-scorecard-as-primary-metric-surface.md` — Step 3C.

## Quality bar

Reuse the per-PR checklist from [[i-want-to-systmetatically-piped-feigenbaum]] §252–268. **Additions for each breaking release**:

- **Release-branch workflow** (Decision P): use `release/v0.46`, `release/v0.47`, `release/v0.48` for collecting sub-PRs; final release commit on the branch merges to main + tags.
- **Consumer dry-run gate before tag**: do not merge `release/vX.Y` to main until a dry-run consumer migration branch compiles AND passes the consumer's full test suite **against the release branch** (not against PyPI'd version). Catches API-shape bugs before they cement.
- **Doctest sweep before tag**: `pytest --doctest-modules src/eval_toolkit/` must pass — old examples updated to current API shape.
- **`**BREAKING CHANGES**` CHANGELOG section** with explicit migration snippets for every removed/renamed symbol.
- **Snapshot review**: manually diff `tests/golden/public_api/snapshot.json` against previous tag; confirm no *accidental* removals or additions.

### Semantic stop-gates (Audit Round 5 — Codex §5.4)

The release-discipline mechanics in this plan (staggered minors, release branches, dry-run gates, hotfix policy) are stronger than the *semantic completeness* of the new public contracts. To prevent semantic holes from leaking into v1.0, each breaking minor has a stop-gate that must close BEFORE its release branch can merge to main:

**Before v0.46 (scorecard) release-branch merge:**
- [ ] `MetricSpec` Protocol shape is final + matches Decision R (threshold-free specs only at v0.46; no `f1`/`accuracy`/`precision`/`recall` in `metric_specs` namespace).
- [ ] `MetricResult` shape is final + matches Decision S (status vocabulary, value-can-be-None).
- [ ] Single-class slice tests pass + per-metric-error-isolation tests pass.
- [ ] `__getattr__` deprecation branch is EXTENDED into the existing lazy resolver (not replacing it); `tests/test_public_api.py` still passes for all non-deprecated names.
- [ ] ADR 0002 drafted, captures threshold-free framing + `MetricState` reuse decision + submodule-internals-not-frozen wording (Decision C reconciled with Decision M).
- [ ] Consumer dry-run on `release/v0.46` branch (NOT on PyPI): consumer's full test suite passes against the release-branch eval-toolkit.

**Before v0.47 (sweep + advanced-6 + cleanup) release-branch merge:**
- [ ] `TextTransform` Protocol shape is final + the 3 preprocessing dataclasses (`DelimitVariant`, `DatamarkVariant`, `EncodeVariant`) exist and satisfy it.
- [ ] `sweep()` neutral-transform path produces identical output to the current `preprocessing.sweep` and `adversarial.sweep` neutral subsets — parity test passes.
- [ ] `sweep()` attack-scoring path requires explicit `attack_threshold` kwarg; no default-0.5 magic.
- [ ] All 12 character_injection techniques (6 core + 6 advanced) satisfy `TextTransform` structurally; adversarial.py `__all__` grows by exactly 6.
- [ ] `__getattr__` deprecation branch deleted (only the BEGIN/END TRANSITIONAL block); base resolver + `__all__` derivation + `__dir__` unchanged.
- [ ] Consumer dry-run on `release/v0.47` branch.

**Before v0.48 (polish + ADRs) release-branch merge:**
- [ ] `metrics_at_threshold` key normalization complete; regression test pins exact dict-key membership.
- [ ] `BootstrapCI.to_dict()` rewrite ships with regression test for non-default `confidence`.
- [ ] All 7 packet-drift fixes from §5E-prep complete (cv_clt_ci docstring, parallelism.md, testing.md, calibration.md, bootstrap.md leakage example + the defensive `val_y is test_y` guard in `paired_bootstrap_op_point_diff`, DeLong docs update, CostSensitiveSelector docstring warning).
- [ ] ADRs 0001 (flat-module) + 0003 (stability contract + Gate 3 governance) drafted.
- [ ] `pytest --doctest-modules src/eval_toolkit/` passes — no stale examples.
- [ ] Consumer dry-run on `release/v0.48` branch.

**Before v1.0.0 tag:**
- [ ] Gate 1 — consumer running v0.48 for ≥1 review cycle without blocker (per Decision Q definition).
- [ ] Gate 2 — `git diff v0.42.0..HEAD -- src/eval_toolkit/protocols.py src/eval_toolkit/evidence.py src/eval_toolkit/claims.py src/eval_toolkit/operating_points.py src/eval_toolkit/manifest.py` shows only additive changes. Any Protocol-shape edit must be either reverted or explicitly accepted as a Gate-2 regression with ADR.
- [ ] Gate 3 — Round 8 Codex + Gemini reports against the v0.48 packet completed (per Decision Y.2; 7-day window); all reviewer-flagged blockers closed or explicitly accepted with rationale in `docs/source/audit_findings.md`.
- [ ] Gate 4 — already MET (v0.41).
- [ ] DeLong disposition resolved per Decision U (keep public, docs aligned in `methodology/comparison.md`, `reading_list.md`, `roadmap.md`).
- [ ] Public-API snapshot diff reviewed across all three breaking releases (cumulative).
- [ ] No `_DEPRECATED_SCALARS` set or transitional branch remains in `__init__.py`.
- [ ] `docs/source/audit_findings.md` ledger lists Rounds 5–8 with disposition for every blocker-severity finding.

### Hotfix policy (Decision Q)

If a tagged release reveals a bug during consumer rolling-bump or observation cycle:

| Bug class | Examples | Response |
|---|---|---|
| **Blocker** | pipeline breakage; wrong API shape (e.g., `Scorecard` returns wrong type); silent data corruption; security/correctness regression | Branch `release/vX.Y.1`; single fix PR; release commit; tag; publish; consumer bump; observe |
| **Non-blocker** | cosmetic; docstring; error-message wording; perf without correctness impact; unhit edge case | File issue; add to next minor's `release/vX.Y+1` branch; CHANGELOG note under next minor's `### Fixed` section |

Document the disposition (hotfix vs roll-forward) in the issue itself so the post-mortem is preserved.

## Verification (end-to-end per release tag)

Same template as [[i-want-to-systmetatically-piped-feigenbaum]] §272–308. Tag-specific smokes:

```bash
# v0.46 smoke: scorecard end-to-end (dict subscript) + DeprecationWarning shim
# Note: TextTransform Protocol does NOT exist yet at v0.46 — introduced at v0.47.
uv run --with eval-toolkit==0.46.0 python -c "
from eval_toolkit import scorecard, metric_specs as ms
import eval_toolkit, numpy as np, warnings

rng = np.random.default_rng(0)
y_true = rng.integers(0, 2, 500)
y_score = rng.random(500)

# Primary path: scorecard with mixed singleton + factory specs (Decision R: threshold-free only)
r = scorecard(y_true, y_score,
              metrics=[ms.pr_auc, ms.brier, ms.ece(n_bins=15)],
              bootstrap=True, n_resamples=200, seed=0)
assert r['pr_auc'].status == 'ok'
assert r['pr_auc'].value is not None
assert r['pr_auc'].ci is not None
assert r['ece_n_bins_15'].status == 'ok'
assert ms.pr_auc is ms.pr_auc                # singleton identity
assert ms.ece(n_bins=15) is ms.ece(n_bins=15)  # LRU-cached factory

# Mapping behavior:
assert 'pr_auc' in r
assert len(list(r.items())) == 3

# Decision S: single-class slice yields status='skipped', not a raise
r_sc = scorecard(np.zeros(100, dtype=int), rng.random(100),
                 metrics=[ms.pr_auc, ms.brier], bootstrap=False)
assert r_sc['pr_auc'].status == 'skipped'
assert r_sc['pr_auc'].value is None
assert r_sc['pr_auc'].reason  # non-empty explanation
assert r_sc['brier'].status == 'ok'  # Brier is defined on single-class
assert r_sc['brier'].value is not None

# Decision R verification: threshold-dependent specs are NOT in metric_specs at v0.46
import pytest
with pytest.raises(AttributeError):
    _ = ms.f1
with pytest.raises(AttributeError):
    _ = ms.accuracy

# DeprecationWarning shim (Decision L): root scalar still works at v0.46 with warning
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    v = eval_toolkit.pr_auc(y_true, y_score)  # type: ignore[attr-defined]
    assert any(issubclass(x.category, DeprecationWarning) for x in w)
    assert isinstance(v, float)

# Verify other root exports still lazy-resolve (Audit F4 — must not have broken __getattr__)
from eval_toolkit import BootstrapCI, MaxF1Selector  # arbitrary non-deprecated names
print('v0.46 ok')
"

# v0.47 smoke: sweep + class removal + shim deleted
uv run --with eval-toolkit==0.47.0 python -c "
from eval_toolkit import sweep, TextTransform
from eval_toolkit.adversarial import ZeroWidthSpaceInjection
df = sweep([ZeroWidthSpaceInjection()], ['hello'])
assert {'text_id', 'variant', 'transformed_text'}.issubset(df.columns)

# Confirm TextTransform Protocol satisfied structurally
assert isinstance(ZeroWidthSpaceInjection(), TextTransform)

# Shim deleted: deprecated names raise AttributeError, NOT DeprecationWarning
import eval_toolkit
try:
    _ = eval_toolkit.pr_auc
    raise AssertionError('shim should be deleted at v0.47')
except AttributeError:
    pass

# Sweep classes removed from public API
assert not hasattr(eval_toolkit, 'CharacterInjectionSweep')
assert not hasattr(eval_toolkit, 'SpotlightingSweep')
print('v0.47 ok')
"

# v0.48 smoke: BootstrapCI dict shape + metrics_at_threshold keys
uv run --with eval-toolkit==0.48.0 python -c "
from eval_toolkit.bootstrap import bootstrap_ci
ci = bootstrap_ci(lambda x: x.mean(), [1.,2.,3.,4.,5.], confidence=0.90)
d = ci.to_dict()
assert set(d) == {'point', 'low', 'high', 'confidence'}
assert d['confidence'] == 0.90
print('v0.48 ok')
"
```

## Risks & open questions

1. **Three consumer migration cycles** (v0.46, v0.47, v0.48) — calendar ~4–6 weeks (down from earlier 6–8 estimate after Q11 → 11.3 eliminated v0.45.1). Mitigation: each cycle is small; v0.46 has DeprecationWarning shim so consumer bump can precede migration; v0.47 and v0.48 are mostly internal-facing.
2. **Gate 3 lead time RESOLVED** — multi-model cross-review (user + Codex + Gemini) has days-not-weeks cycle time. Was the biggest unknown; now bounded.
3. **`scorecard()` design lock-in** — once shipped at v0.46, the surface is effectively frozen for v1.0. Mitigate via consumer dry-run gate (§Quality bar additions). If dry-run surfaces an awkward shape, iterate v0.46.1 before pushing to v0.47.
4. **Snapshot churn cumulative** — three breaking releases each regen the snapshot. Generate diffs manually before each commit. ([[feedback_public_api_snapshot_drift]])
5. **v0.45.0 cycle could uncover regression** — if so, v0.45.0.1 hotfix; patch number for advanced-6 shifts to v0.45.2. SemVer-patch versioning is cheap.
6. **Snapshot behavior with `__getattr__` shim** — `tests/test_public_api.py` snapshots `eval_toolkit.__all__` (verified via head of file); the `__getattr__` shim adds attributes that ARE NOT in `__all__`. So snapshot v0.46 won't include the deprecated names → no snapshot drift from the shim. The deprecation is purely runtime-discoverable (via `import eval_toolkit; eval_toolkit.pr_auc`), which is the right behavior. Audit candidate confirmed: `tests/test_public_api.py:1-30` reads `__all__`, not `dir()`.
7. **`Mapping` vs frozen-dataclass for `Scorecard`** — `Mapping[str, MetricResult]` is the contract; concrete impl can be `dataclass(frozen=True)` wrapping a `dict`, or `collections.abc.Mapping` subclass directly. Decide during implementation based on what makes `mypy --strict` happiest and what serializes cleanest. No user-visible difference.
8. **`metric_specs` factory caching memory** — LRU-caching `ms.ece(n_bins=N)` for arbitrary N could leak memory if a user generates thousands of variants. Set a reasonable `maxsize` (e.g., 128) on the factory cache; document the cap.
9. **SimpleNamespace removal (§4E) might be load-bearing for consumer** — `character_injection` and `spotlighting` SimpleNamespaces are documented as "function-style API from the upstream issue spec" in CHANGELOG v0.43/v0.44. Verify during v0.47 consumer dry-run that consumer doesn't use them; if it does, soft-deprecate at v0.47 + hard-remove at v0.48 instead.
10. **v1-prelude evidence core surface** — roadmap §"v1-prelude evidence core" lists operating points + RunManifest + claim gates as "the next stabilization step." These are already shipped (visible in `_EXPORTS`: `FittedOperatingPoint`, `OperatingPointSpec`, `ClaimReport`, `ClaimSpec`, `EvidenceGate`, `EvidenceAxis`, `GateResult`, `AggregateEvidence`, etc.). Pre-v1.0 verification step: confirm these have NOT had Protocol-level signature changes in v0.43/v0.44 (additive-only); if any did, that's a Gate 2 regression to address.
11. **JSON schema versioning** — `src/eval_toolkit/schemas/` has `manifest.v1.json`, `v2.json`, `v3.json`, plus `ood_manifest.v1.json`, `results.v1.json`, `results_full.v1.json`. The roadmap's "schemas/*.v1.json become canonical at v1.0" is simplified. Pre-v1.0 step: document which schema version is canonical per artifact type in ADR or roadmap; v1.0 freezes the current versions, NOT specifically the v1 versions.

## Out of scope for this plan

- Refactoring modules beyond what Steps 3–5 touch (every unrelated cleanup defers to v1.x).
- New v1.x features.
- Cross-repo work in `prompt-injection-detection-submission` beyond pin bumps + migrations.
- The deprecated `prompt-injection-v4` repo (historical; sibling-CI already removed in v0.43 leg).
- Adoption of new dependencies beyond the already-defined `[losses]` and `[probes]` extras.
- Audit candidate #7 (`_EXPORTS` curation), #9 (Protocol mutability docs) — deferred to v1.x.

---

## Stale-memory updates (post-implementation)

After v1.0 ships:

- [[project_etk_on_pypi]] — bump current version to 1.0.0, replace v0.43→v1.0 plan reference, note "single-consumer / breaking-OK era closed at v1.0; future major bumps require second-consumer review."
- Possibly delete or archive [[project_sdd_migration_pending]] if no longer relevant (verify before).
- Add a new feedback memory: **user prefers staggered breaking releases over bundled rc cycles** — surfaced in /exploring-options Q5 (Why: chose 5.3 against bundled-rc recommendation; How to apply: when planning multi-breaking releases, default to one-cleanup-per-minor not big-bang rc).
- Add a new feedback memory: **user substitutes multi-model cross-review (Codex + Gemini + manual) for external academic peer review on methodology-heavy projects** — surfaced in /exploring-options round 3 Q11 (Why: predictable cycle time and outside-eyes value from differing training corpora, without scheduling uncertainty; How to apply: when a project needs "outside eyes" methodology review and no specific human is required, propose multi-LLM cross-review as default Gate-3-style mechanism).
- Add a new feedback memory: **user invokes /exploring-options multiple times for high-stakes decisions** — four rounds of question-driven planning for the v1.0 plan; signals that pre-commit deliberation is welcomed for stability-commitment-level work. (How to apply: for similar high-stakes decisions, expect to re-enter exploration even after a "complete" round.)
- Add a new memory: **API design philosophy at v1.0** — single consumer made breaking cheap; second consumer would flip the calculus.
- Note: `src/eval_toolkit/_deprecated.py` is **deprecation infrastructure** (the `@deprecated` decorator), not a graveyard of deprecated functions. Currently unused in src; kept as v1.0 infrastructure for future deprecation cycles. Distinct from the v0.46 `__getattr__` shim (which uses a different mechanism for import-time deprecation).
- Add a new feedback memory: **Round 5 LLM cross-review caught 7+ verified-real plan/code issues before any v0.46 code shipped** — Codex (longer, structural) + Gemini (statistical-correctness-focused) had non-overlapping findings. (How to apply: when planning a stability-commitment release for Daisy, treat LLM cross-review as a load-bearing gate — but always verify findings against actual code before incorporating, since some claims are partial or context-dependent. Don't blindly accept; investigate.)
- Add a new feedback memory: **Round 6 LLM cross-review surfaced 11 v0.46 post-ship findings; 2 overlapped between Codex+Gemini, 9 were unique to one model**. The unique-to-one findings were as load-bearing as the overlapping ones (Codex's R6-F1 invalid-ECE-strategy was the most consequential of the round and Gemini didn't catch it; Gemini's R6-F3 to_pandas schema gap and R6-F5 broad-except were equally absent from Codex). (How to apply: do NOT use overlap as a confidence floor — single-reviewer findings can be just as critical. Verify each finding against code regardless of whether multiple models flagged it.)
- Add a new feedback memory: **Always run a runtime probe to verify shipped scorecard / contract behavior, not just static analysis** — Codex's Round 6 process explicitly noted "runtime probes confirmed" for R6-F1 (`metric_specs.ece(strategy="typo")` runtime test), R6-F3 (duplicate-name runtime test), R6-F4 (`seed=None` bit-for-bit equality test). Static code reading would have flagged the validation gap but the live probe locked in the wrong-key + ok-status combination, which made the BLOCKER severity argument airtight. (How to apply: when auditing shipped contract behavior — especially around `Literal` types, default arguments, error paths — always include a runtime probe, not just a code read.)
- Add a new feedback memory: **`__init__.py:__getattr__` is the public-API mechanism in eval-toolkit** — `_EXPORTS` dict → `__all__` → lazy resolver. Any plan that touches `__getattr__` must extend it, not replace it. The Round 5 audit caught this; the original plan would have shattered the package.
- Add a new feedback memory: **Single-author / single-consumer projects accumulate plan/doc drift naturally** — Round 5 audit found 7 verified gaps between plan, code, and methodology docs. (How to apply: before high-stakes releases, run a fresh ground-truth verification pass against source — the plan and docs both lag the code on a months-old project.)
- Add a new feedback memory: **Round 7 cross-review pattern: Codex 3 substantive findings, Gemini 0 — overlap was zero.** The most consequential finding (R7-F1 doc-migration boundary gap between Sybil-tested fences and MyST-NB-executed example notebooks) was Codex-only. Gemini's verdict "highly stable; safe to open v0.48" missed three real problems Codex's runtime probes confirmed. Reinforces the Round 6 pattern (non-overlapping findings; do not use overlap as a confidence floor). (How to apply: read both reviews independently. When verdicts diverge sharply — one model says "no findings", the other says 3 — assume the divergent one is signal until you verify against code yourself. Default trust toward the model that produced runtime probes over the model that produced executive summaries.)
- Already saved: [[feedback_sybil_python_blocks]] — extended in this session with the precise root cause (`pytest tests/` overrides `testpaths`; bare `pytest` collects all multi-root entries) + the Sub-PR 7 incident. Update the description to point at the v0.48 `make pre-push` target (§5L) once it lands.
- Already saved: [[feedback_degradation_layer_removal_hazard]] — created this session for the general pattern (removing a deprecation shim activates EVERY latent callsite). Round 7 R7-F1 is the second instance of the same pattern (MyST-NB-executed examples were a hidden surface the v0.46 shim was masking just like the Sybil fences). After v0.48 lands the §5G migration + §5H docs gate, add a postscript: "the pre-push matrix must cover ALL executable surfaces simultaneously — pytest (no path arg), sphinx-build (with nb_execution_raise_on_error), pytest --doctest-modules. Each surface has a different collection scope; ensuring all three are run was the lesson of Sub-PRs 6+7."
