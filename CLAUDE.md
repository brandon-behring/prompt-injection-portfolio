# prompt-injection-portfolio

**Delegation (context engineering).** Push context-heavy, independent work into a subagent and
read only its distilled result: sweeps → `experiment-runner`; cloud/RunPod sweeps → `gpu-run-watcher`;
dataset survey → `dataset-auditor` (fan out one per dataset, in one message); quality/milestone gates
→ `gate-runner`; session start → `session-orienter`; ADR/Round drafts → `adr-scribe`. These agents
never decide forks, ratify milestones, commit, push, or file public issues — that stays user-led
(present-first). Full When→Delegate→Invocation table: `.claude/delegation.md`.

**Conventions.** Hard coding rules + commit format → `.tooling/research_toolkit/.claude/CLAUDE.md`.
Commit trailer: `Co-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>`.
Library-first (ADR-026): use upstream `eval-toolkit` / `research_toolkit` / `runpod-deploy` — no local
reimplementation; if a library is missing something, file it upstream (`decisions/upstream_issues.md`).
