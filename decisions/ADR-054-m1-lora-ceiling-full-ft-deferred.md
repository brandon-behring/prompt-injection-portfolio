---
adr_id: "054"
slug: "m1-lora-ceiling-full-ft-deferred"
title: "M1 attack-type-LODO ceiling is LoRA (3-rung write-gate); full-FT deferred to a conditional trigger-gate; hybrid local+RunPod execution; off-the-shelf reference column"
date: 2026-06-01
status: Accepted
linked_round: "R29 (M1 Lane-1 launch-wiring session)"
plan_section: "§5 + §16"
supersedes: []
---

# ADR-054: M1 attack-type-LODO ceiling = LoRA; full-FT deferred; hybrid local+RunPod execution; off-the-shelf reference column

## Status

Accepted (Round 29 lock). **Amends, does not supersede, [ADR-052](ADR-052-attack-type-generalization-study-design.md) and [ADR-053](ADR-053-runpod-job-spec-run-job-not-session.md)** — both stay Accepted; this ADR re-scopes their rung set and execution plan. The harness/detectors/falsify/reference-scorer code carrying these six points is committed; the *paid* GPU launch remains user-led and unfired ([ADR-053](ADR-053-runpod-job-spec-run-job-not-session.md)).

## Context

[ADR-052](ADR-052-attack-type-generalization-study-design.md) added `full_ft` (full fine-tune of all ModernBERT-base weights) to the M1 attack-type-LODO headline sweep "to close the never-measured full-FT OOD gap." But `full_ft` is the costliest rung, and four facts make running it on *every* M1 cell front-load the largest GPU cost for the least marginal signal:

- The `criteria.md` §6.5 cheap rungs already **SURVIVE** under the honest payload-clustered estimator (Revision 1): tfidf T=+0.135, frozen T=+0.082, both at the exact-permutation floor (p=0.0143, min-p 1/70) with cluster-bootstrap CI-low > 0 and 100% of resamples positive. The decision-relevant signal is carried by the cheap rungs + `lora`.
- LoRA is already the Lane-2 **primary** parameter budget ([ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md)); full-FT is explicitly out of Lane-2 scope there, on the submission ADR-075 "bottleneck is DATA not parameter budget" rationale.
- Only transformer *training at spec batch* (16 / max_len 512) needs the 24 GB card; `full_ft` needs strictly more VRAM than the `lora` that already OOM'd the local RTX 2070 SUPER probe (`decisions/contingency_unlock_1.md`).
- The §6.5 write-gate is judged on the `lora` rung (`falsify_ood_wall._RUNG_PREFERENCE = (lora, full_ft, frozen, tfidf)` — `lora`-first), so the manifest-completeness predicate, not the decision rule, is the only thing `full_ft` blocks.

## Decision

Record all six:

