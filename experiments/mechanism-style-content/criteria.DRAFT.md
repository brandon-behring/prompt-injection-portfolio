# C2 — mechanism probe (style-vs-content): WHY does the cross-family wall survive? — criteria DRAFT

> **DRAFT — NOT RATIFIED (2026-06-11).** This is the C2 pre-registration scheduled at Round 31
> (`docs/planning/PORTFOLIO_PLAN.md` Round-31 update: "C2 (cross-family mechanism pre-reg) drafts
> during C1's GPU waits") and sharpened by the consolidated audit
> (`docs/planning/consolidated-audit-2026-06-09.md` **W12**: the Mirror/corpus-style confound;
> `roadmap-refresh-2026-06-09.md` Fork-C table: "pre-register a mechanism probe for WHY
> cross-family survives — style-vs-content; the Mirror confound W12 makes causal claims otherwise
> unsupportable"). It awaits its **own present-first ratification** before any corpus is generated
> or any model is trained. Open items needing user adjudication are marked **TBD** throughout.
> Numbers quoted from prior arcs are anchors, not results. No spend is authorized by this file.

## Why this arc exists (the claim it tests)

The ratified spine (ADR-055 + 2026-06-06 amendment) is: **attack-type FALSIFIED · carrier
SMALL-THROUGHOUT (one residual table wall) · cross-family SURVIVES**. But the cross-family
SURVIVES verdict carries a pre-committed, spine-level caveat (ADR-055:257, added per audit W12):

> *The direct train slate is mostly all-positive games, so pos/neg cells are not nuisance-matched
> and a residual style≈injection shortcut is structural… cross-family SURVIVES is an **axis-level
> transfer result, not a mechanism result** — why it survives (family semantics vs corpus style)
> is unsupported without the style-vs-content mechanism probe (the C2 pre-registration candidate).*

Two surviving walls are at stake:
- **Cross-family** (`../cross-family-transfer/verdict.json`): Arm A gap *grew* at the lora ceiling
  (+0.365); direct data does not bridge (B+ 3/4). The Mirror Design Pattern limitation
  (arXiv:2603.11875, registered in the cross-family `criteria.md`) means we cannot yet say whether
  the wall is about the *content* of the direct family (instruction-semantics of the payloads) or
  the *writing style* of its corpora (source/format/register bundle).
- **Residual table carrier wall**, now C1-decided (2026-06-11, audited ROBUST): a synthetic table
  corpus produced a CI-supported frozen-rung reduction (ΔG +0.083, CI-low +0.079 > 0; treated wall
  persists at +0.251) that **did not survive the decision rung — lora verdict NOT-CLOSED**
  (ΔG −0.028, CI-low −0.032 ≤ 0; `../carrier-table-training/{c1_verdict.json,
  AUDIT_C1_2026-06-11.md}`). Format-targeted data moving the wall *partway at frozen and not at
  all at the ceiling* is exactly the signature you'd expect if part of the gap is style-borne and
  part is not — motivating a probe that separates the two.

C2 is the design that breaks the style/content correlation directly, instead of inferring
mechanism from transfer outcomes.

## Question

For a detector trained on the existing slates (the cross-family Arm-A/B configuration and/or the
carrier-LODO table fold — arm scope **TBD-1** below), is the held-out generalization gap carried by
**STYLE** — surface/corpus-style features (source, format, register, dialect, generator
fingerprint; the W12 shortcut) — or by **CONTENT** — the instruction-semantics of the injected
payload? Operationally: when style and content are decoupled by construction, which factor moves
the detector's scores and the gap `G`?

## Hypotheses (load-bearing; to be pre-committed AT ratification)

Factorial, falsifiable, both-ways-publishable:

- **H_style:** detector scores track corpus style, not payload semantics — content-preserving
  restyling (same payload, target-corpus style) collapses detection of true positives, AND/OR
  style-preserving benign swaps (same corpus style, payload removed/benignified) are still flagged.
  ⇒ the surviving wall is (at least partly) a style artifact; the SURVIVES verdict's mechanism
  reading must be qualified.
- **H_content:** detection survives restyling and benign swaps drop to baseline FPR — scores track
  the payload. ⇒ the wall is a genuine semantic-transfer limit; the W12 caveat can be discharged
  as "tested, style shortcut not load-bearing."
- **Mixed** outcomes (one factor moves scores on one axis but not the other) are pre-registered as
  a legitimate result, reported per-cell, no post-hoc promotion to a single headline.

## Design (to be FIXED at ratification)

### Counterfactual corpus — the 2×2 that breaks the style/content correlation

For a fixed evaluation slate (source slate **TBD-1**), construct four cells:

| Cell | Style | Content | Construction |
|---|---|---|---|
| P-orig | original | injected | the existing positives, unmodified (anchor cell) |
| P-restyled | **swapped** | injected | content-preserving restyling: LLM style-transfer of each positive into the *other* axis's corpus style (e.g., direct-family "game" register → indirect-corpus register, or table-format ↔ email-format prose), payload semantics verified preserved |
| N-orig | original | clean | the existing matched negatives, unmodified |
| N-styled | original-positive style | **clean** | style-preserving content swap: the positive's carrier/context with the payload removed or replaced by length-matched benign instruction-shaped text from the same generator |

- **Detector is FROZEN during scoring**: C2's primary read scores *already-trained* detectors
  (the committed cross-family / carrier-LODO / C1 artifacts) on the counterfactual cells — no
  retraining is required for the headline, which is what keeps the cheap rungs $0. A secondary
  retrain-on-counterfactuals arm is **TBD-2** (scope/cost).
- **Generator + matched-cell discipline (the W12 lesson, as executed in C1):** all four cells'
  synthetic text comes from the SAME generator with the same templates, so generator style cannot
  proxy the cell label. Generator = research_toolkit `/dataset-synthesize` orchestrator with the
  C1 Rev-1 OpenAI adapter (`gpt-4.1-mini` via `generate_openai.py`, PR-#38 EmptyResponse gate,
  `--bail-at-cost`) — provider confirmation **TBD-3**.
- **Restyling fidelity gate (pre-scoring):** every P-restyled row must pass a payload-preservation
  check before it enters the eval set — exact-match of the canonical payload string after style
  transfer where the design injects mechanically (the C1 pattern), or an LLM-judge semantic-
  equivalence check where free rewriting is used (judge model + threshold **TBD-4**; rows failing
  the gate are dropped and counted in the manifest, never silently).
- **Leakage gate:** exact normalized-hash + MinHash ≥ 0.8 between every generated cell and every
  train pool whose detector scores it (purge nothing from test — generated cells ARE the test;
  instead, any generated row colliding with a train row is dropped), using the **corrected**
  `(eval_idx, train_idx)` convention (audit W17). 0-collision report committed with the corpus
  manifest, the C1 pattern.
- **Volume:** target order ~1–2k rows per cell, mirroring C1's corpus scale (exact n **TBD-5**,
  sized at ratification against the bootstrap power note below).

### Rung ladder

`tfidf` → `frozen` (local, $0: score the committed cheap-rung detectors on the four cells) →
`lora` (the decision rung: score the committed lora-rung detectors; **GPU-light — inference only**,
local if the 2070S permits batch-1 inference, else a separately-gated RunPod go ~$1–5 — **TBD-6**).
Any retraining arm (TBD-2) sits behind its own separate present-first paid go regardless.

## Statistics + decision rule (logic to be FIXED at ratification; rule SHAPE pre-locked here)

**Primary contrasts** (per rung, per source axis), on the score distributions of the frozen
detector — metric basis ROC-AUC for gap-style reads, plus mean-score shifts for the cell
contrasts (final metric set **TBD-7**, to mirror whichever the source arc's verdict used):

- **Style effect on positives:** `Δ_style = detect(P-orig) − detect(P-restyled)` — how much
  detection collapses when only style changes.
- **Style effect on negatives:** `Δ_shortcut = flag(N-styled) − flag(N-orig)` — how much
  positive-style alone triggers the detector.
- Each with a **payload-clustered bootstrap** (cluster = payload id; ≥10,000 iters; one-sided 95%
  percentile CI; **independent per-seed draws — the W4 lesson**, and the W4 seed-coupling
  disclosure carried into the criteria as in the hardened arcs), plus a **permutation test** on
  cell labels within payload clusters (label-permutation conventions per W5: cluster-level
  shuffle, +1 floor — **TBD-8** to confirm against the P1.5-hardened convention).

**Verdict rule shape** (thresholds **TBD-9**, to be locked pre-datum at ratification; the house
SESOI floor **0.05** and the ½-comparator discipline are the defaults inherited from
carrier-LODO / cross-family / C1):

- **STYLE-DRIVEN** iff `CI-low(Δ_style) > SESOI` AND/OR `CI-low(Δ_shortcut) > SESOI` at the
  decision rung (a material fraction of the wall moves with style alone; fraction-of-G framing
  **TBD-9a**).
- **CONTENT-DRIVEN** iff both CI-lows ≤ 0 at the decision rung AND point estimates < SESOI
  (style manipulation moves nothing material).
- **MIXED** otherwise — reported per-contrast, per-axis, no aggregation into a single label.
- **W10 discipline:** report both the SESOI-gated and the sign-only readings; prose never says
  "no style effect," only "below the pre-registered SESOI."
- Verdict committed via a script with `--out` + refuse-to-overwrite from day one (W3) and a
  manifest-completeness write-gate (all four cells, fidelity-gate report, leakage report, ≥3
  seeds where the source detector has seeds, decision rung present).

## Honest limitations (pre-committed)

- **Restyling is itself LLM-generated** — a residual generator fingerprint shared across cells is
  mitigated by the same-generator matched-cell design, not eliminated; this is the same residue
  C1 declared.
- **Frozen-detector scoring tests the trained artifacts, not the axis in general** — a style
  finding here is about *these* detectors' shortcut reliance; the retraining arm (TBD-2) would be
  needed for a training-dynamics claim.
- **Payload-preservation is gate-checked, not guaranteed** — the fidelity gate bounds, does not
  zero, semantic drift in P-restyled.
- **n of axes is small** (cross-family slices n≈5, carriers n=3) — directional per-cell reads,
  per-unit tables carry the evidence (the ADR-055 spine convention), no cross-fold aggregate CIs.
- **W1 caveat inherited:** any frozen-MiniLM read on table/code text carries the 256-token
  truncation qualifier (66.5% table / 44.1% code positives truncate past the attack tokens);
  cell construction must report truncation shares per cell, and table-cell conclusions at the
  frozen rung are qualified accordingly.
- This probe says nothing about closing any wall — it attributes, it does not fix; C1 (and a
  possible C1-followup) owns intervention.

## Verification + budget + write-gates

- Corpus generation cost-capped (`--bail-at-cost`; envelope **≤ $5** generation — mirrors C1's
  realized $0.27 scale — exact cap **TBD-10**); manifest + sha256 committed; rows committed if
  small else gitignored + manifest (disposition-(b) pattern).
- Cheap rungs $0 local (inference over committed tfidf/frozen artifacts). Decision-rung lora
  inference: $0 if local inference fits, else ~$1–5 RunPod behind a **separate present-first paid
  go** (TBD-6). ADR-014 contingency stays Reserved; base budget only.
- Multi-verifier adversarial audit at verdict time (the B4/post-M1 pattern).
- Ethics: benign-only generation where applicable + full-specificity synthetic-attack disclosure
  per ADR-022/ADR-041 (restyled positives ARE attack text — dataset-card handling **TBD-11**).

## Revision policy

Identical to the carrier / cross-family / C1 arcs: once ratified (DRAFT suffix dropped), this file
is **append-only** — changes land as dated Revision sections; estimator/threshold/label changes
before the first datum only, with rationale; nothing changes after the write-gate opens.

## Open TBDs for ratification (the `/exploring-options` agenda)

| # | Item | Default leaning (not decided) |
|---|---|---|
| TBD-1 | Source-arm scope: cross-family Arm-A detectors only, vs + carrier-LODO table fold, vs + C1 treated arm | cross-family primary (it owns the W12 caveat); table fold secondary once the C1 lora verdict lands |
| TBD-2 | Retraining arm in-scope? | out of v1; register as a follow-up trigger |
| TBD-3 | Generator provider/model | reuse C1 Rev-1 OpenAI path |
| TBD-4 | Restyling fidelity gate: mechanical exact-payload vs LLM-judge + threshold | mechanical where possible; judge spec needed for free rewriting |
| TBD-5 | Per-cell n | ~1–2k, power-checked |
| TBD-6 | lora-rung inference locus (local 2070S vs RunPod) | try local; C1 hit CPU-only for training, inference may differ |
| TBD-7 | Metric basis for the contrasts (ROC-AUC vs TPR-at-val-threshold vs mean score) | TPR at the val-fixed threshold for cell contrasts; ROC for gap framing |
| TBD-8 | Permutation conventions | adopt the P1.5/W5-hardened convention |
| TBD-9 | Verdict thresholds: SESOI value (default 0.05) + 9a fraction-of-G framing | house 0.05; fraction framing needs a decision |
| TBD-10 | Generation cost cap | ≤ $5 |
| TBD-11 | Ethics/dataset-card handling for restyled attack text | full-specificity disclosure, gitignore-or-card decision at ratification |

*Cross-references:* Round 31 (`docs/planning/PORTFOLIO_PLAN.md:708ff`), audit W12/W4/W5/W10/W17/W1
(`docs/planning/consolidated-audit-2026-06-09.md` §7), ADR-055:257 (Mirror caveat),
`../cross-family-transfer/criteria.md` (Mirror Design Pattern limitation; ½·G(frozen) + 0.05 SESOI),
`../carrier-lodo/criteria.md` (payload-clustered bootstrap), `../carrier-table-training/criteria.md`
(C1 — matched-negative W12 execution; frozen-rung reduction ΔG +0.083 did not survive the decision
rung — lora verdict NOT-CLOSED, ΔG −0.028; `../carrier-table-training/AUDIT_C1_2026-06-11.md`).
