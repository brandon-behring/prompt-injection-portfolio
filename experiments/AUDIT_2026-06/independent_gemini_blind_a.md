# Independent Methodology Audit: Prompt-Injection Detection Repositories

This is an independent, adversarial-but-fair audit of the `prompt-injection-portfolio` (PORTFOLIO) and `prompt-injection-detection-prototype` (PROTOTYPE) repositories. The audit strictly evaluates claims against persisted artifacts, methodology soundness, and external citations without relying on the internal `prototype-comparison-audit-2026-06.md` file.

### (1) CLAIMS-VS-EVIDENCE
- **PROTOTYPE:** The claim that TF-IDF + LR reaches 0.971 AUPRC and LoRA reaches 0.974 AUPRC on direct+benign validation is accurate. The claim that cross-family generalization fails (best pooled OOD AUPRC is frozen probe 0.364 vs random floor 0.374; LoRA AUROC is 0.383) is mathematically exact and correctly interprets the floor.
  - **Verdict:** `Sound`
  - **Evidence:** `PROTOTYPE/RESULTS.md` (§1 Cross-Family OOD Table) and `PROTOTYPE/evals/results.json`.
  - **Severity:** `note`
- **PORTFOLIO:** The claim that the OOD prediction is FALSIFIED at the LoRA ceiling is backed by exact statistic matching ($T = -0.003$, permutation $p = 0.900$, CI-low $= -0.008$). The claim that the carrier-LODO gap is "capacity-attenuated" with a "residual table wall" accurately reflects the drop from frozen $G = +0.167$ to LoRA $G = +0.067$.
  - **Verdict:** `Sound`
  - **Evidence:** `PORTFOLIO/experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json` and `PORTFOLIO/experiments/carrier-lodo/verdict.json`.
  - **Severity:** `note`

### (2) COMPARABILITY
- **Construct Analysis:** PROTOTYPE evaluates **cross-family zero-shot generalization** (training on direct injection, testing on indirect/agentic/jailbreak). PORTFOLIO evaluates **within-family adaptation** (training on indirect injection, testing across unseen indirect carriers and attack types).
- **Conflict Assessment:** The headline results are not in genuine conflict; they answer different questions sequentially. PROTOTYPE demonstrates that direct-injection features do not transfer to indirect payloads. PORTFOLIO demonstrates that once trained on indirect payloads, ModernBERT can generalize across attack intents (types), though it still struggles across formatting wrappers (carriers, specifically tables).
  - **Verdict:** `Qualified`
  - **Evidence:** `PROTOTYPE/README.md` (What "OOD" means here) and `PORTFOLIO/experiments/carrier-lodo/FINDINGS.md` (The carrier axis vs the attack-type axis).
  - **Severity:** `note`

### (3) METHODOLOGY SOUNDNESS
- **Leakage & Labels:** Both repositories implement strict Leave-One-Dataset-Out (LODO) protocols with exact-hash and cosine similarity checks to prevent train/test leakage.
- **Construct Validity & Prevalence:** PORTFOLIO geometrically validates its "carrier" construct (MiniLM silhouette by-carrier $0.197$ vs by-attack-type $-0.023$). It also correctly identifies that an 83–94% positive prevalence inflates AUPRC, prompting a switch to ROC-AUC for the carrier-LODO gap. PROTOTYPE acknowledges undefined AUPRC on single-class slices but pools them honestly against a calculated $0.374$ random floor.
- **Pre-Registration:** PORTFOLIO's falsification rules (e.g., top-k/bottom-k tails, $k=4$) were rigorously pre-registered before the LoRA sweep data existed.
  - **Verdict:** `Sound`
  - **Evidence:** `PORTFOLIO/experiments/AUDIT_2026-06/verification_report.md` and `PROTOTYPE/WRITEUP_PAPER.md`.
  - **Severity:** `note`

