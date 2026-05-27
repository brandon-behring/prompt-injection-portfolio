<!-- AGENT-INDEX: indirect prompt-injection datasets (20 entries). Read this README first, then 00_overview.md. -->

# Indirect Prompt-Injection Datasets — Agent Index

**Purpose:** the dataset side of the prompt-injection research program — where injection/detection data
lives, how to access it, what schema/labels it carries, and whether it is encoder-ready for the
attack-type-generalization study.
**Scope:** 20 public datasets (attack benchmarks, `(text,label)` detection corpora, over-defense eval,
competition/real-world/web-agent sets), gathered 2026-05-27.
**Coverage:** every entry has source, access, license (or honest `unknown`), size, and an
encoder-readiness verdict; the BIPIA entry carries the full 15/15 disjoint attack-type taxonomy.
**Last updated:** 2026-05-27.

## ⚠️ Scope boundary

This is a **dataset** dossier (metadata + access + encoder-readiness). For **methodology / paper**
synthesis on prompt injection, see the strict-live paper dossiers under
[`../../`](../../) — `detector-landscape/`, `direct-vs-indirect/`, `agentic-security-architecture/`,
`rag-injection-defenses/`, `training-and-evaluation/`. This dossier is the upstream input to
[`decisions/ADR-052`](../../../decisions/ADR-052-attack-type-generalization.md) and
[`docs/planning/attack-type-lodo-harness-spec.md`](../../planning/attack-type-lodo-harness-spec.md);
it does **not** itself measure detector performance.

## How this is organized

| File | Contents |
|---|---|
| [`00_overview.md`](00_overview.md) | coverage stats + the encoder-readiness tiers + why it matters for ADR-052 |
| [`01_benchmarks_agentic.md`](01_benchmarks_agentic.md) | A1–A5: BIPIA, InjecAgent, AgentDojo, LLMail-Inject, ASB |
| [`02_classifier_corpora.md`](02_classifier_corpora.md) | B1–B8: deepset, jackhhao, xTRam1, SPML, jayavibhav ×2, GenTel-Bench, ProtectAI-v2 mix |
| [`03_overdefense_eval.md`](03_overdefense_eval.md) | C1–C2: NotInject, PINT |
| [`04_competition_wild.md`](04_competition_wild.md) | D1–D5: HackAPrompt, Tensor Trust, WAInjectBench, InjecGuard/PIGuard, Indirect-in-the-Wild |

## Lookup recipes

- **"Which dataset has a disjoint attack-type train/test split (for ADR-052)?"** → `01` § A1 (BIPIA, 15/15 text types).
- **"What's the largest `(text,label)` injection set?"** → `02` § B5 (jayavibhav/prompt-injection, 327k — license unknown).
- **"Smallest clean smoke-test set?"** → `02` § B1 (deepset, 662 rows, apache-2.0).
- **"Which sets are genuinely *indirect* (not direct injection)?"** → `01` § A1–A2 (BIPIA, InjecAgent), `04` § D3/D5 (WAInjectBench, Indirect-in-the-Wild).
- **"What measures over-defense / false positives on benign prompts?"** → `03` § C1 (NotInject).
- **"What's the SOTA reference detector's training data?"** → `02` § B8 (ProtectAI-v2 mixture — a recipe).
- **"Largest real-world *adaptive* attack corpus?"** → `01` § A4 (LLMail-Inject, 208k attacks).
- **"Which web-agent injection set is encoder-ready right now?"** → `04` § D3 (WAInjectBench text JSONL).
- **"Datasets I can train on without license worry?"** → `02` § B1/B2 (apache-2.0), `04` § D4 + `03` § C1 (MIT); avoid xTRam1 / jayavibhav (unknown).
- **"Which datasets have license: unknown?"** → `02` § B3/B5/B6, `04` § D2/D3.
- **"Agent attack-success benchmarks (not text classification)?"** → `01` § A2/A3/A5 (InjecAgent, AgentDojo, ASB).
- **"A benchmark I cannot download (held out)?"** → `03` § C2 (PINT, Lakera — request access).
- **"Which set captures system-vs-user prompt structure?"** → `02` § B4 (SPML).
- **"Where's the prompt-extraction vs hijacking taxonomy?"** → `04` § D2 (Tensor Trust).
- **"Is arXiv 2604.27202 real?"** → yes — `04` § D5 (verified genuine; corpus unreleased; ≠ arXiv:2601.07072).

## Glossary

- **Direct vs indirect injection** — direct: attacker text in the user turn; indirect: attack rides in a
  retrieved/tool/observed document the model ingests. The study targets indirect→indirect.
- **Attack-type-LODO** — leave-one-distribution-out over *attack types* (train on some injection
  techniques, test on disjoint ones); BIPIA's 15/15 split is the substrate.
- **Encoder-readiness** — whether a set is a drop-in `(text, label)` corpus for a ModernBERT-style
  classifier, or needs adaptation (carrier injection, field assembly) or is eval-only.
- **Over-defense / benign-FPR** — flagging benign-but-suspicious prompts as attacks; measured by NotInject.
- **ASR** — attack success rate (agent benchmarks report this, not classification metrics).
- **Hard negatives** — benign inputs crafted to look like attacks (PINT category).
- **Carrier** — the benign host text an injection is embedded into; carrier-shift ≠ attack-type-shift.
- **`task_family`** — the dataset_ledger fixed enum; here `classification` (labeled text) vs `other`
  (attack-success benchmarks, recipes, unreleased corpora).
- **status** — `verified` (WebFetch-confirmed) / `unverified` (data not confirmable, e.g. withheld) /
  `mismatched` (page attribution conflicts, e.g. xTRam1's wrong citation).

## Verification & limits

- All 20 entries WebFetch-checked 2026-05-27; metadata transcribed into `../dataset_ledger.yml` (validates).
- Honest flags retained: `xTRam1` mismatched (license unknown + wrong arXiv citation), `PINT` data
  withheld, `Indirect-in-the-Wild` corpus unreleased, 5 sets license-unknown.
- Row counts marked `~` or "count after clone" where the source card/README omitted exact figures — not
  fabricated.
- No independent audit round run yet (`/dossier-audit --focus "license risks + access stability"` is the
  recommended next step).

## Attribution

Built by `/dataset-research` (gather + index) for the prompt-injection-portfolio research program,
2026-05-27. Source of truth: `../dataset_ledger.yml`.
