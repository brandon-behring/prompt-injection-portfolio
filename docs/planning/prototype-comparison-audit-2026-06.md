# Prototype ↔ Portfolio — Independent Re-Audit (2026-06-02)

> **How to read.** An adversarial-but-fair re-audit of the portfolio's headline results and their
> framing *against* the sibling `prompt-injection-detection-prototype`, written **before the v0.1.0
> public release** as the kind of honesty check the portfolio's own pre-registration ethos demands
> of itself. It is **read-only**: it *proposes* record fixes, applies none; it touches no number, no
> experiment, and no file in the prototype repo.
>
> **Method.** *Re-reason from artifacts.* The arithmetic is the most-audited thing in the repo —
> `experiments/AUDIT_2026-06/` reproduced every headline statistic 5/5, Δ ≤ 1e-4, from raw
> `predictions.parquet`. This audit **accepts those numbers** and re-examines the layer the numeric
> audit could not reach: *interpretation, robustness, scope, and framing* (`program-review-2026-06.md`
> §1.3 concedes the numeric audit "did not catch [a] semantic stretch"). Citations are `file:line`;
> portfolio paths are bare, prototype paths prefixed `prototype:`.
>
> **Verdict taxonomy.** Part A (verdicts): *Upheld · Upheld-with-scope · Qualified · Overclaim-risk ·
> Open*. Part B (framing/record): *Sound · Overclaim-risk · Record-inconsistency · Flagged*.
>
> **Revision.** Corrected 2026-06-02 after an **independent codex + gemini audit** — see **Part G** and
> the **Corrections** changelog at the end.

---

## 0. Central finding

**The two repos never measured the same wall — so their headline narratives only *appear* to
collide.**

- **Prototype wall** = *direct→indirect cross-family transfer across different datasets.* Train on 4
  direct-injection sources (deepset / Gandalf / Mosscap / HackAPrompt); test on a 5-slice cross-family
  OOD slate (BIPIA / InjecAgent / JBB / XSTest / NotInject). Best pooled-OOD AUPRC **0.364 ≤ 0.374
  floor** (`prototype:RESULTS.md:91-96`). Reading: cross-family transfer fails; "fine-tuning hurts"
  (LoRA 0.293 < frozen 0.364); wall is backbone-invariant.
