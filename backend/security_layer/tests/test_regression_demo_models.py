from backend.security_layer.regression.models import RegressionDemoExpectedResult
from backend.security_layer.regression.models import RegressionDemoFamily
from backend.security_layer.regression.models import RegressionDemoFixtureType
from backend.security_layer.regression.models import RegressionDemoOutcome
from backend.security_layer.regression.models import RegressionDemoResult
from backend.security_layer.regression.models import RegressionDemoRunSummary
from backend.security_layer.regression.models import RegressionDemoScenario
from backend.security_layer.regression.models import RegressionDemoScenarioStatus
from backend.security_layer.regression.models import RegressionDemoSeverity


def test_regression_demo_scenario_model_creation() -> None:
    scenario = RegressionDemoScenario(
        scenario_id="RDA-999",
        title="synthetic scenario",
        family=RegressionDemoFamily.MONITOR_ONLY_NO_BLOCK,
        status=RegressionDemoScenarioStatus.IMPLEMENTED,
        expected_result=RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE,
        severity=RegressionDemoSeverity.INFO,
        fixture_type=RegressionDemoFixtureType.SYNTHETIC_MONITOR_ONLY,
        mapped_controls=("monitor_only",),
        mapped_risks=("R-RDA-999",),
        evidence_ref="docs/security/evidence/regression_demo_attack_bundle/scenario_coverage.md#rda-999",
    )

    assert scenario.non_leakage_required is True
    assert scenario.behavior_preserving_required is True
    assert scenario.tenant_safe_id == "tenant_alpha"


def test_regression_demo_run_summary_model_creation() -> None:
    result = RegressionDemoResult(
        scenario_id="RDA-999",
        outcome=RegressionDemoOutcome.NO_CHANGE,
        expected_result=RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE,
        mapped_controls=("monitor_only",),
        mapped_risks=("R-RDA-999",),
        evidence_ref="evidence_ref_demo",
        sanitized_summary="safe synthetic summary",
        non_leakage_validated=True,
        behavior_preserved=True,
    )
    summary = RegressionDemoRunSummary(
        total=1,
        passed=0,
        failed=0,
        flagged=0,
        blocked_isolated=0,
        simulated=0,
        approval_required=0,
        no_change=1,
        non_leakage_validated=result.non_leakage_validated,
        behavior_preserved=result.behavior_preserved,
        live_blocking_enabled=False,
        live_filtering_enabled=False,
        enforce_mode_enabled=False,
        shadow_deny_runtime_enabled=False,
        evidence_refs=(result.evidence_ref,),
        sanitized_summary="safe synthetic summary",
    )

    assert summary.total == 1
    assert summary.no_change == 1
    assert not summary.live_blocking_enabled
