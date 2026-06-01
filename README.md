# prompt-injection-portfolio

> ⚠️ **Pre-alpha release.** This is a field log of methodology
> work-in-progress. Each chapter carries a freshness badge
> (`exploratory` / `experimental-result` / `locked`). At v0.1.0-pre
> all chapters are `scaffolded`; prose fills as Lanes close at M1+.

## 3 ways to read this work

Per Round 17 architecture, the portfolio ships **three peer-level guides**
in `book/src/content/`, each targeting a different reader. All three share
the same experiment-record substrate (fragments per Round 17 follow-up Q2).

| Guide | Audience | TOC | Status |
|---|---|---|---|
| **Textbook** (`/textbook/[slug]`) | Practitioners learning prompt-injection detection methodology | 13 chapters / 4 parts / KF triadic R/O/E | ✓ skeletons shipped; prose fills M1-M7; ratifies at v0.7.0 |
| **Narrative** (`/narrative/[slug]`) | Curious engineers + recruiters who skim story-form writing | Setup → 6 climb attempts → resolution; heavy cross-chapter threading | ⏳ ships at v0.8.0 (~month 13) |
| **Academic IMRaD** (`/academic/[slug]`) | Researchers + reviewers who want compressed journal-paper flow | Introduction → Background → Methods → Results (6 lanes) → Discussion → Future Work | ⏳ ships at v0.9.0 (~month 14) |

> All three guides ratify + polish at **v1.0.0 (~month 16-17)**. Build-in-public
> posts at `docs/build-in-public/`.

---

## The problem

