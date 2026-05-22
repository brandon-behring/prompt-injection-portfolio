<!--
Portfolio PR template per plan §21 Day 15 + plan §2 Tier-4 anti-pattern firewall.
Required checks below must be green before merge.
-->

## Summary

<!-- 1-2 sentences: what changes + why -->

## Quality gates

- [ ] `uv run pytest -m contract` green (all 13 test-contracts pass per Day 3b baseline)
- [ ] `uv run ruff check .` clean
- [ ] `uv run ruff format --check .` clean
- [ ] `uv run mypy --strict src/ scripts/ tests/` clean
- [ ] CI workflow green at the commit being merged

## SDD discipline (per plan §2 Tier-1)

- [ ] No hand-rolled metrics — uses `eval-toolkit` primitives via `scorecard()` + `metric_specs.*`
- [ ] Any new upstream-library import registered in `decisions/library_imports.md`
- [ ] Any new project-specific term landed in `docs/glossary.md`
- [ ] If a Lane closes: 4 experiment-record files + 3 book fragments populated (per Round 17 follow-up Q2)
- [ ] Per-row predictions persisted (parquet) for any new eval result

## Reproducibility (per plan §7)

- [ ] T0/T1/T2/T3 tier impact documented if reproducibility surface changes
- [ ] HF Hub artifacts (model cards / datasets) updated if applicable

## Documentation

- [ ] CHANGELOG entry added under `[unreleased]`
- [ ] Freshness-badge state updated on affected chapter / notebook (per scaffold v3.5 7-state system)
- [ ] Cross-references between ADR + chapter + experiment record kept consistent

## ADR delta (if applicable)

<!-- Reference any ADR being added or superseded; per plan §1 +
plan §9 anticipated ADR set. Light Michael-Nygard format <400 words. -->

## Reviewer checklist

- [ ] Reviewed for hidden methodology decisions that should be ADR'd
- [ ] Confirmed no introduction of `# TODO(upstream #N)` markers (per Round 10
      library-first invariant — no local workarounds)
- [ ] Confirmed no SimpleNamespace patterns or v0.47-removed eval-toolkit APIs
      (per Round 20 canonical surfaces)
