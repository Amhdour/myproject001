from backend.security_layer.regression.non_leakage import detect_forbidden_demo_output
from backend.security_layer.regression.non_leakage import sanitize_demo_attack_output
from backend.security_layer.regression.non_leakage import (
    validate_regression_result_non_leakage,
)
from backend.security_layer.regression.non_leakage import validate_summary_non_leakage
from backend.security_layer.regression.runner import run_all_regression_demo_scenarios
from backend.security_layer.regression.runner import run_regression_demo_scenario
from backend.security_layer.regression.scenarios import get_regression_demo_scenarios


def test_forbidden_output_detection_and_sanitization() -> None:
    unsafe = "api_key=sk-demo123456 and person@example.com raw_prompt: hidden"

    assert detect_forbidden_demo_output(unsafe) is True
    sanitized = sanitize_demo_attack_output(unsafe)
    assert "person@example.com" not in sanitized
    assert "raw_prompt:" not in sanitized
    assert not detect_forbidden_demo_output(sanitized)


def test_results_and_summary_are_non_leaking() -> None:
    scenarios = get_regression_demo_scenarios()
    for scenario in scenarios:
        result = run_regression_demo_scenario(scenario)
        assert validate_regression_result_non_leakage(result) is True
        assert "raw_prompt" not in result.sanitized_summary
        assert "raw_document" not in result.sanitized_summary
        assert "raw_chunk" not in result.sanitized_summary

    summary = run_all_regression_demo_scenarios()
    assert validate_summary_non_leakage(summary) is True
    assert "production_readiness_claim=false" not in summary.sanitized_summary
    assert "no_production_readiness_claim=true" in summary.sanitized_summary
