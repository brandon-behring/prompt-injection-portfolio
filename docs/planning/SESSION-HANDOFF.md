# Session handoff — 2026-05-28

## ✅ START HERE — clean session: Phase 1 (foundational EDA)

**Phase A is COMPLETE.** A 2026-05-27/28 session-stretch took the dataset dossier from a never-audited 20-entry narrow-scope ledger to a comprehensive, saturation-checked, family-tagged, verified-and-audited reference — and authored the EDA design + prototype post-mortem that ground Phase 1. **Next is Phase 1: the foundational EDA itself** (eval-toolkit `eda` layer refinements → Job-1 integrity gate → Jobs 2–3 shortcut + shift).

**Approved plan (source of truth):** `~/.claude/plans/use-the-following-handoff-bright-umbrella.md` — read first.

---

## Current state (2026-05-28)

### Phase A deliverables (done — uncommitted, in the working tree)
- `docs/research/datasets/_candidate_universe.md` — the **saturation-checked landscape map** (20 + ~65 net-new across families injection-direct/indirect, jailbreak, toxicity-safety-guard, over-defense-control, agentic-trajectory, aggregated-recipe, helper). Cross-checked against awesome-prompt-injection, Awesome-Agent-Security, SafetyPrompts.com, JailbreakBench, the InjecGuard ~20-set + ProtectAI/PromptGuard mixture compositions, HF tag — *converged*.
- `docs/research/datasets/dataset_ledger.yml` — **30 verified-tagged entries** (topic broadened to `unsafe_input_guardrail_detection`; every entry carries soft tags `family` / `encoder_readiness` / `study_relevance`). Honest flags retained: 1 `mismatched` (`xtram12024safeguardpromptinjection` — its card cites arXiv:2402.13064 = the unrelated GLAN paper); 6 `license: unknown`; 3 `unverified` (Harelix HF 401, PINT data withheld, IPI-in-the-wild unreleased). `validators/dataset_ledger.py` → `OK`.
- `docs/research/datasets/agent_index/` — **regenerated**: 8 files (`README.md`, `00_overview.md`, `01_injection_direct.md` A1–A11, `02_injection_indirect.md` B1–B5, `03_jailbreak_and_toxicity.md` C1–C4, `04_over_defense.md` D1–D4, `05_agentic_trajectory.md` E1–E3, `06_aggregated_recipes.md` F1–F3). 5-bullet entries + soft-tag triple per entry; family-organized. `agent_index.py` + `cross_stage.py` → `OK`.
- **First `/dossier-audit` round** (audit-trail in `agent_index/README.md`): 2 CORRECT (LLMail-Inject's 5 success flags are *nested* inside the `objectives` JSON, not top-level columns; XSTest's id column is `id_v1`/`id_v2`); 0 DROP / 0 new FLAG; all pre-existing flags re-verified + held. `audit_trail.py` → `OK`.

### Phase-1 design (done — companions)
- `docs/planning/eda-design.md` — **domain-grounded EDA design.** Thesis: EDA here = pre-registering what the data can support; measure the four properties the predecessor found too late. 8 PI-specific traits, A–F analysis catalog, V1–V11 visualization catalog with pitfalls, scope tiers (R = reusable `eval_toolkit.eda` vs D = portfolio-specific), the 6 highest-value analyses that would have *predicted* the OOD wall pre-GPU, build order. **THE doc to read for Phase 1 design.**
- `docs/planning/prototype-postmortem.md` — the **prototype retrospective.** Wins to keep (clean LODO, OOD-wall finding, calibration signal) + the 3 confounds + the "8.4pp inflation" claim with **no derivation in either repo** + the §9.5 anti-correlation as interpretation-not-measurement + carry-forward (B1 calibration, B4 κ/error-correlation, B7 per-row score distributions, B8 cv_clt-vs-block-bootstrap sensitivity flag, B10 label-aware dedup) + doc-form lessons (avoid sprawl / immutability-cascade / planned-vs-happened drift).

