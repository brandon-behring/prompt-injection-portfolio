# NEXT_SESSION

**Scope**: cold-start anchor for a fresh session (potentially on a different
machine). Install instructions + commit summary + critical context.

**Last update**: 2026-05-23 (Round 25 — M0 close follow-up cleanup after Round 24
Sprint 2 closure + Sprint 3 fold-in).
**Repo state**: 41 commits on main; `v0.1.0-pre` tagged at Day 3b.
**R26 dogfooding adoption (2026-05-26, ADR-051)**: eval-toolkit `>=1.0`;
research_toolkit consumed as a repo-local tooling clone pinned `v2.4.0` (dropped as a pip
dep); book-scaffold-astro `^4.4.0` + research-portfolio profile (book builds green).
`make dossier-audit` runs validators from the pinned v2.4.0 clone, but a FULL 5-topic pass
needs the populated `~/Claude/research_cache` body-text cache — a re-fetchable heavy
artifact, like torch (absent here ≠ code-state failure; see Round 24 close + ADR-051).
M0 close artifact-state PASSES.
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

41 commits since repo seed (2026-05-19 → 2026-05-23). Round 24 M0 close + Round
25 follow-up landed Sprint 2 dossier closure + Sprint 3 fold-in + 3 new ADRs +
synthesis doc + BIP post. The originally-deferred dossier sprint is COMPLETE.

### Highlights by phase (most recent first)
- **Round 25** (2026-05-23) — M0 close follow-up cleanup (3 phases):
  `2549994` Phase 1: verification_notes for 2 secondary-blog unverified entries
- **Round 24** (2026-05-23) — M0 close incl. Sprint 3 fold-in (6 commits):
  `8d02272` Phase B: HF 401 attempt + vendor cluster verification
  `fb2669b` Phase C: ADR-036/-038/-041/-045 Sprint 2 dossier cross-refs
  `e41e88f` Phase D: ADR-048 (cross-classification) + ADR-049 (body-quote anchoring)
            + ADR-050 (vendor cluster posture) + Round 24 README
  `4708692` Phase I: book-scaffold-astro ^3.5.0 → ^3.6.5 + MR-13 filed
  `116a405` Phase E: 861-line synthesis doc (dossier_implications_for_roadmap.md)
  `0a29116` Phase F: 175-line Sprint 2 close build-in-public post
- **Sprint 2** (2026-05-22 to 2026-05-23) — dossier expansion (8 commits):
  E1 research_plans / E2 ~124 cached PDFs / E3 verifications + body-anchoring
  / E4 agent_index / E5 audit-trail / E6 MANIFEST + bibliography.bib / F-phase
  fixups / closure
- **Sprint 1 + M0 Day 1-19** (2026-05-19 to 2026-05-22, 18 commits):
  Day 1 seed → Day 19 prep (per prior log; abridged here for brevity)

Full log: `git log --oneline` (41 entries; reverse-chronological).

### Round 24 M0 close deliverables
- 210-entry dossier across 5 topics (97% verified; 166 body-quote-anchored)
- 157 unique BibTeX entries in `book/bibliography.bib`
- 50 ADRs (44 Accepted + 4 Reserved + 2 DROPPED; 48 files)
- 861-line synthesis doc at `docs/planning/dossier_implications_for_roadmap.md`
- 175-line BIP post at `docs/build-in-public/sprint2-close.md`
- `make dossier-audit` PASSES across 5 topics

---

## What's next (user-led; per Round 22 Q2 + Q4 + Round 25 follow-up)

### 1. Dossier sprint — ✅ COMPLETE (Round 24, 2026-05-23)
Sprint 1 (M0 Days 6-12) + Sprint 2 (E0-E6 + closure) + Sprint 3 (M0 close
fold-in) delivered the 5-topic dossier:
- 210 bib_ledger entries (65 detector-landscape + 42 direct-vs-indirect +
  60 training-and-evaluation + 25 agentic-security-architecture + 18
  rag-injection-defenses); 97% verified
- 166 body-quote-anchored carriers (pdftotext + byte-offset + sha256_of_span)
- 124 cached PDFs (~246 MB) under `~/Claude/research_cache/` (gitignored
  per public-repo licensing posture)
