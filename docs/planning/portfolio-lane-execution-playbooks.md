# Portfolio Lane Execution Playbooks

**Companion to** `/home/brandon_behring/.claude/plans/i-want-to-consider-merry-milner.md` §18.
Produced during 2026-05-19 round-7 holistic review (focus area #4: lane execution playbooks).

Six lanes (1, 1b, 2, 3, 4, 5); each playbook is execution-ready as of v0.1.0 portfolio bootstrap.

---

## Lane 1: Direct-Injection Baseline + Tier B Reference Scorers

**Milestone**: M1 | **Cost**: $10-12 | **Chapter**: Ch 8 | **Duration**: ~3-4 days

### Scope + proof goal
Establish direct-injection detection floor across submission's frozen-probe + LoRA baselines + Tier B reference scorers. Per ADR-052 + v1.1.2 DeBERTa null result, frame the backbone-invariance hypothesis: *ModernBERT frozen-probe AUPRC 0.364 is not context-window-driven; the limitation extends across transformer architectures.*

### Eval slate
- BIPIA-direct-only slice (~500-1000 rows stratified)
- Submission frozen-probe + LoRA (via T0 portfolio-clean eval-from-hub)
- ProtectAI v1 + v2 (CPU inference; local)
- **Meta Prompt Guard 2 86M** (Tier B; mDeBERTa-v3-base; ~$10 GPU)
- **PromptShield Llama-3.1-8B** (Tier C #1; gated; ~$40-50)

### Checkpoints in scope
1. `BBehring/prompt-injection-frozen-probe` (submission)
2. `BBehring/prompt-injection-lora` (submission)
3. ProtectAI v1/v2 (HF Hub auto-download)
4. Meta PG2 86M (HF Hub auto-download)
5. **Portfolio output**: `BBehring/prompt-injection-direct-v2-reference-scorers` (per-rung scores + Tier B/C baselines)

### Execution sequence
1. **Pre-flight**: `make verify-data-sources && uv run python scripts/verify_editable_dep.py`
2. **T0 reproducibility** (~1h): `uv run python scripts/eval_from_hub.py --rung {frozen-probe,lora} --eval-slice bipia --n-rows 500`. Verify score-match within 1e-4.
3. **Tier A reference scorers** (local CPU, ~15 min each): `scripts/score_reference_baselines.py --rung {frozen-probe,lora} --scorer protectai-v1 protectai-v2`
4. **Tier B Meta PG2 86M** (interactive approval, ~2-3h wall, ~$10): `scripts/score_reference_baselines_paid.py --rung {frozen-probe,lora} --eval-slice bipia --scorer meta-prompt-guard-2-86m --budget 12`
5. **Metrics battery** (~1h): `scripts/run_metrics_battery.py --rung-pattern frozen_probe lora --metrics-out evals/metrics/lane1_metrics.parquet`. **Emit TPR@1%, 0.5%, 0.1%, 0.05% FPR** per ADR-036.
6. **Bootstrap CI** (~2h): paired-bootstrap 10K resamples seed=1 headline + seed=2 stability check; report 95% BCa CI on delta AUPRC + TPR@1%FPR.
7. **Figures + summary** (~2h): PR curve overlay + bootstrap delta grid + TPR@LowFPR whisker plot; archive at `docs/plots/lane1/`.

### Outcome branches
- **Positive** (likely): Meta PG2 86M AUPRC ≥ 0.35 on BIPIA direct-only; frozen-probe within 0.02 of PG2. → "ModernBERT frozen-probe competitive with SOTA on direct injection; backbone not limiting."
- **Null** (possible): all encoders cluster 0.30-0.37 AUPRC. → "Modern encoders saturate on direct BIPIA; further gains require non-encoding approaches."
- **Negative** (unlikely): Meta PG2 86M > frozen-probe by >0.05 AUPRC. → "ModernBERT advantage is architecture-specific; Lane 2 indirect data may not compensate."

### Contingency-unlock signal (Tier C #1: PromptShield Llama-3.1-8B)
**Unlock condition**: M1 Tier B results show all base detectors (frozen-probe + LoRA + ProtectAI v1/v2 + Meta PG2 86M) cluster below 0.40 AUPRC pooled OOD → unlock PromptShield. Document via `decisions/contingency_unlock_2.md` + ADR-039.

### Test-contracts
- `no_handrolled_metrics` (eval-toolkit primitives only)
- `predictions_persisted` (per-row parquet)
- `leakage_scan_present` (BIPIA externally sourced; attest in `docs/research/lane1/leakage_audit.md`)

### Book citation (Ch 8 "Reading the OOD Wall, More Carefully")
Opens with Lane 1 direct-injection results as **control condition**: "Direct injection via user input is *not* the limiting factor for ModernBERT-base; the backbone generalizes across detection frameworks. The hard ceiling emerges when the attacker controls the trust boundary itself — a problem direct-classification cannot solve."

---

## Lane 1b: Adversarial Robustness (Character-Injection + CourtGuard)

**Milestone**: M1 (co-scheduled with Lane 1) | **Cost**: $5-8 | **Chapter**: Ch 8 sidenote | **Duration**: ~2-3 days

### Scope + proof goal
Measure whether submission's frozen-probe + LoRA baselines survive 12 character-injection techniques (compass "Bypassing Prompt Injection…" paper arXiv 2504.11168) achieving up to 100% ASR against legacy detectors. Add CourtGuard multi-agent debate baseline (Tier B) to test ensembling over-defense vs single-classifier.

### Eval slate
- BIPIA direct slice (reuse Lane 1)
- **12 character-injection transformations** (per MR-2 upstream): homoglyphs / zero-width Unicode / bidi text / emoji smuggling / Unicode tags / ANSI escapes / base-64 wrapping / upside-down Unicode / noise-word insertion / mixed-case randomization / whitespace variants / comment-style wrapping
- **CourtGuard multi-agent debate** (~$5-10 API): 3 independent detector instances voting on attack/benign; report consensus ASR
- Sample: ~100-200 direct pairs × 12 techniques = ~1200-2400 variants

### Checkpoints in scope
1. Submission frozen-probe + LoRA (Lane 1 baselines)
2. ProtectAI v1/v2 (baseline; expect high ASR per compass §4.2)
3. CourtGuard ensemble (Tier B; ~$5-10 API; 3-agent voting)

### Execution sequence
1. **Pre-flight + MR-2 status check**: implement `eval_toolkit.adversarial.character_injection.CharacterInjectionTransformer` upstream first (no local hand-rolling per ADR-026).
2. **Data prep** (~30 min): apply 12 transformations via `scripts/apply_character_injections.py`.
3. **Inference** (~2-3h wall, ~$3-5):
   - ProtectAI + frozen-probe + LoRA via Lane 1's scorer harness
   - CourtGuard (Tier B gated): `scripts/score_courtguard_debate.py --n-agents 3 --budget 10`
4. **Analysis** (~1h): `scripts/analyze_adversarial_matrix.py --out-table docs/research/lane1b_adversarial_matrix.md`. Metrics: baseline ASR / adversarial ASR / delta / rank-by-robustness per technique × scorer.
5. **Figures** (~1h): heatmap (12 techniques × 4 scorers) + ASR vs technique complexity line plot + CourtGuard consensus violin plot.

### Outcome branches
- **Positive** (likely): frozen-probe ASR increases 20-40% under character injection; CourtGuard consensus reduces ASR 5-15% vs single-detector.
- **Null** (possible): frozen-probe ASR jumps >60%; CourtGuard consensus mirrors single-detector. → "Character injection is fundamental evasion; encoder-only cannot solve."
- **Negative** (unlikely): frozen-probe ASR ≤10% increase; completely resilient.

### Contingency
If CourtGuard consensus achieves >50% ASR reduction on a technique → flag Tier D Lane 7 (v0.8+): optimization-based adaptive attacks (GCG/PAIR) to test ensemble hardening limits.

### Test-contracts
- `no_handrolled_metrics`
- `predictions_persisted`
- `leakage_scan_present` (transformations are synthetic; attest in `docs/research/lane1b/transformation_audit.md`)

### Book citation (Ch 8 sidenote)
"Character-injection evasion vectors defeat >90% of legacy DeBERTa detectors and remain effective against ModernBERT, achieving 40-80% ASR. The submission's frozen-probe offers no special robustness; architectural approaches (Spotlighting, StruQ, SecAlign) and ensemble hardening (CourtGuard) are necessary but insufficient."

---

## Lane 2: Indirect-Injection Training Data + Loss Ablation

**Milestone**: M2-M4 | **Cost**: $156-196 base + $34 optional Tier C | **Chapter**: Ch 9 | **Duration**: ~4-5 weeks

### Scope + proof goal
Test whether indirect-injection training data overcomes BOTH (a) the active-harm fine-tuning pattern per ADR-052 (LoRA -0.071 AUPRC vs frozen-probe on OOD) AND (b) backbone-invariant OOD limits per v1.1.2 DeBERTa null result. Two-variant locked ablation: CE (baseline) + Recall@LowFPR (Meta PG2 recipe). **Tier C optional 3rd variant**: energy-based loss (~$34; gated on M3+M4 signal).

### Eval slate
- **Training corpus**: synthesize ~8-10K indirect positives via Sonnet + Opus audit (~$88-128 API)
  - Augmentation: "This email was forwarded to the assistant: [USER_DIRECT_INJECTION_PAYLOAD]" + role-play RAG retrieval + tool output + web-search snippet
  - 50-50 indirect:direct mix; train fold 0 + seed 42
- **Eval slates**: IDD val (submission ~3K) + OOD direct (BIPIA direct slice) + OOD indirect (BIPIA indirect + InjecAgent + LLMail-Inject sample) + pooled OOD (5 submission OOD slices)

### Checkpoints in scope
1. Submission frozen-probe (baseline; AUPRC 0.364 pooled OOD)
2. **Variant A (CE loss)**: ModernBERT-base + LoRA r=32; standard CE; 2 epochs; fold 0 seed 42
3. **Variant B (Recall@LowFPR loss)**: same backbone + data; custom loss target recall ≥95% @ FPR ≤1%
4. **Optional Variant C (energy loss)**: Tier C gated; Meta PG2 recipe; ~$34
5. **Portfolio outputs**: `BBehring/prompt-injection-{frozen-probe,lora}-indirect-v2-{ce,rfpr[,energy]}` on HF Hub

### Execution sequence

**Phase M2: Data synthesis (~1 week, $88-128 API)**
1. **Pre-flight + MR-3 status**: file `/dataset-synthesize` skill upstream (research_toolkit); may defer to M3 just-in-time.
2. **Synthesis** (~$88-128): `scripts/synthesize_indirect_data.py --base-corpus train_positive.parquet --lm-judges sonnet opus --augmentation-ratio 0.5`. 11K rows raw.
3. **Quality audit** (~$30 API): 200-row sample; inter-annotator kappa target ≥0.5. If <0.5 → retrain template; re-synthesize (contingency unlock gate).
4. **Data finalization** (~1h): filter kappa ≥0.6; merge with original directs; 50-50 stratify; 80-20 train/val.

**Phase M3: Baseline retraining (~2 weeks, $68 GPU)**
5. **Configs**: `configs/rungs/lane2_indirect_{ce,rfpr}.yaml` + `configs/runpod/headline-lane2.yaml` (cost-cap $75/job per ADR-020).
6. **Variant A (CE)** (~$34 GPU, 3.5h wall): `runpod-deploy validate` → dry-run → interactive approval → `scripts/train_rung.py --rung lane2_indirect_ce --loss-fn cross-entropy`. Predictions to `evals/predictions/lane2_indirect_ce__fold0__seed42__*.parquet`.
7. **Variant B (Recall@LowFPR)** (~$34 GPU): file upstream MR-4 if not present; `scripts/train_rung.py --rung lane2_indirect_rfpr --loss-fn recall-at-lowfpr --target-fpr 0.01`. Cost track via `make cost-rollup-check`.

**Phase M4: Evaluation + Tier C gate (~2 weeks)**
8. **Metrics battery** (~1h): pooled + per-slice AUPRC/AUROC/TPR@LowFPR per ADR-036.
9. **Bootstrap CI** (~1h): paired-bootstrap CE vs frozen-probe, RFPR vs frozen-probe, CE vs RFPR; 10K resamples × 2 seeds; BCa 95%.
10. **Tier C contingency gate**:
    - **Unlock condition**: M3 audit kappa ≥0.5 (already locked) AND M4 two-variant CI shows interpretable signal (RFPR delta CI not crossing zero).
    - If unlocked: train Variant C (energy loss) ~$34 GPU.
    - If not unlocked: skip; proceed to synthesis.
11. **Result aggregation** (~1h): `docs/research/lane2_results_summary.md` table per variant × slice × metric.

### Outcome branches
- **Positive** (hoped): Lane 2 Variant B pooled OOD AUPRC ≥0.40; RFPR delta CI clear of zero. → "Indirect data + Recall@LowFPR overcomes active-harm + backbone-invariance. Wall is data-bound."
- **Null** (likely per ADR-052 framing): both variants cluster near 0.36 ± 0.02; delta CI crosses zero. → "Indirect data + loss adjustments do not overcome OOD limit. Wall is structural; non-encoding defenses required."
- **Negative**: variants drop below frozen-probe (e.g., 0.32). → "Indirect augmentation induces distribution shift; fine-tuning remains harmful. Hypothesis must be reformulated."

### Cost envelope (M2-M4)
- M2 synthesis: $88-128 API
- M3 retraining: $68 GPU (2 × $34)
- M4 metrics/bootstrap: $0
- **Tier C optional**: +$34
- **Total**: $156-230 (within $250 base + $100 contingency)

### Test-contracts
- `no_handrolled_metrics`
- `predictions_persisted`
- `leakage_scan_present` (synthetic data audit in `docs/research/lane2/data_audit.md`)

### Book citation (Ch 9 "Climbing with New Training Data")
"Lane 2 tests whether the OOD wall is *data-bound* (addressable via indirect-injection training) or *structural* (requiring non-encoder defenses). The submission's v1.1.2 DeBERTa result established backbone-invariance; Lane 2 examines data-dependent generalization. Two-variant ablation (CE vs Recall@LowFPR loss) disentangles loss-function effects from data-source effects."

---

## Lane 3: Spotlighting Structural Defense

**Milestone**: M5 | **Cost**: ~$1 API | **Chapter**: Ch 10 | **Duration**: ~2-3 days

### Scope + proof goal
Evaluate whether trust-boundary marking (Spotlighting: delimiting + datamarking + base-64 encoding) improves detection on indirect-injection data. Per compass §7, Spotlighting reduces *LLM ASR* from >50% to <2%; Lane 3 measures whether it improves *detection AUPRC*.

### Eval slate
- Indirect-injection test set: BIPIA indirect + InjecAgent + LLMail-Inject sample (reuse Lane 2; ~1000-1500 rows)
- **3 Spotlighting variants**:
  1. **Delimiting**: wrap in `[UNTRUSTED_START] ... [UNTRUSTED_END]`
  2. **Datamarking**: every whitespace → marker token `^`
  3. **Encoding**: base-64 encode + prepend `ENCODED: ` (minimal; no decode prompt)
- Detectors: frozen-probe + LoRA (unchanged; inference-time transformation only)

### Execution sequence
1. **Data transformation** (~30 min): `scripts/apply_spotlighting.py --techniques delimit datamark encode`
2. **Inference** (~1h, $0-1): `scripts/score_spotlighting_variants.py --scorer frozen-probe lora`. **Hosted as HF Space** with interactive toggle for book demo per Q4 round 1.
3. **Metrics** (~30 min): compare AUPRC per variant vs baseline (original text); per-slice + pooled.
4. **Analysis** (~1h): variant × detector × metric comparison table. Does marking help frozen-probe/LoRA detect indirection?

### Outcome branches
- **Positive**: Spotlighting (datamarking) lifts AUPRC +0.05-0.10. → "Structural marking improves encoder awareness; feasible low-overhead defense."
- **Null** (likely): Spotlighting ≤0.02 AUPRC lift. → "Encoder classifiers do not leverage trust-boundary signals; architectural defenses (CaMeL, StruQ) required."
- **Negative**: Spotlighting reduces AUPRC. → "Marking increases token-sequence length; truncation loses signal."

### Test-contracts
- `predictions_persisted`
- `leakage_scan_present` (inherited from Lane 2)

### Book citation (Ch 10 "Watching the Wall in the Demo")
"Spotlighting (trust-boundary marking via delimiting, datamarking, or encoding) is a proven structural defense on *LLM robustness* (Hines et al., ASR 50% → 2%). Lane 3 tests whether it aids *detection* (moving the task from content-only to content+structure). Results show [positive/null]; standalone encoders are insufficient; Spotlighting + multi-layer defense (Spotlighting + detector + output filtering) is necessary."

---

## Lane 4: Fusion + Adaptive Evaluation

**Milestone**: M6 | **Cost**: $5-30 (Tier B embedding-scorer + APR metric) | **Chapter**: Ch 11 | **Duration**: ~2-3 weeks

### Scope + proof goal
Stack per-lane per-rung scores via logistic regression (simple stacker; XGBoost optional refinement). Test embedding-based scorer (OpenAI embeddings + XGBoost; Tier B) as meta-learner alternative to text-only encoders. **Report APR metric** (Meta PG2's % attacks blocked at ≤3% utility loss) across all detector combinations.

### Eval slate
- **Fusion data**: LLMail-Inject 5K stratified + PINT-EN 3,016 (Lakera's held-out; never trained by evaluated detectors)
- **Stacker inputs** (8-10 per-row scores): frozen-probe prob + LoRA prob + ProtectAI v1/v2 prob + Meta PG2 86M prob + Lane 2 indirect-{ce,rfpr} prob + CourtGuard consensus prob + per-agent votes
- **Tier B embedding-scorer** (~$5 API): text-embedding-3-small tokenization + XGBoost on 1K labeled pairs
- **APR metric**: utility-loss thresholds 1% / 3% / 5%; report % attacks blocked at each tier

### Checkpoints in scope
1. All prior lane rungs (8-10 detector outputs)
2. **Stacker meta-learner**: logistic regression on 500 labeled examples
3. **Embedding-based scorer**: XGBoost(OpenAI embeddings) on LLMail-Inject subset (Tier B)
4. **Portfolio output**: `BBehring/prompt-injection-fusion-v2-stacker` with stacker coefficients + constituent score table + APR curves

### Execution sequence
1. **Data assembly** (~2h): download LLMail-Inject + PINT; merge per-lane predictions into wide format.
2. **Embedding scorer training** (~$5 API, 2h): `scripts/train_embedding_scorer.py --embedding-model text-embedding-3-small`. Train XGBoost; evaluate AUC vs frozen-probe on held-out 200 rows.
3. **Stacker training** (~1h, $0): logistic regression; training 500 + val 200 rows; threshold optimization per ADR-025.
4. **Ensemble fusion** (~1h): apply stacker + embedding scorer to LLMail (5K) + PINT (3K).
5. **Metrics battery** (~1h): AUC-PR + AUC-ROC + TPR@LowFPR per ADR-036 for all detectors + stacker + embedding-scorer. Bootstrap CI on stacker delta vs best individual. **APR metric reporting per ADR-037** (% attacks blocked at ≤3% utility loss).
6. **Model card + publication** (~1h): HF Hub model card per detector + stacker; per-detector AUPRC + APR @ 1%/3%/5% utility loss.

### Outcome branches
- **Positive**: Stacker AUPRC > best individual by >0.03; APR @ 3% utility loss >60%. → "Fusion via meta-learner is feasible; complementary signals exist. APR reveals utility-security tradeoff."
- **Null** (likely): Stacker matches best individual ±0.01; APR plateaus <40%. → "Detectors highly correlated; fusion adds no new signal. Architectural defenses must replace, not augment."
- **Negative**: Stacker underperforms best individual. → "Imbalanced data (5% attack prior) causes overfitting; meta-learning needs larger labeled set."

### Test-contracts
- `predictions_persisted`
- APR metric reporting (ADR-037)
- TPR@LowFPR reporting (ADR-036)

### Book citation (Ch 11 "Score Fusion + Adaptive Eval")
"Multi-detector fusion via logistic regression combines signals from frozen-probe, LoRA, reference scorers (ProtectAI, Meta PG2), and structural defenses. Results show [positive/null] fusion gains; APR metric (attacks blocked at ≤X% utility loss) reveals the detection-vs-usability frontier. Practical deployment stacks one detector for pre-filtering + one structural defense + output filtering for exfiltration vectors."

---

## Lane 5: Activation-Space Probing (TaskTracker port test)

**Milestone**: M2 + M7 | **Cost**: $10-20 GPU | **Chapter**: Ch 12 | **Duration**: ~2-3 days

### Scope + proof goal
Train linear probe on submission's frozen-probe ModernBERT activation deltas (pre- vs post-untrusted-data injection). Per compass §7 TaskTracker (Microsoft SaTML 2025) achieves >0.99 AUC on synthetic task-drift; Lane 5 tests whether this transfers to *encoder-only* (vs decoder-LLM) prompt-injection detection on real OOD data. **Validation-only scope per plan §5** (Round 5 F1 + F8 framing: hypothesis is OPEN; negative result is informative).

### Eval slate
- **Training data**: submission's frozen-probe val set (fold 0, seed 42; ~2K IDD rows) + synthetic task-drift pairs (benign summarization prompt + injected instruction in footnote)
- **Test data**: BIPIA indirect slice (task-drift-aligned synthetic attacks)
- **Metric**: activation-delta probe AUC vs frozen-probe softmax AUC; gain/loss reported

### Checkpoints in scope
1. Submission frozen-probe ModernBERT (activation extractor; no fine-tuning)
2. **Portfolio output**: `docs/research/lane5_activation_probe.md` (methodology + results); **no checkpoint published** (validation experiment only)

### Execution sequence (M2 + M7)
1. **M2: Activation extraction** (~1h, ~$10-20 GPU): `scripts/extract_modernbert_activations.py --model-path BBehring/prompt-injection-frozen-probe --layer -2`. Penultimate-layer hidden states (768D) pre + post injection.
2. **M2: Probe training** (~30 min): `scripts/train_activation_probe.py --activations evals/lane5/activations/ --out-model evals/lane5/probe_linear.pkl`. Logistic regression on activation deltas (768D → 1D; TaskTracker recipe). Cross-val AUC on training set.
3. **M7: Evaluation** (final pass, ~30 min): apply probe to BIPIA indirect test set. Report AUC vs frozen-probe softmax AUC + TPR@FPR=1%.
4. **M7: Writeup**: "Activation probes [do/do not] capture OOD signals beyond softmax; encoder-only detection [has/lacks] hidden multi-level signals."

### Outcome branches
- **Positive** (rare; per F8 framing): Probe AUC > frozen-probe softmax by >0.05. → "Activation space encodes OOD task-drift signal; encoder architectures have untapped capacity."
- **Null** (likely): Probe AUC ≈ softmax AUC ±0.02. → "Softmax probabilities already compress activation-space signals; linear probes add no marginal value. Encoder-only detection is saturated."
- **Negative** (possible): Probe AUC < softmax AUC. → "Activation-space task drift is orthogonal to injection-detection; architectural defenses necessary."

### Test-contracts
- `predictions_persisted`

### Book citation (Ch 12 "Activation-Space Detection — Does Encoder-Only Work?")
"Do encoder activations encode OOD robustness signals missed by classification-head probabilities? Lane 5 applies the TaskTracker linear-probe recipe to frozen-probe ModernBERT, testing whether multi-level representations help. Results show [positive/null/negative outcome]; implications for architectural future work (fine-tuning intermediate layers vs classification-only fine-tuning)."

---

## Consolidated execution roadmap

| Lane | Scope | Duration | Cost | Key Checkpoint | Book Chapter | Expected Outcome |
|---|---|---|---|---|---|---|
| **1** | Direct-injection baseline + Tier B reference scorers | M1 (~3-4d) | $10-12 | Meta PG2 86M AUPRC | Ch 8 | positive/null |
| **1b** | Adversarial robustness (12 char-injection + CourtGuard) | M1 (co-scheduled) | $5-8 | CourtGuard ASR reduction | Ch 8 sidenote | null |
| **2** | Indirect-injection training + 2-variant loss ablation | M2-M4 (~4-5w) | $156-196 base + $34 opt | RFPR pooled OOD AUPRC | Ch 9 | null (expected) |
| **3** | Spotlighting structural defense | M5 (~2-3d) | $1 API | Datamarking variant AUPRC | Ch 10 | null |
| **4** | Fusion + embedding-scorer + APR metric | M6 (~2-3w) | $5-30 | Stacker AUPRC + APR curves | Ch 11 | positive/null |
| **5** | Activation-space probing (validation-only) | M2 + M7 (~2-3d) | $10-20 | Probe AUC vs softmax | Ch 12 | null |
| **Total** | **All lanes** | **M0-M7 (~13-14w)** | **~$230-280 base** | **5 HF Hub checkpoints** | **6 chapters locked** | **Execution complete** |

### Cost scenario matrix (per plan §16)
- **Base only**: $230-260 realized (within $250 base)
- **Base + Tier B** (CourtGuard + Meta PG2 + embedding-scorer): included above
- **Base + Tier C #1** (PromptShield Llama-3.1-8B Lane 1): +$40-50 (gated unlock)
- **Base + Tier C #2** (energy-loss Lane 2): +$34 (gated unlock)
- **All Tier C**: $304-354 (within $350 hard cap with contingency)
