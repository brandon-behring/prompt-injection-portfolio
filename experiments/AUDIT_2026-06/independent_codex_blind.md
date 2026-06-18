I treated `criteria.md`, `FINDINGS.md`, `verdict.json`, ADRs, and persisted eval JSONs as the formal record. I treated READMEs, narrative writeups, and planning notes as loose summaries unless they matched formal artifacts. I did not read the excluded memo, modify files, recompute metrics, or run experiments.

**(1) Claims Vs Evidence**

- **[Sound][note] Portfolio attack-type formal claim.** The formal record supports: cheap rungs show the predicted OOD-wall pattern, but the LoRA ceiling falsifies the pre-registered prediction. Evidence: pre-reg and rule in `portfolio/experiments/eda/OOD_WALL_PREDICTION/criteria.md:1-15`, `:76-90`; LoRA verdict `FALSIFIED`, `T=-0.00309`, `p=.900`, CI lower bound `<0` in `portfolio/experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json:20-44`; rung table in `portfolio/experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md:65-92`.

- **[Sound][note] Portfolio carrier-LODO formal claim.** The carrier result is not a “standing wall”; it is `SMALL-THROUGHOUT`, with a residual LoRA ROC-AUC gap driven mainly by table. Evidence: decision rule and ROC switch in `portfolio/experiments/carrier-lodo/criteria.md:118-139`; verdict and gaps in `portfolio/experiments/carrier-lodo/verdict.json:2-20`, `:28-87`; interpretation and limitations in `portfolio/experiments/carrier-lodo/FINDINGS.md:1-24`, `:48-62`.

- **[Qualified][note] Portfolio loose summaries lag the formal record.** The README still foregrounds predecessor/prototype OOD collapse and says no lane results were shipped at `v0.1.0-pre`, while current formal experiment artifacts now exist and are more nuanced. Evidence: `portfolio/README.md:27-39`, `:84-88`; current manifest points to canonical OOD-wall results in `portfolio/experiments/MANIFEST.json:5-10`.

- **[Sound][note] Prototype headline numbers match artifacts.** The `RESULTS.md` pooled OOD AUPRC table is backed by persisted JSON and numeric audit: frozen `.364`, LoRA `.293`, TFIDF `.291`, random floor `.374`. Evidence: `prototype/RESULTS.md:89-96`; `prototype/evals/results.json:12-67`, `:69-124`; `prototype/evals/audit/numeric_audit.json:63-133`.

- **[Qualified][note] Prototype direct-learning claim is real but narrower than a full detector claim.** Direct validation is strong, but direct LODO held-out positive sources are all-positive and therefore only recall-like, not ranking/FPR evaluation. Evidence: validation table in `prototype/RESULTS.md:39-48`; LODO recall-only table in `prototype/RESULTS.md:50-64`; all-positive direct LODO test folds in `prototype/evals/data_audit.json:91-224`.

- **[Sound][note] Prototype full-FT OOD absence is disclosed.** Full-FT OOD was not run after the Phase 5 crash, so any full-rung OOD/capacity comparison is absent, not hidden. Evidence: `prototype/RESULTS.md:81-96`; `prototype/decisions/ADR-050-rung-slate-narrowing-llm-judges-and-full-ft-ood-dropped.md:30-46`, `:121-158`.

**(2) Comparability**

- **[Sound][note] They measured different populations and shifts.** Portfolio measures BIPIA indirect-injection generalization over native disjoint attack types and then carrier LODO inside BIPIA. Evidence: `portfolio/decisions/ADR-052-attack-type-generalization-study-design.md:21-42`; `portfolio/docs/planning/attack-type-lodo-harness-spec.md:6-34`; carrier folds in `portfolio/experiments/carrier-lodo/criteria.md:50-57`, `:143-161`.

- **[Sound][note] Prototype measures cross-family OOD from direct-heavy training.** Prototype trains on four direct positive sources plus benign sources, then tests on BIPIA, InjecAgent, JailbreakBench, XSTest, and NotInject. Evidence: `prototype/README.md:136-143`; slate composition in `prototype/RESULTS.md:191-208`; formal paper setup in `prototype/WRITEUP_PAPER.md:130-141`, `:199-211`.