- **Portfolio modeling** = *entirely BIPIA-internal* (`attack-type-lodo/harness.py:63` `BIPIA_ROOT`;
  `OOD_WALL_PREDICTION/criteria.md:114` "the prediction is BIPIA-internal"; carrier-LODO holds within
  BIPIA's email/code/table). Reading: the attack-type wall dissolves under LoRA (capacity-dependent);
  the carrier wall partially persists.

The surface contradiction ("wall stands / fine-tuning hurts" vs. "wall dissolves / capacity-dependent")
is an **axis mismatch**, not a genuine disagreement — and the portfolio's formal record
(`ADR-055`) is largely aware of this. *(An independent codex + gemini audit reached this same
axis-mismatch conclusion **blind** — Part G.)* The **one genuinely open item** is that the prototype's
*actual* wall was deliberately never re-derived under the portfolio's fair-tuning regime. The portfolio
proved that fair-tuned capacity *dissolves the attack-type wall*; the symmetric question — does
fair-tuned capacity climb the *cross-family* wall? — is **untested**, because the only cross-family
fine-tune that exists is the very run (`prototype:RESULTS.md` LoRA 0.293, AUROC 0.383) the portfolio
discards as confounded. That gap (§A.5) is the sharpest result of this audit.

---

## Part A — Independent re-examination of the five headline verdicts

### A.1 §6.5 attack-type falsification — **Qualified**

**Claim.** FALSIFIED at the LoRA ceiling: `T = −0.003`, perm p = 0.90, CI-low −0.008
(`OOD_WALL_PREDICTION/FINDINGS.md:71-81`); interpreted as *"the 'OOD wall' is a property of the
representation, not the task ... surmountable with a small amount of end-to-end capacity"*
(`FINDINGS.md:90-92`).

**Adversarial pass.**
1. **Ceiling-compression.** At `lora` the per-type test AUPRCs sit at **0.956–0.984**
   (`falsification_verdict.json:50-65`; mean top-k 0.978 / bottom-k 0.975) — note the `FINDINGS.md:80`
   prose rounds this up to "0.98–0.999", itself a mild prose-vs-artifact over-statement. The statistic
   is the top-k − bottom-k difference of per-type AUPRC **levels** (`criteria.md` Rev 2, :174-182).
   With all levels pinned near the upper bound (well above the ~0.926 no-skill floor), the contrast is
   *mechanically* compressed toward zero. `T → 0` therefore reflects **uniform near-ceiling detection**
   as much as a "dissolved" gap — the two are observationally entangled at saturation.
2. **Within-corpus axis.** The held-out attack-type shares carrier, corpus, and generating process
   with the training types (BIPIA-internal). Near-uniform transfer to a held-out *task-intent label
   inside the same corpus* is the expected easy case, not a demanding OOD test.

**Verdict.** The FALSIFIED verdict is **methodologically clean** — the rule (judge `lora`; SURVIVES
iff perm p < 0.05 AND CI-low > 0), tails, `k`, and estimator were fixed *before* any LoRA datum and
write-gated (`FINDINGS.md:94-96`); that integrity is real and credited. What is *Qualified* is the
**generalizing interpretation**: "property of the representation, not the task" outruns a
saturation-compressed contrast on a within-BIPIA axis. *(Both codex and gemini red-teams independently
confirmed the ceiling-compression critique — Part G.)* → Fix **A1** (patch).

### A.2 Carrier-LODO `SMALL-THROUGHOUT` — **Upheld (exemplary); watch the downstream label**

**Claim.** G(lora) = +0.067 (CI-low +0.064), table +0.205; "capacity-attenuated, residual table
wall" (`carrier-lodo/FINDINGS.md:1-44`).

**Adversarial pass.** The FINDINGS already does the honest work this audit would otherwise demand: it
flags that the aggregate **masks the table wall** (:58-59), that `SMALL-THROUGHOUT` is the
pre-registered else-branch *label* not the *substance* (:60-62), the n = 3 limitation (:56), and
justifies ROC-over-AUPRC at 83–94% prevalence (:46-52). This is the model the rest of the repo should
follow. The only residual risk is **downstream quotation**: the spine summary did exactly the thing to
avoid — it called the carrier axis the "standing wall" (`ADR-055:32`), which the modeling then had to
walk back (`carrier-lodo/FINDINGS.md:37-44`).

**Verdict.** **Upheld.** Fix is not to the finding but to its *travel*: every downstream mention should
carry "(residual table wall +0.205; n = 3, provisional)". → punch-list (A2-adjacent).

### A.3 EDA carrier-dominance geometry — **Upheld-with-scope**

**Claim.** Silhouette by-carrier 0.197 vs by-attack-type −0.023; KMeans→carrier ARI 0.98;
"attack-type signal is embedding-invisible" (`OOD_WALL_PREDICTION/FINDINGS.md:27-33`).

**Adversarial pass.** True **of the frozen `all-MiniLM-L6-v2` embedding only** — which the FINDINGS
itself states (:31-33). Two scope limits: (a) "embedding-invisible" ≠ "undetectable" — LoRA detects
attack-types at 0.96+ (§A.1); (b) the geometry was computed on **MiniLM, a *different model* than the
detector's ModernBERT backbone** — `lane-1/hypothesis.md:64-66` concedes it "was not recomputed on
ModernBERT." So the claim describes a *separate frozen sentence-encoder*, neither the detector's
representation nor a fine-tuned one. *(The model-mismatch was surfaced by the independent audit —
gemini red-team, Part G.)*

**Verdict.** **Upheld-with-scope.** Fix: the qualifier must read "frozen MiniLM (not the ModernBERT
detector backbone)" wherever the geometry claim travels. → punch-list.

### A.4 Off-the-shelf / V10 scope-blindness — **Qualified**

**Claim.** Direct-trained probes score attacks below their own benign floor (ProtectAI-v2 0.25 attack
vs 0.28 benign; AUROC 0.44), while indirect-capable PG1 fires cleanly (0.86 vs 0.04) ⇒ "the collapse
is **scope-blindness, not undetectable data**" (`FINDINGS.md:41-48`).

