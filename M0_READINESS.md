# M0 Close Readiness — handoff for user-led v0.1.0 ratify

**Scope**: `make ratify-milestone` gate state + user-led TODO checklist
for the formal M0 close (`v0.1.0` tag + announcement). Complements
[`NEXT_SESSION.md`](NEXT_SESSION.md) (cold-start anchor) +
[`docs/planning/README.md`](docs/planning/README.md) (planning artifacts
index).

**Generated**: 2026-05-22 (Round 22 autonomous /loop close; refreshed
Round 23 cross-machine handoff).
**Current tag**: `v0.1.0-pre` (Day 3b checkpoint).
**Pending tag**: `v0.1.0` (M0 close; user-led).

This document captures the state at autonomous-/loop close + the user-led
items that remain before `git tag v0.1.0` + `gh release create v0.1.0`.

## Autonomous /loop completed (Round 22 Days 5/14/15/16/17/18 + CI ref bump)

10 commits since Day 3b's `v0.1.0-pre`:

```
3fb9338  Round 22 mini — submission CI ref v1.2.16 → v1.3.0
7429e33  M0 Day 16 — Dockerfile + compose.yaml + verify_docker.py extension
c30a40e  M0 Day 5 — 6-lane experiment-record skeletons + MANIFEST.json
dcf037a  M0 Day 14 — 13 textbook chapter skeletons + 6 fragment lane dirs
04922fe  M0 Day 15 — governance files + 3-guide README + frontmatter
add5efc  M0 Day 17 — 11 substantive ADRs + decisions/README.md
6a59b40  M0 Day 18 — build-in-public templates (Round 19 loudness policy)
[this commit + push pending]
```

## M0 ratify-milestone checklist

Run `make ratify-milestone` from the portfolio repo root. Expected output:
all 12+ gates pass. Gates covered by the Makefile:

- ✓ `verify-data-sources` (6 OOD sources reachable + SHA-pinned)
- ✓ `verify-docker` (Docker daemon + alpine + portfolio compose config)
- ✓ `verify-deps` (sibling submission editable-dep)
- ✓ `lint` = ruff check + ruff format --check + mypy --strict
- ✓ `test` = pytest -m "not integration"
- ✓ `contracts` = pytest -m contract (13 contract tests)
- ✓ Files-present check (12 root + dirs)

Plus M0 ratification checklist from plan §21 Day 19 (covered by the above):

- [x] All 7 test-contracts pass
- [x] mypy --strict clean on src/ + scripts/ + tests/
- [x] ruff check + format clean
- [x] pytest "not integration" green
- [x] Pre-alpha banner present (README + book frontmatter pre-alpha-banner.mdx)
- [x] ETHICS.md + SECURITY.md + CODE_OF_CONDUCT.md present
- [x] 13 textbook chapter skeletons (book/src/content/textbook/)
- [x] 6 lane experiment-record skeletons (experiments/lane-{1,1b,2,3,4,5}/)
- [x] experiments/MANIFEST.json populated (6 lanes registered)
- [x] decisions/library_imports.md populated (14 v0.47 primitives + scaffold backfill)
- [x] decisions/upstream_issues.md state machine current (8/9 closed; MR-12 added)
- [x] pyproject.toml pins eval-toolkit[probes,losses]>=1.0 (R26; was >=0.47) + runpod-deploy>=0.8.4; research_toolkit dropped as a dep → repo-local tooling clone (ADR-051)
- [x] book/package.json pins @brandon_m_behring/book-scaffold-astro: ^4.4.0 (R26; was ^3.5.0→^3.6.5)
- [x] CI two-step submission ref: v1.3.0
- [x] Dockerfile + compose.yaml + verify-docker green
- [x] gh repo view returns 200 (public from M0; ADR-024)
- [x] First green CI push (commit 0a4938a Day 3b)
- [x] 11 substantive ADRs at decisions/ (ADR-035-038, 041-047) +
      decisions/README.md index with skeleton placeholders for ~25 more
- [x] build-in-public templates at docs/build-in-public/

## User-led items remaining (deferred per Round 22 Q2 + Q4)

These need user presence + cannot be automated by /loop:

