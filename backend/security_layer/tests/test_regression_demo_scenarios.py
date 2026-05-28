from backend.security_layer.regression.models import RegressionDemoExpectedResult
from backend.security_layer.regression.scenarios import get_regression_demo_scenarios
from backend.security_layer.regression.scenarios import map_scenario_to_controls
from backend.security_layer.regression.scenarios import map_scenario_to_expected_result
from backend.security_layer.regression.scenarios import (
    validate_all_regression_demo_scenarios,
)


def test_regression_demo_scenarios_present_and_unique() -> None:
    scenarios = get_regression_demo_scenarios()
    scenario_ids = [scenario.scenario_id for scenario in scenarios]

    assert len(scenarios) == 26
    assert len(scenario_ids) == len(set(scenario_ids))
    assert scenario_ids[0] == "RDA-001"
    assert scenario_ids[-1] == "RDA-026"


def test_regression_demo_scenario_mappings_are_valid() -> None:
    assert validate_all_regression_demo_scenarios() is True
    for scenario in get_regression_demo_scenarios():
        assert (
            map_scenario_to_controls(scenario.scenario_id) == scenario.mapped_controls
        )
        assert (
            map_scenario_to_expected_result(scenario.scenario_id)
            == scenario.expected_result
        )
        assert isinstance(scenario.expected_result, RegressionDemoExpectedResult)
        assert scenario.evidence_ref
