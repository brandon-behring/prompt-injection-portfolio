# NEXT_SESSION

**Scope**: cold-start anchor for a fresh session (potentially on a different
machine). Install instructions + commit summary + critical context.

**Last update**: 2026-05-22 (Round 23 cross-machine handoff; planning artifacts
committed publicly per Round 23 Q1 lock).
**Repo state**: 20+ commits on main; `v0.1.0-pre` tagged at Day 3b;
`make ratify-milestone` PASSES end-to-end.
**Pre-alpha banner**: ACTIVE.

---

## Companion handoff docs

- [`M0_READINESS.md`](M0_READINESS.md) — `make ratify-milestone` gates +
  user-led TODO checklist (dossier sprint + accounts + formal v0.1.0 tag)
- [`docs/planning/README.md`](docs/planning/README.md) — index of design
  rationale + how to read 5 planning artifacts
- [`docs/research/compass-survey/README.md`](docs/research/compass-survey/README.md)
  — index of 3 research-survey artifacts (Anthropic Compass-generated) +
  Days 6-12 dossier-sprint workflow pointer

---

## Where to start (pick up cold from any machine)

1. **Clone the sibling submission** at the parent of portfolio:
   ```bash
   cd <parent-dir>
   git clone -b v1.3.0 https://github.com/brandon-behring/prompt-injection-detection-prototype.git \
     prompt-injection-detection-submission
   ```
   (The editable dep in `pyproject.toml` `[tool.uv.sources]` expects this
   sibling layout.)

2. **Setup**:
   ```bash
   cd prompt-injection-portfolio
   uv sync --extra dev   # ~4GB download (torch + transformers etc.)
   ```

3. **Verify the M0 state**:
   ```bash
   make ratify-milestone   # 12+ gates; expected: all green
   ```

4. **Read the plan + handoff** (all now in-repo per Round 23 Q1 lock):
   - Plan ground truth: [`docs/planning/PORTFOLIO_PLAN.md`](docs/planning/PORTFOLIO_PLAN.md)
     (~2124 lines; 22+ `/exploring-options` rounds locked through Round 23).
   - Companion planning docs at [`docs/planning/`](docs/planning/):
     - `portfolio-chapter-outlines.md` (13-chapter KF-decomposed outline)
     - `portfolio-experiment-record-template.md` (4-file schema)
     - `portfolio-lane-execution-playbooks.md` (6 lane playbooks)
     - `eval-toolkit-v0.43-to-v1.0-roadmap.md` (upstream roadmap context)
   - Research surveys at [`docs/research/compass-survey/`](docs/research/compass-survey/)
     (3 Anthropic Compass surveys; ~1055 lines total; dossier-sprint
     source material).
   - Other public surfaces: this file + `M0_READINESS.md` + `README.md` +
     `decisions/README.md` (ADR index) + `decisions/upstream_issues.md`
     (MR state machine) + `decisions/library_imports.md` (v0.47 registry).

---

## M0 status: close-ready (formal `v0.1.0` tag DEFERRED to user-led)

18 commits since repo seed (2026-05-19 → 2026-05-22):

```
9b07cdf  Day 1   — seed (README + LICENSE + ETHICS.md + verify scripts)
4676cc7  Day 1   — NEXT_SESSION.md (v1)
f011726  Day 2   — book/ scaffold + pyproject + verify_editable_dep
11175db  Day 2   — CI workflow draft (two-step checkout)
e6a2234  Day 2.5 — file 9 upstream MR issues (Round 10 ongoing-filing)
bc30c52  Day 3a/c1 — pin bumps (eval-toolkit v0.47 + scaffold v3.5 + submission v1.2.16)
cbf7d25  Day 3a/c2 — library_imports + upstream_issues state machine + MR-12 file
8d6a60d  Day 3a/c3 — NEXT_SESSION.md rewrite (Round 14-21 absorbed)
6c75693  Day 4   — Round 20 reconciliation close
81765f7  Day 3a/c4 — ruff cleanup (CI hard-gate green)
0a4938a  Day 3b  — 7 test-contracts active + CI hard-gates → tag v0.1.0-pre
3fb9338  Round 22 mini — CI ref v1.2.16 → v1.3.0
7429e33  Day 16  — Docker T2 (Dockerfile + compose + verify extension)
c30a40e  Day 5   — 6 lane experiment-record skeletons + MANIFEST.json
dcf037a  Day 14  — 13 textbook chapter skeletons + 6 fragment dirs
04922fe  Day 15  — governance finish (SECURITY + CODE_OF_CONDUCT + templates + frontmatter + README 3-guides)
add5efc  Day 17  — 11 substantive ADRs + decisions/README.md index
6a59b40  Day 18  — build-in-public templates (Round 19 loudness policy)
b1b66f4  Day 19 prep — ratify-milestone Makefile target + M0_READINESS.md handoff
```

