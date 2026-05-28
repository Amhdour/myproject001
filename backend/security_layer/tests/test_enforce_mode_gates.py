from dataclasses import replace

from backend.security_layer.enforce_mode.feature_flags import (
    ENFORCE_APPROVAL_GATE_ENABLED,
)
from backend.security_layer.enforce_mode.feature_flags import (
    ENFORCE_BLAST_RADIUS_LIMIT_ENABLED,
)
from backend.security_layer.enforce_mode.feature_flags import RETRIEVAL_ENFORCE_ENABLED
from backend.security_layer.enforce_mode.feature_flags import (
    SECURITY_ENFORCE_MODE_ENABLED,
)
from backend.security_layer.enforce_mode.gates import ENFORCE_ACTIVATION_GATES
from backend.security_layer.enforce_mode.gates import evaluate_all_enforce_gates
from backend.security_layer.enforce_mode.models import EnforceApprovalStatus
from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState
from backend.security_layer.enforce_mode.models import EnforceGateStatus
from backend.security_layer.enforce_mode.models import EnforceKillSwitchState
from backend.security_layer.enforce_mode.models import EnforceRollbackState
from backend.security_layer.enforce_mode.simulator import (
    build_enforce_readiness_context,
)


def _passing_context():
    return build_enforce_readiness_context(
        EnforceControlFamily.RETRIEVAL_ACL,
        feature_flags={
            SECURITY_ENFORCE_MODE_ENABLED: EnforceFeatureFlagState.ENABLED,
            RETRIEVAL_ENFORCE_ENABLED: EnforceFeatureFlagState.ENABLED,
            ENFORCE_APPROVAL_GATE_ENABLED: EnforceFeatureFlagState.ENABLED,
            ENFORCE_BLAST_RADIUS_LIMIT_ENABLED: EnforceFeatureFlagState.ENABLED,
        },
        approval_status=EnforceApprovalStatus.FULLY_APPROVED,
        rollback_state=EnforceRollbackState.AVAILABLE,
        kill_switch_state=EnforceKillSwitchState.AVAILABLE,
        blast_radius_status=EnforceBlastRadiusStatus.LIMITED,
        all_evidence_present=True,
    )


def test_all_12_gates_required_and_can_pass_in_isolated_context() -> None:
    results = evaluate_all_enforce_gates(_passing_context())
    assert len(ENFORCE_ACTIVATION_GATES) == 12
    assert len(results) == 12
    assert all(result.status == EnforceGateStatus.PASSED for result in results)


def test_missing_monitor_only_evidence_blocks_activation_gate() -> None:
    results = evaluate_all_enforce_gates(
        replace(_passing_context(), monitor_only_evidence_present=False)
    )
    assert results[0].status == EnforceGateStatus.BLOCKED


def test_missing_shadow_deny_evidence_blocks_activation_gate() -> None:
    results = evaluate_all_enforce_gates(
        replace(_passing_context(), shadow_deny_evidence_present=False)
    )
    assert results[1].status == EnforceGateStatus.BLOCKED


def test_missing_ci_staging_false_positive_incident_blocks_activation_gates() -> None:
    context = replace(
        _passing_context(),
        ci_evidence_present=False,
        staging_dry_run_evidence_present=False,
        false_positive_review_complete=False,
        incident_response_plan_present=False,
    )
    statuses = {
        result.gate_id: result.status for result in evaluate_all_enforce_gates(context)
    }
    assert statuses["EM-8"] == EnforceGateStatus.BLOCKED
    assert statuses["EM-9"] == EnforceGateStatus.BLOCKED
    assert statuses["EM-10"] == EnforceGateStatus.BLOCKED
    assert statuses["EM-11"] == EnforceGateStatus.BLOCKED


def test_non_leakage_safe_denial_and_telemetry_missing_block_activation_gates() -> None:
    context = replace(
        _passing_context(),
        non_leakage_validation_passed=False,
        safe_denial_validation_passed=False,
        audit_event_evidence_present=False,
        finding_evidence_present=False,
        metric_evidence_present=False,
    )
    statuses = {
        result.gate_id: result.status for result in evaluate_all_enforce_gates(context)
    }
    assert statuses["EM-5"] == EnforceGateStatus.BLOCKED
    assert statuses["EM-6"] == EnforceGateStatus.BLOCKED
    assert statuses["EM-7"] == EnforceGateStatus.BLOCKED


def test_approval_gate_required() -> None:
    context = replace(
        _passing_context(), approval_status=EnforceApprovalStatus.NOT_APPROVED
    )
    statuses = {
        result.gate_id: result.status for result in evaluate_all_enforce_gates(context)
    }
    assert statuses["EM-12"] == EnforceGateStatus.BLOCKED
