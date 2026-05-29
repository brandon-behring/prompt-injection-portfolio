# Session handoff — 2026-05-29 (PM) — Phase-2 consolidation + Round 27 milestone rethink DONE

## ✅ START HERE — clean session

**Two things landed this session, both committed, neither pushed:**
1. **Plan reconciliation** (`2054a26`) — `PORTFOLIO_PLAN.md` §21 M0 checklist brought in line with `M0_READINESS.md` (19 technical gates ✓; the X/Mastodon announcement honestly kept **unchecked + DEFERRED**), drifted pins corrected, + a Round 24–26 / EDA-arc narrative block. (This commit was amended from `6a385ef` to fix its Co-Authored-By trailer.)
2. **Round 27 milestone rethink** (`e49918e`) — recorded the one *settled* structural change (the pre-modeling EDA arc = **M1's entry-gate**) and **registered the conditional Lane 1b/4/5 rescopes as §16 trigger-gates**, while **deferring the full lane/chapter re-ladder to post-LODO-results per ADR-052.**

**The big-picture fork from the prior handoff is RESOLVED** — the user chose Phase-2 consolidation (not "start Lane 1 now"), then "reconcile the plan," then a focused milestone rethink. **Do NOT re-present that fork as open.**

**⚠️ Milestones are under active reconsideration.** The user has signalled the M0→M7 ladder will be rethought; Round 27 captured only what's settled and the branch-points. **Treat the M0→M7 ladder as provisional, not a locked forward-plan**, and **the formal `v0.1.0` M0 close (tag / release / announcement) is DEFERRED pending that rethink** — do not push to close M0 formally.

**Git state:** `session/2026-05-26-adoption-and-research-ops`, **HEAD `e49918e`, AHEAD 2 / UNPUSHED** (origin tip is still `151db97`). Tree clean. eval-toolkit **v1.6.0** live on PyPI + `main`.

---

## What happened this session (2026-05-29 PM)

Entered from the prior handoff's fork. Worked it via `/exploring-options` (the user rejected `ExitPlanMode` and a first plan in favour of exploring) across several rounds:

- **Chose Phase-2 consolidation** over starting Lane 1. Then narrowed to **"reconcile the plan"** after exploration **falsified the handoff's "ROADMAP / ADRs / archive" framing**: ADRs were already done (50 files `ADR-001…052`, no stubs/gaps — nothing to draft); archive was trivial (dossier complete, tree clean). The only real work was a **doc desync**: `PORTFOLIO_PLAN.md` §21 said M0 was unstarted while `M0_READINESS.md` said done, and the round narrative dead-ended at Round 23.
- **`2054a26`** fixed that: §21 reconciled (honest-state — announcement stays `[ ]`), pins corrected (eval-toolkit `>=1.0`/v1.6.0, scaffold `^4.4.0`, submission ref `v1.3.0`), Round 24–26 narrative added.
- **Trailer fix:** `2054a26` was an amend of `6a385ef` to switch its Co-Authored-By to the repo's **model-specific** form. **House convention = `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`** (NOT the generic `Claude <…>` from global `git.md`) — match the last commits, not the global pattern.
- **`e49918e`** = Round 27 rethink (above). Key reasoning: the EDA findings (**carrier dominates the embedding; attack-type signal embedding-invisible**) **reframe value-props but falsify NO lane hypothesis**, and ADR-052 already defers lane reorg to post-results — so a full re-ladder now would be premature/speculative. Recorded the settled delta + registered triggers only.

This session's approved plan: `~/.claude/plans/use-the-following-to-rustling-adleman.md`.

---

## NEXT — three live options (confirm the fork with the user; do not barrel in)

1. **Push the 2 commits.** They're local-only per the commit-when-asked default. `git push` (no force needed — fast-forward over `151db97`). Lowest-effort; gets the reconciliation + Round 27 onto origin.
2. **Continue the milestone rethink.** The full M0→M7 re-ladder is the deferred piece. ADR-052 parks the *lane/chapter* reorganization until LODO results exist — but the user may want to rethink the ladder's *shape* (sequencing, the v0.7/0.8/0.9 guide pegs, the formal-close criteria) independently. If so: another `/exploring-options` round → Round 28 + possibly ADR-053.
3. **Start the ADR-052 attack-type-LODO study (Lane 1).** Still the unblocked modeling path; `docs/planning/attack-type-lodo-harness-spec.md` is the executable spec; reuse `experiments/eda/OOD_WALL_PREDICTION/bipia_carrier.py`. Produces the per-test-attack-type LODO gaps that **trigger the issue-#2 falsification** (§6.5). NOTE: this is now recorded as **M1's modeling step** (Round 27), and it's multi-session + GPU-bound (~12–18 GPU-hrs).

The formal `v0.1.0` M0 close is **NOT** on this list — deferred pending the milestone rethink (see START HERE).

---

## Current state (2026-05-29)

### Phases 0–3 (the pre-modeling EDA arc — all done; now recorded as M1's entry-gate)
- **Phase 0–2** (`9d0073d`): RC0 BIPIA go/no-go = **GO** (`experiments/eda/RC0_BIPIA/`); 13-dataset verified-spec survey (`configs/data/dataset_specs.yml`, `experiments/eda/survey_v2.py`, `ledger_corrections.md`).
- **Phase 3** (`0e49792`..`380cc43`) — `experiments/eda/OOD_WALL_PREDICTION/`:
  - `criteria.md` — pre-registration, **attested before any metric/model** (the anti-prototype crux).
  - `results.json` + `FINDINGS.md` — the falsifiable per-test-attack-type **collapse RANK**. top-4 predicted-worst = the **task-intent** types (Task Automation, Business Intelligence, Conversational Agent, Research Assistance); bottom-4 = Reverse Text / Substitution Ciphers / Scams&Fraud / Misinfo.
  - Figures V5 / V9 / A1 / V4 (UMAP) / V10 / D2; drivers `bipia_carrier.py` + `run_prediction.py` / `run_a1_v4.py` / `run_v10_probes.py` / `run_audit_matrix.py`.
  - **Key finding:** the **carrier dominates the MiniLM embedding** — silhouette by-carrier 0.197 vs by-attack-type −0.023; KMeans→carrier ARI 0.98 vs →type −0.001. The attack-type signal is embedding-invisible. (BIPIA also lexically subtle; uncontaminated — 0.0 near-dup vs the 8-dataset working set.)

### Plan doc (after this session)
- `PORTFOLIO_PLAN.md` now reflects post-M0 reality: §21 reconciled; Round 24–26 + **Round 27** narrative blocks; §16 carries the EDA M1 entry-gate + 3 conditional rescope trigger-gates.
- **§16 Round-27 gates** (registered branch-points; each fires only on its trigger — full detail in `dossier_implications_for_roadmap.md` Zone 2):
  - *M1→M2 (Lane 1b):* if M1 confirms `hackett2025bypassing` 100% char-injection ASR ±5pp → cut 12-technique → 3 representative + severity ranking.
  - *M5-close (Lane 4):* if 2-of-3 {PINT, PromptShield, WildGuardMix} saturate >95% AUPRC on the stacker → pivot headline to LLMail-Inject.
  - *M3-entry (Lane 5):* if encoder probe d′ ≤ 0.5 → falsify port-only, promote surface-third-path (CaMeL).
- **§9 "8 milestones M0-M7" header unchanged** (EDA = entry-gate, no new rung). The committed Round 24–26 narrative was left intact (historical record).

### eval-toolkit — v1.6.0 shipped + consumed
- `~/Claude/eval-toolkit` `main` at **v1.6.0** (PyPI, Trusted Publishing). `eda` Tier-2 layer complete (Job-1 #83 / `HFDatasetsLoader` #85 / Job-2 #86→V5 / Job-3 #87→V9).
- ⚠️ **Concurrent work** on eval-toolkit branch `feat/review-eval-tooling` (dirty `loaders.py`). **Do ALL eval-toolkit work in an isolated worktree off `origin/main`** (`git worktree add -b <br> /tmp/etk-pr origin/main`); never touch that checkout. (`gh` from `/tmp` needs `GIT_DISCOVERY_ACROSS_FILESYSTEM=1 gh ... -R brandon-behring/eval-toolkit`.)
- Portfolio pinned **`eval-toolkit[probes,losses]>=1.6`** (`uv.lock` 1.6.0; `library_imports.md` R28). **Always `uv sync --extra dev`** — bare `uv sync` PRUNES the 92-pkg dev extra.

---

## Read first (in order)
1. `docs/planning/PORTFOLIO_PLAN.md` — the canonical plan; read the **Round 27 block** (after Round 24–26, before §1) + the **§16 Round-27 gates** for the current milestone framing.
2. `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md` — the Phase-3 result + the pre-modeling prediction.
3. `experiments/eda/OOD_WALL_PREDICTION/criteria.md` — the pre-registered method + falsification rule.
4. `docs/planning/attack-type-lodo-harness-spec.md` — executable spec for the Lane-1 modeling phase.
5. `docs/planning/dossier_implications_for_roadmap.md` (Zone 2) — the canonical home of the Lane 1b/4/5 rescope rationale the §16 gates reference.
6. `~/.claude/plans/use-the-following-to-rustling-adleman.md` — this session's approved plan (consolidation + Round 27).
7. `decisions/ADR-052-…md` — locks the LODO study *design*; **defers lane/chapter reorg to post-results** (the constraint that bounded Round 27).

## Open tracked items (GitHub Issues + Work-Tracker project #1)
- **#1** `tracked`/`P3`/`improvement` — **Rerun V10 with Prompt-Guard-86M once its Meta Llama gate is granted.** PG1 (the only indirect-valid probe) is gated-pending; protectai-v2 + PG2 are direct-scope, blind to BIPIA indirect. Fix = rerun `run_v10_probes.py` (it skips PG1 gracefully today).
- **#2** `tracked`/`P2`/`research` — **Falsify the OOD-wall prediction** when Lane-1 produces per-type LODO gaps (top-k vs bottom-k; the §6.5 step).

## Gotchas / open items
- **Working-style (the single most important note — borne out AGAIN this session):** the user is present-first / interrogates inconsistencies / wants `/exploring-options`-style focused questions **before** convergence. This session: `ExitPlanMode` + a first plan were rejected in favour of exploring; the milestone framing was interrogated before converging. **Surface real forks + ask before requesting approval; do not barrel into execution.**
- **Commit-trailer convention:** use **`Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`** (model-specific; matches the branch), NOT the generic `Claude <…>` form in global `git.md`. A commit this session was amended to fix exactly this.
- **2 commits are UNPUSHED** (`ahead 2`); push is a fast-forward over `151db97` when the user asks.
- **Milestones under rethink** — don't treat M0→M7 / the formal `v0.1.0` close as settled (see START HERE).
- **PG1 (`meta-llama/Prompt-Guard-86M`) gate is PENDING** Meta approval (re-checked 2026-05-29: 403). PG2's gate WAS granted. `model_info()` succeeding for a gated repo ≠ download access.
- **`uv sync --extra dev`** always (bare prunes dev).
- **Disk:** healthy (**165 GB free**). Phase-3 EDA is BIPIA-internal (tiny); only the audit matrix / model downloads pressure disk.
- **Excluded (honest ceiling):** PINT + Indirect-in-the-Wild (un-loadable); BIPIA qa/abstract carriers (license-gated); gentellab (custom-parquet).
- **research-kb integration is a standing BOUNDARY** — handled in a separate session; do not touch.
- Session `TaskList` is all `completed`; live follow-ups are GitHub issues #1/#2.

---

*↓ Prior handoff (2026-05-29 AM — "Phase 3 COMPLETE; fork: Lane-1-modeling vs consolidation") is superseded by the above: the fork was resolved (consolidation → reconcile → Round 27 rethink). Preserved in git history at `151db97`.*