### eval-toolkit state (synced; layer built + held)
- `/Users/brandonbehring/eval-toolkit` — **pulled v0.24.0 → v1.4.0** (clean `main` fast-forward). The v1.x metrics + Tier-1 stability contract is real (their ADR 0003). The reuse map was re-validated against v1.x source (the v0.24→v1.x rewrite is significant — don't reason against the old surface).
- Branch **`feat/eda-data-audit`** — holds the **built + verified-green** Tier-2 `eval_toolkit.eda` integrity-gate subpackage:
  - `src/eval_toolkit/eda/__init__.py` + `data_audit.py` (~565 lines): `audit_dataset` orchestrator + `DataAudit` / `SplitSummary` frozen dataclasses + `class_balance` / `length_quantiles` / `summarize_split` helpers + three `GateResult`-typed integrity gates (`class_balance`, `no_cross_split_leakage`, `context_window_fit`).
  - `tests/test_eda.py` — 19 tests pass; **100% statement coverage**; ruff + black + mypy-strict + sybil doctests clean; full `make test-fast` style suite green.
  - `pyproject.toml` `[eda]` extra = `["pandas>=2.0", "matplotlib>=3.8"]` (torch-free); **not** in top-level `_EXPORTS` (Tier-2 only — evolvable). `.doctest-modules` + `uv.lock` synced.
- **UNCOMMITTED** — changes live in the working tree on `feat/eda-data-audit`. Held pending the `eda-design.md` refinements before commit + PR.

### Portfolio git state (uncommitted)
On branch **`session/2026-05-26-adoption-and-research-ops`**. Working tree carries: the eda-design + post-mortem + candidate-universe + the back-tagged 30-entry ledger + the regenerated 8-file agent_index + this handoff. Suggested commit boundaries (when you're ready):
1. `docs(planning): EDA design + prototype post-mortem` — `docs/planning/eda-design.md`, `docs/planning/prototype-postmortem.md`.
2. `docs(datasets): Phase A — broad scope + verified-tagged ledger + regenerated agent_index + first audit` — `docs/research/datasets/dataset_ledger.yml`, `docs/research/datasets/agent_index/**`, `docs/research/datasets/_candidate_universe.md`.
3. `docs(handoff): 2026-05-28 — Phase A done; Phase 1 START HERE` — this file.

(The eval-toolkit `feat/eda-data-audit` branch commits separately in *that* repo, once the layer is refined per `eda-design.md`.)

---

## PHASE 1 — start here

### Goal
Run the EDA-first program over the verified working set so that the **OOD-collapse magnitude becomes a *predicted* value pre-modeling** — not a post-hoc surprise. Resolves the roadmap-gating decision **RC0 (BIPIA adequacy)** and the data-conditional decisions the roadmap waits on.

### Decisions locked (from the plan + this session)
- **Tier-2 submodule** (`eval_toolkit.eda`); **not** in the top-level `__all__`/`_EXPORTS` (evolvable; graduate later).
- **Job-1 torch-free** (lean-local); **Jobs 2–3 use a one-time CPU torch + sentence-transformers** install — a scoped, recorded exception to ADR-051's lean-local rule (heavy GPU/training stays CI-only). To be ADR'd in Phase 2.
- **Coupled delivery**: machine-checkable audit JSON/parquet (CI-gateable) + a jupytext notebook report (Decision/Gate callouts, book-chapter-ready per ADR-020) + committed figures.
- **Sequence**: integrity gate first across the working set → then Jobs 2–3 deeper.
- **Selection deferred to the EDA**: Phase A's soft `study_relevance` tag is a hint; the EDA *selects* the actual working set (filter on `encoder_readiness ∈ {drop-in, derivable}` + detection-relevant `family`).

### Step 1 — `eval_toolkit.eda` layer refinements (the held branch)
Work in `/Users/brandonbehring/eval-toolkit` on `feat/eda-data-audit`:
1. **Drop the `seed` param** from `audit_dataset` (`rng` is the §3a canonical via SPEC 7; the integrity gate is fully deterministic — no RNG; the param violates §1.5 anti-overengineering). Adjust `DataAudit` + tests.
2. **Fold obfuscation/encoding/invisible-Unicode prevalence in as a Job-1 integrity prerequisite** (per `eda-design.md` §B2 — the *seen-text ≠ scored-text* hazard; invisible chars silently corrupt every downstream length/n-gram/embedding stat). Lightweight detectors: invisible U+200B/U+200C/U+200D + the U+E0000–U+E007F tag block + variation-selector range; homoglyph/confusables via NFKC-normalization delta; base64/hex via entropy; ROT13 round-trip; leetspeak rate. Expose a `raw vs NFKC` length-delta on `DataAudit`.
3. Then **build the Jobs 2–3 modules** in `eval_toolkit.eda`:
   - `lexical_association` — log-odds informative-Dirichlet (Monroe 2008) + PMI + scaled-F (Kessler / scattertext) + partial-input / structural-only competency baselines (Feng & Wallace 2019; Gururangan 2018 annotation artifacts).
   - `distribution_shift` — proxy-A-distance (Ben-David 2010), MMD (Gretton 2012), k-NN purity, vocab/OOV overlap.
   - Embedding-map helper using `eval_toolkit.embeddings.make_minilm_embedder` (the `[embeddings]` extra; soft-imports torch — Jobs 2–3 only).
   - Cube/carrier tagging scaffold (intent × technique × channel; carrier+position for indirect).
4. Branch + PR (don't self-merge); portfolio consumes via editable install during dev, re-pins on release.

### Step 2 — Job-1 integrity gate run (torch-free; lean-local)
- Select the working set from the ledger: `encoder_readiness ∈ {drop-in, derivable}` + detection-relevant families; high `study_relevance` first. Likely starters: `hendzh2025promptshield`, `guychuk2024benignmalicious`, `shen2023inthewild` (DAN), `lin2023toxicchat`, `han2024wildguard` (**gated** — needs HF token), `bipia2023microsoft` (the LODO axis), `deepset2023promptinjections`, `jackhhao2023jailbreakclassification`, `leolee2024notinject`, `rottger2024xstest`, `cui2024orbench`. Plus the prototype training-pool sources (LMSYS + UltraChat benigns) for parity.
- **Own SHA-pinned manifest** (don't inherit from the submission).
- Per dataset → counts, balance, token-length + %-over-8192 (ModernBERT tokenizer; caller-supplied), exact + near-dup, leakage, **obfuscation/encoding/invisible-Unicode prevalence**. Per-dataset audit JSON + a combined integrity-report notebook + figures; each analysis ends in a Decision/Gate. Certify usability.

### Step 3 — Jobs 2–3 (shortcut + shift; needs embeddings/torch)
Per `eda-design.md`, **highest-value first** (the analyses that would have *predicted* the predecessor's OOD wall pre-GPU):
- **V10** reference-scorer score-distributions per slice (ProtectAI on each slice) — the literal §9.5 missing figure; turns "anti-correlation" from *interpretation* into *measurement*.
- **A1** positive-class cube decomposition (intent × technique × channel) — the heterogeneous-positive picture; map each source to a corner; shows train↔OOD as opposite corners with *zero modeling*.
- **E1** per-fold proxy-A-distance (+ MMD) — the modeling go/no-go; tall PAD bars *predict* OOD collapse per fold pre-GPU.
- + C1 log-odds + C2 partial-input/competency baselines (the *true* floor) + F2 BIPIA attack-type diversity / intra-type similarity (**resolves RC0**) + V4 embedding UMAP (pair with silhouette/ARI per the UMAP-distances-aren't-metric pitfall) + F1 NotInject validity + D3 ProtectAI contamination.
- Cartography (Swayamdipta 2020) = a probe-pass diagnostic (needs one training run; not pre-modeling).
- **Fix the prototype's BIPIA loader collapse** (`/Users/brandonbehring/Claude/prompt-injection-detection-submission/src/data/loaders.py:527-562` discards carrier identity + payload position — needed for the indirect analyses).

### Checkpoints for your review
1. After the held layer's refinements (drop `seed`, fold obfuscation in) — eval-toolkit branch ready for PR.
2. After the integrity gate certifies the working set + **RC0 is answerable with evidence**.
3. After Jobs 2–3 — the **OOD-collapse prediction is recorded pre-modeling**.

---

## Read first (in order)
1. `~/.claude/plans/use-the-following-handoff-bright-umbrella.md` — the approved plan.
2. `docs/planning/eda-design.md` — the EDA design / analysis + viz catalogs / scope tiers.
3. `docs/planning/prototype-postmortem.md` — the prototype retrospective + carry-forward list.
4. `docs/research/datasets/agent_index/README.md` — agent-index hub (glossary, lookup recipes, audit-trail).
5. `docs/research/datasets/dataset_ledger.yml` — the verified ledger (the EDA's selection input).
6. `docs/research/datasets/_candidate_universe.md` — the saturation-checked completeness map (for selecting beyond the ledger).

## Tasks
- **#5** `Step 1 — Build eval-toolkit EDA profiling + DataAudit layer (integrity-gate)` — **in_progress** (built + held; refinements pending: drop `seed`, fold obfuscation in, then build the Jobs 2–3 modules).
- **#6** `Step 2 — Run Job-1 integrity gate across all datasets` — **pending** (unblocked now that #9 is done).
- **#7** `Step 3 — Build + run Jobs 2-3 (shortcut + shift EDA)` — **pending**.
- **#8** `Phase 2 — Consolidate ROADMAP.md + archive + fixes + post-mortem + ADRs` — **pending** (Phase 2; follows Phase 1).
- **#9** `Phase A — Dataset-scope completeness` — **completed**.
- **#10** `Dossier-audit round 1: dataset agent_index` — **completed**.

## Gotchas / open items
- **eval-toolkit local clone** at `/Users/brandonbehring/eval-toolkit` was historically stale at v0.24.0; this session pulled it to v1.4.0 (clean ff). Always `git -C /Users/brandonbehring/eval-toolkit describe --tags` before reasoning about its surface.
- The held `eda` code uses `seed: int = 42` — **must drop first** (§3a / SPEC 7 / deterministic gate) before PR.
- **WildGuardMix is gated** (`auth_required: true` — AI2 Responsible Use); needs an HF token to actually download.
- **Harelix** (`harelix2024mixedtechniques`) HF page is bot-blocked (HTTP 401 to WebFetch); the entry's `status: unverified` reflects that; schema + label semantics need a re-fetch via the HF API / `datasets` lib before training use.
- The **scoped CPU-torch-for-EDA exception to ADR-051** is noted in the plan but **not yet ADR'd** — Phase 2 will author the ADR.
- **`NEXT_SESSION.md` is stale** (last update 2026-05-23 — predates this entire session). Refresh deferred to Phase 2 consolidation.
- The user's **strongest standing preference** (per memory `interrogate-before-planning`): present-first + interrogate inconsistencies in your *own* plan + ask focused goal-clarifying questions *before* convergence. `ExitPlanMode` will be rejected if you've under-interrogated — multiple times in this session. Surface real plan inconsistencies before requesting approval.

---

*↓ Historical content (pre-2026-05-28 — Phase B research-ingestion close, R26 dogfooding adoption, etc.) preserved in git history. The above is the current source of truth.*