- **[Sound][note] Headline results are not directly comparable and not in genuine conflict.** Prototype’s LoRA failure is direct/benign-mixture-to-cross-family OOD at prevalence `.374`; portfolio’s LoRA success is BIPIA indirect-to-indirect attack-type LODO, and carrier-LODO uses high-positive carrier folds. Evidence: prototype random floor `412/1101=.374` in `prototype/RESULTS.md:21-24`; portfolio carrier prevalence caveat `83-94%` in `portfolio/experiments/carrier-lodo/criteria.md:118-139`; AUPRC inflation caveat in `portfolio/experiments/carrier-lodo/FINDINGS.md:48-52`.

**(3) Methodology Soundness**

- **[Sound][note] Leakage controls are strong in both repos.** Prototype reports zero exact and MiniLM near-duplicate overlaps; portfolio audit reports leakage purge and source-disjoint assertions clean. Evidence: `prototype/evals/leakage_report.json:6-118`; `prototype/evals/contamination_scan.json:27-65`; `portfolio/experiments/AUDIT_2026-06/verification_report.md:21-34`.

- **[Qualified][note] Labels are benchmark-valid, not deployment-ground-truth.** Portfolio labels are BIPIA attack-string/context constructions; prototype includes single-class OOD slices and LLM-only dedup calibration labels. Evidence: `portfolio/docs/planning/attack-type-lodo-harness-spec.md:6-23`; `prototype/RESULTS.md:191-208`; `prototype/evals/dedup_calibration.json:13-28`.

- **[Qualified][note] Construct validity is acceptable but thin.** BIPIA attack-type is a real benchmark axis, but only `5/type`; carrier is meaningful but only three carriers, with attack types shared by design in carrier-LODO. Evidence: `portfolio/decisions/ADR-052-attack-type-generalization-study-design.md:21-27`, `:46-49`; `portfolio/experiments/carrier-lodo/criteria.md:93-100`, `:143-161`.

- **[Sound][note] Base-rate handling is unusually honest.** Prototype reports the random AUPRC floor; portfolio explicitly moved carrier-LODO from AUPRC to ROC-AUC because positives are `83-94%`. Evidence: `prototype/RESULTS.md:21-24`; `portfolio/experiments/carrier-lodo/criteria.md:118-139`; `portfolio/experiments/carrier-lodo/FINDINGS.md:48-52`.

- **[Qualified][note] Multiple-comparisons risk remains.** Portfolio’s LoRA decision rule is falsifiable and logged, but Rev1/Rev2 changes and `k=4` tail testing with minimum exact `p=1/70` make it confirmatory-lite, not pristine. Evidence: `portfolio/experiments/eda/OOD_WALL_PREDICTION/criteria.md:150-182`, `:196-222`; red-flag disclosure in `portfolio/experiments/AUDIT_2026-06/verification_report.md:21-34`.

- **[Qualified][note] Statistical power is the largest hard limitation.** Portfolio has `n=5` payload clusters/type and `n=3` carriers; prototype’s per-family OOD slices are small and several are single-class. Evidence: `portfolio/experiments/eda/OOD_WALL_PREDICTION/criteria.md:122-130`; `portfolio/experiments/carrier-lodo/criteria.md:61-89`; `prototype/WRITEUP/limitations-and-future-work.md:60-63`.

- **[Sound][note] Reproducibility hygiene is good.** Prototype pins source revisions and eval metadata; portfolio persists seeds, verdicts, and UTC metadata. Evidence: `prototype/configs/data/source_manifest.yaml:1-153`; `prototype/evals/results.json:2-10`; `portfolio/experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json:2-5`, `:26-30`; `portfolio/experiments/carrier-lodo/verdict.json:89-96`.

