# Plan — M1 Lane-1: attack-type-LODO harness (reconcile + full build + smoke)

**Created:** 2026-05-29 · **Branch:** `session/2026-05-26-adoption-and-research-ops` · **HEAD at start:** `93ba8ee`
**Governs:** ADR-052 · **Spec:** `docs/planning/attack-type-lodo-harness-spec.md` · **Validates:** the pre-modeling EDA arc (`experiments/eda/OOD_WALL_PREDICTION/`).

## Goal

Start M1's modeling step: build the attack-type-LODO detector harness that produces the per-test-attack-type
AUPRC drops the pre-registered **§6.5 OOD-wall falsification** (issue #2) is judged against — and first
**reconcile** the stale `experiments/lane-1/` docs (a pre-ADR-052 reference-scorer study, currently blocked)
to the ADR-052 framing so the repo stops holding two contradictory conceptions of "Lane 1".

## Decisions Made (for posthoc analysis)

| # | Decision | Why | Alternative rejected |
|---|----------|-----|----------------------|
| 1 | Reconcile lane-1 docs **before** building | The two-conceptions desync decides what "Lane 1" *is* | Build first + note desync |
| 2 | Build the **full** harness (3 rungs × 3 folds × seed-loop), smoke-run only | Complete code now, GPU sweep when feasibility known | Skeleton-only; full sweep now |
| 3 | Code home = `experiments/attack-type-lodo/` (spec §6 path, **unedited**) | Clean planning(lane-1)/execution(attack-type-lodo) split; no new path-desync | Unify in lane-1/ + edit spec |
| 4 | `falsify_ood_wall.py` **write-gated** | Smoke/partial drops must never write a verdict into the pre-registered record | Run + write now; sandbox-only |
| 5 | Device-adaptive precision (bf16 if `is_bf16_supported()` else fp16) | RTX 2070 SUPER is Turing — no native bf16 matmul | Hardcode bf16 / hardcode fp16 |
| 6 | Smoke = cheap + 1 LoRA pass **+ local-feasibility probe** | Measure the *real* local wall-clock to decide local-vs-cloud | Cheap-only |
| 7 | Reconcile reaches sibling cross-refs | Repo consistency | lane-1 docs only |
| 8 | **One repo write per turn + isolated read-back** | This session's tool feedback was unreliable; writes vanished — verify each | Trust success messages (failed) |
| 9 | 5-file split kept | User choice; cleaner modularity + per-file tests | 2-file / monolith |

## Assumptions
- Per-type N=5 → per-type drops are **diagnostic** (spec §5/§7); §6.5 is a tail contrast, not a correlation.
- Cheap rungs (TF-IDF, frozen-probe) are legitimate shortcut-learning detectors for H1; their real core-fold
  drops are real (non-headline) inputs — still write-gated (not a complete headline sweep).
- ModernBERT-base locally cached; no network for the smoke. No commit unless asked; PG1/V10 untouched.

## Steps
0. This doc. → 1. ✅ Reconcile `lane-1/{protocol,hypothesis}.md` (+ lane-4 cross-ref broadened; lane-2 ok as-is).
   → 2. Harness (`folds.py`, `detectors.py`, `metrics.py`, `harness.py`) in `experiments/attack-type-lodo/`
   + `library_imports.md` R29. → 3. `falsify_ood_wall.py` (write-gated). → 4. Tests (folds/falsify/metrics).
   → 5. Smoke + feasibility probe. → 6. Verify (ruff/mypy/pytest).

## Verified API facts (eval-toolkit 1.6.0, `.venv`) — CORRECTED 2026-05-29 from library source

> ⚠️ The block below replaces an earlier, **wrong** version of these facts (it claimed
> `scorecard(..., specs=, n_bootstrap=, bootstrap_seed=, ci_level=)` and
> `losses.RecallAtLowFPR(target_fpr=).compute()`). Both were lag-corrupted introspection
> from the paused session. The corrected signatures (read from `scorecards.py` /
> `thresholds.py` / `losses.py`) are authoritative; the code was built against them.

- **`scorecard(y_true, y_score, *, metrics: Sequence[MetricSpec], bootstrap=True, n_resamples=1000, confidence=0.95, rng=None) -> Scorecard`** (`scorecards.py:350`). NOT `specs=`/`n_bootstrap=`/`bootstrap_seed=`/`ci_level=`; no `sample_weight`.
- `Scorecard` = `Mapping[str, MetricResult]`; `MetricResult{value: float|None, status: "ok"|"skipped"|"error", reason, ci: BootstrapCI|None}`. CI is **`m.ci.ci_low`/`m.ci.ci_high`** (not `m.ci_low`); `value is None` unless `status=="ok"` (single-class slice → `"skipped"`, not raised). NaN CIs (BCa degeneracy) → persist as `None`.
- `metric_specs.{pr_auc,roc_auc,brier}` are singletons; `ece(n_bins=15)` → name `"ece_n_bins_15_strategy_uniform"`.
- **TPR@LowFPR = `thresholds.recall_at_fpr(y_true, y_score, target_fpr) -> RecallAtFprResult` (use `.recall`)** (`thresholds.py:745`). NOTE: `losses.RecallAtLowFPR` is a torch **training loss** (`nn.Module`, kwarg `fpr_target`, no `.compute()`) — NOT the reporting metric; the earlier note was wrong.
- Falsification stats = **scipy 1.17.1**: `permutation_test(..., permutation_type="independent", alternative="greater")`, `bootstrap(..., alternative="greater", method="percentile"|"BCa")` (one-sided CI lower bound via `alternative`), `kendalltau(variant="b")`. (eval_toolkit not used for the §6.5 test.)
- Loader returns a **dataclass**: `build_examples(*, root, contexts_per_attack=12, carriers=CARRIERS, seed=0) -> CarrierExamples` — use **`.frame`** (`bipia_carrier.py:123`; `run_prediction.py:78-79`). Add `experiments/eda/OOD_WALL_PREDICTION/` to `sys.path` first.
- Persistence helpers: `artifacts.write_json_strict(payload, path)` (arg order!), `provenance.capture_git_sha(repo_root)`.

## RESUME STATE (paused 2026-05-29) — authoritative

Paused at user request: **tool results lagged ~1–2 turns all session**, repeatedly causing action on stale
output. Resume in a clean session.

### Persisted + verified (DONE)
- `experiments/lane-1/protocol.md` — reconciled to ADR-052 attack-type-LODO (status: active). ✓
- `experiments/lane-1/hypothesis.md` — reconciled (H1 attack-type-generalization). ✓
- `docs/plans/active/lane1-attack-type-lodo_2026-05-29.md` — this doc. ✓
- `experiments/attack-type-lodo/folds.py` — imports OK (core/obfuscation/carrier folds + `carve_val_from_train` + `assert_source_disjoint`). ✓
- `experiments/attack-type-lodo/detectors.py` — compiles OK (tfidf/frozen/lora/full_ft rungs; device-adaptive precision). ✓

### TODO on resume (in order)
1. **FIX `experiments/attack-type-lodo/metrics.py` — currently BUGGY.** `scorecard()` does **not** accept
   `specs=`/`n_bootstrap=` (runtime `TypeError: unexpected keyword argument 'specs'`). The real signature is
   still unknown (all stdout introspection this session was lagged/garbled). **Get it from SOURCE first:**
   `grep -rl "def scorecard" .venv/lib/python*/site-packages/eval_toolkit/` → Read that file (NOT `_scorecard.py`
   — that path does not exist). Then rewrite metrics.py. Confirmed facts: `ScoreCard` is a Mapping name→float
   (`.to_dict()` / `.get()`); `RecallAtLowFPR(target_fpr=f).compute(y_true, y_score)` → float; `bootstrap_ci(estimator,
   *args, statistic=None, n_resamples=10000, confidence_level=0.95, method='percentile', random_state=None, axis=0, paired=False)`.
2. **Fix sibling cross-refs** (genuine stale "Lane 1 reference scorer" framing — confirmed): `lane-1b/protocol.md:21-22`,
   `lane-1b/hypothesis.md:65`, `lane-2/hypothesis.md:21`, `lane-3/protocol.md:21`, `lane-4/protocol.md:23`. Read-before-Edit each.
3. **Write** `harness.py`, `falsify_ood_wall.py` (write-gated), `tests/` (folds/falsify/metrics), then the smoke + local-feasibility probe; register eval_toolkit imports in `decisions/library_imports.md` (R29).

### Notes
- Everything above is **uncommitted** (unstaged); **no commit** made (commit-only-when-asked).
- Decisions locked (see table): code home `experiments/attack-type-lodo/`; falsify write-gated; device-adaptive precision; 5-file split; smoke + feasibility probe.
- Tasks #14–24 track the steps. Approved plan: `~/.claude/plans/use-the-following-to-rustling-adleman.md`.

## Status: BUILD COMPLETE 2026-05-29 (resumed clean session)

All RESUME-STATE TODOs landed + runtime-verified (CPU-safe scope per user decision D1):
- ✅ TODO#1 `metrics.py` fixed — real `scorecard(metrics=, bootstrap=, n_resamples=, rng=)`; `_cell` maps NaN→None; TPR@FPR via `thresholds.recall_at_fpr` (the earlier `losses.RecallAtLowFPR.compute()` was a non-existent API — a 3rd handoff-missed bug).
- ✅ TODO#1b `detectors.py:_val_pr_auc` had the **same** `scorecard(specs=)` bug (handoff missed it) — fixed.
- ✅ TODO#2 sibling cross-refs (D2): re-read all 5 lines — **none mislabel Lane 1's study** (all are detector-pool baseline tags); no edits needed (the prior "confirmed stale" was a lag-window artifact).
- ✅ TODO#3 `harness.py` (seeds×folds×rungs → per-`(rung,fold,seed)` parquet + metrics JSON w/ per-type drops + `MANIFEST.yml`) and `falsify_ood_wall.py` (write-gated §6.5; scipy perm+bootstrap+kendall) written + smoke-proven.
- ✅ Tests: `tests/experiments/{folds,metrics,falsify}` — 21 unit tests pass. R29 registered in `library_imports.md`.
- ✅ **Data-integrity finding** (surfaced by the smoke, not the prior session): BIPIA `email` train/test share 11 clean contexts (spec §1's disjointness premise was false). Fixed in `folds.py` via `purge_train_context_overlap` (purge-from-train, user-confirmed) + hardened `assert_source_disjoint` to check underlying contexts cross-class.
- ✅ Verify: ruff clean, mypy --strict 0 errors (5 files), pytest `unit/smoke/contract` = 27 passed / 4 skipped.

**Deferred (D1, stable session):** the full ≥3-seed × 4-rung headline sweep + the write-gate-OPEN falsification verdict. **Uncommitted** (commit-only-when-asked).

## GPU LoRA feasibility probe — DONE 2026-05-30 (verdict: local capable, full sweep → cloud)

Ran the deferred probe after the user freed the `research-kb` rerank_server (PID 19442, 2.9 GB).
Probe script `/tmp/lora_probe_min.py` drives the **real** `LoRADetector` on the headline
`core_attack_type` fold, seed 0 (train=2038 / val=557 / test=2720).

**Measured (minimal config that fits the card — r=8, batch 2, max_len 256, 1 epoch, `expandable_segments`):**
- `t_fit` = **118.9 s** (1 model · 1 epoch) · `t_predict` = **39.9 s** (2720 rows) · **peak VRAM 1.37 GB**.
- **val AUPRC = 0.958** (score range 0.58–0.92) → the LoRA path trains correctly end-to-end on GPU and
  learns real signal (not a smoke stub). `dtype` selected = **`torch.bfloat16`**.
- (Authoritative source: `/tmp/lora_probe_result.json`, status `OK`.)

**Findings:**
1. **Spec config OOMs locally.** The first probe at near-spec (`batch 8`, r-grid {8,16}, max_len 512)
   died with `torch.OutOfMemoryError` *in the first training forward* — at the failure point only
   ~32 MiB was free: the GNOME desktop + Chrome/nautilus reclaimed the ~3.5 GB freed by stopping the
   daemon. An 8 GB card shared with a live desktop cannot hold ModernBERT-base at `batch 16 / max_len 512`.
2. **bf16 on Turing (spec assumption was wrong).** `torch.cuda.is_bf16_supported()` returns **True**
   on the RTX 2070 SUPER (capability 7.5; torch 2.12 emulates bf16), so `_select_device_dtype()` picks
   **bf16, not fp16**. The spec/plan's "Turing → fp16" premise (Decision 5) is factually incorrect here.
   Not a bug — the run succeeded in bf16 — but the harness comment + spec §4 should be corrected.
3. **Full-sweep extrapolation (forced batch 2, the only local-viable footprint):** per-model spec fit
   ≈ 118.9 s × 3 epochs × ~2× (256→512 seq) ≈ **~12 min/model**; LoRA `(rung,fold,seed)` = 2-rank grid
   ≈ ~25 min; full sweep `(lora+full_ft) × 3 folds × 3 seeds` ≈ **~6–8 h** of GPU wall-clock — and
   `full_ft` at spec batch/seq needs *more* memory than the LoRA that already OOM'd, so it is not even
   runnable locally at spec config. (Note: peak VRAM was only 1.37 GB at minimal config, but the OOM is
   driven by `batch 16 × max_len 512` activations — ~10–16× the minimal footprint — against a desktop
   that holds ~4 GB of the 8 GB card.)

**VERDICT → escalate the full headline sweep to gated cloud GPU** (pre-registered bail-out:
`hypothesis.md` bail-out criteria → **filed `decisions/contingency_unlock_1.md`**, ratified via
**ADR-014** the cost-driven slot — NOT ADR-039, which is the PromptShield SOTA-anchor *method*-expansion
gated on a <0.40-AUPRC research signal; this is an *infrastructure* unlock, separate per ADR-013
§Consequences. Budget classification base-vs-contingency PENDING: `make cost-report` does not exist yet,
so confirm from the spend ledger before drawing — it may fit base $250 with no contingency ADR at all).
Rationale: local is
*proven capable* (correct code, learns signal, 1.37 GB at minimal config) but *not viable* for the
headline sweep — spec config OOMs on the desktop-contended 8 GB card, and a ~6–8 h forced-batch-2 run
carries live OOM risk from desktop VRAM reclamation (already observed killing the batch-8 probe). A
24 GB+ cloud card runs `batch 16 / max_len 512` with no contention at ~3–5× throughput → the full sweep
completes reliably in ~1.5–3 h. The local probe has discharged its purpose: it measured the per-unit
cost and confirmed the GPU path is correct before any cloud spend.

**Probe artifacts (scratch, /tmp — not in repo):** `/tmp/lora_probe.py` (batch-8, OOM'd),
`/tmp/lora_probe_min.py` (minimal, OK), `/tmp/lora_probe_result.json` (the measured result above).
