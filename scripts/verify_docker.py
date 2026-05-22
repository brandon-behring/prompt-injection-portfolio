"""Pre-flight: verify Docker daemon + base image pullable + portfolio compose config.

Per plan §21 M0 Day 1 (Steps 1-4) + Day 16 extension (Step 5 added Round 22):
verifies Docker is operational + the portfolio's Dockerfile + compose.yaml
parse via `docker compose config`. Does NOT build the portfolio image (that
is opt-in via `docker compose build`; ~4GB image with torch/transformers).

Run via: `make verify-docker` or `python scripts/verify_docker.py`.
Exits 0 on green; non-zero on Docker unreachable or compose config invalid.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], timeout: int = 60) -> tuple[int, str]:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        return result.returncode, (result.stdout + result.stderr).strip()
    except subprocess.TimeoutExpired:
        return -1, f"timeout after {timeout}s"
    except FileNotFoundError:
        return -1, "command not found"


def main() -> int:
    # Step 1: docker CLI present
    if not shutil.which("docker"):
        print("✗ docker CLI not found on PATH")
        print("  Install Docker Engine or Docker Desktop: https://docs.docker.com/engine/install/")
        return 1
    print("✓ docker CLI found")

    # Step 2: docker daemon reachable
    code, out = run(["docker", "info", "--format", "{{.ServerVersion}}"], timeout=10)
    if code != 0:
        print(f"✗ docker daemon not reachable: {out[:200]}")
        print("  Start Docker daemon: `sudo systemctl start docker` or Docker Desktop")
        return 1
    print(f"✓ docker daemon reachable; server version: {out}")

    # Step 3: pull a tiny test image
    print("⋯ pulling alpine:3.20 (small smoke test; ~3MB) ...")
    code, out = run(["docker", "pull", "alpine:3.20"], timeout=60)
    if code != 0:
        print(f"✗ docker pull failed: {out[:200]}")
        return 1
    print("✓ docker pull succeeded")

    # Step 4: run a one-shot container
    code, out = run(["docker", "run", "--rm", "alpine:3.20", "echo", "ok"], timeout=10)
    if code != 0 or out.strip() != "ok":
        print(f"✗ docker run failed: {out[:200]}")
        return 1
    print("✓ docker run succeeded (alpine:3.20 echoed 'ok')")

    # Step 5 (Day 16 extension): portfolio Dockerfile + compose.yaml present + parse
    repo_root = Path(__file__).resolve().parent.parent
    dockerfile = repo_root / "Dockerfile"
    compose_yaml = repo_root / "compose.yaml"
    if not dockerfile.exists():
        print(f"⚠ Dockerfile not yet present at {dockerfile} — Day 16 deliverable")
    else:
        print("✓ Dockerfile present (T2 reproducibility tier)")
    if not compose_yaml.exists():
        print(f"⚠ compose.yaml not yet present at {compose_yaml} — Day 16 deliverable")
    else:
        print("✓ compose.yaml present")
        code, out = run(
            ["docker", "compose", "-f", str(compose_yaml), "config", "--quiet"],
            timeout=10,
        )
        if code != 0:
            print(f"✗ docker compose config failed: {out[:200]}")
            return 1
        print("✓ docker compose config parses cleanly")

    print()
    print("OK: Docker pre-flight green. T2 reproducibility tier feasible.")
    print("Next: `docker compose build` (opt-in; ~4GB image with torch).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
