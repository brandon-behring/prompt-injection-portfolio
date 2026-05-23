---
template: milestone
milestone: Sprint 2 close + Sprint 3 fold-in (M0 close preparation)
tag: pre-v0.1.0 (Round 24)
date_posted: 2026-05-23
channels_loud: ["twitter-x", "mastodon-sigmoid", "lesswrong-if-relevant", "linkedin"]
channels_quiet: ["changelog-only"]
---

# Sprint 2 close + Sprint 3 fold-in — pre-v0.1.0 (Round 24)

## TL;DR (3 bullets)

- **210-entry literature dossier across 5 topics** shipped + validated
  via strict-live artifacts (bib_ledger + evidence_ledger +
  cache_manifest + claim_graph + audit_trail). Body-quote-anchored
  ~17 OOD-wall thesis carriers; 124 PDFs cached locally; 157 unique
  BibTeX entries auto-generated into `book/bibliography.bib`.
- **3 new ADRs (048/049/050) + 4 ADR cross-refs (036/038/041/045)**
  formalize the dossier production conventions + cross-link the
  thesis-relevant dossier evidence into the locked decision record.
  Round 24 brings the decisions/ ADR total to 50 entries.
- **861-line synthesis doc** (`docs/planning/dossier_implications_for_roadmap.md`)
  reads the dossier through 6 lane lenses + cross-cutting findings,
  with explicit roadmap-change proposals (decision criteria) for
  Lane 1b / Lane 4 / Lane 5 + a Sprint 4 candidate list.

## What shipped (Round 24, 2026-05-22 to 2026-05-23)

### Sprint 1 (dossier scaffold, M0 Days 6-12) — recap
- Initial dossier scaffold: 5 topic dossiers, ~60-80 files,
  `/research-plan` + `/research-gather` + `/agent-index` +
  `/dossier-audit` pipeline operationalized.

### Sprint 2 (research + cache, this week)
- 2 new topics (`agentic-security-architecture`, `rag-injection-defenses`)
- +88 new bib_ledger entries (210 total across 5 topics)
- +~124 PDFs cached locally (cache stays local per public-repo
  licensing posture — see Sprint 2 plan)
- Body-quote anchors for OOD-wall thesis carriers (~17 entries with
  pdftotext + byte-offset + sha256_of_span precision)
- E6 closure: `experiments/MANIFEST.json` wired to
  `dossier_claim_family` per 6-lane authority graph

### Sprint 3 fold-in (folded into M0 close, this commit set)
- 4/6 vendor cluster entries promoted from unverified to verified
  (HiddenLayer, Guardrails AI, Vijil Dome, Robust Intelligence via
  Cisco acquisition blog)
- 2/6 vendor cluster entries documented as unverified-by-design per
  ADR-050 (CalypsoAI + SafePrompt; parked / for-sale surfaces)
- 2 HF 401 dataset entries probed with browser User-Agent (still 401);
  documented as auth-required, deferred to `/freshness-audit`
- ADR-036/-038/-041/-045 inline "Sprint 2 dossier evidence"
  subsections added (per Sprint 2 E6 deferral)
- 3 new ADRs (048/049/050) formalize cross-classification policy +
  body-quote anchoring discipline + vendor cluster posture
- `book/package.json` bumped from `^3.5.0` to `^3.6.5`
  (book-scaffold-astro brings 10 releases including v3.6.5 release
  pipeline polish)
- MR-13 filed against `brandon-behring/book-scaffold-astro` for a
  citation-js + `%`-comment + `@TYPE`-token lexer bug surfaced
  during Phase I `npm run build:bib` validation

## What we learned (lifted from synthesis doc Zone 1)

### Methodology critique convergence (4 papers, 1 axis)

`bhagwatkar2025firewalls` + `hackett2025bypassing` + `choudhary2025detect`
+ `jung2026postmortem` converge through different methodologies onto
a single observation: detectors that report 95%+ AUPRC on held-out
test sets degrade by 30-60pp under even mild OOD conditions
(character-level perturbation, paraphrase, distribution drift).

A thesis that depends on one paper can be attacked by attacking that
paper. A thesis that depends on a 4-paper convergence with
methodological diversity has a much higher bar.

### TPR@LowFPR is now a multi-paper convergence

Three independent carriers (`jacob2025promptshield` Table 4 +
`li2024injecguard` over-defense quantification +
`meta2025promptguard2-86m` vendor card) treat low-FPR operating points
as the headline metric. ADR-036 shifts from "novel methodology
contribution" to "ratify emerging norm" contribution.

### Vendor landscape is consolidating

