"""Poll RunPod inventory for a sub-L40S GPU and alert when one is gettable.

Zero-spend monitor (it NEVER provisions, deletes, or launches a pod) for the
cross-family B+ relaunch (criteria Rev 8). The committed cheap sweep
(``runpod_crossfamily_bplus_cheap_sweep.yaml``) grabs whatever the launcher
resolves *first*, and -- because ``select_gpu_across_datacenters`` walks the
datacenters in YAML order and returns the first stocked card -- that is usually
the L40S in ``US-TX-3``, even when cheaper cards sit stocked in later
datacenters. This poller asks the faithful question the user actually cares
about: "if I launched a *cheap-only* spec right now, which sub-L40S card would I
get, and is it in stock?"

It reuses ``runpod_deploy``'s own selection logic against live
``runpodctl datacenter list`` data, so its answer matches what a real launch
would do. The RunPod API key is read from ``~/.runpod/config.toml`` in-process
for best-effort pricing labels only; it is never printed.

Each tick reports two picks:
  * ``full_pick``  -- what the committed ``gpu_order`` resolves to (~ the L40S).
  * ``cheap_pick`` -- what a launch with the ``--exclude`` cards (default L40S +
    A100 80GB PCIe) removed from ``gpu_order`` would grab: the actual sub-L40S
    card. ``cheap_pick`` resolving (at an accepted stock tier) is the trigger.

Exit codes: 0 = a cheap card is gettable (ALERT printed, loop stops); 2 = max
wait elapsed with no cheap card; 1 = unexpected fatal error.

Usage::

    uv run python scripts/cheap_gpu_monitor.py --once     # single check, no loop
    uv run python scripts/cheap_gpu_monitor.py            # loop: 10 min ticks, 24 h cap
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import runpod_deploy as rd
from runpod_deploy import pricing
from runpod_deploy.provider import select_gpu_across_datacenters

_REPO = Path(__file__).resolve().parent.parent
_DEFAULT_CFG = (
    _REPO
    / "experiments"
    / "cross-family-transfer"
    / "runpod_crossfamily_bplus_cheap_sweep.yaml"
)
_DEFAULT_EXCLUDE = ("NVIDIA L40S", "NVIDIA A100 80GB PCIe")
_RUNPODCTL_TIMEOUT_SEC = 60


def _now() -> str:
    """UTC timestamp, ``HH:MM:SS`` (matches the prior monitors' log style)."""
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def _load_api_key_into_env() -> bool:
    """Read ``apikey`` from ``~/.runpod/config.toml`` into ``RUNPOD_API_KEY``.

    Best-effort, for pricing labels only. The key value is never printed.
    Returns True if a key was found and set.
    """
    cfg_path = Path.home() / ".runpod" / "config.toml"
    if not cfg_path.exists():
        return False

    def _find(node: object) -> str | None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "apikey" and isinstance(value, str):
                    return value
                found = _find(value)
                if found:
                    return found
        return None

    try:
        key = _find(tomllib.loads(cfg_path.read_text()))
    except (OSError, tomllib.TOMLDecodeError):
        return False
    if key:
        os.environ.setdefault("RUNPOD_API_KEY", key)
        return True
    return False


def _fetch_datacenters_payload() -> list[dict[str, object]]:
    """Return live ``runpodctl datacenter list -o json`` (the selection source).

    Raises RuntimeError on a non-zero exit or unparseable output so the caller
    can log-and-continue rather than silently treat a CLI hiccup as a stock-out.
    """
    proc = subprocess.run(
        ["runpodctl", "datacenter", "list", "-o", "json"],
        capture_output=True,
        text=True,
        timeout=_RUNPODCTL_TIMEOUT_SEC,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"runpodctl exit={proc.returncode}: {proc.stderr.strip()[:200]}")
    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"runpodctl output not JSON: {exc}") from exc
    if not isinstance(payload, list):
        raise RuntimeError(f"runpodctl payload is {type(payload).__name__}, expected list")
    return payload


def _tier_index(payload: list[dict[str, object]]) -> dict[str, dict[str, str]]:
    """Build ``{datacenter_id: {gpuId: stockStatus.lower()}}`` for tier lookups."""
    index: dict[str, dict[str, str]] = {}
    for dc in payload:
        if not isinstance(dc, dict):
            continue
        dc_id = str(dc.get("id") or "")
        availability = dc.get("gpuAvailability") or []
        by_id: dict[str, str] = {}
        if isinstance(availability, list):
            for item in availability:
                if isinstance(item, dict):
                    by_id[str(item.get("gpuId") or "")] = str(item.get("stockStatus") or "").lower()
        index[dc_id] = by_id
    return index


def _select(payload: list[dict[str, object]], *, datacenters, gpu_order) -> tuple[str, str] | None:
    """Run the launcher's own selection; return ``(gpu, dc)`` or None if nothing matches."""
    try:
        return select_gpu_across_datacenters(
            payload, datacenters=tuple(datacenters), gpu_order=tuple(gpu_order)
        )
    except RuntimeError:
        return None


