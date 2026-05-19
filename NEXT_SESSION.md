# NEXT_SESSION

**Last update**: 2026-05-19 (M0 Day 2 close + upstream-issues batch filed)
**Repo state**: v0.1.0-pre; 4 commits on main; 9 upstream MRs filed (8 blocking + 1 deferred)
**Pre-alpha banner**: ACTIVE (visible in README + book frontmatter once book/ bootstraps)

---

## Where to start (pick up cold)

1. Read `/home/brandon_behring/.claude/plans/i-want-to-consider-merry-milner.md` (the plan; ground truth for all decisions).
2. Read the 3 companion docs alongside the plan:
   - `portfolio-chapter-outlines.md`
   - `portfolio-experiment-record-template.md`
   - `portfolio-lane-execution-playbooks.md`
3. Check memory anchors at `~/.claude/projects/-home-brandon-behring-Claude-prompt-injection-detection-submission/memory/MEMORY.md` — especially:
   - `portfolio_plan_approved.md` (project state + Round 6-13 deltas)
   - `library_first_is_project_wide_invariant.md` (no local workarounds rule)
   - `experiment_record_4_file_schema.md` (4-file pattern)
   - `lane_playbook_pattern.md` (per-lane playbook structure)
   - `companion_doc_pattern_for_large_plans.md` (when to extract detail)
4. `git status` here to see uncommitted vs committed state
5. `gh repo view brandon-behring/prompt-injection-portfolio` to confirm public state

---

## M0 status (Day 1 complete; Day 2 starting)

### ✓ Day 1 done

- Pre-flight gates: npm scaffold v3.1.0 + create-book v3.1.0 ✓
- 6 OOD eval sources reachable (BIPIA / AgentDojo / InjecAgent / NotInject / LLMail-Inject / PINT) ✓
- Docker daemon + alpine pull ✓
- Public GitHub repo created ✓
- Initial commit `9b07cdf` pushed (7 files):
  - README.md (132L; scientific-abstract-scaled + pre-alpha banner)
  - LICENSE (Apache-2.0)
  - ETHICS.md (227L; from plan §20)
  - .gitignore
  - Makefile (M0 Day 1 verify targets)
  - scripts/verify_data_sources.py
  - scripts/verify_docker.py
- gitleaks scan clean
- `Co-Authored-By: Claude` commit trailer

### ✓ Day 2 done

- `book/` scaffolded via `npx @brandon_m_behring/create-book ... --profile=academic` (11 files; v3.1.0 pinned)
- `book/LICENSE` added (CC-BY-4.0; bifurcation note pointing at root Apache-2.0 LICENSE)
- `pyproject.toml` written (eval-toolkit≥0.42 + runpod-deploy≥0.8.4 + research_toolkit @ git+v1.9.1 + editable submission dep + dev deps + ruff/mypy/pytest config)
- `scripts/verify_editable_dep.py` (sibling-layout check + submission key files validation)
- `.github/workflows/ci.yml` (two-step checkout portfolio + submission ref:v1.1.1; ruff + mypy + pytest + test-contracts; mypy/pytest/contracts allow-failure at v0.1.0-pre until Day 3)
- 3 commits Day 2: `f011726` scaffold+pyproject+verify-deps → `11175db` CI draft
- CI Run #1 triggered on `11175db` at 16:04 UTC (expected partial; will go fully green at Day 3)

### ✓ Day 2.5 done — upstream MR batch filed (per Round 10 ongoing-issue-filing discipline)

