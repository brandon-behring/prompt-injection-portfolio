---
adr_id: "053"
slug: "runpod-job-spec-run-job-not-session"
title: "RunPod cloud-eval launch via strict YAML job spec + run_job (the phantom runpod_deploy.Session correction); Lane-1 sweep is base-budget"
date: 2026-05-30
status: Accepted
linked_round: "R29 (M1 Lane-1 launch-wiring session)"
plan_section: "§2 Tier-1 + §13 + §16"
supersedes: []
---

# ADR-053: RunPod launch via job spec + `run_job` (not the phantom `Session`); Lane-1 sweep is base-budget

## Status

Accepted (Round 29 lock; launch glue committed `4862e21`). The *paid* launch remains user-led and unfired — this ADR ratifies the **wiring + budget classification**, not the spend.

## Context

The M1 Lane-1 attack-type-LODO headline sweep ([ADR-052](ADR-052-attack-type-generalization-study-design.md)) cannot run on the local RTX 2070 SUPER at spec config (batch 16 / max_len 512 OOMs; feasibility probe in `decisions/contingency_unlock_1.md`), so it must run on a 24 GB+ cloud GPU via the `runpod-deploy` orchestrator already pinned `>=0.8.4` (`decisions/library_imports.md`). Wiring this surfaced a defect: the portfolio plan (`docs/planning/PORTFOLIO_PLAN.md`) and the **sibling-submission** ADR-059 both named `runpod_deploy.Session` with `lifecycle.on_success: recycle` as the launch API. **That symbol does not exist** in the installed `runpod-deploy>=0.8.4`. Verified against the library, the real surface is `load_job_spec(yaml) -> RunpodJobSpec` then `run_job(spec, config_path=..., offline_dry_run=, dry_run=, max_gpu_price_usd=)`; `lifecycle` values are `preserve | stop | delete | recycle`. (`recycle` *is* valid — the phantom was the `Session` object, not that enum value.) Submission ADR-059 belongs to a **different ADR series** (`prompt-injection-detection-submission`), not this repo's `decisions/`; it cannot be amended from here, so the correction lives in this portfolio ADR.

Separately, the sweep's $5–15 cost needed a base-vs-contingency ruling before launch ([ADR-013](ADR-013-cost-contingency-unlock-policy.md) gate). ADR-013 requires a `make cost-report` attestation, but no cost-report target exists; a manual spend tally substitutes (recorded in `contingency_unlock_1.md`).

## Decision

1. **Launch all cloud evals via job spec + `run_job`.** The Lane-1 headline sweep — and future Lane 2 / 1b / 5 cloud runs — launch through `runpod_deploy.load_job_spec → run_job` over a strict schema-v2 YAML job spec. The `Session` API is **struck** from all portfolio references. This is project-specific orchestration glue (ADR-026 §5), not a hand-rolled primitive: `runpod-deploy` stays the upstream owner.
2. **Lifecycle `on_success: delete` for one-shot sweeps.** A one-shot sweep uses `delete` for an unambiguous billing-stop (pod auto-terminates). `recycle`'s pool-reuse semantics are designed for warm-pool reuse, which does not fit a single fire-and-forget sweep. **(Open reconcile — see Alternatives; `recycle` reserved for a future multi-job warm-pool pattern.)** On failure: `on_failure: stop` (preserve for forensics; the gpu-run-watcher captures the partial MANIFEST before lifecycle runs).
3. **Classify the $5–15 sweep as base-budget — no contingency draw.** The manual spend tally in `contingency_unlock_1.md` finds **$0.00 realized cloud spend to date** (all compute local: CPU + the owned RTX 2070 probe). $5–15 « $250 base « $350 hard cap ([ADR-002](ADR-002-cost-cap-250-base-100-contingency.md)). Therefore **[ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) stays Reserved** (not advanced to Accepted); `contingency_unlock_1.md` is a base-budget GPU-spend record routed through the cost-driven slot, not a contingency unlock.

## Consequences

