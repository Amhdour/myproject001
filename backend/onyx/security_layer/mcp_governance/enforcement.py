from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any
from typing import Protocol

from onyx.security_layer.audit.models import AuditEvent
from onyx.security_layer.langfuse_evidence import emit_mcp_governance_langfuse_evidence
from onyx.security_layer.langfuse_evidence import safe_mcp_governance_langfuse_payload
from onyx.security_layer.mcp_governance.decision_mapper import evaluate_mcp_governance
from onyx.security_layer.mcp_governance.models import MCPGovernanceDecision
from onyx.security_layer.mcp_governance.models import MCPGovernanceRequest
from onyx.security_layer.mcp_governance.models import MCPGovernanceResult

MCP_GOVERNANCE_ENFORCEMENT_ENV = "SECURITY_MCP_GOVERNANCE_ENFORCEMENT"
MCP_SERVER_ID = "enterprise-search"

_SELECTED_MCP_TOOL_NAMES = frozenset(
    {
        "search_indexed_documents",
        "search_web",
        "open_urls",
        "read_document",
        "delete_document",
        "export_documents",
        "file_read",
        "file_write",
        "code_execute",
    }
)
_BLOCKING_DECISIONS = {
    MCPGovernanceDecision.DENY,
    MCPGovernanceDecision.APPROVAL_REQUIRED,
}

_ACTION_SCOPE_MAP: dict[str, str] = {
    "search_indexed_documents": "mcp:search",
    "search_web": "mcp:web_search",
    "open_urls": "mcp:open_url",
    "read_document": "mcp:read_document",
    "file_read": "mcp:file_read",
    "file_write": "mcp:file_write",
    "code_execute": "mcp:code_execute",
    "admin": "mcp:admin",
}


def _required_scope_for_mcp_tool(mcp_tool_name: str) -> str:
    return _ACTION_SCOPE_MAP.get(mcp_tool_name, "mcp:use")


class MCPAccessToken(Protocol):
    token: str
    client_id: str | None
    scopes: list[str] | None
    claims: Mapping[str, Any]


class MCPGovernanceAuditRecorder(Protocol):
    def record(self, event: AuditEvent) -> AuditEvent:
        pass


def is_mcp_governance_enforcement_enabled() -> bool:
    return os.getenv(MCP_GOVERNANCE_ENFORCEMENT_ENV, "false").lower() == "true"


def is_selected_mcp_tool_for_governance(mcp_tool_name: str) -> bool:
    return mcp_tool_name.lower().strip() in _SELECTED_MCP_TOOL_NAMES


def _token_extra(access_token: MCPAccessToken) -> Mapping[str, Any]:
    extra = getattr(access_token, "extra", None)
    if isinstance(extra, Mapping):
        return extra
    claims = getattr(access_token, "claims", None)
    if isinstance(claims, Mapping):
        return claims
    return {}


def _access_token_user_id(access_token: MCPAccessToken) -> str:
    extra = _token_extra(access_token)
    for key in ("user_id", "sub", "email"):
        value = extra.get(key)
        if value:
            return str(value)
    return access_token.client_id or "missing:user"


def _access_token_tenant_id(access_token: MCPAccessToken) -> str:
    direct_tenant_id = getattr(access_token, "tenant_id", None)
    if direct_tenant_id:
        return str(direct_tenant_id)
    extra = _token_extra(access_token)
    tenant_id = extra.get("tenant_id")
    if tenant_id:
        return str(tenant_id)
    return "missing:tenant"


def build_mcp_governance_request(
    *,
    access_token: MCPAccessToken,
    mcp_tool_name: str,
    correlation_id: str,
    raw_mcp_payload: Mapping[str, Any],
    mcp_server_id: str = MCP_SERVER_ID,
    mcp_resource_id: str | None = None,
    resource_tenant_id: str | None = None,
) -> MCPGovernanceRequest:
    tenant_id = _access_token_tenant_id(access_token)
    scope = _required_scope_for_mcp_tool(mcp_tool_name)
    return MCPGovernanceRequest(
        user_id=_access_token_user_id(access_token),
        tenant_id=tenant_id,
        mcp_server_id=mcp_server_id,
        mcp_tool_name=mcp_tool_name,
        mcp_resource_id=mcp_resource_id,
        resource_tenant_id=resource_tenant_id,
        requested_scopes=frozenset(access_token.scopes or []),
        required_scopes=frozenset({"mcp:use", scope}),
        correlation_id=correlation_id,
        raw_mcp_payload=dict(raw_mcp_payload),
    )


def record_mcp_governance_evidence(
    *,
    result: MCPGovernanceResult,
    audit_service: MCPGovernanceAuditRecorder,
    session_id: str,
) -> dict[str, str | bool | int | float]:
    safe_evidence = safe_mcp_governance_langfuse_payload(
        result.evidence.model_dump(mode="json")
    )
    audit_service.record(
        AuditEvent(
            event_type="mcp_governance_decision",
            tenant_id=result.tenant_id,
            user_id=result.user_id,
            session_id=session_id,
            decision_id=result.receipt.receipt_hash,
            resource_type="mcp",
            resource_id=result.mcp_resource_id or result.mcp_tool_name or result.mcp_server_id,
            action=result.mcp_tool_name or "execute",
            risk_level="high" if result.approval_required else "medium",
            details={
                **safe_evidence,
                "governance_enforcement_enabled": True,
            },
        )
    )
    emit_mcp_governance_langfuse_evidence(safe_evidence)
    return safe_evidence


def evaluate_mcp_governance_at_invocation_seam(
    *,
    access_token: MCPAccessToken,
    mcp_tool_name: str,
    correlation_id: str,
    raw_mcp_payload: Mapping[str, Any],
    audit_service: MCPGovernanceAuditRecorder,
    session_id: str | None = None,
    mcp_server_id: str = MCP_SERVER_ID,
    mcp_resource_id: str | None = None,
    resource_tenant_id: str | None = None,
) -> MCPGovernanceResult | None:
    """Near-real MCP tool seam for env-gated governance before tool execution.

    FastMCP registers individual Python callables rather than exposing a single
    public pre-dispatch hook here. This wrapper is intentionally narrow and is
    called at the start of selected MCP tool/resource handlers; future FastMCP
    middleware can move this same call to a central dispatcher without changing
    policy behavior.
    """

    if not is_mcp_governance_enforcement_enabled():
        return None
    if not is_selected_mcp_tool_for_governance(mcp_tool_name):
        return None

    request = build_mcp_governance_request(
        access_token=access_token,
        mcp_server_id=mcp_server_id,
        mcp_tool_name=mcp_tool_name,
        mcp_resource_id=mcp_resource_id,
        resource_tenant_id=resource_tenant_id,
        correlation_id=correlation_id,
        raw_mcp_payload=raw_mcp_payload,
    )
    result = evaluate_mcp_governance(request)
    record_mcp_governance_evidence(
        result=result,
        audit_service=audit_service,
        session_id=session_id or access_token.token[:12],
    )
    return result


def should_block_mcp_invocation(result: MCPGovernanceResult | None) -> bool:
    return result is not None and result.decision in _BLOCKING_DECISIONS