### Dossier sprint (Days 6-12)
- **Scope**: ~60-80 files at `docs/research/` via research_toolkit's
  `/research-plan` + `/research-gather` + `/dossier-build` + `/dossier-audit`
  skills (not in autonomous /loop's skill set).
- **Input**: 3 compass artifacts now in-repo at
  [`docs/research/compass-survey/`](docs/research/compass-survey/)
  per Round 23 Q1 (~1055 lines total; renamed from `~/Downloads/compass_artifact_wf-*.md`
  for clarity). See [`docs/research/compass-survey/README.md`](docs/research/compass-survey/README.md)
  for the dossier-sprint workflow + provenance/license notes.
- **Output**: dossier with `claim_family` keys cross-referenced by ADRs
  + chapter citations.

### Build-in-public account creation (Day 18 final step)
- **Twitter/X**: create `@brandonmbehring` or similar; profile bio with
  portfolio URL + book URL
- **Mastodon**: create account at `sigmoid.social` (ML research community)
- **M0 announcement post**: draft using `docs/build-in-public/_template_milestone.md`;
  post to all loud channels per ADR-023 + Round 19 follow-up Q2

### Formal M0 close (Day 19)
- Run `make ratify-milestone` — confirm all gates pass
- `git tag v0.1.0` (annotated tag with M0 release notes)
- `git push origin v0.1.0`
- `gh release create v0.1.0` with M0 announcement notes (link to
  `docs/build-in-public/2026-WW-week01-announcement.md` once posted)
- Update `portfolio_plan_approved.md` memory + `MEMORY.md` description suffix

## Outstanding upstream MRs (per decisions/upstream_issues.md)

- **MR-3** (research_toolkit#1): `/dataset-synthesize` skill —
  M3-blocking; portfolio monitors at Day 13-style intervals
- **MR-12** (eval-toolkit#69): Tier-2 Protocol consolidation —
  NOT blocking; targets eval-toolkit v0.48+

All eval-toolkit (7 MRs) + book-scaffold-astro (2 MRs) MRs are closed
upstream per Round 14-21 cascade.

## Plan + memory pointers

- **Plan** (in-repo per Round 23 Q1):
  [`docs/planning/PORTFOLIO_PLAN.md`](docs/planning/PORTFOLIO_PLAN.md)
- **Planning companion docs**: [`docs/planning/`](docs/planning/) — chapter
  outlines + experiment-record template + lane playbooks + eval-toolkit
  roadmap
- **Compass research surveys**:
  [`docs/research/compass-survey/`](docs/research/compass-survey/) — 3 files
  (detector landscape + direct-vs-indirect deep-dive + training+eval
  methodology)
- **Memory index** (NOT in repo; on user's `~/.claude/`):
  `~/.claude/projects/.../memory/MEMORY.md`
- **Key memories**: `portfolio_plan_approved` (in-place updated through
  Round 23) + `library_first_is_project_wide_invariant` +
  `hierarchical_depth_derivation_rule` +
  `snap-gh-needs-repo-path-for-body-file` +
  `exploring-options-over-handoff-doc-preferred`

---

## v0.1.0 close — staged artifacts (2026-06-01; HELD for accounts)

Per the Round-30 session: `make ratify-milestone` is **GREEN** on HEAD `0dd0aa4` (9/9 stages). The close
is **staged but HELD** until the build-in-public accounts (Twitter/X + Mastodon) exist, so the close +
announcement land together (user's call). The held bundle is a ~15-min **user-led** runbook:

1. ✅ **DONE (2026-06-01 PM)** — merged via **PR #4** (fast-forward; `origin/main` = `116cfd5`; 42
   commits, linear, same SHAs). Remaining held steps (2–6) are tag → release → announce.
2. `git checkout main && git pull` → re-run `make ratify-milestone` on `main` (confirm still green).
3. `git tag -a v0.1.0 -m "<message below>"` → `git push origin v0.1.0`.
4. `gh release create v0.1.0 --notes-file docs/build-in-public/2026-06-01-v0.1.0-announcement.md`.
5. Post the announcement thread (accounts) → `gh release edit v0.1.0` to link it.
6. Update `MEMORY.md` + the `portfolio_plan_approved` memory ("v0.1.0 tagged <date>").

### Annotated tag message (for `git tag -a v0.1.0 -m "..."` on `main`)

```
M0 close (v0.1.0): public pre-alpha portfolio + first result (capacity-dependent OOD wall)

Snapshots the M0 framework + M1's first finding + the Round-30 re-laddered roadmap:
- Public repo, pre-alpha banner (through v0.7.0); 13-chapter textbook skeleton; 6-lane
  experiment-record framework; 210-entry research dossier (5 topics, 97% verified); Docker
  repro; ETHICS/SECURITY/CODE_OF_CONDUCT; 55 ADRs.
- M1 (attack-type-LODO): pre-registered §6.5 OOD-wall prediction FALSIFIED at the LoRA ceiling —
  the per-attack-type wall is capacity-dependent (tfidf +0.135 / frozen +0.082 SURVIVE; lora -0.003).
- Round-30 re-ladder (ADR-055): multi-axis capacity-dependent spine; Lane 2 re-pointed to the
  carrier axis; a carrier-LODO M2 pre-flight gate scheduled.

Pre-alpha: experiments in flight; chapter prose fills as lanes close.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body (`session/2026-05-26-adoption-and-research-ops` → `main`; ~40+ commits)

**Title:** Merge the adoption/research-ops + M1 + Round-30 re-ladder arc into `main` (v0.1.0 snapshot)

**Body:**
> This branch carries the full arc since `main` last advanced (~40 commits; `main` is a strict ancestor →
> clean fast-forward). It is the snapshot the `v0.1.0` M0-close tag is cut from.
>
> **What landed:** the M0 technical close (CI-green framework, dossier, governance, ADRs, Docker); the
> pre-modeling EDA arc + the context-engineering subagent suite; **M1 (attack-type-LODO)** with the
> pre-registered §6.5 OOD-wall prediction **FALSIFIED at the LoRA ceiling** (capacity-dependent —
> tfidf/frozen SURVIVE, lora FALSIFIED); and the **Round-30 re-ladder** (ADR-055: multi-axis spine, Lane 2
> → carrier axis, a carrier-LODO M2 pre-flight gate).
>
> **Gate:** `make ratify-milestone` GREEN on HEAD. **Cost:** $0.83 realized (« the $250 base).
>
> Merge as fast-forward to keep `main` linear; tag `v0.1.0` on `main` immediately after.

