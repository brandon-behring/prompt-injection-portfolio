---
adr_id: "049"
slug: body-quote-anchoring-discipline
title: "Body-quote anchoring discipline — when to extract from PDF body vs cache abstract-level HTML"
date: 2026-05-23
status: Accepted
linked_round: "R24"
plan_section: "Sprint 2 + M0 close"
---

# ADR-049: Body-quote anchoring discipline

## Status

Accepted (Round 24 lock; ratifies Sprint 2's anchoring methodology used
across ~17 OOD-wall thesis carriers).

## Context

The research_toolkit v2.2+ strict-live evidence_ledger schema supports
**body-quote anchored** excerpts: a verbatim substring of the
underlying primary source (PDF, HTML page, etc.) plus a precise
location anchor enabling future readers (human or LLM) to re-locate
the exact span.

The anchor structure is:

```yaml
span:
  text_path_offset: <byte offset into the extracted text>
  sha256_of_span: <hex hash of the verbatim substring>
  excerpt: "verbatim text..."
```

For PDFs, the body-text extraction uses `pdftotext` (poppler 26.03.0).
For HTML pages, an HTML-to-text equivalent is acceptable, though
HTML-based pages often have stable abstract-level content in
`<meta name="description">` or the lead paragraph that suffices
without body-quote work.

Sprint 2 surfaced a practical question: when should an entry's
evidence_ledger excerpt be **body-quote anchored** vs stay at
**abstract-level** (cached HTML extraction from the landing page)?

Concrete: a paper's HTML landing page typically yields the abstract
plus byline + venue metadata. That's a high-confidence cached
extraction usable for status verification. But the OOD-wall thesis +
methodology critique claims (per Ch 5 + Ch 7 + Ch 9 + Ch 11 +
Ch 12 + Ch 13) need verbatim quote-anchoring to the **body** of the
paper — the specific paragraphs documenting hypotheses, methods,
results, limitations.

Abstract-level extraction does not carry that resolution. Body-quote
extraction does, at the cost of:
- PDF download (cache impact — public-repo licensing forbids
  re-distributing closed-access PDFs; vendor blogs OK)
- pdftotext extraction step (~250 ms per PDF)
- byte-offset computation + sha256 of span
- excerpt curation by the researcher (selecting the right paragraph)

## Decision

**Body-quote anchoring is required for OOD-wall thesis carriers; not
required for general supporting citations.**

A carrier qualifies for body-quote anchoring if it satisfies ≥2 of:

1. **Methodology critique target**: the entry's claim is a critique of
   an experimental method, eval design, or interpretation that
   requires citing the paper's specific protocol description (not
   just its conclusion).
2. **Multi-paper convergence anchor**: the entry is part of a
   multi-paper claim convergence (e.g., 9-paper composition_audit;
   3-paper TPR@LowFPR convergence) where reproducibility of the
   convergent observation demands paragraph-level evidence.
3. **OOD-wall thesis carrier**: directly load-bearing for the book's
   OOD-evaluation-wall thesis chapters (Ch 5, 7, 9, 11, 12, 13). The
   thesis argument needs paragraph-precision quotes to survive future
   adversarial reading.
4. **Vendor-blog claim**: a vendor product claim that materially
   affects threat-model framing or detector landscape (e.g., a vendor
   reports a specific false-positive rate that influences ADR-036
   reporting policy). Note: vendor blogs may not always have stable
   long-form PDF artifacts — body-anchor where available, abstract
   anchor where not.

A carrier does NOT need body-quote anchoring if:

- The claim is purely a citation of existence (e.g., "such-and-such
  benchmark exists in HuggingFace at URL X") — primary_url + cached
  HTML suffices.
- The entry is a survey paper cited only for its taxonomy framing
  (the taxonomy can be extracted from the abstract).
- The entry is a vendor product page used solely to establish that
  the vendor offers a product in this space (per ADR-050 vendor
  cluster posture).

**Storage discipline:**

- Body-anchored entries store `text_path_offset` + `sha256_of_span` +
  `excerpt` in evidence_ledger.
- Cached body-text files (the full pdftotext output) live under
  `docs/research/<topic>/cache/body_text/<bibkey>.txt`. **These are
  gitignored** per the cache-stays-local policy.
- Cached metadata (the pdftotext extraction date + tool version +
  page count) lives under
  `docs/research/<topic>/cache/body_meta/<bibkey>.json` (also
  gitignored).
- The `cache_manifest.yml` references the originating cached PDF blob
  by sha256 (the canonical research_cache primary record); the
  body_text + body_meta directories are derived artifacts.

## Consequences

**Sprint 2 inventory:**

~17 body-anchored entries shipped Sprint 2 across:
- detector-landscape: ~5 (e.g., bhagwatkar2025firewalls,
  hackett2025bypassing, jacob2025promptshield)
- training-and-evaluation: ~6 (the composition_audit 9-paper family,
  saxe2024causal, fomin2026benchmarkslie)
- rag-injection-defenses: ~3 (production_rag_incidents EchoLeak +
  Comet + greshake2023bingadvisory)
- agentic-security-architecture: ~3 (debenedetti2024agentdojo,
  zhan2024injecagent, agentic_li2024injecguard)

The remaining ~193 entries (of 210 total) use abstract-level cached
HTML extraction. This is sufficient for status verification + thesis
framing + general literature anchoring; it would be over-engineering
to body-anchor all 210 entries.

**Forward-look:**

Future deepening per-carrier as M1+ chapter authoring exercises
specific paragraphs. The `/freshness-audit` pass may re-survey
high-priority carriers for body-quote anchoring when book chapters
cite them in detail.

The `cache/body_text/` + `cache/body_meta/` directories are stable
filesystem conventions; the validator does not currently enforce
their existence, but future tooling MAY add a check that
body-anchored entries have a corresponding `body_text/<bibkey>.txt`
file on disk.

**Public-repo licensing compatibility:**

Body-quote anchoring is compatible with public-repo licensing because:
- The verbatim excerpt itself is fair-use (short paragraph from a
  scholarly work).
- The cached PDF blob stays local (gitignored per `docs/research/*/papers/`
  in `.gitignore`).
- The byte-offset + sha256 anchor is reproducible: any reader with
  access to the primary PDF (e.g., via the source URL) can verify the
  excerpt was not fabricated.

**Tooling compatibility:**

- `pdftotext` (poppler 26.03.0) is the canonical extraction tool. The
  byte offset is into the **plain-text extraction**, not the PDF
  binary. Re-extraction with a different poppler version may shift
  offsets; sha256_of_span guards against this by hashing the
  substring itself.
- HTML-to-text equivalents (e.g., `lynx -dump`) are acceptable for
  HTML primary sources but rarely required (abstract-level
  extraction usually suffices).

## Cross-references

- ADR-007 (claim_family + evidence_ledger schema)
- ADR-010 (anti-pattern firewall — no URL guessing; URLs in
  evidence_ledger entries are verified, not synthesized)
- ADR-041 (ETHICS — fair-use excerpts; full-specificity disclosure)
- ADR-048 (Round 24, cross-classification policy — companion ADR)
- ADR-050 (Round 24, vendor cluster posture — vendor blog entries
  often use abstract-level anchoring, not body-quote)
- `research_toolkit/validators/evidence_ledger.py` (span schema
  enforcement)
- `.gitignore` line 53-54 (`docs/research/*/papers/` cache exclusion)
- Sprint 2 dossier topic READMEs (5 files document body-anchored
  rosters per topic)
