from __future__ import annotations

from backend.security_layer.runtime.audit import AuditEvent, write_audit_event
from backend.security_layer.runtime.findings import SecurityFinding, record_finding
from backend.security_layer.runtime.metrics import emit_security_metric
from backend.security_layer.tools.argument_validators import validate_prompt_derived_argument, validate_tool_arguments
from backend.security_layer.tools.models import ToolAuthorizationDecision, ToolAuthorizationStage, ToolDecisionStatus
from backend.security_layer.tools.validators import (
    build_tool_decision, validate_delegated_credential, validate_service_account_permission,
    validate_tool_authorization_context, validate_tool_identity, validate_tool_permission_context,
    validate_tool_result_safety, validate_tool_risk_and_approval,
)

def _ok(stage):
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=stage, reason_code="ok", message="ok")

def authorize_tool_registry_loaded(context): return _ok(ToolAuthorizationStage.TOOL_REGISTRY_LOADED)
def authorize_tool_registry_validated(context): return _ok(ToolAuthorizationStage.TOOL_REGISTRY_VALIDATED)
def authorize_tool_call_requested(context): return _ok(ToolAuthorizationStage.TOOL_CALL_REQUESTED)
def authorize_tool_context_validated(context): return validate_tool_authorization_context(context)
def authorize_tool_identity_resolved(context, registry_entry): return validate_tool_identity(context, registry_entry)
def authorize_caller_identity_resolved(context): return _ok(ToolAuthorizationStage.CALLER_IDENTITY_RESOLVED)
def authorize_tenant_scope_validated(context): return validate_tool_authorization_context(context)
def authorize_workspace_scope_validated(context): return validate_tool_authorization_context(context)
def authorize_subject_permission_validated(context, registry_entry): return validate_tool_permission_context(context, registry_entry)
def authorize_service_account_permission_validated(context, registry_entry): return validate_service_account_permission(context, registry_entry)
def authorize_delegated_credential_validated(context, registry_entry): return validate_delegated_credential(context, registry_entry)
def authorize_tool_risk_classified(context, registry_entry): return _ok(ToolAuthorizationStage.TOOL_RISK_CLASSIFIED)
def authorize_tool_argument_schema_validated(context, registry_entry): return _ok(ToolAuthorizationStage.TOOL_ARGUMENT_SCHEMA_VALIDATED)

def authorize_tool_argument_content_validated(context, registry_entry):
    decision = None
    if context.argument_schema is not None:
        validate_tool_arguments(context.arguments, context.argument_schema)
    for arg in context.arguments:
        marker = validate_prompt_derived_argument(str(arg.value))
        if marker.get("flagged_prompt_injection"):
            decision = build_tool_decision(status=ToolDecisionStatus.FLAGGED, stage=ToolAuthorizationStage.TOOL_ARGUMENT_CONTENT_VALIDATED, reason_code="prompt_injection_marker", message="prompt injection marker", safe_denial_category="unsafe_tool_blocked")
    return decision or _ok(ToolAuthorizationStage.TOOL_ARGUMENT_CONTENT_VALIDATED)

def authorize_approval_requirement_evaluated(context, registry_entry): return validate_tool_risk_and_approval(context, registry_entry)
def authorize_tool_execution_authorized(context, registry_entry): return _ok(ToolAuthorizationStage.TOOL_EXECUTION_AUTHORIZED)
def authorize_tool_result_received(context, result_metadata): return _ok(ToolAuthorizationStage.TOOL_RESULT_RECEIVED)
def authorize_tool_result_safety_validated(context, result_metadata): return validate_tool_result_safety(context, result_metadata)

def authorize_tool_audit_written(context):
    write_audit_event(AuditEvent(action="tool_authorization", decision="recorded", mode="isolated", request_id=context.request_id, details={"tool_id": context.tool_id}))
    emit_security_metric(action="tool_authorization", decision="recorded", mode="isolated")
    return _ok(ToolAuthorizationStage.TOOL_AUDIT_WRITTEN)

def authorize_tool_finding_recorded_if_needed(context):
    record_finding(SecurityFinding(action="tool_authorization", reason_code="isolated_finding", request_id=context.request_id))
    return _ok(ToolAuthorizationStage.TOOL_FINDING_RECORDED_IF_NEEDED)
