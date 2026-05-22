---
adr_id: "004"
slug: lane-1b-full-12-character-injection
title: "Lane 1b breadth: full 12-technique character-injection matrix"
date: 2026-05-19
status: Accepted
linked_round: "R1"
plan_section: "§1 Round 1 Q4 + §5"
---

# ADR-004: Lane 1b breadth — full 12-technique character-injection matrix

## Status

Accepted; **simplified by Round 20 cascade** (per
[ADR-045](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md)). The
sequencing complication (core-6 at M1 + advanced-6 backfill) was
resolved by eval-toolkit v0.47.0 shipping `ALL_TECHNIQUES` 12-tuple.

## Context

Lane 1b tests adversarial robustness against character-injection evasion
vectors. Compass survey ("Bypassing Prompt Injection…" arXiv 2504.11168)
documents 12 distinct character-injection techniques achieving up to
100% ASR against legacy DeBERTa detectors.

Three possible breadth strategies:

- **Core subset (~6 techniques)**: cheap; tests common evasion.
- **Full 12-technique matrix**: tests structural robustness across the
  full attack surface; matches compass enumeration.
- **Adaptive expansion**: start with core, expand based on results.

The Round 1 lock prioritized scientific completeness: a robustness
claim that omits half the known attack surface is incomplete.

## Decision

Lane 1b evaluates the **full 12-technique character-injection matrix**:

ZeroWidthSpace + Homoglyph + Diacritic + Whitespace + CaseRandomization +
Punctuation (core-6) + BidiRTL + TagStripping + Synonym + TokenSplitting +
UnicodeNormalization + InvisibleChars (advanced-6).

All 12 techniques shipped as eval-toolkit dataclasses in
`eval_toolkit.adversarial.ALL_TECHNIQUES` (v0.47.0; per
[ADR-045](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md)).

## Consequences

- **M1 Lane 1b matrix**: 12 techniques × ~4 scorers (frozen-probe + LoRA +
  ProtectAI v1/v2 + Meta PG2 + CourtGuard ensemble) = ~48-cell matrix.
  Sample: ~100-200 direct pairs × 12 techniques = ~1.2-2.4k variants.
- **Round 20 simplification**: original sequencing (core-6 M1 start +
  advanced-6 backfill via MR-10) collapsed to single-pass v0.47.0
  consumption. MR-10 OBSOLETED.
- **Cost**: ~$5-8 (CourtGuard ensemble dominates; raw inference is $0-1).
- **Library discipline**: no local character-injection implementations
  permitted per [ADR-026](ADR-026-no-local-workarounds-policy.md);
  all transforms via eval-toolkit dataclasses.

## Cross-references

- Plan §1 Round 1 Q4; plan §5 (Lane 1b hypothesis); plan §10 (MR-2)
- [ADR-045](ADR-045-eval-toolkit-v047-pin-and-api-pivot.md) (v0.47 API pivot)
- [ADR-026](ADR-026-no-local-workarounds-policy.md) (library-first)
- Compass `claim_family=adversarial_robustness`