- `decisions/upstream_issues.md` (state machine + 9 rows; M0 batch + ongoing section)
- `decisions/library_imports.md` (registry; populated as MRs ship)
- 9 issues filed across 3 repos (issue-filed state):
  - eval-toolkit [#48 MR-1](https://github.com/brandon-behring/eval-toolkit/issues/48) `ood_dataset_from_manifest`
  - eval-toolkit [#49 MR-2](https://github.com/brandon-behring/eval-toolkit/issues/49) `character_injection` 12-suite
  - research_toolkit [#1 MR-3](https://github.com/brandon-behring/research_toolkit/issues/1) `/dataset-synthesize` skill
  - eval-toolkit [#50 MR-4](https://github.com/brandon-behring/eval-toolkit/issues/50) `RecallAtLowFPR` loss
  - eval-toolkit [#51 MR-5](https://github.com/brandon-behring/eval-toolkit/issues/51) `spotlighting` (3 variants)
  - eval-toolkit [#52 MR-6](https://github.com/brandon-behring/eval-toolkit/issues/52) `MetaLearner` + `LogisticStacker`
  - eval-toolkit [#53 MR-7](https://github.com/brandon-behring/eval-toolkit/issues/53) `ActivationDeltaProbe`
  - book-scaffold-astro [#6 MR-8](https://github.com/brandon-behring/book-scaffold-astro/issues/6) v3.2 research-portfolio profile
  - book-scaffold-astro [#7 MR-9](https://github.com/brandon-behring/book-scaffold-astro/issues/7) generic frontmatter primitive (deferred)
- `.scratch/` gitignored (for ad-hoc issue-body drafts; snap-confined gh needs body files inside repo, not `/tmp` or `~/.cache`)

### ⏸ Day 3 next steps (per plan §21)

1. **7 test-contracts implementation** (`tests/contracts/test_*.py`):
   - `no_handrolled_metrics`
   - `predictions_persisted`
   - `leakage_scan_present`
   - `glossary_complete`
   - `library_imports_registered` (parses `decisions/library_imports.md`)
   - `mypy_strict_clean`
   - `experiment_records_complete` (per §18 + Round 7 ADR)
2. Configure ruff (check + format) + tighten mypy --strict
3. First fully-green CI run → tag `v0.1.0-pre` checkpoint
4. Push commit → CI must pass with all gates green (no allow-failure shells)

### M0 Day 4-5 ahead

- Implement **MR-1** (eval-toolkit #48 — `ood_dataset_from_manifest`) upstream
- Release eval-toolkit v0.43.0 (semver-minor for new public API)
- Pin in portfolio `pyproject.toml`; update `decisions/library_imports.md` row
- Advance MR-1 row in `upstream_issues.md` to `pinned-in-portfolio`

---

## Critical context (load-bearing; do NOT lose at compaction)

### Submission predecessor
- Path: `~/Claude/prompt-injection-detection-submission/`
- GitHub: `github.com/brandon-behring/prompt-injection-detection-prototype` (current tag: v1.1.2)
- Status: ADRs frozen at v1.0.1; code patches as v1.0.x → v1.1.x
- Key ADRs for portfolio:
  - ADR-014 English-only scope (carried over)
  - ADR-016 LODO methodology
  - ADR-048 LLM label audit protocol (Lane 2 reuses)
  - ADR-050 rung slate narrowing (Ch 13 case study)
  - ADR-052 LoRA active-harm reframing (Lane 2 hypothesis foundation)
  - ADR-055/056/058 eval-toolkit canonical APIs + T0 wiring
  - ADR-059 runpod-deploy modernization
  - ADR-060/063 DeBERTa-v3-base methodology + null result (Ch 7 case study)

### Scaffold v3.2 BLOCKER (R11 lock)
- Currently at npm v3.1.0
- v3.2 needs to ship before M1 book authoring (chapter skeletons depend on research-portfolio profile)
- v3.2 design locked R12 (union schema academic ∪ tools + 3 new generalized components: PreReleaseBanner / PolicyRef / AICollaborationDisclosure)
- M0 dossier / repo / ETHICS / governance / Docker / MR-1/2/7 / ADRs proceed in parallel (NOT blocked on v3.2)
- ~3-5 days upstream implementation effort

### Plan §21 day-by-day sequence
- Weeks 1-3 total M0
- Day 1: pre-flight + repo create + initial commit (DONE)
- Day 2: scaffold bootstrap + uv init + deps + CI draft
- Day 3: test-contracts + CI green + tag `v0.1.0-pre`
- Day 4-5: MR-1 implementation in eval-toolkit
- Day 6-10: Dossier sprint (60-80 files) + MR-2 + Part I+II chapter skeletons
- Day 11-12: Dossier remaining + final dossier audit
- Day 13: MR-7 (ActivationDeltaProbe)
- Day 14: Part III+IV chapter skeletons (PRECONDITION: scaffold v3.2 shipped)
- Day 15: Frontmatter + governance + README polish
- Day 16: Docker T2 setup
- Day 17: ~30 ADRs writing
- Day 18: Build-in-public account setup + M0 announcement draft
- Day 19: M0 close — `make ratify-milestone M=M0` + tag `v0.1.0` + push announcement

### Round-by-round summary (13 rounds total)
See `portfolio_plan_approved.md` memory or plan §1 decision tables. Highlights:
- R1: name + cost cap + Lane breadth + license
- R2: hierarchical depth + reproducibility tiers + skeleton-first
- R3: AI-disclosure + public from M0 + ETHICS + build-in-public + maintenance
- R4: book authoring details + governance
- R5: post-survey realignment (scaffold v2.0 + submission v1.0.7)
- R6: scaffold v3.0 npm pivot + submission v1.1.2 + portfolio writes own clean T0
- R7: 4 holistic-review focus areas → 3 companion docs
- R8: ETHICS.md content drafted
- R9: M0 day-by-day sequence (§21)
- R10: ongoing GH issue filing permission
- R11: scaffold v3.2 BLOCKS M1 (was deferred; promoted to blocking)
- R12: v3.2 design — union schema + 3 generalized components
- R13: repo rename `prompt-injection-detection-portfolio` → `prompt-injection-portfolio`

---

## Active tasks (taskList; preserved across compaction)

23 tasks total; 4 complete (#1, #2, #3, #5); 19 remaining. Key next:

- **#4** wire CI green (Day 3): ruff + mypy --strict + pytest + 7 test-contracts; remove allow-failure shells
- **#5** ✓ filed 9 upstream issues (Day 2.5; eval-toolkit #48/49/50/51/52/53, research_toolkit #1, book-scaffold-astro #6/7)
- **#6** implement 3 critical upstream MRs (Day 4-13): MR-1 (Day 4-5; eval-toolkit #48), MR-7 (Day 13; #53), MR-2 (Day 6-8; #49)
- **#7** dossier work (Day 6-12): 60-80 files via research_toolkit
- **#8** book bootstrap (Day 2 academic ✓; Day 14 chapter skeletons after MR-8 v3.2 ships)
- **#15** portfolio-clean T0 (Day 17 per plan; eval_from_hub.py reimpl per ADR-035)

---

## What NOT to do

- **Don't** rename the repo again (locked Round 13)
- **Don't** consume submission's eval_from_hub.py (portfolio writes own clean T0 per ADR-035)
- **Don't** hand-roll a primitive that belongs in eval-toolkit / runpod-deploy / research_toolkit / book-scaffold-astro (file upstream issue per [[library-first-is-project-wide-invariant]])
- **Don't** start M1 book authoring before scaffold v3.2 ships (R11 lock)
- **Don't** publish synthetic adversarial data without ETHICS.md cross-reference in dataset card (R8 lock + ADR-022/041)
- **Don't** report AUPRC/AUROC on single-class slices (val-fixed TPR only; submission-enforced via eval-toolkit #39)
