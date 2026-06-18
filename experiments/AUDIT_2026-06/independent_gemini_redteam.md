Based on an adversarial read-only review of the prototype and portfolio artifacts, here is the verification of the memo’s claims. 

### Claim Verification

**1. Claim A.5: The cross-family wall under fair tuning is Open**
* **Claim:** The portfolio correctly diagnosed the prototype's LoRA run as confounded and pivoted to a BIPIA-internal attack-type study, but because it discarded the prototype's cross-family LoRA run, the symmetric question—whether *fair-tuned capacity* climbs the cross-family (direct→indirect) wall—was never actually tested.
* **Verdict:** **Confirmed**.
* **Evidence:** `prototype:RESULTS.md` establishes the cross-family failure using both a frozen probe and a LoRA fine-tune. `portfolio:decisions/ADR-052.md` rightly rejects the prototype's LoRA result due to methodological confounds (untuned recipe, frozen pre-head) and explicitly pivots the study to "indirect→indirect" using BIPIA's native split. Because the portfolio never executed a de-confounded LoRA re-run on the original direct→indirect cross-family axis, the memo's logic is flawlessly sound: the capacity question on that specific axis remains untested.

**2. Claim A.1: Ceiling-compression critique**
* **Claim:** The falsification of the attack-type wall (`T -> 0`) at the LoRA rung is partially a mechanical saturation artifact because all test-type AUPRCs sit at `0.98–0.999`. 
* **Verdict:** **Confirmed**.
* **Evidence:** `portfolio:experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md:71-81` confirms the test AUPRCs for LoRA are universally `0.98-0.999`. Because the `T` statistic is defined as the top-k minus bottom-k AUPRC, and AUPRC is mathematically bounded at 1.0, the test statistic is mechanically forced to compress toward 0 as performance saturates the ceiling. The memo's statistical critique that this reflects "uniform near-ceiling detection as much as a dissolved gap" is completely valid.

**3. Claim A4: Argued-not-measured ("frozen > LoRA is a mirage")**
* **Claim:** The assertion that "frozen > LoRA is a mirage" is sound reasoning based on recognized confounds, but it was argued rather than empirically measured on the cross-family axis.
* **Verdict:** **Confirmed**.
* **Evidence:** `portfolio:docs/planning/prototype-postmortem.md:42` dismisses the "frozen > LoRA" finding as a "mirage between two sub-random detectors." It justifies this dismissal based on the confounds listed in ADR-052. However, as established in A.5, the portfolio never actually ran a fair, unconfounded cross-family LoRA to prove this empirically.

**4. Claim A2: Axis-conflation**
* **Claim:** Mapping the prototype's wall onto the "carrier axis" conflates the prototype's cross-dataset shift with the portfolio's within-BIPIA container shift.
* **Verdict:** **Confirmed**.
* **Evidence:** `portfolio:decisions/ADR-055-post-m1-re-ladder-multi-axis-spine.md` maps the submission's wall to the carrier axis. However, the prototype (`RESULTS.md`) evaluated cross-family generalization across entirely distinct datasets (BIPIA, InjecAgent, JBB). In contrast, the portfolio's carrier-LODO (`experiments/carrier-lodo/FINDINGS.md`) evaluates only across email/code/table *within* the single BIPIA dataset. Using a within-corpus result to stand in for a cross-dataset question is an axis conflation.

**5. External Citation A5: arXiv:2602.14161**
* **Claim:** The citation `arXiv:2602.14161: 96.6% separability ↔ 8.4pp drop` cannot be confirmed by a research-kb auditing search.
* **Verdict:** **Confirmed (and understated)**.
* **Evidence:** Web searches for "2602.14161" return absolutely no results. More damningly, `portfolio:docs/planning/prototype-postmortem.md:48` explicitly flags the "8.4pp benchmark inflation" figure as an orphan with *"no derivation in either repo."* It appears this orphan statistic was improperly legitimized in the portfolio by attaching a fabricated arXiv citation to it (seen in `experiments/eda/OOD_WALL_PREDICTION/criteria.md:45` and `lane-1/hypothesis.md:53`). The memo was right to flag it, but too gentle in its diagnosis.

### Missed Issues

* **Model Mismatch in Geometry Claims (A.3 extension):** The memo accurately flags that the carrier-dominance geometry (Silhouette/ARI) applies only to the *frozen* embedding, but it misses a secondary mismatch. The geometry was calculated using `all-MiniLM-L6-v2`, but the actual frozen-probe detector was evaluated using `ModernBERT-base`. `lane-1/hypothesis.md:64-66` admits "The geometry claim... was not recomputed on ModernBERT." The memo should have flagged this model mismatch alongside the "frozen" qualifier.

### Overall Judgment

**The memo is safe to act on as-is and represents an exceptionally sharp, fair, and methodologically rigorous self-audit.** It successfully and accurately identifies areas where the portfolio's narrative (axis shifting, ceiling effects, unmeasured claims) outran its actual empirical measurements. It is not self-serving; it holds the portfolio to a punishingly high standard of evidence.

**Corrections Required to the Memo:**
1. **Apply Draft Patches 1 & 2** as proposed in the memo; they are accurate and necessary.
2. **Upgrade the A5 fix:** Change the prescribed fix from "verify arXiv (one step)" to "remove the fabricated arXiv citation and the 8.4pp claim entirely." The citation does not exist, and it is laundering an orphan statistic.
3. **Add the Model Mismatch qualifier to A.3:** Update the punch-list to require noting that the frozen embedding geometry was calculated on `MiniLM`, not the `ModernBERT` backbone used in the actual detector.
