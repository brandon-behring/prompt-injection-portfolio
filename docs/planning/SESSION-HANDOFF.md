# Session handoff — 2026-06-11 (PM) — C1 ARC CLOSED: lora paid go RAN → verdict **NOT-CLOSED** → 5-verifier audit **ROBUST** · Round-32 draft + C2 draft await ratification · [prior arcs below SUPERSEDED]

> **🆕 LATEST (2026-06-11, afternoon) — the C1 decision datum is in, audited, and recorded; everything below the suggested commits is user-led.**
>
> **The lora paid go RAN** (`runpod_c1_sweep.yaml` wired + committed `7525c77`; offline + price dry-runs green; H100 80GB SECURE @ $3.29/h, pod 09:04→09:31 ≈ 26.8 min ≈ **$1.47**; `.env.local` verified never-staged; pull → `C1_results_runpod_lora/`, merged sha-verified into `C1_results_treated/`, pod deleted only after the verified pull). **Verdict (pre-locked rule, judged at `lora`): NOT-CLOSED** — G_control +0.2054 / G_treated +0.2333 / ΔG **−0.0279** (CI-low −0.0319 ≤ 0). The frozen-rung reduction (ΔG +0.0830, CI-low +0.0788) **did not survive the decision rung**; targeted format-matched table data does not bridge the residual table wall at the ceiling. `c1_verdict.json` written through the W3 gate (first write). Total C1 datum cost ≈ **$1.74** (corpus $0.27 + lora $1.47).
>
> **5-verifier adversarial audit → ROBUST** (`experiments/carrier-table-training/AUDIT_C1_2026-06-11.md`): REPRODUCES exact (Δ=0.0 ×9; lora ΔG ~11.6 sd < 0) · SOUND (treated test row-identical to control ×9; W4 pairing verified; sha chain holds incl. pod files) · LEAK-FREE (all seeds, full re-derivation; the committed gate only scanned seed-0 — closed empirically, 0 hits) · COMPLIANT (0 material deviations) · narrative CORRECTIONS required (audit **F5**, use in all downstream prose): **G_control(tfidf) = −0.148** not −0.149 · REDUCED/CLOSED labels exist only at `lora` (say "frozen-rung reduction … did not survive the decision rung") · never "treated wall grew" (not seed-robust: −0.006 without control seed-0) · the tfidf move is **val-side** (the ratified "no wall at tfidf" reading STANDS; "negative-gap artifact normalizes" was unsupported) · B+ analogy scoped "does-not-bridge at the lora ceiling" · **NotInject secondary readout: no over-defense price paid, no wall bought down** (treated mean 0.705 vs control 0.729, n=113).
>
> **▶ NEXT (all user-led, present-first):**
> 1. **Approve the suggested commits** (presented in-session): (a) C1 verdict + audit + merged lora artifacts + re-stamped MANIFEST + this handoff + memory; (b) optionally the C2 draft. Then push.
> 2. **Ratify Round 32** — draft at `docs/planning/round-32-update.DRAFT.md` (paste into PORTFOLIO_PLAN + delete the draft). It carries the open fork: an **ADR-055 carrier-line amendment** ("residual table wall is data-resistant at the ceiling") — a user decision.
> 3. **Ratify C2** — `experiments/mechanism-style-content/criteria.DRAFT.md` (style-vs-content mechanism probe; frozen-detector scoring of a same-generator 2×2 counterfactual corpus; cheap rungs $0; 11 TBDs flagged for adjudication).
> 4. Parked, unchanged: research_toolkit **PR #38 merge** · v0.1.0 A(b) close HELD on accounts · DF-11/#93 carrier re-lock. Audit follow-ups (LOW, if C1 tooling is reused): widen `leakage_gate.py`'s frame loop beyond seed-0; make `run_c1.py` verify the gate report's corpus sha matches `--corpus`.
>
> **Read-first:** this block → `experiments/carrier-table-training/AUDIT_C1_2026-06-11.md` (incl. the F5 required phrasings) → `c1_verdict.json` → `docs/planning/round-32-update.DRAFT.md` → memory `[[c1-carrier-table-arc]]`.

---

# Session handoff — 2026-06-11 — C1 CHEAP-RUNG ARC DONE + PUSHED (frozen wall REDUCED, ΔG +0.083) · NEXT = the C1 `lora` paid go · [SUPERSEDED by the block above — the lora go has since RUN (verdict NOT-CLOSED, audit ROBUST); per audit F5: tfidf G_control is −0.148, and this block's "REDUCED" headline was an informal cheap-rung label, not a verdict]

