---
adr_id: "048"
slug: cross-classification-policy
title: "Cross-classification policy — topic-prefixed bibkeys for multi-topic primary sources"
date: 2026-05-23
status: Accepted
linked_round: "R24"
plan_section: "Sprint 2 + M0 close"
---

# ADR-048: Cross-classification policy (topic-prefixed bibkeys)

## Status

Accepted (Round 24 lock; ratified Sprint 2 close convention used in
production across 5 topic dossiers).

## Context

Sprint 2 built five topic dossiers in parallel:
`detector-landscape/`, `direct-vs-indirect/`,
`training-and-evaluation/`, `agentic-security-architecture/`,
`rag-injection-defenses/`. Each topic has its own
`bib_ledger.yml` + `evidence_ledger.yml` + `cache_manifest.yml` +
`claim_graph.jsonl` + supporting artifacts validated by the v2.2+
strict-live validators in `research_toolkit/validators/`.

The validators enforce **per-file bibkey uniqueness** in
`bib_ledger.yml`. They do NOT enforce cross-file uniqueness across the
5 topics, because doing so would force a single primary source to be
arbitrarily assigned to exactly one topic — losing the topic-tailored
analytical lens.

Concrete example: **InjecGuard** (Li et al. 2024). Naturally belongs in:
- `detector-landscape/` (it's a guardrail-bench tool — relevant to
  detector cataloging + over-defense quantification)
- `training-and-evaluation/` (NotInject is a benchmark in its own right)
- `agentic-security-architecture/` (the over-defense constraint
  applies to score-fusion stackers)

Three options to handle this:

1. **One canonical home + cross-link**: pick one topic to host the
   entry, others link to that path. Pro: no duplication. Con:
   topic-tailored excerpts impossible; the "canonical home" decision
   is fragile across edits; a single bib_ledger doesn't carry the
   topic-specific evidence_ledger excerpt that the topic's claim
   graph builds on.
2. **Topic-prefix-with-fanout**: each topic gets its own entry with
   topic-tailored excerpts; bibkey is uniquely prefixed by topic.
   Pro: per-topic excerpts work; validators stay simple. Con: same
   primary source appears N times (one per relevant topic).
3. **Cross-topic uniqueness validator + symlink-of-yaml-fragments**:
   technically possible. Pro: no duplication of metadata. Con:
   significant validator complexity for marginal gain.

Sprint 2 used Option 2 in production — 28 cross-classified entries
shipped this way (e.g., `agentic_li2024injecguard` in
`agentic-security-architecture/` alongside `li2024injecguard` in
`detector-landscape/` + `training-and-evaluation/`).

## Decision

When a primary source belongs to more than one topic dossier, each
topic gets its **own bib_ledger entry** with a **topic-prefixed
bibkey**. The prefix is the topic-area short label:

| Topic dossier | Prefix |
|---|---|
| `detector-landscape/` | (no prefix; canonical naming) |
| `direct-vs-indirect/` | (no prefix; canonical naming) |
| `training-and-evaluation/` | (no prefix; canonical naming) |
| `agentic-security-architecture/` | `agentic_` |
| `rag-injection-defenses/` | `rag_` |

The first topic alphabetically to onboard a primary source uses the
canonical bibkey (e.g., `li2024injecguard`). Subsequent topics that
also cite the same source use the topic-prefixed form
(`agentic_li2024injecguard`, `rag_li2024injecguard`).

Each cross-classified entry has:
- Same `primary_url`
- Same `verified_at` (if verified) — verification is shared across
  the family
- Same `cache_ids` (the cached blob is reused — cache_manifest entries
  may reference the same `cache_<sha16>` ID under each topic)
- **Different `claim_family`** — each topic assigns the source to the
  claim family most relevant to that topic's lens
- **Different evidence_ledger excerpts** — each excerpt is tailored to
  the topic's analytical frame (the byte-offset + sha256_of_span
  anchor may be different even when the same PDF is the source)

## Consequences

**Operational (cache + bibliography):**

- The 157-entry `book/bibliography.bib` deduplicates across topics
  using the canonical (non-prefixed) bibkey when present, falling back
  to the prefixed form when only prefixed entries exist. The
  `build-bib.mjs` script consumes all 5 topic bib_ledgers and
  enforces canonical-key resolution.
- `cache_manifest.yml` cache_ids are reusable across topic dossiers.
  A single cached PDF blob backs N entries (one per topic).
- The cache_manifest validator does NOT enforce 1:1 with bib_ledger;
  it enforces "every cache_id referenced in a bib_ledger
  cache_ids[] exists in cache_manifest entries[]." Cross-classified
  entries share cache_ids freely.

**Validation:**

- `cross_stage.py --strict` runs per-topic, does NOT do cross-topic
  uniqueness check. This is the correct behavior; cross-classification
  is supported by design.
- Future tooling MAY add an explicit `cross_classified_with: [topic, ...]`
  field on entries; deferred to a separate ADR if needed.

**ADR cross-references:**

- ADR cross-references that cite a prefixed bibkey explicitly note the
  prefix in prose (e.g., "agentic_li2024injecguard in the
  agentic-security-architecture topic"). See ADR-045 cross-references
  section for the operational pattern.
- The synthesis doc (`docs/planning/dossier_implications_for_roadmap.md`)
  uses canonical bibkeys when the analytical claim cuts across topics;
  uses prefixed bibkeys only when topic-specific excerpts are the
  citation target.

**Sprint 2 inventory (28 cross-classified entries):**

The 28 cross-classified entries are distributed roughly as:
- 16 entries in `agentic-security-architecture/` with `agentic_*`
  prefix
- 12 entries in `rag-injection-defenses/` with `rag_*` prefix
- The canonical entries live in `detector-landscape/` /
  `direct-vs-indirect/` / `training-and-evaluation/` (which use no
  prefix per the table above)

Exact count + roster: see `make dossier-audit` per-topic bib_ledger
summaries.

## Cross-references

- ADR-007 (claim_family naming convention; domain-prefixed lowercase
  per validator regex)
- ADR-011 (immutability discipline — once accepted, ADRs are not
  amended except for typo/link fixes)
- `research_toolkit/validators/bib_ledger.py` (per-file bibkey
  uniqueness enforcement)
- `research_toolkit/validators/cross_stage.py` (per-topic validation,
  not cross-topic)
- Sprint 2 dossier topic READMEs (5 files)
- ADR-049 (Round 24, body-quote anchoring discipline — companion
  policy on excerpt anchoring)
- ADR-050 (Round 24, vendor cluster posture — applies cross-
  classification to commercial detector vendors)
