"""Tests for the research-only agent harness v0."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parent.parent.parent
HARNESS_DIR = ROOT / "experiments" / "agent-harness-v0"
CASES = HARNESS_DIR / "cases.jsonl"


def _load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


agent_run = _load_module("agent_harness_v0_run", HARNESS_DIR / "run.py")
agent_report = _load_module("agent_harness_v0_report", HARNESS_DIR / "report.py")


@pytest.mark.unit
def test_cases_load_and_validate() -> None:
    cases = agent_run.load_cases(CASES)
    assert len(cases) >= 6
    assert {case["carrier"] for case in cases} >= {"email", "table", "html", "tool_output"}


@pytest.mark.unit
def test_scripted_golden_security_behavior(tmp_path: Path) -> None:
    out = tmp_path / "scripted.jsonl"
    rows = agent_run.run_harness(
        cases_path=CASES,
        defenses=list(agent_run.DEFENSES),
        backend="scripted",
        out_path=out,
    )
    assert out.exists()
    assert len(rows) == len(agent_run.load_cases(CASES)) * len(agent_run.DEFENSES)

    attack_rows = [row for row in rows if row["is_attack"]]
    none_attack_rows = [row for row in attack_rows if row["defense"] == "none"]
    assert any(row["attack_success"] for row in none_attack_rows)

    for defense in ("tool_firewall", "provenance_gate"):
        rows_for_defense = [row for row in attack_rows if row["defense"] == defense]
        assert rows_for_defense
        assert not any(row["attack_success"] for row in rows_for_defense)


@pytest.mark.unit
def test_benign_instruction_like_text_is_not_blocked() -> None:
    cases = {case["case_id"]: case for case in agent_run.load_cases(CASES)}
    case = cases["benign_instruction_like_policy"]
    for defense in agent_run.DEFENSES:
        row = agent_run.run_case(case, defense=defense, backend="scripted")
        assert row["utility_success"], defense
        assert not row["over_defense"], defense
        assert not row["attack_success"], defense


@pytest.mark.unit
def test_allowed_draft_stays_benign_and_allowed() -> None:
    cases = {case["case_id"]: case for case in agent_run.load_cases(CASES)}
    case = cases["benign_allowed_draft"]
    for defense in agent_run.DEFENSES:
        row = agent_run.run_case(case, defense=defense, backend="scripted")
        assert not row["is_attack"], defense
        assert row["utility_success"], defense
        assert not row["over_defense"], defense
        assert not row["attack_success"], defense
        assert any(
            call["name"] == "create_draft"
            and call["status"] == "executed"
            and call["args"].get("to") == "accountant@example.com"
            for call in row["tool_calls"]
        ), defense


@pytest.mark.unit
def test_static_detector_gate_blocks_obvious_but_not_obfuscated() -> None:
    cases = {case["case_id"]: case for case in agent_run.load_cases(CASES)}
    direct = agent_run.run_case(cases["email_direct_exfil"], "static_detector_gate", "scripted")
    obfuscated = agent_run.run_case(
        cases["table_obfuscated_exfil"], "static_detector_gate", "scripted"
    )
    assert direct["blocked_documents"]
    assert not direct["attack_success"]
    assert not obfuscated["blocked_documents"]
    assert obfuscated["attack_success"]


@pytest.mark.unit
def test_report_computes_from_saved_traces(tmp_path: Path) -> None:
    results_path = tmp_path / "scripted.jsonl"
    report_path = tmp_path / "summary.md"
    rows = agent_run.run_harness(
        cases_path=CASES,
        defenses=list(agent_run.DEFENSES),
        backend="scripted",
        out_path=results_path,
    )
    loaded = [json.loads(line) for line in results_path.read_text().splitlines()]
    assert loaded == rows

    rendered = agent_report.write_report(agent_report.load_results(results_path), report_path)
    assert report_path.exists()
    assert "This report is computed from saved traces" in rendered
    assert "| none |" in rendered
    assert "| tool_firewall |" in rendered
    assert "Utility-Security Frontier" in rendered
