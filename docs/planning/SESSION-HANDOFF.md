# Session handoff — 2026-05-26

Cold-start anchor for the work done in the 2026-05-26 session. Complements `NEXT_SESSION.md`
(the standing M0-close anchor); this doc is the **live in-flight delta**. Three distinct efforts ran;
all are **UNCOMMITTED**.

## ⚠️ Commit status (read first)

- Branch `main`, HEAD `438b1ae` (unchanged — **nothing committed this session**).
- **44 uncommitted working-tree changes** (31 modified + 13 new). These live only on **this machine's
  working tree** — a fresh clone on another machine will NOT have them until they're committed + pushed.
- Suggested commit structure (on a branch, when ready): (1) dependency-adoption, (2) attack-study design
  docs, (3) research-toolkit Phase-A audits. Nothing has been committed because the user hasn't asked.
- Contract tests green throughout (`uv run --no-project --with pytest pytest -m contract` → 13 passed).

## Plan file

`/Users/brandonbehring/.claude/plans/what-is-happening-here-parsed-dahl.md` currently holds **Effort 3's
plan** (research-toolkit re-engagement). Efforts 1 & 2 were earlier plans (overwritten); their designs
live in the repo (ADR-051, ADR-052, `docs/planning/*`).

---

## Effort 1 — Dependency adoption (dogfooding) — ✅ DONE (uncommitted)

Adopted newer upstream lib versions by *using* them (dogfooding), per **ADR-051**:
- **eval-toolkit `>=0.47`→`>=1.0`** (`pyproject.toml`; lock → 1.2.0). No code consumed it yet; forward-guidance in `library_imports.md`.
- **research_toolkit: dropped as a pip dep → repo-local pinned tooling clone `.tooling/research_toolkit@v2.4.0`** (`Makefile` `dossier-audit` bootstraps + runs validators via an ephemeral `uv` env; `.gitignore` += `/.tooling/`). Reason: it only dragged docling/pdfplumber for code nothing imports.
- **book-scaffold-astro `^3.6.5`→`^4.4.0` (resolves 4.5.1) + research-portfolio profile.** `astro.config.mjs` → `styles:[researchPortfolioStyle]`; `content.config.ts` → `defineBookSchemas({preset:'research-portfolio', chaptersBase:'./src/content/textbook'})`. Forced consumer fixes: per-chapter `freshness` (all 13), required `last_verified`, HTML→MDX comments (6 chapters). **Book builds green.**
- **runpod-deploy:** no change (PyPI 0.8.4 == pin).
- **Test contracts updated:** `test_mypy_strict_clean.py` (eval pin `>=1.0`), `test_library_imports_registered.py` (research_toolkit reclassified out of the import scan).
- **4 upstream issues filed:** book-scaffold-astro **#74** (freshness/last_verified docs), **#75** (validate CLI ignores preset/chaptersBase); research_toolkit **#26** (docling hard-dep packaging), **#27** (evidence_ledger cache-absent handling).
- **2 memories saved** (`~/.claude/projects/.../memory/`): `interrogate-before-planning`, `dogfooding-upgrades`.

**Next:** commit when ready. Heavy `uv sync` (torch) + submission sibling left to CI per decision.

---

## Effort 2 — Attack-type-generalization study — Phase 0 ✅ DONE; Phases 1-3 FUTURE (uncommitted)

