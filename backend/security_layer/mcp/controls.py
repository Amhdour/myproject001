# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from __future__ import annotations
from backend.security_layer.runtime.audit import AuditEvent, write_audit_event
from backend.security_layer.runtime.findings import SecurityFinding, record_finding
from backend.security_layer.runtime.metrics import emit_security_metric
from .models import MCPDecisionStatus, MCPHardeningContext, MCPHardeningDecision, MCPHardeningStage
from .request_validators import validate_mcp_request_arguments
from .validators import validate_mcp_hardening_context, validate_mcp_response_safety, validate_mcp_risk_and_approval


def _mk(stage,status,reason,ctx):
    emit_security_metric("mcp_hardening",status.value,"isolation")
    if status!=MCPDecisionStatus.ALLOWED:
        record_finding(SecurityFinding("mcp_hardening",reason,ctx.request_id))
    return MCPHardeningDecision(stage,status,reason)

def authorize_mcp_registry_loaded(context): return _mk(MCPHardeningStage.REGISTRY_LOADED,MCPDecisionStatus.ALLOWED,"ok",context)
def authorize_mcp_registry_validated(context): return _mk(MCPHardeningStage.REGISTRY_VALIDATED,MCPDecisionStatus.ALLOWED,"ok",context)
def authorize_mcp_request_received(context): return _mk(MCPHardeningStage.REQUEST_RECEIVED,MCPDecisionStatus.ALLOWED,"ok",context)
def authorize_mcp_context_validated(context): return validate_mcp_hardening_context(context)
def authorize_mcp_server_identity_resolved(context, registry_entry): return _mk(MCPHardeningStage.SERVER_IDENTITY_RESOLVED,MCPDecisionStatus.DENIED if context.mcp_server_id!=registry_entry.get('mcp_server_id') else MCPDecisionStatus.ALLOWED,"unknown_server" if context.mcp_server_id!=registry_entry.get('mcp_server_id') else "ok",context)
def authorize_mcp_client_identity_resolved(context): return _mk(MCPHardeningStage.CLIENT_IDENTITY_RESOLVED,MCPDecisionStatus.DENIED if not context.mcp_client_id else MCPDecisionStatus.ALLOWED,"missing_client" if not context.mcp_client_id else "ok",context)
def authorize_mcp_tool_identity_resolved(context, registry_entry): return _mk(MCPHardeningStage.TOOL_IDENTITY_RESOLVED,MCPDecisionStatus.DENIED if context.mcp_tool_id!=registry_entry.get('mcp_tool_id') else MCPDecisionStatus.ALLOWED,"unknown_tool" if context.mcp_tool_id!=registry_entry.get('mcp_tool_id') else "ok",context)
def authorize_mcp_resource_identity_resolved(context, registry_entry): return _mk(MCPHardeningStage.RESOURCE_IDENTITY_RESOLVED,MCPDecisionStatus.DENIED if context.mcp_resource_id!=registry_entry.get('mcp_resource_id') else MCPDecisionStatus.ALLOWED,"unknown_resource" if context.mcp_resource_id!=registry_entry.get('mcp_resource_id') else "ok",context)
def authorize_mcp_prompt_identity_resolved(context, registry_entry): return _mk(MCPHardeningStage.PROMPT_IDENTITY_RESOLVED,MCPDecisionStatus.DENIED if context.mcp_prompt_id!=registry_entry.get('mcp_prompt_id') else MCPDecisionStatus.ALLOWED,"unknown_prompt" if context.mcp_prompt_id!=registry_entry.get('mcp_prompt_id') else "ok",context)
def authorize_mcp_tenant_scope_validated(context): return _mk(MCPHardeningStage.TENANT_SCOPE_VALIDATED,MCPDecisionStatus.DENIED if not context.tenant_id else MCPDecisionStatus.ALLOWED,"missing_tenant" if not context.tenant_id else "ok",context)
def authorize_mcp_workspace_scope_validated(context): return _mk(MCPHardeningStage.WORKSPACE_SCOPE_VALIDATED,MCPDecisionStatus.DENIED if not context.workspace_id else MCPDecisionStatus.ALLOWED,"workspace_mismatch" if not context.workspace_id else "ok",context)
def authorize_mcp_subject_permission_validated(context, registry_entry):
    required=set(registry_entry.get('required_user_permissions',()))
    present=set(context.permission_context.permission_ids)
    return _mk(MCPHardeningStage.SUBJECT_PERMISSION_VALIDATED,MCPDecisionStatus.DENIED if not required.issubset(present) else MCPDecisionStatus.ALLOWED,"missing_permission" if not required.issubset(present) else "ok",context)