> **🆕 LATEST (2026-06-10/11) — C1 (Lane 2 / M2) ratified AND executed through the cheap rungs in one stretch; everything PUSHED (`…5c90d1b`, branch in sync).**
>
> **Ratification (4 modals):** `experiments/carrier-table-training/criteria.md` RATIFIED as-drafted · **spend scope**: corpus ≤$5 + cheap rungs covered by ratification, **`lora` = its own present-first paid go** · #22 gate = demonstrate-not-on-path · v0.1.0 stays held on accounts. The #22 trace found `_extract_text` **ON-PATH** (silent empty-row corpus poisoning) → escalated per the pre-adjudicated rule → fixed upstream as **research_toolkit PR #38** (`fix/21-empty-response-loud`; the `.tooling` clone SITS ON that branch — corpus gen must run from it). **criteria Revision 1 (pre-datum):** Anthropic credits were empty → generation on **OpenAI `gpt-4.1-mini`** via `generate_openai.py` (an Anthropic-interface adapter into the SAME `synthesize()` orchestrator — cap/resume/PR#38 gate retained; key = repo `.env.local`, gitignored).
>
> **Results ($0.27 total):** 600/600 benign table contexts (zero hygiene drops) → corpus **1800 pos / 600 neg** (28 attack types, mechanical BIPIA-pool suffix-injection, `context_sha256` on every row; parquets COMMITTED, 320K) → **leakage gate 0 exact / 0 near** → cheap rungs ×3 seeds **CPU-only** (`CUDA_VISIBLE_DEVICES=""` — the shared 2070S OOMs; first attempt died on it) → **readout:** tfidf G −0.149→−0.013 (the control's negative-gap artifact normalizes) · **frozen G +0.334→+0.251, ΔG +0.083 (CI-low +0.079 > 0) — a REAL, CI-supported reduction; the wall persists ≫ 0.05 SESOI.** Write-gate verified CLOSED at `lora` (0 treated seeds). Gates: lint+mypy+83 tests+13 contracts green.
>
> **▶ NEXT (user-led): the C1 `lora` paid go** (~$1–5 RunPod; treated arm only, 3 seeds × held-table fold; control = `../attack-type-lodo/results` as-committed, NEVER re-run; control anchor G_table(lora) = +0.205):
> 1. Wire `runpod_c1_sweep.yaml` (mirror `runpod_carrier_lodo_sweep.yaml`; **cheap-first `gpu_order`** per cross-family Rev 9 — 4090/A5000 before L40S/H100; excludes scoped `experiments/**/*.parquet`; cap ~$8). The pod runs `run_c1.py --rungs lora` — `corpus_gated.parquet` is COMMITTED, so the pod has everything.
> 2. Monitor with a **plain bash monitor** (NO gpu-run-watcher agent — it over-polls to death; verify-before-delete; DF-12 lessons). Pull `seed=*/carrier_lodo_table/lora.{predictions.parquet,metrics.json}` into `C1_results_treated/`.
> 3. `c1_verdict.py` — rule PRE-LOCKED (CLOSED iff G_treated(lora)<0.05 AND CI-low(ΔG)>0 · REDUCED iff CI-low>0 ≥SESOI · NOT-CLOSED iff CI-low≤0; W4 independent-per-seed paired bootstrap; W10 dual reading; `--out`/`--force` overwrite gate live) → **multi-verifier adversarial audit** (B4 pattern) → **Round 32** entry in PORTFOLIO_PLAN.
> 4. **C2 mechanism pre-reg drafts during the GPU wait** (Round 31 decision; style-vs-content, the W12 Mirror confound is the design driver).
>
> **Also open:** research_toolkit **PR #38 merge** (+ optional BURN_IN_NOTES dogfood entry — the C1 run was the skill's first real burn-in: 600/600 clean, billing-failure recovery exercised, EmptyResponse gate never fired) · v0.1.0 A(b) close HELD on accounts (`M0_READINESS.md`; session branch now 45 ff-able commits) · DF-11/#93 + carrier n=5 when-unblocked.
>
> **Read-first:** this block → `experiments/carrier-table-training/criteria.md` (incl. the gate-check note + Revision 1) → `c1_verdict.py` docstring → memory `[[c1-carrier-table-arc]]`.

---

# Session handoff — 2026-06-10 (LATE) — Round 31 RATIFIED · roadmap = STANDING SURFACE (forks A/B/C all decided) · P1.5 hardening + C1 pre-reg draft in flight · [SUPERSEDED by the block above — C1 since ratified + cheap rungs done]

> **🆕 LATEST (2026-06-10, post-audit-commit) — consolidation COMMITTED + PUSHED (`d92426a`); Round 31 ratified; every roadmap fork decided.**
>
> **Round 31 is IN `PORTFOLIO_PLAN.md`** (pasted after Round 30; the DRAFT file deleted). Six locked decisions: full re-audit PASSED (spine holds, zero BLOCKERs) · agent-harness-v0 = retrospective trio, **own surface** · provenance (b) · v0.1.0 = Fork **A(b)** (HELD on accounts) · milestone-rethink retired · **Fork C = C1: Lane-2 carrier/table training is the next experiment** (pre-registration first; C2 drafts during C1 GPU waits; P1.5 precedes everything).
>
> **`docs/planning/roadmap-refresh-2026-06-09.md` is the STANDING ROADMAP SURFACE** (header promoted from DRAFT): P0 **DONE** (`d92426a`) · P1 **HELD** (accounts) · P1.5 **IN PROGRESS** (this session: W1–W18 full package, $0 local) · P2 = **C1** (criteria.DRAFT this session → separate present-first ratification before any run).
>
> **This session's stretch (approved plan):** Round-31 paste ✓ → roadmap promotion ✓ → P1.5 full hardening (W3 write-gate, W17 leakage-gate fix, W2 injecagent fix + slice retirement, W1 email-only silhouette, W16 PAD CI, W9 PG1 provenance, disclosure batch W4/5/10/11/12/13/14/15, W18 archive) → `experiments/carrier-table-training/criteria.DRAFT.md`. Commits suggested at checkpoints, user-approved.
>
> ⚠️ Until W3 lands: do NOT run `falsify_ood_wall.py` casually — it overwrites the committed `falsification_verdict.json`.

---

# Session handoff — 2026-06-10 — FULL RE-AUDIT PASSED (spine holds, 30 verifiers + codex/gemini) · consolidation APPLIED · [SUPERSEDED by the block above — consolidation since committed `d92426a`, Round 31 ratified]

> **🆕 (2026-06-09/10) — the user-elected FULL RE-AUDIT of every ratified verdict is DONE and the spine HOLDS.**
>
> **Audit:** 30 adversarial verifiers (5 roles × 6 arcs) + mechanical reproduction (verdict scripts Δ=0 point-exact; **162/162** parquet recomputes Δ=0.0; bit-exact tfidf retrains ×4) + codex/gemini refutation (codex 36-CONFIRMED/6-WEAKENED/0-REFUTED; gemini's one refutation failed artifact-grounding). **attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family SURVIVES — zero BLOCKERs.** Record: `docs/planning/consolidated-audit-2026-06-09.md` (15 FIX-NOW applied / 18 FOLLOW-UP / 10 cosmetic). Two NEW substantive findings: **W1** MiniLM-256 truncation artifact (66.5% table / 44.1% code positives truncated out of the EDA embedder — email-only re-check owed) · **W2** InjecAgent materialization bug (placeholder concatenated, not substituted; conservative for verdicts).
>
> **Checkpoint decisions (user, 2026-06-10):** FIX-NOWs apply-all (DONE, in working tree) · agent-harness-v0 = **retrospective record trio** (criteria/FINDINGS/verdict EXPLORATORY-VALIDATED, claim-fenced) · RunPod provenance = **(b)** 28 metrics.json + `B3_PROVENANCE_MANIFEST.md` enter git, parquets gitignored · v0.1.0 = **Fork A(b)** full-spine close (ff the 38-commit arc into `main` first; corrected tag text now in `M0_READINESS.md`; still accounts-gated) · milestone-rethink **folded + retired** (roadmap surface = `docs/planning/roadmap-refresh-2026-06-09.md`).
>
> **Gates:** `make lint` + `make test` (64) + `make contracts` (13) ALL GREEN after fixes (incl. cheap_gpu_monitor ruff/mypy + library-imports registration). **Everything is UNCOMMITTED, user-led:** ~30 modified + 7 new files; suggested commit presented in-session; Round-31 PORTFOLIO_PLAN update drafted at `docs/planning/round-31-update.DRAFT.md` (ratify + paste + delete).
>
> **▶ NEXT (all user-led):** 1) review diff → commit the consolidation; 2) ratify the Round-31 draft into PORTFOLIO_PLAN; 3) the v0.1.0 Fork A(b) close when accounts exist (`M0_READINESS.md` runbook step 1b); 4) **P1.5 methods-hardening** (W1 email-only silhouette, W2 injecagent fix/re-derive, W3 falsify_ood_wall `--out` gate, disclosure notes) — recommended before any new experiment; 5) **Fork C** next-experiment decision (C1 Lane-2 carrier/table RECOMMENDED vs C2 mechanism pre-reg vs C3 agent-harness-v1).
>
> ⚠️ Until W3 lands: do NOT run `falsify_ood_wall.py` casually — it overwrites the committed `falsification_verdict.json` (restore via `git checkout` if hit).

---

# Session handoff — 2026-06-06 (LATE) — CROSS-FAMILY ARC COMPLETE: 3-arm SURVIVES · audit ROBUST · ADR-055 amendment RATIFIED + PUSHED · [prior arcs SUPERSEDED]

