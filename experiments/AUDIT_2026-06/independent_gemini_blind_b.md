# Research Methodology Audit

## (1) Claims vs. Evidence
* **Verdict:** Sound
* **Evidence:** 
  - *Portfolio:* `experiments/carrier-lodo/verdict.json` accurately reports `G(lora)` = +0.067 and CI-low = +0.064, leading to the exact pre-registered `SMALL-THROUGHOUT` verdict utilized in `experiments/carrier-lodo/FINDINGS.md:5`. `experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json` reports T = -0.003, accurately matching the `FALSIFIED` label found in its results matrix.
  - *Prototype:* `RESULTS.md:42` claims LoRA direct validation AUPRC is 0.974. `evals/results.json` corroborates this exactly and accurately matches the claimed pooled OOD AUPRC for the frozen-probe (0.364) and LoRA (0.293) against the 0.374 random floor originally published (`RESULTS.md:83`).
* **Severity:** note

## (2) Comparability
* **Verdict:** Qualified
* **Evidence:** Prototype's `README.md:144` establishes its shift as training on direct-injection data (HackAPrompt, Gandalf, etc.) and testing on a cross-family slate (indirect BIPIA). Portfolio's `README.md:58` shifts the paradigm for Lane 2 to "Indirect-injection training data" and tests on held-out domains *within* the indirect family (`experiments/carrier-lodo/criteria.md:65`).
* **Severity:** note
* **Findings:** The headline results are not in genuine conflict because they answer fundamentally different questions. The prototype demonstrates a failure in *cross-family* transfer (direct $\rightarrow$ indirect). The portfolio circumvents climbing this specific wall by intentionally adding indirect data to the training pool, thereby testing *intra-family* transfer (indirect $\rightarrow$ novel indirect vectors). 

## (3) Methodology Soundness
* **Verdict:** Sound
* **Evidence:**
  - *Leakage Controls:* Both enforce strict source-disjoint splits (`evals/leakage_report.json`).
  - *Prevalence / Base-rate Effects:* Portfolio (`experiments/carrier-lodo/criteria.md:112`) properly diagnoses that 83-94% positive prevalence in BIPIA carriers severely inflates AUPRC, establishing a rigorous basis for switching to the prevalence-invariant ROC-AUC metric.
  - *Pre-registration:* Portfolio utilizes rigorous, dated revisions to definitively lock in evaluation logic before generating predictions (`experiments/carrier-lodo/criteria.md:9`).
  - *Statistical Power:* Portfolio (`experiments/carrier-lodo/FINDINGS.md:46`) honestly caveats its limited statistical power due to n=3 carriers. 
* **Severity:** note

## (4) Audit of Portfolio's Critique of Prototype
* **Verdict:** Wrong (on Confound A), Sound (on B & C)
* **Evidence:** 
  - *Confound A (Frozen pre-head):* Portfolio claims the prototype left the classifier head frozen via `modules_to_save=["classifier"]`. This is factually **WRONG**. In the Hugging Face PEFT library, `modules_to_save` explicitly defines modules that are *unfrozen* and trained in full precision. The head *was* fully co-adapted (`src/training/lora_config.py:27`).
  - *Confound B & C (Untuned recipe & no model selection):* Portfolio's critique here is **SOUND**. Prototype's `src/training/training_args.py:65-67` rigidly locks hyperparameters (LR 1e-4, 2 epochs) and explicitly sets `eval_strategy="no"` (`src/training/training_args.py:166`). This structurally forces the use of the final checkpoint without validation-based early stopping, virtually guaranteeing severe lexical overfitting.
* **Severity:** must-fix-before-release

## (5) Over- and Under-claiming
* **Verdict:** Overclaim (Prototype), Underclaim (Portfolio)
* **Evidence:** 
  - *Prototype Overclaim:* Frames the LoRA failure as a fundamental "cross-family generalization failure" (`README.md:27`), but an AUROC of 0.383 (`evals/results.json`) is significantly below random chance (0.500). This indicates active anti-correlation driven by severe lexical overfitting, rather than an underlying representational wall. 
  - *Portfolio Underclaim:* `experiments/carrier-lodo/FINDINGS.md:5` aggregates the carrier generalization gap entirely under the `SMALL-THROUGHOUT` label (G=+0.067). This effectively buries a crucial security finding: the "table" carrier specifically retains a massive, capacity-resistant +0.205 ROC-AUC gap (`experiments/carrier-lodo/FINDINGS.md:27`). 
* **Severity:** note

## (6) External-Citation Check
* **Verdict:** Wrong
* **Evidence:** Live Google web searches for "arXiv:2602.14161" ("When Benchmarks Lie" / "96.6% dataset-separability <-> 8.4 percentage-point drop") and "arXiv:2510.05244" ("Are Firewalls All You Need?" Bhagwatkar et al. 2025) yield zero results. The citations are either heavily mangled or entirely hallucinated. Consequently, the portfolio's claim that the OOD wall is "over-determined" by 4 independent literature axes relies heavily on unverifiable sources.
* **Severity:** must-fix-before-release

---

## Overall Verdicts

**Overall Verdict on Prototype:** 
The prototype exhibits excellent transparency and artifact persistence. However, its experimental architecture—an untuned, fixed-epoch training recipe devoid of model selection—induced massive lexical overfitting. It over-claims by incorrectly misattributing this self-inflicted artifact to a fundamental cross-family generalization wall.

**Overall Verdict on Portfolio:** 
The portfolio demonstrates exceptional pre-registration rigor and appropriately mitigates metric base-rate inflation. However, its adversarial posture is undermined by a factually incorrect critique of PEFT mechanics (falsely accusing the prototype of freezing the classifier head) and an alarming reliance on unverifiable, hallucinated external arXiv citations to anchor its narrative.

### Top-3 Fixes
1. **Retract the "Frozen Head" Critique (Portfolio):** Correct the postmortem logic to reflect that PEFT's `modules_to_save=["classifier"]` *unfreezes* the head. Confound A is mathematically invalid and must be removed.
2. **Purge/Verify Hallucinated Citations (Portfolio):** Immediately remove or correct all references to `arXiv:2602.14161` and `arXiv:2510.05244`. The claim that the OOD wall is "over-determined" must be critically re-evaluated using exclusively verified, accessible literature.
3. **Elevate the Table Carrier Vulnerability (Portfolio):** Revise the `SMALL-THROUGHOUT` narrative to prominently highlight the +0.205 ROC-AUC generalization gap associated with table-formatted contexts. This critical structural vulnerability must not be obscured by the aggregate mean.
