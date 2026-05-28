# Step 22B: MCP hardening remains monitor-only (no enforcement side effects).
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class MCPHardeningStage(str, Enum):
    REGISTRY_LOADED = "registry_loaded"
    REGISTRY_VALIDATED = "registry_validated"
    REQUEST_RECEIVED = "request_received"
    CONTEXT_VALIDATED = "context_validated"
    SERVER_IDENTITY_RESOLVED = "server_identity_resolved"
    CLIENT_IDENTITY_RESOLVED = "client_identity_resolved"
    TOOL_IDENTITY_RESOLVED = "tool_identity_resolved"
    RESOURCE_IDENTITY_RESOLVED = "resource_identity_resolved"
    PROMPT_IDENTITY_RESOLVED = "prompt_identity_resolved"
    TENANT_SCOPE_VALIDATED = "tenant_scope_validated"
    WORKSPACE_SCOPE_VALIDATED = "workspace_scope_validated"
    SUBJECT_PERMISSION_VALIDATED = "subject_permission_validated"
    SERVICE_ACCOUNT_PERMISSION_VALIDATED = "service_account_permission_validated"
    DELEGATED_CREDENTIAL_VALIDATED = "delegated_credential_validated"
    RESOURCE_ACL_VALIDATED = "resource_acl_validated"
    PROMPT_ISOLATION_VALIDATED = "prompt_isolation_validated"
    REQUEST_ARGUMENTS_VALIDATED = "request_arguments_validated"
    CONFUSED_DEPUTY_CHECKED = "confused_deputy_checked"
    EGRESS_POLICY_CHECKED = "egress_policy_checked"
    REQUEST_SIGNATURE_VALIDATED = "request_signature_validated"
    REPLAY_PROTECTION_CHECKED = "replay_protection_checked"
    APPROVAL_REQUIREMENT_EVALUATED = "approval_requirement_evaluated"
    EXECUTION_AUTHORIZED = "execution_authorized"
    RESPONSE_RECEIVED = "response_received"
    RESPONSE_SAFETY_VALIDATED = "response_safety_validated"
    AUDIT_WRITTEN = "audit_written"
    FINDING_RECORDED_IF_NEEDED = "finding_recorded_if_needed"

class MCPDecisionStatus(str, Enum): ALLOWED="allowed"; DENIED="denied"; FLAGGED="flagged"; APPROVAL_REQUIRED="approval_required"
class MCPOperationType(str, Enum): TOOL="tool"; RESOURCE="resource"; PROMPT="prompt"
class MCPServerStatus(str, Enum): ACTIVE="active"; DISABLED="disabled"
class MCPTrustTier(str, Enum): LOW="low"; MEDIUM="medium"; HIGH="high"
class MCPRiskTier(str, Enum): LOW="low"; MEDIUM="medium"; HIGH="high"; CRITICAL="critical"
class MCPDefaultEffect(str, Enum): DENY="deny"; ALLOW="allow"
class MCPResourceType(str, Enum): DOCUMENT="document"; API="api"; DATASET="dataset"
class MCPCredentialType(str, Enum): USER="user"; SERVICE="service"; DELEGATED="delegated"
class MCPEgressDecision(str, Enum): ALLOW="allow"; DENY="deny"; FLAG="flag"

@dataclass(frozen=True)
class MCPRegistryEntry: metadata: dict[str, object]
@dataclass(frozen=True)
class MCPRequestArguments: values: dict[str, object] = field(default_factory=dict)
@dataclass(frozen=True)
class MCPServerIdentity: mcp_server_id:str
@dataclass(frozen=True)
class MCPClientIdentity: mcp_client_id:str
@dataclass(frozen=True)
class MCPToolIdentity: mcp_tool_id:str
@dataclass(frozen=True)
class MCPResourceIdentity: mcp_resource_id:str
@dataclass(frozen=True)
class MCPPromptIdentity: mcp_prompt_id:str

@dataclass(frozen=True)
class MCPCredentialContext:
    credential_id:str|None=None; credential_type:MCPCredentialType=MCPCredentialType.USER; delegated_scope:str|None=None
    tenant_id:str|None=None; subject_id:str|None=None; issued_at:int|None=None; expires_at:int|None=None; placeholder_only:bool=True

@dataclass(frozen=True)
class MCPPermissionContext:
    subject_id:str|None=None; group_ids:tuple[str,...]=(); role_ids:tuple[str,...]=(); permission_ids:tuple[str,...]=(); service_account:bool=False

@dataclass(frozen=True)
class MCPEgressPolicy:
    egress_policy_id:str; allowed_domains:tuple[str,...]=(); denied_domains:tuple[str,...]=(); block_internal_network:bool=True; block_metadata_service:bool=True

@dataclass(frozen=True)
class MCPReplayContext: nonce:str|None=None; nonce_issued_at:int|None=None; max_nonce_age_seconds:int=300
@dataclass(frozen=True)
class MCPSignatureContext: signature_id:str|None=None; signature_algorithm:str|None=None; signed_at:int|None=None; max_signature_age_seconds:int=300
@dataclass(frozen=True)
class MCPApprovalRequirement: approval_required:bool=False; approval_risk_level:MCPRiskTier=MCPRiskTier.LOW; approved:bool=False
@dataclass(frozen=True)
class MCPResponseMetadata: response_safety_policy_id:str|None=None; contains_secret_marker:bool=False; contains_prompt_injection_marker:bool=False

@dataclass(frozen=True)
class MCPHardeningContext:
    request_id:str; mcp_server_id:str|None=None; mcp_client_id:str|None=None; mcp_tool_id:str|None=None; mcp_resource_id:str|None=None; mcp_prompt_id:str|None=None
    tenant_id:str|None=None; workspace_id:str|None=None; subject_id:str|None=None; group_ids:tuple[str,...]=(); role_ids:tuple[str,...]=(); operation_type:MCPOperationType=MCPOperationType.TOOL
    request_arguments:MCPRequestArguments=field(default_factory=MCPRequestArguments); credential_context:MCPCredentialContext=field(default_factory=MCPCredentialContext)
    permission_context:MCPPermissionContext=field(default_factory=MCPPermissionContext); egress_policy:MCPEgressPolicy|None=None; replay_context:MCPReplayContext=field(default_factory=MCPReplayContext)
    signature_context:MCPSignatureContext=field(default_factory=MCPSignatureContext); approval_requirement:MCPApprovalRequirement=field(default_factory=MCPApprovalRequirement)
    resource_acl_policy_id:str|None=None; prompt_isolation_policy_id:str|None=None; response_safety_policy_id:str|None=None; metadata_schema_version:str="1.0"

@dataclass(frozen=True)
class MCPFinding: reason_code:str; message:str; stage:MCPHardeningStage
@dataclass(frozen=True)
class MCPHardeningDecision:
    stage:MCPHardeningStage; status:MCPDecisionStatus; reason_code:str; findings:tuple[MCPFinding,...]=(); safe_details:dict[str, object]=field(default_factory=dict)
