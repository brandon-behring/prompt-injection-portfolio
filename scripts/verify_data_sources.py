"""Pre-flight: verify the 6 OOD eval data sources are reachable.

Per plan §21 M0 Day 1. Read-only HTTP HEAD checks against HF Hub + GitHub.
Does NOT download datasets; just confirms they exist publicly.

Run via: `make verify-data-sources` or `uv run python scripts/verify_data_sources.py`.
Exits 0 on all-reachable; non-zero on any unreachable source.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    name: str
    kind: str  # "hf_dataset" | "github_repo"
    path: str  # "owner/name"
    note: str = ""


SOURCES: tuple[Source, ...] = (
    # 3 carried over from submission's source_manifest.yaml
    Source(
        "bipia",
        "github_repo",
        "microsoft/BIPIA",
        "Yi et al. KDD '25; 5 scenarios; canonical indirect-injection benchmark",
    ),
    Source(
        "injecagent",
        "github_repo",
        "uiuc-kang-lab/InjecAgent",
        "Zhan et al. ACL 2024; 1,054 agentic test cases",
    ),
    Source(
        "notinject",
        "hf_dataset",
        "leolee99/NotInject",
        "Li et al. arXiv 2410.22770; 339 benign over-defense probes",
    ),
    # 3 NEW for portfolio per plan §5
    Source(
        "agentdojo",
        "github_repo",
        "ethz-spylab/agentdojo",
        "Debenedetti et al. NeurIPS '24; 97 user tasks × 629 security cases",
    ),
    Source(
        "llmail_inject",
        "github_repo",
        "microsoft/llmail-inject-challenge",
        "Microsoft SaTML 2025 challenge; 208K attack submissions; 5K stratified",
    ),
    Source(
        "pint",
        "github_repo",
        "lakeraai/pint-benchmark",
        "Lakera multilingual hard-negative benchmark; English-only 3,016 used",
    ),
)


def check_hf_dataset(path: str) -> tuple[bool, str]:
    """Return (reachable, detail) for an HF Hub dataset path 'owner/name'."""
    url = f"https://huggingface.co/api/datasets/{path}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        downloads = data.get("downloads", "?")
        last_modified = data.get("lastModified", "?")
        return True, f"public; downloads={downloads}, last_modified={last_modified}"
    except urllib.error.HTTPError as e:
        if e.code == 401:
            return False, "HTTP 401 (gated; may need HF_TOKEN)"
        if e.code == 404:
            return False, "HTTP 404 (not found)"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"error: {type(e).__name__}: {e}"


def check_github_repo(path: str) -> tuple[bool, str]:
    """Return (reachable, detail) for a GitHub repo path 'owner/name'."""
    url = f"https://api.github.com/repos/{path}"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
        stars = data.get("stargazers_count", "?")
        pushed_at = data.get("pushed_at", "?")
        return True, f"public; stars={stars}, pushed_at={pushed_at}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"error: {type(e).__name__}: {e}"


def main() -> int:
    print(f"Verifying {len(SOURCES)} OOD eval data sources (read-only HEAD checks):\n")
    failures = []
    for src in SOURCES:
        if src.kind == "hf_dataset":
            ok, detail = check_hf_dataset(src.path)
        elif src.kind == "github_repo":
            ok, detail = check_github_repo(src.path)
        else:
            ok, detail = False, f"unknown kind: {src.kind}"
        mark = "✓" if ok else "✗"
        print(f"  {mark} {src.name:20s} ({src.kind:13s}) {src.path:40s} — {detail}")
        if not ok:
            failures.append(src)

    print()
    if failures:
        print(f"FAILED: {len(failures)} source(s) unreachable:")
        for src in failures:
            print(f"  - {src.name} ({src.path}): {src.note}")
        return 1
    print(f"OK: all {len(SOURCES)} sources reachable.")
    print("Next: pin revision SHAs via scripts/pin_indirect_manifest.py")
    print("      (see plan §9 M0 task #2 manifest pinning).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
