# Independent Multi-Voice Audit — Synthesis (codex + gemini, 2026-06-02)

A cross-model independent check on the in-house memo
(`docs/planning/prototype-comparison-audit-2026-06.md`), which compares `prompt-injection-portfolio`
against the sibling `prompt-injection-detection-prototype`. Two heterogeneous voices — **codex**
(OpenAI gpt-5.5, `xhigh`) and **gemini** (Google 2.5-pro) — each ran a **blind** pass (not shown the
memo) and a **red-team** pass (challenging the memo), read-only, with web-enabled citation checks,
against a single shared rubric. This complements the numeric audit (`verification_report.md`, which
reproduced every statistic 5/5) by re-examining the layer numbers cannot reach: interpretation, scope,
framing, and citation provenance.

## Coverage (honest, including failures)

| Run | Voice | Pass | Status | Report |
|---|---|---|---|---|
| 1 | codex | blind A | **failed** — model context-window overflow (grepped the large `artifacts/*.log`) | — |
| 2 | codex | blind B | ok | `independent_codex_blind.md` |
| 3 | codex | red-team | ok | `independent_codex_redteam.md` |
| 4 | gemini | blind A | ok | `independent_gemini_blind_a.md` |
| 5 | gemini | blind B | ok | `independent_gemini_blind_b.md` |
| 6 | gemini | red-team | ok | `independent_gemini_redteam.md` |
| (retry) | codex | blind C (scoped) | failed — same overflow class | — |

Net: **cross-voice blind** (codex B + gemini A/B) and **cross-voice red-team** both achieved; the
×2 same-voice stability check held for gemini blind (A vs B). codex blind required two attempts; the
failures were plumbing (context overflow / a transient fd error), not signal.

## Consensus — confirmed by ≥2 independent voices + artifacts

- **The two repos are not in genuine conflict — different axes.** All blind voices reached this
  *independently* (gemini blind, while blind to the memo: "not in genuine conflict; they answer
  different questions"; codex blind: "not directly comparable and not in conflict"). Strong,
  un-coached corroboration of the memo's central finding.
- **The memo's four sharp claims survive adversarial review.** Both red-teams marked **A.1**
  (ceiling-compression), **A.2** (axis-conflation), **A.4** (argued-not-measured), and **A.5**
  (cross-family capacity Open) *Confirmed*.
- **The portfolio's critique of the prototype is mostly valid** — the untuned shared recipe and
  no-model-selection confounds are "real and material"; full-FT-OOD-missing is real.
- **The portfolio is methodologically stronger** and its pre-registration is genuine; the carrier-LODO
  record is exemplary self-qualification. Both repos have unusually strong leakage/contamination
  hygiene.
- **Verdict on the memo:** gemini red-team — "safe to act on as-is… exceptionally sharp, fair… not
  self-serving"; codex — core conclusion "logically sound," needs the corrections below.

## The two confident-but-wrong findings (the headline lesson)

A single voice (gemini) issued **two** severe, "must-fix / retract" verdicts that were **both false**,
each caught only by grounding in the actual artifacts:

1. **"`arXiv:2602.14161` is a fabricated citation (web returns no results)."** → **False.** The PDF is
   physically present (`docs/research/training-and-evaluation/papers/fomin2026benchmarkslie.pdf`,
   11.5 MB) and ledgered (`evidence_ledger.yml:3163`, `gather_trace.yml:494`). codex + gemini-blind-A
   independently web-confirmed it. The real (mild) issue: the paper's **8.4pp CV→LODO AUC gap** and its
   **96.6% dataset-classifier accuracy** are *distinct* figures, so the memo/portfolio "↔" should read
   as an association, not equivalence.
2. **"The portfolio's 'frozen pre-head' confound is mathematically invalid — `modules_to_save`
   unfreezes the head."** → **False.** It conflated two modules: `modules_to_save=["classifier"]`
   (`prototype:src/training/lora_config.py:32`) trains only the *final classifier*, leaving the
   *intermediate `head`* frozen — so the portfolio's confound is technically correct (though "real but
   overstated," as it is the PEFT `SEQ_CLS` default).

gemini was even internally inconsistent: blind-A said the citation was real, blind-B and red-team said
it was hallucinated. **Lesson:** lone adversarial LLM voices produce confident, severe, wrong verdicts;
existence / "is-wrong / fabricated" claims **must** be verified against artifacts before being acted on.

## ×2 stability (gemini blind A vs B)

Stable across both samples: comparability/axis-mismatch, methodology soundness, claims-vs-evidence,
the buried table-wall. Unstable: the citation-existence verdict (A: real, B: hallucinated) and the
Confound-A challenge (only B raised it). Both unstable points were resolved by artifact-grounding.

## Corrections applied to the memo (2026-06-02)

1. **A.1 numbers** 0.98–0.999 → **0.956–0.984** (`falsification_verdict.json`). *(codex)*
2. **A5** flipped *Flagged-open* → **Sound (citation real)**; reworded the "↔". *(codex + local check)*
3. **A.3** added the **MiniLM-vs-ModernBERT** geometry model-mismatch. *(gemini red-team)*
4. **§A.5** added the **Confound-A** nuance (correct but overstated). *(cross-voice + config)*
5. **A6/A7/A8** added — stale V10 line; program-review "answered" vs cross-family-Open; full-FT
   monotonicity conjecture. *(codex)*
6. **Part G** added to the memo recording this audit.

## Provenance
- Raw reports: `independent_{codex_blind, codex_redteam, gemini_blind_a, gemini_blind_b, gemini_redteam}.md`.
- Shared rubrics + run commands: `~/.claude/plans/i-want-to-do-elegant-spark.md` (Procedure v2).
- Methodology lesson + procedure upgrades (chain-of-verification, REFORMS + leakage taxonomy,
  bounded heterogeneous debate, inter-rater agreement) are codified in that plan for a future skill.
