# Session handoff — 2026-06-01 — M1 LoRA headline sweep DONE; §6.5 OOD-wall **FALSIFIED** (capacity-dependent); push + milestone-rethink remain

## ✅ START HERE — clean session

**The M1 attack-type-LODO LoRA headline sweep is COMPLETE, and §6.5 has a verdict.** The paid RunPod H100
run trained `lora × 3 folds × 3 seeds` (**~$0.83 realized**), was merged with the local `tfidf`+`frozen`
tree, the §6.5 **write-gate OPENED**, and the falsification verdict is persisted. Everything is committed
(unpushed). The remaining work is **push + the milestone rethink** — no more paid compute is queued.

**The headline result — the OOD wall is capacity-dependent:**

| rung | representation | T (top−bottom per-type AUPRC) | perm p | CI-low | verdict |
|---|---|---|---|---|---|
| tfidf | lexical | +0.135 | 0.014 | +0.111 | SURVIVES |
| frozen | frozen MiniLM emb + LogReg | +0.082 | 0.014 | +0.064 | SURVIVES |
| **lora** | **end-to-end ModernBERT FT** | **−0.003** | **0.900** | **−0.008** | **FALSIFIED** |

Judged on `lora` per criteria **Revision 2** → **FALSIFIED at the ceiling**. `T` collapses monotonically as
capacity rises: the pre-modeling OOD-wall prediction (built on the frozen MiniLM embedding, where the
carrier dominates) **does not transfer** to an end-to-end LoRA, which detects every attack type near-uniformly
(test AUPRC 0.98–0.999, held-out included). This is the **pre-registered S2 encoder-transfer caveat, realized** —
and it's credible *because* the rule + tail sets + judged-rung were fixed before any LoRA datum existed and
write-gated. Record: `experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json` + `FINDINGS.md` §"Realized
verdict" + `criteria.md` footer. **Issue #2 CLOSED.**

**Five commits this session (branch `session/2026-05-26-adoption-and-research-ops`; ALL UNPUSHED):**
1. **`81d7093`** — ADR-054: defer `full_ft` to a trigger-gate, `lora` = M1 ceiling, hybrid local+RunPod,
   `REQUIRED_RUNGS` decoupling, off-the-shelf reference column, criteria Revision 2.
2. **`d187a50`** — fail-fast GPU guard in the pod run-script + DF-5 (pricing-403) logged.
3. **`f0f1523`** — the LoRA verdict + FINDINGS/criteria realized-verdict record + budget actuals
   ($0.83) + the `falsify_ood_wall.py` relative-path fix + the `rsync` setup step + DF-6.
