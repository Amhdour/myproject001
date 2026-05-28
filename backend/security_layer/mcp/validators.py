# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from __future__ import annotations
from .models import MCPDecisionStatus, MCPFinding, MCPHardeningContext, MCPHardeningDecision, MCPHardeningStage, MCPResponseMetadata, MCPRiskTier

def _deny(stage, code): return MCPHardeningDecision(stage=stage,status=MCPDecisionStatus.DENIED,reason_code=code)
def _flag(stage, code): return MCPHardeningDecision(stage=stage,status=MCPDecisionStatus.FLAGGED,reason_code=code,findings=(MCPFinding(code,code,stage),))

def validate_mcp_tenant_context(context): return bool(context.tenant_id)
def validate_mcp_subject_context(context): return bool(context.subject_id)
def validate_mcp_workspace_scope(context): return bool(context.workspace_id)
def validate_mcp_hardening_context(context):
    if not validate_mcp_tenant_context(context): return _deny(MCPHardeningStage.CONTEXT_VALIDATED,"missing_tenant")
    if not validate_mcp_subject_context(context): return _deny(MCPHardeningStage.CONTEXT_VALIDATED,"missing_subject")
    return MCPHardeningDecision(MCPHardeningStage.CONTEXT_VALIDATED,MCPDecisionStatus.ALLOWED,"ok")
def validate_mcp_server_identity(context, registry_entry): return context.mcp_server_id==registry_entry.get("mcp_server_id")
def validate_mcp_tool_identity(context, registry_entry): return context.mcp_tool_id==registry_entry.get("mcp_tool_id")
def validate_mcp_resource_identity(context, registry_entry): return context.mcp_resource_id==registry_entry.get("mcp_resource_id")
def validate_mcp_prompt_identity(context, registry_entry): return context.mcp_prompt_id==registry_entry.get("mcp_prompt_id")
def validate_mcp_permission_context(context, registry_entry): return all(p in context.permission_context.permission_ids for p in registry_entry.get("required_user_permissions",()))
def validate_mcp_service_account_permission(context, registry_entry): return not context.permission_context.service_account or registry_entry.get("service_account_allowed",False)
def validate_mcp_delegated_credential(context, registry_entry): return (not registry_entry.get("delegated_credential_required")) or bool(context.credential_context.delegated_scope)
def validate_mcp_resource_acl(context, registry_entry): return context.resource_acl_policy_id==registry_entry.get("mcp_resource_acl_policy_id")
def validate_mcp_prompt_isolation(context, registry_entry): return context.prompt_isolation_policy_id==registry_entry.get("mcp_prompt_isolation_policy_id")
def validate_mcp_confused_deputy(context, registry_entry): return context.subject_id!=context.mcp_client_id
def validate_mcp_risk_and_approval(context, registry_entry):
    if registry_entry.get("approval_required") and registry_entry.get("approval_risk_level") in {MCPRiskTier.HIGH.value,MCPRiskTier.CRITICAL.value} and not context.approval_requirement.approved:
        return MCPHardeningDecision(MCPHardeningStage.APPROVAL_REQUIREMENT_EVALUATED,MCPDecisionStatus.APPROVAL_REQUIRED,"approval_required")
    return MCPHardeningDecision(MCPHardeningStage.APPROVAL_REQUIREMENT_EVALUATED,MCPDecisionStatus.ALLOWED,"ok")
def validate_mcp_response_safety(context, response_metadata:MCPResponseMetadata):
    if response_metadata.contains_secret_marker: return _flag(MCPHardeningStage.RESPONSE_SAFETY_VALIDATED,"secret_response_marker")
    if response_metadata.contains_prompt_injection_marker: return _flag(MCPHardeningStage.RESPONSE_SAFETY_VALIDATED,"prompt_injection_response_marker")
    return MCPHardeningDecision(MCPHardeningStage.RESPONSE_SAFETY_VALIDATED,MCPDecisionStatus.ALLOWED,"ok")
def build_mcp_decision(stage,status,reason): return MCPHardeningDecision(stage=stage,status=status,reason_code=reason)
