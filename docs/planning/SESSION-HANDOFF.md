# Session handoff — 2026-05-30 — Context-engineering subagent suite SHIPPED + prior WIP committed

## ✅ START HERE — clean session

**Three things landed this session, all committed, none pushed:**
1. **Context-engineering subagent suite** (`1bfefaf`) — six focused agents under `.claude/agents/` + wiring (`CLAUDE.md` pointer → `.claude/delegation.md` + committed `.claude/settings.json` allowlist) + `survey_run.py --out` (collision-free parallel audits) + its test.
2. **M1 attack-type-LODO harness** (`695a739`) — the previously-uncommitted Lane-1 modeling harness (code + 3 tests + dogfooded-symbol registry + spec precision note). CI-green.
3. **Lane-1 pre-registration + cloud-GPU contingency** (`a3026f7`) — `lane-1/{hypothesis,protocol}.md` reconciled to ADR-052, `contingency_unlock_1.md` (RunPod unlock, DRAFT), working plan.

**🔑 The subagent suite is now LIVE for you.** Custom agents load at Claude Code **startup** — they were written last session but become invocable this (restarted) session. **Dogfood them** (that's the point): orient with `session-orienter`, run gates with `gate-runner`, local smoke with `experiment-runner`, the RunPod sweep with `gpu-run-watcher`, draft ADRs/Rounds with `adr-scribe`, fan out the dataset survey with `dataset-auditor`. The When→Delegate→Invocation table is `.claude/delegation.md`. **They are present-first: no agent decides a fork, ratifies, commits, pushes, or files a public issue** — they run/parse/brief/draft, you decide.

**⚠️ Milestones still under active reconsideration** (carried from last session). Treat M0→M7 as provisional; the formal `v0.1.0` M0 close (tag/release/announcement) stays **DEFERRED** pending the rethink — do not push to close M0 formally.

**Git state:** `session/2026-05-26-adoption-and-research-ops`, **HEAD `a3026f7`, 6 commits UNPUSHED** vs upstream `origin/session/2026-05-26-adoption-and-research-ops` (still at `151db97`); 0 behind → push is a clean fast-forward. Tree clean. (The 6: `2054a26 e49918e 93ba8ee` from prior sessions + this session's `1bfefaf 695a739 a3026f7`.) eval-toolkit **v1.6.0** live on PyPI + `main`.

---

## What happened this session (2026-05-30)

The user asked for better **context + environment engineering** — subagents that do parallel/independent context-heavy work so the main agent sees only distilled results. Worked it via `/exploring-options` (the user rejected an initial `ExitPlanMode` to interrogate the design first — present-first, again) across **8 locked decisions**:

1. **Granularity** → six focused single-responsibility agents (not consolidated).
2. **Long jobs** → split by target: local = detached-and-parse; RunPod = a watcher agent.
3. **Watcher** → its own 6th agent `gpu-run-watcher` (distinct tool grant + telemetry contract).
4. **Watcher authority** → alert + recommend; auto-kill ONLY on hard cost-ceiling / no-progress guards; + draft `runpod-deploy` friction upstream.
5. **Playbook** → ~lean `CLAUDE.md` pointer → `.claude/delegation.md`.
6. **Survey I/O** → patch `survey_run.py --out` (+ test) for collision-free parallel persistence.
7. **Permissions** → committed `.claude/settings.json`; safe ops auto-approved; **paid RunPod launch + git commit/push deliberately excluded → always prompt**.
8. **Scribe I/O** → return draft only; user ratifies + writes.

Then committed the suite, and — at the user's request — committed the **previously-uncommitted M1 harness and Lane-1 pre-registration** as their own `feat:` / `docs:` commits.

This session's approved plan: `~/.claude/plans/i-want-o-have-async-bee.md` (the 6-agent design + full verification).

---

## NEXT — live options (confirm the fork with the user; do not barrel in)

This session was a **tooling detour** — the milestone/modeling work below is still pending. Options:

1. **Push the 6 commits.** Clean fast-forward to `origin/session/…`. Lowest-effort; gets the suite + harness + prereg + the prior Round 27 work onto origin.
2. **Run the M1 attack-type-LODO headline sweep on RunPod** — the big deferred deliverable: produces the per-type LODO gaps → the **write-gate-OPEN §6.5 verdict** (issue #2 falsification). **Both pre-launch blockers are now cleared (ADR-053):** the launch glue is **wired** (`scripts/runpod_sweep.py` → `load_job_spec→run_job` over `experiments/attack-type-lodo/runpod_lane1_sweep.yaml`, offline + live `--dry-run`-validated) and the spend is **base-budget** ($0 realized; `contingency_unlock_1.md` tally). Only the **paid launch** remains — your go-ahead + `RUNPOD_API_KEY` + a fresh `--dry-run` to confirm provider-side values (cheap 24 GB cards need the key + broader datacenters; the SECURE H100 fallback resolves in-budget now). Then `gpu-run-watcher` drives + watches it.
3. **Continue the milestone rethink** (the deferred M0→M7 re-ladder) → another `/exploring-options` round → Round 28 (± ADR-053).
4. **Dogfood the new suite on real work** — e.g. `adr-scribe` → draft the ADR recording the suite itself (worth ratifying; currently undocumented as an ADR); `dataset-auditor` → refresh the dataset survey via the new `--out` fan-out.

The formal `v0.1.0` M0 close is **NOT** on this list — deferred pending the milestone rethink.

---

## Current state (2026-05-30)

### The subagent suite (`1bfefaf`) — `.claude/agents/`
- `experiment-runner` (sonnet) — LOCAL smoke/minimal harness + §6.5 falsification + OOD parse → metrics + write-gate verdict.
- `dataset-auditor` (sonnet) — ONE HF dataset per call, fan-out, reads its own `--out` JSON → one status row.
- `gate-runner` (sonnet) — lint/test/contracts/ratify/dossier-audit → PASS/FAIL + actionable failures only.
- `gpu-run-watcher` (sonnet) — RunPod launch+watch via `scripts/runpod_sweep.py` (`load_job_spec→run_job`); poll + alert + guarded auto-kill (cost ceiling default $15 / no-progress default 20 min); drafts upstream friction. **Launch glue WIRED (ADR-053); paid launch user-gated.**
- `session-orienter` (opus) — cold-start briefing; never decides.
- `adr-scribe` (opus) — draft ADR / Round-update; never ratifies.
- Each has a tight OUTPUT CONTRACT + anti-pattern guardrails (counters the `BURN_IN_NOTES.md` failure modes). Verified: frontmatter valid, smoke sweep produces parseable `metrics.json`, `make lint/test/contracts` green.

### M1 harness (`695a739`) — `experiments/attack-type-lodo/`
- `folds.py` (core / obfuscation sub-split / external-carrier; purge-from-train for 11 shared BIPIA email contexts), `detectors.py` (4 rungs; device-adaptive precision — native bf16 Ampere+ else fp16), `metrics.py` (scorecard battery + per-type AUPRC + TPR@FPR), `harness.py` (sweep + strict-JSON + git-SHA MANIFEST), `falsify_ood_wall.py` (§6.5 write-gated verdict).
- `results/` is now **gitignored** (large runtime parquet; regenerated by the harness). Full sweep is RunPod-only (local OOMs at spec config).

### Pre-modeling EDA arc (Phases 0–3, prior sessions; M1's entry-gate)
- `experiments/eda/OOD_WALL_PREDICTION/` — pre-registered falsifiable collapse RANK. **Key finding: carrier dominates the MiniLM embedding** (silhouette by-carrier 0.197 vs by-type −0.023; KMeans→carrier ARI 0.98 vs →type −0.001) — attack-type signal is embedding-invisible. Reframes value-props, falsifies NO lane hypothesis.

### Plan doc + §16 Round-27 gates (unchanged this session)
- `PORTFOLIO_PLAN.md` reflects post-M0 reality; §16 carries the EDA M1 entry-gate + 3 conditional rescope trigger-gates (M1→M2 Lane 1b / M5-close Lane 4 / M3-entry Lane 5 — detail in `dossier_implications_for_roadmap.md` Zone 2).

### eval-toolkit — v1.6.0 shipped + consumed
- `~/Claude/eval-toolkit` `main` at v1.6.0 (PyPI). Portfolio pinned `eval-toolkit[probes,losses]>=1.6`. ⚠️ Concurrent work on branch `feat/review-eval-tooling` (dirty `loaders.py`) — do ALL eval-toolkit work in an isolated worktree off `origin/main`; never touch that checkout. **Always `uv sync --extra dev`** (bare `uv sync` prunes the dev extra).

---

## Read first (in order)
1. `.claude/delegation.md` — the subagent suite's When→Delegate→Invocation table (you can dogfood the agents this session).
2. `~/.claude/plans/i-want-o-have-async-bee.md` — this session's approved plan (the 6-agent design + 8 decisions + verification).
3. `docs/planning/PORTFOLIO_PLAN.md` — canonical plan; read the **Round 27 block** + **§16 gates** for the milestone framing.
4. `docs/planning/attack-type-lodo-harness-spec.md` — executable spec for the Lane-1 modeling phase (now implemented in `experiments/attack-type-lodo/`).
5. `experiments/lane-1/{hypothesis,protocol}.md` — the Lane-1 pre-registration (H-LANE-1; outcome pre-commitment + §6.5 falsification).
6. `decisions/contingency_unlock_1.md` — the RunPod unlock (DRAFT; budget classification pending `make cost-report`).
7. `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md` + `criteria.md` — Phase-3 result + the pre-registered falsification rule.
8. `decisions/ADR-052-…md` — locks the LODO study design; defers lane/chapter reorg to post-results.

## Open tracked items (GitHub Issues + Work-Tracker project #1)
- **#1** `tracked`/`P3`/`improvement` — Rerun V10 with Prompt-Guard-86M once its Meta Llama gate is granted (`run_v10_probes.py` skips PG1 gracefully today).
- **#2** `tracked`/`P2`/`research` — Falsify the OOD-wall prediction when Lane-1 produces per-type LODO gaps (the §6.5 step; now executable via the committed harness + `gpu-run-watcher`).

## Gotchas / open items
- **Working-style (single most important — borne out AGAIN):** present-first; interrogates inconsistencies; wants `/exploring-options`-style focused questions **before** convergence. This session: `ExitPlanMode` rejected in favour of exploring the agent design across 8 forks. **Surface real forks + ask before requesting approval; do not barrel into execution.**
- **🔑 Subagents are LIVE this session + you should use them.** See `.claude/delegation.md`. Present-first: they never decide forks, ratify, commit, push, or file public issues. The `.claude/settings.json` allowlist auto-approves safe read-only/local-run ops but **deliberately NOT the paid RunPod launch or git commit/push** → those always prompt.
- **`gpu-run-watcher` launch glue is WIRED (ADR-053, `4862e21`)** — there is no `runpod_deploy.Session`; the real API is `scripts/runpod_sweep.py` → `load_job_spec→run_job` over `experiments/attack-type-lodo/runpod_lane1_sweep.yaml`, validated via `--offline-dry-run` + a live `--dry-run`. Only the **paid launch** remains user-gated (go-ahead + `RUNPOD_API_KEY`).
- **Before any RunPod spend:** resolve `contingency_unlock_1.md` base-vs-contingency from the spend ledger — its required `make cost-report` attestation **does not exist yet** (slated M1).
- **Commit-trailer convention:** `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` (model-specific; matches the branch), NOT the generic global `git.md` form. All 3 commits this session used it.
- **6 commits UNPUSHED** — clean fast-forward to `origin/session/…` (upstream at `151db97`) when the user asks.
- **Milestones under rethink** — M0→M7 / formal `v0.1.0` close not settled.
- **PG1 (`meta-llama/Prompt-Guard-86M`) gate PENDING** Meta approval (403 as of 2026-05-29). PG2's gate WAS granted.
- **`uv sync --extra dev`** always (bare prunes the dev extra).
- **Disk:** healthy (~165 GB free); only model downloads / a real sweep pressure it.
- **Excluded (honest ceiling):** PINT + Indirect-in-the-Wild (un-loadable); BIPIA qa/abstract carriers (license-gated); gentellab (custom-parquet).
- **research-kb integration is a standing BOUNDARY** — separate session; do not touch.
- Session `TaskList` all `completed`; live follow-ups are GitHub issues #1/#2.

---

*↓ Prior handoff (2026-05-29 PM — "Phase-2 consolidation + Round 27 rethink") is superseded by the above (the suite shipped + the M1 harness/Lane-1 prereg got committed). Preserved in git history at `93ba8ee`.*