> **🆕 (2026-06-06) — the cross-family transfer arc is DONE end-to-end; the ADR-055 spine amendment is ratified + pushed.**
>
> **3-arm verdict (B4, LoRA ceiling): cross-family SURVIVES (capacity-resistant).** Arm A (direct→indirect) SURVIVES Gx_lora **+0.365** (wall GREW vs frozen +0.313); Arm B− (dialect-LODO) **3/4 SURVIVE** (bipia +0.291 / browsesafe +0.445 / fujitsu +0.228; injecagent FALSIFIED but **uninformative** — 17 negatives, degenerate, NOT a counterexample); Arm B+ (dialect-LODO + direct base) **3/4 SURVIVE** + **direct data does NOT bridge** (fujitsu anti-transfers, perm_p 0.9988 below chance). **Cross-arch reconciliation PASSES** (browsesafe-s0 4090 0.5999 vs H100 0.5928, Δ0.0072 ≪ SESOI).
>
> **Spine (RATIFIED into `decisions/ADR-055`): attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family SURVIVES** — axis-dependent, not uniformly capacity-dependent; cross-family is the one capacity-RESISTANT axis. Decision 1 reworded; README row + prototype-audit §A.5 (CLOSED) + `verdict.json` updated.
>
> **Audit:** 5 adversarial verifiers → **ROBUST** (numbers reproduce exactly, no bug, no leakage, labels correct; one finding-note over-claim — Arm A "lexical-shortcut over-defense" — downgraded). `experiments/cross-family-transfer/AUDIT_B4_2026-06-06.md`.
>
> **B+ run:** finished clean on a cheap Ada RTX-4090 (~7h, ~$3–5, within $8 cap, pod auto-deleted) after the cheap-only-`gpu_order` fix (`criteria.md` Rev 9 — the committed spec was falling through to L40S; new `scripts/cheap_gpu_monitor.py`). **Total cross-family lora spend ≈ $35.**
>
> **▶ NEXT (all user-led):** the held `v0.1.0` M0 close (accounts-gated, unchanged); the carrier/clustered re-lock (DF-11 / eval-toolkit#93); Lane 2 (carrier-axis training). **The cross-family arc needs nothing further.**
>
> Full detail: memory `[[cross-family-arm-a-b2-4]]`; `experiments/cross-family-transfer/{B4_FINDINGS.md, AUDIT_B4_2026-06-06.md, ADR-055-cross-family-amendment.DRAFT.md, verdict.json}`.
>
> **[The block below is SUPERSEDED — B+ has since landed; the audit + ADR ratification are done.]**

---

# Session handoff — 2026-06-06 — CROSS-FAMILY B4: A+B− VERDICT DONE (Arm A SURVIVES); B+ pending a cheap GPU · [prior arcs below, SUPERSEDED]

> **🆕 LATEST (2026-06-06) — the cross-family B4 verdict is computed for Arm A + Arm B− (PRELIMINARY, pre-audit); B+ + the audit remain.**
>
> **B4 VERDICT (preliminary):** **Arm A (direct→indirect) SURVIVES** — Gx_lora **+0.365** (CI-low +0.284>0, ≥ ½·frozen +0.156, ≥ 0.05 SESOI; the wall GREW vs frozen +0.313). **Arm B− (dialect-LODO) MIXED, 3/4 SURVIVE** — bipia +0.291 / browsesafe +0.445 / fujitsu +0.228 SURVIVE; **injecagent −0.014 FALSIFIED** (tool-output transfers). **Cross-axis spine: attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family SURVIVES** — the steepest axis HOLDS at the lora ceiling (capacity-resistant).
>
> **The saga (B3 got messy — read before re-running anything):** the original sequential B3 **stranded** A+B− on an EXITED pod RunPod couldn't restart (capacity); the **all-27 concurrent H100 re-run** recovered A+B− (pulled 16/27) but **cost-capped at ~$16 before B+** because concurrency is **compute-bound (~1.6×, NOT the assumed ~2.5–3×)** — the heavy B+ barely ran (**1/12**, browsesafe s0). The recovered A+B− lora (35 files) was merged into the cheap-rung trees → `b4_verdict` gave the above.
>
> **▶ NEXT (all user-led, present-first):**
> 1. **B+ (remaining 11–12 runs).** User chose to FINISH B+, but the cheap-fast cards (4090/A5000) are **unavailable** (the cheap path resolves a slow L40S ~$1/hr ≈ H100 cost). **Decision: WAIT for a card cheaper than L40S.** Poller `bxbjgrfwt` was watching but **LIKELY DIED on this compaction**. **▶ RECOVERY:** run `uv run python scripts/runpod_sweep.py --config experiments/cross-family-transfer/runpod_crossfamily_bplus_cheap_sweep.yaml --dry-run`; if it resolves a **non-L40S/A100** card → **launch it** (drop `--dry-run`) + a **CORRECTED bash monitor** (direct-`find` count + **verify-before-delete**; **NO gpu-run-watcher agent** — it over-polled to death; **NO `lc()` inside a `set -u` subshell**). Else keep waiting, OR pay ~$15 H100 / ~$13 L40S for complete B+. B+ feeds the **full 3-arm verdict** + the **cross-arch reconciliation** (re-run browsesafe-s0 already done on H100 → drift check).
> 2. **A+B− multi-verifier adversarial audit** (the verdict-trust gate) — OFFERED + deferred to this compact; the user's go is pending. Independent of B+; can run now.
> 3. **ADR-055 amendment** (cross-family SURVIVES) — drafted from the verdict, after the audit.
>
> **Git:** `f39949a` (cheap-B+ YAML + criteria **Rev 7/8**) · `4d3601d` (all27 YAML) · `5f82983` (bplus YAML + **DF-12** + **Rev 6**) on `session/2026-05-26-adoption-and-research-ops`, **UNPUSHED**. Recovered tree: `experiments/cross-family-transfer/B3_results_runpod_all27_lora/` (untracked, on disk; merged into the cheap-rung trees for the verdict). **Spend so far on cross-family lora ≈ $30** (stranded ~$14 + all27 ~$16); B+ adds ~$5 (cheap) / ~$13–15 (L40S/H100).
>
> **Lessons:** the **gpu-run-watcher AGENT over-polls to death** (527 tool-uses/52 min — use a plain bash monitor for multi-hour runs); local orchestration (`run_job` + bash monitors) **dies on context boundaries** → rely on incremental-pull + verify-before-delete; a cost-guard must **never pod-delete before a verified local pull**. DF-12 case 4 (orchestrator-death → no pull) recorded in `decisions/upstream_issues.md`.
>
> Full detail: memory `[[cross-family-arm-a-b2-4]]`. Plan: `~/.claude/plans/use-the-following-handoff-resilient-dolphin.md`. Verdict tool: `experiments/cross-family-transfer/b4_verdict.py`; recipe lock + cross-arch notes: `criteria.md` Rev 6/8.
>
> **[The 2026-06-05 "B3-wired / paid-go-next" block below is SUPERSEDED — B3 ran (all-27 + recovery + verdict); this is the post-run state.]**

---

# Session handoff — 2026-06-05 (LATE) — B3 `lora` rung WIRED + committed + PUSHED (`5bd5c6b`); the paid RunPod go is the ONLY remaining step · [prior arcs below]

> **🆕 LATEST (2026-06-05 LATE) — the B3 `lora` rung is now WIRED, gate-verified, committed, and PUSHED; only the paid RunPod launch remains.**
> The prior handoff's "lora needs only the RunPod launch" was **wrong** — `run_b2_4.py:241` hardcoded `choices=["tfidf","frozen"]` and the lora runner, the RunPod YAML, and the verdict fn did **not** exist. Built them (free, local, reversible); all gates green. Driven via `/exploring-options` ×4 → `/proceeding-now`. **1 commit PUSHED** (`5bd5c6b`; gitleaks clean; +818 lines):
>
> - **NEW** `run_b3_lora.py` — train-only lora orchestrator; **reuses** `_build_fold` / `make_dialect_fold` + **imports** `detectors.make_detector("lora")` (ADR-026, no reimpl); emits the **frozen-identical schema** so `falsify_dialect_lodo` + `b4_verdict` ingest the lora column UNCHANGED; `--smoke` (subsampled CPU schema check) / `--merge` (post-pull) modes; NotInject over-defense on Arm A.
> - **NEW** `runpod_crossfamily_sweep.yaml` — **single pod**; run.body ordered **A→B−→B+** (cheapest-robust-first — a 240-min timeout still leaves Arm A + B− scorable); cap **$14** / 240 min @ $3.29/h; excludes scoped to `experiments/**/*.parquet` (NOT `data/`).
> - **NEW** `b4_verdict.py` — the write-gated **SURVIVES/FALSIFIED/SMALL-THROUGHOUT** rule (criteria §Stat 2), **locked before any lora datum**; `--pre-validate` maps lora→frozen for a free arithmetic dry-run.
> - **MOD** `criteria.md` **Revision 5** — cost reconciliation **$6→$14** (full 27-run matrix kept, not trimmed; logic/thresholds/labels UNCHANGED).
>
> **Decisions (all user-adjudicated via the 4 modals):** build now / hold paid launch · full **27-run** matrix (Arm A 3 + B− 12 + B+ 12) · **single pod** · `r=(8,16)` (pre-registered) · `b4_verdict` locked-first · **full free B4 pre-validation** · **A→B−→B+** ordering · **NotInject** over-defense · **multi-verifier adversarial audit at B4**.
>
> **3 free gates GREEN (zero spend):** (1) **schema smoke** — lora `predictions.parquet` cols `[text,label,dialect,cluster_id,y_score]` **≡ frozen sibling** + `val_roc_auc` present (ran on **CPU**: the 2070S is OOM-occupied ~4.3 GB by desktop/research-kb; plumbing identical, real train is the cloud H100). (2) **offline dry-run** — spec valid, `estimated_spend=$13.16 ≤ $14`, paths resolved, ordering correct. (3) **B4-path pre-validation** — verdict arithmetic exercised end-to-end on the existing cheap trees (Arm B SURVIVES×3 + FALSIFIED×1; Arm A single-unit SURVIVES).
>
> **Cost (Rev 5, empirically anchored):** M1 $0.83 / carrier $1.17 (H100 @ $3.29/h) → 27 runs on 8–16× pools = **$7.6 / ~$11.3 / $17.5**. The $17.5 high bound > the $14 cap → the A→B−→B+ ordering is the graceful-degradation hedge.
>
> **▶ NEXT (all user-led, present-first) — the paid B3 go is the ONLY remaining step:**
> 1. **B3 paid go:** price `--dry-run` (re-confirm live H100 $/h + `pod.image`/`gpu_order`/`datacenters`; API key from `~/.runpod/config.toml`) → `uv run python scripts/runpod_sweep.py --config experiments/cross-family-transfer/runpod_crossfamily_sweep.yaml` under **`gpu-run-watcher`** (`run_in_background:true`) → pull to `B3_results_runpod_lora/` → `run_b3_lora.py --merge experiments/cross-family-transfer/B3_results_runpod_lora` → `b4_verdict.py` (real: lora vs frozen, per arm) → **B4** verdict → **multi-verifier adversarial audit** → ADR-055 spine amendment (drafted FROM the result).
> 2. **carrier/clustered re-lock** — when **DF-11 / [eval-toolkit#93](https://github.com/brandon-behring/eval-toolkit/issues/93)** ships `return_samples`/`frac_gt`.
> 3. **The held `v0.1.0` M0 close** (accounts-gated; unchanged).
>
> **Read-first:** this block → `experiments/cross-family-transfer/criteria.md` **Revision 5** (+ B3/B4 §Verification 2-3) → `B2_4_FINDINGS.md` (the cheap-rung read B3 completes) → memory `[[cross-family-arm-a-b2-4]]` + `[[workflow-proceeding-now-not-exitplanmode]]` → plan `~/.claude/plans/use-the-following-handoff-resilient-dolphin.md`. **Working-style:** present-first; `/proceeding-now` (never ExitPlanMode); reserve questions for design forks; **GPU runs = tracked background Bash, NO subagents, kill strays by PID** (the local 2070S is shared/OOM — the paid run is on RunPod).

---

# Session handoff — 2026-06-05 (AM, SUPERSEDED ↑) — Arm-A B2.4 harness BUILT + cheap-rung directional read DONE + Revision 4 ratified + PUSHED · [prior arcs below]

> **⚠️ SUPERSEDED (2026-06-05 LATE) — the B3 lora rung is now WIRED + committed + PUSHED (`5bd5c6b`); see the top block. Kept for the B2.4 cheap-rung directional table + Revision 4 corrections.** _(The "lora needs only the RunPod launch" line below was wrong — it was unwired; now built.)_
> **(2026-06-05 AM) — the Arm-A harness is built, run, and committed; B3 (paid `lora`) is the live next step.**
> Built the full Arm-A direct→indirect cross-family harness per Revision 3, ran the local/free cheap rungs, ratified **Revision 4** (realized counts). Driven via `/exploring-options` (3 modals → 10 locked decisions) then `/proceeding-now`. **1 commit PUSHED** (`761a712`; `make lint` + 58 tests green; gitleaks clean):
>
> - **NEW** `assemble_arm_a.py` (loaders + capped/uncapped pools + pooled test + over-defense) · `leakage_gate_arm_a.py` (§vi 4-scan; manifest 257) · `run_b2_4.py` (single-fold orchestrator — reuses `falsify_dialect_lodo.directional_table` UNCHANGED via an `arm_a_pooled` fold). **MOD** `folds_dialect.load_direct_base` re-export (unblocks B+) · `run_b2_3.py --variant B+` · `criteria.md` **Revision 4** ratified.
> - **648 MB per-fold parquets gitignored** (`B2_3_results_Bplus` + `B2_4_results`; mirror the B2.3 pattern); curated `summary.json` ×3 + `B2_4_FINDINGS.md` + `leakage_gate_armA.json` committed.
>
> **The cheap-rung directional read (NO verdict — lora-gated at B3; full table in `B2_4_FINDINGS.md`):**
>
> | evidence | result | reading |
> |---|---|---|
> | pooled gate tfidf→frozen | Gx **+0.47 → +0.31** (CI [+0.39,+0.51]→[+0.23,+0.36], perm_p 0) | large wall, **attenuates with capacity, persists** |
> | uncapped robustness | tfidf +0.49 ≈ capped +0.47 | **not a cap artifact** |
> | B+−B− bridging | ≈0 (bipia/browsesafe); +0.14/+0.12 (fujitsu/injecagent frozen) | **direct does NOT bridge indirect** (family shift corroborated) |
> | per-slice (frozen) | XSTest 0.62 > JBB 0.55 ≈ BIPIA 0.54 > InjecAgent 0.39 | tool-output anti-transfers; no slice masked by the mean |
> | over-defense | ~38% NotInject FPR @ 1% val-fixed thr | trigger-word over-defense, loud |
> | E8 deployed guards | PG1 0.97 BIPIA / **0.33 JBB** | scope-blind, not universal |
>
> The cross-family axis is the **steepest-walled start** of the three (attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family +0.47→+0.31); whether `lora` dissolves it (repos unify) or it stands (within-BIPIA headline bounded) is the **B4** verdict.
>
> **Revision 4 realized corrections (ratified):** neuralchemy "~16.3k" → **3,475** (a naive sum over overlapping subdirs `core`⊆`full`+`data`); capped positives **7,262**; train ≈29k @ 3.0:1 (deepset 399 / neuralchemy 3,475 / guychuk top-up 17,912); light game-artifact filter (a **deviation from §iii**, 0 drops from curated deepset/gandalf); leakage manifest **257** (direct⊗test 1 + negative⊗test 200 + near-dup 231; direct⊗direct 448 → keep-first dedup, not a leakage purge). **Fixed** a latent `cross_dedup_pairs` `(eval,train)` index-convention bug in the Arm-B `leakage_gate.py` (harmless there — 0 near pairs; worth an upstream fix).
>
> **▶ NEXT (all user-led, present-first):**
> 1. **B3 — the paid `lora` rung**, both arms (Arm-B B+ and B−), ≥3 seeds; hard cap ~$6 (`gpu-run-watcher`); real cost reconciled at the go. → **B4** verdict (FIXED ½·Gx(frozen)+0.05 SESOI logic, per arm). Harness + cheap rungs are ready; lora needs only the RunPod launch.
> 2. **carrier/clustered re-lock** — when **DF-11 / [eval-toolkit#93](https://github.com/brandon-behring/eval-toolkit/issues/93)** ships `return_samples`/`frac_gt`.
> 3. **The held `v0.1.0` M0 close** (accounts-gated; unchanged).
>
> **Read-first:** this block → `experiments/cross-family-transfer/B2_4_FINDINGS.md` + `criteria.md` **Revision 4** → memory `[[no-dataset-claims-without-eda]]` + `[[workflow-proceeding-now-not-exitplanmode]]`. **Working-style:** present-first; `/proceeding-now` (never ExitPlanMode); reserve questions for design forks; no dataset claim without real EDA; **GPU runs = tracked background Bash, NO subagents, kill strays by PID** (the frozen rung shares the RTX 2070S with research-kb ~3.8 GB).

---

# Session handoff — 2026-06-04 (EVENING, SUPERSEDED ↑) — Consolidation EXECUTED + Arm-A B2.4 PRE-REGISTERED (Revision 3) · [prior arcs below]

> **⚠️ SUPERSEDED (2026-06-05) — the Arm-A harness is now BUILT + the cheap-rung directional read DONE + Revision 4 ratified (see the top block). Kept for the 4 locked design decisions + the pre-registration context.**
> **(2026-06-04 evening) — the deferred experiment-axis decision RESOLVED + executed; the Arm-A harness BUILD was the next step (now complete).**
> This session: deliberated the next axis via `/exploring-options` → chose **consolidate, then open Arm-A** → a **ground-first** discipline (read-only `data/raw/` audit of all 9 Arm-A corpora + 5 test slices + 2 negative sources) + **best-practice research** (prompt-injection guardrail literature) turned a thin spec into an evidence-backed one. **3 commits PUSHED** (`afb344e..2d10747`):
>
> - **`9e776f9`** — **ADR-055 carrier amendment FILED** (status line on the Carrier-LODO resolution) + carrier "standing wall" → *partially capacity-resistant / residual-at-table (provisional n=3)* cite sweep (`glossary` ×3 + AUDIT `verification_report`). Cross-family `criteria.md:56,73` left intact (a different, still-open axis).
> - **`019dd6a`** — **dialect-LODO bootstrap re-locked** onto `stratified_cluster_bootstrap_ci` v1.8.0 (verified point EXACT / CI Δ≤0.0023 / ruff+mypy green; perm-p preserved). **1 of 3** — `falsify_carrier_lodo` + `falsify_clustered` stay hand-rolled, **blocked by DF-11** (`frac_gt0` unrecoverable from the primitive) → **issue filed [eval-toolkit#93](https://github.com/brandon-behring/eval-toolkit/issues/93)**.
> - **`2d10747`** — **B2.4 Revision 3** appended to `cross-family-transfer/criteria.md` — the deferred Arm-A pre-registration; *specifies*, does NOT change, the FIXED cross-family question.
>
> **The 4 locked Arm-A design decisions (grounded + research-backed):** **D1** broad **attack-vs-benign** positive (injection∪jailbreak∪harmful; + an injection-only BIPIA+InjecAgent descriptive sub-cut) · **D2** negatives = **deepset-neg + neuralchemy hard-negatives (InjecGuard MOF) + guychuk diversity**, benign-heavy ≈3.5:1, leakage-gated · **D3** pooled-ROC gate over the 4 two-class slices, **NotInject → over-defense FPR column** · **D4** C=3000 positives, size matched to Arm-B via the benign side. **Corpus-style confound** (Mirror Design Pattern) recorded as a structural limitation.
>
> **▶ NEXT (all user-led, present-first):**
> 1. **BUILD the Arm-A harness** — implement `load_direct_base` (stub at `folds_dialect.py:104`) + an `assemble_arm_a` + the Arm-A leakage gate + `run_b2_4`, per Revision 3 (§i–§viii). Now **unblocked** by the pre-registration; the only remaining grounding is the **JBB/XSTest within-slice `cluster_id`** (read from loaders at build). Then **B3** paid `lora` (~$6, `gpu-run-watcher`) → **B4** verdict (½·Gx(frozen)+0.05 SESOI, lora-gated).
> 2. **carrier/clustered re-lock** — when **DF-11 / [eval-toolkit#93](https://github.com/brandon-behring/eval-toolkit/issues/93)** ships a resample-distribution accessor (`return_samples` / `frac_gt`).
> 3. **The held `v0.1.0` M0 close** (accounts-gated; unchanged).
>
> **Read-first:** this block → `experiments/cross-family-transfer/criteria.md` **Revision 3** → memory `[[bootstrap-reproduction-audit]]` + `[[reserve-questions-for-design-not-trivia]]` + `[[no-dataset-claims-without-eda]]` → plan `~/.claude/plans/use-the-following-handoff-logical-candy.md`. **Working-style:** present-first; `/proceeding-now` (never ExitPlanMode); **reserve questions for design forks, default implementation trivia**; no dataset claim without real EDA; **run full `make ci` before pushing eval-toolkit**.

---

# Session handoff — 2026-06-04 (PM, SUPERSEDED ↑) — Consolidation DONE: `stratified_cluster_bootstrap_ci` v1.8.0 + ALL 3 LODO verdicts REPRODUCED + B2.3 frozen rung DONE · [Phase B / M0/M1 arc below]

> **⚠️ SUPERSEDED (2026-06-04 PM) — the deferred experiment-axis decision is now RESOLVED + executed (Arm-A chosen + B2.4 pre-registered Revision 3); see the top block.**
> This session: resumed + finished the **B2.3 frozen rung** (directional read in `B2_3_FINDINGS.md`: browsesafe
> `Gx` +0.459 at chance / **fujitsu +0.354 GROWS** / bipia +0.356 / injecagent −0.034 no-wall), then ran a
> **reproduction audit** — re-derive all 3 LODO bootstrap verdicts on a tested upstream primitive (distrust →
> independent re-derivation, CPU-only).
>
> **Two eval-toolkit releases (PyPI live):** `cluster_bootstrap_ci` **v1.7.0** (DF-9, #90 — single-block) then,
> after the audit found it **can't express the seed-averaging** the LODO estimators do inside the bootstrap
> (`Gx = val − mean_seed`), **`stratified_cluster_bootstrap_ci` v1.8.0** (DF-10, #92 — the composite
> **multi-stratum** primitive they actually need; the single-block one is its special case). Honest mis-scope,
> corrected + on the record.
>
> **Reproduction (`experiments/REPRODUCTION_2026-06/`): all 3 re-derived — point EXACT, CI within MC noise
> (Δ ≤ 0.001), conclusions unchanged:** dialect 8/8 (walls persist/grow) · carrier 3/3 incl. **lora
> SMALL-THROUGHOUT** · §6.5 **lora FALSIFIED**. Records: README + 3 scripts + 3 JSON; B2.3 re-lock note; DF-10
> ledger; `library_imports.md` floor `>=1.8` DOGFOODED; ADR-055 "reproduction stamp + dialect open-axis" note.
> **Commits PUSHED:** `a7c0f4d` (reproduction + notes) + `69fa8cd` (ruff) + this handoff → `origin/session/2026-05-26-…`.
>
> **▶ NEXT (all user-led, present-first):**
> 1. **The next EXPERIMENT axis — the deliberately-deferred decision** (the consolidation `/exploring-options`
>    Q1 deferred it). Re-open fresh: `/exploring-options` over { **Arm-A** cross-family direct→indirect (B2.4) ·
>    **dialect `lora`** verdict (B3, paid ~$6, `gpu-run-watcher`) · the **formal ADR-055 carrier amendment** }.
>    The foundation is now re-locked + reproduced ⇒ the spine reflects re-derived numbers.
> 2. **Optional production re-lock** (follow-up): refactor `falsify_dialect_lodo` / `falsify_carrier_lodo` /
>    `falsify_clustered` to consume `stratified_cluster_bootstrap_ci` (parallel future runs; does NOT affect any
>    verdict). Self-contained unit; the reproduction scripts already prove equivalence.
> 3. **The held `v0.1.0` M0 close** (accounts-gated; unchanged).
>
> **Read-first:** this block → `experiments/REPRODUCTION_2026-06/README.md` → memory `[[bootstrap-reproduction-audit]]`
> → the deferred-experiment context in the (now-superseded) Phase-B block just below. **Working-style:**
> present-first; `/proceeding-now` (never ExitPlanMode); **run full `make ci` before pushing eval-toolkit**
> (public-API golden on #90 + `black --check` on #92 each cost a CI round-trip; repo pre-commit gates gitleaks
> only); no subagents for long/GPU runs.

---

# Session handoff — 2026-06-04 (AM, SUPERSEDED) — Phase B underway: pre-reg RATIFIED + Arm-B harness built + tfidf directional read DONE+PUSHED; FROZEN RUNG = the clean-session resume · [Phase-2 + M0/M1 arc below]

> **⚠️ SUPERSEDED by the LATEST block above** — the frozen rung is now DONE (result in `B2_3_FINDINGS.md`) and
> B2.3's verdicts were reproduced on `stratified_cluster_bootstrap_ci` v1.8.0. Kept for the Arm-B / B2.4 spec + ops detail.

> **🆕 LATEST (2026-06-04) — Phase B (cross-family + within-indirect dialect transfer) underway; RESUME = the frozen rung.**
> Pre-reg **RATIFIED** (`c8248f4`) · Arm-B harness + leakage gate + criteria **Rev 1** (`5cb81f4`) · InjecAgent
> re-cluster + **Rev 2** (`7d169a8`) · **B2.3 tfidf directional read DONE** (`e574912`) — **ALL PUSHED**
> (`origin/session/2026-05-26-…`; branch in sync). Dir = `experiments/cross-family-transfer/`: `criteria.md`
> (locked pre-reg + Rev 1+2) · `B2_3_FINDINGS.md` (tfidf result) · `falsify_dialect_lodo.py` + `run_b2_3.py` +
> `e8_reference.py` (harness) · `assemble.py` + `folds_dialect.py` (data/folds). Per-fold parquet gitignored
> (~650 MB); `summary.json` committed.
>
> **tfidf FINDING (directional — NOT a verdict):** a LARGE within-indirect dialect-transfer wall at the cheap rung
> for **3/4 dialects** — browsesafe `Gx +0.46` (test ROC **0.535 ≈ chance**), bipia `+0.35`, fujitsu `+0.15`;
> injecagent `−0.04` (no wall — the 17-negative low-power fold). CIs exclude 0; robust under dialect-balancing.
> The pre-registered question — does **capacity** (frozen→lora) shrink these gaps — is what the frozen rung tests.
>
> **▶ RESUME — the frozen rung, in a clean session:**
> 1. **Clear the GPU.** Local **RTX 2070S (8 GB) is SHARED with `research-kb` (~3.2 GB)** (`nvidia-smi`); frozen
>    needs ~2 GB but crawls under contention. **NO subagents for this run** (the B2.3 build subagent ran away
>    ~96 min/1317 calls + spawned a GPU-hog that survived `pkill`); run via a **tracked background Bash**, kill
>    strays by **PID** (`pkill -f <script>` self-matches the issuing shell).
> 2. **Frozen smoke first** (a frozen fold was never seen to finish — only timed out under contention):
>    `uv run python experiments/cross-family-transfer/run_b2_3.py --dialects bipia --conditions natural --seeds 0 --rungs frozen --skip-e8`
> 3. **Full sweep at the pre-registered ≥10k bootstrap, BOTH rungs** (~1–2 h; background):
>    `PYTHONUNBUFFERED=1 uv run python experiments/cross-family-transfer/run_b2_3.py --rungs tfidf frozen --n-boot 10000 --n-perm 10000 > experiments/cross-family-transfer/B2_3_run.log 2>&1`
>    (cached embedder reuses embeddings across seeds; redirect-masking bit me before → keep `PYTHONUNBUFFERED` + read the log).
> 4. **E8** (`e8_reference.py`, chunk+max — BUILT but UNRUN): drop `--skip-e8`; cap-and-LOG if browsesafe/fujitsu
>    scoring is impractically slow (no silent truncation).
> 5. **Update `B2_3_FINDINGS.md` (frozen+E8) + commit.** Still **NO verdict** (lora-gated). Then **B2.4** (Arm A
>    9-corpus direct→indirect rebuild + B+; pos/neg construction TBD) → **B3** paid lora (~$6 cap, `gpu-run-watcher`)
>    → **B4** verdict (criteria Rev 1/2: ½·Gx(frozen) + 0.05 SESOI, lora-gated).
>
> **Read-first:** this block → plan `~/.claude/plans/use-the-following-handoff-iridescent-firefly.md` (full B2 spec
> + ops lessons) → `experiments/cross-family-transfer/B2_3_FINDINGS.md` + `criteria.md` → memory
> `[[dataset-strategy-rethink-and-acquisition]]`. **Working-style:** present-first; `/proceeding-now` (never
> ExitPlanMode); **no subagents for long/GPU runs.** *(A weekly usage limit was hit 2026-06-04, resets 7 am ET —
> why the frozen rung was deferred to a clean session.)*

---

# Session handoff — 2026-06-03 — dataset-universe Phase-2 EDA-gate DONE + pushed; experiment DESIGNED (E1–E8); Phase-A foundation-correction NEXT · [M0/M1 arc below]

> **PRIOR (2026-06-03, evening) — Phase-2 EDA-gate DONE; experiment DESIGNED (superseded by the 2026-06-04 block above; kept for detail).**
> Phase 2 (the plan in the block below) is complete. **8 new datasets EDA-gated** (materialize → survey →
> geometry → leakage scan → content deep-dive); **3 commits PUSHED** (`71c8526` materialize+specs / `1482d8f`
> EDA tooling / `b3068fd` findings+catalogue → `origin/session/2026-05-26-…`).
>
> **Headline: 2 NEW indirect carrier axes** — browsesafe (HTML) + fujitsu B1 (RAG) — BIPIA is no longer the
> lone indirect dialect. **Verdicts:** browsesafe = indirect-HTML TEST; **fujitsu B1** = indirect-RAG TRAIN/TEST
> (B1 per-doc, exclude augmented, skip B2 image; gate granted — real id `Fujitsu/agentic-rag-redteam-bench`,
> handoff's `…/agentic-rag` 404s); falsereject = benign-FPR (NC); neuralchemy = **PARK** (dedup-salvageable,
> 3,787 clean); aegis2 = PARK (off-axis); jailbreakdb = PARK (severe contamination — full 1.54M scan: shen_dan
> 17,783 / jackhhao 1,387 / jbb 288 + scrambled labels; "12.2M" was a line-count artifact); agentdyn =
> execution/Lane-5; agentdam = off-axis. Atlas **30→38**; ledger "Newly-surfaced 2026-06-03" table. EDA-code
> cleaned to consume upstream (`proxy_a_distance` + `audit_source_label_similarity`); **DF-7/DF-8 drafted, NOT filed**.
>
> **Elevated experiment DESIGNED (E1–E8; write-gated; the headline next block):** **leave-one-INDIRECT-corpus-out**
> over 4 distinct dialects (BIPIA / browsesafe / fujitsu-B1 / InjecAgent; PAD-vs-BIPIA 1.94–1.99 confirm
> distinctness), **both axes** (within-indirect + direct→indirect); fujitsu per-doc; browsesafe head+tail;
> corpus-OOD framing + carrier-LODO cross-ref; metric = keep ROC-AUC Gx + rung ladder but **adapt the low-n
> frame** (per-dialect lead + within-fold bootstrap + permutation test); **E8 = public-detector reference column**
> (ProtectAI / Prompt-Guard, frozen, run-ourselves-only); **promote Lane 6 to active**. Full spec = the plan file.
>
> **NEXT — methodological order ("do it right, not in a hurry"):** **Phase A** (records-corrected-FIRST) —
> A1 handoff refresh (this) ✓ · **A2 read the corrected program-review → write a RECONCILIATION NOTE** (the
> write-gate lens; what holds vs needs-update given M1/carrier-LODO/Phase-2) · A3 ratify the ADR-055 carrier
> amendment **POST-A2** (re-present Pieces + the Decision-6-vs-§16 sub-fork) · A4 commit `record-fixes-A1-A8`
> as-is. → **Phase B** (write-gated): finalize the full pre-reg (criteria.DRAFT's 7 TBDs + E1–E8) → cheap rungs
> (tfidf/frozen + E8, local/free) → paid LoRA (separate go ~$2–5) → verdict. → **Phase C**: `v0.1.0` close
> (accounts-gated, orthogonal).
>
> **Read-first:** this block → **the plan file `~/.claude/plans/use-the-following-handoff-iridescent-firefly.md`**
> → memory `[[dataset-strategy-rethink-and-acquisition]]` (updated) + `[[workflow-proceeding-now-not-exitplanmode]]`
> + `[[no-dataset-claims-without-eda]]`. **Working-style:** present-first; drive via `/proceeding-now` (never
> ExitPlanMode); no dataset claim without real EDA.

> **Prior (2026-06-03, Phase-1 plan — SUPERSEDED by the block above; kept for the Phase-2 task detail it spells out) — dataset-universe expansion arc** (a *separate* thread from the M0/M1 modeling
> arc documented below; **all uncommitted, user-led**). Multi-day arc: program-review correction → prototype
> audit → explore-first EDA → full dataset materialization → widened source audit. **Phase 1 DONE; Phase 2
> NEXT.** Full plan: **`~/.claude/plans/deep-review-ius-soft-starlight.md`**. Re-orient from memory
> `[[dataset-strategy-rethink-and-acquisition]]` + `[[no-dataset-claims-without-eda]]`.
>
> **On disk + done (Phase 1):**
> - `data/raw/` = **24 datasets materialized** (3.19 M rows, **1.09 GB**, gitignored) + `MANIFEST.json`; 5
>   unlicensed quarantined under `_eda_only_unlicensed/`. Built by `experiments/eda/materialize_datasets.py` (idempotent).
> - **Corrections applied:** Gandalf×2 + Mosscap = **MIT** (an `isinstance(cd,dict)` probe-bug had read `None`),
>   relocated out of quarantine; `xstest` → canonical **`walledai/XSTest`** (450 rows; `dataset_specs.yml` updated);
>   WAInjectBench pruned to text-only (−4 GB).
> - **EDA (earlier in arc):** E1–E7 cross-dataset geometry → `experiments/eda/CROSS_DATASET/FINDINGS.md`.
>   Headline: cross-family wall is **per-corpus** at frozen MiniLM; **BIPIA is one indirect *dialect*** (E7) ⇒
>   a CF test must hold out *multiple* indirect corpora.
> - **Ledger:** `docs/planning/dataset-acquisition-deep-dive-2026-06.md` (re-verified; bucket B = 5 unlicensed;
>   3 unavailable exhausted: Harelix 404 / PINT withheld / Indirect-in-the-Wild no-release).
>
> **Phase 2 — NEXT (EDA-gated; the user's hard rule: NO role/spec without REAL EDA on the actual data):**
> 1. Full-materialize the schema-verified new keepers — `perplexity-ai/browsesafe-bench` (MIT, indirect HTML),
>    `nvidia/Aegis-2.0` (CC-BY), `youbin2014/JailbreakDB` (CC-BY), `neuralchemy/Prompt-injection-dataset` (cfg
>    `core`, Apache), `AmazonScience/FalseReject` (CC-BY-NC, benign-control), `Fujitsu/agentic-rag` (derive
>    poison/benign) — + git-clone `SaFo-Lab/AgentDyn`, `facebookresearch/ai-agent-privacy`.
> 2. **Real EDA on disk** = `survey_v2` audit + fold into `cross_dataset_geometry` E2/E4: true label balance,
>    dedup, **leakage matrix across old+new = a HARD gate** (esp. JailbreakDB's 14 sources vs jackhhao/shen_dan/JBB).
> 3. Scaffold a **per-set content deep-dive** (read N sampled rows — stats miss mislabeling/junk).
> 4. Role-assign **from the EDA evidence** → spec only leakage-clean earners in `dataset_specs.yml` → catalogue
>    ALL (incl. parked) in the ledger + the `docs/research/datasets/agent_index/` atlas (30 → ~49).
> 5. **`prodnull/prompt-injection-repo-dataset`** = `gate_pending` (manual gate; the OWNER must approve — not user-actionable).
>
> **Gotchas:** (a) `MANIFEST` `n_rows` = all-files-per-snapshot ⇒ multi-config repos over-count vs carded —
> subset at load via `dataset_specs.yml`; (b) **subagent dataset findings are unreliable — live-verify** (HF
> `dataset_info`/tags/raw-README); web-search "verified ✓" can be a **stale cache of a deleted set** (the
> Harelix trap); (c) `data/raw/` is gitignored — never commit it.
>
> **Other uncommitted this arc (user-led):** program-review `.tex`/`.pdf`, `record-fixes-A1-A8.DRAFT.md`,
> `experiments/cross-family-transfer/criteria.DRAFT.md`, the 3 EDA scripts, the 2 dataset planning docs, the
> prototype-comparison audit. **Nothing committed.** (The M0/M1-arc held items below — v0.1.0 close, formal
> ADR-055 carrier amendment, ratify A1–A8 — still stand.)


> **✅ Post-session update (2026-06-01 — audit + carrier-LODO session):** ran the post-M1 **audit +
> independent re-examination** (5 adversarial verifier agents; **5/5 results reproduce, no mismatch** —
> `experiments/AUDIT_2026-06/verification_report.md`) and the **carrier-LODO M2 pre-flight** end-to-end.
> **Carrier-LODO verdict: `SMALL-THROUGHOUT`** — the carrier gap is real at frozen (G=+0.167) but
> **capacity-attenuated** at the LoRA ceiling (G=+0.067, CI-low +0.064 → not FALSIFIED; < ½·G(frozen) → not
> capacity-resistant), with a **residual table-carrier wall** (+0.205; email/code close). So the carrier axis
> is *partially* capacity-resistant — more than the attack-type axis (which fully dissolved). The spine's
> "carrier is the standing wall" claim is **refined → capacity-attenuated, residual, table-concentrated**; the
> formal **ADR-055 amendment is DEFERRED** to a fresh present-first session. Records:
> `experiments/carrier-lodo/{verdict.json,FINDINGS.md}` + criteria Rev 1 (ROC basis) + Rev 2 (in-distribution
> val). **3 commits this session, PUSHED (`ee397a7..3c8662a`):** `cef309d` (audit + Phase-2 record fixes),
> `876b867` (carrier-LODO harness + criteria), `3c8662a` (verdict/FINDINGS/PLAN-pointer). `make lint` + 57 unit + 13
> contracts green; the paid `lora` ran on a RunPod H100 (~$0.85–1.20, pod deleted). The carrier-LODO "run"
> item in NEXT below is **DONE**; the new deferred item is the formal ADR-055 carrier amendment.
>
> **✅ Prior post-session update (2026-06-01 PM):** the 2 commits are **pushed**, and the full 42-commit
> session arc is **merged to `main` via PR #4** (fast-forward; `origin/main` = `116cfd5`, linear,
> same SHAs). The "push / merge-to-main" steps in NEXT below are **DONE** — only the **`v0.1.0` tag +
> release + announcement remain held** for accounts (the merge prerequisite is now satisfied).

## ✅ START HERE — clean session

**The milestone re-ladder is DONE (Round 30 → ADR-055), and the `v0.1.0` M0 close is STAGED + held for
accounts.** M1 (attack-type-LODO) closed with its §6.5 verdict (attack-type axis capacity-dependent; table below); this
session ran the deferred post-LODO re-ladder and staged the formal close. The re-ladder edits are
**committed this session (2 commits on the session branch, UNPUSHED)**: ADR-055 +
a Round-30 PORTFOLIO_PLAN block + §5/§9/§16 edits + Ch 7/8/9/12/13 re-axis notes + a new
`experiments/carrier-lodo/criteria.md`. `make ratify-milestone` is **GREEN** on the committed tree. See
"NEXT" for the three remaining (all user-led).

**The headline M1 result — the per-attack-type wall is capacity-dependent (one axis of the later 3-axis spine):**

| rung | representation | T (top−bottom per-type AUPRC) | perm p | CI-low | verdict |
|---|---|---|---|---|---|
| tfidf | lexical | +0.135 | 0.014 | +0.111 | SURVIVES |
| frozen | frozen MiniLM emb + LogReg | +0.082 | 0.014 | +0.064 | SURVIVES |
| **lora** | **end-to-end ModernBERT FT** | **−0.003** | **0.900** | **−0.008** | **FALSIFIED** |

Judged on `lora` per criteria **Revision 2** → **FALSIFIED at the ceiling**. `T` collapses monotonically as
capacity rises: the pre-modeling OOD-wall prediction (built on the frozen MiniLM embedding, where the
carrier dominates) **does not transfer** to an end-to-end LoRA, which detects every attack type near-uniformly
(test ROC-AUC 0.965–0.981 across folds; per-type AUPRC 0.956–0.984 over a 0.926 prevalence floor). This is **capacity-dependence** (S2 pre-registered the frozen prediction-encoder transfer, verified at the frozen rung; the LoRA dissolution extends beyond S2's letter) —
and it's credible *because* the rule + tail sets + judged-rung were fixed before any LoRA datum existed and
write-gated. Record: `experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json` + `FINDINGS.md` §"Realized
verdict" + `criteria.md` footer. **Issue #2 CLOSED.**

**Nine commits this session (branch `session/2026-05-26-adoption-and-research-ops`; ALL PUSHED — HEAD `76b68d3`):**
1. **`81d7093`** — ADR-054: defer `full_ft`, `lora` = M1 ceiling, hybrid, `REQUIRED_RUNGS`, reference column, criteria Rev 2.
2. **`d187a50`** — fail-fast GPU guard + DF-5 (pricing-403) logged.
3. **`f0f1523`** — LoRA verdict + FINDINGS/criteria realized-verdict + budget actuals ($0.83) + falsify path fix + rsync setup + DF-6.
4. **`98c1804`** — handoff refresh + DF-6 filed ([runpod-deploy#116]).
5. **`f241bcc`** — ADR-054 ratified: full-FT §16 trigger RESOLVED (does not fire).
6. **`47ed870`** — DF-5 (pricing-403) filed ([runpod-deploy#117]).
7. **`3dde171`** — milestone-rethink inputs captured (re-ladder deferred to a fresh session).
8. **`8762ad4`** — scrub absolute `/home/` paths (closes #3).
9. **`76b68d3`** — V10 completed with PG1; the indirect-capable probe fires (closes #1).

**Cost:** $0.83 realized of the $250 base (base-budget; ADR-014 stays Reserved; « the $350 hard cap).

---

## NEXT — three things remain (all user-led; present-first)

> **Superseded — see the top post-session block (audit + carrier-LODO session) for the CURRENT state.** Below
> is prior-session context: item 3 (the carrier-LODO run) is now **DONE** (verdict `SMALL-THROUGHOUT`); the new
> deferred item is the **formal ADR-055 carrier amendment** (refine "standing wall" → capacity-attenuated,
> residual, table-concentrated). This session's 3 commits (`cef309d`, `876b867`, `3c8662a`) are **PUSHED**;
> the formal ADR amendment + the held `v0.1.0` close remain user-led.

**Updated 2026-06-01 PM (post-rethink).** The milestone re-ladder ran this session (Round 30 → ADR-055,
committed — 2 commits, unpushed); the `v0.1.0` close is staged + held for accounts; a carrier-LODO
validation run is scheduled as a separate go. Concretely:

1. **Push the 2 session-branch commits** (re-ladder + close-staging) — committed this session,
   **UNPUSHED**. Commit 1 = ADR-055 + Round-30 PORTFOLIO_PLAN + §5/§9/§16 + Ch 7/8/9/12/13 + glossary +
   `experiments/carrier-lodo/criteria.md`; commit 2 = the staged `v0.1.0` close + handoff. Push is
   user-led (always prompts).
2. **The `v0.1.0` M0 close bundle (HELD for accounts)** — once Twitter/X + Mastodon exist: merge the PR
   `session → main` → `git tag v0.1.0` on `main` → `gh release` → post announcement → `gh release edit`
   to link it. `make ratify-milestone` GREEN on the committed tree; release notes + announcement + PR body
   drafted. Nothing outward has fired.
3. **The carrier-LODO M2 pre-flight run** — a separate present-first go (not queued): validates the
   spine's "carrier is the standing wall" claim (cheap rungs free; `lora` ~$1). Criteria pre-registered
   at `experiments/carrier-lodo/criteria.md`; finalize its implementation Revision before launching.

*(Superseded — the prior "two things remain" framing just below is from the M1-close state, preserved as history.)*

The M1 arc is **fully closed, ratified, and pushed**; both upstream frictions filed ([#116] rsync, [#117]
pricing-403); issues **#1 / #2 / #3 all CLOSED**. ~~Only two things remain, both user-led:~~

1. **Milestone rethink — DEFERRED to a fresh session; inputs captured.** The post-LODO-results re-ladder
   condition (Round 27 / ADR-052) is now **met**; M1's implications are distilled in
   **`docs/planning/milestone-rethink-inputs.md`** (read-first brief). Pick up the full re-ladder fresh →
   `/exploring-options` → ADR-055+.
2. **Formal `v0.1.0` M0 close** — `git tag v0.1.0` + `gh release` + the build-in-public announcement. Stays
   **user-led** (accounts not created); see `M0_READINESS.md`. Orthogonal to the rethink.

*(Done this session: the paid LoRA sweep + §6.5 verdict, ADR-054 ratification + trigger resolution, the push,
both DF filings, the `/home/`-path scrub, and the V10/PG1 completion. The `full_ft` §16 trigger is RESOLVED —
does not fire: FALSIFIED ⇒ no decision-relevant full-FT point.)*

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
- **No open portfolio issues.** All three closed this session:
  - **#2** — §6.5 OOD-wall falsification — CLOSED (FALSIFIED at the LoRA ceiling; `76b68d3`/`f0f1523`).
  - **#3** — Scrub absolute `/home/` paths — CLOSED (`8762ad4`).
  - **#1** — Rerun V10 with PG1 — CLOSED (PG1 fires; `76b68d3`).
- Upstream (runpod-deploy): **#116** (rsync on lean base image) + **#117** (GraphQL pricing 403) — filed, open upstream.

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
