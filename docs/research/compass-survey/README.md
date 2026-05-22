# Compass survey artifacts

This directory holds the **raw research-survey artifacts** that seed the
portfolio's literature dossier (plan §4; `docs/research/`). These are
Anthropic Compass-generated literature reviews — published as portable
references so a fresh session on any machine can run the M0 Days 6-12
dossier sprint without needing private `~/Downloads/` state.

## Files

| File | Topic | Lines |
|---|---|---|
| [`01-detector-landscape.md`](01-detector-landscape.md) | Comprehensive survey of every major open detector, every proprietary detector with published benchmarks, every prominent eval benchmark, reconciled head-to-head numbers | ~500 |
| [`02-direct-vs-indirect-deep-dive.md`](02-direct-vs-indirect-deep-dive.md) | Direct vs indirect (XPIA) split codified; multi-layer defense pattern; EchoLeak + Month-of-AI-Bugs case studies; engineering recommendations for 2026 | ~218 |
| [`03-training-and-evaluation-methodology.md`](03-training-and-evaluation-methodology.md) | TPR@LowFPR + OOD methodology; why headline 98-99% accuracy numbers are misleading; PromptShield + PINT benchmark validity arguments | ~337 |

## How to use these (Days 6-12 dossier sprint)

The dossier sprint per plan §4 + §21 ingests these surveys via
`research_toolkit`'s skill pipeline:

```bash
# Compass artifacts are now at docs/research/compass-survey/ instead of
# ~/Downloads/. Run from portfolio repo root:

/research-plan --inbox docs/research/compass-survey/ --output docs/research/_inbox/
/research-gather --inbox docs/research/_inbox/ --output docs/research/gathered/
/dossier-build --gathered docs/research/gathered/ --manifest docs/research/MANIFEST.json
/dossier-audit --manifest docs/research/MANIFEST.json
```

Expected output: ~60-80 decomposed dossier files at `docs/research/`
organized by `claim_family` (e.g., `injection_threat_model`,
`lodo_methodology`, `bootstrap_methodology`, `rung_ladder`,
`ood_evaluation_methodology`, etc.). Each ADR + book chapter +
experiment record cross-references the `claim_family` keys.

## Provenance

- **Source**: Anthropic Compass research outputs (auto-generated literature
  surveys requested by the portfolio author at M0 start).
- **Original location**: `~/Downloads/compass_artifact_wf-*.md` (3 files,
  uuid-suffixed filenames; renamed in-repo for clarity).
- **License + attribution**: per Anthropic Commercial Service Agreement
  (Customer Content; redistributable; cite as Compass-generated literature
  surveys when used).
- **No novel attack vectors**: these surveys synthesize published
  literature (Greshake et al. 2023 + OWASP LLM01:2025 + MITRE ATLAS +
  vendor docs + arXiv preprints). They contain no exfiltration tooling,
  no unpublished exploit payloads, no operational red-team content.

## Update policy

Compass surveys are **point-in-time snapshots** (generated mid-May 2026).
They will become stale as the field evolves. Portfolio's dossier sprint
at Days 6-12 decomposes them into versioned dossier files at
`docs/research/` — those are the live ground-truth references; this
compass-survey directory is the **raw input archive**, not the live
research surface.

## Cross-references

- Plan §4 (dossier target ~60-80 files exhaustive refresh)
- Plan §21 Day 6-12 (dossier sprint deferred to user-led session per
  Round 22 Q2)
- ADR-038 (benchmark integrity audit; cites compass-survey claim about
  Goodhart-discipline)
- ETHICS.md §1 (dual-use disclosure; cites compass artifact threat-model
  taxonomy)
