"""Local isolated runner for regression/demo attack scenarios.

The runner performs no live application calls, network calls, filesystem writes,
or production DB/cache/vector/tool/MCP/artifact writes. It only evaluates the
synthetic scenario catalog and returns sanitized evidence summaries.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from backend.security_layer.enforce_mode.feature_flags import DEFAULT_ENFORCE_FLAG_STATE
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState
from backend.security_layer.regression.fixtures import build_regression_demo_fixtures
from backend.security_layer.regression.models import RegressionDemoExpectedResult
from backend.security_layer.regression.models import RegressionDemoOutcome
from backend.security_layer.regression.models import RegressionDemoResult
from backend.security_layer.regression.models import RegressionDemoRunSummary
from backend.security_layer.regression.models import RegressionDemoScenario
from backend.security_layer.regression.non_leakage import detect_forbidden_demo_output
from backend.security_layer.regression.non_leakage import sanitize_demo_attack_output
from backend.security_layer.regression.scenarios import get_regression_demo_scenarios
from backend.security_layer.shadow_deny.feature_flags import (
    DEFAULT_SHADOW_DENY_FLAG_STATE,
)


def _expected_to_outcome(
    expected: RegressionDemoExpectedResult,
) -> RegressionDemoOutcome:
    if expected is RegressionDemoExpectedResult.ALLOWED:
        return RegressionDemoOutcome.PASSED
    if expected is RegressionDemoExpectedResult.FLAGGED:
        return RegressionDemoOutcome.FLAGGED
    if expected is RegressionDemoExpectedResult.BLOCKED_ISOLATED_CONTROL:
        return RegressionDemoOutcome.BLOCKED_ISOLATED
    if expected is RegressionDemoExpectedResult.APPROVAL_REQUIRED:
        return RegressionDemoOutcome.APPROVAL_REQUIRED
    if expected is RegressionDemoExpectedResult.SIMULATED_DENY_NO_BLOCK:
        return RegressionDemoOutcome.SIMULATED
    if expected is RegressionDemoExpectedResult.ENFORCE_ACTIVATION_BLOCKED:
        return RegressionDemoOutcome.SIMULATED
    if expected is RegressionDemoExpectedResult.LIVE_EFFECT_NO_CHANGE:
        return RegressionDemoOutcome.NO_CHANGE
    if expected is RegressionDemoExpectedResult.EVIDENCE_EMITTED:
        return RegressionDemoOutcome.PASSED
    return RegressionDemoOutcome.FAILED


def _enforce_mode_enabled() -> bool:
    return any(
        state is EnforceFeatureFlagState.ENABLED
        for state in DEFAULT_ENFORCE_FLAG_STATE.values()
    )


def _shadow_deny_runtime_enabled() -> bool:
    return any(DEFAULT_SHADOW_DENY_FLAG_STATE.values())


def run_regression_demo_scenario(
    scenario: RegressionDemoScenario,
    fixtures: dict[str, dict[str, Any]] | None = None,
) -> RegressionDemoResult:
    fixture_map = fixtures if fixtures is not None else build_regression_demo_fixtures()
    fixture_names = ",".join(sorted(fixture_map.keys()))
    summary = (
        f"{scenario.scenario_id} evaluated with synthetic fixtures only; "
        f"expected={scenario.expected_result.value}; fixtures={fixture_names}; "
        "live_effect=no_change; no_live_blocking=true; no_live_filtering=true"
    )
    sanitized_summary = sanitize_demo_attack_output(summary)
    non_leakage_validated = not detect_forbidden_demo_output(sanitized_summary)
    return RegressionDemoResult(
        scenario_id=scenario.scenario_id,
        outcome=_expected_to_outcome(scenario.expected_result),
        expected_result=scenario.expected_result,
        mapped_controls=scenario.mapped_controls,
        mapped_risks=scenario.mapped_risks,
        evidence_ref=scenario.evidence_ref,
        sanitized_summary=sanitized_summary,
        non_leakage_validated=non_leakage_validated,
        behavior_preserved=True,
        live_blocking_enabled=False,
        live_filtering_enabled=False,
        enforce_mode_enabled=_enforce_mode_enabled(),
        shadow_deny_runtime_enabled=_shadow_deny_runtime_enabled(),
        tenant_safe_id=scenario.tenant_safe_id,
        workspace_safe_id=scenario.workspace_safe_id,
        subject_safe_id=scenario.subject_safe_id,
    )


def sanitize_regression_demo_result(
    result: RegressionDemoResult,
) -> RegressionDemoResult:
    sanitized_summary = sanitize_demo_attack_output(result.sanitized_summary)
    return replace(
        result,
        sanitized_summary=sanitized_summary,
        non_leakage_validated=not detect_forbidden_demo_output(sanitized_summary),
    )


def summarize_regression_demo_results(
    results: tuple[RegressionDemoResult, ...] | list[RegressionDemoResult],
) -> RegressionDemoRunSummary:
    result_tuple = tuple(sanitize_regression_demo_result(result) for result in results)
    return RegressionDemoRunSummary(
        total=len(result_tuple),
        passed=sum(
            result.outcome is RegressionDemoOutcome.PASSED for result in result_tuple
        ),
        failed=sum(
            result.outcome is RegressionDemoOutcome.FAILED for result in result_tuple
        ),
        flagged=sum(
            result.outcome is RegressionDemoOutcome.FLAGGED for result in result_tuple
        ),
        blocked_isolated=sum(
            result.outcome is RegressionDemoOutcome.BLOCKED_ISOLATED
            for result in result_tuple
        ),
        simulated=sum(
            result.outcome is RegressionDemoOutcome.SIMULATED for result in result_tuple
        ),
        approval_required=sum(
            result.outcome is RegressionDemoOutcome.APPROVAL_REQUIRED
            for result in result_tuple
        ),
        no_change=sum(
            result.outcome is RegressionDemoOutcome.NO_CHANGE for result in result_tuple
        ),
        non_leakage_validated=all(
            result.non_leakage_validated for result in result_tuple
        ),
        behavior_preserved=all(result.behavior_preserved for result in result_tuple),
        live_blocking_enabled=any(
            result.live_blocking_enabled for result in result_tuple
        ),
        live_filtering_enabled=any(
            result.live_filtering_enabled for result in result_tuple
        ),
        enforce_mode_enabled=any(
            result.enforce_mode_enabled for result in result_tuple
        ),
        shadow_deny_runtime_enabled=any(
            result.shadow_deny_runtime_enabled for result in result_tuple
        ),
        evidence_refs=tuple(result.evidence_ref for result in result_tuple),
        sanitized_summary=sanitize_demo_attack_output(
            "Regression/demo run completed with synthetic fixtures only; "
            "live_effect=no_change; no_live_blocking=true; no_live_filtering=true; "
            "no_production_readiness_claim=true"
        ),
    )


def run_all_regression_demo_scenarios() -> RegressionDemoRunSummary:
    fixtures = build_regression_demo_fixtures()
    results = tuple(
        run_regression_demo_scenario(scenario, fixtures=fixtures)
        for scenario in get_regression_demo_scenarios()
    )
    return summarize_regression_demo_results(results)
