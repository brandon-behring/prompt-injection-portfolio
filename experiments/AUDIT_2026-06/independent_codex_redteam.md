**Overall:** the memo is mostly fair on the big axis-separation argument, but **not safe to act on as-is**. It has one clear factual error: A5/arXiv is verifiable and real. It also overstates a few supporting claims.

| Claim checked | Verdict | Evidence |
|---|---|---|
| Prototype measured direct-trained detectors on cross-family OOD, not BIPIA-internal attack-type LODO. | Confirmed | Prototype training/OOD sources: `prototype/WRITEUP_PAPER.md:132-137`; pooled OOD composition/floor: `prototype/WRITEUP_PAPER.md:203-211`; AUPRC table: `prototype/RESULTS.md:89-96`. |
| Portfolio modeling is BIPIA-internal. | Confirmed | `experiments/attack-type-lodo/harness.py:62-63`; `experiments/eda/OOD_WALL_PREDICTION/criteria.md:112-118`; carrier-LODO uses email/code/table only: `experiments/carrier-lodo/criteria.md:50-53`. |
| A.1 LoRA falsification numbers and pre-registration integrity. | Confirmed | `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md:71-81`, `:94-96`; audit reproduction: `experiments/AUDIT_2026-06/verification_report.md:15-34`. |
| A.1 “all per-type AUPRCs sit near 0.98–0.999.” | Overstated | Actual `lora` per-type AUPRCs are **0.956–0.984**, not 0.98–0.999: `experiments/eda/OOD_WALL_PREDICTION/falsification_verdict.json:50-65`. |
| A.1 ceiling-compression critique is statistically valid. | Confirmed | The gate is algebraically a test on per-type AUPRC **levels**: `criteria.md:174-182`; with no-skill floor around 0.926 and values near the upper bound, headroom is limited. But use the corrected 0.956–0.984 range. |
| A.1 within-corpus scope critique. | Confirmed | Core fold holds scenario set constant, so “only shift is attack type”: `docs/planning/attack-type-lodo-harness-spec.md:27-35`. |
| A.2 Carrier-LODO result is fairly characterized as capacity-attenuated, table-residual. | Confirmed | `experiments/carrier-lodo/FINDINGS.md:3-7`, `:15-24`, `:56-62`. |
| A2 axis-conflation claim: ADR-055 maps prototype wall onto carrier/direct→indirect too loosely. | Confirmed | ADR-055 says prototype measured “carrier / direct→indirect”: `decisions/ADR-055-...md:24-26`; prototype actually bundles direct→indirect, cross-dataset, and multi-family slate: `prototype/WRITEUP_PAPER.md:132-137`, `:287-297`; carrier-LODO isolates only BIPIA carriers: `experiments/carrier-lodo/criteria.md:50-53`. |
| A.3 frozen-MiniLM geometry scope. | Confirmed | Geometry is MiniLM/frozen-embedding-specific: `FINDINGS.md:27-33`; LoRA later detects types strongly: `FINDINGS.md:77-92`. |
| A.4 “scope-blindness” is argued/mechanistic, not fully demonstrated. | Confirmed | V10 shows direct-trained probes fail while PG1 fires: `FINDINGS.md:41-48`; `v10_scores.json:13-16`, `:71-76`; but mechanism label still goes beyond the measured score distributions. |
| A.5 cross-family fair-tuned capacity question is open. | Confirmed | Prototype LoRA is the only fine-tuned cross-family number and is confounded/discarded by portfolio: `decisions/ADR-052-...md:16-20`; prototype LoRA AUPRC/AUROC: `prototype/RESULTS.md:91-95`, `:277-282`; no portfolio fair-tuned direct→indirect cross-family rerun found. |
| A.5 “clean frozen probe at chance / no signal” phrasing. | Overstated | AUPRC is below/random-floor: `prototype/RESULTS.md:91-96`; but frozen AUROC is **0.515 [0.505, 0.525]**, a tiny but statistically above-floor signal: `prototype/RESULTS.md:277-282`. Phrase as “no useful AUPRC signal,” not absolute “no signal.” |
| A5 arXiv:2602.14161 unverifiable / flagged-open. | Wrong | The paper is real: [arXiv:2602.14161](https://arxiv.org/abs/2602.14161). It reports **8.4pp AUC inflation** in the abstract and Table 1: [HTML lines 223-232](https://arxiv.org/html/2602.14161v1). The local cached PDF text reports **96.6%** dataset-identity accuracy: `docs/research/training-and-evaluation/papers/fomin2026benchmarkslie.pdf` via extracted text lines 443-445. Local KB already has it verified: `docs/research/training-and-evaluation/agent_index/05_ood_methodology_reproducibility.md:5-12`, `bib_ledger.yml:953-975`. |
| Memo missed stale V10 limitation. | Missed-by-memo | `FINDINGS.md` says V10 is now complete and PG1 added: `:41-48`, but still says “V10 is incomplete pending PG1”: `:62`. |
| Memo missed “science question settled” overclaim in program review. | Missed-by-memo | `program-review-2026-06.md:15-29` says the science question is settled, but A.5 correctly says fair-tuned cross-family capacity remains open. |
| Memo missed overconfident full-FT monotonicity language. | Missed-by-memo | ADR-054 says full-FT “would only dissolve the wall further”: `decisions/ADR-054-...md:78-82`; program review repeats “more capacity can only dissolve”: `program-review-2026-06.md:83-86`. Full-FT was not measured. |

**Required corrections**

1. Replace A5 with: arXiv:2602.14161 is verified and reports the 8.4pp AUC inflation plus 96.6% dataset separability. Keep a caveat that “↔” should not imply a proven causal equivalence.
2. Fix A.1’s numeric premise to `0.956–0.984`, while keeping the ceiling-compression critique.
3. Qualify A.5 “no signal” as AUPRC-floor-specific; frozen AUROC has a tiny above-floor signal.
4. Add the missed stale V10 limitation and program-review/full-FT overclaim fixes.
5. Keep the main conclusion: **cross-family fair-tuned capacity remains open**. That part is logically sound.