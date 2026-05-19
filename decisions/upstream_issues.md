# Upstream issues — state machine

Tracks all upstream issues filed against the 4 load-bearing libraries
(`eval-toolkit`, `runpod-deploy`, `research_toolkit`,
`@brandon_m_behring/book-scaffold-astro`).

Per Round 10 library-first invariant: **no local workarounds.** Missing
primitives become upstream issues + MRs; portfolio's `pyproject.toml`
(or `book/package.json`) pins the new version once released, then the
dependent lane proceeds. The standing GH-issue-filing permission lets
portfolio file issues during execution (not only the M0 batch) when
friction is encountered.

## State machine (per row)

```
issue-filed → pr-opened → pr-merged → released-vX.Y.Z → pinned-in-portfolio
```

`needs-redesign` is a side state when an issue is open but needs more
upstream discussion before a PR can be opened.

---

## M0 batch — filed 2026-05-19 (week 1 of M0)

Per plan §10 (Library-first audit). Effort estimates per plan; sequencing
checks (which M-milestone blocks on which MR) per the same.

| # | Repo | Issue | Primitive | Blocks | State | Notes |
|---|------|-------|-----------|--------|-------|-------|
| MR-1 | brandon-behring/eval-toolkit | [#48](https://github.com/brandon-behring/eval-toolkit/issues/48) | `loaders.ood_dataset_from_manifest(yaml_path)` | M1 Lane 1 (~Day 4-5 M0) | issue-filed | ~1d impl |
| MR-2 | brandon-behring/eval-toolkit | [#49](https://github.com/brandon-behring/eval-toolkit/issues/49) | `adversarial.character_injection` (12-technique suite + Scorer-Protocol wrapper) | M1 Lane 1b (~Day 6-8 M0) | issue-filed | ~2-3d impl |
| MR-3 | brandon-behring/research_toolkit | [#1](https://github.com/brandon-behring/research_toolkit/issues/1) | `/dataset-synthesize` skill (prompt-caching template) | M3 Lane 2 data (~week 7) | issue-filed | ~1d impl |
| MR-4 | brandon-behring/eval-toolkit | [#50](https://github.com/brandon-behring/eval-toolkit/issues/50) | `losses.RecallAtLowFPR` (Meta PG2 recipe) | M4 Lane 2 train (~week 8) | issue-filed | ~1d impl |
| MR-5 | brandon-behring/eval-toolkit | [#51](https://github.com/brandon-behring/eval-toolkit/issues/51) | `preprocessing.spotlighting` (delimit + datamark + encode variants) | M5 Lane 3 (~week 10) | issue-filed | ~0.5d impl |
| MR-6 | brandon-behring/eval-toolkit | [#52](https://github.com/brandon-behring/eval-toolkit/issues/52) | `stacking.MetaLearner` Protocol + `LogisticStacker` reference impl | M6 Lane 4 (~week 11) | issue-filed | ~0.5d impl |
| MR-7 | brandon-behring/eval-toolkit | [#53](https://github.com/brandon-behring/eval-toolkit/issues/53) | `probes.ActivationDeltaProbe` (TaskTracker-style linear probe) | M2 Lane 5 (~week 4-5) | issue-filed | ~1-2d impl |
| MR-8 | brandon-behring/book-scaffold-astro | [#6](https://github.com/brandon-behring/book-scaffold-astro/issues/6) | v3.2 `research-portfolio` profile (union academic ∪ tools schema + 3 new components + recipe + template) | **M1 book authoring** (chapter skeletons, Day 14 M0; blocks chapter prose, not M0 dossier/ETHICS/repo/MR-1/2/7/governance/Docker/ADRs which proceed in parallel) | issue-filed | ~3-5d impl |
| MR-9 | brandon-behring/book-scaffold-astro | [#7](https://github.com/brandon-behring/book-scaffold-astro/issues/7) | Generic frontmatter collection + dynamic route helper (for v3.3+) | NOT blocking M0 (portfolio uses local impl as prototype) | issue-filed | ~2-3d impl, defer to v3.3+ |

---

## Filed during execution

Per Round 10 ongoing-issue-filing discipline (user grant 2026-05-19):
when friction is encountered during execution (e.g., upstream primitive
doesn't compose ergonomically, scaffold callout missing for a chapter,
runpod-deploy validate flag missing), capture friction here + open the
issue + reference its `#N` here + continue execution.

Workflow:
1. Encounter friction
2. Add row below under "Filed during execution"
3. `gh issue create --repo brandon-behring/<lib> --label enhancement`
4. Reference issue number in the row
5. Continue execution — don't block unless friction has no clean
   compose-around using existing primitives. If genuinely blocking,
   escalate to "lane blocked until upstream ships" per
   no-local-workarounds rule.

| # | Repo | Issue | Friction | Workaround taken | State |
|---|------|-------|----------|------------------|-------|
| (none yet) |  |  |  |  |  |

---

## Library-first invariant — restatement

- 4 load-bearing libraries are infrastructure for multiple consumers; portfolio
  is one consumer.
- Reusable primitives belong upstream, never hand-rolled in portfolio.
- Project-specific glue (lane orchestration scripts, data loaders composing
  eval-toolkit primitives, project-named CLI wrappers) is allowed in portfolio's
  `src/`.
- Missing upstream primitive + no clean compose-around → lane is blocked
  until upstream ships. No `# TODO(upstream #N)` markers; no transition
  commits with both paths live.

See also: `library_imports.md` (registry of primitives consumed by portfolio).
