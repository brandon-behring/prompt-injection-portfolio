# Dataset ledger corrections — card vs load-inspected (2026-05-28)

Phase-2 full-landscape survey corrected the `dataset_ledger.yml` tags from **measured
truth** (actual `load_dataset()` + `eval_toolkit.eda.audit_dataset`), replacing card-derived
guesses. Each ledger entry now carries a `verification:` marker + an `eda:` summary. Evidence:
`experiments/eda/<bibkey>/audit.json`, `survey_v2_summary.json`, `configs/data/dataset_specs.yml`.

## Corrections that changed a card claim

| dataset | card said | load-inspected reality |
|---|---|---|
| `gentellab` | verified · drop-in | **drop-in via per-file load** — HF auto-concat FAILS (jailbreaking file uses `combined_text` not `text`); load 3 parquets + rename. (My first heuristic pass wrongly marked LOAD-FAIL.) ~177k rows, gates PASS. |
| `reshabhs/SPML` | derivable | **drop-in (binary)** — `System Prompt`+`User Prompt` → `Prompt injection` 0/1. Heuristic missed the spaced/capitalized columns. 16,012 rows, gates PASS. |
| `jayavibhav-safety` | drop-in | **multiclass (3-class)** {0:23414, 1:22586, 2:4000} — NOT binary. |
| `hackaprompt` | adaptation-heavy | confirmed — but the derivable label (`correct`) is **ATTACK-SUCCESS, not injection-presence** → a *different task*, not a binary injection detector. 601,757 rows. |
| `jayavibhav/prompt-injection` | (size carded smaller) | **327,154 rows** + leaky official split. |
| `guychuk/benign-malicious` | (size carded smaller) | **464,470 rows**; gates PASS; has a >8192-token text. |
| `harelix` | unverified | **404 — does not exist on the Hub** (confirms exclude). |
| `wildguardmix` | gated | confirmed **gated** — load blocked even with HF token (needs gate acceptance). |

## Integrity findings the survey surfaced (would have silently inflated metrics)

- **Leaky OFFICIAL train/test splits** (verified real near-duplication, not TF-IDF artifacts —
  spot-checked `jackhhao`: 51/262 test rows are ≥0.9 matches of a train row, differing only by a
  leading newline): `jackhhao`, `xtram1` (120), `hendzh` (86), `jayavibhav` (4/15k sample),
  `lin/toxic-chat` (362). **Use a fresh re-split, not the shipped split.**
- **Class imbalance**: `lin/toxic-chat` is 7% positive (ratio ≥10 — fails `class_balance`).
- **Single-class**: `shen/in-the-wild` is all-jailbreak (positive-only pool); `NotInject` / `xstest` /
  `or-bench` are all-benign (over-refusal/FPR controls). Expected; not defects.

## Honest exclusions / caveats

- `PINT`, `Indirect-in-the-Wild` — withheld / unreleased → `cannot-verify`, never profiled.
- Large sets (`guychuk`, `jayavibhav`, `gentellab`, `hendzh`, `or-bench`, `reshabhs`) were audited
  on a 15k seeded sample (near-dup skipped on the sample); their dedup/leakage counts are **lower
  bounds**. Full-data leakage may be higher.

## Method note (the anti-prototype discipline)

A first heuristic pass (`survey_run.py`) *guessed* columns and produced **false** verdicts on
`gentellab` + `reshabhs`. Replaced with **verified declarative specs** (`configs/data/dataset_specs.yml`)
+ a schema-aware `eval_toolkit.loaders.HFDatasetsLoader` (fail-fast with observed columns).
The loader's fail-fast caught a real NaN-join bug and the un-capped O(n²) runaway — both surfaced
loudly rather than producing silent wrong data.
