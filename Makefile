# Portfolio Makefile — M0 minimal scaffold (pre-flight gates only).
# Full Makefile per plan §21 expands across M0 Day 2-19 (lane targets, book-dev,
# book-pdf, cost-report, ratify-milestone, dossier-audit, etc.).
#
# Current targets are M0 Day 1 pre-flight only (read-only verification).

.PHONY: verify-data-sources verify-docker verify-deps

verify-data-sources:
	@python3 scripts/verify_data_sources.py

verify-docker:
	@python3 scripts/verify_docker.py

verify-deps:
	@python3 scripts/verify_editable_dep.py
