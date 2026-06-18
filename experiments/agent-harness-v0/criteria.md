# agent-harness-v0 — RETROSPECTIVE SCOPE DECLARATION (2026-06-10)

> **This is NOT a pre-registration.** It was written 2026-06-10, AFTER the v0 build and scripted run
> (results of 2026-06-08), during the full re-audit (`docs/planning/consolidated-audit-2026-06-09.md`
> §5, W7; record form chosen by the user at Checkpoint 1: retrospective trio). It declares the
> experiment's scope and claim fence so the record is a citable, honestly-labeled surface. A v1 with
> real stakes (LLM backend) requires a true pre-registration BEFORE any run.

## Question

In a simulated email-RAG agent (user task + trusted context + untrusted documents + tools with side
effects), how do five harness-level defenses compare on attack success, utility, over-defense, and
parse failure — **as properties of the harness construction**, exercised end-to-end?

## Design (as built)

- **Unit of evaluation:** the agent *trace* (tool calls + final answer), not a detector score.
- **Cases:** n=6 (`cases.jsonl`) — 4 attack (carriers: email, html, table, tool_output; styles:
  direct, obfuscated, second_order, task_aligned_decoy) + 2 benign (incl. instruction-like benign
  text and an allowed draft).
- **Backend:** `scripted` — deterministic policy (no LLM, no randomness, no timestamps); byte-stable
  reruns by construction.
- **Defenses:** none · spotlight_delimit · static_detector_gate · tool_firewall · provenance_gate.
- **Metrics:** ASR (forbidden side-effect tool call executed), Utility (expected answer produced),
  Over-defense (benign case blocked), Parse fail.

## Claim fence (what the v0 numbers ARE and ARE NOT)

Under the scripted backend, defense outcomes are **construction properties**, not empirical findings
about LLM agents:

- `spotlight_delimit` **cannot** change behavior (the scripted policy ignores the delimiters —
  `run.py:223-224`); its ASR row equals `none` BY CONSTRUCTION.
- `provenance_gate` and `tool_firewall` **cannot fail** (they structurally remove the side-effect
  channel for untrusted-sourced actions); their 0.00 ASR is BY CONSTRUCTION.
- `static_detector_gate` is the only defense whose outcome depends on case *content* (pattern match
  vs obfuscation) — the 0.25 ASR / 0.50 utility row is the one v0 result with empirical texture, at
  n=6.

**Permitted claims:** the harness mechanics work end-to-end; the metric definitions compute what they
say; the defense *taxonomy* and its failure-mode structure are exercised. **Forbidden claims:** any
statement about real-agent or LLM-backed effectiveness of these defenses (esp. "spotlighting is
useless" / "provenance gating is perfect") — those require the v1 LLM backend.

## What a v1 pre-registration must lock BEFORE running

LLM backend + model id; case count ≥30 with held-out carriers; ASR/utility gates with CIs and a
pre-stated decision rule; over-defense corpus; prompt-variation robustness; cost cap.

## Verification (v0)

`tests/experiments/test_agent_harness_v0.py` (6 tests) + audited rerun 2026-06-10: scripted rerun
byte-identical; every `reports/summary.md` cell an exact arithmetic consequence of
`results/scripted.jsonl` (consolidated-audit §5).