def _price_label(prices: dict, gpu_id: str, *, cloud_type: str, spot: bool) -> str:
    """Best-effort ``$X.XX/hr`` label; ``n/a`` when GraphQL pricing is unavailable."""
    if not prices:
        return "n/a"
    value = pricing.select_price_for_pod(prices, gpu_id=gpu_id, cloud_type=cloud_type, spot=spot)
    return f"${value:.2f}/hr" if value is not None else "n/a"


def _tick(spec, cheap_order, accept_tiers, prices) -> tuple[bool, str]:
    """One inventory check. Returns ``(triggered, message)``; never raises on CLI hiccups."""
    try:
        payload = _fetch_datacenters_payload()
    except (RuntimeError, subprocess.TimeoutExpired, OSError) as exc:
        return False, f"[{_now()}] runpodctl error (will retry): {exc}"

    tiers = _tier_index(payload)
    full = _select(payload, datacenters=spec.pod.datacenters, gpu_order=spec.pod.gpu_order)
    cheap = _select(payload, datacenters=spec.pod.datacenters, gpu_order=cheap_order)

    def _fmt(pick: tuple[str, str] | None) -> str:
        if pick is None:
            return "none"
        gpu, dc = pick
        tier = tiers.get(dc, {}).get(gpu, "?")
        price = _price_label(prices, gpu, cloud_type=spec.pod.cloud_type, spot=spec.pod.spot)
        return f"{gpu}@{dc}({tier}, {price})"

    full_str, cheap_str = _fmt(full), _fmt(cheap)
    if cheap is not None:
        gpu, dc = cheap
        tier = tiers.get(dc, {}).get(gpu, "?")
        if tier in accept_tiers:
            price = _price_label(prices, gpu, cloud_type=spec.pod.cloud_type, spot=spec.pod.spot)
            if full is not None and full[0] in cheap_order:
                detail = "  committed gpu_order resolves it directly -- LAUNCH-READY (no edit needed)."
            else:
                detail = (
                    f"  but the committed gpu_order would pick {full_str} (datacenter-order\n"
                    f"  fallthrough); to grab the cheap card, remove the --exclude GPUs from\n"
                    f"  pod.gpu_order (price-cap is inert: GraphQL pricing is empty here)."
                )
            return True, f"[{_now()}] CHEAP CARD GETTABLE: {gpu} @ {dc} ({tier}, {price})\n{detail}"
    return False, f"[{_now()}] waiting | full_pick={full_str} | cheap_pick={cheap_str}"


def main(argv: list[str] | None = None) -> int:
    """Parse args and run the (looping) zero-spend cheap-GPU monitor."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, default=_DEFAULT_CFG, help="cheap sweep job-spec YAML")
    ap.add_argument("--interval", type=int, default=600, help="seconds between ticks (default 600)")
    ap.add_argument("--max-hours", type=float, default=24.0, help="give up after this many hours")
    ap.add_argument(
        "--accept-tiers",
        default="high,medium,low",
        help="comma stock tiers that count as gettable (default: high,medium,low)",
    )
    ap.add_argument(
        "--exclude",
        default=",".join(_DEFAULT_EXCLUDE),
        help="comma GPU names that define 'too expensive' (removed for cheap_pick)",
    )
    ap.add_argument("--once", action="store_true", help="single check then exit (no loop)")
    ap.add_argument(
        "--watch",
        action="store_true",
        help="persistent mode: emit a line ONLY on gettable<->not transitions "
        "(for the Monitor tool / a background tail). --max-hours<=0 runs forever.",
    )
    args = ap.parse_args(argv)

    spec = rd.load_job_spec(args.config)
    exclude = {name.strip() for name in args.exclude.split(",") if name.strip()}
    cheap_order = [g for g in spec.pod.gpu_order if g not in exclude]
    accept_tiers = {t.strip().lower() for t in args.accept_tiers.split(",") if t.strip()}
    _load_api_key_into_env()
    prices = pricing.fetch_gpu_prices(force_refresh=False)  # {} if GraphQL unavailable

    print(
        f"[{_now()}] cheap-gpu monitor armed | cheap_order={cheap_order} | "
        f"accept_tiers={sorted(accept_tiers)} | interval={args.interval}s | "
        f"max={args.max_hours}h | spend=NONE (dry inventory only)",
        flush=True,
    )

    if args.watch:
        prev: bool | None = None
        elapsed = 0.0
        while args.max_hours <= 0 or elapsed < args.max_hours * 3600:
            triggered, message = _tick(spec, cheap_order, accept_tiers, prices)
            if prev is None or triggered != prev:
                edge = "GETTABLE" if triggered else "NO LONGER GETTABLE"
                print(f"[transition -> {edge}] {message}", flush=True)
                prev = triggered
            time.sleep(args.interval)
            elapsed += args.interval
        print(f"[{_now()}] watch window ({args.max_hours}h) elapsed -- stopping", flush=True)
        return 0

    max_ticks = 1 if args.once else max(1, int(args.max_hours * 3600 / args.interval))
    for tick in range(max_ticks):
        triggered, message = _tick(spec, cheap_order, accept_tiers, prices)
        print(message, flush=True)
        if triggered:
            return 0
        if args.once or tick == max_ticks - 1:
            break
        time.sleep(args.interval)

    if args.once:
        return 0  # single-check mode: exit 0 regardless; read the line above
    print(f"[{_now()}] max wait ({args.max_hours}h) elapsed -- no cheap card gettable", flush=True)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
