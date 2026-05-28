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
from backend.security_layer.enforce_mode.models import EnforceActivationDecisionStatus
from backend.security_layer.enforce_mode.models import EnforceApprovalStatus
from backend.security_layer.enforce_mode.models import EnforceBlastRadiusStatus
from backend.security_layer.enforce_mode.models import EnforceControlFamily
from backend.security_layer.enforce_mode.models import EnforceFeatureFlagState
from backend.security_layer.enforce_mode.models import EnforceKillSwitchState
from backend.security_layer.enforce_mode.models import EnforceLiveEffect
from backend.security_layer.enforce_mode.models import EnforceRollbackState
from backend.security_layer.enforce_mode.models import EnforceSimulatedEffect
from backend.security_layer.enforce_mode.simulator import (
    apply_enforce_kill_switch_if_enabled,
)
from backend.security_layer.enforce_mode.simulator import (
    apply_enforce_rollback_if_enabled,
)
from backend.security_layer.enforce_mode.simulator import (
    build_enforce_readiness_context,
)
from backend.security_layer.enforce_mode.simulator import compare_enforce_to_shadow_deny
from backend.security_layer.enforce_mode.simulator import (
    sanitize_enforce_simulation_output,
)
from backend.security_layer.enforce_mode.simulator import (
    simulate_enforce_activation_decision,
)
from backend.security_layer.enforce_mode.simulator import (
    validate_enforce_activation_blocked_by_default,
)
from backend.security_layer.enforce_mode.simulator import (
    validate_enforce_no_live_blocking,
)
from backend.security_layer.enforce_mode.simulator import (
    validate_enforce_no_live_filtering,
)


def _approved_context():
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


def test_enforce_mode_remains_disabled_by_default() -> None:
    context = build_enforce_readiness_context(EnforceControlFamily.RETRIEVAL_ACL)
    decision = simulate_enforce_activation_decision(context)
    assert validate_enforce_activation_blocked_by_default(context)
    assert decision.status == EnforceActivationDecisionStatus.BLOCKED
    assert decision.live_effect == EnforceLiveEffect.NO_CHANGE


def test_simulated_enforce_never_blocks_or_filters_live_response() -> None:
    decision = simulate_enforce_activation_decision(_approved_context())
    assert decision.status == EnforceActivationDecisionStatus.APPROVED_SIMULATION_ONLY
    assert decision.simulated_effect == EnforceSimulatedEffect.WOULD_BLOCK
    assert validate_enforce_no_live_blocking(decision)
    assert validate_enforce_no_live_filtering(decision)
    assert decision.live_effect == EnforceLiveEffect.NO_CHANGE


def test_rollback_flag_blocks_activation() -> None:
    context = replace(_approved_context(), rollback_state=EnforceRollbackState.ENABLED)
    decision = simulate_enforce_activation_decision(context)
    rolled_back = apply_enforce_rollback_if_enabled(context, decision)
    assert rolled_back.status == EnforceActivationDecisionStatus.BLOCKED
    assert rolled_back.live_effect == EnforceLiveEffect.NO_CHANGE


def test_kill_switch_blocks_activation() -> None:
    context = replace(
        _approved_context(), kill_switch_state=EnforceKillSwitchState.ENABLED
    )
    decision = simulate_enforce_activation_decision(context)
    killed = apply_enforce_kill_switch_if_enabled(context, decision)
    assert killed.status == EnforceActivationDecisionStatus.BLOCKED
    assert killed.live_effect == EnforceLiveEffect.NO_CHANGE


def test_compare_enforce_simulation_to_shadow_deny_simulation() -> None:
    decision = simulate_enforce_activation_decision(
        build_enforce_readiness_context(EnforceControlFamily.RETRIEVAL_ACL)
    )
    comparison = compare_enforce_to_shadow_deny(
        decision, shadow_deny_decision={"sanitized": True}
    )
    assert comparison["shadow_deny_status"] == "provided_sanitized_reference"
    assert comparison["comparison"] == "simulation_only_no_runtime_effect"


def test_sanitized_output_has_no_raw_query_prompt_document_chunk_or_secret() -> None:
    decision = simulate_enforce_activation_decision(_approved_context())
    output = sanitize_enforce_simulation_output(decision)
    output_text = str(output).lower()
    for forbidden in (
        "raw query",
        "raw prompt",
        "raw document",
        "raw chunk",
        "secret-value",
    ):
        assert forbidden not in output_text
