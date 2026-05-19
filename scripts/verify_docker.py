"""Pre-flight: verify Docker daemon is available + base image pullable.

Per plan §21 M0 Day 1. Doesn't build the portfolio Dockerfile (that's M0 Day 16);
just confirms `docker` CLI works and a small base image can be pulled.

Run via: `make verify-docker` or `python scripts/verify_docker.py`.
Exits 0 on green; non-zero on Docker unreachable or base image pull failure.
"""
from __future__ import annotations

import shutil
import subprocess
import sys


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

    print()
    print("OK: Docker pre-flight green. T2 reproducibility tier feasible.")
    print("Next M0 Day 16: portfolio Dockerfile + compose.yaml (per plan §21).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