---

## What's next (user-led; per Round 22 Q2 + Q4 deferrals)

### 1. Dossier sprint (M0 Days 6-12; ~60-80 files)
- **Skills needed**: `research_toolkit`'s `/research-plan` + `/research-gather` +
  `/dossier-build` + `/dossier-audit` (not in autonomous /loop's skill set)
- **Input**: 3 compass artifacts at `~/Downloads/compass_artifact_*.md`
  (~1055 lines total)
- **Output**: `docs/research/` with claim_family-keyed dossier files

### 2. Build-in-public account creation (M0 Day 18 final step)
- **Twitter/X**: create `@brandonmbehring` or similar handle
- **Mastodon**: `sigmoid.social` account (ML research community)
- **M0 announcement post**: draft using
  `docs/build-in-public/_template_milestone.md`; post to all loud channels
  per ADR-023 + Round 19 follow-up Q2

### 3. Formal `v0.1.0` tag (M0 Day 19 close)
```bash
make ratify-milestone               # final check; all gates green
git tag -a v0.1.0 -m "M0 close: ..." # annotated tag
git push origin v0.1.0
gh release create v0.1.0 \
  --notes-file docs/build-in-public/2026-WW-week01-announcement.md
```

### 4. Memory + CHANGELOG update at v0.1.0 close
- Update `~/.claude/.../memory/portfolio_plan_approved.md` description
  to "v0.1.0 tagged on YYYY-MM-DD" (in-place per Round 14 round-2 Q4)
- Bump MEMORY.md description suffix
- Add CHANGELOG.md entry (if not already present)

---

## Open upstream MRs (per `decisions/upstream_issues.md`)

- **MR-3** (research_toolkit#1): `/dataset-synthesize` skill — M3-blocking
  (escalate if M2/M3 approaches without ship)
- **MR-12** (eval-toolkit#69): Tier-2 Protocol consolidation —
  NOT blocking; targets eval-toolkit v0.48+

All 7 eval-toolkit MRs (MR-1/2/4/5/6/7 + MR-10 obsoleted) + 2
book-scaffold-astro MRs (MR-8 + MR-9) are CLOSED upstream.

---

## Plan + memory pointers

- **Plan ground truth** (in-repo per Round 23 Q1):
  [`docs/planning/PORTFOLIO_PLAN.md`](docs/planning/PORTFOLIO_PLAN.md)
- **Memory index** (NOT in repo; lives on user's `~/.claude/`):
  `~/.claude/projects/-home-brandon-behring-Claude-prompt-injection-detection-submission/memory/MEMORY.md`
- **Key project memory**: `portfolio_plan_approved` (in-place updated
  through Round 23).
- **Related feedback memories** (NOT in repo; sync from origin separately
  if needed on new machine):
  - `library_first_is_project_wide_invariant` (no local workarounds)
  - `hierarchical_depth_derivation_rule` (L0-L5 layer model)
  - `experiment_record_4_file_schema` (hypothesis/protocol/results/decisions)
  - `snap-gh-needs-repo-path-for-body-file` (gh CLI workaround for snap)
  - `exploring-options-over-handoff-doc-preferred` (multiple-round walkthrough preferred)

## Optional: symlink ~/.claude/plans/ → in-repo (Round 23 Q1 SoT)

On the origin machine (or any machine continuing plan-mode work):
```bash
# Move plan-mode file to in-repo location + symlink back for plan-mode discovery
mv ~/.claude/plans/i-want-to-consider-merry-milner.md /tmp/backup.md  # safety
ln -sf $(pwd)/docs/planning/PORTFOLIO_PLAN.md \
    ~/.claude/plans/i-want-to-consider-merry-milner.md
```

Future plan-mode edits land at `docs/planning/PORTFOLIO_PLAN.md` directly;
single canonical source. Eval-toolkit roadmap can be symlinked similarly
from `~/.claude/plans/evaluate-all-the-work-twinkly-kite.md` to
`docs/planning/eval-toolkit-v0.43-to-v1.0-roadmap.md`.

---

## Critical context (load-bearing; do NOT lose at compaction)

### v0.47 canonical API surfaces (Round 20)
Portfolio code uses ONLY:
- `from eval_toolkit import scorecard, sweep, metric_specs`
- `from eval_toolkit import TextTransform, Probe, MetricSpec, MetaLearner, Scorer`
  (top-level canonical per ADR 0002)
- `from eval_toolkit.adversarial import ALL_TECHNIQUES` + 12 dataclasses
- `from eval_toolkit.preprocessing import DelimitVariant, DatamarkVariant, EncodeVariant`
- `from eval_toolkit.losses import RecallAtLowFPR` (requires `[losses]` extra)
- `from eval_toolkit.probes import ActivationDeltaProbe` (requires `[probes]` extra)
- `from eval_toolkit.stacking import LogisticStacker`

**Do NOT** use: SimpleNamespace patterns (`character_injection.zero_width_space`);
per-module Protocols (`CharacterInjectionStrategy`); module-level sweeps
(`adversarial.sweep`); top-level scalar metric imports (`from eval_toolkit
import pr_auc` — REMOVED in v0.47.0).

### 3-guide architecture (Round 17 + ADR-044)
- M7 v0.7.0 ships textbook only (`book/src/content/textbook/`)
- v0.8.0 (~month 13): narrative guide (`book/src/content/narrative/`)
- v0.9.0 (~month 14): academic IMRaD (`book/src/content/academic/`)
- v1.0.0 (~month 16-17): all 3 polished + citable
- Shared substrate: `book/src/content/fragments/lane-N/{methodology,results,interpretation}.mdx`

### Lane 2 scope (Round 15 + ADR-043)
- Retrain = LoRA-only on ModernBERT-base; no full-FT
- All trainable baselines + Lane 4 stacker + Lane 5 probe train on the
  SAME Lane 2 MR-3 corpus (Round 16 cross-lane comparability)
- Lane 5 timing shifts M2 → M4 (Round 16 Q5; post-Lane-2-corpus)

### Submission CI ref policy
- Currently pinned at `v1.3.0` (Round 22 mini-commit advance)
- Dynamic-detect via `git ls-remote --tags origin | grep refs/tags/v1.X.X
  | sort -V | tail -1` on next Day-3a-style re-sync

---

## What NOT to do

- **Don't** retrain full fine-tuning (Round 15 Q1 LoRA-only across portfolio)
- **Don't** train baselines on different corpora (Round 16 Q1 cross-lane
  comparability requires same Lane 2 MR-3 corpus)
- **Don't** use eval-toolkit SimpleNamespace patterns or module-level sweep
  (Round 20 — removed in v0.47.0)
- **Don't** start narrative + academic chapter authoring before v0.7.0 M7
  textbook ratification (Round 17 Q3 sequential rollout)
- **Don't** publish synthetic adversarial data without ETHICS.md cross-reference
  (ADR-022 + ADR-041)
- **Don't** report AUPRC/AUROC on single-class slices (val-fixed TPR only;
  enforced upstream via eval-toolkit#39 + submission ADR-055)
- **Don't** ship a "transition commit" with both library-first + hand-rolled
  paths live (per memory `no-orphaned-code-during-refactor`)
- **Don't** rewrite git history (per CLAUDE.md "no amend / no squash / no force-push")
