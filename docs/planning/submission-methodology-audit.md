# Submission methodology audit (motivates ADR-052)

Independent read-only audit of the sibling submission (`prompt-injection-detection-prototype` @ v1.3.0)
done 2026-05-26. It reframed the portfolio (see [[ADR-052]] / `decisions/ADR-052-*`). This is **not** a
criticism of the submission's locked ADRs — they followed a deliberate hyperparameter-immutability
discipline — but a record of *why the portfolio runs a fairer, independently-rebuilt comparison*.

## Findings (from the submission's own RESULTS.md + ADRs)

1. **Sub-random-floor collapse (the real headline).** Cross-Family **Pooled OOD AUPRC** (random floor =
   prevalence **0.374**): frozen-probe **0.364**, ProtectAI-v1 0.361, ProtectAI-v2 0.314, LoRA **0.293**,
   TF-IDF 0.291. **Every rung AND both SOTA references are at/below the random floor** → direct→indirect
   transfer has no signal. "frozen>LoRA" is a **mirage** — a gap between two non-generalizing detectors.
   (Source: submission `RESULTS.md` §1 Cross-Family OOD table.)

2. **LoRA was not broken.** In-distribution validation AUPRC: LoRA **0.974** vs frozen 0.653. LoRA learned
   the task near-perfectly → the OOD collapse is **genuine overfitting**, not an implementation bug.

3. **The cross-rung comparison was confounded** (3 ways, all favoring the simplest rung):
   - **Frozen pre-head:** `ModernBertForSequenceClassification` = encoder → mean-pool → `head`
     (Linear768→768+GELU+LN) → `classifier`. The submission's `modules_to_save=["classifier"]` **freezes
     the `head` for all rungs** (confirmed in `src/training/train_modernbert.py:prepare_model`). Frozen-
     probe's frozen head matches its frozen encoder; LoRA shifts the encoder but reads it out through the
     *same frozen MLM head* + a single linear → the head can't co-adapt. (PEFT's SEQ_CLS default, but it
     makes the comparison unfair.)
   - **Uniform untuned recipe:** LR **1e-4 / 2 epochs / `eval_strategy: no`** shared across frozen-probe,
     LoRA, **and full-FT** (`configs/rungs/*.yaml`; ADR-019). 1e-4 is fine for LoRA but **too high for
     full-FT** (they use 2e-5 for the DeBERTa rung). No model selection / early stopping.
   - ADR-019 acknowledged the single-point lock as "methodologically intentional" but **did not flag**
     that a uniform untuned recipe systematically handicaps the higher-capacity rungs (LoRA, full-FT)
     relative to a linear probe — i.e., it can *manufacture* a frozen>LoRA ordering.

4. **Full-FT OOD was never measured.** ADR-075: the Phase-5 run crashed (X11/FUSE); the "full-FT
   collapse" is **inferred** from LoRA's paired-bootstrap (LoRA −0.071 vs frozen on pooled_ood), not
   observed.

## Implications for the portfolio (→ ADR-052)

- The honest, defensible thesis is the **OOD wall** (all rungs + SOTA ≤ random floor), not an inversion.
- The portfolio's **fair comparison** corrects the confound: per-rung tuning + model selection on a
  **train-internal val split** (LODO test untouched), a **trainable-pre-head option** for LoRA, and an
  **actually-run full-FT OOD** — then re-compare on the disjoint attack-type test.
- The reoriented question is **attack-type generalization** (ADR-052), testable on real data via BIPIA's
  disjoint train/test attack-type split.

## Caveat

Numbers/claims above are from the submission @ v1.3.0 (read via `gh`). The portfolio **independently
rebuilds** the comparison (does not inherit these predictions); these figures are the *motivation*, not
load-bearing portfolio results.
