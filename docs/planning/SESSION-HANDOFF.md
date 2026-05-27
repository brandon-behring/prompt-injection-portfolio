# Session handoff — 2026-05-26

Cold-start anchor for the work done in the 2026-05-26 session. Complements `NEXT_SESSION.md`
(the standing M0-close anchor); this doc is the **live in-flight delta**. Three distinct efforts ran;
all are **UNCOMMITTED**.

---

## ⏭ 2026-05-27 UPDATE 2 — v2.5.0 released; Phase B started + backlog reconciled (READ THIS FIRST)

Follow-on session on `session/2026-05-26-adoption-and-research-ops`. Supersedes UPDATE 1's "remaining" + loose-ends below.

- **research_toolkit v2.5.0 released + re-pinned — ✅ `f3d26c3`.** PR #28 reviewed (15 tests, ruff clean, producer reproduces real detector anchors byte-for-byte) → maintainer merged + tagged `v2.5.0` (annotated, at the producer release commit) → `Makefile RT_TAG := v2.5.0` + `.tooling` re-bootstrapped; `make dossier-audit` green ×5. NB: the `v2.4.1..v2.5.0` audit-path is byte-identical (`verify_citations` + every dossier-audit validator unchanged; the only deltas are a new unused-here `topic_backlog.py` + the producer) — so the re-pin is a **reproducibility/provenance** step, not a functional gate change.
- **Phase B premise corrected: `missed_seeds`'s "73-item backlog" is largely ALREADY-TRIAGED, not an open to-do list.** Both Sprint-2 "new" dossiers were built to their plans on 2026-05-22 (cross-class folded in; out-of-scope declined). Verified against the live ledgers this session:
  - **E (rag) was already complete + green** (18 entries); the 3 cross-class items (BIPIA/Spotlighting/EchoLeak) already in. **Scope-expanded**: new family `rag_retrieval_dynamics` (E5) + 3 retrieval/embedding papers (Lost-in-the-Middle 2307.03172, SBERT 1908.10084, Ethayarajh 1909.00512) — `6b0a64f`.
  - **D (agentic) was already complete + green** (25 entries); its "21" was mostly already-in (CaMeL/MELON/Task Shield/IsolateGPT/Design Patterns/LlamaFirewall/AgentDojo) or mis-routed. Added 2 real D1 net-new (Anthropic browser-PI blog + computer-use docs) — `eb31a3f`.
  - **Mis-filed items re-routed** (recorded in the gitignored `_inbox/missed_seeds.md` → "## 2026-05-27 Phase B reconciliation"): UltraChat/LMSYS/XSTest→**C**; InjecAgent/ASB/WASP/WAInjectBench/MCPVerse→**B4**; Whispers→**B1**; the 6 vendor URLs→**A4 (unverified)**.
  - Both E + D: `make dossier-audit` green ×5; citation substring 100% (E 33/33, D 5/5); 0 stale.

### Phase B — what actually remains (corrected)
⚠️ **A (18) / B (10) / C (14 + re-routed) are ESTABLISHED topics — do NOT take the raw `missed_seeds` counts at face value.** Like D/E, each listed net-new must be **checked against the actual bib_ledger first** (many are likely already in or out-of-scope): triage-before-grind. The 4 method sources (Attention Tracker `2411.00348` / ASIDE `2503.10566` / Mirror `2603.11875` / PromptLocate `2510.12252`) still need routing to their correct topics. The PR #28 + v2.5.0 loose-ends in UPDATE 1 below are now **DONE**.

---

## ⏭ 2026-05-27 UPDATE — supersedes the EXECUTION ROADMAP below (read this first)

The continue-all-phases session ran. **STEP 1's premise was wrong** and is corrected; everything is now
committed + pushed on `session/2026-05-26-adoption-and-research-ops`.

