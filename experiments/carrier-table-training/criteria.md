# C1 — carrier/table training arc (Lane 2): does carrier-targeted data close the residual table wall?

> **RATIFIED 2026-06-10 (user, via `/exploring-options` Q1 — "ratify as drafted").** Fork C = C1
> was decided at Round 31 (`docs/planning/PORTFOLIO_PLAN.md`); this file is its pre-registration.
> The DRAFT suffix is dropped; the **append-only revision policy below is now in force**. Numbers
> quoted from prior arcs are anchors, not results.
>
> **Spend scope locked at ratification (Q2):** this ratification authorizes the cost-capped corpus
> generation (≤ $5, `--bail-at-cost`) and the $0 cheap rungs (tfidf, frozen) including the leakage
> gate; the **`lora` decision rung remains behind its own separate present-first paid go** (~$1–5),
> per the write-gate below. The pre-run gate (research_toolkit #22, Honest limitations) must clear
> before corpus generation; its dated gate-check note is appended at the end of this file.

## Why this arc exists (the claim it tests)

The ratified carrier-LODO verdict (ADR-055 amendment; `../carrier-lodo/verdict.json`) is
**SMALL-THROUGHOUT** with one residual: the held-**table** fold keeps a real wall at the LoRA
ceiling — `G_table(lora) = +0.205` (val_roc 0.998 → test_roc 0.793; tfidf −0.148, frozen +0.334).
ADR-055 re-pointed Lane 2 at exactly this: attack the carrier wall with **carrier-targeted training
data**. The cross-family arc's sharpest lesson (B+: *direct data does not bridge*; fujitsu
anti-transfers) makes the outcome genuinely uncertain — targeted data closing the wall is NOT a
foregone conclusion, which is what makes this falsifiable and worth running.

## Question

Does augmenting the held-table fold's training pool with **provenance-disjoint, table-carrier**
injection data close the table wall at the LoRA ceiling — or does the table wall behave like the
cross-family axis, where adding in-axis data fails to bridge?

## Hypothesis (load-bearing, pre-committed at ratification)

