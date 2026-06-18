# Consolidated full re-audit — 2026-06-09/10 (DRAFT — Checkpoint 1)

**Status: Checkpoint-1 decisions taken 2026-06-10 (FIX-NOWs apply-all · harness-v0 retrospective trio · provenance (b) · v0.1.0 Fork A(b)). All 15 FIX-NOWs + dispositions are APPLIED in the working tree; nothing committed (user-led).**

**Bottom line: the spine holds. All three ratified verdicts — attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family SURVIVES — reproduce bit-exactly from raw artifacts under 30 adversarial verifiers, 4 independent mechanical reproduction jobs, cheap-rung retrains, and a numerically-quantified stress test of the one shared estimator defect found. Zero BLOCKERs. The harvest is 15 FIX-NOW doc corrections (applied), 18 FOLLOW-UP work items (two of them substantive new findings: a MiniLM truncation artifact confounding part of the EDA geometry story, and an InjecAgent materialization bug), and 10 cosmetic notes.**

## 1. Scope

Full re-audit, user-elected over the gap-focused alternative (every ratified verdict re-verified from scratch, not just the unaudited 2026-06-07/08 frontier). Executed:

- **Phase 0** — baseline gates (gate-runner) + git immutability ledger.
- **Phase 1** — mechanical reproduction: all committed reproduction/verdict scripts re-run; independent parquet-level recompute of every stored metric; cheap-rung retrains (one fold per arc). **LoRA fence:** lora rungs are not re-trainable without paid GPU; their verification ceiling is parquet-level recompute + the committed cross-arch reconciliation (H100 vs RTX-4090, Δ0.0072).
- **Phase 2** — 30 adversarial verifiers: 5 roles (numbers-reproduce / leakage-hunt / label-correctness / estimator-stats / claim-vs-evidence) × 6 arcs (attack-type §6.5, carrier, cross-family Arm A, cross-family B−/B+, EDA+deployed-guards, statistical machinery).
- **Phase 3** — frontier audit of the uncommitted work (agent-harness-v0, RunPod provenance dirs, results-analysis-2026-06-08.md, glossary diff).
- **Phase 4** — methodology-audit mechanical sweep (303 docs) + codex/gemini external refutation of this register (§6).

## 2. Baseline + prior-audit chain (Phase 0)

| Gate | Result |
|---|---|
| `make test` | **PASS** — 45 baseline + 6 frontier (agent-harness) tests green |
| `make lint` | **FAIL** — 3 ruff issues, all in committed `scripts/cheap_gpu_monitor.py` (→ W6) |
| `make contracts` | **FAIL** — 12/13; 2 unregistered imports, same file (→ W6) |

Immutability ledger (git log since each prior audit over its subject paths): carrier-lodo, cross-family (since B4 audit 06-06), and REPRODUCTION_2026-06 untouched; attack-type/OOD-wall paths touched only by `df74b18` (+6 docstring lines in reference_scorers.py — verified benign and numerically exact) and `f00e035` (the known A3+A4 record fixes). All four prior audits (5-verifier post-M1; B4 ROBUST; bootstrap reproduction; prototype-comparison) remain anchored — and were re-executed anyway under this full re-audit.

## 3. Mechanical reproduction (Phase 1) — all PASS

**Verdict scripts re-run** (reproduce_6_5/carrier/dialect + b4_verdict): every point estimate **exact (Δ=0)**; all CI-low drift ≤9.8e-4, within pure MC noise of the pre-stated ±0.02 tolerance. Headline checks: §6.5 lora T=−0.0030903 (FALSIFIED, p=0.900=63/70 exact); carrier G_lora=+0.0670170 (SMALL-THROUGHOUT); Arm A Gx_lora=+0.3645896, CI-low +0.2835917 (SURVIVES); B− 3/4 + B+ 3/4 with fujitsu perm_p 0.9988 — all match committed verdict files to the digit.

**Parquet-level recompute** (bypassing metrics.json): 162/162 checkable files reproduce ROC-AUC and PR-AUC at **Δ = 0.0** across all four results trees. Not checkable by design: 9 reference-scorer files (no row-level predictions) and B2_4's PR-AUC (not stored — flat schema).

**Cheap-rung retrains** (CPU-only, committed code, one tfidf fold per arc): **BIT-EXACT** on all four arcs, including every per-type AUPRC entry. Frozen retrain skipped — CPU-infeasible (~hours for ModernBERT-base embedding); fence recorded.

