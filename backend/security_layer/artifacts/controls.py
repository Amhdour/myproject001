from __future__ import annotations

from backend.security_layer.artifacts.models import ArtifactDecisionStatus, ArtifactSecurityContext
from backend.security_layer.artifacts.validators import build_artifact_decision, validate_artifact_context_and_metadata, validate_artifact_namespace_authorization
from backend.security_layer.runtime.audit import AuditEvent, write_audit_event
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import SecurityFinding, record_finding
from backend.security_layer.runtime.metrics import emit_security_metric


def authorize_artifact_stage(context: ArtifactSecurityContext):
    if not validate_artifact_context_and_metadata(context):
        emit_security_metric(context.stage.value, ArtifactDecisionStatus.DENY.value, "inactive")
        return build_artifact_decision(context, ArtifactDecisionStatus.DENY, "invalid artifact context or metadata", DenialCategory.VALIDATION_FAILED)
    if not validate_artifact_namespace_authorization(context):
        emit_security_metric(context.stage.value, ArtifactDecisionStatus.DENY.value, "inactive")
        return build_artifact_decision(context, ArtifactDecisionStatus.DENY, "unauthorized namespace", DenialCategory.ACCESS_DENIED)
    write_audit_event(AuditEvent(action=context.stage.value, decision="allow", mode="inactive", request_id=context.request_id))
    record_finding(SecurityFinding(action=context.stage.value, reason_code="artifact_safety_stage", request_id=context.request_id))
    emit_security_metric(context.stage.value, ArtifactDecisionStatus.ALLOW.value, "inactive")
    return build_artifact_decision(context, ArtifactDecisionStatus.ALLOW, "artifact stage validated")
