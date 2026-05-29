---
adr_id: "051"
slug: "dogfood-driven-upstream-adoption-batch"
title: "Dogfood-driven adoption of eval-toolkit v1.x, research_toolkit v2.4.0, book-scaffold-astro v4.x"
date: 2026-05-26
status: Accepted
linked_round: "R26 (dogfooding adoption session)"
plan_section: "§10"
---

# ADR-051: Dogfood-driven upstream adoption batch

## Context

The three load-bearing upstream libraries had drifted ~2 majors ahead of the
portfolio's pins. Rather than a hygiene bump, the goal was **dogfooding**: adopt
the new versions by *using* them as a real consumer, surface friction, and feed
it back upstream as tracked issues (advances ADR-045 / ADR-046).

## Decision

- **eval-toolkit `>=0.47` → `>=1.0`** (lock resolves 1.2.0). Opts into the upstream
  v1.0 stability contract (their ADR 0003: Tier-1 API + 9 Protocols frozen for 1.x).
  No consumer code exists yet (`src/` placeholder) → dogfooding **deferred to M1**;
  this pass is pin + forward-guidance only.
- **research_toolkit reclassified as TOOLING, not a Python dependency.** Removed the
  vestigial `git+…@v1.9.1` dep (nothing imports it; it dragged docling/pdfplumber).
  `make dossier-audit` now bootstraps a repo-local clone pinned to `v2.4.0`
  (`.tooling/research_toolkit`, gitignored) and runs validators in an ephemeral
  `uv` env (PyYAML only) — reproducible, lean, no torch.
- **book-scaffold-astro `^3.6.5` → `^4.4.0`** (resolves 4.5.1) **+ switch to the
  `research-portfolio` profile.** v4's `defineStyle` architecture: `styles:
  [researchPortfolioStyle]` in `astro.config.mjs`; `defineBookSchemas({ preset:
  'research-portfolio', chaptersBase: './src/content/textbook' })` in
  `content.config.ts` (BOOK_PROFILE env is dead in v4).
- **runpod-deploy unchanged** — `>=0.8.4` already equals PyPI latest (the GitHub
  Releases page lagged PyPI; not an unsatisfiable pin).

## Consequences

- Consumer fixes the build forced: per-chapter `freshness` values (the blanket
  `exploratory` was invalid *and* conflated freshness-vs-status); added the
  **required** `last_verified` to all 13 chapters; converted HTML comments
  (`<!-- -->`) to MDX (`{/* */}`) in 6 chapters. Book builds green; 13 chapters
  validate under research-portfolio.
- **Dogfooding friction filed upstream (issues-only):** see
  `upstream_issues.md` — book-scaffold `last_verified`-required-not-optional +
  `book-scaffold validate` CLI ignoring `preset`/`chaptersBase` (reports
  profile=minimal); research_toolkit docling/pdfplumber as hard deps for
  validator-only consumers + evidence_ledger validator can't distinguish
  "cache not populated (re-fetchable)" from a broken anchor.
- **Lane 2 `/dataset-synthesize` stays designated-but-gated** on research_toolkit
  #21/#22/#23 (silent-failure + install gaps); no reliance until they close.
- `make dossier-audit` full pass now requires the populated body-text cache
  (`~/Claude/research_cache`), a heavy re-fetchable artifact — like torch, a CI /
  cache-present concern, not a clean-checkout gate.
- Verification was lightweight-local (contracts + book build + validator mechanism)
  per the chosen posture; full `uv sync` (torch) + cache population stay in CI.

## 2026-05-26 follow-up — bump `v2.4.0` → `v2.4.1` (dogfooding: pin-gap correction)

Re-engaging the dossiers surfaced that the citation/anchor gate was **100% failing**
(detector-landscape substring `0/61`), and the original Consequences above misattributed
it to *cache population* ("can't distinguish 'cache not populated' from a broken anchor",
"full pass requires the populated body-text cache"). **That diagnosis was wrong.** The
cache *is* populated (`~/Claude/research_cache`, 2467 files; blobs **and** extracted
`text/sha256/*.txt` both present). The real cause was a **path-resolution bug**: the
manifests declare `cache_root: ~/Claude/research_cache` with *relative* `text_path` (the
portable form adopted in `5da5fd4`), but in `v2.4.0` the three v3-anchor callers
(`verify_citations.py`, `evidence_ledger.py`, `pre_selection_manifest.py`) never passed
`cache_root` into `verify_excerpt_anchor`, so resolution fell back to the empty
dossier-local `text/` dir → every anchor "file does not exist".

The fix already existed upstream — commit `33f07f9` *"fix(validators): … mixed-cache-location
(#15)"*, **merged to `main` but never tagged**. The `v2.4.0` tag-pin stranded the portfolio
one fix-commit behind a correctness fix it needed. Adopted by tagging **`v2.4.1`** at
`33f07f9` (= `v2.4.0` + #17 docs + #15 fix, validators-only) and bumping `Makefile`
`RT_TAG`. Result: substring pass `0/61 → 61/61` (detector) and `→ 100%` across all
dossiers with verbatim claims (direct 51/51, training 13/13, rag 28/28, agentic 0/0); **`make
dossier-audit` PASS ×5 @ v2.4.1** with no re-fetching.

**Lesson (dogfooding pin policy):** pinning the tooling clone to a *tag* froze it behind a
merged-but-unreleased validator-correctness fix. The pin should track validator-correctness
releases, not a frozen point. A second gap surfaced the same way — no mechanical v3
excerpt-anchor *producer* exists (only a verifier) — addressed separately (producer built +
`v2.5.0`).

## 2026-05-29 amendment — NARROW GPU-ML-stack-for-EDA exception (Phase-3 pre-modeling EDA)

**Scope of the lean-local / library-first posture, clarified.** The ML stack (torch +
sentence-transformers + transformers) is already declared in `pyproject.toml` for M1+ **lane**
modeling. Phase-3 pre-modeling EDA (the deep shortcut/shift analyses → the pre-registered OOD-wall
prediction, `experiments/eda/OOD_WALL_PREDICTION/`) is the first use of that stack **outside** lane
modeling — it runs MiniLM (GPU, via `eval_toolkit.embeddings.make_minilm_embedder`) to compute
embeddings for proxy-A-distance / MMD / UMAP, and loads frozen off-the-shelf reference-scorer probes
(Prompt-Guard-86M, protectai-v2, Prompt-Guard-2) for the V10 score-distribution figure.

**Decision (NARROW):** the local GPU ML stack is authorized **strictly for pre-modeling EDA under
`experiments/eda/`** — embedding-based shift metrics, the reference-scorer probes, and figure
generation. This does **not** widen the posture elsewhere: lane/library code stays library-first
(consumes the frozen eval-toolkit surface; new analytical primitives are built **upstream** in
eval-toolkit, not hand-rolled here — the two Phase-3 modules `eda.lexical_association` +
`eda.distribution_shift` ship as upstream Tier-2 PRs per that invariant). The reference-scorer probes
are **frozen, inference-only** (no training) and carry per-slice contamination/scope caveats — they
are a diagnostic probe, not a trained detector, so this is not "modeling on assumed data."

**Why narrow, not broad:** preserves the lean-local invariant everywhere except the one place with a
concrete, bounded need; avoids re-litigating each future EDA run while not granting a blanket
"EDA may pull anything" licence.
