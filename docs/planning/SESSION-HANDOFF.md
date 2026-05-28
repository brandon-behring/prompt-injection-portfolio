# Session handoff — 2026-05-28 (PM update — PR-1 open)

## ✅ START HERE — clean session: Phase 1 Step 2 (Job-1 integrity gate run)

**Phase A is COMPLETE; Phase 1 Step 1 refinements are COMPLETE.** The 2026-05-28 PM session shipped the eval-toolkit `eda` Tier-2 layer + Job-1 integrity gate + the §B2 obfuscation prevalence detectors as **PR-1 (`brandon-behring/eval-toolkit#83`, OPEN)**. Two commits on `feat/eda-data-audit`: Tier-2 layer (audit_dataset, schema v2, no seed) + obfuscation profile (full §B2 detector list). 71 tests, 99.46% coverage on `eda/`, lint + mypy strict + doctest all clean. Portfolio's 4 docs commits are now pushed too.

**Next** is Phase 1 **Step 2** — Job-1 integrity gate **run** across the verified working set, via editable install of the PR-1 branch while review proceeds. Step 3 (Jobs 2–3 build: `lexical_association`, `distribution_shift`, embedding-map, cube/carrier scaffold) becomes a follow-on PR-2 later.

**Approved plan (source of truth):** `~/.claude/plans/use-the-following-handoff-bright-umbrella.md` — read first.

---

## Current state (2026-05-28 PM — post-PR-1)

### Phase A deliverables (done — committed in `f214089`, pushed)
- `docs/research/datasets/_candidate_universe.md` — the **saturation-checked landscape map** (20 + ~65 net-new across families injection-direct/indirect, jailbreak, toxicity-safety-guard, over-defense-control, agentic-trajectory, aggregated-recipe, helper). Cross-checked against awesome-prompt-injection, Awesome-Agent-Security, SafetyPrompts.com, JailbreakBench, the InjecGuard ~20-set + ProtectAI/PromptGuard mixture compositions, HF tag — *converged*.
- `docs/research/datasets/dataset_ledger.yml` — **30 verified-tagged entries** (topic broadened to `unsafe_input_guardrail_detection`; every entry carries soft tags `family` / `encoder_readiness` / `study_relevance`). Honest flags retained: 1 `mismatched` (`xtram12024safeguardpromptinjection` — its card cites arXiv:2402.13064 = the unrelated GLAN paper); 6 `license: unknown`; 3 `unverified` (Harelix HF 401, PINT data withheld, IPI-in-the-wild unreleased). `validators/dataset_ledger.py` → `OK`.
- `docs/research/datasets/agent_index/` — **regenerated**: 8 files (`README.md`, `00_overview.md`, `01_injection_direct.md` A1–A11, `02_injection_indirect.md` B1–B5, `03_jailbreak_and_toxicity.md` C1–C4, `04_over_defense.md` D1–D4, `05_agentic_trajectory.md` E1–E3, `06_aggregated_recipes.md` F1–F3). 5-bullet entries + soft-tag triple per entry; family-organized. `agent_index.py` + `cross_stage.py` → `OK`.
- **First `/dossier-audit` round** (audit-trail in `agent_index/README.md`): 2 CORRECT (LLMail-Inject's 5 success flags are *nested* inside the `objectives` JSON, not top-level columns; XSTest's id column is `id_v1`/`id_v2`); 0 DROP / 0 new FLAG; all pre-existing flags re-verified + held. `audit_trail.py` → `OK`.

### Phase-1 design (done — committed in `881a0e8`, pushed)
- `docs/planning/eda-design.md` — **domain-grounded EDA design.** Thesis: EDA here = pre-registering what the data can support; measure the four properties the predecessor found too late. 8 PI-specific traits, A–F analysis catalog, V1–V11 visualization catalog with pitfalls, scope tiers (R = reusable `eval_toolkit.eda` vs D = portfolio-specific), the 6 highest-value analyses that would have *predicted* the OOD wall pre-GPU, build order. **THE doc to read for Phase 1 design.**
- `docs/planning/prototype-postmortem.md` — the **prototype retrospective.** Wins to keep (clean LODO, OOD-wall finding, calibration signal) + the 3 confounds + the "8.4pp inflation" claim with **no derivation in either repo** + the §9.5 anti-correlation as interpretation-not-measurement + carry-forward (B1 calibration, B4 κ/error-correlation, B7 per-row score distributions, B8 cv_clt-vs-block-bootstrap sensitivity flag, B10 label-aware dedup) + doc-form lessons (avoid sprawl / immutability-cascade / planned-vs-happened drift).

