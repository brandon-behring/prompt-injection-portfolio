---
adr_id: "023"
slug: build-in-public-continuous-weekly-cadence
title: "Build-in-public: continuous weekly cadence (Twitter + Mastodon + monthly LessWrong/LinkedIn)"
date: 2026-05-19
status: Accepted
linked_round: "R3"
plan_section: "§8.2"
---

# ADR-023: Build-in-public continuous weekly cadence

## Status

Accepted; **loudness policy updated by Round 19 Q2** (quiet ship at
v0.8.0 / v0.9.0; big-announcement only at M0 + M7 + v1.0.0).

## Context

Portfolio is public from M0 ([ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md))
+ the work develops over 13-14 weeks then a 3-4 month community
feedback window. Without a cadence, the public surface goes silent
between milestones — visitors arrive at a stale-looking repo.

Build-in-public discipline serves three audiences:

- **Recruiters + curious engineers** (narrative-guide audience per Round
  17): weekly threads provide low-investment progress signal.
- **Researchers** (academic-guide audience): monthly deep-dives surface
  methodology evolution.
- **Future-self**: archived posts trace the chronology of decisions —
  doubles as project journal.

## Decision

Build-in-public cadence:

1. **Weekly Twitter/X thread** (every Friday) — ~3-5 tweets summarizing
   the week's progress + 1 figure + link to relevant chapter/dossier.
2. **Weekly Mastodon cross-post** (`sigmoid.social` for ML reach).
3. **Archive to `docs/build-in-public/YYYY-WW-week-summary.md`** — every
   weekly post is committed; the archive is repo-citable.
4. **Monthly deep-dive** (first weekday of month) — 500-1500 word blog
   post; cross-post to LessWrong (ML-safety-relevant) or LinkedIn
   (hiring-audience-relevant); archive to
   `docs/build-in-public/YYYY-MM-month-deepdive.md`.
5. **Per-milestone announcement** (M0 + M5 + M7 + v1.0.0) — longer-form;
   all channels + HN if traction.

**Round 19 Q2 loudness policy** (post-Round-17 sequential rollout):
- M0 (v0.1.0), M7 (v0.7.0 textbook), v1.0.0 (3-guide complete) = LOUD
  (all channels + thread + cross-post).
- v0.8.0 (narrative ship), v0.9.0 (academic ship) = QUIET (CHANGELOG
  entry + model card updates; NO viral push). Reserve viral push for
  v1.0.0 final.
- Weekly + monthly cadence continues throughout but at "documentary"
  not "announcement" volume.

## Consequences

- **Time budget**: ~1-2h/week human-time; Claude drafts; Brandon edits +
  posts.
- **Per-milestone build-in-public skill** (Claude Code skill in
  `~/.claude/skills/`) generates first-draft thread from previous week's
  commit log + experiment record diffs.
- **Archive citability**: weekly post hashes pin to specific commits
  (per [ADR-011](ADR-011-commit-discipline.md) no-amend rule); readers
  can `git checkout` to inspect repo state at thread publication.
- **Round 19 Q3 model card link section**: model cards carry a 1-link
  (textbook-only at M7) → 2-link (+narrative at v0.8.0) → 3-link
  (+academic at v0.9.0) section.

## Cross-references

- Plan §8.2 (build-in-public cadence); Round 19 Q2 + Q3
- [ADR-024](ADR-024-public-from-m0-pre-alpha-banner.md) (public-from-M0)
- [ADR-044](ADR-044-three-guide-architecture-with-shared-substrate.md) (3-guide sequential rollout)
- `docs/build-in-public/_template_weekly.md` + `_template_milestone.md`