def authorize_mcp_service_account_permission_validated(context, registry_entry): return _mk(MCPHardeningStage.SERVICE_ACCOUNT_PERMISSION_VALIDATED,MCPDecisionStatus.DENIED if context.permission_context.service_account and not registry_entry.get('service_account_allowed') else MCPDecisionStatus.ALLOWED,"service_account_outside_scope" if context.permission_context.service_account and not registry_entry.get('service_account_allowed') else "ok",context)
def authorize_mcp_delegated_credential_validated(context, registry_entry): return _mk(MCPHardeningStage.DELEGATED_CREDENTIAL_VALIDATED,MCPDecisionStatus.DENIED if registry_entry.get('delegated_credential_required') and not context.credential_context.delegated_scope else MCPDecisionStatus.ALLOWED,"delegated_credential_missing" if registry_entry.get('delegated_credential_required') and not context.credential_context.delegated_scope else "ok",context)
def authorize_mcp_resource_acl_validated(context, registry_entry): return _mk(MCPHardeningStage.RESOURCE_ACL_VALIDATED,MCPDecisionStatus.DENIED if context.resource_acl_policy_id!=registry_entry.get('mcp_resource_acl_policy_id') else MCPDecisionStatus.ALLOWED,"resource_acl_mismatch" if context.resource_acl_policy_id!=registry_entry.get('mcp_resource_acl_policy_id') else "ok",context)
def authorize_mcp_prompt_isolation_validated(context, registry_entry): return _mk(MCPHardeningStage.PROMPT_ISOLATION_VALIDATED,MCPDecisionStatus.DENIED if context.prompt_isolation_policy_id!=registry_entry.get('mcp_prompt_isolation_policy_id') else MCPDecisionStatus.ALLOWED,"prompt_isolation_violation" if context.prompt_isolation_policy_id!=registry_entry.get('mcp_prompt_isolation_policy_id') else "ok",context)
def authorize_mcp_request_arguments_validated(context):
    r=validate_mcp_request_arguments(context.request_arguments.values)
    return _mk(MCPHardeningStage.REQUEST_ARGUMENTS_VALIDATED,MCPDecisionStatus.DENIED if not r['allowed'] else MCPDecisionStatus.ALLOWED,"unsafe_arguments" if not r['allowed'] else "ok",context)
def authorize_mcp_confused_deputy_checked(context, registry_entry): return _mk(MCPHardeningStage.CONFUSED_DEPUTY_CHECKED,MCPDecisionStatus.FLAGGED if context.subject_id==context.mcp_client_id else MCPDecisionStatus.ALLOWED,"confused_deputy_attempt" if context.subject_id==context.mcp_client_id else "ok",context)
def authorize_mcp_egress_policy_checked(context, registry_entry): return _mk(MCPHardeningStage.EGRESS_POLICY_CHECKED,MCPDecisionStatus.FLAGGED,"unsafe_egress_target",context)
def authorize_mcp_request_signature_validated(context, registry_entry): return _mk(MCPHardeningStage.REQUEST_SIGNATURE_VALIDATED,MCPDecisionStatus.FLAGGED if registry_entry.get('request_signing_required') and not context.signature_context.signature_id else MCPDecisionStatus.ALLOWED,"missing_request_signature" if registry_entry.get('request_signing_required') and not context.signature_context.signature_id else "ok",context)
def authorize_mcp_replay_protection_checked(context, registry_entry): return _mk(MCPHardeningStage.REPLAY_PROTECTION_CHECKED,MCPDecisionStatus.FLAGGED if registry_entry.get('replay_protection_required') and not context.replay_context.nonce else MCPDecisionStatus.ALLOWED,"missing_replay_nonce" if registry_entry.get('replay_protection_required') and not context.replay_context.nonce else "ok",context)
def authorize_mcp_approval_requirement_evaluated(context, registry_entry): return validate_mcp_risk_and_approval(context, registry_entry)
def authorize_mcp_execution_authorized(context, registry_entry): return _mk(MCPHardeningStage.EXECUTION_AUTHORIZED,MCPDecisionStatus.ALLOWED,"isolated_only_no_live_execution",context)
def authorize_mcp_response_received(context, response_metadata): return _mk(MCPHardeningStage.RESPONSE_RECEIVED,MCPDecisionStatus.ALLOWED,"ok",context)
def authorize_mcp_response_safety_validated(context, response_metadata): return validate_mcp_response_safety(context, response_metadata)
def authorize_mcp_audit_written(context): write_audit_event(AuditEvent("mcp_hardening","recorded","isolation",context.request_id,{})); return _mk(MCPHardeningStage.AUDIT_WRITTEN,MCPDecisionStatus.ALLOWED,"ok",context)
def authorize_mcp_finding_recorded_if_needed(context): return _mk(MCPHardeningStage.FINDING_RECORDED_IF_NEEDED,MCPDecisionStatus.ALLOWED,"ok",context)