Reoriented the detector effort. **The reframe (verified against the submission's RESULTS.md v1.3.0):**
on pooled OOD, **every rung AND SOTA ProtectAI sit at/below the random floor (0.374)** — frozen 0.364,
ProtectAI-v1 0.361, v2 0.314, LoRA 0.293, TF-IDF 0.291. So direct→indirect transfer has no signal;
"frozen>LoRA" is a **mirage** (two sub-random detectors) and the comparison was **confounded** (frozen
pre-head + uniform untuned recipe + no model selection; LoRA hit 0.974 in-dist = overfitting not a bug;
full-FT OOD was never measured — ADR-075 crash).

**The pivot (ADR-052):** indirect→indirect **attack-type generalization** via BIPIA's native **disjoint
15/15 attack-type train/test split** (verified in `microsoft/BIPIA`; only "Language Translation"
overlaps; obfuscation sub-family is a clean technique slice; ⚠️ small diversity = ~75 attack strings/
split → memorization risk). **Axis C** = attack-type-LODO core + joint carrier+attack-shift check.
Methodologist-first; an honest negative result is acceptable.

**Artifacts:** `decisions/ADR-052`, `docs/planning/attack-type-lodo-harness-spec.md`,
`docs/planning/submission-methodology-audit.md`, `decisions/README.md` (index + tally → 52).

**Next:** Phase 1 (build harness + independently train frozen-probe/LoRA/full-FT with **fair per-rung
tuning on a train-internal val split**; ~$250/CI) → Phase 2 (interventions: Attention Tracker,
counterfactual augmentation) → Phase 3 (lane/chapter restructure + writeup). The dataset dossier from
Effort 3 (Phase C) is the upstream this study needs.

---

## Effort 3 — Research-toolkit re-engagement sprint — 🔄 IN PROGRESS (Phase A done)

Plan approved: **A→B→C→D, full strict-live**, one continuous sprint (re-engage overlooked toolkit
patterns + ingest overlooked research). Skills (`/freshness-audit`, `/citation-audit`,
`/research-gather`, `/agent-index`, `/dataset-research`, `/research-kb-export`) are available in-session.

**Phase A ✅ DONE** — ran `freshness-audit` + `build_dashboard.py` + `verify_citations.py` on all 5
dossiers (via `.tooling/research_toolkit@v2.4.0` + ephemeral `uv` env). Produced **5 new `dashboard.md`**
(never existed) + completed `citation_audit_report.md` to **5/5** (was 2/5).

**Phase A FINDINGS (the overlooked debt):**
- `freshness --strict`: detector-landscape ✅, agentic ✅; **direct-vs-indirect 16 errors,
  training-and-evaluation 21, rag-injection-defenses 26** (63 total). Root cause = **missing cached
  files** (PDF + body_text + body_meta) for named sources (e.g. direct-vs-indirect: CaMeL/SecAlign/
  Instruction-Hierarchy/Meta-SecAlign) — **NOT staleness** (0 stale blockers everywhere). The dossiers
  reference a cache that isn't fully present on this machine.
- Grounding gaps (dashboards): verbatim-anchored **0%** (agentic), **8%** (training-and-eval), 39%
  (detector), 81% (direct), 88% (rag); **corroboration ~0% everywhere** (synthesis_entry unused).

**Phase A remediation (diagnosed, bounded):** re-fetch the ~15–20 missing cached sources via
`.tooling/research_toolkit/scripts/cache_source.py <url> --topic <t> --escalate-on-failure` (Phase-3
refresh) → re-run freshness/citation until 5/5 green.

**Next (pacing was the OPEN question to the user):**
1. **Cache-repair** the missing sources → all 5 dossiers freshness-green.
2. **Phase B** — full strict-live ingestion of the **67-source backlog in `docs/research/_inbox/
   missed_seeds.md`** (incl. foundational Perez&Ribeiro 2022, DomainBed, Spotlighting, CaMeL, MELON,
   WASP) + **this session's uncaptured sources** (Attention Tracker, ASIDE, Mirror, PromptLocate,
   Indirect-in-the-Wild, BIPIA attack-type structure), topic-by-topic: `/research-gather` →
   `/agent-index` → `/dossier-audit` → `/citation-audit`. (Notably grows the thin agentic + RAG dossiers.)
3. **Phase C** — `/dataset-research` on indirect-injection attack datasets → `dataset_ledger`
   (`docs/research/datasets/`); **directly feeds ADR-052** (BIPIA attack-type taxonomy + alternatives).
4. **Phase D** — `docs/planning/research-ingestion-protocol.md` + `/research-kb-export` to
   `~/Claude/research-kb/inbox/` + **ADR-053** + registry/`NEXT_SESSION` updates.

---

## Environment notes (for a clean session)

- **Lean portfolio venv** (no torch/docling deliberately — ADR-051). Full `uv sync --extra dev` (~4 GB
  torch) needs the **submission sibling** `../prompt-injection-detection-submission` which is **NOT
  cloned locally** → heavy gates (full sync, training) run in **CI / a complete env**, not here.
- **`~/Claude/research_cache`** ≈ 2467 files (mostly populated; ~15–20 named sources missing → the
  Phase-A freshness failures).
- **`.tooling/research_toolkit@v2.4.0`** bootstrapped (pinned, gitignored). Run validators/scripts via:
  `uv run --no-project --with pyyaml [--with requests] python .tooling/research_toolkit/...`.
- The toolkit **skills** hardcode `~/Claude/research_toolkit` (a dirty feature branch); prefer the
  pinned `.tooling` clone for reproducibility (as done in Phase A).
- **`make dossier-audit`** bootstraps `.tooling` + runs the 9 validators (needs the cache populated;
  will fail on the same ~15–20 missing sources until cache-repair).

## Open decisions / loose ends

- **Commit the 44-file working tree?** (suggested 3 commits on a branch). Nothing committed yet.
- **Effort-3 pacing:** cache-repair now vs jump to dataset dossier (unblocks ADR-052) vs pause to review
  the new dashboards/citation reports.
- **Effort-2 Phase 1** needs CI/full env (training, ~$250).
- **Misplaced file:** `encoder-classification-design-space.md` sits untracked at the repo root but its
  own header says it's gitignored `.scratch/` (a submission artifact that landed here) — decide to move
  to `.scratch/` or remove. The user pointed at it; it seeded Effort 2.

## How to resume

1. Read this + the plan file + `decisions/ADR-051` + `decisions/ADR-052` + `docs/planning/submission-methodology-audit.md`.
2. `git status` (confirm the 44 changes present) + `git -C .tooling/research_toolkit describe --tags` (expect `v2.4.0`).
3. Pick up Effort 3 (cache-repair → Phase B/C/D) or wherever directed; Efforts 1 & 2 are done-pending-commit.
