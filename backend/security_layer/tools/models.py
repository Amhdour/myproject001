from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ToolAuthorizationStage(str, Enum):
    TOOL_REGISTRY_LOADED = "tool_registry_loaded"
    TOOL_REGISTRY_VALIDATED = "tool_registry_validated"
    TOOL_CALL_REQUESTED = "tool_call_requested"
    TOOL_CONTEXT_VALIDATED = "tool_context_validated"
    TOOL_IDENTITY_RESOLVED = "tool_identity_resolved"
    CALLER_IDENTITY_RESOLVED = "caller_identity_resolved"
    TENANT_SCOPE_VALIDATED = "tenant_scope_validated"
    WORKSPACE_SCOPE_VALIDATED = "workspace_scope_validated"
    SUBJECT_PERMISSION_VALIDATED = "subject_permission_validated"
    SERVICE_ACCOUNT_PERMISSION_VALIDATED = "service_account_permission_validated"
    DELEGATED_CREDENTIAL_VALIDATED = "delegated_credential_validated"
    TOOL_RISK_CLASSIFIED = "tool_risk_classified"
    TOOL_ARGUMENT_SCHEMA_VALIDATED = "tool_argument_schema_validated"
    TOOL_ARGUMENT_CONTENT_VALIDATED = "tool_argument_content_validated"
    APPROVAL_REQUIREMENT_EVALUATED = "approval_requirement_evaluated"
    TOOL_EXECUTION_AUTHORIZED = "tool_execution_authorized"
    TOOL_RESULT_RECEIVED = "tool_result_received"
    TOOL_RESULT_SAFETY_VALIDATED = "tool_result_safety_validated"
    TOOL_AUDIT_WRITTEN = "tool_audit_written"
    TOOL_FINDING_RECORDED_IF_NEEDED = "tool_finding_recorded_if_needed"


class ToolDecisionStatus(str, Enum):
    ALLOWED = "allowed"
    DENIED = "denied"
    APPROVAL_REQUIRED = "approval_required"
    FLAGGED = "flagged"


class ToolOperationType(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"


class ToolCategory(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    ADMIN = "admin"


class ToolRiskTier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ToolStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"


class ToolDefaultEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


@dataclass(frozen=True)
class ToolRegistryEntry:
    tool_id: str
    tool_name: str
    tool_version: str
    tool_owner: str
    tool_category: ToolCategory
    tool_risk_tier: ToolRiskTier
    tool_status: ToolStatus
    allowed_tenant_scope: list[str]
    allowed_workspace_scope: list[str]
    required_user_permissions: list[str]
    required_group_permissions: list[str]
    required_role_permissions: list[str]
    service_account_allowed: bool
    delegated_credential_required: bool
    delegated_credential_scope: str
    approval_required: bool
    approval_risk_level: str
    argument_schema_id: str
    result_safety_policy_id: str
    audit_required: bool
    finding_required_on_violation: bool
    metric_required: bool
    default_effect: ToolDefaultEffect
    metadata_schema_version: str
    tool_description_placeholder: str


@dataclass(frozen=True)
class ToolArgumentSchema:
    schema_id: str
    metadata_schema_version: str
    argument_types: dict[str, str] = field(default_factory=dict)
    max_lengths: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ToolArgument:
    name: str
    value: str


@dataclass(frozen=True)
class ToolCallerContext:
    caller_id: str
    caller_type: str


@dataclass(frozen=True)
class ToolTenantScope:
    tenant_id: str


@dataclass(frozen=True)
class ToolWorkspaceScope:
    workspace_id: str


@dataclass(frozen=True)
class ToolPermissionContext:
    subject_id: str
    user_permissions: list[str] = field(default_factory=list)
    group_permissions: list[str] = field(default_factory=list)
    role_permissions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ToolDelegatedCredential:
    credential_id: str
    tenant_id: str
    scope: str
    expires_at: datetime


@dataclass(frozen=True)
class ToolApprovalRequirement:
    required: bool
    approved: bool
    risk_level: str


@dataclass(frozen=True)
class ToolResultMetadata:
    result_safety_policy_id: str
    metadata_schema_version: str
    flagged_unsafe: bool = False
    flagged_secret_leakage: bool = False


@dataclass(frozen=True)
class ToolAuthorizationContext:
    request_id: str
    tool_id: str
    operation: ToolOperationType
    caller: ToolCallerContext
    tenant_scope: ToolTenantScope | None
    workspace_scope: ToolWorkspaceScope | None
    permission_context: ToolPermissionContext | None
    delegated_credential: ToolDelegatedCredential | None = None
    approval_requirement: ToolApprovalRequirement | None = None
    argument_schema: ToolArgumentSchema | None = None
    arguments: list[ToolArgument] = field(default_factory=list)


@dataclass(frozen=True)
class ToolAuthorizationDecision:
    status: ToolDecisionStatus
    stage: ToolAuthorizationStage
    reason_code: str
    message: str
    safe_denial_category: str | None = None


@dataclass(frozen=True)
class ToolFinding:
    finding_code: str
    request_id: str
    stage: ToolAuthorizationStage
