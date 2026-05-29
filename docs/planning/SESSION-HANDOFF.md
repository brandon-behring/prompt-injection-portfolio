# Session handoff — 2026-05-29 — Phase 3 COMPLETE; pre-modeling EDA arc CLOSED

## ✅ START HERE — clean session

**The entire pre-modeling dataset-EDA arc (Phases 0–3) is DONE.** The project's defining goal —
*rigorous, evidence-based EDA before any modeling, so we don't repeat the predecessor's "assumed
data → post-hoc OOD wall" failure* — is achieved: a **falsifiable, pre-registered OOD-wall
prediction is recorded pre-modeling** in `experiments/eda/OOD_WALL_PREDICTION/`.

**The natural next phase is the modeling study itself — the ADR-052 attack-type-LODO experiment
(Lane 1)** — for which `docs/planning/attack-type-lodo-harness-spec.md` is the executable spec.
Running it produces the per-test-attack-type LODO gaps that **trigger the OOD-wall falsification**
(tracked issue **#2**). Alternative: Phase-2 consolidation (ROADMAP/ADRs/archive). **Confirm the
fork with the user before converging** (see the working-style note in Gotchas).

**Git state:** portfolio session branch `session/2026-05-26-adoption-and-research-ops` pushed
through **`380cc43`**. eval-toolkit **v1.6.0** live on PyPI + `main`.

---

## Current state (2026-05-29)

### eval-toolkit — v1.6.0 shipped + consumed
- `~/Claude/eval-toolkit` `main` is at **v1.6.0** (PyPI, Trusted Publishing, receipt verified).
  The `eda` Tier-2 layer is complete: **Job-1** integrity gate (`audit_dataset`/`DataAudit`/
  `SplitSummary` + 3 gates + obfuscation, #83), schema-aware **`HFDatasetsLoader`** (#85),
  **Job-2 `lexical_association`** (C1 log-odds/PMI + C2 competency baselines, #86 → V5),
  **Job-3 `distribution_shift`** (E1 PAD[linear+CV] + unbiased-RBF-MMD[perm p] + kNN purity,
  #87 → V9). All 100% line+branch cov, CI-green, squash-merged.
- ⚠️ **Concurrent work** lives on eval-toolkit branch `feat/review-eval-tooling` (dirty `loaders.py`).
  **Do ALL eval-toolkit work in an isolated worktree off `origin/main`** (`git worktree add -b <br>
  /tmp/etk-pr origin/main`) — never touch that checkout. (`gh` from a `/tmp` worktree needs
  `GIT_DISCOVERY_ACROSS_FILESYSTEM=1 gh ... -R brandon-behring/eval-toolkit`.)
- Portfolio pinned **`eval-toolkit[probes,losses]>=1.6`** (`uv.lock` 1.6.0; `decisions/library_imports.md`
  R28). **Always `uv sync --extra dev`** — bare `uv sync` PRUNES the 92-pkg dev extra.

### Phases 0–3 (all done)
- **Phase 0–2** (`9d0073d`): RC0 BIPIA go/no-go = **GO** (`experiments/eda/RC0_BIPIA/`); 13-dataset
  verified-spec survey (`configs/data/dataset_specs.yml`, `experiments/eda/survey_v2.py`,
  `ledger_corrections.md`); ledger corrected in place.
- **Phase 3** (`0e49792`..`380cc43`) — `experiments/eda/OOD_WALL_PREDICTION/`:
  - `criteria.md` — pre-registration, **attested before any metric/model** (the anti-prototype crux).
  - `results.json` + `FINDINGS.md` — the falsifiable per-test-attack-type **collapse RANK** (fused
    E1 shift + C1/C2 shortcut; weighted rank-average). **top-4 predicted-worst = the task-intent
    types** (Task Automation, Business Intelligence, Conversational Agent, Research Assistance);
    bottom-4 = Reverse Text / Substitution Ciphers / Scams&Fraud / Misinfo.
  - Figures: **V5** (log-odds + competency) · **V9** (PAD/MMD) · **A1** (cube) · **V4** (UMAP) ·
    **V10** (probe distributions) · **D2** (cross-dataset audit). Drivers: `bipia_carrier.py` +
    `run_prediction.py` / `run_a1_v4.py` / `run_v10_probes.py` / `run_audit_matrix.py`.
  - **Key finding:** the **carrier dominates the MiniLM embedding** — silhouette by-carrier 0.197 vs
    by-attack-type −0.023; KMeans→carrier ARI 0.98 vs →type −0.001; carrier+attack external PAD 2.0
    ≫ core 0.51. The attack-type signal is embedding-invisible. (Also: BIPIA attacks are lexically
    subtle; BIPIA is uncontaminated — 0.0 near-dup vs the 8-dataset working set, within-dataset floor ≈0.)

### Governance
- **ADR-051 amendment** (narrow): the local GPU ML stack (torch/sentence-transformers + `umap-learn`,
  now in `[dev]`) is authorized **strictly for pre-modeling EDA in `experiments/eda/`**, not lane code.
- **`attack-type-lodo-harness-spec.md`**: §5 **retention pre-commit** (Lane-1 MUST persist per-type
  diagnostic AUPRCs) + §6.5 **post-run falsification step** (run the OOD-wall test on them).

---

## NEXT — the ADR-052 attack-type-LODO modeling study (Lane 1)

**Goal:** execute the honest attack-type-generalization study the EDA gated — train detectors
(frozen-probe / LoRA / full-FT, fair per-rung val-selection) on BIPIA train-attack-types, test on the
disjoint test-types, and measure the OOD collapse. **`docs/planning/attack-type-lodo-harness-spec.md`
is the executable spec.** Reuse `experiments/eda/OOD_WALL_PREDICTION/bipia_carrier.py` (the
carrier-preserving loader). The study must (per the spec) **persist the per-test-attack-type
diagnostic AUPRCs**, then **run the OOD-wall falsification** (§6.5) → records SURVIVES/FALSIFIED →
closes tracked issue #2.

This is **modeling** (was out-of-scope for the EDA plan) → its own phase/plan. Confirm with the user
whether to start it, or do Phase-2 consolidation (ROADMAP/ADRs/archive) first.

## Read first (in order)
1. `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md` — the Phase-3 result + the pre-modeling prediction.
2. `experiments/eda/OOD_WALL_PREDICTION/criteria.md` — the pre-registered method + falsification rule.
3. `docs/planning/attack-type-lodo-harness-spec.md` — the executable spec for the next (modeling) phase.
4. `docs/planning/eda-design.md` — the A–F / V1–V11 catalog (design source of truth).
5. `docs/planning/prototype-postmortem.md` — the failure list the whole arc is built to break.
6. `~/.claude/plans/we-are-very-behind-fizzy-hearth.md` — this session's approved plan (the EDA arc, fully executed).

## Open tracked items (GitHub Issues + Work-Tracker project #1)
- **#1** `tracked`/`P3`/`improvement` — **Rerun V10 with Prompt-Guard-86M once its Meta Llama gate is
  granted.** PG1 (the only indirect-valid probe) is gated-pending; protectai-v2 + PG2 (loaded) are
  direct-scope and blind to BIPIA indirect injection. Fix = rerun `run_v10_probes.py` (it skips PG1
  gracefully today).
- **#2** `tracked`/`P2`/`research` — **Falsify the OOD-wall prediction** when Lane-1 produces per-type
  LODO gaps (top-k vs bottom-k; the §6.5 step).

## Gotchas / open items
- **Working-style (the single most important note — borne out twice this session):** the user
  present-first / interrogates inconsistencies / wants `/exploring-options`-style focused questions
  **before** convergence. `ExitPlanMode` was rejected twice this session in favour of exploring
  options. Surface real forks + ask before requesting approval; do not barrel into execution.
- **PG1 (`meta-llama/Prompt-Guard-86M`) gate is PENDING** Meta approval (re-checked 2026-05-29: 403).
  PG2's gate WAS granted. `model_info()` succeeding for a gated repo ≠ download access.
- **eval-toolkit concurrent branch** `feat/review-eval-tooling` — use worktrees off `origin/main`.
- **`uv sync --extra dev`** always (bare prunes dev). The v1.6.0 PyPI index had a brief CDN lag —
  if `uv lock --upgrade-package eval-toolkit` says "unsatisfiable," just retry.
- **Disk:** healthy now (**165 GB free**); was 97% full early-session (external cleanup + I removed 4
  out-of-working-set HF datasets). Phase-3 EDA is BIPIA-internal (tiny); only the audit matrix /
  model downloads pressure disk.
- **Excluded (honest ceiling):** PINT + Indirect-in-the-Wild (un-loadable); BIPIA qa/abstract carriers
  (license-gated); gentellab (custom-parquet, skipped in the audit matrix loop).
- **research-kb integration is a standing BOUNDARY** — handled in a separate session; do not touch.
- Session `TaskList` (#8–#23) is all `completed`; the live follow-ups are GitHub issues #1/#2.

---

*↓ Prior handoff (2026-05-28 PM — "Phase 1 Step 2 next", PR-1 open) is superseded; preserved in git
history. The above is the current source of truth.*