- **[Qualified][note] Deployment validity is limited but mostly not hidden.** Prototype says it is not a production detector; portfolio explicitly scopes BIPIA limitations and carrier limitations. Evidence: `prototype/README.md:17-20`, `:216-218`; `prototype/WRITEUP_NARRATIVE.md:96-110`; `portfolio/decisions/ADR-052-attack-type-generalization-study-design.md:46-49`; `portfolio/experiments/carrier-lodo/criteria.md:93-100`.

**(4) Portfolio Critique Of Prototype Confounds**

- **[Qualified][note] “Frozen pre-head” confound is real but overstated.** Prototype’s frozen rung still trains a linear head, and LoRA also saves/trains the classifier head; this matters for causal claims about “fine-tuning” but does not invalidate the frozen-vs-LoRA fixed-recipe comparison. Evidence: `prototype/WRITEUP/model-rungs.md:64-74`, `:94-105`; `prototype/docs/HYPERPARAMETER_DISCLOSURE.md:41-65`.

- **[Sound][note] Uniform untuned recipe is real and material.** Prototype explicitly locked one recipe and rejected validation grid search, so cross-rung architecture conclusions are weak. Evidence: `prototype/docs/HYPERPARAMETER_DISCLOSURE.md:3-7`, `:90-97`, `:116-153`; `prototype/decisions/ADR-019-lora-and-transformer-training-recipe.md:47-49`, `:187-192`.

- **[Sound][note] No model selection is real and material.** Prototype made the fixed-recipe choice deliberately, which improves anti-cherry-picking but weakens claims about model-class capability. Evidence: `prototype/docs/HYPERPARAMETER_DISCLOSURE.md:90-97`; portfolio’s corrected design requires per-rung train-internal validation in `portfolio/docs/planning/attack-type-lodo-harness-spec.md:36-49`.

- **[Sound][note] Full-FT OOD missing is real and material.** The prototype cannot support a full capacity ladder in cross-family OOD because full-FT OOD inference was dropped. Evidence: `prototype/decisions/ADR-050-rung-slate-narrowing-llm-judges-and-full-ft-ood-dropped.md:30-46`, `:150-176`.

- **[Overclaim][note] “Frozen > LoRA was a mirage” is too strong.** Frozen AUROC `.515` vs LoRA `.383` is a real artifact-level difference on the prototype slate, even if it should not be generalized to model-class superiority. Evidence: `prototype/RESULTS.md:250-282`; portfolio critique text in `portfolio/decisions/ADR-052-attack-type-generalization-study-design.md:16-20`.

**(5) Over- And Under-Claiming**

- **[Overclaim][note] Prototype mechanism language sometimes outruns evidence.** Lexical overfit/label-shift is plausible and partly diagnosed, but the paper itself says mechanism is not empirically demonstrated. Evidence: mechanism prose in `prototype/README.md:50-62`; caveat in `prototype/WRITEUP_PAPER.md:515-525`.

- **[Overclaim][note] Prototype DeBERTa/context-window inference should stay narrow.** The ablation is one fold/seed and two truncation variants, so “context window not explanation” is supported only for those configurations. Evidence: `prototype/RESULTS.md:117-163`; residual confounds in `prototype/WRITEUP/limitations-and-future-work.md:163-193`.

- **[Overclaim][note] Portfolio full-FT inference is unmeasured.** ADR-054 says full-FT would only dissolve further, but full-FT was deferred by trigger and not measured. Evidence: `portfolio/decisions/ADR-054-m1-lora-ceiling-full-ft-deferred.md:33-38`, `:76-82`.

- **[Underclaim][note] Portfolio carrier result is useful precisely because it is nuanced.** The formal record downgrades a strong wall to a small residual and isolates table as hard carrier. Evidence: `portfolio/experiments/carrier-lodo/FINDINGS.md:28-44`, `:56-62`; `portfolio/experiments/carrier-lodo/verdict.json:28-87`.

