# agent-harness-v0 — FINDINGS (scripted backend; retrospective record)

> Scope + claim fence: `criteria.md` (RETROSPECTIVE — not a pre-registration). All rows below are
> **construction properties** of the scripted backend except where marked, per the fence.

## Results (n=6 cases: 4 attack / 2 benign; scripted backend)

| Defense | ASR | Utility | Over-defense | Parse fail | Nature of the row |
|---|---|---|---|---|---|
| none | 1.000 | 1.000 | 0.000 | 0.000 | baseline by construction |
| spotlight_delimit | 1.000 | 1.000 | 0.000 | 0.000 | **by construction** — scripted policy ignores delimiters (`run.py:223-224`) |
| static_detector_gate | 0.250 | 0.500 | 0.000 | 0.000 | content-dependent (the one empirical-textured row, n=6) |
| tool_firewall | 0.000 | 1.000 | 0.000 | 0.000 | **by construction** — side-effect channel removed |
| provenance_gate | 0.000 | 1.000 | 0.000 | 0.000 | **by construction** — untrusted-sourced actions gated |

Static-detector texture: 1 of 4 attacks passes (the table-carrier payload matches none of the 6
`SUSPICIOUS_PATTERNS`); the blocked document degrades the benign-side answer for 3 of 6 rows →
utility 0.500. The detector blocks obvious (direct) but not obfuscated payloads — the expected
shape of a static pattern gate.

## What v0 establishes

1. The trace-level harness (cases → agent loop → defense hooks → metrics → report) works end-to-end
   and is deterministic (byte-stable reruns).
2. The defense taxonomy separates *channel-removal* defenses (firewall/provenance — fail-closed by
   design) from *content* defenses (static detector — bypassable) from *representation-only*
   defenses (spotlighting — inert without a policy that reads it). This structure, not the numbers,
   is the v0 takeaway.
3. Benign instruction-like text and allowed drafts are not blocked by any defense (over-defense 0.000
   at n=2 benign — floor, not evidence).

## Audit stamp (2026-06-10)

Full re-audit (`docs/planning/consolidated-audit-2026-06-09.md` §5): scripted rerun **byte-identical**
to `results/scripted.jsonl`; `reports/summary.md` arithmetic **EXACT**; results cited nowhere outside
this directory (claim containment verified); 6/6 unit tests green.

## Verdict

See `verdict.json`: **EXPLORATORY-VALIDATED** — mechanics validated, no empirical defense claims.
Next step (optional, roadmap Fork C3): pre-registered v1 with an LLM backend.
