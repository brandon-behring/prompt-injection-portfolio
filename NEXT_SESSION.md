# NEXT_SESSION

**Last update**: 2026-05-19 (M0 Day 1 close)
**Repo state**: v0.1.0-pre placeholder; pushed to github.com/brandon-behring/prompt-injection-portfolio
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

### ⏸ Day 2 next steps (per plan §21)

1. `npx @brandon_m_behring/create-book prompt-injection-portfolio --profile=academic`
   - Academic profile at first (v3.1)
   - Later upgrade to `--profile=research-portfolio` when scaffold v3.2 ships (R11 lock; BLOCKS M1 book authoring on this)
2. `uv init` + `pyproject.toml` with:
   - `eval-toolkit>=0.42` (per submission v1.0.9 ADR-055/056/058)
   - `runpod-deploy>=0.8.4` (per submission v1.1.0 ADR-059)
   - `research_toolkit` (latest)
   - `[tool.uv.sources] prompt-injection-detection-prototype = { path = "../prompt-injection-detection-submission", editable = true }`
3. Write `scripts/verify_editable_dep.py` (validates sibling-layout import path)
4. Draft `.github/workflows/ci.yml` two-step checkout (portfolio + submission `ref: v1.1.1`)

### M0 Day 3 next

- 7 test-contracts implementation (`tests/contracts/test_*.py`)
- Configure ruff (check + format) + mypy --strict
- Second push → CI must go green → tag `v0.1.0-pre` checkpoint

### M0 Day 4-5

- Implement **MR-1** (`eval_toolkit.loaders.ood_dataset_from_manifest`) upstream in eval-toolkit repo
- Release eval-toolkit v0.42.1
- Pin in portfolio pyproject.toml

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

23 tasks total; 3 complete (#1, #2, #3); 20 pending. Key next:

- **#4** wire CI (Day 2-3): ruff + mypy --strict + pytest + nbval + 7 test-contracts + two-step checkout for submission editable dep
- **#5** file 8 upstream issues (Day 1-3): 7 eval-toolkit/research_toolkit MRs + 1 scaffold v3.1 design issue (deferred; MR-8 now blocking M1 per R11)
- **#6** implement 3 critical upstream MRs (Day 4-13): MR-1 (Day 4-5), MR-7 (Day 13), MR-2 (Day 6-8)
- **#7** dossier work (Day 6-12): 60-80 files via research_toolkit
- **#8** book bootstrap (Day 2 academic; Day 14 chapter skeletons after v3.2)
- **#15** portfolio-clean T0 (Day 17 per plan; eval_from_hub.py reimpl per ADR-035)

---

## What NOT to do

- **Don't** rename the repo again (locked Round 13)
- **Don't** consume submission's eval_from_hub.py (portfolio writes own clean T0 per ADR-035)
- **Don't** hand-roll a primitive that belongs in eval-toolkit / runpod-deploy / research_toolkit / book-scaffold-astro (file upstream issue per [[library-first-is-project-wide-invariant]])
- **Don't** start M1 book authoring before scaffold v3.2 ships (R11 lock)
- **Don't** publish synthetic adversarial data without ETHICS.md cross-reference in dataset card (R8 lock + ADR-022/041)
- **Don't** report AUPRC/AUROC on single-class slices (val-fixed TPR only; submission-enforced via eval-toolkit #39)