**Audit-incident note:** `falsify_ood_wall.py` overwrote the committed `falsification_verdict.json` during the tfidf/frozen re-derivation (no `--out` flag; unconditional write). Restored via `git checkout`; committed content verified intact. Registered as W3.

## 4. Adversarial verifier matrices (Phase 2) — 30/30 returned

| Arc | numbers | leakage | labels | stats | claims | Verdict holds? |
|---|---|---|---|---|---|---|
| 1 attack-type §6.5 | REPRODUCES | CLEAN | CLEAN | CLEAN | over-claims (mild) | **YES** |
| 2 carrier | REPRODUCES | CLEAN | CLEAN | minor discrepancy | CLEAN | **YES** |
| 3 Arm A | REPRODUCES | CLEAN | doc-drift only | CLEAN | over-claims (mild) | **YES** |
| 4 dialect B−/B+ | REPRODUCES | CLEAN¹ | CLEAN² | 2 estimator defects³ | over-claims (mild) | **YES** |
| 5 EDA + guards | REPRODUCES⁴ | CLEAN (pre-reg chain intact) | 1 real bug (W2) | 1 real artifact (W1) | over-claims (1 substantive, F5) | **YES (scoped)** |
| 6 stat machinery | primitive-usage CLEAN | hand-rolled: defect quantified, no flip (W4) | cluster-units: 2 disclosure gaps (W11) | RULE-DRIFT found (W10) | DF/repro claims: minor (F14, W15) | **YES** |

¹ With one REFUTED-CLAIM: the criteria's "index bug fixed" statement is wrong — the inverted `cross_dedup_pairs` reading still exists in Arm-B's `leakage_gate.py:85` (harmless: 0 pairs, reproduced with corrected reading; the fix exists only in `leakage_gate_arm_a.py`) → W17.
² Plus a NEW direction-strengthening artifact: all 2,108 injecagent positives carry the literal `<Attacker Instruction>` placeholder → W2.
³ Row-level permutation (diagnostic-only) and the shared seed-coupling defect → W4/W5.
⁴ One provenance gap: PG1 0.998 rests on a gitignored tree → W9.

**Highest-value independent reproductions:** every verifier re-derived its arc's numbers with its OWN implementation (own AUROC/bootstrap/permutation code, different RNG) and matched the committed values to the 4th decimal or better. Leakage hunters went empirical: zero exact train↔test overlap reproduced across all folds/seeds in every arc, including a full 791,911-row Arm-A superset rebuild, containment probes across all 4 dialects, and hash-identity of the persisted parquets against fold reconstruction (proving the RunPod lora rung scored exactly the audited rows).

**Stress test of the one shared estimator defect (W4):** re-running the committed data with corrected (shared-across-seed) draws widens CIs ×1.2–1.7 and flips nothing: carrier lora CI-low +0.0640→+0.0634; Arm A +0.2837→+0.2477; bipia B− +0.2051→+0.1666 — all still clear their gates.

## 5. Frontier audit (Phase 3)

- **agent-harness-v0**: 6/6 tests pass; scripted rerun **byte-identical**; every cell of reports/summary.md is an **exact** arithmetic consequence of results/scripted.jsonl; results leak into no other doc (grep-verified — all `agent_harness` hits elsewhere are the dossier's pre-existing claim family). One validity tension (part of W7): `spotlight_delimit` cannot affect the scripted backend by construction (`run.py:223-224` acknowledges; Claim Boundaries doesn't), so its "no security benefit" row is a property of the harness design, not an empirical result — same caution applies, in mirror image, to the "perfect" provenance_gate/tool_firewall rows. Retrofit variants for Checkpoint-1 decision:
  - **(A) Retrospective record trio** — add `criteria.md` opening "RETROSPECTIVE SCOPE DECLARATION (not a pre-registration)", a FINDINGS.md fenced to scripted-backend/n=6 construction-property claims, and a verdict.json with `verdict: "EXPLORATORY-VALIDATED"`.
  - **(B) Exploratory, no verdict** — add only a STATUS banner to its README ("exploratory; no verdict surface; v1 requires true pre-registration"); no criteria/FINDINGS/verdict files.
