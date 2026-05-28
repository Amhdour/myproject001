"""Isolated enforce-mode activation gate evaluation."""

from __future__ import annotations

from collections.abc import Callable

from backend.security_layer.enforce_mode.feature_flags import (
    enforce_approval_gate_enabled,
)
from backend.security_layer.enforce_mode.feature_flags import (
    enforce_blast_radius_enabled,
)
from backend.security_layer.enforce_mode.feature_flags import enforce_family_enabled
from backend.security_layer.enforce_mode.feature_flags import validate_enforce_flags
from backend.security_layer.enforce_mode.models import EnforceApprovalStatus
from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceGateResult
from backend.security_layer.enforce_mode.models import EnforceGateStatus
from backend.security_layer.enforce_mode.models import EnforceKillSwitchState
from backend.security_layer.enforce_mode.models import EnforceReadinessContext
from backend.security_layer.enforce_mode.models import EnforceRollbackState

ENFORCE_ACTIVATION_GATES: tuple[str, ...] = (
    "EM-1",
    "EM-2",
    "EM-3",
    "EM-4",
    "EM-5",
    "EM-6",
    "EM-7",
    "EM-8",
    "EM-9",
    "EM-10",
    "EM-11",
    "EM-12",
)


def _gate(
    gate_id: str,
    passed: bool,
    reason: str,
    required_evidence: tuple[str, ...],
) -> EnforceGateResult:
    return EnforceGateResult(
        gate_id=gate_id,
        status=EnforceGateStatus.PASSED if passed else EnforceGateStatus.BLOCKED,
        reason=reason,
        required_evidence=required_evidence,
    )


def validate_monitor_only_evidence_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    return _gate(
        "EM-1",
        context.monitor_only_evidence_present,
        "monitor-only evidence required",
        ("monitor_only_evidence",),
    )


def validate_shadow_deny_evidence_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    return _gate(
        "EM-2",
        context.shadow_deny_evidence_present,
        "shadow-deny evidence required",
        ("shadow_deny_evidence",),
    )


def validate_feature_flag_gate(context: EnforceReadinessContext) -> EnforceGateResult:
    try:
        flags_valid = validate_enforce_flags(context.feature_flags)
        family_enabled = enforce_family_enabled(
            context.feature_flags, context.control_family
        )
        approval_enabled = enforce_approval_gate_enabled(context.feature_flags)
        blast_radius_enabled = enforce_blast_radius_enabled(context.feature_flags)
    except ValueError:
        return _gate(
            "EM-3",
            False,
            "valid default-disabled feature flags required",
            ("feature_flag_matrix",),
        )
    return _gate(
        "EM-3",
        flags_valid and family_enabled and approval_enabled and blast_radius_enabled,
        "global, family, approval, and blast-radius flags required for simulated activation",
        ("feature_flag_matrix",),
    )


def validate_rollback_kill_switch_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    passed = (
        context.rollback_state == EnforceRollbackState.AVAILABLE
        and context.kill_switch_state == EnforceKillSwitchState.AVAILABLE
        and context.rollback_evidence_present
        and context.kill_switch_evidence_present
    )
    return _gate(
        "EM-4",
        passed,
        "rollback and kill-switch evidence required",
        ("rollback_evidence", "kill_switch_evidence"),
    )


def validate_non_leakage_gate(context: EnforceReadinessContext) -> EnforceGateResult:
    return _gate(
        "EM-5",
        context.non_leakage_validation_passed,
        "non-leakage validation required",
        ("non_leakage_tests",),
    )


def validate_safe_denial_gate(context: EnforceReadinessContext) -> EnforceGateResult:
    return _gate(
        "EM-6",
        context.safe_denial_validation_passed,
        "safe-denial validation required",
        ("safe_denial_tests",),
    )


def validate_audit_finding_metric_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    passed = (
        context.audit_event_evidence_present
        and context.finding_evidence_present
        and context.metric_evidence_present
    )
    return _gate(
        "EM-7",
        passed,
        "audit, finding, and metric evidence required",
        ("audit_event", "finding", "metric"),
    )


def validate_ci_evidence_gate(context: EnforceReadinessContext) -> EnforceGateResult:
    return _gate(
        "EM-8", context.ci_evidence_present, "CI evidence required", ("ci_evidence",)
    )


def validate_staging_dry_run_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    return _gate(
        "EM-9",
        context.staging_dry_run_evidence_present,
        "staging dry-run evidence required",
        ("staging_dry_run",),
    )


def validate_false_positive_review_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    return _gate(
        "EM-10",
        context.false_positive_review_complete,
        "false-positive review required",
        ("false_positive_review",),
    )


def validate_incident_response_gate(
    context: EnforceReadinessContext,
) -> EnforceGateResult:
    return _gate(
        "EM-11",
        context.incident_response_plan_present,
        "incident response plan required",
        ("incident_response_plan",),
    )


def validate_final_approval_gate(context: EnforceReadinessContext) -> EnforceGateResult:
    passed = (
        context.approval_status == EnforceApprovalStatus.FULLY_APPROVED
        and context.blast_radius_status == EnforceBlastRadiusStatus.LIMITED
    )
    return _gate(
        "EM-12",
        passed,
        "limited-scope final approval required",
        ("owner_approval", "blast_radius_limit"),
    )


_GATE_VALIDATORS: dict[str, Callable[[EnforceReadinessContext], EnforceGateResult]] = {
    "EM-1": validate_monitor_only_evidence_gate,
    "EM-2": validate_shadow_deny_evidence_gate,
    "EM-3": validate_feature_flag_gate,
    "EM-4": validate_rollback_kill_switch_gate,
    "EM-5": validate_non_leakage_gate,
    "EM-6": validate_safe_denial_gate,
    "EM-7": validate_audit_finding_metric_gate,
    "EM-8": validate_ci_evidence_gate,
    "EM-9": validate_staging_dry_run_gate,
    "EM-10": validate_false_positive_review_gate,
    "EM-11": validate_incident_response_gate,
    "EM-12": validate_final_approval_gate,
}


def evaluate_enforce_gate(
    gate_id: str, context: EnforceReadinessContext
) -> EnforceGateResult:
    if gate_id not in _GATE_VALIDATORS:
        raise ValueError("unknown enforce activation gate")
    return _GATE_VALIDATORS[gate_id](context)


def evaluate_all_enforce_gates(
    context: EnforceReadinessContext,
) -> tuple[EnforceGateResult, ...]:
    return tuple(
        evaluate_enforce_gate(gate_id, context) for gate_id in ENFORCE_ACTIVATION_GATES
    )
