"""Isolated enforce-mode gate simulation.

No function in this module integrates with live retrieval, vector, cache, tool,
MCP, artifact, ingestion, prompt, or worker paths.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from backend.security_layer.enforce_mode.feature_flags import build_enforce_flag_state
from backend.security_layer.enforce_mode.feature_flags import enforce_family_enabled
from backend.security_layer.enforce_mode.gates import evaluate_all_enforce_gates
from backend.security_layer.enforce_mode.models import EnforceActivationDecision
from backend.security_layer.enforce_mode.models import EnforceActivationDecisionStatus
from backend.security_layer.enforce_mode.models import EnforceApprovalStatus
from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState
from backend.security_layer.enforce_mode.models import EnforceGateStatus
from backend.security_layer.enforce_mode.models import EnforceKillSwitchState
from backend.security_layer.enforce_mode.models import EnforceLiveEffect
from backend.security_layer.enforce_mode.models import EnforceReadinessContext
from backend.security_layer.enforce_mode.models import EnforceReadinessStage
from backend.security_layer.enforce_mode.models import EnforceRollbackState
from backend.security_layer.enforce_mode.models import EnforceSimulatedEffect


def build_enforce_readiness_context(
    control_family: EnforceControlFamily,
    *,
    feature_flags: Mapping[str, EnforceFeatureFlagState | str] | None = None,
    approval_status: EnforceApprovalStatus = EnforceApprovalStatus.NOT_APPROVED,
    rollback_state: EnforceRollbackState = EnforceRollbackState.DISABLED,
    kill_switch_state: EnforceKillSwitchState = EnforceKillSwitchState.DISABLED,
    blast_radius_status: EnforceBlastRadiusStatus = EnforceBlastRadiusStatus.NONE_ALLOWED,
    all_evidence_present: bool = False,
) -> EnforceReadinessContext:
    return EnforceReadinessContext(
        control_family=control_family,
        stage=EnforceReadinessStage.SIMULATED,
        feature_flags=build_enforce_flag_state(feature_flags),
        approval_status=approval_status,
        rollback_state=rollback_state,
        kill_switch_state=kill_switch_state,
        blast_radius_status=blast_radius_status,
        monitor_only_evidence_present=all_evidence_present,
        shadow_deny_evidence_present=all_evidence_present,
        ci_evidence_present=all_evidence_present,
        staging_dry_run_evidence_present=all_evidence_present,
        false_positive_review_complete=all_evidence_present,
        incident_response_plan_present=all_evidence_present,
        non_leakage_validation_passed=all_evidence_present,
        safe_denial_validation_passed=all_evidence_present,
        audit_event_evidence_present=all_evidence_present,
        finding_evidence_present=all_evidence_present,
        metric_evidence_present=all_evidence_present,
        rollback_evidence_present=all_evidence_present,
        kill_switch_evidence_present=all_evidence_present,
    )


def simulate_enforce_activation_decision(
    context: EnforceReadinessContext,
) -> EnforceActivationDecision:
    gate_results = evaluate_all_enforce_gates(context)
    gates_pass = all(
        result.status == EnforceGateStatus.PASSED for result in gate_results
    )
    family_enabled = enforce_family_enabled(
        context.feature_flags, context.control_family
    )
    rollback_forces_noop = context.rollback_state == EnforceRollbackState.ENABLED
    kill_switch_forces_noop = (
        context.kill_switch_state == EnforceKillSwitchState.ENABLED
    )
    approved = (
        gates_pass
        and family_enabled
        and not rollback_forces_noop
        and not kill_switch_forces_noop
    )
    return EnforceActivationDecision(
        status=(
            EnforceActivationDecisionStatus.APPROVED_SIMULATION_ONLY
            if approved
            else EnforceActivationDecisionStatus.BLOCKED
        ),
        control_family=context.control_family,
        simulated_effect=(
            EnforceSimulatedEffect.WOULD_BLOCK
            if approved
            else EnforceSimulatedEffect.NO_CHANGE
        ),
        live_effect=EnforceLiveEffect.NO_CHANGE,
        approval_status=context.approval_status,
        rollback_state=context.rollback_state,
        kill_switch_state=context.kill_switch_state,
        blast_radius_status=context.blast_radius_status,
        non_leakage_validation_passed=context.non_leakage_validation_passed,
        safe_denial_validation_passed=context.safe_denial_validation_passed,
        gate_results=gate_results,
        reason=(
            "approved simulation only"
            if approved
            else "blocked by enforce-mode readiness gates"
        ),
    )


def compare_enforce_to_shadow_deny(
    enforce_decision: EnforceActivationDecision,
    shadow_deny_decision: object | None = None,
) -> dict[str, str]:
    shadow_status = (
        "not_provided"
        if shadow_deny_decision is None
        else "provided_sanitized_reference"
    )
    return {
        "enforce_status": enforce_decision.status.value,
        "enforce_live_effect": enforce_decision.live_effect.value,
        "shadow_deny_status": shadow_status,
        "comparison": "simulation_only_no_runtime_effect",
    }


def validate_enforce_activation_blocked_by_default(
    context: EnforceReadinessContext,
) -> bool:
    return (
        simulate_enforce_activation_decision(context).status
        == EnforceActivationDecisionStatus.BLOCKED
    )


def validate_enforce_no_live_blocking(decision: EnforceActivationDecision) -> bool:
    return decision.live_effect == EnforceLiveEffect.NO_CHANGE


def validate_enforce_no_live_filtering(decision: EnforceActivationDecision) -> bool:
    return decision.live_effect == EnforceLiveEffect.NO_CHANGE


def apply_enforce_rollback_if_enabled(
    context: EnforceReadinessContext,
    decision: EnforceActivationDecision,
) -> EnforceActivationDecision:
    if context.rollback_state != EnforceRollbackState.ENABLED:
        return decision
    return _blocked_no_change(
        decision, "rollback enabled; simulated activation disabled"
    )


def apply_enforce_kill_switch_if_enabled(
    context: EnforceReadinessContext,
    decision: EnforceActivationDecision,
) -> EnforceActivationDecision:
    if context.kill_switch_state != EnforceKillSwitchState.ENABLED:
        return decision
    return _blocked_no_change(
        decision, "kill switch enabled; simulated activation disabled"
    )


def sanitize_enforce_simulation_output(
    decision: EnforceActivationDecision,
) -> dict[str, Any]:
    return {
        "status": decision.status.value,
        "control_family": decision.control_family.value,
        "simulated_effect": decision.simulated_effect.value,
        "live_effect": decision.live_effect.value,
        "approval_status": decision.approval_status.value,
        "rollback_state": decision.rollback_state.value,
        "kill_switch_state": decision.kill_switch_state.value,
        "blast_radius_status": decision.blast_radius_status.value,
        "gate_statuses": {
            result.gate_id: result.status.value for result in decision.gate_results
        },
        "schema_version": decision.schema_version,
    }


def _blocked_no_change(
    decision: EnforceActivationDecision, reason: str
) -> EnforceActivationDecision:
    return EnforceActivationDecision(
        status=EnforceActivationDecisionStatus.BLOCKED,
        control_family=decision.control_family,
        simulated_effect=EnforceSimulatedEffect.NO_CHANGE,
        live_effect=EnforceLiveEffect.NO_CHANGE,
        approval_status=decision.approval_status,
        rollback_state=decision.rollback_state,
        kill_switch_state=decision.kill_switch_state,
        blast_radius_status=decision.blast_radius_status,
        non_leakage_validation_passed=decision.non_leakage_validation_passed,
        safe_denial_validation_passed=decision.safe_denial_validation_passed,
        gate_results=decision.gate_results,
        findings=decision.findings,
        simulation_records=decision.simulation_records,
        reason=reason,
    )
