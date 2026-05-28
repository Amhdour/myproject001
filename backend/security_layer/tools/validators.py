from __future__ import annotations

from datetime import datetime, UTC

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.tools.models import ToolAuthorizationDecision, ToolAuthorizationStage, ToolDecisionStatus


def build_tool_decision(*, status: ToolDecisionStatus, stage: ToolAuthorizationStage, reason_code: str, message: str, safe_denial_category: str | None = None) -> ToolAuthorizationDecision:
    return ToolAuthorizationDecision(status=status, stage=stage, reason_code=reason_code, message=message, safe_denial_category=safe_denial_category)


def validate_tool_tenant_context(context):
    if context.tenant_scope is None or not context.tenant_scope.tenant_id:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.TENANT_SCOPE_VALIDATED, reason_code="tenant_missing", message="tenant required", safe_denial_category=DenialCategory.TENANT_CONTEXT_MISSING.value)
    return None


def validate_tool_subject_context(context):
    if context.permission_context is None or not context.permission_context.subject_id:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.SUBJECT_PERMISSION_VALIDATED, reason_code="subject_missing", message="subject required", safe_denial_category=DenialCategory.SUBJECT_CONTEXT_MISSING.value)
    return None


def validate_tool_workspace_scope(context):
    if context.workspace_scope is None or not context.workspace_scope.workspace_id:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.WORKSPACE_SCOPE_VALIDATED, reason_code="workspace_missing", message="workspace required", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    return None


def validate_tool_authorization_context(context):
    for fn in (validate_tool_tenant_context, validate_tool_subject_context, validate_tool_workspace_scope):
        decision = fn(context)
        if decision:
            return decision
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.TOOL_CONTEXT_VALIDATED, reason_code="ok", message="context valid")


def validate_tool_identity(context, registry_entry):
    if context.tool_id != registry_entry.tool_id:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.TOOL_IDENTITY_RESOLVED, reason_code="unknown_tool", message="tool unknown", safe_denial_category=DenialCategory.UNSAFE_TOOL_BLOCKED.value)
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.TOOL_IDENTITY_RESOLVED, reason_code="ok", message="tool matched")


def validate_tool_registry_entry_for_call(context, registry_entry):
    return validate_tool_identity(context, registry_entry)


def validate_tool_permission_context(context, registry_entry):
    pc = context.permission_context
    if not pc:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.SUBJECT_PERMISSION_VALIDATED, reason_code="permission_missing", message="permission required", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    if set(registry_entry.required_user_permissions) - set(pc.user_permissions):
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.SUBJECT_PERMISSION_VALIDATED, reason_code="user_permission_missing", message="missing user permission", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    if set(registry_entry.required_group_permissions) - set(pc.group_permissions):
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.SUBJECT_PERMISSION_VALIDATED, reason_code="group_permission_missing", message="missing group permission", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    if set(registry_entry.required_role_permissions) - set(pc.role_permissions):
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.SUBJECT_PERMISSION_VALIDATED, reason_code="role_permission_missing", message="missing role permission", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.SUBJECT_PERMISSION_VALIDATED, reason_code="ok", message="permissions valid")


def validate_service_account_permission(context, registry_entry):
    if context.caller.caller_type == "service" and not registry_entry.service_account_allowed:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.SERVICE_ACCOUNT_PERMISSION_VALIDATED, reason_code="service_account_out_of_scope", message="service account not allowed", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.SERVICE_ACCOUNT_PERMISSION_VALIDATED, reason_code="ok", message="service account valid")


def validate_delegated_credential(context, registry_entry):
    dc = context.delegated_credential
    if registry_entry.delegated_credential_required and dc is None:
        return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.DELEGATED_CREDENTIAL_VALIDATED, reason_code="delegated_credential_missing", message="delegated credential required", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    if dc is not None:
        if dc.expires_at <= datetime.now(UTC):
            return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.DELEGATED_CREDENTIAL_VALIDATED, reason_code="delegated_credential_expired", message="delegated credential expired", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
        if context.tenant_scope and dc.tenant_id != context.tenant_scope.tenant_id:
            return build_tool_decision(status=ToolDecisionStatus.DENIED, stage=ToolAuthorizationStage.DELEGATED_CREDENTIAL_VALIDATED, reason_code="delegated_credential_wrong_tenant", message="delegated credential tenant mismatch", safe_denial_category=DenialCategory.ACCESS_DENIED.value)
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.DELEGATED_CREDENTIAL_VALIDATED, reason_code="ok", message="delegated credential valid")


def validate_tool_risk_and_approval(context, registry_entry):
    if registry_entry.approval_required and registry_entry.tool_risk_tier.value == "high":
        if not context.approval_requirement or not context.approval_requirement.approved:
            return build_tool_decision(status=ToolDecisionStatus.APPROVAL_REQUIRED, stage=ToolAuthorizationStage.APPROVAL_REQUIREMENT_EVALUATED, reason_code="approval_required", message="approval required", safe_denial_category=DenialCategory.APPROVAL_REQUIRED.value)
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.APPROVAL_REQUIREMENT_EVALUATED, reason_code="ok", message="approval valid")


def validate_tool_result_safety(context, result_metadata):
    if result_metadata.flagged_unsafe or result_metadata.flagged_secret_leakage:
        return build_tool_decision(status=ToolDecisionStatus.FLAGGED, stage=ToolAuthorizationStage.TOOL_RESULT_SAFETY_VALIDATED, reason_code="unsafe_result_metadata", message="unsafe result metadata", safe_denial_category=DenialCategory.UNSAFE_TOOL_BLOCKED.value)
    return build_tool_decision(status=ToolDecisionStatus.ALLOWED, stage=ToolAuthorizationStage.TOOL_RESULT_SAFETY_VALIDATED, reason_code="ok", message="result metadata valid")
