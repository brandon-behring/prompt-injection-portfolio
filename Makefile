# Portfolio Makefile — M0 minimal scaffold + ratify-milestone target.
# Full Makefile per plan §21 expands across M0+ (lane targets, book-dev,
# book-pdf, cost-report, dossier-audit, etc.) as lane work begins at M1.

.PHONY: verify-data-sources verify-docker verify-deps ratify-milestone lint test contracts

verify-data-sources:
	@python3 scripts/verify_data_sources.py

verify-docker:
	@python3 scripts/verify_docker.py

verify-deps:
	@python3 scripts/verify_editable_dep.py

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
	@echo "Outstanding (deferred to user session per Round 22 Q2):"
	@echo "  - Dossier sprint (~60-80 files via research_toolkit; compass artifacts at ~/Downloads/)"
	@echo "  - Twitter/X + Mastodon account creation + M0 announcement post"
	@echo "  - Open MRs to monitor: MR-3 (research_toolkit#1) + MR-12 (eval-toolkit#69)"