- **STEP A (was STEP 1 "cache-repair") — ✅ DONE, committed `3d11757`.** The 63 "freshness errors" were
  **not** missing cache — they were citation-audit **substring** failures from a **path-resolution bug**:
  `verify_excerpt_anchor`'s callers didn't pass the manifest `cache_root`, so relative `text_path`
  resolved against the empty dossier-local `text/` dir. The fix already existed upstream (`33f07f9`, #15,
  merged to main, **never tagged**). Adopted by tagging **research_toolkit `v2.4.1`** at `33f07f9` +
  `Makefile RT_TAG := v2.4.1`. Re-green: substring **0→100%** on all dossiers (detector 61/61, direct
  51/51, training 13/13, rag 28/28, agentic 0/0); **`make dossier-audit` PASS ×5**. No re-fetching. ADR-051
  follow-up records the misdiagnosis. (Lesson saved as memory `tag-pins-strand-fixes`.)
- **STEP B — v3 excerpt-anchor PRODUCER built (the second dogfooding gap).** The toolkit could *check*
  anchors but had no *producer* (BURN_IN 2026-05-25). New `scripts/build_excerpt_anchor.py` (manifest-mode,
  whitespace-tolerant, multi-byte-correct, `--occurrence`, self-verifies through `verify_excerpt_anchor`).
  14 tests, ruff clean, **reproduces all 61 real detector-landscape anchors** (41 via `--occurrence`).
  Wired into `/agent-index` Phase 2a + `/research-gather`. **Opened as PR #28 — NOT merged (maintainer-gated;
  do not self-merge).** `.tooling` stays at **v2.4.1**; the **v2.5.0 re-pin is pending the PR #28 merge**.
  For Phase B now, run the producer from the `feat/build-excerpt-anchor` checkout of `~/Claude/research_toolkit`.
- **Phase C dataset dossier — ✅ DONE, committed `ebfd2f2`.** `docs/research/datasets/` = 20-entry
  `dataset_ledger.yml` + validated `agent_index/`. Feeds ADR-052 (cross-linked both ways). BIPIA is the
  only set with a disjoint 15/15 attack-type split; honest flags kept (xTRam1 mismatched, PINT withheld,
  5 license-unknown, arXiv 2604.27202 genuine but corpus unreleased).

### Phase B — strict-live ingestion: REMAINING (multi-session)
Per-topic loop, each ending **green**: update `research_plan.md` claim_family → `/research-gather` (append;
`--escalate-on-failure`; caches + evidence_ledger v3 + claim_graph + gather_trace) → **anchor new verbatim
claims with `build_excerpt_anchor.py`** → `/agent-index` → `/dossier-audit` → `/citation-audit`. Gate:
`make dossier-audit` green ×5 + `missed_seeds` drained. Commit per topic.
- Queue from `docs/research/_inbox/missed_seeds.md` (entries are **verify+complete-metadata stubs**, not
  blind searches): **A** detector 18 · **B** direct 10 · **C** training 15 · **D** agentic 21 · **E** rag 9.
  Plus this-session method sources: Attention Tracker `2411.00348`, ASIDE `2503.10566`, Mirror `2603.11875`,
  PromptLocate `2510.12252`. Suggested order: thin dossiers first (**E rag**, **D agentic**).
- **ETHICS exclusions (do NOT ingest):** `browserbench2025adversarial`, `restricted2025threatreport`
  (synthetic/placeholder URLs); `piv4internaldata2026`, `piv4evaltoolkitfeedback2026` (internal-repo refs).
  Cross-class entries (CaMeL/Spotlighting/MELON/BIPIA/EchoLeak/LlamaFirewall) get topic-prefixed bibkeys.

### Loose ends (maintainer actions)
- **Merge PR #28** → tag/push `research_toolkit v2.5.0` → bump `Makefile RT_TAG := v2.5.0` + re-bootstrap `.tooling`.
- Open the portfolio PR for `session/2026-05-26-adoption-and-research-ops` (or merge to `main`).
- Effort 2 / STEP 5-7 (attack-type-LODO training) still needs CI / ~$250 / the un-cloned submission sibling.

---

### ↓ Original 2026-05-26 roadmap below (STEP 1 misdiagnosed — see correction above) ↓

