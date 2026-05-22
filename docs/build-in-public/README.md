# Build-in-public archive

Per plan §8.2 (Round 3 Q4'' decision; ADR-023): portfolio develops
continuously in public via weekly Twitter/X threads + monthly Mastodon
cross-posts + per-milestone blog posts. Archive lives here for the
v1.0.0 citation surface.

## Cadence

- **Weekly** (every Friday during active development): 3-5 tweet
  thread on the week's progress + 1 figure + link to chapter/dossier.
  Cross-post to Mastodon (`sigmoid.social`). Archive at
  `YYYY-WW-week-summary.md`.
- **Monthly** (first weekday): 500-1500 word blog post on a recent
  badge-promoted finding. Cross-post to LessWrong (ML-safety) or
  LinkedIn (hiring-audience). Archive at `YYYY-MM-month-deepdive.md`.
- **Per-milestone**: M0 / M5 / M7 / v1.0.0 announcement threads on
  all channels (per Round 19 follow-up Q2: M0 + M5 + M7 + v1.0.0
  announced loudly; v0.8 + v0.9 ship quietly with CHANGELOG only).

## Templates

- `_template_weekly.md` — weekly thread skeleton
- `_template_monthly.md` — monthly deep-dive skeleton
- `_template_milestone.md` — milestone-announcement skeleton

## File naming

- Weekly: `2026-W21-week-summary.md` (ISO week number)
- Monthly: `2026-06-month-deepdive.md`
- Milestone: `2026-MM-DD-vX.Y.Z-announcement.md`

## Posting workflow

1. Draft in `_template_*.md` clone
2. Pre-vet for tone + factual accuracy
3. Post to channels (manual; user-led)
4. Save link metadata + post date in archive file frontmatter
5. Commit to repo

(Channel handles + posting are user-led; templates here are
draft-ready content only.)
