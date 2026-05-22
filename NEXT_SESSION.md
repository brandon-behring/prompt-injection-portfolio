# NEXT_SESSION

**Last update**: 2026-05-22 (M0 Day 3a complete; Day 3b + Day 4 ahead)
**Repo state**: v0.1.0-pre; 7 commits on main; 6/9 upstream MRs CLOSED; v0.47/v3.5/v1.2.16 pinned
**Pre-alpha banner**: ACTIVE (visible in README + book frontmatter)
**Plan file**: `/home/brandon_behring/.claude/plans/i-want-to-consider-merry-milner.md` (ratified 2026-05-21; 8 /exploring-options rounds 14-21 folded in)

---

## M0 progress summary (Day 1 → Day 3a complete)

```
9b07cdf  Day 1 — seed (README + LICENSE + ETHICS.md + verify scripts)
4676cc7  Day 1 — NEXT_SESSION.md
f011726  Day 2 — book/ scaffold + pyproject + verify_editable_dep
11175db  Day 2 — CI workflow draft (two-step checkout)
e6a2234  Day 2.5 — file 9 upstream MR issues (Round 10 ongoing-issue-filing)
bc30c52  Day 3a/c1 — pin bumps (eval-toolkit v0.47 + scaffold v3.5 + submission v1.2.16)
cbf7d25  Day 3a/c2 — library_imports + upstream_issues state machine + MR-12 file
```