- **[Underclaim][note] Prototype’s reproducibility and contamination audits are stronger than a typical case study.** Source pins, leakage report, contamination scan, and numeric audit are all persisted. Evidence: `prototype/configs/data/source_manifest.yaml:1-153`; `prototype/evals/leakage_report.json:116-118`; `prototype/evals/contamination_scan.json:64-65`; `prototype/evals/audit/numeric_audit.json:271-273`.

**(6) External-Citation Check**

- **[Qualified][must-fix-before-release] arXiv:2602.14161 is real and supports both numbers, but not a literal equivalence.** The paper reports `0.996` CV vs `0.912` LODO AUC, an `8.4%` gap, and separately reports `96.6%` dataset-classifier accuracy; the portfolio wording “dataset-separability ↔ 8.4pp drop” should be phrased as an association/motivation, not a proven bidirectional causal relation. Evidence: local claim in `portfolio/experiments/eda/OOD_WALL_PREDICTION/criteria.md:38-46`; paper at https://arxiv.org/html/2602.14161, especially abstract/table text around the `8.4` gap and dataset-classifier section.

- **[Sound][note] Firewalls citation is real and relevant to benchmark-validity skepticism.** The paper claims simple tool-boundary firewalls achieve `0%` or lowest ASR with high utility across AgentDojo, ASB, InjecAgent, and Tau-Bench, then argues existing benchmarks have weak attacks and flawed metrics. Evidence: local survey in `portfolio/docs/research/detector-landscape/agent_index/05_specialized_detectors.md:104-111`; paper at https://arxiv.org/html/2510.05244.

- **[Sound][note] Guardrail-evasion citation is real and relevant.** Hackett et al. test six guardrails, 12 character-injection methods, and 8 AML/TextAttack-style methods, reporting up to `100%` evasion in some cases. Evidence: local survey in `portfolio/docs/research/detector-landscape/agent_index/05_specialized_detectors.md:113-120`; paper at https://arxiv.org/html/2504.11168.

- **[Sound][note] Over-defense/NotInject citation is real and relevant.** InjecGuard/NotInject frames benign trigger-word false positives and reports SOTA models dropping near random on NotInject. Evidence: local survey in `portfolio/docs/research/detector-landscape/agent_index/05_specialized_detectors.md:23-30`; paper at https://arxiv.org/abs/2410.22770.

- **[Qualified][note] The “over-determined by ~4 axes” claim is directionally supported but should be scoped.** The four axes are real: dataset OOD/shortcut learning, agentic benchmark saturation, adversarial evasion, and over-defense/base-rate false positives; together they justify skepticism about public detector benchmarks, not a proof of any specific portfolio result. Evidence: portfolio research-plan list in `portfolio/docs/research/training-and-evaluation/research_plan.md:19-25`; caveat note in `portfolio/docs/research/compass-survey/02-direct-vs-indirect-deep-dive.md:212-216`; URLs above.

**Overall Verdicts**

- **Portfolio:** Methodologically stronger and more falsifiable than the prototype. The strongest formal result is not “OOD wall everywhere”; it is “attack-type OOD wall prediction fails at LoRA, while carrier has a small residual ROC gap, especially table.” Release claims should match that narrow, useful result.

- **Prototype:** A credible fixed-recipe case study showing cross-family OOD failure for several detectors, with unusually good artifact hygiene. It should not be framed as a fair model-class or capacity-ladder comparison because recipe tuning and full-FT OOD are absent.

- **Comparability:** Not directly comparable and not in conflict. Prototype asks “does direct-trained detection transfer to a heterogeneous cross-family OOD slate?” Portfolio asks “within BIPIA indirect injection, do disjoint attack types/carriers generalize under selected rungs?”

**Top 3 Fixes**

1. Update portfolio public/loose summaries to match formal verdicts, and downgrade the exact `96.6% ↔ 8.4pp` wording to “related evidence from the same paper.”
2. For prototype, either run a fair per-rung selected OOD ladder including full-FT, or label the result as a fixed-recipe case study everywhere.
3. Add targeted mechanism tests: balanced/low-FPR carrier diagnostics for portfolio, and per-prediction lexical/label-shift validation for prototype.