1. **Decouple the write-gate rung set from the implemented ladder.** `detectors.REQUIRED_RUNGS = ("tfidf","frozen","lora")` is new and drives (a) the harness `--rungs` default and (b) the §6.5 write-gate completeness predicate. `RUNG_NAMES` stays 4-wide `("tfidf","frozen","lora","full_ft")`; `full_ft` stays in `make_detector` + the `--rungs` choices (still selectable).
2. **`full_ft` is DEFERRED via a trigger-gate (PORTFOLIO_PLAN §16), not dropped.** Re-run `full_ft × 3 folds × 3 seeds` **iff** the merged 3-rung §6.5 `lora` verdict is decision-relevant — i.e. LoRA SURVIVES with a real capacity lift over `frozen`, OR is borderline such that the never-measured full-FT OOD point would change the writeup. Deferred-not-dropped; ~$2–6 incremental, disclosed now.
3. **Hybrid execution.** tfidf + frozen + §6.5-falsify + off-the-shelf reference scorers run **LOCAL** (8 GB); only `lora` trains on **RunPod** (24 GB+). New `harness.rebuild_manifest()` computes `complete_headline_sweep` from the on-disk **union** (local cheap rungs merged with a RunPod `lora` pull) against `REQUIRED_RUNGS`; `falsify_ood_wall.manifest_complete()` is **UNCHANGED** (still trusts the `complete_headline_sweep` flag); new `harness.py --finalize-manifest` re-stamps the manifest post-merge.
4. **§6.5 pre-registration amended 4→3 required-rung set as `criteria.md` Revision 2** (judged on the `lora` rung). **The DECISION RULE is BYTE-FOR-BYTE UNCHANGED** — SURVIVES iff one-sided permutation p<0.05 AND one-sided 95% bootstrap CI-low > 0. Only the manifest-completeness predicate (which rungs must be present) moved.
5. **Off-the-shelf reference column (`reference_scorers.py`).** Score frozen guards (ProtectAI ungated; Meta PG1/PG2 skip-gracefully on a 403) on each LODO test set as a seed-invariant reference. **NON-gating** — artifacts named `reference_{probe}.test_scores.parquet`, outside `REQUIRED_RUNGS`, never seen by `_scan_artifacts` / the write-gate.
6. **Budget.** The RunPod sweep drops from 4-rung ~$5–15 to `lora`-only ~$1–5; the launch YAML `budget.cost_cap_usd` 15 → 8.

### What this amends

- **[ADR-052](ADR-052-attack-type-generalization-study-design.md)'s** "Detectors: frozen + LoRA + **full-FT** (closes the never-measured OOD gap)" is re-scoped to "**full-FT deferred** behind a documented §16 trigger; **M1's measured ceiling is LoRA**." ADR-052's *intent* (eventually measure the full-FT OOD point) is **preserved as a fireable gate, not discharged**.
- **[ADR-053](ADR-053-runpod-job-spec-run-job-not-session.md)'s** ratified `runpod_lane1_sweep.yaml` now runs `--rungs lora` (not `tfidf frozen lora full_ft`), and the **on-pod `falsify_ood_wall` call is removed** — falsification runs locally on the merged tree (cheap rungs + pulled `lora`) via `--finalize-manifest` then `falsify_ood_wall.py`. ADR-053's launch API (`load_job_spec → run_job`), `on_success: delete` lifecycle, and base-budget classification are unchanged.

### Scope boundary

Does **not** perform the deferred M0→M7 milestone re-ladder — still deferred per [ADR-052](ADR-052-attack-type-generalization-study-design.md) (Phase 3 / Round-27 Q3). This ADR re-scopes the M1 sweep's rung set + execution, nothing downstream of M1.

## Consequences