- **RunPod provenance dirs** (421MB + 324MB): all 28 metrics.json **byte-identical (sha256)** to their canonical counterparts; the single expected mismatch is the documented H100↔4090 cross-arch pair (Δroc 0.0072, confirmed to the 4th decimal); zero orphans either direction; the B+ canonical tree correctly comes from the 4090 run. sha256 manifest drafted (28 entries + parquet counts) ready to land under either disposition.
- **results-analysis-2026-06-08.md**: **FAITHFUL** — 12/12 sampled cells, 3/3 verdict-file checks, 6/6 inventory counts exact. Framing notes fold into F4-adjacent fixes (its "solved/near ceiling" phrasing leans on the AUPRC inflation its own mitigation table warns about).
- **glossary diff**: **ALIGNED** — all numbers match the ratified ADR-055; three wording fixes queued (F9). The DRAFT amendment file in the experiment dir is a superseded condensed copy → W18.

## 6. Doc sweep + external voices (Phase 4)

Mechanical sweep (methodology-audit, 303 docs): 0 critical / 25 warnings / 231 suggestions. The warnings are broken links — vendored `data/raw/**` READMEs (out of audit scope; tool-scoping note), ~10 dossier agent_index relative-path errors, B2_3_FINDINGS.md:111, and the DRAFT amendment's links (→ F15/W18). The 231 path:line suggestions are dossier→code drift; no load-bearing surface among them (all load-bearing surfaces were verified by the 30-verifier pass). Adjusted traffic light: **doc-hygiene YELLOW, verdicts GREEN** (the tool's volume-triggered RED counts vendored junk).

**External refutation (codex 0.137.0 + gemini 0.44.1), run against this register: see §9 — appended after both voices returned and were artifact-grounded.**

## 7. Findings register

> Severity scheme: **BLOCKER** (invalidates a ratified claim — none found) · **FIX-NOW** (wrong/stale statement on a public or handoff surface; correct before tag/push) · **FOLLOW-UP** (real work, queued; feeds the roadmap) · **COSMETIC** (note-only).

### FIX-NOW (15)

| ID | Location | Problem → fix |
|---|---|---|
| F1 | README.md:136-137 | Milestone rows stale (M0 close "pending: dossier"; M1 "pending" though closed; no spine row) → refresh table |
| F2 | NEXT_SESSION.md:3,10 | "do not push to close M0" + "41 commits on main" superseded → refresh or reduce to a pointer at SESSION-HANDOFF |
| F3 | M0_READINESS.md:153,148,156,174 | Tag text "55 ADRs" (53 on disk); "capacity-dependent spine" → axis-dependent; runbook predates the 38-commit arc → rewrite close texts (both variants drafted in the roadmap doc) |
| F4 | ADR-054:82 · SESSION-HANDOFF:320-321 · glossary:337-338 · lane-1/RESULTS_POINTER.md:22 · milestone-rethink-inputs.md:16 · announcement:33 | Stale "0.98–0.999 held-out types included" (A1 fix never propagated; artifact: per-type 0.956–0.984, prevalence floor 0.9265) → propagate corrected range |
| F5 | OOD_WALL FINDINGS.md:46-48 · glossary:145 | "collapse IS scope-blindness, confirmed both ways" violates own §A.4 prescription → soften to "consistent with" |
| F6 | B2_4_FINDINGS.md:54,64-68 | "trigger-word over-defense" mechanism language survives the B4 audit downgrade → annotate (visible, not causal) |
| F7 | SESSION-HANDOFF.md:303,310 | Axis-unqualified "capacity-dependent" headers vs corrected line 7 → qualify |
| F8 | docs/planning/README.md | Missing index rows (results-analysis + audit/roadmap docs) → add |
| F9 | glossary diff | "3/4 genuine dialects" misphrase; injecagent missing "uninformative, NOT a counterexample"; silhouette/ARI + carrier-axis entries missing frozen-MiniLM qualifier; stale "carrier became the spine" closer → reword |
| F10 | PORTFOLIO_PLAN.md:703 | Stale present-tense geometric-only carrier line → add resolution annotation |
| F11 | carrier FINDINGS.md:34 (+ADR-055:161) | Seed-0 (0.837) mixed with seed-mean (0.793) next to +0.205 → use the consistent pair / label the illustration |
| F12 | carrier criteria.md:156-161 · cross-family assemble.py:12,77 | Rev-1 row counts 2× under materialized (140 clusters/1680 pos) → correct with dated note |
| F13 | B4_FINDINGS.md:87 · B2_4_FINDINGS.md:133-136 · criteria.md:568-571 | Realized-composition drift (3,219/18,168/29,048/7,262) + "~38% near 1.0" conflation (28.9% vs 38.5% FPR; the conflation line sits in B4_FINDINGS.md:87 — register originally mislocated it) → reconcile to summary.json |
| F14 | upstream_issues.md:163 | "Production falsify_* loops unchanged" contradicted by 019dd6a → strike line |
| F15 | dossier agent_index ×~10 · B2_3_FINDINGS.md:111 | Broken relative links (wrong ../ depth; misnamed ADR-052 target) → batch fix |

