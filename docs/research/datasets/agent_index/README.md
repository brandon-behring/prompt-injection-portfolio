<!-- AGENT-INDEX: unsafe-input / guardrail-detection datasets (30 entries, family-split). Read this README first, then 00_overview.md. -->

# Unsafe-Input / Guardrail-Detection Datasets — Agent Index

**Purpose:** the dataset side of the prompt-injection research program — where
unsafe-input/guardrail-detection data lives, how to access it, what schema/labels
it carries, and whether it is encoder-ready for the attack-type-generalization study.
**Primary intended consumer:** future Claude Code / LLM agents working in adjacent
projects who need detailed dataset metadata grounded in primary sources. Secondary:
humans reading the material directly.
**Self-containedness guarantee:** this folder has no hard dependence on sibling
files outside itself.
**Scope:** 30 public datasets across direct/indirect injection, jailbreak,
toxicity-safety-guard, over-defense, agentic-trajectory, and aggregated-recipe
families. Gathered + per-entry verified 2026-05-27.
**Coverage:** every entry has source, access, license (or honest `unknown`),
size, soft-tag triple (family / encoder_readiness / study_relevance), and an
encoder-readiness verdict; BIPIA carries the full 15/15 disjoint attack-type taxonomy.
**Last updated:** 2026-05-27.

## ⚠️ Scope boundary

This is a **dataset** dossier (metadata + access + encoder-readiness). For
**methodology / paper synthesis** on prompt injection, see the strict-live paper
dossiers under [`../../`](../../) — `detector-landscape/`, `direct-vs-indirect/`,
`agentic-security-architecture/`, `rag-injection-defenses/`, `training-and-evaluation/`.
This dossier is the upstream input to
[`decisions/ADR-052`](../../../decisions/ADR-052-attack-type-generalization.md)
and the
[attack-type-LODO harness spec](../../planning/attack-type-lodo-harness-spec.md);
it does **not** itself measure detector performance.

**Scope = unsafe-input / guardrail detection** — direct/indirect injection,
jailbreak, toxicity-safety-guard, over-defense, agentic-trajectory,
aggregated-recipe, helper; multimodal/image = pointer only. Phase A captures the
comprehensive map ([`../_candidate_universe.md`](../_candidate_universe.md)); the
ledger holds the verified subset; **dataset SELECTION is deferred to the EDA** —
relevance is a soft hint, not a depth gate.

## How this is organized

