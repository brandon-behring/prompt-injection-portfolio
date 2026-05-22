---
template: monthly
month: YYYY-MM
date_posted: TBD
channels: ["lesswrong-or-linkedin", "twitter-x-promo"]
linked_chapter: TBD
linked_adrs: []
---

# YYYY-MM Deep Dive — [headline]

## Audience choice (pick one per month)

- **LessWrong** (ML safety audience): emphasize methodology rigor +
  CI apparatus + Goodhart-discipline + the OOD wall framing.
- **LinkedIn** (hiring audience): emphasize the case-study positioning,
  collaboration with Claude, build-in-public discipline, the 3-guide
  architecture.

## Structure (500-1500 words)

### Hook (1 paragraph)
- What changed this month? Specific finding or methodology decision.

### Background (1-2 paragraphs)
- Cite the chapter or ADR that drives the finding.
- Connect to submission predecessor's evidence (ADR-075 OOD wall).

### What we did (2-3 paragraphs)
- Methodology / experiment / decision walk-through.
- 1 figure if available (predictions parquet derived; cross-ref the
  chapter for full detail).

### What we learned (1-2 paragraphs)
- 3-way outcome interpretation. Was the lane's H1 / H0 / H∅ realized?
- Reference any contingency-unlock decision (per ADR-013 cost discipline).

### What's next (1 paragraph)
- Forward-look to next milestone. Link to relevant chapter + lane
  experiment record.

### Cross-references
- Chapter: `book/src/content/textbook/chXX-...mdx`
- Experiment record: `experiments/lane-N/results.md`
- ADRs: ADR-NNN

## Promo thread (3 tweets)

After publishing the monthly post, promote on Twitter/X with a 3-tweet
thread linking back to the full post.

## Cross-references

- Plan §8.2
- ADR-023 (build-in-public cadence)