- 157 unique BibTeX entries auto-generated to `book/bibliography.bib`
- `make dossier-audit` PASSES (45+ validator checks across 5 topics)
- 6 unverified entries (all with explicit `verification_notes`):
  - 2 vendor cluster (CalypsoAI + SafePrompt; per ADR-050)
  - 2 HF 401 (protectai validation + harelix mixed; per ADR-049 + Phase B)
  - 2 secondary-blog (lakera2024pint + jung2026postmortem; per Round 25
    convention notes — see ADR-050 parallel)
- Synthesis doc: `docs/planning/dossier_implications_for_roadmap.md`
  (861 lines; 3-zone audience layering; 5 roadmap-change proposals;
  decision criteria for Lane 1b / Lane 4 / Lane 5)
- BIP post: `docs/build-in-public/sprint2-close.md` (175 lines; content
  source for future v0.1.0 announcement thread)

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

## Upstream MRs — ALL CLOSED as of 2026-05-24 (per `decisions/upstream_issues.md`)

Every upstream MR the portfolio filed is now resolved:

- **MR-3** (research_toolkit#1): `/dataset-synthesize` skill —
  **MERGED 2026-05-24 (research_toolkit PR #16, squash 4d5b420)**.
  Lane 2's PRIMARY data path is now available (see below).
- **MR-12** (eval-toolkit#69): Tier-2 Protocol consolidation —
  **CLOSED (wontfix-with-docs)**: upstream kept `protocols.py`
  lightweight + added ADR 0004 naming-conventions doc. Top-level
  canonical imports already work; no portfolio change needed.
- **MR-13** (book-scaffold-astro#54): citation-js `%`-comment lexer —
  **CLOSED: resolved in book-scaffold-astro v4.0.0**. Portfolio **adopted v4.x at R26**
  (now `^4.4.0`, resolves 4.5.1; the BREAKING `defineStyle` migration is done — ADR-051).
- **MR-14** (research_toolkit#14): cache_manifest path-resolution
  inconsistency — **MERGED 2026-05-24 (research_toolkit PR #15,
  squash 33f07f9)**. `make dossier-audit` PASSES again; cache_manifest
  migrated to portable relative paths (commit 5da5fd4).

All 7 eval-toolkit MRs (MR-1/2/4/5/6/7 + MR-10 obsoleted) + 2
book-scaffold-astro MRs (MR-8 + MR-9) + MR-3/-12/-13/-14 are CLOSED.
**Zero open upstream MRs from the M0 batch.** (R26 then dogfooded + adopted all three
newer versions and filed fresh consumer-friction findings **DF-1..4** — see
`decisions/upstream_issues.md`.)

---

## Lane 2 data path (MR-3 shipped 2026-05-24; readiness-GATED per ADR-051)

**DESIGNATED PRIMARY — execution GATED** (R26 dogfooding, ADR-051): `/dataset-synthesize`
(research_toolkit v2.4.0) is the designated path to generate the ~10k synthetic
indirect-injection corpus, **but do NOT rely on it until research_toolkit #22/#23 close**.
#22 is a confirmed **silent-failure** path (`_extract_text` drops non-text blocks, returns
"") that would silently corrupt the corpus; #23 = not-installed-by-default. See
`decisions/upstream_issues.md` (DF findings + Lane 2 gate). When unblocked: recipe at
`~/Claude/research_toolkit/templates/dataset_synthesis_recipe.template.yml`; cost-bounded
via `--bail-at-cost 80.00` (per plan §16 + ADR-013); exit code 3 on API failure with
resumable partial manifest. Seed templates from the 7 `production_rag_incidents` carriers
(EchoLeak / Slack AI / Comet / Gemini / ChatGPT-plugin image / Unseeable / Greshake Bing).

**Fallback ladder (only if `/dataset-synthesize` proves insufficient
at M2)** — kept for reference, no longer the expected path:

1. `harelix2024_mixed` (HuggingFace) IF `/freshness-audit` resolved
   the HF 401 with an auth token. Unknown size + license.
2. `lakeraai2025pintbenchmark` (public GitHub; accessible now).
   Distribution differs from the synthetic-corpus goal.
3. Hand-author ~50-100 positives per `production_rag_incidents`
   carrier. Smaller but production-realistic.

Cross-references: ADR-026 (no-local-workarounds — the upstream skill
shipping IS the library-first resolution); ADR-041 (ETHICS —
full-specificity disclosure norm for synthetic attack carriers);
synthesis doc Lane 2 risk discussion at
`docs/planning/dossier_implications_for_roadmap.md` Zone 2.

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
