# Session handoff — 2026-06-03 — dataset-universe Phase-2 EDA-gate DONE + pushed; experiment DESIGNED (E1–E8); Phase-A foundation-correction NEXT · [M0/M1 arc below]

> **🆕 LATEST (2026-06-03, evening) — Phase-2 EDA-gate DONE + COMMITTED + PUSHED; experiment DESIGNED.**
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
accounts.** M1 (attack-type-LODO) closed with its §6.5 verdict (capacity-dependent; table below); this
session ran the deferred post-LODO re-ladder and staged the formal close. The re-ladder edits are
**committed this session (2 commits on the session branch, UNPUSHED)**: ADR-055 +
a Round-30 PORTFOLIO_PLAN block + §5/§9/§16 edits + Ch 7/8/9/12/13 re-axis notes + a new
`experiments/carrier-lodo/criteria.md`. `make ratify-milestone` is **GREEN** on the committed tree. See
"NEXT" for the three remaining (all user-led).

**The headline result — the OOD wall is capacity-dependent:**

| rung | representation | T (top−bottom per-type AUPRC) | perm p | CI-low | verdict |
|---|---|---|---|---|---|
| tfidf | lexical | +0.135 | 0.014 | +0.111 | SURVIVES |
| frozen | frozen MiniLM emb + LogReg | +0.082 | 0.014 | +0.064 | SURVIVES |
| **lora** | **end-to-end ModernBERT FT** | **−0.003** | **0.900** | **−0.008** | **FALSIFIED** |

Judged on `lora` per criteria **Revision 2** → **FALSIFIED at the ceiling**. `T` collapses monotonically as
capacity rises: the pre-modeling OOD-wall prediction (built on the frozen MiniLM embedding, where the
carrier dominates) **does not transfer** to an end-to-end LoRA, which detects every attack type near-uniformly
(test AUPRC 0.98–0.999, held-out included). This is **capacity-dependence** (S2 pre-registered the frozen prediction-encoder transfer, verified at the frozen rung; the LoRA dissolution extends beyond S2's letter) —
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
