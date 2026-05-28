from backend.security_layer.enforce_mode.models import EnforceActivationDecision
from backend.security_layer.enforce_mode.models import EnforceActivationDecisionStatus
from backend.security_layer.enforce_mode.models import EnforceApprovalStatus
from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceKillSwitchState
from backend.security_layer.enforce_mode.models import EnforceLiveEffect
from backend.security_layer.enforce_mode.models import EnforceReadinessContext
from backend.security_layer.enforce_mode.models import EnforceRollbackState
from backend.security_layer.enforce_mode.models import EnforceSimulatedEffect


def test_readiness_context_creation_uses_safe_placeholders() -> None:
    context = EnforceReadinessContext(control_family=EnforceControlFamily.RETRIEVAL_ACL)
    assert context.tenant_safe_id == "tenant-placeholder"
    assert context.workspace_safe_id == "workspace-placeholder"
    assert context.subject_safe_id == "subject-placeholder"
    assert context.schema_version


def test_activation_decision_creation_is_explicit_no_live_change() -> None:
    decision = EnforceActivationDecision(
        status=EnforceActivationDecisionStatus.BLOCKED,
        control_family=EnforceControlFamily.CACHE_SECURITY,
        simulated_effect=EnforceSimulatedEffect.NO_CHANGE,
        live_effect=EnforceLiveEffect.NO_CHANGE,
        approval_status=EnforceApprovalStatus.NOT_APPROVED,
        rollback_state=EnforceRollbackState.DISABLED,
        kill_switch_state=EnforceKillSwitchState.DISABLED,
        blast_radius_status=EnforceBlastRadiusStatus.NONE_ALLOWED,
        non_leakage_validation_passed=False,
        safe_denial_validation_passed=False,
        gate_results=(),
    )
    assert decision.live_effect == EnforceLiveEffect.NO_CHANGE
    assert decision.simulated_effect == EnforceSimulatedEffect.NO_CHANGE


def test_model_fields_do_not_store_raw_sensitive_content() -> None:
    field_names = set(EnforceReadinessContext.__dataclass_fields__)
    forbidden = {
        "query",
        "prompt",
        "document",
        "chunk",
        "secret",
        "raw_query",
        "raw_prompt",
        "raw_document",
        "raw_secret",
    }
    assert field_names.isdisjoint(forbidden)