### FOLLOW-UP (18)

| ID | Item | Substance |
|---|---|---|
| **W1** | **MiniLM truncation artifact** (NEW) | max_seq_length=256 + suffix injection ⇒ **66.5% of table / 44.1% of code** positives carry zero attack tokens into the embedder (codex re-measured); EDA geometry partly literal truncation. Owed: email-only silhouette check + disclosure in EDA FINDINGS. Conclusion plausibly survives (email untruncated; 2-class control; cheap-rung corroboration) |
| **W2** | **InjecAgent materialization bug** (NEW) | materialize_datasets.py:529 concatenates instead of substituting `<Attacker Instruction>`; all 2,108 positives keep the placeholder → class separable by template artifact; "tool-output dialect" framing structurally off. Conservative for verdicts (slice already ruled uninformative). Fix+re-derive or retire slice with dated note |
| W3 | falsify_ood_wall.py write-gate | No --out; clobbers committed verdict JSON (happened during this audit; restored). Add gate |
| W4 | Seed-coupling anti-conservatism | Shared defect (carrier hand-rolled + v1.8.0-as-used); quantified: CIs widen ×1.2–1.7, **no flips**. Disclose in criteria; consider upstream option |
| W5 | Dialect permutation conventions | Row-level shuffle + no +1 floor (diagnostic-only) → note |
| W6 | Baseline gate failures | cheap_gpu_monitor.py: 3 ruff + 2 unregistered imports → fix + register |
| W7 | agent-harness-v0 retrofit | Checkpoint decision A/B (§5); plus Claim-Boundaries line for the construction-property rows |
| W8 | Provenance dirs disposition | Checkpoint decision a/b/c (§5); manifest drafted; recommend (b) |
| W9 | PG1 0.998 provenance | Rests on gitignored tree → commit the 9 reference metrics.json or mark derived-from-disk |
| W10 | Carrier rule-sensitivity | Under §6.5's sign-only rule carrier would read SURVIVES; SMALL-THROUGHOUT rests on the (pre-registered) ½-knob → one-line disclosure; fix "never large" gloss (cross-family criteria:159) |
| W11 | Cluster-unit disclosure gaps | fujitsu pairing vacuous under stratification (iid); bipia 3-neg-cluster thinness unflagged → criteria notes |
| W12 | Mirror/corpus-style confound | Missing from spine-level caveat list (ADR-055:256, decisions/README row, glossary, verdict.json) → add |
| W13 | "wall GREW" headline | Point-only Δ+0.052 (seed-range +0.020…+0.075, no CI) presented as established in headlines → soften/range |
| W14 | injecagent data nits | 2× duplicated positives; 45 inner⊗val dups → dated note |
| W15 | Reproduction-audit disclosures | §6.5 scheme deviation undisclosed; "pure MC noise" overstated; dialect_balanced exclusion unmentioned → README notes |
| W16 | PAD CI never computed | criteria.md:101 promised CI; n_bootstrap=0; V9 zero-width whiskers → compute or annotate |
| W17 | Arm-B index-convention defect stands | leakage_gate.py:85 inverted reading (harmless, 0 pairs); criteria Rev-4 "fixed" claim wrong as stated → fix code + correct claim |
| W18 | DRAFT amendment redundant | Superseded condensed copy of ratified text → archive/delete (user-led) |

### COSMETIC (9)

C1 rounding nits (−0.008 vs −0.0075; "0.000" vs −0.003) · C2 criteria:116 val-ROC vs implemented val-PR-AUC selection wording · C3 "95% CI" header for one-sided-95% · C4 verdict.json bridging rung-unlabeled · C5 glossary gap-score umbrella vs T's actual form · C6 stale "(PG1 once gate granted)" · C7 231 dossier path:line drift + vendored-README link noise (tool-scoping) · C8 run_b2_4.py threshold=inf sentinel reports 0.0 over-defense · C9 latent NaN path in single-class bootstrap draws (unreachable today) · C10 stale TODO/NotImplemented comments in folds_dialect.py:18-19,171-172 for the implemented B+ loading (codex NEW).

