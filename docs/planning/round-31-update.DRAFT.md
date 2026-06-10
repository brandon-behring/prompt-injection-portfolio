# Round 31 update — DRAFT for user ratification (adr-scribe, 2026-06-10)

> Paste into `docs/planning/PORTFOLIO_PLAN.md` immediately after the Round 30 section (after ~line 706,
> before the `---`), then delete this file. Scribe's open wording questions are listed at the bottom.

### Round 31 update — full re-audit ratified (the spine holds) + consolidation dispositions (2026-06-09/10)

First round after the cross-family arc closed (ADR-055 amendment ratified 2026-06-06, `4881514`). Folds three input streams: `docs/planning/results-analysis-2026-06-08.md` (the post-arc results read), the user-elected **full re-audit** (`docs/planning/consolidated-audit-2026-06-09.md`), and the roadmap refresh (`docs/planning/roadmap-refresh-2026-06-09.md`). This round ratifies the audit and locks five Checkpoint-1 dispositions; it does **not** re-sequence milestones (still M0→M7) and does **not** pick the next experiment (Fork C registered open below).

**Decisions locked** (5):
- **Full re-audit executed + PASSED (full scope user-elected over gap-focused).** 30 adversarial verifiers (5 roles × 6 arcs) + mechanical reproduction — verdict scripts re-run (every point estimate **Δ=0**; CI-low drift ≤9.8e-4, MC noise), **162/162** parquet-level metric recomputes at **Δ=0.0**, **bit-exact** tfidf retrains on all 4 arcs — + codex/gemini external refutation (codex 36 CONFIRMED / 6 WEAKENED / 0 REFUTED; gemini's single refutation failed artifact-grounding). **The spine holds: attack-type FALSIFIED · carrier SMALL-THROUGHOUT · cross-family SURVIVES. Zero BLOCKERs.** Register: **15 FIX-NOW** (all applied 2026-06-10, user-approved) + **18 FOLLOW-UP** + **10 cosmetic**. Two substantive new findings: **W1** MiniLM-256 truncation artifact (66.5% of table / 44.1% of code positives carry zero attack tokens into the EDA embedder — email-only silhouette re-check owed) and **W2** InjecAgent materialization bug (`<Attacker Instruction>` placeholder concatenated, not substituted; conservative for verdicts — the slice was already ruled uninformative). Canonical record: `consolidated-audit-2026-06-09.md`.
- **agent-harness-v0 → adopted as a retrospective record trio (Fork B = variant A):** `experiments/agent-harness-v0/` enters the record with a `criteria.md` opening RETROSPECTIVE SCOPE DECLARATION (explicitly not a pre-registration), a fenced `FINDINGS.md`, and `verdict.json` = **EXPLORATORY-VALIDATED**. Claim fence: **construction properties of the scripted backend only** — no empirical claims about LLM-agent defense effectiveness (those require a pre-registered v1 with an LLM backend; a P3 option, now unblocked by adoption).
- **RunPod provenance → disposition (b):** the 28 `metrics.json` (16 all-27 H100 + 12 B+ cheap-4090) + the mechanical sha256 manifest (`experiments/cross-family-transfer/B3_PROVENANCE_MANIFEST.md`) enter git; the 745MB of parquets stay gitignored-local, inventoried in the manifest. Audit basis: all 28 byte-identical to their canonical counterparts; the single expected cross-arch pair (H100 0.5928 vs 4090 0.5999, Δroc 0.0072 ≪ 0.05 SESOI) confirmed; zero orphans either direction.
- **v0.1.0 close → re-scoped to Fork A(b):** fast-forward the 38-commit cross-family arc into `main` (`git merge --ff-only`; commits already public on the session branch), then tag with the corrected full-spine text (now in `M0_READINESS.md`, replacing the stale "55 ADRs / capacity-dependent" draft — F3). The release then matches the ratified record and the announcement tells the 3-axis story. Close + announce remain **accounts-gated** (unchanged human gate).
- **Milestone-rethink deliberation → folded + retired:** `milestone-rethink-inputs.md` carries a SUPERSEDED banner; all four of its OPEN implications are resolved by the ADR-055 arc (`roadmap-refresh-2026-06-09.md` §6). The standing roadmap surface is now **`docs/planning/roadmap-refresh-2026-06-09.md`** (P0 consolidation → P1 close → P1.5 methods-hardening → P2 Lane-2 carrier arc), until the next refresh.

**Open forks** (registered, not decided — each a separate present-first go):
- **Fork C — next experiment:** **C1** Lane-2 carrier/table training (RECOMMENDED — direct continuation of ADR-055's Lane-2 re-point; attacks the residual +0.205 table wall; pre-registration first) vs **C2** cross-family mechanism pre-registration (style-vs-content; W1/W2 feed the design) vs **C3** agent-harness-v1 with an LLM backend.
- **W18** — archival of the superseded DRAFT-amendment copy in the experiment dir (archive vs delete; user-led).
- **P1.5 timing** — when the methods-hardening FOLLOW-UP package (W1 email-only check, W2 fix/re-derive, disclosure notes) runs relative to the P1 close; the roadmap recommends P1.5 before any Fork-C run so the next experiment doesn't build on an unhardened record.

**Implications**:
- The audit + roadmap docs are the canonical records — register, don't duplicate: the 43-item findings register lives in `consolidated-audit-2026-06-09.md` §7; sequencing detail and the fork analyses live in `roadmap-refresh-2026-06-09.md`.
- **W1 caveats the EDA geometry headline**: "the carrier dominates the MiniLM embedding" (Rounds 24–27 above) is partly a 256-token truncation artifact until the email-only silhouette re-check (P1.5) lands; prose citing the silhouette/ARI numbers must carry the frozen-MiniLM + truncation qualifier (the conclusion plausibly survives — email untruncated, 2-class control, cheap-rung corroboration).
- The 15 FIX-NOWs landed across README / NEXT_SESSION / M0_READINESS / ADR-054 / SESSION-HANDOFF / glossary / this file (the Round-30 resolution annotation above = F10); the stale "0.98–0.999" range (F4) is propagated out everywhere.
- **No new ADR filed** — ADR-055 + its amendments already govern the spine; this round records audit ratification + dispositions only (mirrors Round 27's no-ADR pattern).
- No milestone re-sequencing and no §16 gate changes; M2 = the Lane-2 carrier arc per Round 30, pending the Fork-C decision.

---

**Scribe's open questions for the user (answer or ignore at ratification):**
1. Fork-B *placement* (own experiment surface vs folded under Lane 3/4 playbooks) — record-form is decided; placement either rides this round as a 4th open fork or is settled by adoption-as-own-surface.
2. "Open forks" as a named block is a format extension over Rounds 27/30 — keep or inline.
3. Confirm no ADR-056 intended for this round.
4. Title wording is adjustable.