## ✅ Commit status (read first)

- **Committed + pushed** on branch **`session/2026-05-26-adoption-and-research-ops`** (off `main`;
  `main` untouched), 3 commits:
  - `8a63794` — dependency adoption / dogfooding (ADR-051), 30 files
  - `f0c1012` — attack-type-generalization reorientation (ADR-052) + design docs, 4 files
  - `8cedd82` — research_toolkit Phase-A audits (5 dashboards + 5 citation reports) + this handoff, 11 files
- Pushed to `origin` → **durable across machines**. PR not yet opened (yours to open/merge).
- **Excluded (still untracked):** `encoder-classification-design-space.md` — the misplaced `.scratch/`
  submission artifact (loose end: move to `.scratch/` or remove).
- Contract tests green (`uv run --no-project --with pytest pytest -m contract` → 13 passed).
- This handoff's roadmap edits + all further work are NEW changes on top of the 3 commits — commit per step.

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

## EXECUTION ROADMAP — continue all phases

Integrated + dependency-ordered. **Research-ops (Effort 3) precedes the empirical study (Effort 2)** —
the study must run on current, ingested research + the dataset dossier. **Commit per step.**

### Quick-start (fresh session)
1. `git fetch && git switch session/2026-05-26-adoption-and-research-ops` (or merge to `main` first).
2. Read: this doc → `decisions/ADR-051` → `decisions/ADR-052` → `docs/planning/submission-methodology-audit.md` → `docs/planning/attack-type-lodo-harness-spec.md`.
3. State-check: `git -C .tooling/research_toolkit describe --tags` (expect `v2.4.0`); `find ~/Claude/research_cache -type f | wc -l`; `grep -E 'stale|verbatim|corroborated' docs/research/*/dashboard.md`.
4. Start at STEP 1.

> **Invocation pattern (lean, no torch):** `uv run --no-project --with pyyaml --with requests [--with pdfplumber] python .tooling/research_toolkit/<path>`. Toolkit **skills** (`/freshness-audit`, `/citation-audit`, `/research-gather`, `/agent-index`, `/dossier-audit`, `/dataset-research`, `/research-kb-export`) are invocable in-session — prefer the pinned `.tooling` clone over the dirty `~/Claude/research_toolkit`.

### STEP 1 — Effort 3: cache-repair → all 5 dossiers freshness-green
Failing: direct-vs-indirect (16), training-and-evaluation (21), rag-injection-defenses (26) — all **missing cached sources**, not staleness.
- Per failing dossier: list missing via `validators/freshness.py --strict docs/research/<t> --today <DATE>` (names bibkeys, e.g. direct-vs-indirect: `debenedetti2025camel` / `chen2025secalign` / `wallace2024instructionhierarchy` / `chen2025metasecalign`); get `source_url`s from that dossier's `cache_manifest.yml` / `bib_ledger.yml`; re-fetch with `scripts/cache_source.py <url> --topic <t> --escalate-on-failure` (writes `papers/` + `cache/body_text/` + `cache/body_meta/` + updates manifest). Mind the dual cache: global `~/Claude/research_cache` vs dossier-local `cache/`.
- **Gate:** `freshness.py --strict` OK ×5 + `verify_citations.py` acceptable ×5; rebuild dashboards (`scripts/build_dashboard.py`). Commit.

### STEP 2 — Effort 3 Phase B: full strict-live ingestion (biggest; multi-session)
- Triage `docs/research/_inbox/missed_seeds.md` (67, binned A–E) + this-session sources: **Attention Tracker** (2411.00348), **ASIDE** (2503.10566), **Mirror** (2603.11875), **PromptLocate** (2510.12252), **Indirect-in-the-Wild** (2604.27202), the submission-audit findings, the BIPIA attack-type structure. Dedupe vs `bib_ledger`.
- Per topic: update `research_plan.md` claim_family (new families: adaptive/"attacker-moves-second", OOD-eval-methodology, agentic-defense, RAG-defense) → `/research-gather` (append; caches + evidence_ledger v3 + claim_graph + gather_trace; **verifies/drops the recent arXiv IDs**) → `/agent-index` → `/dossier-audit` → `/citation-audit`.
- **Gate:** `make dossier-audit` green ×5; `missed_seeds` drained; citation 5/5. Commit per topic. (Grows the thin D/agentic + E/RAG dossiers.)

