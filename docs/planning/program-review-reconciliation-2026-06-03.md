# Program-review reconciliation — 2026-06-03 (A2)

**Purpose (the write-gate lens for the experiment pre-reg).** The corrected program review
(`program-review-2026-06.tex`) was written mid-Phase-1. This note reconciles it against the current state:
M1 + carrier-LODO (already in the review) and — the substantive part — the **Phase-2 dataset expansion + the
elevated experiment design**, which *postdate* the review. Verdict: the review **holds almost entirely**; one
forward path (Critical #1) is **upgraded, not contradicted** — the windfall realized something the review
explicitly anticipated.

## A. Still holds — no change
- **M1 attack-type FALSIFIED at LoRA** (capacity-dependent) + both caveats — ceiling-compression (a bound, not
  a refutation) and within-corpus. Verbatim-valid.
- **Carrier-LODO SMALL-THROUGHOUT** (G frozen +0.167 → lora +0.067; residual **table** +0.205, n=3 provisional).
- **The axis-scoping** — attack-type + carrier are *within-BIPIA*; cross-family is *across datasets* and **OPEN**.
- **V10 off-the-shelf** — ProtectAI AUROC 0.44 (scope-blind), PG1 0.97 (indirect-capable); the softened
  "consistent-with-scope-blindness" wording.
- **A1–A8 record-fixes** (drafted, ratification-gated); the **ADR-055 amendment** (Appendix) — both unchanged by
  Phase-2 (they concern M1/carrier-LODO, not the new datasets).
- **Budget posture** (~$2 of the $250 base; $100 contingency untouched) and the **forward-path structure** +
  the **Lane-2 upstream blockers** (#22 silent-failure / #23 installability).

## B. Needs update — Phase-2 + this session postdate the review
1. **★ Critical #1 (cross-family re-run) is UPGRADED to a 4-dialect leave-one-INDIRECT-out.** The review
   describes the *single-arm* direct→indirect design (train deepset/Gandalf/Mosscap/HackAPrompt → test
   BIPIA/InjecAgent/JBB/XSTest/NotInject) on the prototype slate. The review's own EDA finding — *"BIPIA is one
   indirect dialect ⇒ a cross-family test must hold out **multiple** indirect corpora"* — is now **satisfied**:
   Phase-2 added **2 new indirect carrier axes** (browsesafe = HTML, fujitsu B1 = RAG-document), and the
   geometry confirms 4 mutually-distinct indirect dialects (PAD-vs-BIPIA 1.94–1.99). The current design (plan
   file **E1–E8**) is therefore **both axes**: (A) the review's direct→indirect arm **+** (B) within-indirect
   **leave-one-out** over {BIPIA, browsesafe, fujitsu, InjecAgent}. This is an *enrichment the review called for*,
   not a contradiction. ⇒ promote it from "Critical #1" to **active Lane 6** (E7).
2. **The "three walls / axes" glossary** gains a refinement: the cross-family axis now decomposes into
   *direct→indirect* (the prototype's wall) **and** *within-indirect dialect-transfer* (the new leave-one-out).
   Frame as corpus-level OOD; cross-reference the within-BIPIA carrier-LODO for carrier-vs-source attribution (E5).
3. **E8 — extend V10's off-the-shelf reading to the new carriers.** The review's V10 is BIPIA-only; the
   experiment adds a frozen **public-detector reference column** (ProtectAI / Prompt-Guard, run-ourselves-only)
   on the new dialects — *does a deployed guard generalize to HTML/RAG indirect, or is it blind there too?*
   (Likely blind, per ProtectAI's 0.44 on BIPIA.) Detector set sourced from the existing **detector-landscape
   atlas** (`docs/research/detector-landscape/`, 67 entries) — which the review's glossary references only via
   ProtectAI/PG1/PG2.
4. **Metric (low-n adaptation).** Keep the review's ROC-AUC Gx + rung ladder, but for the 4-dialect low-n,
   **lead with the per-dialect table + within-fold bootstrap + a permutation test** (the carrier-LODO n=3 lesson
   + DG best-practice), not a cross-fold cluster-bootstrap aggregate.
5. **Budget.** +~$2–5 for the elevated experiment (cheap rungs free + the paid LoRA rung) — still « $250.
6. **New sources to cite** in the eventual write-up: the Phase-2 datasets (ledger "Newly-surfaced 2026-06-03"
   table + `experiments/eda/NEW_SETS_AUDIT/FINDINGS.md`) + the detector-landscape atlas.

## C. Implications for the next steps (A3 / A4 / B1)
- **A3 (ADR-055 amendment):** ratify **as drafted** — Phase-2 doesn't change the carrier-LODO substance. *Add*
  (when the spine is touched): note Lane 6's promotion-to-active + the dialect-transfer axis (B.1/B.2). The
  Appendix's "open choices" (keep prior "standing wall" mentions as pre-resolution record; §16 re-test gate not
  a new Decision; carry "(provisional, n=3)") stand.
- **A4 (A1–A8):** ratify **as-is** — the record-fixes are valid + corroborated by the Phase-2 ledger.
- **B1 (pre-reg):** the review's `criteria.DRAFT.md` (Critical #1) is the *predecessor*; finalize it as the
  **upgraded E1–E8** version (its 7 TBDs + the both-axes leave-one-indirect-out + the metric refinement + E8).
  The write-gate holds: pre-reg locked on this reconciled framing before any datum.

**Net:** the program review is sound and current; the only material change is that its sharpest forward path
(cross-family) has *grown a second axis* from the Phase-2 windfall it anticipated. Nothing in the review is
falsified by Phase-2; the experiment is its upgraded execution.