**Adversarial pass.** The *data* is solid and the PG1 contrast is strong positive evidence that
indirect injection **is** detectable. But "below-chance ⇒ *scope*-blindness specifically" is an
**interpretation** of a below-chance score — and it is **the same interpretive move the portfolio
faulted in the prototype**: `postmortem.md:44` marks the prototype's "below-floor AUROC =
anti-correlation / label inversion" as *"Interpretation, not demonstrated → measure it (per-row score
distributions)."* The portfolio then makes the structurally identical leap for V10 without the per-row
demonstration it prescribed. Alternative readings (threshold/polarity mismatch, a different scored
construct) are not excluded.

**Verdict.** **Qualified** — the mechanism label inherits exactly the *interpreted-not-demonstrated*
gap the portfolio criticized. Fix: either run the prescribed per-row/threshold check, or soften to
"consistent with scope-blindness." → punch-list.

### A.5 The cross-family wall under fair tuning — **Open** *(the sharpest item)*

**Claim.** `ADR-052:16-18` judges that on the prototype's pooled OOD "**every rung AND SOTA ProtectAI
sit at/below the random floor (0.374) — direct→indirect transfer has no signal, and 'frozen>LoRA' is a
mirage (two sub-random detectors)**," and pivots all portfolio modeling to BIPIA-internal
indirect→indirect; `postmortem.md:18` calls the cross-family wall "over-determined ... Keep it."

