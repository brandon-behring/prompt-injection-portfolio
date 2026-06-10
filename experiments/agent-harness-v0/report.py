#!/usr/bin/env python3
"""Render a Markdown report from saved agent-harness traces."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_results(path: Path) -> list[dict[str, Any]]:
    """Load JSONL traces produced by run.py."""
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for lineno, line in enumerate(handle, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                rows.append(json.loads(stripped))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
    if not rows:
        raise ValueError(f"{path}: no result rows found")
    return rows


def _rate(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return numerator / denominator


def _fmt(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.3f}"


def _group(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key, "unknown"))].append(row)
    return dict(grouped)


def summarize_defense(rows: list[dict[str, Any]]) -> dict[str, float | int | None]:
    """Compute primary metrics from persisted labels only."""
    attack_rows = [row for row in rows if row.get("is_attack")]
    benign_rows = [row for row in rows if not row.get("is_attack")]
    return {
        "n": len(rows),
        "attack_n": len(attack_rows),
        "benign_n": len(benign_rows),
        "asr": _rate(sum(bool(row.get("attack_success")) for row in attack_rows), len(attack_rows)),
        "utility": _rate(sum(bool(row.get("utility_success")) for row in rows), len(rows)),
        "over_defense_rate": _rate(
            sum(bool(row.get("over_defense")) for row in benign_rows), len(benign_rows)
        ),
        "parse_fail_rate": _rate(sum(bool(row.get("parse_fail")) for row in rows), len(rows)),
    }


def summarize_asr_by(rows: list[dict[str, Any]], field: str) -> dict[str, float | None]:
    """Compute ASR by carrier or attack style."""
    out: dict[str, float | None] = {}
    for value, group_rows in sorted(
        _group([row for row in rows if row.get("is_attack")], field).items()
    ):
        out[value] = _rate(
            sum(bool(row.get("attack_success")) for row in group_rows), len(group_rows)
        )
    return out


def render_report(rows: list[dict[str, Any]]) -> str:
    """Render a compact Markdown report."""
    by_defense = _group(rows, "defense")
    summaries = {
        defense: summarize_defense(group_rows) for defense, group_rows in by_defense.items()
    }
    baseline = summaries.get("none", {})
    baseline_asr = baseline.get("asr") if isinstance(baseline.get("asr"), float) else None
    baseline_utility = (
        baseline.get("utility") if isinstance(baseline.get("utility"), float) else None
    )

    lines: list[str] = [
        "# Agent Harness V0 Report",
        "",
        "This report is computed from saved traces, not live agent state.",
        "",
        "## Primary Metrics",
        "",
        "| Defense | n | Attack n | Benign n | ASR | Utility | Over-defense | Parse fail |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for defense in sorted(summaries):
        summary = summaries[defense]
        lines.append(
            "| {defense} | {n} | {attack_n} | {benign_n} | {asr} | {utility} | "
            "{over_defense} | {parse_fail} |".format(
                defense=defense,
                n=summary["n"],
                attack_n=summary["attack_n"],
                benign_n=summary["benign_n"],
                asr=_fmt(summary["asr"] if isinstance(summary["asr"], float) else None),
                utility=_fmt(summary["utility"] if isinstance(summary["utility"], float) else None),
                over_defense=_fmt(
                    summary["over_defense_rate"]
                    if isinstance(summary["over_defense_rate"], float)
                    else None
                ),
                parse_fail=_fmt(
                    summary["parse_fail_rate"]
                    if isinstance(summary["parse_fail_rate"], float)
                    else None
                ),
            )
        )

    lines.extend(
        [
            "",
            "## Utility-Security Frontier",
            "",
            "| Defense | ASR reduction vs none | Utility loss vs none |",
            "|---|---:|---:|",
        ]
    )
    for defense in sorted(summaries):
        summary = summaries[defense]
        asr = summary.get("asr")
        utility = summary.get("utility")
        asr_reduction = (
            baseline_asr - asr if baseline_asr is not None and isinstance(asr, float) else None
        )
        utility_loss = (
            baseline_utility - utility
            if baseline_utility is not None and isinstance(utility, float)
            else None
        )
        lines.append(f"| {defense} | {_fmt(asr_reduction)} | {_fmt(utility_loss)} |")

    lines.extend(["", "## ASR By Carrier"])
    for defense in sorted(by_defense):
        lines.extend(["", f"### {defense}", "", "| Carrier | ASR |", "|---|---:|"])
        for carrier, value in summarize_asr_by(by_defense[defense], "carrier").items():
            lines.append(f"| {carrier} | {_fmt(value)} |")

    lines.extend(["", "## ASR By Attack Style"])
    for defense in sorted(by_defense):
        lines.extend(["", f"### {defense}", "", "| Attack style | ASR |", "|---|---:|"])
        for style, value in summarize_asr_by(by_defense[defense], "attack_style").items():
            lines.append(f"| {style} | {_fmt(value)} |")

    lines.extend(
        [
            "",
            "## Claim Boundaries",
            "",
            "- Scripted results validate benchmark plumbing and defense semantics.",
            "- Static detector numbers are a baseline, not a detector-quality claim.",
            "- Optional LLM runs are exploratory unless model, prompt, and trace versions "
            "are pinned.",
            "- This v0 does not replace AgentDojo, LLMail-Inject, PIArena, ARGUS, or "
            "CaMeL-scale evaluation.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_report(rows: list[dict[str, Any]], path: Path) -> str:
    """Render and persist the report."""
    rendered = render_report(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rendered, encoding="utf-8")
    return rendered


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    rows = load_results(args.results)
    write_report(rows, args.out)
    print(f"wrote report to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
