"""Launch the Lane-1 attack-type-LODO headline sweep on RunPod (runpod-deploy).

Session-launch wrapper (ADR-026 library-first): load the strict YAML job spec and hand it
to ``runpod_deploy.run_job`` — provision a 24 GB+ GPU pod, stage the repo, train the ``lora`` rung
only (``--rungs lora``, 3 folds × 3 seeds; ADR-054 hybrid), pull → ``results_runpod_lora/``, then
apply the lifecycle (delete on success). The cheap rungs, the §6.5 falsification, and the
off-the-shelf baselines all run locally; merge + ``--finalize-manifest`` + falsify run locally
afterward. The job spec lives in ``experiments/attack-type-lodo/runpod_lane1_sweep.yaml``.

The paid launch is **user-led**. ``--offline-dry-run`` validates the spec + local paths with
**zero provider calls and zero spend**; ``--dry-run`` adds price/inventory checks but does
not provision. ``contingency_unlock_1.md`` classifies this as a **base-budget** spend.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import runpod_deploy as rd

_REPO = Path(__file__).resolve().parent.parent
_DEFAULT_SPEC = _REPO / "experiments" / "attack-type-lodo" / "runpod_lane1_sweep.yaml"


def main(argv: list[str] | None = None) -> int:
    """Parse args, load the job spec, and hand it to ``run_job``."""
    ap = argparse.ArgumentParser(description="Launch the Lane-1 LODO headline sweep on RunPod.")
    ap.add_argument("--config", type=Path, default=_DEFAULT_SPEC, help="job-spec YAML path")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument(
        "--offline-dry-run",
        action="store_true",
        help="validate spec + local paths only (no provider calls, no spend)",
    )
    mode.add_argument(
        "--dry-run",
        action="store_true",
        help="provider price/inventory checks but do NOT provision a pod",
    )
    ap.add_argument(
        "--max-gpu-price-usd",
        type=float,
        default=None,
        help="hard cap on the GPU $/h price the orchestrator will accept",
    )
    args = ap.parse_args(argv)

    spec = rd.load_job_spec(args.config)
    rd.run_job(
        spec,
        config_path=args.config,
        offline_dry_run=bool(args.offline_dry_run),
        dry_run=bool(args.dry_run),
        max_gpu_price_usd=args.max_gpu_price_usd,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
