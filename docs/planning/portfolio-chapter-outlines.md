# Portfolio Book Chapter Outlines (13 chapters)

**Companion to** `~/.claude/plans/i-want-to-consider-merry-milner.md` §19.
Produced during 2026-05-19 round-7 holistic review (focus area #1: book pedagogy + 13-chapter outline refinement).

Note: full per-chapter KF-decomposed detail (R/O/E structure, callout strategy, citation density) was generated as a ~70KB analysis. This document captures the **concise summary table + per-part narrative arc**. The original detailed analysis is preserved in a local Claude Code transcript artifact (28K tokens; author-local, not in the repo; read in chunks if needed at M0 chapter authoring).

---

## Pedagogical foundation (scaffold v3.0 academic profile per Round 6 Q2''''')

- **KF triadic chapter shape** per scaffold pedagogy/kf-chapter-shape.md:
  - **Representation (R)**: entity/phenomenon the chapter handles — what is it?
  - **Operation (O)**: how methodology engages with R — what do we do with it?
  - **Evolution (E)**: how R or O changed over time / through experiments — what's the trajectory?
- **Volatility classes** per scaffold pedagogy/volatility-classes.md:
  - `stable-principle`: definitions, math, threat models
  - `architectural-pattern`: methodology choices, ADRs
  - `feature-surface`: per-lane experiment results, benchmark numbers
- **Source tiers** per scaffold pedagogy/source-tiers.md:
  - T1-official (peer-reviewed papers, OWASP/MITRE), T2-release (HF model cards), T3-practitioner (blog posts), T4-conjecture
- **18 callouts available** (scaffold v3.0 academic profile): SkillBox / CaseStudy / ConceptBox / KeyIdea / TryThis / Recovery / Convergence / Divergence + NoteBox / ExampleBox / DynConnect / InsightBox / WarnBox / CounterBox / TipBox / OpenQuestion / PaperBox / ResultBox
- **7-state freshness machine** per Round 5 Q2'''': implemented / chapter_only / reading_only / prose_only / code_only / scaffolded / planned

---

## Part I — Representation: What a prompt-injection classifier is, and isn't (Ch 1-3)

**Narrative arc**: Establish the *what*. Define the threat model, the binary-classification framing, the metrics that matter. Reader learns enough to evaluate later experimental claims. Heavy on `ConceptBox` + `KeyIdea` callouts; medium citation density (3-5 per chapter).

### Ch 1: Prompt-Injection Detection as a Classification Problem

| Field | Value |
|---|---|
| **Thesis** | A detector is a binary classifier over the input space; design constraints derive from the geometry of attacks. |
| **R** | Prompt injection as a phenomenon: threat model (direct vs indirect), input/output invariants (token sequences, context windows), prevalence across domains |
| **O** | How we formalize detection: threat taxonomy (16-18 techniques per Lane 1b matrix), binary-classification framing, single-class metrics (TPR@FPR), AUPRC/AUROC on slices |
| **E** | Evolution from "jailbreaks" (2022) → "prompt injection" (OWASP 2023) → "indirect attacks" (2024-25). Convergence on multi-vector threat models; divergence on detection framing |
| **Callouts** | ConceptBox (threat-model definition), KeyIdea (binary-class framing is load-bearing), CaseStudy (**SDD ADR-018 label-corruption** — Round 7 Tier B citation: deepset loader silently destroyed 343 benign rows), Recovery (over-defense pitfall) |
| **Citations** | Greshake et al. 2023 (indirect injection); OWASP LLM01:2025; MITRE ATLAS prompt-injection taxonomy; **SDD ADR-018** + dossier `claim_family=injection_threat_model` |
| **Volatility** | `stable-principle` (definitions) |
| **Freshness state at v0.1.0** | `scaffolded` (skeleton + R section drafted) |
| **Cross-references** | Lane 1 protocol.md (eval slate); Lane 1b protocol.md (12-technique attack surface) |
| **Failure-branch prose** | N/A (definitional chapter) |

### Ch 2: Six Attack Types + Train/Test Composition is Fate

| Field | Value |
|---|---|
| **Thesis** | Train/test data composition determines achievable AUPRC ceilings; 6 attack-type taxonomy (5 from WRITEUP §1.5 + character-injection as 6th class per Lane 1b) anchors the design space. |
| **R** | Direct / indirect / agentic-flow / jailbreak-as-question / FP-probe + character-injection (Round 7 Lane 1b addition) |
| **O** | LODO methodology; cross-source disjoint splits per ADR-016; contamination signature detection (**V4 finding** — Round 7 Tier B citation: ~8.4pp aggregate AUC inflation random vs source-disjoint LODO) |
| **E** | From single-source PoCs (V0/V3) to LODO-discipline (V4) to backbone-invariance (submission v1.1.2 DeBERTa null) |
| **Callouts** | ConceptBox (LODO definition), KeyIdea (composition determines ceiling), **CaseStudy (V4 contamination signature)**, OpenQuestion (multilingual coverage deferred) |
| **Citations** | WRITEUP §1.5 attack taxonomy; ADR-016 LODO; **V4 Fomin 2025 contamination signature**; dossier `claim_family=lodo_methodology` |
| **Volatility** | `architectural-pattern` (methodology choice) |
| **Freshness state at v0.1.0** | `scaffolded` |
| **Cross-references** | Lane 1 (BIPIA-direct), Lane 1b (12 char-injection × N detectors), Lane 2 (indirect-augmented training data) |

### Ch 3: What Honest OOD Means + NotInject's Over-Defense Lesson

| Field | Value |
|---|---|
| **Thesis** | OOD evaluation requires source-disjoint splits AND held-out benchmark suites (NotInject, PINT, PromptShield); over-defense is a first-class failure mode. |
| **R** | OOD vs IDD; single-class slices (val-fixed TPR per ADR-027); NotInject as over-defense probe |
| **O** | Eval slate: BIPIA-full + AgentDojo + InjecAgent + NotInject + LLMail-Inject 5K + PINT-EN 3016. **TPR@LowFPR reporting per ADR-036** (1%, 0.5%, 0.1%, 0.05% FPR). Benchmark integrity audit per ADR-038. |
| **E** | From AUC-only reporting → PromptShield's TPR@LowFPR forcing function (2024-25) → APR metric (Meta PG2 utility-aware framing) |
| **Callouts** | ConceptBox (OOD/IDD definition), KeyIdea (TPR@LowFPR is the forcing function), CaseStudy (NotInject over-defense gap: ProtectAI v2 <60%), Convergence (PromptShield 2025 + InjecGuard 2024 both emphasize low-FPR), TryThis (run notebook Ch 5 bootstrap walkthrough) |
| **Citations** | Jacob et al. arXiv 2501.15145 PromptShield; Li et al. arXiv 2410.22770 InjecGuard NotInject; Lakera PINT benchmark; dossier `claim_family=ood_evaluation_methodology` |
| **Volatility** | `stable-principle` (eval methodology principles) |
| **Freshness state at v0.1.0** | `scaffolded` |
| **Cross-references** | All Lanes (eval slate); Ch 5 (bootstrap walkthrough notebook) |

---

## Part II — Operation: Building the prototype's instrument (Ch 4-6)

**Narrative arc**: Establish the *how*. Build the methodology toolkit: rung ladder, statistical apparatus, threshold policy. Reader learns enough to reproduce. Heavy on `SkillBox` + `TryThis` + `Recovery` callouts; high citation density (5-7 per chapter); paired with selective T3 notebooks (Ch 5 bootstrap, Ch 6 threshold-policy).

### Ch 4: The Rung Ladder as Instrument

| Field | Value |
|---|---|
| **Thesis** | The rung ladder (frozen-probe → LoRA → full-FT → reference scorers) is a methodology instrument, not a leaderboard. Pretraining does ~68% of the work (**V0 finding** — Round 7 Tier B citation). |
| **R** | Submission's rung ladder: TF-IDF + LR → ModernBERT frozen-probe → LoRA → ProtectAI v1/v2 reference. Now extended with Meta PG2 86M (Lane 1 Tier B). |
| **O** | Frozen-probe vs LoRA paired-bootstrap delta; per ADR-052: LoRA -0.071 AUPRC on pooled OOD (CI clears zero); active-harm framing. |
| **E** | V0 rung decomposition: pretraining +0.054 / LoRA +0.043 on test_id; locked holdout +0.210 / +0.099 → **pretraining does ~68% of work** (Round 7 Tier B citation). Backbone-invariance per v1.1.2 DeBERTa null. |
| **Callouts** | SkillBox (rung-ladder construction recipe), KeyIdea (pretraining dominates), **CaseStudy (V0 rung decomposition)**, Recovery (when fine-tuning hurts: ADR-052), PaperBox (Liu NeurIPS 2020 energy-based loss; optional Lane 2 Tier C), TryThis (Ch 5 bootstrap walkthrough notebook) |
| **Citations** | ADR-017/019 rung methodology; ADR-052 LoRA active-harm; **V0 rung decomposition finding**; v1.1.2 ADR-060 DeBERTa null; dossier `claim_family=rung_ladder` |
| **Volatility** | `architectural-pattern` |
| **Freshness state at v0.1.0** | `scaffolded` |
| **Cross-references** | Lane 1 (rung ladder eval), Lane 2 (variant retraining), Lane 5 (activation probe) |

### Ch 5: The Statistical Apparatus

| Field | Value |
|---|---|
| **Thesis** | Paired-bootstrap CIs + pre-registered stopping rules (**V4 finding**) protect against regression-hiding; "Are Firewalls All You Need?" critique (Bhagwatkar 2025) sidenote on benchmark-saturation risk. |
| **R** | Bootstrap apparatus: 10K resamples per ADR-022; BCa 95% CI; paired-bootstrap delta; multi-seed stability (n=2 minimum) |
| **O** | **Companion notebook (T3 per Q5'/Round 5)**: `book/src/content/notebooks/ch05_bootstrap_walkthrough.{py,ipynb}` — adjustable seeds, CI shape across resample counts |
| **E** | From AUC point-estimates → BCa-corrected paired-bootstrap → **V4's pre-registered stopping rule** (Round 7 Tier B citation: V4.1 rejected Phase B-α because Δ-CI overlapped zero on test_id [-0.271, +0.003]) |
| **Callouts** | SkillBox (compute paired-bootstrap delta CI in 5 lines), KeyIdea (CIs replace p-values), **CaseStudy (V4 stopping rule)**, **WarnBox/CaseStudy "Are Firewalls All You Need?" sidenote** — Bhagwatkar et al. NeurIPS 2025 arXiv 2510.05244 saturates 4 agentic benchmarks with simple two-firewall defense, TryThis (rerun notebook with different seeds) |
| **Citations** | Efron & Tibshirani 1993 bootstrap; ADR-022 bootstrap methodology; **V4_1_RESULTS.md §7A.7 stopping rule**; **Bhagwatkar 2025 firewalls critique**; dossier `claim_family=bootstrap_methodology` |
| **Volatility** | `stable-principle` (methodology) |
| **Freshness state at v0.1.0** | `scaffolded` |
| **Cross-references** | All Lanes (CI apparatus); companion notebook |

### Ch 6: Dual-Policy Thresholds + val→OOD Transfer Failure

| Field | Value |
|---|---|
| **Thesis** | Threshold policy is where submission's calibration broke; val-fixed TPR transfer fails when OOD distribution shifts. **Companion notebook**: `ch06_threshold_policy.{py,ipynb}` — reader picks FPR target, sees corresponding TPR + threshold, explores val→test drift. |
| **R** | Dual-policy thresholds per ADR-025; detection vs verification operating points |
| **O** | val-fixed TPR application via `eval_toolkit.operating_points.apply_operating_points`; single-class slate convention per ADR-027 (submission-enforced upstream) |
| **E** | From single-threshold reporting → dual-policy (detection + verification) → val→OOD transfer failure → **APR metric framing per ADR-037** (utility-aware threshold selection) |
| **Callouts** | ConceptBox (operating point definitions), SkillBox (threshold-policy recipe), Recovery (val→test threshold drift; submission threshold-policy.md case), KeyIdea (single-class slices need val-fixed TPR), TryThis (notebook walkthrough) |
| **Citations** | ADR-025 dual-policy; ADR-027 single-class metric; ADR-037 APR metric; PromptShield Llama-3.1-8B threshold paper; dossier `claim_family=threshold_policy` |
| **Volatility** | `architectural-pattern` |
| **Freshness state at v0.1.0** | `scaffolded` |
| **Cross-references** | Lane 1 (threshold transfer), Lane 4 (APR + utility-aware stacker thresholds), companion notebook |

---

## Part III — Evolution: The wall, quantified and climbed (Ch 7-12)

**Narrative arc**: The *what changed*. Six experimental chapters: one anchor (Ch 7) + five lane chapters (Ch 8-12). Each Part III chapter ends with Convergence/Divergence + outcome-branch prose. Heavy on `CaseStudy` + `ResultBox` + `Convergence`/`Divergence` callouts; very high citation density (7-10 per chapter); paired with T3 notebooks where applicable.

### Ch 7: The OOD Wall + EchoLeak Case Study Anchor

| Field | Value |
|---|---|
| **Thesis** | Submission's headline finding (LoRA -0.071 AUPRC vs frozen-probe on OOD per ADR-052) + v1.1.2 DeBERTa null result (chunk_and_average 0.2912 ≈ head_truncation 0.2895) demonstrate the OOD wall is **backbone-invariant**. EchoLeak (CVE-2025-32711, June 2025) is the real-world manifestation. |
| **R** | The OOD wall: LoRA on direct-injection-heavy LODO data made indirect/agentic OOD AUPRC *worse* than frozen-probe |
| **O** | Two foundations: (1) submission ADR-052 LoRA active-harm + (2) v1.1.2 DeBERTa null result. Plus **EchoLeak case study anchor** — 0-click M365 Copilot indirect-injection (bypassed XPIA classifier + link redaction + CSP). |
| **E** | From "OOD wall as data choice" (v1.0.x ADR-050) → "active-harm methodology" (v1.0.3 ADR-052) → "backbone-invariance" (v1.1.2 DeBERTa null) |
| **Callouts** | **CaseStudy: EchoLeak** (CVE-2025-32711; first 0-click indirect-injection in production), KeyIdea (OOD wall is backbone-invariant per v1.1.2), **CaseStudy: ADR-052 active-harm** (-0.071 AUPRC CI clears zero), ResultBox (v1.1.2 DeBERTa table), Divergence ("Are Firewalls All You Need?" critique sidenote already in Ch 5), OpenQuestion (data-bound vs structural — to be answered by Lanes 2 + 5) |
| **Citations** | ADR-050/052; v1.1.2 ADR-060/063; EchoLeak Aim Labs disclosure June 2025 (CVE-2025-32711); Greshake et al. 2023; Bhagwatkar 2025; dossier `claim_family=ood_wall + claim_family=production_incidents` |
| **Volatility** | `feature-surface` (specific results; ages quickly) |
| **Freshness state at v0.1.0** | `scaffolded` (anchors EchoLeak + submission ADRs at skeleton; results filled at M1 close) |
| **Cross-references** | All subsequent Part III chapters trace back here |

> **Round 30 re-axis (ADR-055).** The anchor reframes from a single "backbone-invariant OOD wall" to the **multi-axis, capacity-dependent** spine: the submission's backbone-invariant null is the **carrier** axis; M1 adds the **attack-type** axis, where the per-type wall is **capacity-dependent** (FALSIFIED at the LoRA ceiling; SURVIVES tfidf/frozen). The OpenQuestion ("data-bound vs structural") is now axis-typed — the *attack-type* wall is not structural (capacity dissolves it); the *carrier* wall is **partially capacity-resistant (provisional, n=3), residual at table — and data-resistant at the ceiling** (C1 carrier/table training `NOT-CLOSED`, 2026-06-11; ADR-055 amendment) — the carrier-LODO M2 pre-flight gate resolved it `SMALL-THROUGHOUT` (ADR-055). backbone-invariant ≠ capacity-invariant.

### Ch 8: Lane 1 — Reading the OOD Wall, More Carefully

| Field | Value |
|---|---|
| **Thesis** | Direct-injection detection is NOT the limiting factor for ModernBERT-base; the wall emerges when attacker controls trust boundary. Lane 1 + Lane 1b results control for backbone choice; Lane 1b sidenote on character-injection adversarial robustness. |
| **R** | Direct-injection baseline + Tier B reference scorers (ProtectAI v1/v2 + Meta PG2 86M); optionally PromptShield Llama-3.1-8B (Tier C #1 if unlocked) |
| **O** | T0 portfolio-clean eval-from-hub + reference scorer batch + metrics battery + bootstrap CI; **TPR@LowFPR reporting per ADR-036** |
| **E** | If positive (likely): backbone-invariance confirmed across encoders. If null: all encoders saturate near 0.30-0.37 AUPRC. If negative: Lane 2 indirect data may not compensate. |
| **Callouts** | ResultBox (per-scorer AUPRC + TPR@LowFPR table), CaseStudy (Meta PG2 86M state-of-the-art per compass), ConceptBox (Tier B vs Tier C reference scorers), **CounterBox / Convergence on Lane 1b 12-technique adversarial-robustness sidenote** (per Round 6 Q4 lane 1b breadth lock), Divergence (PromptShield Tier C contingency unlock vs base detectors) |
| **Citations** | Compass §2 detector landscape; Meta PG2 model card; ProtectAI v1/v2; **Lane 1b: Bypassing arXiv 2504.11168**; **Lane 1b CourtGuard: Sun arXiv 2510.19844** (Round 7 Tier B); dossier `claim_family=direct_injection + claim_family=adversarial_robustness` |
| **Volatility** | `feature-surface` |
| **Freshness state at v0.1.0** | `planned` → `prose_only` at M1 close → `implemented` after Lane 1 ratification |
| **Cross-references** | Lane 1 + Lane 1b experiment records; Ch 7 (foundation); Ch 11 (fusion uses Lane 1 scores) |

> **Round 30 re-axis (ADR-055).** Ch 8 now headlines M1's **pre-registered §6.5 falsification** as the chapter's result: the attack-type-LODO per-type "wall" is **capacity-dependent** (T = +0.135 tfidf / +0.082 frozen / −0.003 lora; FALSIFIED on `lora`, SURVIVES cheap rungs). The "E" branch ("backbone-invariance confirmed across encoders") is re-axised — M1 varied *capacity*, not backbone; the finding is that end-to-end LoRA dissolves the attack-type gap (test AUPRC 0.98–0.999), a capacity-axis result distinct from (and consistent with) the carrier-axis backbone-invariance.

### Ch 9: Lane 2 — Climbing with New Training Data

| Field | Value |
|---|---|
| **Thesis** | Does indirect-injection training data + Recall@LowFPR loss overcome BOTH active-harm + backbone-invariance? **3-way pre-commitment**: positive (data-bound wall) / null (structural wall) / negative (worsened distribution shift). |
| **R** | Synthetic indirect-injection corpus (Sonnet + Opus audit) + 2-variant ablation (CE baseline + Recall@LowFPR per Meta PG2 recipe) |
| **O** | Sonnet synthesis ($88-128 API) + 2-variant retrain ($68 GPU). **Optional Tier C #2 3rd variant**: energy-based loss ($34 gated). |
| **E** | If RFPR pooled OOD AUPRC ≥0.40 with CI clear of zero → wall is data-bound. If clusters near 0.36 ± 0.02 → residual table-carrier wall (per ADR-055 carrier-LODO `SMALL-THROUGHOUT`). If drops below 0.32 → indirect augmentation induces distribution shift. |
| **Callouts** | KeyIdea (data-bound vs structural framing), **CaseStudy: Lane 2 attribution table** (3-row: CE-direct only / CE-mixed / RFPR-mixed), ResultBox (per-variant per-slice grid), OpenQuestion (energy-loss Tier C contingency), Divergence (if results contradict ADR-052) |
| **Citations** | ADR-052 active-harm baseline; ADR-060 DeBERTa methodology; Meta PG2 RFPR loss recipe (compass §2.1); Liu NeurIPS 2020 energy-based loss (Tier C reference); dossier `claim_family=indirect_injection_training` |
| **Volatility** | `feature-surface` |
| **Freshness state at v0.1.0** | `planned` → `prose_only` at M4 close → `implemented` |
| **Cross-references** | Lane 2 experiment records; Ch 7 foundation; Ch 11 (Lane 2 variants feed Lane 4 stacker) |

> **Round 30 re-axis (ADR-055).** Lane 2's headline evaluation axis moves from attack-type to **carrier generalization** (method unchanged — LoRA + 2-variant loss per ADR-043). The thesis ("does indirect data overcome active-harm + backbone-invariance") re-axises to "can training data close the **carrier**-axis OOD gap M1 left **partially standing** — `SMALL-THROUGHOUT`, with a residual **table** wall to close (provisional, n=3; ADR-055)," sized first by the carrier-LODO M2 pre-flight gate. The E-branches re-axis to the carrier wall (the *attack-type* wall is capacity-solved). "Confirm attack-type generalization" is a cheap optional secondary. *[First Lane-2 datum 2026-06-11 (C1): the synthetic format-matched recipe returned `NOT-CLOSED` — the table wall is data-resistant at the ceiling (ADR-055 amendment); the carrier-diverse real-data variant this chapter outlines remains the open H-branch frame, and the row-E criterion inherits the C1 anchor.]*

### Ch 10: Lane 3 — Watching the Wall in the Demo

| Field | Value |
|---|---|
| **Thesis** | Structural marking (Spotlighting: delimit + datamark + base-64 encoding) is proven to reduce LLM ASR; does it improve detection AUPRC? Interactive HF Space demo lets reader watch frozen-probe respond to spotlighted vs raw indirect injection. |
| **R** | Spotlighting variants applied at inference-time to BIPIA indirect + InjecAgent + LLMail-Inject test set |
| **O** | 3 transformations × frozen-probe + LoRA; HF Space deployment with toggle for delimit / datamark / encoding modes |
| **E** | If +0.05-0.10 AUPRC lift → marking helps; if ≤0.02 → encoder doesn't leverage trust-boundary signals (likely); if negative → truncation loses signal |
| **Callouts** | **TryThis (HF Space interactive demo)**, KeyIdea (Spotlighting is LLM-targeted not detection-targeted), Recovery (encoding variant likely fails for short-context detectors), ResultBox (per-variant AUPRC delta), Convergence (Hines 2024 Spotlighting validates as defense) |
| **Citations** | Hines et al. arXiv 2403.14720 Spotlighting; Azure Document Shield Build 2025 GA; compass §7 structural defenses; dossier `claim_family=structural_defenses` |
| **Volatility** | `feature-surface` |
| **Freshness state at v0.1.0** | `planned` → `prose_only` at M5 close |
| **Cross-references** | Lane 3 experiment record; HF Space link; Ch 11 (Spotlighting + detection + output filter = practical deployment) |

### Ch 11: Lane 4 — Score Fusion + Adaptive Evaluation

| Field | Value |
|---|---|
| **Thesis** | Multi-detector fusion (logistic stacker + embedding-based meta-learner from CodeIntegrity approach) tests whether complementary signals exist across detectors; APR metric reveals utility-security frontier. |
| **R** | Stacker inputs: per-row scores from all prior Lane rungs (frozen-probe + LoRA + ProtectAI v1/v2 + Meta PG2 86M + Lane 2 indirect-ce/rfpr + CourtGuard consensus) |
| **O** | Logistic regression stacker on 500 labeled rows + XGBoost on OpenAI text-embedding-3-small (Round 7 Tier B embedding-scorer); **APR metric reporting per ADR-037** at 1% / 3% / 5% utility-loss thresholds |
| **E** | If stacker AUPRC > best individual by >0.03 + APR @ 3% utility loss >60% → fusion adds value. If matches best individual ±0.01 → detectors highly correlated; architectural defenses must replace not augment. |
| **Callouts** | ConceptBox (APR metric definition), **CaseStudy: embedding-scorer (CodeIntegrity approach)** per Round 7 Tier B, ResultBox (per-detector + stacker AUPRC + APR table), KeyIdea (fusion's utility frontier), Divergence (stacker overfitting risk on imbalanced data) |
| **Citations** | Ayub & Majumdar arXiv 2410.22284 embedding-based detectors; LLMail-Inject SaTML 2025; Meta PG2 APR metric; compass §3 evaluation methodology; dossier `claim_family=detector_fusion` |
| **Volatility** | `feature-surface` |
| **Freshness state at v0.1.0** | `planned` → `prose_only` at M6 close |
| **Cross-references** | Lane 4 experiment record; all prior Lane experiment records (provide stacker inputs); Ch 13 lessons |

### Ch 12: Lane 5 — Activation-Space Detection (Encoder vs Decoder Methodology Port Test)

| Field | Value |
|---|---|
| **Thesis** | Does TaskTracker's >0.99 ROC AUC activation-probe finding (decoder LLMs) transfer to encoder-only architectures (ModernBERT)? **Validation-only scope** per F8 framing — negative result is informative either way. |
| **R** | Activation deltas (pre vs post untrusted-data injection) from submission's frozen-probe ModernBERT (no fine-tuning) |
| **O** | Linear probe per TaskTracker recipe; trained on submission val + synthetic task-drift pairs; evaluated on BIPIA indirect |
| **E** | If probe AUC > softmax AUC by >0.05 → activation space encodes OOD signal (encoder has untapped capacity). If ±0.02 → softmax already compresses activation signal (encoder saturated). If negative → activation task-drift is orthogonal to injection detection. |
| **Callouts** | OpenQuestion (does encoder-only TaskTracker work?), ConceptBox (activation-delta probe methodology), CaseStudy (Abdelnabi et al. TaskTracker decoder evidence base), ResultBox (probe vs softmax AUC + TPR@FPR=1%), Divergence (architectural mismatch hypothesis vs portfolio's encoder choice) |
| **Citations** | Abdelnabi et al. arXiv 2406.00799 TaskTracker; Microsoft SaTML 2025 toolkit; compass §7 activation-based detection; dossier `claim_family=activation_probes` |
| **Volatility** | `feature-surface` |
| **Freshness state at v0.1.0** | `planned` → `prose_only` at M7 close |
| **Cross-references** | Lane 5 experiment record; Ch 13 lessons (what activation-space results imply for future architectural work) |

> **Round 30 re-axis (ADR-055).** Lane 5's probe hypothesis is sharpened: M1 showed the attack-type signal is **learnable end-to-end** (LoRA, AUPRC 0.98–0.999) **but embedding-invisible** (frozen final-layer silhouette −0.023). The probe question becomes recovering the signal from **intermediate** activations — between the embedding-invisible final layer and the LoRA-visible end-to-end. The M3-entry d′ > 0.5 gate is unchanged (port-only vs surface-third-path / CaMeL capability-isolation).

---

## Part IV — Methodology lessons (Ch 13)

### Ch 13: What the Wall Taught Us (Cross-Cutting Lessons)

| Field | Value |
|---|---|
| **Thesis** | Detection is necessary but architecturally insufficient. Methodology rigor (LODO contamination signature + paired-bootstrap stopping rules + pre-registered hypotheses + freshness-badge claim register) is the durable contribution. **CodeIntegrity 98% post-mortem anchor**: 98% accuracy on historical data ≠ 98% on tomorrow's attacks. |
| **R** | The full portfolio methodology stack: SDD-as-instrument (calibrated, not heavy per Round 2); library-first invariant (4 PyPI deps, no local workarounds); experiment records as primary unit of work; hierarchical depth L0-L5 verification gate; build-in-public cadence |
| **O** | Cross-cutting: what survived submission's experience (SDD discipline); what surfaced new (V0 rung decomposition, V4 contamination signature + stopping rule, SDD label-corruption); what got documented vs deferred to v0.8+ (Tier D items in §16 prioritized roadmap) |
| **E** | From submission v1.0.1 audit-heavy SDD → Round 2 calibrated lighter ADR pattern → Round 6 portfolio as "next version built from submission's experience, done cleaner" → Round 7 Tier A/B/C prioritization framework |
| **Callouts** | **CaseStudy: CodeIntegrity 98% post-mortem anchor** (Jan 2026 vendor self-critique), KeyIdea (detection is necessary but not sufficient), **CaseStudy: V4 contamination signature methodology** (Round 7 Tier B citation), **CaseStudy: SDD label-corruption** (Round 7 Tier B citation; deepset loader silent failure), Recovery (regression-hiding without paired-bootstrap), Convergence (PromptShield 2025 + InjecGuard 2024 + Meta PG2 + this portfolio all align on TPR@LowFPR), OpenQuestion (Tier D v0.8+ candidates) |
| **Citations** | All prior chapters; ADR catalog; dossier comprehensive review; **CodeIntegrity 98% post-mortem**; compass §1 detector reliability critique; dossier `claim_family=methodology_lessons` |
| **Volatility** | `architectural-pattern` |
| **Freshness state at v0.1.0** | `scaffolded` (skeleton + lesson list) → `prose_only` at M7 close |
| **Cross-references** | All chapters; NEXT_SESSION.md (Tier D candidates) |

> **Round 30 re-axis (ADR-055).** Add the durable lesson: the OOD "wall" is **axis-typed and capacity-typed** — not one wall but several axes (attack-type vs carrier), each with its own capacity regime. M1's pre-registered falsification (capacity dissolves the attack-type wall; the carrier wall stands, pending the carrier-LODO gate) is itself a methodology centerpiece: a falsifiable prediction that passed a write-gate at the cheap rungs and was honestly overturned at the LoRA ceiling.

---

## Pedagogical summary

- **Part I (Ch 1-3)**: ~3-5 citations/chapter; `stable-principle` + `architectural-pattern` volatility; heavy ConceptBox + KeyIdea; freshness `scaffolded` at v0.1.0
- **Part II (Ch 4-6)**: ~5-7 citations/chapter; companion T3 notebooks for Ch 5 + Ch 6; SkillBox + TryThis + Recovery emphasis
- **Part III (Ch 7-12)**: ~7-10 citations/chapter; experimental chapters with `feature-surface` volatility; ResultBox + CaseStudy emphasis; freshness progresses `planned` → `prose_only` → `implemented` as lanes close
- **Part IV (Ch 13)**: methodology synthesis; CaseStudy-heavy; cross-cutting Convergence/Divergence; `architectural-pattern` volatility

**Round 7 Tier B citation placement** (per Q1''''''):
- Ch 1 SDD ADR-018 label-corruption ✓
- Ch 4 V0 rung decomposition (pretraining ~68%) ✓
- Ch 5 V4 contamination signature + V4 stopping rule + Bhagwatkar 2025 "Firewalls" critique ✓
- Ch 13 CodeIntegrity 98% post-mortem anchor + V4/SDD/V0 reprise ✓

**Round 7 Tier A reporting requirements**:
- Ch 3 (TPR@LowFPR introduction + APR metric introduction); referenced throughout Part III
- ADR-036 / ADR-037 / ADR-038 cited in Ch 3 sidenotes