**H (optimistic-lane, falsifiable):** synthetic table-carrier training data closes the table wall —
`G_table^treated(lora)` falls below the **0.05 SESOI** floor. A null (the wall persists, mirroring
B+'s "doesn't bridge") is publishable and feeds the C2 mechanism design.

## Design (FIXED at ratification)

**Fold + estimator inherited unchanged** from the ratified carrier arc: the carrier-LODO
held-**table** fold (`carrier_lodo_table`: train = BIPIA email+code, test = BIPIA table);
`G = val_roc − mean_seed(test_roc)` with **in-distribution val** (the carrier-lodo carve fix —
attack types held fixed in the carve); ROC-AUC basis; **payload-clustered-within-carrier**
bootstrap (carrier criteria Rev 1). ≥ **3 seeds** × the rung ladder.

**Two arms:**
- **Control = the ratified carrier-LODO artifacts as-committed** (no recompute, no re-run):
  G_table per rung as anchored above.
- **Treated:** train = control train ∪ the synthetic table corpus (below); test/val construction
  byte-identical to control.

**Synthetic table corpus (the manipulated variable is the CARRIER FORMAT only):**
- **Positives:** the SAME BIPIA attack-payload pool the fold already uses (payload overlap
  train↔test is inherent to the carrier-LODO axis — carriers are held out, payloads are not),
  injected into **non-BIPIA table-format contexts** (markdown/CSV/HTML tables). Target ~1–2k rows.
- **Matched negatives (Mirror lesson, audit W12):** clean table contexts from the SAME generator,
  same formats, same volume order — so corpus style cannot proxy the label.
- **Generator:** research_toolkit `/dataset-synthesize` (library-first, ADR-026), cost-bounded
  via `--bail-at-cost`; ethics per ADR-022/ADR-041 (full-specificity synthetic-attack disclosure).
- **Provenance disjointness enforced by a leakage gate** (exact normalized-hash + MinHash ≥ 0.8,
  purge-from-train, test sacrosanct) between the synthetic corpus and the BIPIA table test —
  using the **corrected** `(eval_idx, train_idx)` convention (audit W17).

**Rungs:** `tfidf` → `frozen` (local, $0) → `lora` (the decision rung; RunPod, write-gated behind
both cheap rungs completing + the leakage gate + a separate present-first paid go). LoRA recipe =
the locked carrier/cross-family recipe (ADR-043 Lane-2 method; `r=(8,16)` as pre-registered there).

## Statistics + decision rule (logic FIXED at ratification)

Primary contrast at each rung: `ΔG = G_table^control − G_table^treated` (positive = the
augmentation helped), with the per-arm CIs from the payload-clustered bootstrap
(≥ 10,000 iters, one-sided 95%) and — **W4 lesson — independent per-seed draws** (no draw
indexes all seeds' replicates).

Verdict at the `lora` ceiling:
- **CLOSED** iff `G_table^treated(lora) < 0.05` (SESOI) **AND** `CI-low(ΔG) > 0`.
- **REDUCED** iff `CI-low(ΔG) > 0` **AND** `G_table^treated(lora) ≥ 0.05`.
- **NOT-CLOSED** iff `CI-low(ΔG) ≤ 0` — targeted data does not bridge (the B+ pattern).

**Dual reading (W10 discipline):** alongside the labels above, report the carrier arc's two rule
readings (sign-only and ½·G(frozen)) on `G_table^treated` for cross-axis comparability; prose says
"small under the pre-registered knob," never "no wall."

**Secondary (non-gating):** NotInject over-defense FPR at the val-fixed 1% threshold (does table
augmentation buy the wall down at the price of over-defense?); optional held-code replication if
the table result is CLOSED (generalization of the recipe, not verdict-bearing).

## Honest limitations (pre-committed)

- **n = 1 fold** (table) for the headline — this is a targeted intervention on a named residual,
  not a survey; the read is fold-specific by design.
- **Synthetic ≠ deployed tables**: a CLOSED verdict shows the wall is closable by format-targeted
  data, not that any specific production corpus closes it.
- **Payload overlap train↔test** is inherent to the carrier axis (declared above); this arc says
  nothing about cross-family or attack-type transfer.
- **Generator confound residue**: matched negatives mitigate, not eliminate, generator-style
  shortcuts; the leakage gate handles only string-level proximity.
- Pre-run gate: confirm research_toolkit **#22** (silent `_extract_text` failure) is closed or
  demonstrably not on the recipe's path **before** corpus generation (ADR-051 gate).

## Verification + budget + write-gates

- Corpus generation: cost-capped (`--bail-at-cost`, target ≤ $5); manifest + sha256 committed,
  corpus rows committed if small (else gitignored + manifest, the disposition-(b) pattern).
- Cheap rungs local ($0); `lora` treated arm ≈ 3 seeds × 1 fold ≈ **$1–5** RunPod (base budget;
  ADR-014 stays Reserved). Control arm is never re-run.
- The verdict script ships with `--out` + refuse-to-overwrite from day one (**W3 lesson**) and a
  manifest-completeness write-gate (≥3 seeds, both arms, decision rung present).
- Audit plan: multi-verifier adversarial audit at verdict time (the B4/post-M1 pattern).

## Revision policy

Identical to the carrier/cross-family arcs: this file is **append-only after ratification** —
any change lands as a dated Revision section; estimator/threshold/label changes before the first
datum only, with rationale; nothing changes after the write-gate opens.

## Pre-run gate check — research_toolkit #22 (2026-06-10; gate CLEARED via upstream fix)

The gate required #22 (silent `_extract_text` failure) be *closed or demonstrably not on the
recipe's path* before corpus generation. **The trace found it ON the path**: `_extract_text`
(`.tooling/research_toolkit/scripts/dataset_synthesize.py:316`) silently returns `""` on
all-non-text responses, and `synthesize()` called it on every sample, writing `content: ""` rows
**counted against `target_count`** — a silent corpus-poisoning path for exactly the generator
this arc uses. Per the pre-adjudicated rule, generation was STOPPED and escalated.

**User decision (escalation modal): minimal upstream fix + dogfood.** Landed as research_toolkit
**PR #38** (`fix/21-empty-response-loud`, commit `c9fae12`, branched from upstream `main`
`c3a74f4`): empty/whitespace-only responses now drop the row (not written, not counted), keep
honest cost accounting, set `api_error = "EmptyResponse: …"`, and exit 3 with partial-manifest
recovery — plus a regression test (module suite 22/22). The repo-local `.tooling/research_toolkit`
clone now sits on that branch, so **corpus generation runs with the fix regardless of upstream
merge timing**. Per #22's own "recommended path to ready," the C1 corpus generation doubles as the
skill's first real burn-in/dogfood run — friction logged to research_toolkit `BURN_IN_NOTES.md`
(items 1–2 of #22).

**Gate disposition: CLEARED** — the silent path is eliminated in the exact code the recipe
executes; the fail-late `ANTHROPIC_API_KEY` path (#21 item #5) is not exercised by this arc
(CLI entry checks the env var at `dataset_synthesize.py:593`).