Prompt-injection detectors routinely report 99% accuracy on held-out splits
of training-adjacent data but collapse under realistic out-of-distribution
evaluation. The submission predecessor at
[brandon-behring/prompt-injection-detection-prototype](https://github.com/brandon-behring/prompt-injection-detection-prototype)
demonstrated this honestly: fine-tuning ModernBERT on direct-injection-heavy
LODO data made the indirect/agentic OOD slice **worse** than the
frozen-probe baseline (BIPIA AUPRC: LoRA 0.293 · frozen-probe 0.364 ·
prevalence 0.374). **Fine-tuning consumed the OOD generalization budget.**

The submission's v1.1.2 DeBERTa-v3-base ablation extended this finding:
chunk_and_average (0.2912) ≈ head_truncation (0.2895) on pooled OOD —
the wall is **not** context-window-driven. It's *backbone-invariant* across
ModernBERT and DeBERTa.

**The wall exists. This repo asks: *can we climb it?***

## Why it matters

Real-world consequences:

- **EchoLeak** (CVE-2025-32711, June 2025) was the first publicly
  documented zero-click indirect-injection exploit in production
  (Microsoft 365 Copilot). It bypassed Microsoft's XPIA classifier +
  Markdown link redaction + Content Security Policy.
- The **"Are Firewalls All You Need?"** critique
  ([Bhagwatkar et al. NeurIPS 2025](https://arxiv.org/abs/2510.05244))
  shows current agentic benchmarks (AgentDojo, InjecAgent, ASB, τ-Bench)
  are saturated by simple two-firewall defenses — exposing how detector
  evaluation can mislead.
- The **CodeIntegrity "98% post-mortem"** (Jan 2026) is the most-cited
  industry self-critique: *"98% on historical data ≠ 98% on tomorrow's
  attacks. Treat your 98% detector as a speed bump, not a wall."*

Detection alone is structurally insufficient — but understanding *why* is
necessary before architectural defenses can be evaluated honestly.

## Our approach

This portfolio extends the submission as the **prototype**. Five lanes
plus a 12-technique adversarial-robustness lane will climb the wall via
complementary methodologies — each a controlled experiment producing
positive or negative evidence:

| Lane | Question | Milestone |
|---|---|---|
| **1** | Direct-injection baseline + Tier B reference scorers (Meta PG2 86M, ProtectAI v1/v2) — is ModernBERT competitive with contemporary SOTA encoders? | M1 |
| **1b** | Full 12-technique character-injection adversarial robustness + CourtGuard multi-agent baseline | M1 |
| **2** | Indirect-injection training data + 2-variant loss ablation (CE baseline + Recall@LowFPR per Meta PG2 recipe) — does new data overcome backbone-invariance? | M2-M4 |
| **3** | RAG-injection live demo + 3-variant Spotlighting toggle (delimit + datamark + encoding) | M5 |
| **4** | Agentic harness + score fusion stacker + adaptive eval (5K LLMail-Inject + PINT-EN 3016) | M6 |
| **5** | TaskTracker activation probe (encoder vs decoder methodology port test) | M2 + M7 |

The book at `book/` (Astro+MDX, Cloudflare Pages — bootstraps at M0 Day 14
once scaffold v3.2 ships) is the field log. Chapters carry freshness
badges indicating maturity (`exploratory` → `experimental-result` →
`locked`).

## What we found

*This section fills in per-milestone as lanes close. Latest results will
link to `evals/` and `book/src/content/chapters/`. At v0.1.0-pre (current),
no lane results have shipped — see plan §9 milestone sequence.*

## Reproduce + read

**Reproducibility ladder** (per ADR-018 + Round 2 Q2'):

- **T0** (eval-from-hub; ~15 min on a laptop, $0): `scripts/eval_from_hub.py`
  — portfolio-owned clean reimplementation per Round 6 Q1''''' (ADR-035).
  Lands at M0 Day 1 / Day 17.
- **T1** (full retrain blueprint; ~18 GPU-h × variant; runpod-deploy):
  `scripts/retrain_blueprint.py` — for researchers with GPU budget.
- **T2** (Docker; cross-machine portability): `Dockerfile` + `compose.yaml`
  — lands at M0 Day 16.
- **T3** (selective notebooks): ~5-6 jupytext-paired notebooks at
  `book/src/content/notebooks/` for Ch 5 (bootstrap walkthrough), Ch 6
  (threshold policy), Ch 8 (12-technique bypass matrix), Ch 9 (Lane 2
  attribution table), Ch 11 (stacker analysis), Ch 12 (activation probe).

**Methodology pointers**:

- Library-first discipline: `decisions/library_imports.md` (lands M0 Day 5)
- ADR governance: `decisions/ADR-*.md` (~30-32 ADRs anticipated)
- Research dossier: `docs/research/` (60-80 files at M0 close)
- Experiment records: `experiments/lane-N-*/{hypothesis,protocol,results,decisions}.md`

**Build-in-public**: weekly Twitter/Mastodon thread + monthly deep-dive
blog post per Round 3 Q4''. Archive at `docs/build-in-public/`.

## License + AI assistance

- **Code**: Apache-2.0 (this file's LICENSE).
- **Book + prose**: CC-BY-4.0 (separate `book/LICENSE` at M0 Day 2+).
- **Citation**: see `ETHICS.md` §5 for BibTeX.
- **AI assistance**: this project was developed in collaboration with
  Claude (Anthropic). See `ETHICS.md` §4 and (when book bootstraps) the
  book frontmatter AI-disclosure for full details. Detailed per-commit
  attribution is preserved via `Co-Authored-By: Claude` git trailers.

## Status + roadmap

| Milestone | Date | Tag | Status |
|---|---|---|---|
| **M0 Day 1** | 2026-05-19 | (seed) | ✓ pre-flight green; repo public |
| **M0 Day 2** | 2026-05-19 | — | ✓ book scaffold + uv pyproject + CI workflow |
| **M0 Day 2.5** | 2026-05-19 | — | ✓ 9 upstream MR issues filed |
| **M0 Day 3a** | 2026-05-22 | — | ✓ Round 20/21/22 pin cascade (eval-toolkit v0.47 + scaffold v3.5 + submission v1.3.0); 6 of 9 MRs closed upstream |
| **M0 Day 3b** | 2026-05-22 | `v0.1.0-pre` | ✓ 7 test-contracts + CI hard-gates green |
| **M0 Day 5 + 14 + 16** | 2026-05-22 | — | ✓ lane skeletons + chapter skeletons + Docker T2 |
| **M0 close** | TBD-week-3 | `v0.1.0` | pending: dossier 60-80 (user-led) + Day 15 governance + Day 17 ADRs + Day 18 templates + Day 19 ratify |
| M1 Lane 1 + 1b | TBD-week-4-5 | `v0.2.0` | pending |
| M7 close (textbook ratify) | TBD-week-13-14 | `v0.7.0` | pending |
| v0.8.0 (narrative ship) | TBD-~month-13 | `v0.8.0` | pending |
| v0.9.0 (academic IMRaD ship) | TBD-~month-14 | `v0.9.0` | pending |
| v1.0.0 cutover (all 3 polished) | ~month 16-17 | `v1.0.0` | pending |

Plan + companion docs:

- Plan: `~/.claude/plans/i-want-to-consider-merry-milner.md`
- Chapter outlines: `~/.claude/plans/portfolio-chapter-outlines.md`
- Experiment record template: `~/.claude/plans/portfolio-experiment-record-template.md`
- Lane execution playbooks: `~/.claude/plans/portfolio-lane-execution-playbooks.md`

(These plan + companion docs are private; portfolio's public ADR + dossier
+ chapter prose will mirror the decisions at M0 close.)