### eval-toolkit state (PR-1 OPEN — `feat/eda-data-audit`)
- `/Users/brandonbehring/eval-toolkit` — synced at `v1.4.0`-derived; branch **`feat/eda-data-audit`** carries **two commits** ahead of `main`, both pushed to `origin`. **PR #83 OPEN** (`https://github.com/brandon-behring/eval-toolkit/pull/83`).
  - `ef79b2c` **feat(eda): Tier-2 EDA layer + Job-1 integrity gate** — `audit_dataset` + `DataAudit` / `SplitSummary` frozen dataclasses + `class_balance` / `length_quantiles` / `summarize_split` helpers + three `GateResult`-typed integrity gates (`class_balance`, `no_cross_split_leakage`, `context_window_fit`). **Schema authored as v2 from the outset — no `seed` field** (gate is deterministic; STYLE.md §3a). `[eda]` extra pins `pandas>=2.0` + `matplotlib>=3.8` (torch-free); **not** in top-level `_EXPORTS` (Tier-2 only).
  - `ae4d375` **feat(eda): obfuscation prevalence detection (§B2 integrity prerequisite)** — new `eval_toolkit.eda.obfuscation` module (pure stdlib): invisible Unicode (U+200B/C/D + Tags block + variation selectors + BOM + WJ); NFKC change + char-count delta (fullwidth Latin / math-bold / ligatures); base64- / hex-alphabet high-entropy runs; ROT13 PI markers; leetspeak tokens (length-capped 3–12 to filter hex hashes). `analyze_obfuscation(texts) → ObfuscationProfile`. Integrated into `SplitSummary.obfuscation` + `audit_dataset(obfuscation=True)` flag. **Profile-only — does NOT gate `gate_passed`.**
- Quality bar: **71 tests** (19 + 40 + 12 doctests), **99.46% statement coverage on `eda/`** (100% on `obfuscation.py`), ruff + black + mypy strict + `.doctest-modules` doctests clean.
- **NOT in this PR (deferred to PR-2):** `lexical_association`, `distribution_shift`, MiniLM embedding-map, cube/carrier scaffold + the ADR for the scoped CPU-torch-for-EDA exception (ADR-051).

### Portfolio git state (pushed)
On branch **`session/2026-05-26-adoption-and-research-ops`**, **pushed to `origin`** (`0037ee3..8dffced`). 4 commits cover: EDA design + post-mortem (`881a0e8`); Phase-A dataset ledger + agent_index + first audit (`f214089`); Phase-1 START HERE handoff (`f2cd014`); NEXT_SESSION redirect (`8dffced`).

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

### Step 1 — eval-toolkit eda layer ✅ DONE (PR #83 OPEN)
Shipped as PR-1 (commits `ef79b2c` + `ae4d375` on `feat/eda-data-audit`). Schema authored as v2 with no `seed` param/field; the full §B2 obfuscation list lives in the new `eval_toolkit.eda.obfuscation` module. Profile-only integration (does not gate `gate_passed`). Jobs 2–3 build is **deferred to PR-2** (next-session Phase-1 Step-3 work):
- `lexical_association` — log-odds informative-Dirichlet (Monroe 2008) + PMI + scaled-F (Kessler / scattertext) + partial-input / competency baselines (Feng & Wallace 2019; Gururangan 2018).
- `distribution_shift` — proxy-A-distance (Ben-David 2010), MMD (Gretton 2012), k-NN purity, vocab/OOV overlap.
- Embedding-map helper via `eval_toolkit.embeddings.make_minilm_embedder` (the `[embeddings]` extra; soft-imports torch).
- Cube/carrier tagging scaffold (intent × technique × channel; carrier+position for indirect).
- ADR-051 amendment authoring the scoped CPU-torch-for-EDA exception.