### STEP 3 — Effort 3 Phase C: dataset dossier (feeds Effort 2)
- `/dataset-research` on indirect-injection attack/detection datasets → `dataset_ledger.yml` + index at `docs/research/datasets/`. Cover **BIPIA** (+ its 15/15 attack-type taxonomy — the ADR-052 input), InjecAgent, AgentDojo, LLMail-Inject, ASB, HackAPrompt, Indirect-in-the-Wild, deepset, ProtectAI-validation, NotInject, PINT, TensorTrust, GenTel-Bench (schema / size / license / attack-type labels / encoder-readiness). Cross-link `ADR-052` + the harness spec.
- **Gate:** `dataset_ledger` validates (dataset-index audit); covers the harness-spec datasets. Commit.

### STEP 4 — Effort 3 Phase D: ingestion protocol + export + ADR-053
- Write `docs/planning/research-ingestion-protocol.md` (repeatable new-source → dossier workflow + standing `_inbox/` triage). `/research-kb-export` per dossier → `~/Claude/research-kb/inbox/` (only after citation-audit passes). **ADR-053**; update `decisions/README.md` + `decisions/library_imports.md` (skills now used: freshness-audit / citation-audit / dataset-research / research-kb-export) + `NEXT_SESSION.md`.
- **Gate:** `research_kb_export.jsonl` per topic; ADR-053 indexed. Commit.

### STEP 5 — Effort 2 Phase 1: build + run the attack-type-LODO ⚙️ NEEDS FULL ENV / CI (~$250)
- Build per `docs/planning/attack-type-lodo-harness-spec.md`: `(content,label)` from BIPIA attacks×scenarios; **disjoint-attack-type folds** (train-types→test-types) + **obfuscation sub-split** + **joint carrier+attack shift**; train-internal val.
- Independently train frozen-probe + LoRA + full-FT (ModernBERT-base) with **fair per-rung tuning on the train-internal val** (LODO test untouched); trainable-head option for LoRA.
- Metrics: AUPRC + TPR@{1,0.5,0.1}%FPR + **random-floor per fold** + benign FPR + in-dist-vs-LODO inflation.
- **Env:** clone the submission sibling (`git clone -b v1.3.0 https://github.com/brandon-behring/prompt-injection-detection-prototype.git ../prompt-injection-detection-submission`) + `uv sync --extra dev` (~4 GB torch) — NOT the lean local venv; run in CI / a complete machine.
- **Gate:** reproduce random-floor + in-dist→LODO gap on ONE fold before scaling; per-fold results table. Commit.

### STEP 6 — Effort 2 Phase 2: interventions (does anything beat the floor?)
- **Attention Tracker** (training-free, inference-only → cheap first), **counterfactual augmentation**, optionally **ASIDE** — using the method research ingested in STEP 2.
- **Gate:** per-intervention LODO delta vs the random floor. Commit.

### STEP 7 — Effort 2 Phase 3: restructure + writeup
- Reorganize the 6 mechanism-lanes → the robustness/eval-rigor structure (per the deliberation in git history); rewrite affected chapters (ch08–ch13); new ADR(s); the honest **"universal OOD wall + what (if anything) generalizes across injection types"** narrative + the in-dist-vs-LODO inflation demonstration.
- **Gate:** book builds; ADRs consistent; `make dossier-audit` green. Commit.

## Loose ends not on the critical path
- Open the PR for the session branch (or merge to `main`).
- Move/remove `encoder-classification-design-space.md` (misplaced `.scratch/` artifact).
- `cache_manifest` schema still v2 (v3 substring-anchor upgrade deferred; not blocking).
