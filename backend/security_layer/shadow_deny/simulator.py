from datetime import datetime, UTC
from backend.security_layer.shadow_deny.decision_schema import build_shadow_deny_decision_record, sanitize_shadow_deny_decision_record
from backend.security_layer.shadow_deny.feature_flags import build_shadow_deny_flag_state, shadow_deny_compare_monitor_only_enabled, shadow_deny_decision_recording_enabled, shadow_deny_family_enabled, shadow_deny_rollback_enabled
from backend.security_layer.shadow_deny.models import *

IN_MEMORY_DECISION_LOG: list[ShadowDenyDecisionRecord] = []

def build_shadow_deny_simulation_context(**kwargs) -> ShadowDenySimulationContext:
    kwargs.setdefault("timestamp", datetime.now(UTC).isoformat())
    kwargs["flags"] = build_shadow_deny_flag_state(kwargs.get("flags", {}))
    return ShadowDenySimulationContext(**kwargs)

def simulate_shadow_deny_decision(context: ShadowDenySimulationContext, monitor_only_decision=None):
    enabled = shadow_deny_family_enabled(context.flags, context.control_family)
    if not enabled or shadow_deny_rollback_enabled(context.flags):
        status = ShadowDenyDecisionStatus.NOOP
        simulated = ShadowDenySimulatedEffect.NO_CHANGE
    else:
        status = ShadowDenyDecisionStatus.SIMULATED_DENY
        simulated = ShadowDenySimulatedEffect.DENY
    rec=build_shadow_deny_decision_record(
        decision_id=context.decision_id,timestamp=context.timestamp,control_family=context.control_family.value,stage=context.stage.value,
        tenant_id_hash_or_safe_id=context.tenant_id_hash_or_safe_id,workspace_id_hash_or_safe_id=context.workspace_id_hash_or_safe_id,subject_id_hash_or_safe_id=context.subject_id_hash_or_safe_id,
        decision_status=status.value,simulated_effect=simulated.value,live_effect=ShadowDenyLiveEffect.NO_CHANGE.value,monitor_only_decision_id=context.monitor_only_decision_id,
        deny_reason_code=context.deny_reason_code,safe_denial_category=context.safe_denial_category,finding_ids=[],metric_names=[],audit_event_id=f"audit-{context.decision_id}",evidence_ref=f"evidence/{context.decision_id}",
        rollback_flag_state=ShadowDenyRollbackState.ENABLED.value if shadow_deny_rollback_enabled(context.flags) else ShadowDenyRollbackState.DISABLED.value,
        feature_flag_state=ShadowDenyFeatureFlagState.ENABLED.value if enabled else ShadowDenyFeatureFlagState.DISABLED.value,non_leakage_validated=True,created_at=context.timestamp,
    )
    decision=ShadowDenySimulationDecision(decision_record=rec)
    if shadow_deny_compare_monitor_only_enabled(context.flags) and monitor_only_decision:
        decision.comparison = compare_shadow_deny_to_monitor_only(decision, monitor_only_decision)
    decision.recorded = record_shadow_deny_decision_if_enabled(context, decision)
    return sanitize_shadow_deny_simulation_output(decision)

def compare_shadow_deny_to_monitor_only(shadow_decision, monitor_only_decision):
    return ShadowDenyComparisonResult(monitor_only_decision_id=str(monitor_only_decision.get("decision_id","")),shadow_decision_id=shadow_decision.decision_record.decision_id,decision_status_match=False,simulated_effect_match=False)

def record_shadow_deny_decision_if_enabled(context, decision):
    if shadow_deny_decision_recording_enabled(context.flags):
        IN_MEMORY_DECISION_LOG.append(decision.decision_record)
        decision.audit_events.append(decision.decision_record.audit_event_id)
        decision.finding_ids.append(f"finding-{decision.decision_record.decision_id}")
        decision.metric_names.append("shadow_deny_simulated")
        return True
    return False

def apply_shadow_deny_rollback_if_enabled(context, decision):
    if shadow_deny_rollback_enabled(context.flags):
        decision.recorded = False
    return decision

def validate_shadow_deny_non_blocking(decision):
    return decision.decision_record.live_effect in {ShadowDenyLiveEffect.ALLOWED.value, ShadowDenyLiveEffect.NO_CHANGE.value}

def validate_shadow_deny_non_filtering(decision):
    return decision.decision_record.live_effect == ShadowDenyLiveEffect.NO_CHANGE.value

def sanitize_shadow_deny_simulation_output(decision):
    decision.decision_record = sanitize_shadow_deny_decision_record(decision.decision_record)
    return decision
