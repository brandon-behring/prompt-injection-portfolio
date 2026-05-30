# Delegation playbook

Subagents run in their own context window and return only their final message. Delegate work that
(1) emits many tokens, (2) distills to a small conclusion, (3) needs no mid-task back-and-forth — so
this main context stays on decisions, synthesis, and presenting forks to the user.

## When → Delegate → Invocation

| When you need to… | Delegate to | Invocation |
|---|---|---|
| Run a LOCAL harness smoke/minimal sweep, §6.5 falsification, or OOD-wall parse | `experiment-runner` | foreground; or Bash `run_in_background` for a long local run |
| Launch + watch the multi-hour RunPod headline sweep | `gpu-run-watcher` | **`run_in_background: true`** (don't block the main loop for hours) |
| Audit the dataset survey | `dataset-auditor` | **fan out one call per dataset in a single message** (one bibkey + a unique `--out` each) |
| Run lint / type / tests / contracts, or ratify a milestone | `gate-runner` | foreground |
| Orient at session start | `session-orienter` | foreground (briefs only — never picks the fork) |
| Draft an ADR or a Round-update | `adr-scribe` | foreground (drafts only — never ratifies/writes/commits) |

## Rules
- **Present-first boundary.** No agent decides a fork, ratifies a milestone, commits, pushes, or files
  a public issue. They run, parse, brief, or draft — the user owns every irreversible/outward step.
- **Parallel > sequential** for independent work: issue the N `dataset-auditor` calls (or independent
  gates) in ONE message so they run concurrently.
- **Background the long cloud sweep.** `gpu-run-watcher` is the only multi-hour agent; always background it.
- **Paid launches always prompt.** The RunPod launch (spends money) is deliberately NOT in the
  permission allowlist; you'll be asked each time. Commits/pushes also stay manual.
- **Each agent has a tight OUTPUT CONTRACT** — that contract is all you should expect back; if an agent
  returns raw logs/dumps, that's a bug in its prompt, not a signal to widen the contract.

## Cost / cloud notes
- Local RTX 2070 (8 GB) OOMs at spec config (`decisions/contingency_unlock_1.md`) → only smoke/minimal
  runs locally; the real sweep is RunPod (24 GB+) via `scripts/runpod_sweep.py` (`load_job_spec→run_job`; wired per ADR-053, paid launch user-gated).
- `gpu-run-watcher` auto-kills only on hard guards (cost ≥ ceiling, default $15; or no progress for N
  min, default 20) and records any `runpod-deploy` friction into `decisions/upstream_issues.md`
  (drafts the upstream issue; you file it).

## Future composition (opt-in, not built)
The 14-dataset survey fan-out and the full seed×fold×rung sweep are natural `Workflow` candidates
(deterministic `parallel()`/`pipeline()` + adversarial verification of the write-gate verdict). Build
that only when explicitly requested.