Sub-section anchors use a per-file letter prefix (`## A1.` in file 01, `## B1.` in
file 02, etc.). Files split by **family** (the ledger's soft-tag `family` field),
not by source host.

| File | Family | Anchors | When to read |
|---|---|---|---|
| [`00_overview.md`](00_overview.md) | navigation + encoder-readiness tiers + ADR-052 rationale | — | Start here if new to the dossier |
| [`01_injection_direct.md`](01_injection_direct.md) | Direct prompt injection (11) | A1–A11 | User-turn attacks; the largest training corpora |
| [`02_injection_indirect.md`](02_injection_indirect.md) | Indirect injection (5) | B1–B5 | Retrieved/tool/observed; ADR-052's substrate |
| [`03_jailbreak_and_toxicity.md`](03_jailbreak_and_toxicity.md) | Jailbreak + toxicity-safety-guard (4) | C1–C4 | Adjacent unsafe-input axes; co-training material |
| [`04_over_defense.md`](04_over_defense.md) | Over-defense / false-refusal (4) | D1–D4 | Benign FPR controls — keep out of training |
| [`05_agentic_trajectory.md`](05_agentic_trajectory.md) | Agent-environment ASR (3) | E1–E3 | Agent-level eval, not classifier corpora |
| [`06_aggregated_recipes.md`](06_aggregated_recipes.md) | Training-mixture recipes (3) | F1–F3 | SOTA-detector training mixtures |

## Lookup recipes

Routes by question type. Each points to a specific file and section anchor.

- **"Which dataset has a disjoint attack-type train/test split (for ADR-052)?"** → `02` § B1 (BIPIA, 15/15 text types).
- **"What's the largest `(text,label)` injection-intent corpus?"** → `01` § A2 (guychuk, 464,470 rows, apache-2.0) — note "manipulation only" label semantics.
- **"What's the largest binary injection corpus by row count?"** → `01` § A8 (jayavibhav/prompt-injection, 327,154 — license unknown).
- **"What dataset has native train/val/test splits?"** → `01` § A3 (PromptShield, 18.9k/1k/23.5k).
- **"Smallest clean smoke-test set?"** → `01` § A1 (deepset, 662 rows, apache-2.0).
- **"Which sets are genuinely *indirect* (not direct injection)?"** → `02` (whole file: BIPIA B1, Indirect-in-the-Wild B2, LLMail-Inject B3, WAInjectBench B4, WASP B5).
- **"What measures over-defense / false positives on benign prompts?"** → `04` (whole file: OR-Bench D1, NotInject D2, XSTest D3, PINT D4).
- **"Largest over-refusal eval?"** → `04` § D1 (OR-Bench, ~80,400 in `or-bench-80k`).
- **"What's the SOTA reference detector's training data?"** → `06` § F3 (ProtectAI-v2 mixture — a recipe).
- **"Largest real-world *adaptive* attack corpus?"** → `02` § B3 (LLMail-Inject, 208k attacks).
- **"Which web-agent injection set is encoder-ready right now?"** → `02` § B4 (WAInjectBench text JSONL).
- **"Datasets I can train on without license worry?"** → apache-2.0: `01` A1/A2/A3/A7, `03` C2, `06` F1/F3; MIT: `01` A4, `03` C4, `04` D2, `06` F2.
- **"Which datasets have `license: unknown`?"** → `01` § A5/A8/A9/A11, `02` § B2/B4.
- **"What dataset is gated (auth required)?"** → `03` § C1 (WildGuardMix, AI2 Responsible Use), `04` § D4 (PINT, request from Lakera).
- **"Agent attack-success benchmarks (not text classification)?"** → `05` (whole file: AgentDojo E1, ASB E2, InjecAgent E3) + `02` § B5 (WASP).
- **"A benchmark I cannot download (held out)?"** → `04` § D4 (PINT — withheld for anti-contamination).
- **"Which set captures system-vs-user prompt structure?"** → `01` § A4 (SPML).
- **"Where's the prompt-extraction vs hijacking taxonomy?"** → `01` § A5 (Tensor Trust).
- **"Is arXiv 2604.27202 real?"** → yes — `02` § B2 (verified genuine; corpus unreleased; ≠ arXiv:2601.07072).
- **"Which dataset carries an `adversarial` flag for shortcut-vs-adversarial EDA?"** → `03` § C1 (WildGuardMix) + `03` § C3 (ToxicChat `jailbreaking` column).
- **"Which dataset has both `toxicity` AND `jailbreaking` axes?"** → `03` § C3 (ToxicChat).
- **"Real-traffic moderation corpus?"** → `03` § C3 (ToxicChat — anonymized Vicuna-demo).
- **"Multilingual coverage?"** → `01` § A1 (deepset DE+EN), `03` § C3/`04` § D2 (multilingual subsets), `02` § B4 (multilingual annotations on PromptShield).
- **"Which entries are flagged unverified?"** → `01` § A7 (Harelix, HF 401), `02` § B2 (Indirect-in-the-Wild, unreleased), `04` § D4 (PINT, withheld); plus `01` § A11 (xTRam1, mismatched).

## Glossary

- **Direct vs indirect injection** — direct: attacker text in the user turn;
  indirect: attack rides in a retrieved/tool/observed document the model ingests.
  The study targets indirect→indirect.
- **Jailbreak** — user-turn attempts to bypass system/safety policy (distinct
  from injection, though the boundary blurs). Family file `03`.
- **Toxicity-safety-guard** — general harm/refusal moderation labels (often from
  real traffic); useful as co-training material for guardrail detectors.
- **Over-defense / benign-FPR** — flagging benign-but-suspicious prompts as
  attacks; measured by NotInject + XSTest + OR-Bench.
- **Attack-type-LODO** — leave-one-distribution-out over *attack types* (train
  on some injection techniques, test on disjoint ones); BIPIA's 15/15 split is
  the substrate.
- **Encoder-readiness** — whether a set is a drop-in `(text, label)` corpus for
  a ModernBERT-style classifier, or needs adaptation (carrier injection, field
  assembly) or is eval-only.
- **ASR** — attack success rate (agent benchmarks report this, not classification
  metrics).
- **Hard negatives** — benign inputs crafted to look like attacks (PINT category).
- **Carrier** — the benign host text an injection is embedded into;
  carrier-shift ≠ attack-type-shift.
- **`task_family`** — the dataset_ledger's fixed enum: here `classification`
  (labeled text) vs `other` (attack-success benchmarks, recipes, unreleased
  corpora).
- **`status`** (ledger field) — `verified` (WebFetch-confirmed) / `unverified`
  (data not confirmable — e.g. withheld or HF 401) / `mismatched` (page
  attribution conflicts, e.g. xTRam1's wrong citation).

### Soft-tag enums (ledger fields)

- **`family`** — `injection-direct` / `injection-indirect` / `jailbreak` /
  `toxicity-safety-guard` / `over-defense-control` / `agentic-trajectory` /
  `aggregated-recipe` / `helper`. Drives the file split here.
- **`encoder_readiness`** — `drop-in` (clean `(text,label)` with split) /
  `derivable` (assemble fields, supply benign carriers, or concatenate configs) /
  `eval-only` (held-out, never a training split) / `adaptation-heavy` (not a
  static labeled corpus; needs harness adaptation) / `pointer` (recipe or
  unreleased corpus).
- **`study_relevance`** — `high` / `medium` / `low`. **Soft hint only** —
  dataset selection is deferred to the EDA, not gated by this field.

## Verification & limits

- All 30 entries WebFetch-checked 2026-05-27; metadata transcribed into
  `../dataset_ledger.yml` (validates).
- Honest flags retained: xTRam1 mismatched (license unknown + wrong arXiv
  citation), Harelix unverified (HF 401 at gather; license corroborated by
  search snippets), PINT data withheld, Indirect-in-the-Wild corpus unreleased,
  6 sets license-unknown (xTRam1, both jayavibhav, Tensor Trust, WAInjectBench,
  Indirect-in-the-Wild).
- Row counts marked `~` or "count after clone" where the source card/README
  omitted exact figures — not fabricated.
**Independent audit, round 1 (2026-05-27):** A complementary-scope review pass
focused on license + access + metadata correctness (the first audit round on
this dossier). Prior rounds covered nothing (initial audit). Findings: 0 dropped,
2 corrected, 0 newly flagged (existing license-unknown / unverified / mismatched
flags re-verified and retained). Spot-check passed on ~28/30 entries against
primary sources (HF dataset cards + GitHub READMEs + arXiv abstracts). The two
CORRECT fixes: (1) **LLMail-Inject** schema clarified — success flags
(email.retrieved / defense.undetected / exfil.sent / exfil.destination /
exfil.content) are NESTED inside the `objectives` JSON-string column, not
separate top-level columns; the `scenario` column's 40 string-classes are
scenario×defense×LLM **levels** (only 4 underlying scenarios per the dataset
card); also expanded the column list to include the missing `completed_time`,
`job_id`, `output`, `scheduled_time`, `started_time`, `team_id` columns observed
on the HF card. (2) **XSTest** `prompts` subset schema corrected from `id` →
`id_v1, id_v2` (per HF column listing). High-priority verifications that
re-confirmed existing flags: xTRam1 citation arXiv:2402.13064 IS the unrelated
"GLAN" paper (confirmed verbatim — flag retained); xTRam1 license remains
undisclosed; both jayavibhav datasets have empty README + no license tag
(retained as `unknown`); Tensor Trust repo has no LICENSE file (paper's CC-BY-4.0
applies to paper text per arXiv abstract; data-redistribution terms unconfirmed
— retained as `unknown`); WAInjectBench has no LICENSE file or statement in the
README (retained as `unknown`); WildGuardMix gated status confirmed
(`auth_required: true` + AI2 Responsible Use); PINT data withheld confirmed;
Indirect-in-the-Wild paper (arXiv:2604.27202) genuine and ≠ arXiv:2601.07072,
corpus not released. Metadata reconciliations: GenTel-Bench HF count is 177,015
(paper headline is 84,812 attacks — HF release evidently bundles benign;
existing caveat retained); BIPIA 15+15 text and 10+10 code attack-type splits
verified verbatim against `text_attack_{train,test}.json` and
`code_attack_{train,test}.json` (the only overlap is "Language Translation");
BIPIA author list including Keegan Hines (4th author) confirmed via secondary
sources (arXiv abstract truncates author list). Harelix (A7) HF page still
returns HTTP 401 — re-verification not possible; status retained as `unverified`.
Reviewer: automated agent (CoVE-factored verification per
`research_toolkit/references/audit_protocol.md`). Recommendation: stop here for
license + access + metadata correctness — the dossier is internally consistent
with primary sources. Future complementary-scope rounds could focus on (a)
detector-claim / paper-headline reconciliations across F-family recipes or (b)
multilingual-coverage / encoder-readiness claims.

- Original gather-stage note: all 30 entries were WebFetch-checked 2026-05-27
  before the audit; metadata transcribed into `../dataset_ledger.yml`
  (validates).

## Attribution

Built by `/dataset-research` (gather + index) for the prompt-injection-portfolio
research program; re-rendered 2026-05-27 against the broadened
unsafe-input/guardrail scope (20 → 30 entries; family split). Source of truth:
`../dataset_ledger.yml`.
