# Agent Harness V0

Research-only email-RAG prompt-injection benchmark. The unit of evaluation is an
agent trace with simulated tools, not a prompt-injection detector score.

> **Claim fence (see `criteria.md` — RETROSPECTIVE scope declaration, not a pre-registration):**
> under the scripted backend, the defense rows are **construction properties** — `spotlight_delimit`
> cannot act (the policy ignores delimiters) and `provenance_gate`/`tool_firewall` cannot fail (the
> side-effect channel is structurally removed). No empirical claims about LLM-agent defense
> effectiveness; those require a pre-registered v1 with an LLM backend. Verdict:
> `verdict.json` → EXPLORATORY-VALIDATED.

The default backend is deterministic:

```bash
uv run python experiments/agent-harness-v0/run.py \
  --cases experiments/agent-harness-v0/cases.jsonl \
  --backend scripted \
  --defenses none spotlight_delimit static_detector_gate tool_firewall provenance_gate \
  --out experiments/agent-harness-v0/results/scripted.jsonl

uv run python experiments/agent-harness-v0/report.py \
  --results experiments/agent-harness-v0/results/scripted.jsonl \
  --out experiments/agent-harness-v0/reports/summary.md
```

Optional LLM runs are exploratory:

```bash
uv run python experiments/agent-harness-v0/run.py \
  --cases experiments/agent-harness-v0/cases.jsonl \
  --backend llm \
  --model MODEL_NAME \
  --max-cases 25
```

## Defenses

- `none`: naive access to retrieved untrusted documents.
- `spotlight_delimit`: wraps retrieved documents in explicit untrusted markers.
- `static_detector_gate`: quarantines documents with obvious injection markers.
- `tool_firewall`: blocks side-effect calls not entailed by the trusted user task.
- `provenance_gate`: blocks side-effect calls controlled by untrusted content.

## Metrics

- ASR: attack success rate from executed forbidden tool calls.
- Utility: expected answer or allowed tool completion.
- Over-defense: benign case degraded or blocked.
- Parse fail: invalid backend output.

The report computes these metrics from saved JSONL traces only.