6 commercial vendor entries in `detector-landscape/` document two
acquisitions in past 12 months (Robust Intelligence → Cisco;
CalypsoAI → F5) + two parked surfaces. The portfolio's value to
readers shifts: detector cataloging is decreasingly novel;
methodology critique increasingly so.

### Saturated benchmarks justify LLMail-Inject adaptive eval

`abdelnabi2025llmailinject` operationalizes adaptive evaluation in a
way PINT + PromptShield + WildGuardMix cannot. Lane 4's protocol
should pivot to LLMail-Inject as primary headline if M3 results
suggest benchmark saturation per `jung2026postmortem`'s
98%-accurate-still-broken framing.

### Composition_audit methodology is mature

9-paper claim family provides drop-in audit primitives
(`shi2023minkprob` Min-K%-Prob; `zawalski2025codec` CoDeC). Lane 2's
MR-3 synthetic-corpus + ADR-038 audit step can leverage directly.

## What's next (M0 close → M1 lane execution)

### v0.1.0 tag (user-led; separate session)
- `git tag v0.1.0` + `gh release create v0.1.0` (per ADR-047
  Round 22 lock — tag stays user-led)
- M0 announcement Twitter/X + Mastodon thread per this template's
  channel-loudness policy

### M1 entry (post-v0.1.0)
- Lane 1 + Lane 1b execution begins
- Lane 1b fast-iter Hackett-replication check: 3 of 12 character-
  injection techniques against the primary detector set at M1 start.
  If 100% ASR reproduces, Lane 1b rescope decision criterion triggers
  per synthesis doc Zone 2.
- Per-milestone dossier refresh cadence kicks in:
  M1 close → refresh detector-landscape + direct-vs-indirect

### Sprint 4 candidates (deferred to a separate session)
- Cross-vol synthesis layer (portfolio + submission predecessor)
- Lane 6 multimodal injection (`sahib2025unseeable` + Gemini trifecta
  carriers as seeds)
- Post-M1 dossier refresh
- `/freshness-audit` pass — HF 401 entries (auth-resolved retry) +
  vendor cluster re-verification cycle (per ADR-050)
- MR-3 (research_toolkit#1) — `/dataset-synthesize` skill;
  Lane 2 M3-blocking; STILL OPEN at M0 close

## Links

- 📄 Synthesis doc: `docs/planning/dossier_implications_for_roadmap.md`
  (861 lines, 3-zone audience layering, 5 roadmap-change proposals)
- 📚 5 dossier topic READMEs:
  - `docs/research/detector-landscape/agent_index/README.md`
  - `docs/research/direct-vs-indirect/agent_index/README.md`
  - `docs/research/training-and-evaluation/agent_index/README.md`
  - `docs/research/agentic-security-architecture/agent_index/README.md`
  - `docs/research/rag-injection-defenses/agent_index/README.md`
- 🗂 `experiments/MANIFEST.json` (6-lane authority graph + dossier
  claim_family cross-refs)
- 📑 `decisions/ADR-048-cross-classification-policy.md`
- 📑 `decisions/ADR-049-body-quote-anchoring-discipline.md`
- 📑 `decisions/ADR-050-vendor-cluster-posture.md`
- 📑 `decisions/README.md` Round 24 section (3 new ADRs + 4 cross-ref
  ADRs)
- 🐛 MR-13: brandon-behring/book-scaffold-astro#54
  (citation-js + `%`-comment + `@TYPE` lexer bug)
- 🛠 `make dossier-audit` (close-gate validator pipeline) — PASSES
  across 5 topics with all v2.2+ strict-live artifacts green
- 📦 `book/bibliography.bib` — 157 unique BibTeX entries
  auto-generated from 5 dossier bib_ledgers

## Cross-references

- ADR-007 (claim_family naming) + ADR-010 (anti-pattern firewall) +
  ADR-011 (immutability)
- ADR-021 (AI-assistance disclosure — Claude collaboration acknowledged
  in synthesis doc + commit messages per Anthropic ToS)
- ADR-022 + ADR-041 (ETHICS — full-specificity disclosure norm
  per WildGuardMix; production_rag_incidents 7-entry family enabled)
- ADR-023 (build-in-public continuous weekly cadence — this post
  is the Round 24 / Sprint 2 close artifact)
- ADR-024 (public-from-M0 visibility — repo public throughout this work)
- ADR-026 (no-local-workarounds — Lane 2 MR-3 risk discussion in
  synthesis doc respects this)
- ADR-031 + ADR-046 (book-scaffold-astro consumption; this commit
  bumps the pin to ^3.6.5)
- ADR-047 (M0 finish-out strategy — v0.1.0 tag stays user-led)
- Round 24 Sprint 2 close + Sprint 3 fold-in (this artifact set)
