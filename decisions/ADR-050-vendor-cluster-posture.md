---
adr_id: "050"
slug: vendor-cluster-posture
title: "Vendor cluster posture — unverified-by-design for parked/acquired commercial detector vendors"
date: 2026-05-23
status: Accepted
linked_round: "R24"
plan_section: "Sprint 2 + M0 close"
---

# ADR-050: Vendor cluster posture

## Status

Accepted (Round 24 lock; formalizes the Sprint 2 → Sprint 3 fold-in
treatment of 6 commercial detector vendor entries in
`detector-landscape/bib_ledger.yml`).

## Context

Sprint 2's `detector-landscape/` dossier surfaced a "vendor cluster"
from `docs/research/_inbox/` compass artifact §6: six commercial
detector vendors that offer or claim to offer prompt-injection
detection products. These are NOT academic publications; they are
vendor product pages, often subject to:

- **Acquisition rerouting**: vendor sites redirect to acquirer (e.g.,
  Robust Intelligence acquired by Cisco; CalypsoAI acquired by F5).
- **Domain parking**: vendor sites parked at domain marketplaces
  (e.g., calypso.ai → domainnames.com listing; safeprompt.com → for
  sale on Spaceship.com).
- **Product surface migration**: features absorbed into a larger
  vendor offering (e.g., Robust Intelligence → Cisco Security Cloud).
- **GitHub org rename**: open-source projects may move org slugs
  (e.g., vijil-ai/dome → vijilAI/vijil-dome).

The six entries are:
- `hiddenlayer2025_cluster` (hiddenlayer.com) — verified Sprint 3
- `robustintelligence2025_cluster` (Cisco acquisition blog) — verified
  Sprint 3
- `vijildome2025_cluster` (vijilAI/vijil-dome) — verified Sprint 3
  (after URL correction)
- `guardrailsai2025_cluster` (guardrails-ai GitHub) — verified Sprint 3
- `calypsoai2025_cluster` — UNVERIFIED (domain parked at
  domainnames.com)
- `safeprompt2025_cluster` — UNVERIFIED (domain for sale at
  Spaceship.com)

After Sprint 3 verification work (M0 close Phase B), 4/6 entries were
promoted to `status: verified` against either the original vendor
URL (where live) or the acquirer's announcement blog (where the
original surface migrated). The remaining 2/6 remain unverified
because their primary surfaces are demonstrably not currently hosted.

The question this ADR settles: **is `status: unverified` a defect or a
deliberate posture for vendor entries whose primary surfaces have
parked or are for-sale?**

## Decision

**`status: unverified` IS a deliberate posture for vendor cluster
entries whose primary surface is parked, for-sale, or
acquisition-rerouted without a stable replacement.** These entries
are NOT defects; they are documented unverified-by-design with
explicit `verification_notes` documenting the exact failure mode.

A vendor cluster entry MAY remain `status: unverified` if it meets
ALL of:

1. **Primary surface is demonstrably not currently hosted** — the
   primary_url returns a parking page, a for-sale listing, or refuses
   connection (HTTP 000, NXDOMAIN, etc.). Documented in
   `verification_notes` with the specific failure (e.g., "calypso.ai
   redirects to domainnames.com domain-sale listing; F5 acquired
   CalypsoAI; product surface moved to f5.com/products/ai-guardrails
   per detector-landscape cross-link.").
2. **No stable acquirer or successor URL** is currently available. If
   an acquirer announcement is available, the entry should promote
   to `verified` against the acquirer's blog URL (per Sprint 3
   robustintelligence2025_cluster pattern with Cisco).
3. **The entry's analytical value is preserved by the unverified
   listing** — i.e., the vendor's name + product category + claimed
   capabilities (per the compass artifact's original §6 surfacing)
   are noted for future re-verification, even if no current URL
   anchors them.

For unverified-by-design entries, the bib_ledger entry MUST:

- Carry `verification_notes` with the exact failure mode + acquirer
  context + cross-link to verified successor entries where they
  exist.
- Retain the original `primary_url` (so future `/freshness-audit`
  passes can re-attempt).
- NOT have `verified_at` set (so the schema correctly reflects
  unverified status).
- Carry whatever websearch_snippet or other secondary evidence is
  available in `evidence_ledger`, with the originating evidence_id
  referenced in `evidence_ids`.

## Consequences

**Sprint 2 + Sprint 3 inventory:**

- 6 vendor cluster entries surfaced in
  `detector-landscape/bib_ledger.yml`.
- Sprint 3 (folded into M0 close Phase B): 4 promoted to verified
  (HiddenLayer, Guardrails AI, Vijil Dome, Robust Intelligence via
  Cisco acquisition).
- 2 remain unverified-by-design (CalypsoAI, SafePrompt) with
  explicit `verification_notes`.

This is NOT a failure to verify — it is the correct posture per this
ADR, ratified retroactively.

**Detector-landscape audit posture:**

- Final detector-landscape unverified count after Phase B: 2 entries.
- These are the 2 vendor cluster entries unverified-by-design.
- `make dossier-audit` PASSES with `status: unverified` entries
  present in any topic; the validator does not require all entries
  to be verified.

**Periodic re-verification:**

The `/freshness-audit` skill (research_toolkit) MAY re-attempt
unverified vendor cluster entries periodically. Acceptable triggers:
- M0.5 / M1 / M3 / M6 / M7 milestone close-out passes
- News of an acquirer announcement (re-verify against new URL)
- News of a re-launch of the original vendor surface

The unverified-by-design posture does NOT bind future passes; it
documents the *current* failure mode.

**Cross-link discipline:**

When a vendor's product surface has migrated, the unverified entry
SHOULD cross-link to the acquirer's verified entry in
`verification_notes` (per the calypsoai2025_cluster → F5 example).
This preserves analytical continuity for readers.

**Ethics + disclosure compatibility:**

Per ADR-041, vendor product pages are first-party public docs and are
safe to cite at full specificity (no novel attack vectors disclosed
by quoting vendor product claims). The unverified status reflects
URL liveness, not disclosure risk.

**Public-repo licensing compatibility:**

Vendor blog posts are commonly licensed for fair-use quotation. Cached
HTML of vendor blogs is kept local (gitignored per Sprint 2 plan;
public-repo licensing posture: "vendor blogs + closed-access papers
cannot be re-hosted publicly even if arXiv mirroring is technically
permitted"). The unverified entries do NOT host any cached content
publicly.

## Cross-references

- ADR-007 (claim_family + bib_ledger schema)
- ADR-010 (anti-pattern firewall — no URL guessing; verification
  notes use only WebFetch / WebSearch / direct knowledge sources)
- ADR-011 (immutability — once a primary surface goes parked, the
  bib_ledger record of its original URL is preserved)
- ADR-041 (ETHICS — first-party vendor docs safe to cite at full
  specificity)
- ADR-048 (Round 24, cross-classification policy — companion ADR)
- ADR-049 (Round 24, body-quote anchoring discipline — vendor blogs
  often use abstract-level rather than body-quote anchoring)
- `docs/research/detector-landscape/bib_ledger.yml` (6 vendor
  cluster entries documented per this posture)
- Sprint 3 fold-in commit (M0 close Phase B): vendor verification
  attempts + Cisco/F5 acquisition anchoring
