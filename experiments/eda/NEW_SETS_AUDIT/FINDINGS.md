# Phase-2 new-dataset EDA gate — FINDINGS + PROPOSED roles (2026-06-03)

**Status: evidence gathered; roles PROPOSED, not finalized.** Per the session's hard rule (no research-role
or published spec without real EDA) this is the review checkpoint. Nothing has been written to the canonical
atlas (`docs/research/datasets/agent_index/`) or the ledger — that is the post-review follow-up. Specs in
`configs/data/dataset_specs.yml` carry only `load_shape_only: true / research_role: PENDING_EDA`.

Evidence: materialize `MANIFEST.json` · survey audits `experiments/eda/<bibkey>/audit.json` · geometry
`experiments/eda/NEW_SETS_AUDIT/geometry/cross_dataset_geometry.json` · leakage
`experiments/eda/NEW_SETS_AUDIT/jailbreakdb_leakage.json` · content `…/content_samples.json`.

## Proposed-role slate

| set | license | shape | EDA verdict | PROPOSED research-role |
|---|---|---|---|---|
| **browsesafe** | MIT | 14.7K binary (no/yes), full-HTML | clean; PAD-vs-BIPIA **1.968** (distinct dialect); **zero** E4 leakage (novel) | **indirect-HTML TEST anchor — the prize** (new carrier axis; the E7 "2nd indirect dialect") |
| **neuralchemy** (core) | Apache | 6.3K binary 60/40; has source+group_id | leakage scan (G-EDA-1): exact 303 (4.8%, jbb 300) + near 363 (5.8%) + ~35% declared-from-our-sources; **3,787 clean (60%) recoverable** but modest + hackaprompt-provenance-entangled | **PARK** (user-leaned, evidence-backed) — dedup-and-use documented as the option if a clean Apache trainer is later wanted |
| **falsereject** | CC-BY-**NC** | 15.8K all-benign over-refusal | benign prompts crafted to look unsafe (textbook over-refusal); leakage-clean | **benign-FPR / over-defense control** (like notinject/xstest/orbench); NC ⇒ eval-only |
| **aegis2** | CC-BY | 33K binary safe/unsafe | `prompt_label` = content-safety (criminal/sexual/harassment), **not injection-presence** → OFF-AXIS | **PARK for injection**; catalogue as toxicity/content-safety reference (optional hard-negative source) |
| **jailbreakdb** | CC-BY | 1.54M records (not 12.2M — line-count artifact) | **SEVERE leakage** + **scrambled labels** | **PARK — not slate-eligible** (see below) |
| **fujitsu** (B1 core) | CC-BY-4.0 | 10,943 poison / 10,943 benign (balanced, clean RAG-doc poisoning) | gate GRANTED 2026-06-03 (id `Fujitsu/agentic-rag-redteam-bench`); CORE clean; augmented configs leak (gandalf 777 verbatim, jbb 9); B2=image; B4 all-success=true | **indirect/RAG-injection TRAIN or TEST (B1 core)** — 2nd new carrier axis; EXCLUDE augmented configs, skip B2 |
| agentdyn | **MIT** | 60 tasks + 560 injection cases (verified, AgentDojo) | runs/=48,672 trajectory JSONs; not (text,label) | **execution/Lane-5 candidate**; extract the 560 cases only if it earns a role |
| agentdam | **CC-BY-NC** | privacy/data-minimization (verified, VisualWebArena) | privacy-leakage ≠ injection | **OFF-AXIS** — catalogue-only-with-reason |

## The two decisive findings (why the rigor mattered)

### JailbreakDB — PARK (severe contamination + unreliable labels)
- **Exact overlap with our universe = 19,458 rows** (full 1.54M scan): `shen_dan 17,783` (almost all via its
  `DAN` source = shen's in-the-wild prompts), `jackhhao 1,387`, `jbb 288` (via JBB-Behaviors/AdvBench/HarmBench).
  Plus a ~2.1% near-dup paraphrase tail. ⇒ using JailbreakDB **contaminates any split holding out
  shen_dan/jackhhao/jbb**.
- **Labels scrambled** (content deep-dive): the classic `DAN` jailbreak sits in `text_regular` (jailbreak=0);
  benign Safe-RLHF questions sit in `text_jailbreak` (jailbreak=1). Provenance explains it — JailbreakDB
  mixes instruction-tuning corpora (OpenHermes 494K, glaive-code 181K, metamath, alpaca, platypus) with
  jailbreak/harm sets; `jailbreak` is not the intuitive "is-a-jailbreak" label.
- **Record-count caveat (resolved):** 1,539,874 records (445,752 + 1,094,122); the materialize "12.2M" was a
  multi-line-quoted-field line count. The scan read both CSVs to EOF → complete.

### browsesafe — the prize (a genuinely new carrier axis)
- PAD-vs-BIPIA **1.968** (near-max separability) ⇒ HTML-carrier indirect is a **distinct dialect** from
  text-carrier indirect (BIPIA) — exactly the multi-indirect-corpus gap E7 flagged. Zero E4 leakage (novel
  content). Clean injection-vs-benign in realistic HTML. Caveat: content p50 46KB / p95 140KB → needs a
  truncation strategy for modeling (high pct_over_8192).

## Family re-examination (D4 directive)
Frozen-MiniLM silhouette ≈ 0 across the board (the known weak-separation regime) ⇒ no provisional family
assignment is **contradicted**. browsesafe's high PAD-vs-BIPIA **affirms** the new `indirect_html` family.
neuralchemy→`aggregated` is consistent with its multi-source composition. **4.1 taxonomy stands; no revision forced.**

## Deferred to the post-review follow-up (NOT done this pass)
Finalize research-roles · atlas `agent_index/` entries (30→catalogue the earners + park the rest) + count
bumps · ledger "Newly-surfaced 2026-06-03" table · promote provisional specs (source-dedup neuralchemy;
decide browsesafe truncation; mark jailbreakdb/aegis2 parked-with-reason).
