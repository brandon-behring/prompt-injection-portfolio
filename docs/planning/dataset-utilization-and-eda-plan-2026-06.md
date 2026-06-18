# Dataset utilization atlas + comprehensive cross-dataset EDA plan (2026-06)

> **Status: analysis / proposal — no EDA executed, no canonical record edited.** Drafted in response to
> the concern that an early planning decision narrowed the modeling to BIPIA and left a large vetted
> dataset corpus idle. Restores the original intent: *use the EDA tooling to explore all candidate
> datasets and let the data decide what we can do.* Present-first; the EDA runs are a separate go.

## 1. The concern, made precise

The EDA tooling (`experiments/eda/survey_run.py`, the A1 geometry probes in
`experiments/eda/OOD_WALL_PREDICTION/run_a1_v4.py`, the `dataset-auditor` subagent) was built to survey a
**30-dataset candidate universe** (`docs/research/datasets/agent_index/`) and let the EDA decide which
graduate into modeling (`00_overview.md`: *"Dataset SELECTION is deferred to the EDA … the EDA decides
which ones graduate"*).

That selection step **never ran across the universe.** `ADR-052` (R26) chose *attack-type-LODO within
BIPIA* as the headline — justified by "BIPIA is the only one shipping a disjoint attack-type split" —
which collapsed the modeling to a single corpus **before** the cross-dataset EDA could inform "what can
we do." The consequence, quantified:

- **~1.13M audited rows** across 13 gate-passed datasets were used **only as a near-duplicate yardstick
  vs BIPIA** (`OOD_WALL_PREDICTION/FINDINGS.md:51`), never modeled.
- The narrowing reached **even inside the indirect family**: **LLMail-Inject (462k adaptive indirect
  attacks)** and **WAInjectBench** (drop-in indirect, 8 attack types) sit idle — BIPIA was treated as
  "the only" indirect corpus when it is one of five.
- We modeled the **smallest clean corpus** (BIPIA: 5 attack strings/type, 75/split) and shelved the
  large ones.

This doc is the corrective: the cross-dataset EDA the tooling was built for, scoped across all 30.

## 2. The utilization atlas (all 30 → family · tier · candidate use)

Tiers verbatim from `agent_index/00_overview.md`; "Candidate lane" is the proposed use.
`⚠L` = license unknown / needs legal review **before publication** (fine to EDA locally).

| # | Dataset | Family | Tier | Avail. | Candidate lane |
|---|---|---|---|---|---|
| 1 | deepset/prompt-injections | direct | drop-in | ✓ | CF-train (smoke) |
| 2 | guychuk/benign-malicious (464k) | direct | drop-in | ✓ | **CF-train (primary, largest clean)** |
| 3 | hendzh/PromptShield (43k) | direct | drop-in | ✓ | CF-train **+ Lane 1b (has obfuscated/unicode cases)** |
| 4 | reshabhs/SPML (16k) | direct | derivable | ✓ | CF-train (system-vs-user structure) |
| 5 | Tensor Trust (172k) | direct | derivable | ✓ ⚠L | CF-train (extract-vs-hijack taxonomy) |
| 6 | HackAPrompt (600k+) | direct | adapt-heavy | ✓ | CF-train (attack-success signal) |
| 7 | Harelix Mixed-Techniques | direct | drop-in | ⚠ 401 | CF-train (ProtectAI-v2 component) |
| 8 | jayavibhav/prompt-injection (327k) | direct | drop-in | ✓ ⚠L | CF-train (large; license review) |
| 9 | jayavibhav/prompt-injection-safety (60k) | direct | drop-in | ✓ ⚠L | multiclass (license review) |
| 10 | Open-Prompt-Injection | direct | derivable | ✓ | CF-train (7-task framework) |
| 11 | xTRam1/safe-guard (10k) | direct | drop-in | ⚠ mismatch | hold (citation/license mismatch) |
| 12 | **BIPIA** | indirect | derivable | ✓ | CF-test + attack-type/carrier (current) |
| 13 | Indirect-in-the-Wild (15.4k) | indirect | pointer | ✗ unreleased | CF-test (gold-standard) — monitor |
| 14 | **LLMail-Inject (462k)** | indirect | derivable | ✓ | **CF-test + within-indirect cross-corpus (idle!)** |
| 15 | WAInjectBench | indirect | drop-in | ✓ ⚠L | CF-test (web-agent indirect) |
| 16 | WASP | indirect | adapt-heavy | ✓ | agentic (executable sandbox) |
| 17 | **WildGuardMix** (just unblocked) | toxicity-guard | derivable | ✓ (gate accepted) | benign/harm control + **Lane 4 gate** |
| 18 | jackhhao/jailbreak-classification | jailbreak | drop-in | ✓ | CF-train (ProtectAI-v2 component) |
| 19 | ToxicChat (10k) | toxicity-guard | drop-in | ✓ | CF-train (toxicity+jailbreak cols) |
| 20 | In-the-Wild Jailbreak / DAN (21.5k) | jailbreak | derivable | ✓ | CF-train (community jailbreaks) |
| 21 | OR-Bench (80k) | over-defense | eval-only | ✓ | **benign-FPR / over-refusal eval** |
| 22 | NotInject (339) | over-defense | eval-only | ✓ | benign-FPR (already used in M1) |
| 23 | XSTest v2 (450) | over-defense | eval-only | ✓ | benign-FPR contrast |
| 24 | PINT (4.3k) | over-defense | eval-only | ✗ withheld | Lane 4 gate (request-only) |
| 25 | AgentDojo | agentic | adapt-heavy | ✓ | agentic lane (future) |
| 26 | Agent Security Bench | agentic | adapt-heavy | ✓ | agentic lane (future) |
| 27 | InjecAgent (1k) | agentic | adapt-heavy | ✓ | CF-test (tool-integrated indirect) |
| 28 | GenTel-Bench (177k) | aggregated | drop-in | ✓ | CF-train (harm taxonomy) |
| 29 | InjecGuard / PIGuard | aggregated | drop-in | ✓ | CF-train (⚠ contains BIPIA → leakage check) |
| 30 | ProtectAI-v2 recipe | aggregated | pointer | ✓ | reference detector (already V10) |

**CF = cross-family.** Unavailable: Indirect-in-the-Wild (unreleased), PINT (withheld), WildGuardMix
(was gated — now accepted), xTRam1 (mismatched), Harelix (401). License-review-before-publication:
jayavibhav×2, Tensor Trust, WAInjectBench.

## 3. EDA done vs. the gap

**Done** (`survey_v2_summary.json`, `OOD_WALL_PREDICTION/`): per-dataset schema audit (rows, splits,
label-semantics, length, **obfuscation-invisible-rate**); three gate checks (class-balance,
cross-split-leakage, errors); near-duplicate check **vs BIPIA only**; embedding geometry **on BIPIA
carriers only**. All single-dataset or vs-BIPIA.

**The gap** — the cross-dataset analysis that would tell us "what we can do":

| Missing EDA | Why it matters | Lane it unlocks |
|---|---|---|
| Cross-**dataset** geometry (silhouette/ARI/PAD/MMD with dataset/family as the grouping axis) | The pre-modeling **measurement of the cross-family wall** — the analog of the carrier geometry that called M1's result | Cross-family #1 (entry-gate) |
| Label harmonization (numeric/string/bool/3–18-way → injection-vs-benign) | Required to **pool** heterogeneous sets for train/test | all pooled lanes |
| Pairwise near-dup / leakage **matrix** (train-sources × test-slate) | Source-disjoint CF-LODO; 4 sets already fail internal leakage | Cross-family #1 |
| Per-dataset prevalence | AUPRC-vs-AUROC discipline beyond BIPIA's 83–94%; 5 fail class-balance | all |
| Obfuscation / invisible-char ranking | A ready Lane-1b candidate list (PromptShield, BIPIA-obf, Mindgard) | Lane 1b |
| Indirect-corpus characterization (BIPIA + LLMail-Inject + WAInjectBench) | Is there a **within-indirect cross-corpus** experiment beyond BIPIA? | new option |

## 4. The proposed comprehensive EDA plan (library-first; mostly local/free)

Each task names its question, the existing tool it reuses, and the output. **Nothing here runs yet** —
present-first.

- **E1 — Universe survey completion.** Extend `survey_run.py --out` (and fan out the `dataset-auditor`
  subagent, one per dataset) across the **~12 universe members not yet HF-audited** (LLMail-Inject,
  WAInjectBench, Tensor Trust, Open-Prompt-Injection, Shen DAN, the agentic sets, …). Output: a complete
  30-row audit (rows/splits/labels/length/obfuscation/gates). *Local; cheap.*
- **E2 — Cross-dataset geometry (headline).** Re-run the A1 machinery (`run_a1_v4.py`) with **dataset /
  family as the grouping variable** on a unified embedding: silhouette, ARI (KMeans→family), PAD/MMD
  pairwise matrix, UMAP. Output: *does the embedding cluster by source family, and how separable is
  direct vs indirect?* — the cross-family wall's geometry, currently only a one-line "PAD ~2.0" aside
  (`FINDINGS.md:53`). *Local; free.*
- **E3 — Label harmonization map.** A documented `injection | benign | (out-of-scope)` mapping across all
  schemes + the rationale per dataset. Output: a harmonization table (the prerequisite for any pooled
  train/test). *Analysis.*
- **E4 — Leakage / near-dup matrix.** TF-IDF (+ optional embedding) near-dup across the **full pairwise
  grid**, not just vs BIPIA. Output: a disjointness matrix → which datasets can co-train/co-test without
  leakage. *Local; cheap.*
- **E5 — Prevalence + metric-basis check.** Per-dataset positive rate → confirm AUROC-primary
  reporting (the BIPIA 83–94% lesson, generalized). *Analysis.*
- **E6 — Obfuscation / char-injection inventory.** Collate `obfuscation_invisible_rate` + the index's
  obfuscation flags (PromptShield unicode cases, BIPIA obfuscation sub-family, Mindgard evaded-samples)
  → a ranked **Lane-1b** candidate list. *Reuses measured fields.*
- **E7 — Within-indirect cross-corpus probe.** Characterize BIPIA + LLMail-Inject + WAInjectBench
  jointly: do they share carriers/attack-types, and is there a clean **indirect→indirect cross-corpus**
  generalization experiment beyond BIPIA's within-corpus axis? *Local.*

## 5. What it determines — "what we can do"

The EDA outcomes gate a concrete experiment menu (this is the payoff of restoring explore-first):

1. **Cross-family #1** (the audit's critical experiment): E2 + E3 + E4 decide whether the
   prototype-comparable slate is sound and whether the **extended arm** (option 1) — folding in the
   vetted direct corpus (guychuk, PromptShield, jackhhao, GenTel, …) — is separable/poolable enough to
   strengthen the generalization claim.
2. **Within-indirect cross-corpus** (new, from E7): a possible experiment BIPIA-narrowing hid —
   train on BIPIA indirect → test on LLMail-Inject / WAInjectBench indirect (or pooled).
3. **Lane 1b (char-injection):** E6 yields the candidate set directly.
4. **Lane 4 (saturation gate):** WildGuardMix (now unblocked) + PromptShield + PINT (request-only).
5. **Benign-FPR / over-defense:** OR-Bench + XSTest + NotInject as a proper false-positive slate.

## 6. Sequencing, licenses, scope guard

- **This EDA is the restored explore-first step** and doubles as the **cross-family #1 entry-gate**
  (mirrors the EDA-arc-as-M1-entry-gate pattern that made M1 credible). It should precede finalizing the
  cross-family pre-registration (`experiments/cross-family-transfer/criteria.DRAFT.md`) — E2/E3/E4 tell
  us whether the extended-arm slate is viable.
- **Licenses:** every ⚠L set is fine to **EDA locally**; license clearance (jayavibhav×2, Tensor Trust,
  WAInjectBench) is owed only before any **published** training/eval. PINT (request-only) and
  Indirect-in-the-Wild (unreleased) stay out.
- **Cost:** E1–E7 are local/free (embeddings + TF-IDF + schema audits); no GPU. The only paid step
  remains the eventual cross-family `lora` rung (~$1–2), unchanged.
- **Downstream record note (not edited here):** `ADR-052`'s "BIPIA is the only usable corpus" framing is
  true *for the attack-type-LODO axis only*; this atlas shows a much wider usable universe for the
  cross-family + char-injection + saturation axes. A reframe belongs in the cross-family pre-reg and/or
  an ADR addendum — **flagged, user-led, not applied.**

## Scope guard
- Analysis/proposal only: **no EDA executed, no dataset downloaded, no canonical record edited, nothing committed.**
- Reuses existing tooling (`survey_run.py`, `run_a1_v4.py`, `dataset-auditor`, eval-toolkit) — library-first, no reimplementation.
- The EDA runs (E1–E7) and any modeling are separate present-first goes.

---

*Sources: `docs/research/datasets/agent_index/{00_overview,01–06,README}.md` + `_candidate_universe.md`
(the 30-set universe); `experiments/eda/{survey_run.py, survey_v2_summary.json}`;
`experiments/eda/OOD_WALL_PREDICTION/{run_a1_v4.py, FINDINGS.md}`; `decisions/ADR-052`. Per-dataset
classifications cross-checked against the agent index this session.*
