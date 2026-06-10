# Roadmap refresh — 2026-06-09/10 (STANDING ROADMAP SURFACE — ratified Round 31, 2026-06-10)

> **Status (2026-06-10):** ratified into `PORTFOLIO_PLAN.md` Round 31. Forks A/B/C below are
> **decided** (A = variant b, held on accounts · B = retrospective trio, own surface · C = C1);
> the fork analyses are kept for the record. Live state: §1 table.

**Inputs:** the ratified 3-axis spine (ADR-054/-055 + amendments) · the full re-audit (`consolidated-audit-2026-06-09.md` — spine holds, 15 FIX-NOW / 18 FOLLOW-UP) · `results-analysis-2026-06-08.md` "Paths forward" · `milestone-rethink-inputs.md` (folded in + retired, §6) · `M0_READINESS.md` held bundle · DF-11 · the 13-chapter outline.

**Where the science stands.** The first experimental arc is complete and audit-hardened: attack-type transfer is solved at the LoRA ceiling (FALSIFIED wall), carrier is capacity-attenuated with one residual table wall (+0.205, provisional n=3), cross-family is the one capacity-resistant axis (SURVIVES, +0.365, direct data doesn't bridge). Nothing experimental is in flight; every queued item below is user-led.

## 1. Recommended sequence (the short version)

| Priority | Work package | Size | Status / gate |
|---|---|---|---|
| **P0** | **Consolidation session** — the audit's 15 FIX-NOWs, the 6 uncommitted-artifact dispositions, W6 + broken links, SESSION-HANDOFF refresh | ~1 session, $0 | **DONE** — Checkpoint-1 approved; committed `d92426a` (pushed) |
| **P1** | **v0.1.0 close** — Fork A **decided: variant (b)** full-spine close (ff-merge → tag → release → announce) | ~15-min runbook | **HELD** — accounts (unchanged human gate); runbook staged in `M0_READINESS.md` |
| **P1.5** | **Methods-hardening mini-arc** — W1 email-only silhouette check (conclusion SURVIVES), W2 injecagent fix + slice retirement, W3 write-gate (+3 tests), disclosure notes W4/W5/W10/W11/W12/W13/W14/W15, W9 (9 reference metrics committed), W16 PAD CI, W17, W18 archive | ~1 session, $0 | **DONE** (2026-06-10; gates 67 tests + 13 contracts green) |
| **P2** | **Lane 2: carrier/table training arc** — Fork C **decided: C1** (pre-registration first; C2 mechanism pre-reg drafts during C1 GPU waits) | pre-reg + cheap rungs free; lora ~$1–5 | criteria.DRAFT this session → separate present-first ratification before any run |
| **P3** | Dossier sprint · Lane 3/4/5 per ladder · agent-harness-v1 (v0 adopted → unblocked) | — | user-led |
| **When unblocked** | DF-11 carrier/clustered re-lock (eval-toolkit#93) · carrier n=5 retest (license gate) | small | upstream ships |

## 2. Fork A — v0.1.0 close timing/scope (the 38-commit question) — **DECIDED: (b), held on accounts**

`main` = `ee397a7` (post-M0-merge, 2026-06-01). The session branch holds 38 fast-forwardable, already-pushed commits = the entire carrier-amendment + cross-family arc + audits. The staged tag text (M0_READINESS.md:148-162) is stale either way (F3: "55 ADRs" vs 53; "capacity-dependent" vs the ratified axis-dependent wording; runbook's recorded main SHA also stale).

- **(a) Tag `main` as it stands (`ee397a7`).** Snapshot = M0 + M1 + Round-30 re-ladder, *without* cross-family. Honest but instantly dated: the tree's own docs carry the since-amended "capacity-dependent spine," and the strongest result (cross-family SURVIVES) is excluded from the release the announcement describes.
- **(b) Fast-forward the 38 commits into `main`, then tag (RECOMMENDED).** One `git merge --ff-only` (no history rewrite; commits already public on the session branch). The release then matches the ratified record, the announcement can tell the 3-axis story, and the audit's FIX-NOWs (P0) land *before* the tag so the snapshot is clean. Still accounts-gated for the announce step (close + announcement land together, per the standing decision).
- **(c) Keep holding** — no change; F3 text fixes still required eventually.

### Pre-drafted tag message — variant (b) (replaces M0_READINESS.md:148-162)

```
M0 close (v0.1.0): public pre-alpha portfolio + the three-axis OOD spine

Snapshots the M0 framework + the complete first experimental arc:
- Public repo, pre-alpha banner (through v0.7.0); 13-chapter textbook skeleton; 6-lane
  experiment-record framework; 210-entry research dossier (5 topics, 97% verified); Docker
  repro; ETHICS/SECURITY/CODE_OF_CONDUCT; 53 ADRs.
- The axis-dependent OOD spine (ADR-055 + amendments) — all three axes pre-registered,
  write-gated, audited, and independently reproduced:
  attack-type FALSIFIED at the LoRA ceiling (tfidf +0.135 / frozen +0.082 SURVIVE; lora −0.003) ·
  carrier SMALL-THROUGHOUT (G_lora +0.067; residual table wall +0.205; provisional n=3) ·
  cross-family SURVIVES (Gx_lora +0.365, capacity-resistant; direct data does not bridge).
- Audit chain: 5-verifier post-M1 · 5-verifier B4 (ROBUST) · bootstrap reproduction ·
  full re-audit 2026-06-09 (30 verifiers; spine reproduces bit-exact).
- Total compute ≈ $37 of the $250 base budget.

Pre-alpha: chapter prose fills as lanes close.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### Pre-drafted tag message — variant (a) (if tagging `ee397a7` as-is)

```
M0 close (v0.1.0): public pre-alpha portfolio + first finding (M1 attack-type LODO)

Snapshots the M0 framework + M1 + the Round-30 re-ladder (the cross-family arc lives on the
session branch and ships in the next tag):
- Public repo, pre-alpha banner; 13-chapter skeleton; 6-lane framework; 210-entry dossier;
  Docker repro; governance docs; 53 ADRs.
- M1: pre-registered §6.5 OOD-wall prediction FALSIFIED at the LoRA ceiling
  (tfidf +0.135 / frozen +0.082 SURVIVE; lora −0.003) — judged on the pre-locked rule.
- Round-30 re-ladder (ADR-055): multi-axis spine; Lane 2 re-pointed to the carrier axis.

Pre-alpha: experiments in flight; chapter prose fills as lanes close.

Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### Announcement refresh spec (`docs/build-in-public/2026-06-01-v0.1.0-announcement.md`)

Required under every fork: fix line 33's stale "0.98–0.999" range (F4). Under (b): replace the single-result headline with the 3-axis spine (same numbers as the tag text), add one line on the audit chain, keep length/tone. Under (a): add a "what's next: cross-family arc already complete on the session branch" teaser instead.

## 3. Fork B — agent-harness-v0 disposition — **DECIDED: (A) retrospective record trio, own surface**

Audit verdict: deterministic, internally exact, claims contained (consolidated-audit §5). Decision pair:

1. **Record form:** (A) retrospective record trio — explicitly-labeled `criteria.md` scope declaration + fenced FINDINGS + `verdict: EXPLORATORY-VALIDATED` — vs (B) exploratory README banner only, no verdict surface until a pre-registered v1. Both drafted; (A) makes it a citable experiment surface, (B) is the stricter pre-registration reading.
2. **Placement:** new experiment surface alongside the LODO arcs (its own chapter-7-adjacent slot) vs folded under the Lane 3/4 playbooks (it evaluates *defenses* — spotlighting/firewalls — which is Lane 3/4 territory and dossier family `agent_harness_architecture`). *[Decided 2026-06-10 (Round 31): **own surface**, cross-referenced from Lane 3/4; a v1 extends it in place.]*

A v1 with an LLM backend (the only way `spotlight_delimit` and the gates produce *empirical* rather than construction-property results) is a P3 option, only meaningful after adoption.

## 4. Fork C — the next experiment (after P0/P1) — **DECIDED: C1 (2026-06-10)**

| Option | What | Cost/blockers | Case |
|---|---|---|---|
| **C1 (RECOMMENDED): Lane 2 carrier/table training** | Attack the one residual within-BIPIA wall (+0.205 table) with carrier-targeted training data; pre-register first | cheap rungs $0; lora ~$1–5; corpus gen via research_toolkit `/dataset-synthesize` (merged; #22/#23 open but non-blocking) | Direct continuation of ADR-055's re-point; smallest pre-registered step with a falsifiable target |
| C2: Cross-family mechanism test | Pre-register a mechanism probe for WHY cross-family survives (style-vs-content; the Mirror confound W12 makes causal claims otherwise unsupportable) | $0–small; design work dominates | results-analysis "do next"; the audit sharpened it (W1/W2 feed the design) — but P1.5 already buys most of the cheap insight |
| C3: agent-harness-v1 (LLM backend) | Turn the v0 construction-property table into empirical ASR/utility numbers | LLM API spend; needs Fork B = adopt | New axis (agentic defense eval); furthest from the spine |

Recommendation: **C1**, with C2's pre-registration drafted during C1's GPU waits. P1.5 (methods hardening) precedes either — it closes W1/W2 so neither experiment builds on an unhardened record.

## 5. Held items (single human gate) + when-unblocked

- **Accounts** (Twitter/X + Mastodon) remain the only human gate for close+announce (Fork A) and the build-in-public cadence; dossier sprint (Days 6–12 runbook) stays user-led behind it.
- **DF-11 / eval-toolkit#93** — carrier/clustered bootstrap re-lock when `return_samples`/`frac_gt` ships; W4's upstream note can ride the same issue.
- **Carrier n=5 retest** — queued behind its license gate; do not block consolidation (per results-analysis).

## 6. Milestone-rethink fold-in (retiring `milestone-rethink-inputs.md`)

Its four OPEN implications, resolved:

1. **Narrative re-point** → executed beyond its ask: not just "wall is capacity-dependent" but the 3-axis spine (ADR-055 + 2 amendments). Chapter-thesis re-pointing lands with M2+ prose; no further deliberation owed.
2. **Lane reframings** → Lane 2 re-pointed to carrier (ADR-055 Decision); Lane 5 sharpened to intermediate-activation recovery; Lane 1b/4 §16 gates rechecked Round 30 — untripped.
3. **Sequencing** → ladder order unchanged; M2 = Lane 2 carrier arc (Fork C1). This doc is the sequencing record.
4. **"An ADR-055 iff reorganization"** → landed as ADR-055 + amendments.

→ **Action (P0):** add a SUPERSEDED banner to `milestone-rethink-inputs.md` pointing here + ADR-055 (also fixes its stale line 16, F4).

## 7. Cross-walk (coverage proof)

- **git-status rows ↔ disposition table:** 6 rows ↔ consolidated-audit §8 rows 1–6, bijective. (7th related item: the committed DRAFT amendment → W18, P0.)
- **M0_READINESS held steps 2–6** → Fork A (runbook re-validated; step-2 "re-run ratify-milestone on main" stays inside the user-led runbook).
- **SESSION-HANDOFF NEXT items** (held close / DF-11 re-lock / Lane 2) → Fork A / §5 / Fork C1.
- **results-analysis "Paths forward" (5 rows)** → consolidate-first = P0; provenance = disposition 5–6 + W8; mechanism pre-reg = C2; Lane 2 carrier/table = C1; carrier n=5 = §5.
- **milestone-rethink implications (4)** → §6.
- **A1–A8 punch-list:** A3/A4 applied (`f00e035`); A5 applied (criteria citation gloss, verified); A1 applied at source but un-propagated → F4 closes it; remaining framing items are absorbed where the verifiers re-found them (F5/F6/W10/W12/W13); a final A1–A8 line-item check rides the P0 session.
- **Audit FOLLOW-UPs:** W1/W2/W4/W5/W9/W10/W11/W12/W15/W16/W17 → P1.5; W3/W6/W14/W18 + F-batch → P0; W7 → Fork B; W8 → disposition; W13 → F-batch wording.

## 8. What remains open (post-Round-31)

All of this doc's forks are now decided (Round 31, 2026-06-10): Fork A = (b), Fork B = trio + own
surface, Fork C = C1, FIX-NOWs + dispositions applied (`d92426a`). Still open:

- **Accounts timing** (the single human gate) — releases the P1 close + announce and the
  build-in-public cadence; nothing else blocks on it.
- **C1 pre-registration ratification** — the criteria DRAFT is a separate present-first go; no run
  before it.
- **When-unblocked items** (§5): DF-11 / eval-toolkit#93 re-lock · carrier n=5 retest (license gate).
- ~~W18 archive form~~ — *resolved in the P1.5 session (archived with SUPERSEDED header).*

This doc is the standing roadmap surface until the next refresh.
