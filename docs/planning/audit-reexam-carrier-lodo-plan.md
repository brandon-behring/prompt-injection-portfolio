# Audit + independent re-examination + Lane-2 carrier-LODO — working plan

> **Repo copy of the approved session plan** (durable, version-controlled). The canonical working
> copy lives at `~/.claude/plans/only-two-things-remain-sorted-toast.md`; this is the shareable
> in-repo record. Started 2026-06-01 (post-M1-close, post-Round-30 re-ladder).

## Context

After M1 closed (the §6.5 OOD-wall prediction FALSIFIED at the LoRA ceiling) and the Round-30
re-ladder landed (ADR-055: multi-axis capacity-dependent spine), this session does three things:
(1) **audit** whether all experiments ran + were saved + done properly, (2) **independently
re-examine** the results so far (recompute from the raw parquets — do not trust our own persisted
JSONs), and (3) **analyze "2"** = run the **carrier-LODO** M2 pre-flight gate (Lane 2's next step).

### State snapshot (2026-06-01 PM)
- On `session/2026-05-26-adoption-and-research-ops` @ `ee397a7`, clean, synced with origin; `main`
  is the same SHA via the PR-#4 fast-forward. **M0 closed; M1 closed; Round-30 re-ladder done
  (ADR-055).** `v0.1.0` tag/release/announcement **HELD for accounts**.
- **M1 headline — the OOD wall is capacity-dependent (attack-type axis):** `lora` T=−0.003 / p=0.90 /
  CI-low=−0.008 **FALSIFIED**; cheap rungs SURVIVE (tfidf +0.135, frozen +0.082). Verdict:
  `experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json`.
- **Re-ladder:** multi-axis spine; the **carrier** axis is **partially capacity-resistant (provisional,
  n=3), residual at table** (carrier-LODO `SMALL-THROUGHOUT`; ADR-055 — refined from the geometric-only
  "standing wall" prior). The **carrier-LODO
  M2 pre-flight gate** is pre-registered at `experiments/carrier-lodo/criteria.md` to test it.
- **Disk check (post-compaction):** 36 result parquets / 15 MB present at
  `experiments/attack-type-lodo/results/` — the recompute is executable, no regeneration needed.
  **3 fold families** on disk: `core_attack_type` (the §6.5 headline), `obfuscation_technique`, and
  `carrier_plus_attack_external`, each tfidf/frozen/lora × seeds 0–2; reference scorers on seed=0 only.

### Decisions locked (post-compaction /exploring-options — 2026-06-01)
- **Q1 Audit scope → VERIFY ALL 3 FOLDS.** Recompute + record verdicts for all three. **Honesty
  constraint:** only `core_attack_type` is the pre-registered §6.5 falsification (and its top-k/bottom-k
  contrast is hard-wired to that fold's 14 BIPIA task-types); the other two get their **actual reported
  generalization metric** (held-out test AUPRC per rung) recomputed and recorded as **exploratory,
  explicitly non-pre-registered** LODO-axis diagnostics — no retro-dressing as predictions.
- **Q2 Mechanism → ADVERSARIAL SUBAGENTS.** One Agent per result, prompted to find discrepancies
  (not confirm), recomputing from the raw parquets via the harness code path.
- **Q3 Sequencing → AUDIT GATES CARRIER-LODO.** Phases 1–2 complete + `make ratify-milestone` green
  before any Phase-3 carrier-LODO build/run.
- **Q4 Lane-1 closure → RESULTS-RECORDED, FRAGMENTS DEFERRED.** Author `results.md` + `decisions.md`
  now (all 3 fold verdicts); MANIFEST lane-1 → a 'results-recorded' state the contract tolerates;
  defer the 3 book fragments to the prose pass.

## Phase 0 — Durability + orient
- This file (the repo copy) + re-orient from `docs/planning/SESSION-HANDOFF.md`.

## Phase 1 — Independent re-examination (adversarial verifier agents) — ALL 3 FOLDS
- **V1 — §6.5 headline (`core_attack_type`, pre-registered):** recompute via
  `falsify_clustered.py --rung {tfidf,frozen,lora}` from the parquets; confirm the persisted verdict.
- **V1-ext — `obfuscation_technique` + `carrier_plus_attack_external` (exploratory):** confirm each
  ran; recompute its held-out test AUPRC per rung; record reproducibility, labelled exploratory.
- **V2 — EDA carrier-dominance:** re-derive silhouette/ARI on the 384-dim MiniLM embedding.
- **V3 — reference scorers:** re-score PG1/ProtectAI-v2/PG2; confirm non-gating.
- Output: `experiments/AUDIT_2026-06/verification_report.md`. **Any mismatch → halt before Phase 2/3.**

## Phase 2 — Completeness/persistence audit + fix the clear gaps
- **A1 — Lane-1 record:** populate `experiments/lane-1/{results.md,decisions.md}` (all 3 fold verdicts,
  extras separated); MANIFEST lane-1 → results-recorded; fragments deferred (Q4).
- **A2 — MR-3 contradiction:** correct the stale doc (open vs merged).
- **A3 — results archiving:** present options (status quo / condensed metrics summary / HF Hub).
- **A4 — completeness confirm:** EDA + M1 + reference recorded; deferred items = expected-not-gaps.

## Phase 3 — Lane 2 / carrier-LODO (implement + run full) — gated on Phases 1–2 green
- **C1** finalize the criteria Revision (impl specifics; not the rule). **C2** `folds.py`
  `_build_carrier_lodo` + `falsify_carrier_lodo.py` + per-carrier metrics + tests. **C3** cheap rungs
  (free, `experiment-runner`). **C4** paid `lora` (~$1, `gpu-run-watcher`) — **waits for explicit go**.
  **C5** verdict (SURVIVES/FALSIFIED/SMALL-THROUGHOUT) → `experiments/carrier-lodo/{verdict.json,
  FINDINGS.md}`. **C6** fold into the spine (validate or revise ADR-055).

## Phase 4 — Wrap
- Commit artifacts (proposed, present-first); refresh handoff + memory; pushes wait for the user's go.

## Verification
- **Phase 1:** each verifier independently reproduces the number (or flags a discrepancy); a mismatch halts.
- **Phase 2:** Lane-1 record complete; MANIFEST consistent; MR-3 corrected; `make ratify-milestone` green.
- **Phase 3:** new tests green; criteria Revision dated **before** the run; verdict gate-driven.
- **End-to-end:** `make ratify-milestone` GREEN; the carrier claim is now a modeling result (or revised).