### Step 2 — Job-1 integrity gate run (torch-free; lean-local) — **START HERE NEXT**
**Consume the open PR via editable install** while review proceeds:
```bash
# In the portfolio repo:
uv pip install -e /Users/brandonbehring/eval-toolkit
# (or `pip install -e ../../eval-toolkit` from inside the portfolio venv)
```
Then:
- Select the working set from the ledger: `encoder_readiness ∈ {drop-in, derivable}` + detection-relevant families; high `study_relevance` first. Likely starters: `hendzh2025promptshield`, `guychuk2024benignmalicious`, `shen2023inthewild` (DAN), `lin2023toxicchat`, `han2024wildguard` (**gated** — needs HF token), `bipia2023microsoft` (the LODO axis), `deepset2023promptinjections`, `jackhhao2023jailbreakclassification`, `leolee2024notinject`, `rottger2024xstest`, `cui2024orbench`. Plus the prototype training-pool sources (LMSYS + UltraChat benigns) for parity.
- **Own SHA-pinned manifest** (don't inherit from the submission).
- Per dataset → counts, balance, token-length + %-over-8192 (ModernBERT tokenizer; caller-supplied), exact + near-dup, leakage, **obfuscation prevalence (now built-in: `audit_dataset(obfuscation=True)` is the default)**. Per-dataset audit JSON + a combined integrity-report notebook + figures; each analysis ends in a Decision/Gate. Certify usability.

### Step 3 — Jobs 2–3 (shortcut + shift; needs embeddings/torch)
Per `eda-design.md`, **highest-value first** (the analyses that would have *predicted* the predecessor's OOD wall pre-GPU):
- **V10** reference-scorer score-distributions per slice (ProtectAI on each slice) — the literal §9.5 missing figure; turns "anti-correlation" from *interpretation* into *measurement*.
- **A1** positive-class cube decomposition (intent × technique × channel) — the heterogeneous-positive picture; map each source to a corner; shows train↔OOD as opposite corners with *zero modeling*.
- **E1** per-fold proxy-A-distance (+ MMD) — the modeling go/no-go; tall PAD bars *predict* OOD collapse per fold pre-GPU.
- + C1 log-odds + C2 partial-input/competency baselines (the *true* floor) + F2 BIPIA attack-type diversity / intra-type similarity (**resolves RC0**) + V4 embedding UMAP (pair with silhouette/ARI per the UMAP-distances-aren't-metric pitfall) + F1 NotInject validity + D3 ProtectAI contamination.
- Cartography (Swayamdipta 2020) = a probe-pass diagnostic (needs one training run; not pre-modeling).
- **Fix the prototype's BIPIA loader collapse** (`/Users/brandonbehring/Claude/prompt-injection-detection-submission/src/data/loaders.py:527-562` discards carrier identity + payload position — needed for the indirect analyses).

### Checkpoints for your review
1. ✅ After the layer's refinements (drop `seed`, fold obfuscation in) — eval-toolkit **PR #83 OPEN**.
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
- **#5** `Step 1 — Build eval-toolkit EDA profiling + DataAudit layer (integrity-gate)` — **PR-1 OPEN** (`brandon-behring/eval-toolkit#83`); Jobs 2–3 build deferred to PR-2 (see #7).
- **#6** `Step 2 — Run Job-1 integrity gate across all datasets` — **unblocked, START HERE** (consume PR-1 via editable install).
- **#7** `Step 3 — Build + run Jobs 2-3 (shortcut + shift EDA)` — **pending** (now reframed as the PR-2 eval-toolkit work + portfolio Job-2/3 run).
- **#8** `Phase 2 — Consolidate ROADMAP.md + archive + fixes + post-mortem + ADRs` — **pending** (Phase 2; follows Phase 1).
- **#9** `Phase A — Dataset-scope completeness` — **completed**.
- **#10** `Dossier-audit round 1: dataset agent_index` — **completed**.

## Gotchas / open items
- **WildGuardMix is gated** (`auth_required: true` — AI2 Responsible Use); needs an HF token to actually download.
- **Harelix** (`harelix2024mixedtechniques`) HF page is bot-blocked (HTTP 401 to WebFetch); the entry's `status: unverified` reflects that; schema + label semantics need a re-fetch via the HF API / `datasets` lib before training use.
- **`xtram12024safeguardpromptinjection`** is `mismatched` — its card cites arXiv:2402.13064 = the unrelated GLAN paper. Flag in any downstream use.
- The **scoped CPU-torch-for-EDA exception to ADR-051** is noted in the plan but **not yet ADR'd** — to be authored alongside PR-2 (the embedding-map work) or in Phase 2 consolidation.
- **`NEXT_SESSION.md` is stale** (last update 2026-05-23 — predates this entire session). Refresh deferred to Phase 2 consolidation.
- **Editable install of the open PR** (`uv pip install -e /Users/brandonbehring/eval-toolkit`) is the recommended Step-2 consumption path; re-pin to a released version once PR-1 lands.
- **NFKC limitation documented in the layer** (`obfuscation.py` + `test_eda_obfuscation.py`): NFKC does not fold cross-script homoglyphs (Cyrillic 'а' stays 'а'). A future cross-script detector belongs in Job-2.
- The user's **strongest standing preference** (per memory `interrogate-before-planning`): present-first + interrogate inconsistencies in your *own* plan + ask focused goal-clarifying questions *before* convergence. `ExitPlanMode` will be rejected if you've under-interrogated. Surface real plan inconsistencies before requesting approval.

---

*↓ Historical content (pre-2026-05-28 — Phase B research-ingestion close, R26 dogfooding adoption, etc.) preserved in git history. The above is the current source of truth.*