4. **(pending, this handoff's commit)** — DF-6 → filed as [runpod-deploy#116] + this handoff refresh.

**Cost:** $0.83 realized of the $250 base (base-budget; ADR-014 stays Reserved; « the $350 hard cap).

---

## NEXT — live options (confirm the fork with the user; present-first)

1. **Push the branch** — 3+ commits unpushed (user-led; the push itself always prompts).
2. **`full_ft` trigger-gate decision (§16, ADR-054).** The trigger fires iff LoRA SURVIVES with a real
   capacity lift **or** is borderline such that the never-measured full-FT OOD point would change the writeup.
   **The verdict is FALSIFIED (no wall at LoRA capacity)** → more capacity (full-FT) would only dissolve it
   further → **no decision-relevant info → the trigger does NOT fire; `full_ft` stays deferred.** (Record this
   if ratifying ADR-054 / closing the gate.)
3. **Milestone rethink — DEFERRED to a fresh session; inputs captured.** The post-LODO-results re-ladder
   condition (Round 27 / ADR-052) is now **met**; M1's implications are distilled in
   **`docs/planning/milestone-rethink-inputs.md`** (the read-first brief). M0→M7 still provisional; the
   formal `v0.1.0` M0 close stays user-led. Pick up the full re-ladder fresh → `/exploring-options` → ADR-055+.
4. **Optional housekeeping:** file **DF-5** (pricing-403) upstream (drafted in `upstream_issues.md`; user-led);
   address new **issue #3** (scrub absolute `/home/` paths from the repo); rerun `run_v10_probes.py` with **PG1**
   now its Meta gate is cleared (**issue #1**).

---

## Current state (2026-06-01)

### §6.5 falsification — COMPLETE
- Write-gate OPEN on the merged `tfidf+frozen+lora` 3-rung tree (3 seeds × 3 folds). Verdict FALSIFIED on
  `lora`, persisted to `OOD_WALL_PREDICTION/falsification_verdict.json`. Cross-rung table reproducible via
  `falsify_ood_wall.py --rung {tfidf,frozen,lora}` (or `falsify_clustered.compute_verdict` directly to avoid
  overwriting the persisted `lora` verdict).
- `results/` holds the full merged tree (`tfidf+frozen+lora`, gitignored); RunPod telemetry in
  `artifacts/runpod/20260601T174326Z/` (gitignored). The committed record is the verdict JSON + FINDINGS.

### RunPod launch — DONE (ADR-053 + ADR-054)
- `runpod_lane1_sweep.yaml` (LoRA-only, SECURE H100 resolved at launch, `cost_cap=8`/`max_runtime=180`,
  `on_success: delete`) + `scripts/runpod_sweep.py`. **Two run-script hardenings landed:** the fail-fast GPU
  guard (`assert torch.cuda.is_available()`) and a `setup:` step that `apt-get install`s `rsync` (lean base
  image lacks it — DF-6/#116). Pod `j6xy6h8wi7ycfu` deleted; billing stopped.
- **Wrapper logging gotcha:** `scripts/runpod_sweep.py` configures NO logging → run with
  `logging.basicConfig(level=INFO)` (via an importlib shim) to see `run_job` price/plan/progress.
- **API key:** not in the environment — source inline from `~/.runpod/config.toml` (`apikey`, 50 chars);
  `runpodctl` reads it natively.

### Off-the-shelf reference column (local, non-gating)
- `reference_scorers.py`: ProtectAI + PG1 + PG2 scored on the 3 LODO test folds (`reference_*.test_scores.parquet`,
  outside `REQUIRED_RUNGS`). PG1 gate is CLEARED (issue #1 unblocked).

### Pre-modeling EDA arc + subagent suite + eval-toolkit
- EDA `OOD_WALL_PREDICTION/` (carrier dominates the MiniLM embedding → the §6.5 prediction, now FALSIFIED at
  the LoRA ceiling). The six `.claude/agents/` are LIVE + heavily dogfooded (experiment-runner ran the LoRA
  smoke; gpu-run-watcher drove the paid sweep). eval-toolkit v1.6.0 pinned.

---

## Read first (in order)
1. `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md` §"Realized verdict" — the headline + capacity-dependent reading.
2. `experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json` — the machine-readable verdict.
3. `experiments/eda/OOD_WALL_PREDICTION/criteria.md` — the pre-registration (incl. Revision 2 + the record-only verdict footer).
4. `decisions/ADR-054-m1-lora-ceiling-full-ft-deferred.md` — the M1 ceiling / hybrid / trigger-gate decision (awaiting ratification).
5. `decisions/contingency_unlock_1.md` — the $0.83 realized tally (base-budget, RESOLVED).
6. `decisions/upstream_issues.md` — DF-5 (pricing-403, pending) + DF-6 (rsync, filed #116).

## Open tracked items (GitHub Issues + Work-Tracker #1)
- **#2** — §6.5 OOD-wall falsification — **CLOSED** (FALSIFIED at the LoRA ceiling).
- **#3** `tracked` — Scrub absolute `/home/` paths from the repo (opened 2026-06-01). Not yet triaged.
- **#1** `P3`/`improvement` — Rerun V10 with PG1 (Meta gate now CLEARED → unblocked).

## Gotchas
- **Working-style (most load-bearing):** present-first; interrogates inconsistencies; wants `/exploring-options`
  forks **before** convergence. This session the user caught a launch that was verified only for GPU-*use* but
  not end-to-end *runnability* — a local LoRA code-path smoke gate was added before paying. Surface real forks;
  do not barrel into execution or commits.
- **Commit trailer:** `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>` (model-specific).
- **Paid launch + git push always prompt** (not auto-approved). Filing public issues is user-led (the user
  directed the DF-6 / #116 filing explicitly).
- **`uv sync --extra dev`** always. eval-toolkit work → isolated worktree off `origin/main`.
- **Milestones under rethink** — M0→M7 / formal `v0.1.0` close not settled.
- The `full_ft` rung stays selectable (`--rungs full_ft`); its trigger did NOT fire (see NEXT #2).

---

*↓ Prior handoff (2026-05-30 PM — "M1 pre-launch gate COMPLETE; only the paid launch remains") is superseded
by the above: the launch ran (~$0.83), the §6.5 verdict came back FALSIFIED at the LoRA ceiling, and issue #2
closed. Preserved in git history at `6db5c45`.*