- **Launch glue committed (`4862e21`).** `experiments/attack-type-lodo/runpod_lane1_sweep.yaml` (24 GB+ GPU; stage repo; run `tfidf+frozen+lora+full_ft × 3 folds × 3 seeds` + `falsify_ood_wall`; pull results + verdict; `budget.cost_cap_usd: 15` + `max_runtime_minutes: 240` hard guards) and `scripts/runpod_sweep.py` (thin `load_job_spec → run_job` wrapper). Three new `runpod_deploy` symbols registered in `library_imports.md` (`load_job_spec`, `run_job`, `RunpodJobSpec`); the `library_imports_registered` contract passes.
- **Validated without spend.** `--offline-dry-run` (zero provider calls; schema + local-path validation) **and** a live `--dry-run` that resolved a real GPU (H100 80GB / US-CA-2, est ~$10 worst-case « $15 cap) and formed the `runpodctl pod create` command — no provision, no spend.
- **Provider-side caveats remain (launch is user-led).** Cheap ~24 GB cards (~$0.40/h) need `RUNPOD_API_KEY` + broader (COMMUNITY) datacenters; the SECURE H100 fallback resolves in-budget now. Provider-side values (`pod.image`, `pod.gpu_order`, `pod.datacenters`, the registered SSH key) are **not** checked by `--offline-dry-run` and must be re-confirmed by a fresh `--dry-run` at launch time, with explicit user go-ahead.
- **gpu-run-watcher unblocked.** The `runpod_deploy.Session` blocker named in the M1 handoff is dissolved; `gpu-run-watcher` (corrected to WIRED in `4862e21`) can now launch+watch the real sweep.

## Alternatives considered

- **Hand-roll a `Session`-shaped wrapper to match the plan/ADR-059 name** — rejected: that would invent a local primitive to paper over a doc error (ADR-026 violation) and entrench the phantom. The fix is to correct the docs to the real API, not to forge the API to the docs.
- **`lifecycle.on_success: recycle` (as ADR-059 specified)** — rejected for a one-shot sweep: `recycle`'s warm-pool reuse leaves billing semantics ambiguous for a single fire-and-forget run; `delete` gives a clean, auditable billing-stop. (Flagged for reconcile if a future multi-job warm-pool pattern wants `recycle`.)
- **Route the sweep through a contingency unlock (advance ADR-014)** — rejected: with $0.00 realized spend, $5–15 sits well inside the base $250; per [ADR-013](ADR-013-cost-contingency-unlock-policy.md) §Consequences this is an infrastructure relocation of a pre-registered base-budget sweep, not a research-signal method-expansion, so it is base-budget and ADR-014 stays Reserved.
- **Block on a `make cost-report` target before classifying** — rejected: no such target exists; a manual ledger tally (enumerating realized spend from the project record) is a faithful substitute and is recorded in `contingency_unlock_1.md` for audit.

## Cross-references

- [ADR-052](ADR-052-attack-type-generalization-study-design.md) (the attack-type-generalization study this sweep executes)
- [ADR-002](ADR-002-cost-cap-250-base-100-contingency.md) ($250 base + $100 contingency; $350 hard cap; manual `make cost-report` monitoring)
- [ADR-013](ADR-013-cost-contingency-unlock-policy.md) (contingency unlock gate + `make cost-report` requirement)
- [ADR-014](ADR-014-cost-contingency-unlock-reserved-1.md) (cost slot — **stays Reserved**; not advanced)
- [ADR-026](ADR-026-no-local-workarounds-policy.md) (library-first; §5 project-specific-glue carve-out for the launch wrapper)
- `decisions/contingency_unlock_1.md` (the $0.00 spend tally + base-budget classification + pre-spend checklist)
- `decisions/library_imports.md` (runpod-deploy section: `load_job_spec` / `run_job` / `RunpodJobSpec`; the 2026-05-30 phantom-`Session` correction)
- `experiments/lane-1/hypothesis.md` (bail-out: "local GPU sweep infeasible within budget → escalate to gated cloud GPU")
- `experiments/attack-type-lodo/runpod_lane1_sweep.yaml` + `scripts/runpod_sweep.py` (committed launch glue, `4862e21`)
- Submission **ADR-059** (`prompt-injection-detection-submission` series — the phantom-`Session` source; a *different* ADR series, not amendable from this repo)
