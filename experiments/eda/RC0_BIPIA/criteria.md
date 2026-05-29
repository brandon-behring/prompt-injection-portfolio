# RC0 — BIPIA attack-type-split adequacy: PRE-REGISTERED criteria

**Pre-registered:** 2026-05-28, **before any BIPIA data was loaded or inspected.**
**Attestation:** at the time of writing, no BIPIA attack strings, counts, or embeddings
have been observed. Thresholds below are committed in advance to prevent post-hoc
rationalization (the predecessor prototype's root failure). Any later change requires a
written rationale appended to this file (not a silent edit).

## Question

Is BIPIA's native disjoint attack-type train/test split adequate to support the ADR-052
attack-type-generalization study (train on some indirect-injection *types* → test on
held-out *types*)? This is a **go/no-go** gate; an honest "inadequate" is an acceptable
outcome.

## Criteria (measured against BIPIA `text` attack strings; code split reported secondarily)

| # | Criterion | Method | PASS threshold |
|---|-----------|--------|----------------|
| i | **Disjoint attack-type split** | Parse train/test attack-type sets from the BIPIA benchmark files; intersect | ≤ 1 overlapping type (drop the known "Language Translation" overlap); ≥ 10 types per side |
| ii | **Per-type sample size** | Count attack strings per attack_type | median per-type N ≥ 5; no train-type with N < 3 |
| iii | **Within-type semantic diversity** (memorization floor) | MiniLM (`make_minilm_embedder`) embeddings; mean pairwise cosine within each type | **mean within-type cosine < 0.95** (≥ 0.95 ⇒ near-paraphrase ⇒ memorization risk); report per-type, flag any type ≥ 0.98 |
| iv | **Train-vs-test type populations distinct** | Centroid cosine between pooled-train vs pooled-test embeddings; optional proxy-A-distance | descriptive — report; expect distinct (split is by type). Not a hard gate, but a near-1.0 centroid cosine is a red flag |
| v | **Benign-FPR control feasible** | Load NotInject (`leolee99/NotInject`, already cached); confirm loadable + auditable via `audit_dataset` | loads + yields ≥ 1 usable benign split |

## Decision rule

- **PASS** (proceed to the broad survey + the ADR-052 study) iff **i, ii, iii, v all hold**.
  (iv is descriptive context, not a gate.)
- **FAIL** (esp. iii — within-type near-duplication) ⇒ the type-LODO study is at memorization
  risk on real data; redesign required: diversity augmentation via synthesis, an alternative
  disjoint-split corpus (WAInjectBench-class), or a descriptive-only framing. Record which.

## Honesty notes (pre-committed)

- BIPIA's attack-string diversity is known-small (~5/type, ~75/split) — criterion iii is the
  crux and the most likely to fail; that is an *expected, acceptable* finding if it occurs.
- The WebQA/Summarization *context* data is redistribution-restricted and **not needed** for
  RC0 (RC0 is about attack-string structure, not full eval instances).
- Measurement uses the merged eval-toolkit `eda` layer + `make_minilm_embedder` — this RC0 run
  is also the layer's first real-data dogfood.

## Results (measured 2026-05-28, after pre-registration)

Full detail in `results.json`; figure `within_type_diversity.png`. Reproduce via `run_rc0.py`.

| # | Criterion | Measured | PASS? |
|---|-----------|----------|-------|
| i | disjoint split | 15 train / 15 test types; **1 overlap** ("Language Translation"); **14v14** after drop | ✅ |
| ii | per-type N | min 5, median 5; 75 strings/split | ✅ |
| iii | within-type diversity | **aggregate mean within-type cosine = 0.352**; **0/28 types ≥ 0.95** (and 0 ≥ 0.80 ref) | ✅ |
| iv | train-vs-test separation | centroid cosine 0.829 (descriptive — distinct, not a red flag) | n/a |
| v | benign-FPR control | NotInject loads (113 prompts: `prompt`/`word_list`/`category`) | ✅ |

**eda-layer dogfood** (`audit_dataset` on the 140 attack strings): ran clean — 0.0 invisible-char
rate, char p95 ~98–111, **no train/test attack-string leakage**; the only failed gate is
`class_balance` (all-positive set — expected, not a defect).

## VERDICT: **GO** ✅

All gates (i, ii, iii, v) pass. BIPIA's disjoint attack-type split is adequate for the ADR-052
study. **Criterion iii (the crux) is a strong pass** — within-type cosine 0.352 means the ~5
strings/type are genuinely diverse, so attack-type-LODO is a real generalization test, not a
memorization artifact. The memorization-risk concern pre-registered as most-likely-to-fail did
**not** materialize. Proceed to Phase 2 (broad survey).