**Upstream-MR closures via Round 20/21 cascade** (eval-toolkit + book-scaffold-astro
parallel-Codex agents shipped overnight 2026-05-19 → 2026-05-22):
- ~~MR-1~~ → eval-toolkit v0.43.0 (#48)
- ~~MR-2~~ → eval-toolkit v0.43.0 (core-6) + v0.47.0 (advanced-6) (#49) — 12-tech ALL_TECHNIQUES
- MR-3 → research_toolkit #1 **STILL OPEN**; M3-blocking
- ~~MR-4~~ → eval-toolkit v0.44.0 (#50)
- ~~MR-5~~ → eval-toolkit v0.44.0 (#51)
- ~~MR-6~~ → eval-toolkit v0.45.0 (#52)
- ~~MR-7~~ → eval-toolkit v0.43.0 (#53)
- ~~MR-8~~ → book-scaffold-astro v3.5.0 (#6) — UNBLOCKS Day 14 book authoring
- ~~MR-9~~ → book-scaffold-astro v3.3+ (#7)
- ~~MR-10~~ → OBSOLETED before filing (advanced-6 shipped via MR-2 v0.47.0 consolidation)
- **MR-12** → eval-toolkit #69 filed 2026-05-21 (Tier-2 Protocol consolidation;
  Day 3a smoke-test discovered ProtocolImportError; canonical top-level imports
  work per ADR 0002)

**Only 1 upstream MR remaining**: MR-3 (research_toolkit #1 /dataset-synthesize).
M3-blocking. Re-check at Day 13 + escalate if M2/M3 approaches without ship.

---

## Day 3b next (~4-6h)

**7 test-contracts implementation** (`tests/contracts/test_*.py`):
1. `no_handrolled_metrics` — verify portfolio doesn't reimplement eval_toolkit metrics
2. `predictions_persisted` — every lane writes predictions parquet
3. `leakage_scan_present` — eval slates not in training pool
4. `glossary_complete` — every project-specific term in `docs/glossary.md`
5. `library_imports_registered` — parse `decisions/library_imports.md`; verify every `from eval_toolkit / runpod_deploy / research_toolkit` import in `src/` or `scripts/` appears in registry
6. `mypy_strict_clean` — mypy --strict passes (no `Any` propagation)
7. `experiment_records_complete` — every lane has 4-file expt-record (hypothesis/protocol/results/decisions) + 3 fragment files (methodology/results/interpretation.mdx) per Round 17 follow-up Q2

**Tighten gates**: remove `2>&1 || echo "..."` allow-failure shells from
`.github/workflows/ci.yml`. mypy + pytest + contracts become hard gates.

**Commit**: `feat: M0 Day 3b — 7 test-contracts active (hard gates)`. Push →
CI fully-green → **tag `v0.1.0-pre` checkpoint**.

---

## Day 4 next (~0.5h, simplified from original 1.5h per Round 20)

Originally Round 14 Day 4 was "file MR-10 + open-MR monitoring". Round 20
OBSOLETED MR-10 filing (advanced-6 shipped in v0.47.0). Day 4 simplifies to:

1. **Empirical verify v0.47.0 advanced-6**: Python REPL — already done at
   Day 3a step 4 (12 dataclasses + `ALL_TECHNIQUES` 12-tuple confirmed).
2. **Open-MR monitoring** (~15 min): MR-3 (research_toolkit #1) status check.
3. **Commit**: `chore: M0 Day 4 — Round 20 reconciliation (MR-6 + MR-10 obsoleted upstream)`.

---

## Day 5+ buffer + Days 6-19

Per plan §21 with Round 14 + Round 17 + Round 20 + Round 21 timeline updates:

- **Day 5** — freed buffer; use to start Day 6 dossier sprint early OR draft
  Lane 1/1b/5 experiment-record skeletons ahead of Day 14 chapter skeletons.
- **Days 6-12** — Dossier sprint (~60-80 files via research_toolkit pipeline).
- **Day 13** — Open-MR monitoring (MR-3 watch) + ADR-036/037/038 drafts if
  Day 17 looks tight + experiment-record skeletons.
- **Day 14** — Textbook chapter skeletons Part III + IV (Ch 7-13) — **UNBLOCKED**
  per Round 21 (scaffold v3.5.0 + research-portfolio preset shipped).
- **Day 15** — Frontmatter (4 files; exec-summary REMOVED per Round 17 follow-up
  Q2 — content in README instead) + governance (SECURITY + CODE_OF_CONDUCT +
  issue/PR templates) + README polish (3 peer-level guide entry-points per Q3).
- **Day 16** — Docker T2 setup.
- **Day 17** — ADR-001..046 batch (~30-35 ADRs).
- **Day 18** — Twitter/X + Mastodon account setup + M0 announcement draft.
- **Day 19** — M0 close: `make ratify-milestone M=M0` + `git tag v0.1.0` +
  `gh release create v0.1.0` + announcement thread.

---

## Critical context (load-bearing for next session)

### v0.47 canonical API surfaces (Round 20)
- `from eval_toolkit import scorecard, sweep, metric_specs` — primary
  surfaces for evaluation + sweep + metric specs
- `from eval_toolkit import TextTransform, Probe, MetricSpec, MetaLearner,
  Scorer, SliceAwareScorer` — Tier-2 Protocols (canonical top-level per
  ADR 0002; submodule paths fragmented per MR-12)
- `from eval_toolkit.adversarial import ALL_TECHNIQUES` + 12 dataclasses
  (core-6 + advanced-6 char-injection)
- `from eval_toolkit.preprocessing import DelimitVariant, DatamarkVariant,
  EncodeVariant` (Spotlighting 3 variants)
- `from eval_toolkit.losses import RecallAtLowFPR` (`[losses]` extra)
- `from eval_toolkit.probes import ActivationDeltaProbe` (`[probes]` extra)
- `from eval_toolkit.stacking import LogisticStacker`

**Do NOT use**: SimpleNamespace patterns (`character_injection.zero_width_space()`);
per-module Protocols (`CharacterInjectionStrategy`); module-level sweeps
(`adversarial.sweep`); top-level scalar metric imports (`from eval_toolkit
import pr_auc` — REMOVED in v0.47.0).

### 3-guide architecture (Round 17)
M7 v0.7.0 ships **Textbook only** (the current 13-chapter outline at
`book/src/content/textbook/`). Story arc ("Can we climb the wall?") ships
at v0.8.0 (~month 13). Academic IMRaD ships at v0.9.0 (~month 14). All 3
locked at v1.0.0 (~month 16-17).

**Shared substrate pattern**: each lane has fragments at `book/src/content/
fragments/lane-N/{methodology,results,interpretation}.mdx` (single source
of truth for experiment data + citations). Each guide's chapter MDX imports
+ sequences fragments with guide-specific framing prose. `experiment_records_
complete` contract enforces fragments at lane close.

### Round 17 follow-up Q3 (cross-chapter narrative)
**Heavy threading** for the narrative guide (each chapter opens with story
recap + closes with hook to next). Light threading for textbook (each
chapter self-contained); academic-IMRaD is journal-paper structure.

### Submission CI ref policy (Round 14 Q1 + dynamic-detection)
Currently pinned at `v1.2.16` (Round 21 update). Re-detect via
`git -C ../prompt-injection-detection-submission ls-remote --tags origin |
grep -E 'refs/tags/v1\.[0-9]+\.[0-9]+$' | sort -V | tail -1` on each Day 3a-style
re-sync. Submission's `CLAUDE.md` previews v1.3.0 with ADR-078/079
(two-guide reader architecture) — validates portfolio's Round 17 3-guide
direction.

---

## Round 14-21 plan-update reference

All structural decisions for portfolio post-M0-Day-2.5 captured in plan file
under sections marked "Round NN update". Critical highlights:

- **Round 14** (CI ref + eval-toolkit floor + MR-10 file + Task #6 split)
- **Round 15** (Lane 2 LoRA-only; baseline expansion TF-IDF + open category)
- **Round 16** (cross-lane comparability; Lane 4 + Lane 5 train on Lane 2 corpus;
  Lane 5 timing shift M2 → M4)
- **Round 17** (3-guide architecture: textbook + narrative + academic IMRaD;
  shared-substrate fragments; sequential rollout v0.7.0 → v0.8.0 → v0.9.0 → v1.0.0)
- **Round 20** (eval-toolkit v0.47 pin + canonical-surface API pivot;
  MR-6 + MR-10 obsoleted)
- **Round 21** (book-scaffold-astro v3.5 pin + M1 book authoring unblock;
  MR-8 + MR-9 closed)

ADRs anticipated at Day 17 batch: ~35-37 (incl. ADR-041 ETHICS content lock,
ADR-042 Round 14 upstream-MR cascade, ADR-043 Lane 2 LoRA-only scope,
ADR-044 3-guide architecture, ADR-045 eval-toolkit v0.47 pivot, ADR-046
book-scaffold-astro v3.5 unblock).

---

## What NOT to do

- **Don't** advance submission CI ref past v1.2.16 without dynamic-detect
  re-verify (Round 14 round-3 Q2)
- **Don't** use eval-toolkit SimpleNamespace patterns or module-level sweep
  (Round 20 — removed in v0.47.0)
- **Don't** start narrative + academic chapter authoring before v0.7.0 M7
  textbook ratification (Round 17 Q3 sequential rollout)
- **Don't** retrain full-fine-tuning anywhere in portfolio (Round 15 Q1 LoRA-only)
- **Don't** train baselines on different corpora — all baselines + LoRA
  variants + Lane 4 stacker + Lane 5 probe share Lane 2's MR-3 corpus per
  Round 16 Q1
- **Don't** publish synthetic adversarial data without ETHICS.md cross-reference
  (Round 8 + ADR-022/041)
- **Don't** report AUPRC/AUROC on single-class slices (single-class metric
  convention upstream-enforced via eval-toolkit #39)
