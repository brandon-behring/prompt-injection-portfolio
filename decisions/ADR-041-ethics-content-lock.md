---
adr_id: "041"
slug: ethics-content-lock
title: "ETHICS.md content + HF Hub dataset card alignment"
date: 2026-05-19
status: Accepted
linked_round: "R8"
plan_section: "§20"
---

# ADR-041: ETHICS content lock

## Status

Accepted (Round 8 — locked via 4 sub-questions).

## Context

Per Round 8 walkthrough, ETHICS.md content needs 4 lock decisions:
- Q1: dual-use disclosure tone (full-specificity vs context-trimmed)
- Q2: HF Hub publication terms (public CC-BY-4.0 vs gated)
- Q3: reporting channel (GH Security Advisories vs email vs hybrid)
- Q4: citation format (BibTeX + AI-collaboration acknowledgment)

Round 8 user answers (recommendations accepted):
- Q1: WildGuardMix-style full-specificity disclosure
- Q2: Public CC-BY-4.0 + terms-of-use note in HF Hub card frontmatter
- Q3: Hybrid (GH Security Advisories + secondary email channel)
- Q4: BibTeX + acknowledge Anthropic-ToS-compliant Claude collaboration

## Decision

Lock the ETHICS.md text + HF Hub dataset card text per the Round 8
choices above. The full ETHICS.md draft is captured in plan §20 + landed
in the repo at `/ETHICS.md` (committed Day 1, M0 9b07cdf).

ETHICS.md structure (final):
1. Dual-use disclosure (Round 8 Q1: full-specificity per WildGuardMix
   norms; no novel attack vectors — only documented techniques from
   Greshake et al. 2023 + OWASP LLM01:2025; withholding context would
   foreclose reproducibility without meaningful attacker uplift)
2. Intended use (research / safety eval / benchmarking / teaching)
3. Responsible use (cite + don't redistribute / don't train attack-gen /
   disclose AI assistance in derived work)
4. Anthropic Commercial Service Agreement compliance
5. Citation guidance (BibTeX + AI-collaboration acknowledgment)
6. Reporting concerns (Q3 hybrid: GH Security Advisories + ETHICS.md §6.2
   email channel)
7. Acknowledgments (OWASP / MITRE / Greshake / WildGuardMix / HarmBench /
   ACL Publication Ethics / Anthropic Responsible Disclosure)
8. Version + change log

HF Hub dataset card (frontmatter + body) cross-references ETHICS.md §1
+ §3 + §6.2 for terms-of-use.

## Consequences

- Day 1 ETHICS.md commit (9b07cdf) IS the authoritative text;
  ADR-041 ratifies retroactively.
- Day 15 SECURITY.md complements ETHICS.md §6.1 (GH Security Advisories
  channel) — they cross-reference each other.
- All HF Hub artifact pushes (M3 dataset + M2-M6 model checkpoints)
  include the terms-of-use frontmatter pointing back to portfolio's
  ETHICS.md.
- Future ETHICS.md changes require either a new ADR (substantive) or
  the immutability narrow-relaxation path (typo / link fix).

## Sprint 2 dossier evidence (added M0 close, Round 24)

The Sprint 2 literature dossier reinforces the full-specificity
disclosure decision (Q1) with three lines of evidence from
`docs/research/rag-injection-defenses/` + `docs/research/training-and-evaluation/`:

**Field-norm precedents (cited as disclosure baseline):**

- **`greshake2023bingadvisory`** (greshake.de advisory; production_rag_incidents
  claim family) — Greshake et al.'s 2023 advisory on indirect prompt
  injection. Live primary source verified Sprint 2 with body-quote
  anchoring. The full-specificity-disclosure pattern this ADR adopts
  was already operationalized here.
- **`han2024wildguard`** (WildGuardMix; detector_benchmarks claim
  family) — the comparator's disclosure tone is the calibration target
  for ETHICS.md §1.
- OWASP LLM01:2025 — already cited above; mapped to ADR-041 via
  the public LLM Top 10 documentation.

**Concrete application — `production_rag_incidents` (7 carriers):**

The full-specificity rule directly enables the dossier's
production-incident coverage in `rag-injection-defenses/`:

- **`rag_aimlabs2025echoleak`** (EchoLeak, first zero-click AI
  vulnerability) — Aim Labs disclosure that ETHICS.md §1 norms permit
  citing in full detail.
- **`rag_promptarmor2024slackai`** (Slack AI data exfiltration via
  indirect injection) — PromptArmor 2024 disclosure.
- **`chaikin2025cometprompt`** (Perplexity Comet agentic browser
  indirect injection) — Brave Software 2025 disclosure.
- **`rehberger2025geminimem`** (Gemini memory injection + delayed tool
  invocation) — Embrace The Red 2025 disclosure.
- **`rehberger2023chatgptmd`** (ChatGPT plugin image-based
  exfiltration) — Embrace The Red 2023 disclosure.
- **`sahib2025unseeable`** (unseeable injections in screenshots) —
  Lior Sahib 2025 disclosure.
- Plus EchoLeak's primary advisory + 1 additional carrier.

Without the ADR-041 §1 lock, the dossier could not cite these
incidents with their disclosed payload-shape detail. The lock is what
makes the dossier's production-incident anchoring feasible.

Claim families anchored: `production_rag_incidents` (7 entries) +
`detector_benchmarks` (han2024wildguard).

## Cross-references

- Plan §20 (full ETHICS.md draft text)
- ETHICS.md root file (committed Day 1)
- SECURITY.md (Day 15 governance complement)
- ADR-022 (Round 3 dual-use disclosure decision; superseded by ADR-041
  expansion)
- ADR-024 (Round 3 public-from-M0 visibility; co-ratified)
- ADR-050 (Round 24, vendor cluster posture — applies ADR-041's
  disclosure norm to commercial detector vendors)
- `docs/research/rag-injection-defenses/bib_ledger.yml`
  (claim_family: `production_rag_incidents`)
- Sprint 2 dossier topic README:
  `docs/research/rag-injection-defenses/README.md`