- **Code committed against this decision:** `detectors.REQUIRED_RUNGS` (decoupled from `RUNG_NAMES`); `harness.rebuild_manifest()` + `--finalize-manifest` (union-of-disk completeness); `reference_scorers.py` (non-gating reference column); `falsify_ood_wall.manifest_complete()` unchanged. Tests assert the contract: `test_required_rungs_ceiling_and_full_ft_selectable` (`REQUIRED_RUNGS == (tfidf,frozen,lora)`, `full_ft` selectable but not required), `test_rebuild_manifest_complete_on_required_rungs` / `_incomplete_without_lora`, and `test_reference_scores_are_non_gating`.
- **Reconciliation edits applied in this session (Round 29):** `criteria.md` Revision 2 (the 4→3 rung amendment + a superseded-pointer on the Rev-1 "≥3-seed × 4-rung" close); PORTFOLIO_PLAN §16 (the `full_ft` trigger-gate, beside the existing M1→M2 / M5-close / M3-entry gates); `contingency_unlock_1.md` (the 2026-06-01 LoRA-only revision note + the expected-outcome command/`4-rung` lines). Owed at the launch boundary: `runpod_lane1_sweep.yaml` (`--rungs lora`, drop the on-pod falsify step + dead `verdict` artifact, `cost_cap_usd: 8`), `gpu-run-watcher.md` / `experiment-runner.md` / `delegation.md`, `SESSION-HANDOFF.md`, the harness-spec §4/§6.5, and the `decisions/README.md` index row.
- **Honest framing of the write-gate relaxation.** The 4→3 move is via a **named constant** (`REQUIRED_RUNGS`) + a **timestamped `criteria.md` Revision 2** appended per the file's own revision policy — never a silent edit. The **decision rule is unchanged**; the **judged rung (`lora`) is unchanged** and was always `_RUNG_PREFERENCE`-first. The dropped rung is the **ceiling-above-the-ceiling**, not the rung H1 is about — `full_ft` would only raise the absolute detection level, whereas H1 (and the §6.5 gate) is a test on the per-type detectability *ordering*, which `full_ft` does not arbitrate.
- **Budget unchanged in posture, smaller in fact.** `lora`-only ~$1–5 « the ~$5–15 already classified **base-budget** in [ADR-053](ADR-053-runpod-job-spec-run-job-not-session.md) / `contingency_unlock_1.md` ($0.00 realized; « $250 base « $350 hard cap). [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) stays Reserved; the deferred `full_ft` (~$2–6) also sits inside base budget when/if its trigger fires.
- **Reference column may be empty.** ProtectAI always scores; Meta PG1/PG2 are gated and skip-gracefully (issue #1, Meta Llama gate). A reference column with only ProtectAI is the expected near-term state and is non-blocking by construction.

## Alternatives considered

- **Delete `full_ft` from `RUNG_NAMES`** — rejected: loses selectability and reads as abandoning [ADR-052](ADR-052-attack-type-generalization-study-design.md)'s stated goal of measuring the full-FT OOD point. Deferring behind a fireable §16 trigger preserves the intent.
- **Force local full-FT at batch-2** — rejected: ≈6–8 h GPU wall-clock with live OOM risk from desktop VRAM reclamation (already observed killing the batch-8 probe; `decisions/contingency_unlock_1.md`).
- **Keep the 4-rung sweep on RunPod (as [ADR-053](ADR-053-runpod-job-spec-run-job-not-session.md)'s YAML specifies)** — rejected: front-loads the costliest rung for the least marginal signal, when the cheap rungs already SURVIVE and `lora` is the judged ceiling.

## Cross-references

- [ADR-052](ADR-052-attack-type-generalization-study-design.md) (attack-type-generalization study design — the rung set + "close the full-FT OOD gap" this ADR amends; intent preserved as a §16 trigger)
- [ADR-053](ADR-053-runpod-job-spec-run-job-not-session.md) (RunPod launch via `load_job_spec → run_job`; the ratified YAML now runs `--rungs lora` + drops the on-pod falsify call; base-budget classification unchanged)
- [ADR-043](ADR-043-lane-2-lora-only-and-baseline-expansion.md) (Lane 2 LoRA-only — the precedent that LoRA is the portfolio's primary parameter budget and full-FT is out of scope)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) ($250 base + $100 contingency; $350 hard cap)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (contingency unlock gate — the `lora`-only ~$1–5 and deferred `full_ft` ~$2–6 stay base-budget)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) (cost slot — **stays Reserved**; not advanced)
- `experiments/eda/OOD_WALL_PREDICTION/criteria.md` (the §6.5 pre-registration; Revision 1 = payload-clustered estimator + levels-not-magnitude; Revision 2 = 4→3 required-rung set, decision rule unchanged)
- `decisions/contingency_unlock_1.md` ($0.00 realized spend tally + base-budget classification + the 2026-06-01 LoRA-only revision)
- `docs/planning/attack-type-lodo-harness-spec.md` §4 (the detector rungs) + §6.5 (the OOD-wall falsification step + FIXED decision rule)
- `experiments/attack-type-lodo/detectors.py` (`REQUIRED_RUNGS` / `RUNG_NAMES` / `make_detector`), `harness.py` (`rebuild_manifest` / `--finalize-manifest`), `falsify_ood_wall.py` (`manifest_complete` unchanged; `_RUNG_PREFERENCE` lora-first), `reference_scorers.py` (non-gating reference column)
