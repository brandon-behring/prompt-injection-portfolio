# Overview — unsafe-input / guardrail-detection datasets

38 public datasets for **unsafe-input / guardrail detection** (broadened from the
original 20-entry indirect-prompt-injection scope on 2026-05-27; +8 EDA-gated in the
2026-06-03 Phase-2 expansion — see the ledger "Newly-surfaced 2026-06-03" table). Built to feed
[ADR-052](../../../../decisions/ADR-052-attack-type-generalization-study-design.md) (attack-type
generalization) and the [attack-type-LODO harness spec](../../../planning/attack-type-lodo-harness-spec.md).

Scope = **unsafe-input / guardrail detection** across families: direct/indirect
prompt injection, jailbreak, toxicity-safety-guard, over-defense, agentic-trajectory,
aggregated-recipe, helper. Multimodal/image = pointer only. The comprehensive
landscape map lives in [`../_candidate_universe.md`](../_candidate_universe.md);
the ledger holds the verified subset.

**Dataset SELECTION is deferred to the EDA** — `study_relevance` is a soft hint
for prioritization, not a depth gate. All 30 entries are equally first-class for
discovery; the EDA decides which ones graduate into a training/eval pipeline.

## Coverage

| File | Family | Entries |
|---|---|---|
| `01_injection_direct.md` | Direct prompt injection (user-turn attacks) | 11 |
| `02_injection_indirect.md` | Indirect injection (retrieved/tool/observed) | 7 |
| `03_jailbreak_and_toxicity.md` | Jailbreak + toxicity-safety-guard (merged) | 6 |
| `04_over_defense.md` | Over-defense / false-refusal controls | 5 |
| `05_agentic_trajectory.md` | Agent-environment ASR benchmarks | 5 |
| `06_aggregated_recipes.md` | Training-mixture recipes | 4 |

By status: **35 verified · 3 unverified** (Harelix/Mixed-Techniques HF 401 at
gather; PINT data deliberately withheld; Indirect-in-the-Wild corpus unreleased) ·
**1 mismatched** (xTRam1 — citation wrong + license unknown). The +8 Phase-2 sets
(2026-06-03) are all EDA-gated + verified; 5 earn roles (2 indirect-carrier prizes +
1 benign control + 1 dedup-salvageable), 3 parked (off-axis / contaminated / env).

By license shorthand (verbatim from ledger): apache-2.0 (deepset, jackhhao,
guychuk, jayavibhav×2 → `unknown`, hendzh PromptShield, Harelix, GenTel-Bench,
ProtectAI-v2 mix); MIT (BIPIA-code, InjecAgent, AgentDojo, LLMail-Inject, ASB,
SPML, NotInject, PINT-harness, InjecGuard, Shen DAN); CC-BY-4.0 (XSTest,
OR-Bench); CC-BY-NC-4.0 (ToxicChat, WASP-majority); ODC-BY (WildGuardMix); **license:
unknown** (xTRam1, jayavibhav×2, Tensor Trust, WAInjectBench, Indirect-in-the-Wild).

## Encoder-readiness tiers (load-bearing for the study)

- **Drop-in `(text,label)`** (train directly, maybe a rename/label-map):
  deepset (A1), guychuk (A2), PromptShield (A3), jayavibhav/prompt-injection (A8
  — ⚠license), jayavibhav/prompt-injection-safety (A9 — ⚠license, multiclass),
  Harelix (A7 — ⚠schema unconfirmed), xTRam1 (A11 — ⚠license/mismatched),
  WAInjectBench text (B4), jackhhao (C2), ToxicChat (C3), GenTel-Bench (F1),
  InjecGuard/PIGuard (F2).
- **Derivable** (inject into carriers / assemble fields / concatenate configs):
  BIPIA (B1 — the ADR-052 attack-type-split set), LLMail-Inject (B3),
  SPML (A4), Open-Prompt-Injection (A10), Tensor Trust (A5),
  WildGuardMix (C1 — ⚠gated), Shen DAN (C4).
- **Eval-only — keep out of training:** NotInject (D2 — benign FPR),
  XSTest (D3), OR-Bench (D1), PINT (D4 — withheld).
- **Adaptation-heavy (not `(text,label)`):** AgentDojo (E1), ASB (E2),
  InjecAgent (E3), WASP (B5), HackAPrompt (A6).
- **Pointer / unreleased:** ProtectAI-v2 mixture (F3 — recipe over named
  public sets), Indirect Prompt Injection in the Wild (B2 — corpus not
  released as of 2026-05-27).

## Why this matters for ADR-052

The study's axis is **indirect→indirect attack-type generalization**.
**BIPIA (B1)** is the only surveyed set that ships a *disjoint attack-type
train/test split* (15/15 text types, "Language Translation" the sole overlap),
making it the natural attack-type-LODO substrate — with the caveat that ~75
strings/split is a memorization risk. **WAInjectBench (B4)** and the (unreleased)
**in-the-wild corpus (B2)** are the closest genuinely **indirect** detection data;
the high-volume direct-injection classifier corpora (jayavibhav, xTRam1, GenTel,
guychuk, PromptShield) would test carrier-shift, not attack-type-shift.
**NotInject (D2)** supplies the benign-FPR axis the harness spec calls for;
**XSTest (D3)** and **OR-Bench (D1)** broaden the over-defense control axis.
**WildGuardMix (C1)** and **ToxicChat (C3)** add toxicity-safety-guard co-training
material with axis labels (`adversarial`, `jailbreaking`) that are useful for
EDA shortcut diagnostics.
