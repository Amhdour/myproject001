"""Control-family enforce-mode simulations.

These helpers produce in-memory simulation evidence only and never call live
control implementations.
"""

from __future__ import annotations

from collections.abc import Callable

from backend.security_layer.enforce_mode.models import EnforceActivationDecision
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceFinding
from backend.security_layer.enforce_mode.models import EnforceLiveEffect
from backend.security_layer.enforce_mode.models import EnforceReadinessContext
from backend.security_layer.enforce_mode.models import EnforceSimulationRecord
from backend.security_layer.enforce_mode.simulator import (
    simulate_enforce_activation_decision,
)


def _simulate(
    context: EnforceReadinessContext,
    expected_family: EnforceControlFamily,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    del shadow_deny_decision
    if context.control_family != expected_family:
        raise ValueError("context control family does not match simulation helper")
    decision = simulate_enforce_activation_decision(context)
    finding = EnforceFinding(
        finding_id=f"simulated-{expected_family.value}-finding",
        control_family=expected_family,
        severity="info",
        sanitized_summary="in-memory enforce-mode gate simulation evidence only",
    )
    record = EnforceSimulationRecord(
        record_id=f"simulated-{expected_family.value}-record",
        control_family=expected_family,
        simulated_effect=decision.simulated_effect,
        live_effect=EnforceLiveEffect.NO_CHANGE,
        sanitized_summary="placeholder IDs only; no raw request, prompt, document, chunk, or secret data",
    )
    return EnforceActivationDecision(
        status=decision.status,
        control_family=decision.control_family,
        simulated_effect=decision.simulated_effect,
        live_effect=EnforceLiveEffect.NO_CHANGE,
        approval_status=decision.approval_status,
        rollback_state=decision.rollback_state,
        kill_switch_state=decision.kill_switch_state,
        blast_radius_status=decision.blast_radius_status,
        non_leakage_validation_passed=decision.non_leakage_validation_passed,
        safe_denial_validation_passed=decision.safe_denial_validation_passed,
        gate_results=decision.gate_results,
        findings=(finding,),
        simulation_records=(record,),
        reason=decision.reason,
    )


def simulate_retrieval_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(context, EnforceControlFamily.RETRIEVAL_ACL, shadow_deny_decision)


def simulate_vector_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(
        context, EnforceControlFamily.VECTOR_DB_SECURITY, shadow_deny_decision
    )


def simulate_cache_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(context, EnforceControlFamily.CACHE_SECURITY, shadow_deny_decision)


def simulate_tool_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(
        context, EnforceControlFamily.TOOL_AUTHORIZATION, shadow_deny_decision
    )


def simulate_mcp_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(context, EnforceControlFamily.MCP_HARDENING, shadow_deny_decision)


def simulate_artifact_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(
        context, EnforceControlFamily.ARTIFACT_SAFETY, shadow_deny_decision
    )


def simulate_ingestion_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(
        context, EnforceControlFamily.SECURE_INGESTION, shadow_deny_decision
    )


def simulate_safe_denial_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(context, EnforceControlFamily.SAFE_DENIAL, shadow_deny_decision)


def simulate_audit_metric_enforce_gate(
    context: EnforceReadinessContext,
    shadow_deny_decision: object | None = None,
) -> EnforceActivationDecision:
    return _simulate(
        context, EnforceControlFamily.AUDIT_FINDING_METRIC, shadow_deny_decision
    )


CONTROL_SIMULATORS: dict[
    EnforceControlFamily, Callable[[EnforceReadinessContext], EnforceActivationDecision]
] = {
    EnforceControlFamily.RETRIEVAL_ACL: simulate_retrieval_enforce_gate,
    EnforceControlFamily.VECTOR_DB_SECURITY: simulate_vector_enforce_gate,
    EnforceControlFamily.CACHE_SECURITY: simulate_cache_enforce_gate,
    EnforceControlFamily.TOOL_AUTHORIZATION: simulate_tool_enforce_gate,
    EnforceControlFamily.MCP_HARDENING: simulate_mcp_enforce_gate,
    EnforceControlFamily.ARTIFACT_SAFETY: simulate_artifact_enforce_gate,
    EnforceControlFamily.SECURE_INGESTION: simulate_ingestion_enforce_gate,
    EnforceControlFamily.SAFE_DENIAL: simulate_safe_denial_enforce_gate,
    EnforceControlFamily.AUDIT_FINDING_METRIC: simulate_audit_metric_enforce_gate,
}