**Adversarial pass.**
1. **The pivot's core justification is sound — credit it.** "No signal cross-family" rests most
   cleanly on the **frozen probe**, which is *not* recipe-confounded (it is not fine-tuned) and sits at
   chance (AUPRC 0.364, AUROC 0.515; `prototype:RESULTS.md:91,256`). A clean detector at chance on
   cross-family, plus the external literature (`postmortem.md:18`; PromptShield / PromptLocate / "How
   Not to Detect…" are real and present in the research corpus), over-determines that the cross-family
   wall is **real**. This is not circular and is not in dispute.
2. **But the symmetric capacity question is untested.** The portfolio's headline contribution is that
   *fair-tuned capacity dissolves the attack-type wall* (§A.1). The natural symmetric question — *does
   fair-tuned capacity climb the **cross-family** wall?* — has **no clean answer**, because the only
   fine-tuned cross-family numbers that exist are the prototype's LoRA (0.293, AUROC 0.383 < chance),
   which the portfolio itself discards as confounded/mirage (`ADR-052:18`; `postmortem.md:42`). *(The
   discard rests on three confounds; the independent audit verified that the "frozen pre-head" one is
   **technically correct** — `modules_to_save=["classifier"]` trains only the final classifier, leaving
   the intermediate `head` frozen, `prototype:lora_config.py:32` — but "real but overstated", since
   that is the PEFT `SEQ_CLS` default; the **material** confound is the untuned shared recipe.)* There
   is a clean *frozen* cross-family estimate (at floor) but **no clean *fine-tuned* cross-family
   estimate** — precisely the rung where capacity mattered on the attack-type axis.
3. **A residual phrasing point.** "*Every* rung ... no signal" (`ADR-052:17`) folds the confounded
   fine-tuned rungs into the no-signal evidence; the load-bearing clean estimate is the frozen probe
   alone. Minor, but it lets "no signal" read as stronger (capacity-inclusive) than the clean evidence
   supports.

**Verdict.** **Open.** The pivot is a sound prioritization and "the cross-family wall is real" is
well-supported; neither is in question. What is genuinely open — and nowhere marked as open — is
whether *fair-tuned capacity* reduces the cross-family wall as it did the attack-type wall. The
overclaim risk is confined to any summary that implies capacity has been shown *not* to help
cross-family: it has not been tested there. *(Both red-teams independently marked this Confirmed —
Part G.)* → Fix **A3** (patch); the gap-closer (§E) is precisely the experiment that would answer it.

---

## Part B — Framing / record-integrity

| # | Claim under audit | Verdict | Minimal fix |
|---|---|---|---|
| **A1** | "the OOD wall is a property of the representation, not the task" / "M1 dissolved the wall" (`FINDINGS.md:90-92`; `program-review §1.2`; auto-memory) | **Overclaim-risk (summary layer)** — `ADR-055:32,65` scope it and *reject* outright-dissolution; the experiment + review one-liners generalize past the within-BIPIA attack-type axis | **Draft patch 1** (below) |
| **A2** | `ADR-055:26` maps the prototype's wall onto "the carrier / direct→indirect axis" | **Partial conflation** — the prototype's wall bundles (i) direct→indirect *training-scope* shift + (ii) *cross-dataset* shift; carrier-LODO isolates only (iii) the within-BIPIA *container*. A within-corpus result stands in for a cross-family question it does not test | Name the 3 shift components in the spine; state carrier-LODO speaks to (iii) only; mark (i)+(ii) not-re-tested |
| **A3** | `postmortem.md:41` "re-derive 0.364 via ADR-052" vs `ADR-052:17` pivot | **Record-inconsistency / unfulfilled action** | **Draft patch 2** (below) |
| **A4** | D1 "frozen > LoRA is a mirage" (`postmortem.md:42`) | **Sound reasoning, undemonstrated on the prototype's own axis** — argued from confounds + near-/below-chance AUROC (frozen 0.515 ≈ chance, LoRA 0.383 < chance) + within-BIPIA fair-LoRA, never a cross-family fair re-run. The one inference in an otherwise pre-registered program that is *argued, not measured* | State this explicitly; couple it to A3 / §A.5 |
| **A5** | The arXiv:2602.14161 citation behind "96.6% separability ↔ 8.4pp drop" (`criteria.md:46`, `FINDINGS.md:54`, `carrier-lodo/FINDINGS.md:63`) | **Sound — citation real & ledgered** (verified: `docs/research/training-and-evaluation/papers/fomin2026benchmarkslie.pdf` 11.5 MB + `evidence_ledger.yml:3163` + `gather_trace.yml:494`; codex + gemini-blind-A web-confirmed). The paper reports an **8.4pp CV→LODO AUC gap (0.996→0.912)** *and, separately,* **96.6% dataset-classifier accuracy** — the "↔" wrongly *links* two distinct figures. **Not fabricated** (gemini red-team + blind-B claimed so — a hallucination; see Part G). | Reword "↔" as *association*, not equivalence; cross-reference the cached paper from `postmortem.md:48`, whose "no derivation" flag refers to the *prototype's* un-attributed inheritance (now properly cited) |
| **A6** | `FINDINGS.md:62` still says "V10 is incomplete pending PG1" while `:41-48` reports V10 complete (PG1 scored) | **Record-inconsistency (stale)** — codex red-team | Update/remove the stale line |
| **A7** | `program-review-2026-06.md:15-29` frames "the science question is now answered" | **Overclaim-risk** — contradicts §A.5 (cross-family is Open) — codex red-team | Qualify: "settled on the within-BIPIA attack-type + carrier axes; cross-family transfer under fair tuning remains open" |
| **A8** | full-FT monotonicity: "more capacity can only dissolve the wall further" (`ADR-054:78-82`; `program-review:83-86`) | **Overclaim-risk** — full-FT OOD was **never measured**; it is a conjecture — codex blind | Mark as an expectation/conjecture, not a result |

---

## Part C — What is **not** in question (fairness)

- **The numbers.** Every headline statistic was independently reproduced 5/5, Δ ≤ 1e-4, from raw
  artifacts (`experiments/AUDIT_2026-06/verification_report.md`). This audit accepts them in full.
- **Pre-registration is genuine and load-bearing.** The §6.5 FALSIFIED verdict *could not be gamed* —
  rule, tails, `k`, estimator fixed before any LoRA datum, write-gate opened only on a complete sweep
  (`FINDINGS.md:94-96`). The revision policy (R1/R2) is honest (timestamped rationale, rule byte-for-byte
  unchanged).
- **The carrier-LODO record is exemplary** — it pre-empts its own aggregate's masking effect and
  downgrades "standing wall" itself (`carrier-lodo/FINDINGS.md:37-62`).
- **The multi-axis reframe is a real scientific advance**, and `ADR-055:65` explicitly *rejects* the
  outright-dissolution overclaim this audit guards against.

The audit targets **interpretation, framing, and a few record items** — not the integrity of the
experiments.

---

## Part D — Fixes

### Punch-list (location + rationale; no wording)
- **A2** — `ADR-055` spine + `program-review`: distinguish the 3 shift components; scope carrier-LODO to the container component.
- **A4** — `postmortem.md` §4 / a footnote: state the "mirage" refutation is *argued* (confounds + within-BIPIA fair-LoRA), not measured on the cross-family axis.
- **A5** — **resolved: citation real** (cached PDF + ledger; web-confirmed). Reword the "↔" to an *association* (the paper's 8.4pp CV→LODO gap and 96.6% dataset-classifier accuracy are distinct figures); cross-reference the cached paper from `postmortem.md:48` to retire the "no derivation" flag.
- **A6/A7/A8** — fix the stale V10 line; qualify the program-review "answered" framing; mark the full-FT monotonicity as conjecture.
- **§A.2 / §A.3 / §A.4** — attach travelling qualifiers ("residual table wall, n=3"; "frozen MiniLM, not the ModernBERT backbone"; "consistent with scope-blindness") wherever those claims are quoted downstream.

### Draft patch 1 — A1 (the summary-layer over-generalization)
**Target:** `experiments/eda/OOD_WALL_PREDICTION/FINDINGS.md:90-92` (the bolded closing sentence).
**Proposed replacement:**
> **On the attack-type axis, within BIPIA indirect injection, the "OOD wall" is a property of the
> representation, not the task:** real for lexical / frozen-embedding detectors, and surmountable by a
> small amount of end-to-end capacity, which detects every held-out attack-type near-uniformly (test
> AUPRC 0.956–0.984). *Two scope caveats:* (a) at that near-ceiling level the top-k−bottom-k contrast is
> partly saturation-compressed, so `T → 0` reflects uniform high detection as much as a "dissolved"
> gap; (b) the held-out type shares carrier and corpus with training — this is *within-corpus*
> generalization, **not** the prototype's *cross-family* (direct→indirect, cross-dataset) wall, which
> was not re-derived under fair tuning (`ADR-052`) and remains **open**.

*(Mirror the axis qualifier into `program-review-2026-06.md §1.2`, which already carries per-axis
qualifiers but lacks the cross-family scope note.)*

### Draft patch 2 — A3 (the unfulfilled re-derivation action)
**Target:** `docs/planning/prototype-postmortem.md:41` (the §4 table row for the 0.364 claim).
**Proposed replacement row:**
> \| Best pooled-OOD AUPRC 0.364 vs floor 0.374 *(cross-family: direct→indirect, across datasets)* \|
> **Not re-derived — deliberately deferred** \| Cross-rung confounds A–C; **and** `ADR-052:17` judged
> direct→indirect "no signal" and pivoted to BIPIA-internal indirect→indirect \| The portfolio measured
> a *different* axis (within-BIPIA attack-type + carrier); the prototype's cross-family number was
> **never re-run under fair per-rung tuning**. The cross-family comparison remains **OPEN** —
> see `prototype-comparison-audit-2026-06.md §A.5`. \|

*(Add a one-line note under the table: "no signal" is clean for the *frozen probe*, but the symmetric
question — whether **fair-tuned capacity** climbs the cross-family wall, as it did the attack-type wall
— is untested, since the only cross-family fine-tune is the discarded confounded run. See §A.5.)*

---

## Part E — The one experiment that would *close* (not just scope) the gap *(note only)*

A **fair-tuning direct→indirect cross-family re-run** is the only thing that would settle the open
item: replicate the prototype's exact pooled-OOD setup (train deepset/Gandalf/Mosscap/HackAPrompt →
test BIPIA/InjecAgent/JBB/XSTest/NotInject) under the portfolio's **fair per-rung tuning** (`ADR-052`),
and ask whether capacity climbs the cross-family wall the way it climbed the attack-type wall. The
prototype already holds the configs and data slate. Rough cost ≈ M1's LoRA rung (**~$1–2** RunPod H100;
tfidf/frozen local-free).

