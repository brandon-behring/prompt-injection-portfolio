# Dataset acquisition deep-dive — what we can actually acquire (2026-06)

> **Independent acquisition audit of the full ~30-dataset candidate universe.** Question: *which can we
> actually get, under the access we now hold?* Method: **live load-tests under the user's HF credentials
> (BBehring)** via `huggingface_hub.dataset_info` + streaming peeks (no full downloads), plus the index
> atlas + the prototype `source_manifest.yaml` + targeted web checks for withheld/unreleased sets.
> Read-only verification — nothing downloaded in bulk, nothing committed.
>
> **Verification provenance is marked per row:** `live✓` = load-tested this session; `survey✓` = loaded
> in the EDA survey (⇒ acquirable); `atlas/web` = from the index/manifest/web (two fan-out auditors for
> the git + agentic groups were cut off by a session usage limit — those rows are atlas/manifest/web-sourced
> and flagged for an optional live re-verify after the limit resets).

## Bottom line

> **Re-verified + materialized + widened-source audit, 2026-06-02/03.** Live re-probe: universe stable; the
> assumption double-check overturned priors — **InjecAgent ships static `(text,label)`**, **HackAPrompt is
> MIT**, and **the three Lakera sets (Gandalf×2 + Mosscap) are MIT** (an `isinstance(cd, dict)` probe-bug had
> read `None`); Harelix 404 re-confirmed (a web-cache misreports it live). **24/24 materialized** to the
> gitignored `data/raw/` (3.19 M rows, **1.09 GB** after pruning WAInjectBench's 4 GB image modality). A
> **widened scan (2026-06-03)** then surfaced ~19 live-verified NEW datasets. See *Materialization round* +
> *Widened source audit* below.

Of ~30 core datasets, **3 are out of reach** (Harelix — 404 re-confirmed; PINT — withheld; Indirect-in-the-Wild
— no public data + no stated release plan, exhaustively checked across HF/GitHub/Kaggle/Zenodo/OSF/USENIX-AE);
**~5 are *loadable but unlicensed*** (jayavibhav×2, xTRam1, Tensor Trust, WAInjectBench — internal EDA only);
everything else is cleanly acquirable — a few needing a **documented build** (BIPIA qa/abstract) or
**derivation** (LLMail-Inject + InjecAgent, both derived to disk). **Your gate approvals worked** — WildGuardMix,
walledai/XSTest, Fujitsu all load. The one approval that *can't* help is PINT (Lakera withholds the data itself).

## Master acquisition table

| Dataset | Family | Acquire verdict | License | Verified | Use / caveat |
|---|---|---|---|---|---|
| WildGuardMix (allenai) | toxicity-guard | **YES — gate now cleared** | ODC-By | live✓ | 86.7k+1.7k; harm/refusal/**adversarial** flags → benign/harm control + Lane-4 gate |
| HackAPrompt | direct | **YES** | **MIT** (re-verify 2026-06-02; was carded CC-BY-4.0) | live✓ 2× | 601k; label=`correct` (81% pos, skewed); trivial map → CF-train |
| JBB-Behaviors | jailbreak | **YES** | MIT | live✓ | `behaviors`: harmful/benign goals (100/100) → CF-test OOD slice |
| LLMail-Inject (microsoft) | indirect | **YES — needs derivation** | MIT | live✓ | Phase1/2 competition **logs** (subject/body/objectives/output); derive labels from `objectives` (attack-success) → big indirect train/test |
| jayavibhav/prompt-injection | direct | YES-loads / **license-blocked** | **none** | live✓ | 327k text/label 0/1; loadable ≠ licensed → EDA-only |
| jayavibhav/prompt-injection-safety | direct | YES-loads / **license-blocked** | **none** | live✓ | actually **binary** (survey "multiclass" was wrong); 60k balanced; undocumented labels → EDA-only |
| xTRam1/safe-guard | direct | YES-loads / **hold** | **none** | live✓ | 10.3k (70/30); citation "mismatch" benign (GLAN = inspiration); GPT-3.5 synthetics → redistribution unclear → EDA-only |
| Harelix Mixed-Techniques | direct | **NO — 404** | — | live✓ 2× | **404 re-confirmed 2026-06-02** (a web-search cache misreports it live w/ Apache-2.0 + dl-stats; the live `dataset_info` API is 404) → **drop** |
| deepset/prompt-injections | direct | YES | Apache-2.0 | survey✓ | 662; bilingual smoke set |
| guychuk/benign-malicious | direct | YES | Apache-2.0 | survey✓ | **464k — largest clean direct** → CF-train primary |
| hendzh/PromptShield | direct | YES | Apache-2.0 | survey✓ | 43k native splits; **has unicode/obfuscated cases** → CF-train + Lane-1b |
| reshabhs/SPML | direct | YES | MIT | survey✓ | 16k; system-vs-user structure |
| jackhhao/jailbreak-classification | jailbreak | YES | Apache-2.0 | survey✓ | 1.3k balanced |
| lmsys/toxic-chat | toxicity-guard | YES **(NC)** | **CC-BY-NC-4.0** | survey✓ | 10k; toxicity+jailbreak cols; **non-commercial** caveat |
| TrustAIRLab/in-the-wild (DAN) | jailbreak | YES | MIT | survey✓ | community jailbreaks; high obfuscation rate |
| leolee99/NotInject | over-defense | YES | MIT | survey✓ | 339; already used (M1 benign-FPR) |
| natolambert/xstest-v2 | over-defense | YES | CC-BY-4.0 | survey✓ | 450; safe/unsafe contrast |
| bench-llm/or-bench | over-defense | YES | CC-BY-4.0 | survey✓ | 80k over-refusal eval |
| GenTelLab/gentelbench-v1 | aggregated | YES | Apache-2.0 | survey✓ | 177k harm taxonomy (verify composition) |
| BIPIA (microsoft) | indirect | YES (on disk) | MIT (code; derived sets CC-BY-SA) | live✓ | email/code/table ready; **qa/abstract need NewsQA+XSum build** (below) |
| InjecAgent | agentic | **YES — ships STATIC cases** | MIT | live✓ 2× | `test_cases_*.json`/`attacker_cases_*.jsonl` load directly as (text, attack_type) **without an agent run** (full ASR still needs execution) → usable indirect/agentic CF-test |
| Open-Prompt-Injection | direct | YES — needs derivation | MIT | live✓ | toolkit (`create_task` factories); not pre-labeled pairs |
| InjecGuard / PIGuard | aggregated | YES | MIT | live✓ | repo redirects → `leolee99/PIGuard`; **bundles `BIPIA_text/code.json` → confirmed leakage** vs any BIPIA test |
| WAInjectBench | indirect | YES-loads / **unlicensed** | **none (confirmed)** | live✓ | drop-in {text,label} JSONL, but **no LICENSE anywhere** → EDA-only |
| Tensor Trust | direct | YES-loads / **unlicensed** | **none (confirmed)** | live✓ | 172k; "permissive" reputation **unbacked** (paper ToU = gameplay rules) → EDA-only |
| AgentDojo | agentic | YES — **high cost** | MIT | live✓ | `pip install`; agent *environment*, not (text,label) |
| Agent Security Bench | agentic | YES — **high cost** | MIT | live✓ | ASR framework; outputs metrics not rows |
| WASP | agentic/indirect | YES — **very high cost** | CC-BY-NC-4.0 | live✓ | Docker sandbox ~4–6h/run; **non-commercial** |
| PINT (Lakera) | over-defense | **NO — withheld** | harness MIT | live✓ 2× | repo `lakeraai/pint-benchmark` (not `lakera/`) ships only `example-dataset.yaml`; 4,314 inputs withheld by design; request opensource@lakera.ai |
| Indirect-in-the-Wild | indirect | **NO — no public release** | none stated | live✓ 2× | arXiv:2604.27202 (Khodayari; + the confusable 2601.07072 Chang/USENIX) — **no public data + no stated release plan** (re-checked 2026-06-02; prior "release pending" was optimistic); author email only |

## Buckets (the actionable summary)

**A. Ready to use — permissive license, acquirable now (~14):** deepset, guychuk (464k), PromptShield
(43k, +Lane-1b), SPML, jackhhao, in-the-wild/DAN, NotInject, XSTest, OR-Bench, GenTel, HackAPrompt
(601k), JBB-Behaviors, BIPIA (email/code/table), InjecAgent, Open-Prompt-Injection, InjecGuard
(leakage-caveat), **WildGuardMix** (gate cleared). → the cross-family + benign-FPR + Lane-1b material.

**B. Acquirable but LICENSE-BLOCKED for publication — internal EDA only (5):** jayavibhav/prompt-injection
(327k), jayavibhav/prompt-injection-safety (60k), xTRam1/safe-guard (10k), **Tensor Trust (172k —
confirmed: no LICENSE artifact anywhere, incl. the official `HumanCompatibleAI/tensor-trust-data` repo;
"permissive" reputation unbacked)**, **WAInjectBench (confirmed: no LICENSE)**. *Loadable ≠ licensed* —
fine to explore locally; must clear license (author contact) before any released benchmark/model.
**CORRECTION (2026-06-03):** the three Lakera sets (`gandalf_ignore_instructions`, `gandalf_summarization`,
`mosscap_prompt_injection`) were briefly listed here as unlicensed — they are in fact **MIT** (3-way
verified: HF tag + `cardData.license` + raw-README YAML); an earlier `isinstance(cd, dict)` probe-bug
read `None` (`cardData` is an object, not a dict). They are **bucket A**, materialized to `data/raw/`
(out of quarantine), and usable in a *published* cross-family TRAIN slate.

**C. Build-required (documented, not approval-blocked):** BIPIA **qa** (← NewsQA, MIT, `load_dataset(..,
trust_remote_code=True)` or BIPIA's docker) + **abstract** (← XSum, EdinburghNLP) → run BIPIA's
`process.py`. A few-hours data-engineering task; **not** an external-license wall.

**D. High acquisition cost (adaptation/derivation):** LLMail-Inject (derive labels from competition
logs), **InjecAgent** + **Open-Prompt-Injection** (execution/derivation toolkits, not pre-labeled),
AgentDojo / ASB / WASP (agent environments, not text/label). Defer unless an agentic lane opens.

**E. Not acquirable (3 — all double-checked 2026-06-02):** Harelix (**404 re-confirmed** on the live API;
a web-search cache misreports it live with Apache-2.0 — ignore it), PINT (withheld; repo
`lakeraai/pint-benchmark` ships only `example-dataset.yaml`; request-only via opensource@lakera.ai).
**Indirect-in-the-Wild**: re-checked — **no public data and no stated release plan** for arXiv:2604.27202
(Khodayari) *or* the confusable arXiv:2601.07072 (Chang/USENIX); the prior "stripped release pending" was
optimistic. Author email (shl.khodayari@gmail.com / pellegrino@cispa.de) is the only speculative path —
worth a watch/ask but do not count on it. (No outreach drafted this round — verdicts only.)

**Special caveat — non-commercial:** ToxicChat + WASP are CC-BY-NC-4.0 → usable for research/eval, but
flag if any commercial use is contemplated.

## What this unlocks (tie-back to the EDA plan)

- **Cross-family #1 (the audit's critical experiment) is over-supplied.** Direct TRAIN: guychuk (464k),
  PromptShield, HackAPrompt, deepset, jackhhao, SPML, GenTel — all bucket A. Indirect TEST: BIPIA,
  InjecAgent, JBB, + LLMail-Inject (derivation). Benign controls: NotInject, XSTest, OR-Bench. The
  extended-arm slate (your option 1) is fully feasible on permissive licenses alone — the bucket-B sets
  are optional bonus, not needed.
- **Lane 1b (char-injection):** PromptShield (unicode/obfuscated cases) + BIPIA obfuscation sub-family +
  high-obfuscation-rate sets (in-the-wild/DAN) → ready candidate pool.
- **Lane 4 (saturation gate):** WildGuardMix (now cleared) + PromptShield; PINT remains request-only.
- **The license distinction is the only real gate:** bucket B is fine for the EDA atlas (E1–E7) but must
  be cleared before publication; PINT/Indirect-in-the-Wild are the sole hard exclusions.

## Materialization round (2026-06-02/03) — full corpus persisted to disk

Acting on the "full materialize" decision: `experiments/eda/materialize_datasets.py` persisted **24/24
accessible datasets** to the **gitignored** `data/raw/` (+ `data/raw/MANIFEST.json`) — **~3.19 M rows
across all files, now 1.09 GB** (was 5.37 GB before pruning). Unlicensed sets quarantined under
`data/raw/_eda_only_unlicensed/` (+ README). **2026-06-03 corrections applied:** Gandalf×2 + Mosscap
relocated out of quarantine (MIT → bucket A); `xstest` switched to the canonical `walledai/XSTest`
(450 rows, replacing the `-copy` mirror); the script is now **idempotent** (re-runs skip cached, no re-clone).

- **Tier-3 derivations succeeded:** LLMail-Inject → **461,640** rows (`text`=subject+body; `defense_undetected`
  parsed ~50/50: True 231,767 / False 229,873); InjecAgent → **2,108** static `(text, attack_type)` rows
  (no agent run — the corrected assumption); WAInjectBench → **3,698** text rows (label-by-directory).
- **Row-count caveat:** `MANIFEST.json` `n_rows` = **all rows across all files in each repo snapshot**, so
  multi-config repos *exceed* their carded binary-task subset — toxicchat 428k (carded 10k), shen_dan 21k
  (666), spml 86k (16k), jackhhao 43k (1.3k). Subset at load time via `dataset_specs.yml`
  (config/splits/label). Single-config sets match exactly (guychuk 464,470 ✓, hackaprompt 601,757 ✓,
  gentelbench 177,015 ✓).
- **Disk note (DONE 2026-06-03):** WAInjectBench's ~4 GB image modality + `.git` history pruned → only the
  3,698 text rows (`data/text`) kept; total corpus dropped 5.37 GB → **1.09 GB**.
- **Not materialized (recorded as manifest rows):** Tier-4 execution-only (Open-PI, AgentDojo, ASB, WASP);
  Tier-5 unavailable (Harelix, PINT, Indirect-in-the-Wild); PIGuard **available-but-not-fetched** (BIPIA
  leakage); BIPIA qa/abstract **deferred** (opt-in `--build-bipia`).

## Newly-surfaced 2026-06-03 — Phase-2 expansion (EDA-gated; 8 sets assessed)

A widened scan surfaced 8 new candidates; all were **EDA-gated** (materialize → survey → cross-dataset
geometry → leakage scan → content deep-dive) before any role. Evidence:
`experiments/eda/NEW_SETS_AUDIT/{FINDINGS.md,*_leakage.json,fujitsu_audit.json,content_samples.json}` +
`geometry/cross_dataset_geometry.json`. Roles are research-roles (prose; the codebase `role` field is a
loader-shape switch). **Headline: 2 new indirect carrier axes (HTML + RAG)** → BIPIA is no longer the lone
indirect dialect (enables the leave-one-indirect-out experiment).

| Dataset (id) | Family | License | EDA verdict / research-role | Leakage (vs our universe) | Use / caveat |
|---|---|---|---|---|---|
| `perplexity-ai/browsesafe-bench` | indirect_html | MIT | **indirect-HTML TEST anchor** (prize #1) | clean (PAD-vs-BIPIA 1.968; 0 E4 pairs) | `content`→`label`{no,yes}; full-HTML 34K tok → **head+tail** truncation; own-split leakage → own folds |
| `Fujitsu/agentic-rag-redteam-bench` (B1) | indirect_rag | CC-BY-4.0 | **indirect-RAG TRAIN/TEST** (prize #2) | core clean; augmented configs leak (gandalf 777 verbatim, jbb 9) | **B1 per-document only** (poison/benign 10,943 each); exclude augmented configs; skip B2 image; gate granted 2026-06-03 (handoff id `Fujitsu/agentic-rag` 404s) |
| `neuralchemy/Prompt-injection-dataset` (core) | aggregated | Apache-2.0 | **PARK** (dedup-and-use viable but deferred) | exact 303 (jbb 300) + near 363 (5.8%); ~35% declared-from-our-sources; 3,787 clean (60%) recoverable | dedup-and-use documented as the option if a clean Apache trainer is later wanted |
| `AmazonScience/FalseReject` | over_defense | CC-BY-**NC** | **benign-FPR / over-refusal control** | leakage-clean | all-benign prompts crafted to look unsafe; eval-only (NC) |
| `nvidia/Aegis-AI-Content-Safety-Dataset-2.0` | toxicity | CC-BY-4.0 | **PARK for injection** (off-axis) | tiny (jackhhao 2) | `prompt_label`{safe,unsafe} = content-safety, NOT injection-presence; toxicity reference |
| `youbin2014/JailbreakDB` | jailbreak | CC-BY-4.0 | **PARK — not slate-eligible** | **SEVERE**: exact shen_dan 17,783 / jackhhao 1,387 / jbb 288 (full 1.54M scan) | scrambled labels (DAN→"regular", benign→"jailbreak"); instruction-tuning+jailbreak grab-bag (1.54M records, not 12.2M = line-count) |
| `SaFo-Lab/AgentDyn` (github) | agentic | MIT | **execution / Lane-5 candidate** | n/a (env) | 60 tasks + 560 injection cases on AgentDojo; runs/=48,672 trajectory JSONs; derive (text,label) only if it earns a role |
| `facebookresearch/ai-agent-privacy` (=AgentDAM, github) | agentic | CC-BY-NC | **OFF-AXIS — catalogue-only** | n/a (env) | privacy-leakage / data-minimization (VisualWebArena), not injection detection |

**Net:** 2 prizes (browsesafe + fujitsu B1), 1 benign control (falsereject), 1 park-salvageable (neuralchemy),
2 park (aegis2 off-axis, jailbreakdb contaminated), 2 env (agentdyn execution, agentdam off-axis). The 4
indirect dialects (BIPIA / browsesafe / fujitsu / InjecAgent) are mutually distinct in MiniLM geometry
(PAD-vs-BIPIA 1.94–1.99) → a genuine leave-one-indirect-corpus-out test. `Fujitsu` was gate-blocked under the
wrong handoff id; corrected + gate granted. **EDA-only / not-yet-cleared:** falsereject + agentdam are NC.

## Provenance + honesty note

- **Live-verified this session (8):** WildGuardMix, HackAPrompt, JBB, LLMail-Inject, jayavibhav×2,
  xTRam1, Harelix — load-tested under BBehring (`dataset_info` + streaming).
- **Survey-confirmed (11):** loaded in the prior EDA survey ⇒ acquirable (licenses from
  `source_manifest.yaml` / cards).
- **Live re-verified (git + agentic + withheld, 11):** the two groups first cut by the session limit were
  re-run live (GitHub license API + raw `LICENSE`/README probes + paper PDFs). Net findings:
  WAInjectBench + Tensor Trust carry **no LICENSE artifact** (all-rights-reserved by default);
  InjecGuard/PIGuard is MIT but **bundles `BIPIA_text/code.json`** (confirmed leakage risk);
  AgentDojo/ASB MIT, WASP CC-BY-NC; PINT data withheld (only `example-dataset.yaml` ships);
  Indirect-in-the-Wild has **no public data and no stated release plan** (re-checked 2026-06-02 —
  2604.27202 + the confusable 2601.07072; the earlier "release intended" was optimistic) → author email
  only. All rows in the table are now live-verified (2× for the re-probed sets).

## Scope guard
- The *deep-dive* (above the materialization section) was verification-only: streaming peeks + metadata.
  The **2026-06-02 materialization round** then bulk-downloaded to the **gitignored** `data/raw/` — **no
  dataset committed** (gitignore confirmed), **no canonical research record edited** (this is a planning ledger).
- License calls are *advisory* — bucket B needs a real license clearance before any published use; this doc flags, does not clear.

---

*Sources: live `huggingface_hub`/`datasets` probes under user BBehring (this session);
`experiments/eda/survey_v2_summary.json`; `../prompt-injection-detection-submission/configs/data/source_manifest.yaml`;
`docs/research/datasets/agent_index/` (atlas); web (Maluuba/newsqa, Lakera PINT, arXiv:2604.27202).*