### (4) AUDIT THE PORTFOLIO'S CRITIQUE OF THE PROTOTYPE
- **The Critique:** PORTFOLIO asserts the PROTOTYPE's cross-rung comparison was confounded by: (a) a frozen pre-head that prevented LoRA from co-adapting the classification head, (b) a uniform untuned recipe (LR 1e-4 / 2 epochs) that handicapped higher-capacity rungs, and (c) a lack of model selection.
- **Independent Assessment:** These confounds are real and material. PROTOTYPE's `modules_to_save=["classifier"]` combined with a fixed 1e-4 learning rate systematically depresses full fine-tuning and adapter efficacy. The observed "frozen > LoRA" ordering in PROTOTYPE is an artifact of undertuning the adapter, not an inherent capability inversion.
  - **Verdict:** `Sound`
  - **Evidence:** `PORTFOLIO/docs/planning/submission-methodology-audit.md:19-31` and `PROTOTYPE/configs/rungs/*.yaml`.
  - **Severity:** `note`

### (5) OVER- AND UNDER-CLAIMING
- **PROTOTYPE:** *Underclaims* the baseline robustness of the frozen probe by attributing its superior performance relative to LoRA to a label-inversion mechanism, rather than acknowledging LoRA's tuning confounds. *Overclaims* an "8.4pp benchmark inflation" figure, which lacks a local derivation in the repository.
  - **Verdict:** `Overclaim` (for the 8.4pp figure), `Underclaim` (for frozen > LoRA mechanism).
  - **Evidence:** `PORTFOLIO/docs/planning/prototype-postmortem.md:43-52`.
  - **Severity:** `must-fix-before-release` (8.4pp claim requires citation or derivation).
- **PORTFOLIO:** Exhibits rigorous self-correction. It actively downgraded its own "standing wall" hypothesis to "capacity-attenuated, residual" based on the LoRA ceiling results, and accepted the falsification of its OOD-wall prediction.
  - **Verdict:** `Sound`
  - **Evidence:** `PORTFOLIO/experiments/carrier-lodo/FINDINGS.md:27-33`.
  - **Severity:** `note`

### (6) EXTERNAL-CITATION CHECK
- **arXiv:2602.14161 (Fomin, 2026):** Verifiably exists. The paper explicitly argues that dataset separability does not equal deployment robustness, citing an 8.4-point AUC inflation due to lexical shortcuts.
- **arXiv:2510.05244 (Bhagwatkar et al., NeurIPS 2025):** Verifiably exists. The "Are Firewalls All You Need?" paper confirms that current agentic benchmarks (AgentDojo, InjecAgent) are easily saturated and lack robustness, supporting PORTFOLIO's claim that the OOD wall is over-determined in the literature.
  - **Verdict:** `Sound`
  - **Evidence:** [Web Search] arXiv:2602.14161 (Max Fomin) and arXiv:2510.05244 (Bhagwatkar et al.).
  - **Severity:** `note`

---

## Overall Verdicts & Top 3 Fixes

**PROTOTYPE Verdict:** A highly transparent, honest, but methodologically confounded zero-shot baseline. It successfully proves that direct-injection detection does not transfer cross-family, but its cross-rung capability comparisons (frozen vs. LoRA) are compromised by an untuned, uniform training recipe.

**PORTFOLIO Verdict:** A scientifically rigorous, well-controlled adaptation study. Its use of pre-registration, geometric cluster validation, and willingness to falsify its own central hypotheses make its findings highly credible.

**Top-3 Recommended Fixes:**
1. **Derive or Cite the 8.4pp Claim:** PROTOTYPE must either provide the local derivation for the "8.4pp benchmark inflation" or explicitly attribute it as an external literature finding (arXiv:2602.14161) rather than a local measurement.
2. **Correct the "Frozen > LoRA" Narrative:** PROTOTYPE's narrative should be amended to acknowledge that the underperformance of LoRA vs. the frozen probe on OOD tasks is largely an artifact of the hyperparameter immutability discipline (frozen pre-head, LR 1e-4), rather than a pure label-inversion capability failure.
3. **Clarify Construct Boundaries:** PORTFOLIO's references to PROTOTYPE's failures must meticulously specify that PROTOTYPE failed at *cross-family zero-shot* transfer, to prevent readers from incorrectly assuming that indirect-injection detection is entirely unsolvable under *within-family* adaptation.
