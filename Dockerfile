# Portfolio T2 reproducibility tier — per plan §7 (mandatory at M5; M0 Day 16
# initial setup per plan §21).
#
# Pins Python 3.13 (matches pyproject `requires-python = ">=3.13"`) + uv as
# the package manager. Builds with the portfolio repo + the sibling submission
# (per Round 14 Q1 v1.3.0 pin + Round 6 editable-dep layout per [tool.uv.sources]).
#
# Image purpose: reproducibility-tier T2 entry point. Reader can:
#   docker compose up --build
#   docker compose run portfolio uv run pytest -m contract
#   docker compose run portfolio bash
#
# This is NOT a GPU-equipped image (Lane work requiring CUDA runs via
# runpod-deploy from the operator's machine per plan §3 dev-only pin). For
# inference-only CPU smoke-tests + the 13 test-contracts + ruff + mypy
# --strict + the v0.47 import smoke-tests from Day 3a, CPU is sufficient.

FROM python:3.13-slim

# Install uv (Astral) + minimal system deps (curl for HEAD-check, git for
# editable-dep resolution against the submission sibling repo).
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        git \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir uv

# Working directory layout matches the Round 6 sibling-repo design:
#   /workspace/prompt-injection-portfolio/
#   /workspace/prompt-injection-detection-prototype/
# `compose.yaml` mounts the host's sibling prototype read-only.
WORKDIR /workspace/prompt-injection-portfolio

# Copy portfolio + sync dependencies. uv resolves the editable-dep against
# the sibling path at sync time; `compose.yaml` mounts the prototype.
COPY pyproject.toml uv.lock ./
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY tests/ ./tests/
COPY decisions/ ./decisions/
COPY docs/ ./docs/
COPY experiments/ ./experiments/
COPY Makefile README.md LICENSE ETHICS.md SECURITY.md ./

# Default behaviour: drop into bash so the reader can explore. Tests + smoke
# checks run via `docker compose run portfolio uv run pytest -m contract`.
ENV PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy
CMD ["bash"]