## 8. Uncommitted-artifact disposition table (Checkpoint-1 decisions)

| # | Path | Audit result | Options (recommend bold) |
|---|---|---|---|
| 1 | docs/glossary.md (modified) | ALIGNED; 3 wording fixes queued (F9) | **commit after F9 fixes** / commit as-is / hold |
| 2 | docs/planning/results-analysis-2026-06-08.md | FAITHFUL; framing nits | **commit (+ optional framing softening + index row)** / hold |
| 3 | experiments/agent-harness-v0/ | Valid within fence; byte-stable; tests green | **commit with retrofit A (retrospective trio)** / commit with B (exploratory banner) / hold |
| 4 | tests/experiments/test_agent_harness_v0.py | 6/6 green | **commit with #3** |
| 5 | B3_results_runpod_all27_lora/ (421MB) | Fully reconciled, byte-identical | (a) manifest-only / **(b) commit 16 metrics.json + sha256 manifest; parquets stay local** / (c) HF Hub |
| 6 | B3_results_runpod_bplus_cheap_lora/ (324MB) | Fully reconciled | same as #5 — **(b)** (12 metrics.json) |

## 9. External refutation results (codex 0.137.0 · gemini 0.44.1)

Both voices received the full register (42 IDs) with an adversarial refute-by-default mandate, running read-only inside the repo.

- **codex: 36 CONFIRMED, 6 WEAKENED, 0 REFUTED.** The weakenings are refinements, applied above: W1 truncation shares re-measured as table **66.5% / code 44.1%** (code worse than first reported); W9's 0.998 quote locus is `AUDIT_2026-06/verification_report.md:87` + results-analysis:1299 (not ADR-054's text); W14's 45-straddle attribution is BIPIA split overlap (folds_dialect.py:200), not the injecagent pool; F13's "~38% near 1.0" wording sits at B2_4_FINDINGS.md:88 (composition drift at :133-135 confirmed); C5/C7 minor (path:line drift count 244, not 231).
- **codex NEW (accepted after grounding):** C10 — `folds_dialect.py:18-19,:171-172` retain TODO/NotImplemented comments for the B+ direct-base loading that :181-183 implements; and the DRAFT amendment's line 64 claims no cross-family verdict.json exists while it does — folded into W18's archive rationale.
- **gemini: 36 CONFIRMED, 1 REFUTED, 5 CANNOT-VERIFY.** The single refutation (W1: "max_seq_length=256 appears in neither script") **fails artifact-grounding**: the limit is the embedding model's own `sentence_bert_config.json` (codex-confirmed; live-tokenizer-measured by the original verifier). Rejected — the third gemini counter-hallucination this procedure has caught. Its CANNOT-VERIFYs are checks it didn't execute (F15/W11/W14/C5/C7), all covered by codex or the verifier fan-out.

**Net effect: no finding removed; W1 strengthened; four wordings refined; one cosmetic added (C10).**

## 10. Verification appendix (re-runnable)

- Gates: `make lint && make test && make contracts`
- Verdict scripts: `uv run python experiments/REPRODUCTION_2026-06/reproduce_{6_5,carrier,dialect}.py` (writes /tmp; compare to committed `*_reproduction.json`); `uv run python experiments/cross-family-transfer/b4_verdict.py` — **do not run `falsify_ood_wall.py` until W3 lands (it overwrites the committed verdict file)**
- Parquet recompute: `/tmp/audit-recompute/recompute.py` (+`recompute_b24.py`), results in `/tmp/audit-recompute/results.json`
- Retrains: harness/run_b2_3/run_b2_4 invocations in `/tmp/audit-retrain/` (commands in the dirs' metrics provenance)
- Seed-coupling quantification: `/tmp/v-st-hand/{carrier,dialect}_shared_vs_indep.py` + `*_out.log`
- Harness rerun: `run.py --backend scripted` → diff vs `results/scripted.jsonl` (byte-identical expected)
- Provenance manifest data: sha256 blocks in §5 agent transcript; one corrected hash: fujitsu seed=2 B+ = `ba9d402a5ffa1689f16b306ce87964dcb9a05becd98d7a97753a6685f033864d`
- Immutability ledger: `git log --oneline --since=<audit-date> -- <subject paths>` per §2
