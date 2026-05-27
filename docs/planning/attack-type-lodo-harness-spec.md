# Attack-type-LODO harness spec (Phase 1 build target)

Executable spec for the independent attack-type-generalization harness locked by **ADR-052**.
Methodologist-first; independent rebuild (own pipeline; do NOT inherit submission predictions).

## 1. Data construction (from BIPIA, verified v=`microsoft/BIPIA`)

Build `(text, label)` rows for a content classifier ("does this untrusted content contain an
injection?"):
- **Positive:** a scenario context with one BIPIA attack string injected (record `attack_type`,
  `attack_subfamily ∈ {task-intent, obfuscation}`, `scenario`, `position`).
- **Negative:** the same scenario contexts *clean* (no injection) + **NotInject** benign-with-trigger
  prompts (the over-defense control).
- Scenarios immediately usable: `email` (50/50), `code` (50/50), `table` (900/100). `qa` (WebQA) and
  `abstract` (Summarization) require license-gated context generation (newsqa / XSum) — Phase-1 optional.
- Attack pool: `text_attack_train.json` = 15 types ×5 = 75 strings; `text_attack_test.json` = 15 types
  ×5 = 75 strings. **Drop "Language Translation" (only overlap) → fully disjoint type sets.**
- Use BIPIA's own context **train/test split** for clean contexts so contexts are disjoint too
  (prevents context memorization confounding the attack-type signal).

## 2. Folds

- **Core — attack-type-LODO (carrier held constant):** train = contexts(train split) × **train-attack
  -types**; test = contexts(test split) × **test-attack-types** (disjoint). Same scenario set both
  sides → the only shift is attack type. Headline experiment.
- **Obfuscation sub-split:** restrict to obfuscation types only — train {Alphanumeric, Homophonic,
  Misspelling, Anagram, Space-Removal} → test {Substitution-Ciphers, Base-Encoding, Reverse-Text,
  Emoji-Sub}. The cleanest *technique*-generalization slice.
- **External check — joint carrier+attack shift:** hold out a scenario AND use test-attacks for it,
  e.g. train {code, table × train-attacks} → test {email × test-attacks}.

## 3. Train-internal validation (corrects the submission's confound)

Carve a **val split from TRAIN only** (e.g. hold out ~3 of the 15 train-attack-types, or a fraction of
train contexts). Use it for **per-rung** LR/epoch (+ LoRA `modules_to_save=["classifier","head"]` toggle)
selection. **Never** touch the test-attack-types / test contexts for selection. This is legitimate
model selection (not test tuning), unlike the submission's uniform untuned recipe.

## 4. Detectors (rungs)

ModernBERT-base: **frozen-probe**, **LoRA** (r∈{8,16} swept on val), **full-FT** (LR swept on val incl.
~2e-5 — the submission's shared 1e-4 was too high for full-FT). TF-IDF+LR classical floor as anchor.
bf16 + fp32-softmax-cast; class_weight balanced. Each rung gets its *own* val-selected recipe.

## 5. Metrics + reporting (per fold)

- **AUPRC** (primary) with bootstrap CI; **random-floor = positive prevalence** in the fold (report
  AUPRC vs floor — the honest "is this above random?" test).
- **TPR@{1, 0.5, 0.1}% FPR**.
- **Benign FPR** on NotInject (over-defense).
- **In-distribution (val) vs LODO (test) inflation** — the "benchmarks lie" gap, measured per rung.
- Per-attack-type breakdown (noisy at N=5/type — report as diagnostic, not headline).

Reporting template per fold: `{rung, fold, AUPRC[CI], floor, TPR@FPR×3, benign_FPR, val→test_drop}`.

## 6. Reproducibility

Seeds (≥3); `experiments/attack-type-lodo/MANIFEST.yml`; predictions parquet per `(rung, fold, seed)`;
source-disjointness assertion (no train↔test attack-type or context overlap) as a pre-run check.

## 7. Honest limitations (document in the writeup)

- **Small attack diversity** (75 strings/split, 5/type) → memorization risk; generalization is to 75
  disjoint test strings, not an open technique space. Mitigation/future: augment diversity (synthesis —
  deferred, gated on `/dataset-synthesize` #22).
- Per-type N=5 → per-type results are diagnostic only; the headline is the aggregate type-split +
  obfuscation sub-family.
- qa/abstract require context generation; Phase 1 may run on email/code/table first.
- Likely outcome: collapse to ~random on the disjoint test-types (echoing the submission) — accepted;
  the value is the *correct, fair* measurement + the val→test inflation demonstration.
