# Prototype Post-Mortem — `prompt-injection-detection-prototype` (v1.3.0)

> **How to read.** A retrospective on the **first attempt** — the hiring-manager case-study submission — written to inform this independent successor. It is *not* the narrative (that lives in the prototype's own `WRITEUP_*`); it answers four questions: what the prototype achieved, where it fell short and why, what to **carry forward**, and what to **independently re-verify** rather than inherit.
>
> **Provenance.** Read-only audit of the prototype @ tag `v1.3.0`, cross-checked against our own research corpus and `docs/planning/submission-methodology-audit.md` + `decisions/ADR-052-*`, on 2026-05-27. Citations are `file:line` in the prototype unless prefixed `portfolio:`.

---

## 1. What it was

- **Purpose & context.** A polished case-study **submission for a hiring manager** — which is *why* it carries a deliberately heavy, prescribed doc machine (79 ADRs, ~15 root markdown files, an 8-spoke `WRITEUP`, a Quarto site). That weight was fit-for-purpose there; it is **not** the model for this research repo (see §7).
- **Research question** (`WRITEUP_PAPER.md:69-72`): when detectors trained on *direct* prompt-injection examples meet attack families absent from training, does detection generalize? It is a **capability characterization, explicitly not a deployment recommendation**.
- **Scope.** Detection only. Defenses (adversarial robustness, spotlighting, ensembles, augmentation) were *named but deferred*.

## 2. What it shipped — the genuine wins (keep)

- **A clean source-disjoint LODO design** — 4 folds × 3 seeds, a 5-slice OOD slate (BIPIA / InjecAgent / JBB / XSTest / NotInject), with leakage controls and a label-aware dedup discipline (`WRITEUP/data-decisions.md`).
- **The headline finding — the OOD wall.** On pooled OOD, *every* rung sits at/below the random floor (best = frozen probe AUPRC **0.364** vs floor **0.374**) (`RESULTS.md:91-109`). ✅ **Our research independently corroborates this** via four other methodological axes (Bhagwatkar, Hackett, Jung, Fomin, PromptShield Table 4) — so it is *over-determined*, not inherited. **Keep it.**
- **An honest metric suite** — AUPRC + recall@FPR{0.1,1,5%} + ECE (equal-mass + Kumar-debiased) + Brier, all with BCa bootstrap CIs.
- **Calibration as the cleanest *discriminating* signal** — frozen ECE **0.144** vs LoRA **0.444** (`RESULTS.md:236-240`). This was the prototype's most decision-relevant *non-floor* result.
- **Reproducibility + decision rigor** — config-hash invariants, library-first discipline, per-decision ADRs with falsifiable acceptance criteria.

## 3. Where it fell short — and the root causes

The headline is sound; the **cross-rung comparison is confounded**. Per `portfolio:docs/planning/submission-methodology-audit.md:19-31` and `portfolio:decisions/ADR-052`:

- **Confound A — one frozen MLM head for *all* rungs** (`modules_to_save=["classifier"]`): LoRA reads through a head it can't co-adapt.
- **Confound B — a uniform, untuned recipe** (LR 1e-4 / 2 epochs / `eval_strategy: no`): handicaps the higher-capacity rungs.
- **Confound C — no model selection.**
- **Plus:** full-FT OOD was **never measured** (Phase-5 FUSE crash, ADR-075); the context-window ablation is a single fold/seed; and the **"8.4pp contamination-inflation" number has *no derivation in either repo*** — it is inherited from an unnamed prior "V4" iteration.

**Root causes (the useful part):**
1. **A hyperparameter-immutability discipline** ("single locked recipe per rung, no val-set gridsearch") — a *reproducibility* intention applied in the wrong place — **directly produced** confounds A–C. ADR-052 correctly overturns it (fair per-rung tuning on a train-internal val split).
2. **Submission/time pressure** → interventions deferred, the mechanism *asserted not demonstrated*, single-seed ablations.
3. **Cost overrun (16×)** → the LLM-judge rung was dropped at Phase 4.

## 4. Conclusions to NOT inherit — re-verify independently

| Prototype claim | Status | Why fragile | Portfolio action |
|---|---|---|---|
| Best pooled-OOD AUPRC 0.364 vs floor 0.374 | Re-derive | Cross-rung confounds A–C | Re-run with fair per-rung tuning (ADR-052) |
| **"frozen > LoRA"** | ✗ **Do not inherit** | A "mirage" between two sub-random detectors; **our dossiers show fine-tuning (LoRA/DoRA) is field-standard** | Drop as a finding; let Lane-2 measure cleanly |
| "full-FT collapses on OOD too" | Re-verify | **Never measured** (inferred after a crash) | Actually run full-FT OOD (ADR-052) |
| Below-floor AUROC = "anti-correlation/label inversion" | Re-verify | Interpretation, **not demonstrated** | Measure it (per-row score distributions — see B7) |
| "Context window isn't the cause" | Re-verify | Single seed + unseparated backbone/tokenizer confounds | Re-run multi-seed before relying on it |
| Val thresholds don't transfer (LoRA FPR 11.5%) | Partial | Inherits Confound B + single seed | Keep the *val→test inflation* metric; drop the number |
| ProtectAI v2 per-slice deltas | Re-audit | Both versions `suspected_contamination` | Re-run on our own disjoint BIPIA attack-type slate |
| **"8.4pp benchmark inflation"** | ✗ **No evidence** | **No derivation in either repo** | Re-derive on our data, or downgrade to a literature reference |

## 5. Ideas to CARRY FORWARD (present in the prototype, thin/absent in our current plan)

| Idea | Why it matters | Status in portfolio |
|---|---|---|
| **B1 — Calibration battery** (ECE/Brier/reliability + Platt/Beta/isotonic/temperature) | The prototype's *cleanest discriminating signal*; **ADR-052's metric list omits calibration entirely** | **Adopt** — add to the eval suite |
| **B7 — Per-row score-distribution analysis** | The cheap experiment that **demonstrates** the lexical-overfitting mechanism the prototype only *asserted* | **Adopt** — turns interpretation into evidence |
| **B4 — Cohen's-κ / inter-detector error-correlation** | The missing *motivation* for a fusion/stacker lane (low-correlation detectors → ensemble can help) | **Adopt** as a stacker-lane pre-gate |
| **B8 — cv_clt vs block-bootstrap sensitivity flag** | Matters *more* with BIPIA's tiny per-type N (5/type) | **Adopt** — an honesty mechanism |
| **B10 — Label-aware, minimal-pair-preserving dedup** | Needed when we build the independent BIPIA + synthetic corpora (it's a *method*, not the prototype's data) | **Adopt** the discipline |
| B2 dual-policy thresholds · B3 LLM-judge rung + `vendor_black_box` tier (cheap revisit) · B5 style-tagger · B6 conformal · B9 machine-checkable claim-gates | Each a legitimate option | **Hold as options** in the decisions register |

## 6. What to DISCARD / not resurrect

- **The LLM-judge *headline* ladder** (16× cost) — but B3's cheap revisit is fine.
- **Hyperparameter-immutability for modeling** — the root of Confounds A–C; ADR-052 overturns it. (Keep immutability for *decisions/ADRs*, not for *recipes*.)
- **Lakera Guard** reference scorer (ToS, public repo); the **generic line-number citation auditor** (the prototype itself closed it as not-adopted; we use research_toolkit); **single-class-slice metric handling as a project problem** (solved upstream in eval-toolkit #39).

## 7. Process / doc lessons — *why the successor stays simpler*

The prototype's doc machine was built for a submission; replicating it here would be a mistake. Lessons:

- **Avoid:** doc sprawl (15+ root markdown + a parallel `docs/` tree); the **same decisions re-narrated across 3 files** (SPEC_GREENFIELD ↔ SPEC_SHEET ↔ WRITEUP spokes, ~1500 duplicated lines); an immutability rule so rigid it **spawned ~9 ADRs governing the ADR process itself**; version-churn woven into living reference docs; and docs that **mix "planned" with "happened" until they rot** (the prototype needed bolted-on "current-state overlays").
- **Keep (lightly):** the `[LOCKED]/[OPEN]/[DEFERRED]` inline tags and the **`[OPEN]` micro-template (Decision needed / Options / Considerations / *Default if unsure*)**; a **single decision-ledger table**; **work-completed (not metric-threshold) phase gates**; the `NEXT_STEPS` three-tier future-work ledger (extend / rethink / open-question / out-of-scope); and "How to read this page" headers.
- **→ The successor uses ONE lean `ROADMAP.md`** (plus this post-mortem), not a doc ecosystem. The prototype's own `SPEC_GREENFIELD.md` already models the good half: organize by **concern** (threat/data/model/eval/threshold/process), separate `[LOCKED]` rigor from `[OPEN]` instantiation, and carry a single decision ledger.

## 8. Independence status — where the portfolio still leaks the prototype

Tracked as **open items** in `ROADMAP.md` (most resolve once the lane-vs-reframe structural decision resolves):

- **E1** — `decisions/ADR-016` declares LODO "identical to submission's" and treats the undrivable **8.4pp** as operative evidence.
- **E2** — the lane playbooks (`portfolio:docs/planning/portfolio-lane-execution-playbooks.md:15,117`) quote **0.364** and **"frozen>LoRA"** as fact.
- **E3** — `experiments/MANIFEST.json` links submission ADRs and sources its data slate from the submission's `configs/`; the 6-lane structure is unreconciled with ADR-052.
- **E4** — shared public datasets without our own SHA-pinning; ProtectAI contamination not re-audited on our slate.
- **E5** — the inherited interpretive frame ("fine-tuning hurts") propagated into a few chapter outlines.

**Bottom line.** ADR-052 + the methodology audit + the BIPIA native attack-type split already did the hard independence work and are methodologically *better* than the prototype. The remaining job is to (a) carry forward B1/B4/B7/B8/B10, (b) refuse to inherit the §4 numbers, and (c) reconcile the old 6-lane scaffolding — all captured in `ROADMAP.md`.

---

*Source files — prototype:* `RESULTS.md`, `EVIDENCE.md`, `SUBMISSION_AUDIT.md`, `assumptions.md` (A-008), `WRITEUP/{eval-design,threshold-policy,limitations-and-future-work,data-decisions}.md`, `SPEC_GREENFIELD.md`, `decisions/` (ADR-016/-075). *Portfolio:* `decisions/ADR-052-attack-type-generalization-study-design.md`, `docs/planning/submission-methodology-audit.md`, `docs/planning/attack-type-lodo-harness-spec.md`, `docs/planning/dossier_implications_for_roadmap.md`.
