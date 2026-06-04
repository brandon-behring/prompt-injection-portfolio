# Reproduction audit (2026-06) — all three LODO bootstrap verdicts re-derived

**Why.** Distrust of the older results → independently re-derive all three axes' bootstrap verdicts
on a tested, released upstream primitive (not the hand-rolled serial loops that produced them).
CPU-only re-aggregation of the on-disk predictions — **no paid re-runs**.

**What the audit also surfaced (the honest correction).** The first upstream attempt,
`cluster_bootstrap_ci` (DF-9, v1.7.0), is **single-block** — it cannot express the **seed-averaging**
all three estimators do *inside* the bootstrap (`Gx = val − mean_seed(test_roc)`). So it fit none of
the three sites — a mis-scope on the v1.7.0 PR. The corrected primitive,
**`stratified_cluster_bootstrap_ci` (DF-10, v1.8.0)** — a composite statistic reduced over several
independently-resampled cluster strata — is what these estimators actually need, and is what the
reproduction below consumes. `cluster_bootstrap_ci` is its single-stratum special case.

## Pre-stated rule (write-gate — fixed before any number was read)

1. **Point estimate must match the committed serial EXACTLY** — it is deterministic (`val − mean_seed`
   / the per-type AUPRC contrast on the persisted predictions; no bootstrap). The strong check.
2. **CI-low within MC noise** — on the genuinely-clustered folds, the new one-sided 95% CI-low agrees
   with the committed serial within **±0.02** (≫ the bootstrap MC SE; ≪ the 0.05 SESOI).
3. **Verdict / directional reading unchanged.**
4. **Any breach ⇒ a surfaced finding** (old-serial bug vs new-primitive bug vs scheme mismatch).

## Result — 3/3 axes reproduced, no breach

| axis | estimator | strata → combine | folds/rungs | point | CI-low Δ | conclusion |
|---|---|---|---|---|---|---|
| **dialect** (B2.3) | `Gx = val − mean_seed(ROC)` | `{seed}` → `val − mean_seed` | 8/8 (tfidf+frozen × 4) | **exact** | ≤ 0.0010 | walls persist/grow (directional) — unchanged |
| **carrier** (M2) | `G = mean_carrier(val − mean_seed(ROC))` | `{(carrier,seed)}` → carrier-mean gap | 3/3 (tfidf/frozen/**lora**) | **exact** | ≤ 0.0002 | **SMALL-THROUGHOUT** — unchanged |
| **§6.5** (attack-type) | `T = mean(AUPRC[bottom]) − mean(AUPRC[top])` | `{(type,seed)}` → top−bottom `T` | lora (the verdict) | **exact** | 0.0007 | **FALSIFIED** — unchanged |

Per-axis JSON: `dialect_reproduction.json`, `carrier_reproduction.json`,
`attack_type_6_5_reproduction.json`. The point estimates are bit-exact (the same predictions, the
same metric fn); every CI bound is within pure Monte-Carlo noise.

### Method notes (honest scope)

- **Point re-derivation is the rigorous check** — independent code path, the deterministic statistic;
  it caught nothing (all exact), which is the strong evidence the verdicts are sound.
- **CI cross-check** uses the committed serial as the baseline (the serial 10k-iter bootstrap is
  pathologically slow on the cluster=row folds — the very reason for the parallel primitive). It is
  run on the genuinely-clustered, low-power folds (dialect bipia/injecagent; all carrier; §6.5) where
  the cluster bootstrap is most distinct from a row bootstrap; cluster=row folds (dialect
  browsesafe/fujitsu) are covered by point-exact + identical scheme + the upstream-tested primitive.
- `n_jobs=1` (no cross-process pickling); `n_boot` 5 000–10 000 for the CI comparison (the point is
  `n_boot`-invariant). The new primitive's `n_jobs`-reproducibility is verified upstream (test suite).

## Reproduce

```bash
uv run python experiments/REPRODUCTION_2026-06/reproduce_dialect.py   # 8/8
uv run python experiments/REPRODUCTION_2026-06/reproduce_carrier.py   # 3/3 (incl. lora)
uv run python experiments/REPRODUCTION_2026-06/reproduce_6_5.py       # lora FALSIFIED
```

Reads the gitignored per-fold prediction parquets (`cross-family-transfer/B2_3_results/`,
`attack-type-lodo/results/`); requires `eval-toolkit>=1.8`.
