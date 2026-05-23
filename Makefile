# Portfolio Makefile — M0 minimal scaffold + ratify-milestone target.
# Full Makefile per plan §21 expands across M0+ (lane targets, book-dev,
# book-pdf, cost-report, dossier-audit, etc.) as lane work begins at M1.

.PHONY: verify-data-sources verify-docker verify-deps ratify-milestone lint test contracts dossier-audit

verify-data-sources:
	@python3 scripts/verify_data_sources.py

verify-docker:
	@python3 scripts/verify_docker.py

verify-deps:
	@python3 scripts/verify_editable_dep.py

# Dossier-audit close-gate (per ADR-007 M7-ratify gate).
# Validates v2.2+ strict-live artifacts across all 5 topic dossiers.
# Iterates: bib_ledger + evidence_ledger + cache_manifest + claim_graph +
# gather_trace + agent_index + pre_selection_manifest + cross_stage --strict.
dossier-audit:
	@echo "=== M7 dossier-audit close-gate (5 topics) ==="
	@for topic in detector-landscape direct-vs-indirect training-and-evaluation agentic-security-architecture rag-injection-defenses; do \
		echo ""; \
		echo "--- $$topic ---"; \
		python3 ~/Claude/research_toolkit/validators/bib_ledger.py docs/research/$$topic/bib_ledger.yml || exit 1; \
		python3 ~/Claude/research_toolkit/validators/evidence_ledger.py docs/research/$$topic/evidence_ledger.yml || exit 1; \
		python3 ~/Claude/research_toolkit/validators/cache_manifest.py docs/research/$$topic/cache_manifest.yml || exit 1; \
		python3 ~/Claude/research_toolkit/validators/claim_graph.py docs/research/$$topic/claim_graph.jsonl || exit 1; \
		python3 ~/Claude/research_toolkit/validators/gather_trace.py docs/research/$$topic/gather_trace.yml || exit 1; \
		python3 ~/Claude/research_toolkit/validators/agent_index.py docs/research/$$topic/agent_index/ || exit 1; \
		python3 ~/Claude/research_toolkit/validators/pre_selection_manifest.py docs/research/$$topic/agent_index/pre_selection_manifest.yml || exit 1; \
		python3 ~/Claude/research_toolkit/validators/audit_trail.py docs/research/$$topic/agent_index/README.md || exit 1; \
		python3 ~/Claude/research_toolkit/validators/cross_stage.py docs/research/$$topic/ || exit 1; \
	done
	@echo ""
	@echo "✓ M7 dossier-audit PASS (5 topics validated)"

# Aggregated quality gates (mirrors CI workflow).
lint:
	@uv run ruff check .
	@uv run ruff format --check .
	@uv run mypy --strict src/ scripts/ tests/

test:
	@uv run pytest -m "not integration"

contracts:
	@uv run pytest -m contract

# Day 19 M0 ratify-milestone: aggregates the close-gate checks.
# Exit non-zero on any failure. Composable: `make ratify-milestone M=M0`.
# Does NOT tag or push — that stays user-led per Round 22 Q4.
ratify-milestone:
	@echo "=== M0 ratify-milestone close-gate ==="
	@echo ""
	@echo "--- 1. Verify pre-flight gates (data + Docker + sibling) ---"
	@$(MAKE) verify-data-sources
	@$(MAKE) verify-docker
	@$(MAKE) verify-deps
	@echo ""
	@echo "--- 2. Quality gates (ruff + mypy + pytest) ---"
	@$(MAKE) lint
	@$(MAKE) test
	@$(MAKE) contracts
	@echo ""
	@echo "--- 3. Files-present check ---"
	@test -f README.md && echo "  ✓ README.md" || (echo "  ✗ README.md missing" && exit 1)
	@test -f LICENSE && echo "  ✓ LICENSE" || (echo "  ✗ LICENSE missing" && exit 1)
	@test -f ETHICS.md && echo "  ✓ ETHICS.md" || (echo "  ✗ ETHICS.md missing" && exit 1)
	@test -f SECURITY.md && echo "  ✓ SECURITY.md" || (echo "  ✗ SECURITY.md missing" && exit 1)
	@test -f CODE_OF_CONDUCT.md && echo "  ✓ CODE_OF_CONDUCT.md" || (echo "  ✗ CODE_OF_CONDUCT.md missing" && exit 1)
	@test -f Dockerfile && echo "  ✓ Dockerfile" || (echo "  ✗ Dockerfile missing" && exit 1)
	@test -f compose.yaml && echo "  ✓ compose.yaml" || (echo "  ✗ compose.yaml missing" && exit 1)
	@test -f experiments/MANIFEST.json && echo "  ✓ experiments/MANIFEST.json" || (exit 1)
	@test -d book/src/content/textbook && echo "  ✓ book/src/content/textbook/" || (exit 1)
	@test -d book/src/content/fragments && echo "  ✓ book/src/content/fragments/" || (exit 1)
	@test -d decisions && echo "  ✓ decisions/" || (exit 1)
	@test -d docs/build-in-public && echo "  ✓ docs/build-in-public/" || (exit 1)
	@echo ""
	@echo "✓ M0 ratify-milestone PASS"
	@echo ""
	@echo "Next (user-led): \`git tag v0.1.0\` + \`gh release create v0.1.0\` + announcement thread"
	@echo "Outstanding (deferred to user session per Round 22 Q2 + Round 24 Sprint 2):"
	@echo "  - Twitter/X + Mastodon account creation + M0 announcement post"
	@echo "  - Open MRs to monitor: MR-3 (research_toolkit#1) + MR-12 (eval-toolkit#69)"
	@echo "  Dossier sprint COMPLETE per Sprint 1 + Sprint 2 (210 entries / 5 topics):"
	@echo "    Use 'make dossier-audit' to validate v2.2+ strict-live artifacts."
