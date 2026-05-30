# Session handoff — 2026-05-30 (PM) — M1 pre-launch gate COMPLETE; only the paid RunPod launch remains

## ✅ START HERE — clean session

**The M1 attack-type-LODO headline sweep is LAUNCH-READY.** This session was an *audit-first methodological hardening* of the EDA→§6.5 chain (the user's call: "be confident in the local work + framing before spending on RunPod"), carried all the way through to a validated, decision-recorded launch mechanism. Everything up to provisioning is **done, gate-clean, and PUSHED**. The **only** remaining step is the paid RunPod launch (user-led).

**Four commits this session, all pushed to `origin/session/2026-05-26-adoption-and-research-ops` (HEAD `170cb51`, 0 unpushed):**
1. **`216bb7c`** — S1 honest **payload-clustered §6.5 estimator** (`falsify_clustered.py`; `criteria.md` **Revision 1**) fixing a pseudo-replication error; **F1=levels** framing; **M2** LoRA head fix.
2. **`6d21dc9`** — **M1** NotInject over-defense FPR (now records clean-context AND NotInject) + **S2** recorded as an empirically-mitigated limitation.
3. **`4862e21`** — **RunPod launch glue** (`runpod_lane1_sweep.yaml` + `scripts/runpod_sweep.py`, offline + live `--dry-run`-validated) + **base-budget** spend tally.
4. **`170cb51`** — **ADR-053** ratified + 9 phantom-`runpod_deploy.Session` refs scrubbed across 5 files.

**🔑 The §6.5 verdict is now honest AND looks positive.** A 4-agent audit found three defects pre-registration missed (all fixed locally, $0): (a) the §6.5 "drop" *cancels* `val_auprc` → it's a detectability-**ordering** test, not collapse-magnitude (relabeled, F1=A); (b) the bootstrap was **pseudo-replicated** (180 rows vs 5 payloads) → rebuilt as payload-clustered; (c) the prediction's encoder gap (MiniLM vs ModernBERT) — empirically closed by the frozen rung. **Under the honest estimator, the cheap rungs (tfidf+frozen) SURVIVE** (perm at the 1/70 floor = perfect tail separation; cluster-CI 100% positive; τ-b 0.45/0.58) — so the eventual GPU verdict is a de-risked *confirmation*, not a discovery.

**⚠️ Milestones still under reconsideration** — M0→M7 provisional; the formal `v0.1.0` M0 close stays **DEFERRED**. (Note: `ADR-053` is now **taken** by the RunPod decision; a future milestone-rethink ADR is ADR-054+.)

---

## NEXT — live options (confirm the fork with the user; present-first)

1. **Launch the M1 headline sweep on RunPod — the marquee remaining deliverable (closes issue #2).** Everything is wired + validated; this is user-led + paid (~$1–6). Steps: set `RUNPOD_API_KEY` + give go-ahead → `uv run python scripts/runpod_sweep.py --dry-run` (a *fresh* dry-run to confirm live availability + price; tune to a cheap ~$0.40/h 24 GB card by switching `pod.cloud_type: COMMUNITY` + broadening `pod.datacenters` — the SECURE H100 fallback resolves in-budget now but is pricier) → `scripts/runpod_sweep.py` (the live launch) → **`gpu-run-watcher`** drives + watches the ~1.5–3 h sweep (poll + guarded auto-kill at the `cost_cap_usd=15` / `max_runtime=240` guards) → `falsify_ood_wall.py` writes the **write-gate-OPEN SURVIVES/FALSIFIED verdict** into `OOD_WALL_PREDICTION/` (the §6.5 falsification, issue #2).
2. **Continue the milestone rethink** (deferred M0→M7 re-ladder) → another `/exploring-options` round → Round 28 (± ADR-054+).
3. **Dogfood the suite further** — e.g. `dataset-auditor` → refresh the dataset survey via `survey_run.py --out`; or other lanes.

The formal `v0.1.0` M0 close is **NOT** on this list — deferred pending the rethink.

---

## Current state (2026-05-30 PM)

### §6.5 falsification — honest unit (this session)
- `experiments/attack-type-lodo/falsify_clustered.py` — the payload-clustered estimator (type-level exact permutation, min-p 1/70; payload-cluster bootstrap; contrast on per-type test-AUPRC **levels** per F1=A). `falsify_ood_wall.py` is now a thin write-gated wrapper that delegates to it. `criteria.md` **Revision 1** records the amendment (R1 unit, R2 levels-not-magnitude, R3 permutation-resolution).
- **Honest-unit rehearsal verdict on the cheap rungs: SURVIVES** (tfidf T=+0.135, frozen T=+0.082; both perm p=0.0143 floor, cluster-CI >0, 100% of resamples positive). The GPU run adds `lora`+`full_ft` to complete the 4-rung manifest → open the write-gate.

### RunPod launch glue (`4862e21`; ADR-053)
- `experiments/attack-type-lodo/runpod_lane1_sweep.yaml` (24 GB+ GPU; stage repo; run `tfidf+frozen+lora+full_ft × 3 folds × 3 seeds` + `falsify_ood_wall`; pull results+verdict; `cost_cap_usd=15` + `max_runtime_minutes=240`; `on_success: delete`) + `scripts/runpod_sweep.py` (`load_job_spec → run_job`; `--offline-dry-run` = zero-spend validation, `--dry-run` = live price/inventory). **There is no `runpod_deploy.Session`** — ADR-053 records the correction.
- **Budget = base-budget** ($0.00 realized cloud spend; $5–15 « $250; ADR-014 stays Reserved; tally in `contingency_unlock_1.md`).

### M1 harness (`695a739` + this session) — `experiments/attack-type-lodo/`
- `folds.py` / `detectors.py` (4 rungs; LoRA now `modules_to_save=["classifier","head"]`) / `metrics.py` / `harness.py` (now records `clean_context_fpr` + `notinject_fpr`) / `falsify_*`. `results*/` gitignored. 40 tests; ruff + mypy --strict green.

### Pre-modeling EDA arc + subagent suite + eval-toolkit
- EDA `OOD_WALL_PREDICTION/` (carrier dominates the MiniLM embedding; the §6.5 prediction). The six `.claude/agents/` are LIVE + dogfooded this session (session-orienter, experiment-runner, gate-runner, adr-scribe all exercised). eval-toolkit v1.6.0 (pinned `[probes,losses]>=1.6`); concurrent dirty `feat/review-eval-tooling` — do eval-toolkit work in an isolated worktree off `origin/main`.

---

## Read first (in order)
1. `experiments/eda/OOD_WALL_PREDICTION/criteria.md` — the pre-registration **incl. Revision 1** (the payload-cluster amendment + F1=A).
2. `decisions/ADR-053-runpod-job-spec-run-job-not-session.md` — the RunPod launch decision + base-budget ruling.
3. `experiments/attack-type-lodo/runpod_lane1_sweep.yaml` + `scripts/runpod_sweep.py` — the launch glue (read before launching; confirm provider-side values).
4. `decisions/contingency_unlock_1.md` — the spend tally + base-budget classification (RESOLVED).
5. `decisions/ADR-052-…md` + `experiments/lane-1/{hypothesis,protocol}.md` — the study design + Lane-1 pre-registration (incl. the S2 encoder-transfer note).
6. `experiments/attack-type-lodo/falsify_clustered.py` + `falsify_ood_wall.py` — the honest §6.5 estimator + write-gate.
7. `docs/planning/PORTFOLIO_PLAN.md` — Round 27 block + §16 gates (milestone framing, under rethink).

## Open tracked items (GitHub Issues + Work-Tracker #1)
- **#2** `P2`/`research` — Falsify the OOD-wall prediction (§6.5). **Now one launch away:** the harness + honest estimator + write-gate are committed; the RunPod sweep produces the verdict.
- **#1** `P3`/`improvement` — Rerun V10 with Prompt-Guard-86M once its Meta gate is granted.

## Gotchas
- **Working-style (most load-bearing, borne out all session):** present-first; interrogates inconsistencies; wants `/exploring-options`-style focused forks **before** convergence. **Surface real forks + ask before requesting approval; do not barrel into execution.** (This session: the user reframed a menu-pick into "is the methodology sound?" — which paid off.)
- **RunPod launch mechanics:** no `Session` (ADR-053); it's the YAML spec + `run_job`. The cheap-card path needs `RUNPOD_API_KEY` + COMMUNITY/broader datacenters; `--offline-dry-run` does NOT check provider-side values (image/datacenter/GPU/SSH-key) — always do a fresh live `--dry-run` at launch. The paid launch + git commit/push always prompt (not auto-approved).
- **Commit trailer:** `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` (model-specific; NOT the generic global `git.md` form).
- **`uv sync --extra dev`** always (bare prunes the dev extra). eval-toolkit work → isolated worktree off `origin/main`.
- **PG1 (`meta-llama/Prompt-Guard-86M`)** Meta gate still PENDING (403). **research-kb integration is a standing BOUNDARY** — separate session.
- **Milestones under rethink** — M0→M7 / formal `v0.1.0` close not settled.
- Session `TaskList` all `completed`; live follow-ups are GitHub issues #1/#2.

---

*↓ Prior handoff (2026-05-30 — "subagent suite SHIPPED") is superseded by the above (this session hardened the §6.5 methodology, wired + ratified the RunPod launch, and pushed everything). Preserved in git history at `b0cb448`.*