**Flagged as an optional, user-led §16 / Lane candidate — out of scope for this memo.** If pursued, its
pre-registration belongs in its own timestamped `criteria.md` (`ADR-055:68`), not here.

---

## Part F — Overall verdict (pre-publication)

The portfolio's experiments are **reproducible, pre-registered, and honest at the formal layer**, and
the carrier-LODO record is a model of self-qualification. The headline science — a **multi-axis,
capacity-dependent OOD picture** — stands. What needs tightening before public release is the
**boundary between what was *shown* (within-BIPIA attack-type + carrier axes) and what was *inherited or
asserted* (the prototype's cross-family wall)**:

1. Apply the two scope patches (A1, A3) so the summary layer matches the careful formal layer.
2. Apply the minor framing fixes (A2, A4, A5) and the three record fixes (A6, A7, A8).
3. **Mark the cross-family comparison explicitly OPEN**, decoupling "the wall is real (literature)"
   from "fair-tuned capacity cannot reduce it (untested)."

None of this touches a number. It is a framing-and-record tightening that brings the *narrative* up to
the same standard as the *experiments*.

---

## Part G — Independent multi-voice audit outcome (codex + gemini, 2026-06-02)

This memo was itself put through an independent cross-model audit — **codex** (OpenAI gpt-5.5) and
**gemini** (Google 2.5-pro), each running a *blind* pass (not shown this memo) and a *red-team* pass,
read-only, with web-enabled citation checks. Raw reports + a reconciliation live in
`experiments/AUDIT_2026-06/independent_*.md` and `independent_audit_synthesis.md`.

- **The spine was confirmed independently.** Both models, *blind*, reached the **axis-mismatch** (the
  two repos are not in genuine conflict); both red-teams marked **A.1, A.2, A.4, A.5** *Confirmed*.
- **Two adversarial findings were confident-but-wrong, caught by artifact-grounding** — and they
  motivated the corrections above: (i) gemini called `arXiv:2602.14161` a *fabricated citation* — it is
  real and ledgered (A5); (ii) gemini called the "frozen pre-head" confound *mathematically invalid* —
  it conflated `head` with `classifier`; the confound is technically correct (§A.5 note). Both were
  resolved by reading the actual artifacts, not by trusting a single voice.
- **Net.** The memo's conclusions hold; the audit *sharpened* them. The methodology lesson — a lone
  adversarial voice issues confident, severe, wrong verdicts; **verify "is-wrong / fabricated" claims
  against artifacts** — is codified in the audit-procedure note developed alongside this work.

---

## Corrections from the independent audit (2026-06-02)

Applied **in-place** to this memo; git preserves the pre-audit version.

1. **A.1 numbers** — per-type lora AUPRC corrected **0.98–0.999 → 0.956–0.984** (`falsification_verdict.json`); flagged the FINDINGS prose as a mild over-round. *(codex)*
2. **A5 verdict flipped** — *Flagged-open* → **Sound (citation real & ledgered)**; reframed the "↔" as an association; **not** fabricated. *(codex + a local file check; gemini was wrong both ways)*
3. **A.3** — added the **MiniLM-vs-ModernBERT** model mismatch in the geometry claim. *(gemini red-team)*
4. **§A.5 note** — added the **Confound-A** nuance (technically correct, "real but overstated"). *(cross-voice + `lora_config.py` check)*
5. **A6 / A7 / A8 added** — stale V10 line; program-review "answered" vs cross-family-Open; full-FT monotonicity conjecture. *(codex)*
6. **Part G added** — the independent-audit outcome + the two caught hallucinations.

---

*Sources — portfolio:* `experiments/eda/OOD_WALL_PREDICTION/{FINDINGS.md, criteria.md, falsification_verdict.json}`,
`experiments/carrier-lodo/FINDINGS.md`, `experiments/AUDIT_2026-06/{verification_report.md, independent_audit_synthesis.md}`,
`experiments/attack-type-lodo/{harness.py, folds.py}`, `decisions/ADR-05{2,4,5}-*.md`,
`docs/planning/{prototype-postmortem.md, program-review-2026-06.md}`. *Prototype:* `RESULTS.md`,
`src/training/lora_config.py`. Numbers accepted from `AUDIT_2026-06` (5/5 reproduced, Δ ≤ 1e-4); no
statistic was recomputed for this memo — the only computed checks were artifact-existence verifications
during the independent audit (Part G).
