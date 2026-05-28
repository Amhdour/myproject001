from backend.security_layer.enforce_mode.feature_flags import DEFAULT_ENFORCE_FLAG_STATE
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState
from backend.security_layer.regression.models import RegressionDemoOutcome
from backend.security_layer.regression.runner import run_all_regression_demo_scenarios
from backend.security_layer.regression.runner import run_regression_demo_scenario
from backend.security_layer.regression.scenarios import get_regression_demo_scenarios
from backend.security_layer.shadow_deny.feature_flags import (
    DEFAULT_SHADOW_DENY_FLAG_STATE,
)


def test_runner_executes_all_scenarios_and_counts_outcomes() -> None:
    summary = run_all_regression_demo_scenarios()

    assert summary.total == 26
    assert summary.failed == 0
    assert summary.passed >= 2
    assert summary.flagged >= 10
    assert summary.blocked_isolated >= 2
    assert summary.simulated >= 3
    assert summary.approval_required >= 1
    assert summary.no_change >= 3
    assert summary.non_leakage_validated is True
    assert summary.behavior_preserved is True


def test_runner_preserves_live_behavior_and_runtime_modes() -> None:
    summary = run_all_regression_demo_scenarios()

    assert summary.live_blocking_enabled is False
    assert summary.live_filtering_enabled is False
    assert summary.enforce_mode_enabled is False
    assert summary.shadow_deny_runtime_enabled is False
    assert all(
        state is EnforceFeatureFlagState.DISABLED
        for state in DEFAULT_ENFORCE_FLAG_STATE.values()
    )
    assert not any(DEFAULT_SHADOW_DENY_FLAG_STATE.values())


def test_specific_scenario_outcomes_are_expected() -> None:
    scenarios = {
        scenario.scenario_id: scenario for scenario in get_regression_demo_scenarios()
    }

    assert (
        run_regression_demo_scenario(scenarios["RDA-002"]).outcome
        is RegressionDemoOutcome.SIMULATED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-003"]).outcome
        is RegressionDemoOutcome.FLAGGED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-004"]).outcome
        is RegressionDemoOutcome.FLAGGED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-005"]).outcome
        is RegressionDemoOutcome.FLAGGED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-007"]).outcome
        is RegressionDemoOutcome.FLAGGED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-009"]).outcome
        is RegressionDemoOutcome.BLOCKED_ISOLATED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-013"]).outcome
        is RegressionDemoOutcome.FLAGGED
    )
    assert (
        run_regression_demo_scenario(scenarios["RDA-015"]).outcome
        is RegressionDemoOutcome.FLAGGED
    )
    assert run_regression_demo_scenario(scenarios["RDA-018"]).behavior_preserved is True
    assert run_regression_demo_scenario(scenarios["RDA-020"]).behavior_preserved is True
    assert (
        run_regression_demo_scenario(scenarios["RDA-021"]).outcome
        is RegressionDemoOutcome.SIMULATED
    )
    assert run_regression_demo_scenario(scenarios["RDA-024"]).evidence_ref
