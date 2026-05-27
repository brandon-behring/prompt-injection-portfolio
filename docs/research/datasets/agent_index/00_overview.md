# Overview — indirect prompt-injection datasets

20 public datasets for prompt-injection **attack** and **detection**, gathered 2026-05-27.
Built to feed [ADR-052](../../../decisions/ADR-052-attack-type-generalization.md) (attack-type
generalization) and the [attack-type-LODO harness spec](../../planning/attack-type-lodo-harness-spec.md).

## Coverage

| File | Category | Entries |
|---|---|---|
| `01_benchmarks_agentic.md` | Attack-success / agent-environment benchmarks | 5 |
| `02_classifier_corpora.md` | `(text,label)` detection corpora | 8 |
| `03_overdefense_eval.md` | Over-defense / held-out eval | 2 |
| `04_competition_wild.md` | Competition / real-world / web-agent | 5 |

By host: ~11 HuggingFace, ~8 GitHub, 1 arXiv-only. By license: permissive (MIT/Apache/CC0) for most
benchmarks + deepset/jackhhao/SPML/NotInject/GenTel/InjecGuard; **`unknown` for xTRam1, both jayavibhav
sets, Tensor Trust, WAInjectBench** (flag before publishing trained artifacts); PINT data withheld.

## Encoder-readiness tiers (the load-bearing synthesis for the study)

- **Drop-in `(text,label)`** (train directly, maybe a rename/label-map): `deepset` (A small smoke-test),
  `jackhhao`, `xTRam1` ⚠license, `jayavibhav/prompt-injection` (327k, the largest) ⚠license,
  `jayavibhav/prompt-injection-safety` (multiclass) ⚠license, `GenTel-Bench`, `WAInjectBench` (text),
  `InjecGuard/PIGuard`.
- **Derivable** (inject into carriers / assemble fields): **BIPIA** (the ADR-052 attack-type-split set),
  `SPML` (system+user fields), `LLMail-Inject` (all-attack; add benign), `InjecAgent` (all-attack).
- **Eval-only — keep out of training:** `NotInject` (benign over-defense / FPR), `PINT` (withheld neutral
  benchmark).
- **Adaptation-heavy (not `(text,label)`):** `AgentDojo`, `ASB`, `HackAPrompt`, `Tensor Trust`.
- **Pointer / unreleased:** `ProtectAI-v2 mixture` (a recipe over named public sets), `Indirect Prompt
  Injection in the Wild` (corpus not released as of 2026-05-27).

## Why this matters for ADR-052

The study's axis is **indirect→indirect attack-type generalization**. **BIPIA** is the only surveyed set
that ships a *disjoint attack-type train/test split* (15/15 text types, "Language Translation" the sole
overlap), making it the natural attack-type-LODO substrate — with the caveat that ~75 strings/split is a
memorization risk. `WAInjectBench` and the (unreleased) in-the-wild corpus are the closest genuinely
**indirect** detection data; the high-volume classifier corpora (`jayavibhav`, `xTRam1`, `GenTel`) are
mostly **direct**-injection text and would test carrier-shift, not attack-type-shift. `NotInject` supplies
the benign-FPR axis the harness spec calls for.
