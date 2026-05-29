from __future__ import annotations

import importlib.util
from pathlib import Path
import socket
import subprocess
import sys
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = ROOT / "demo_attacks" / "run_demo_attacks.py"
EXPECTED_CASE_IDS = {
    "prompt_injection",
    "retrieval_cross_tenant_leakage",
    "unsafe_tool_call",
    "mcp_confused_deputy",
    "sensitive_data_exposure",
}


def load_runner_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("demo_attack_runner", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_all_five_demo_attack_cases_exist() -> None:
    runner = load_runner_module()

    cases = runner.get_demo_attack_cases()

    assert {case.case_id for case in cases} == EXPECTED_CASE_IDS
    assert len(cases) == 5


@pytest.mark.parametrize("case_id", sorted(EXPECTED_CASE_IDS))
def test_expected_outcomes_are_denied_or_flagged(case_id: str) -> None:
    runner = load_runner_module()

    cases_by_id = {case.case_id: case for case in runner.get_demo_attack_cases()}

    assert cases_by_id[case_id].expected_decision == "denied_or_flagged"
    assert runner.simulate_portfolio_decision(cases_by_id[case_id]) == "denied_or_flagged"


def test_runner_main_returns_success(capsys: pytest.CaptureFixture[str]) -> None:
    runner = load_runner_module()

    assert runner.main() == 0
    output = capsys.readouterr().out
    assert "Overall result: PASS" in output
    for case_id in EXPECTED_CASE_IDS:
        assert case_id in output


def test_runner_performs_no_network_tool_mcp_or_runtime_calls(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    runner = load_runner_module()

    def fail_network_or_process_call(*args: object, **kwargs: object) -> None:
        raise AssertionError(
            "demo attack runner must not perform network, tool, MCP, or runtime calls"
        )

    monkeypatch.setattr(socket, "socket", fail_network_or_process_call)
    monkeypatch.setattr(subprocess, "Popen", fail_network_or_process_call)
    monkeypatch.setattr(subprocess, "run", fail_network_or_process_call)
    monkeypatch.setattr(subprocess, "check_call", fail_network_or_process_call)
    monkeypatch.setattr(subprocess, "check_output", fail_network_or_process_call)

    assert runner.main() == 0
    output = capsys.readouterr().out
    assert "Network/tool/MCP calls performed: no." in output
