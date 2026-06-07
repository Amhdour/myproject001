from __future__ import annotations

from collections.abc import Mapping

from onyx.security_layer.mcp_governance.models import MCPGovernanceConfig
from onyx.security_layer.mcp_governance.models import MCPGovernanceDecision
from onyx.security_layer.mcp_governance.models import MCPGovernanceEvidence
from onyx.security_layer.mcp_governance.models import MCPGovernanceRequest
from onyx.security_layer.mcp_governance.models import MCPGovernanceResult
from onyx.security_layer.mcp_governance.models import MCPServerPolicy
from onyx.security_layer.mcp_governance.receipts import create_mcp_governance_receipt
from onyx.security_layer.mcp_governance.registry import get_mcp_server_policy
from onyx.security_layer.tracing import security_span
from onyx.security_layer.tracing import set_security_span_attributes


def _missing_required_scopes(
    *,
    requested_scopes: frozenset[str],
    required_scopes: frozenset[str],
) -> frozenset[str]:
    return required_scopes.difference(requested_scopes)


def _resolve_required_scopes(
    request: MCPGovernanceRequest,
    server_policy: MCPServerPolicy | None,
) -> frozenset[str]:
    if request.required_scopes:
        return request.required_scopes
    if server_policy is not None:
        return server_policy.default_required_scopes
    return frozenset()


def _base_decision(
    request: MCPGovernanceRequest,
    *,
    config: MCPGovernanceConfig,
    server_policy: MCPServerPolicy | None,
    required_scopes: frozenset[str],
) -> tuple[MCPGovernanceDecision, str, bool]:
    if server_policy is None:
        if config.unknown_server_monitor_mode:
            return (
                MCPGovernanceDecision.MONITOR,
                "Unknown MCP server monitored by local MCP governance configuration",
                False,
            )
        return MCPGovernanceDecision.DENY, "Unknown MCP server denied", False

    if (
        request.mcp_resource_id is not None
        and request.resource_tenant_id is not None
        and request.resource_tenant_id != request.tenant_id
    ):
        return MCPGovernanceDecision.DENY, "Cross-tenant MCP resource access denied", False

    missing_scopes = _missing_required_scopes(
        requested_scopes=request.requested_scopes,
        required_scopes=required_scopes,
    )
    if missing_scopes:
        missing_scope_list = ",".join(sorted(missing_scopes))
        return (
            MCPGovernanceDecision.DENY,
            f"Missing required MCP scope: {missing_scope_list}",
            False,
        )

    if request.mcp_tool_name in server_policy.high_risk_tools:
        return (
            MCPGovernanceDecision.APPROVAL_REQUIRED,
            "High-risk MCP tool requires approval",
            True,
        )

    if (
        request.mcp_resource_id is not None
        and request.resource_tenant_id == request.tenant_id
    ):
        return (
            MCPGovernanceDecision.ALLOW,
            "Same-tenant MCP resource access allowed with required scopes",
            False,
        )

    return MCPGovernanceDecision.ALLOW, "MCP request allowed with required scopes", False


def evaluate_mcp_governance(
    request: MCPGovernanceRequest,
    *,
    config: MCPGovernanceConfig | None = None,
    registry: Mapping[str, MCPServerPolicy] | None = None,
    previous_receipt_hash: str | None = None,
) -> MCPGovernanceResult:
    resolved_config = config or MCPGovernanceConfig()
    server_policy = get_mcp_server_policy(request.mcp_server_id, registry)
    required_scopes = _resolve_required_scopes(request, server_policy)
    decision, reason, approval_required = _base_decision(
        request,
        config=resolved_config,
        server_policy=server_policy,
        required_scopes=required_scopes,
    )

    if resolved_config.shadow_mode and decision == MCPGovernanceDecision.DENY:
        decision = MCPGovernanceDecision.SHADOW_DENY
        reason = f"Shadow mode would block: {reason}"

    receipt = create_mcp_governance_receipt(
        correlation_id=request.correlation_id,
        user_id=request.user_id,
        tenant_id=request.tenant_id,
        mcp_server_id=request.mcp_server_id,
        mcp_tool_name=request.mcp_tool_name,
        mcp_resource_id=request.mcp_resource_id,
        decision=decision,
        reason=reason,
        previous_receipt_hash=previous_receipt_hash,
    )
    evidence = MCPGovernanceEvidence(
        receipt_id=receipt.receipt_id,
        user_id=request.user_id,
        tenant_id=request.tenant_id,
        mcp_server_id=request.mcp_server_id,
        mcp_tool_name=request.mcp_tool_name,
        mcp_resource_id=request.mcp_resource_id,
        decision=decision,
        reason=reason,
        receipt_hash=receipt.receipt_hash,
        correlation_id=request.correlation_id,
    )

    with security_span(
        "security.mcp_governance.decision",
        {
            "security.correlation_id": request.correlation_id,
            "security.mcp_server_id": request.mcp_server_id,
            "security.mcp_tool_name": request.mcp_tool_name,
            "security.mcp_resource_id": request.mcp_resource_id,
            "security.decision": decision.value,
        },
    ) as span:
        set_security_span_attributes(
            span,
            {
                "security.reason": reason,
                "security.approval_required": approval_required,
                "security.receipt_hash": receipt.receipt_hash,
            },
        )

    return MCPGovernanceResult(
        correlation_id=request.correlation_id,
        user_id=request.user_id,
        tenant_id=request.tenant_id,
        mcp_server_id=request.mcp_server_id,
        mcp_tool_name=request.mcp_tool_name,
        mcp_resource_id=request.mcp_resource_id,
        resource_tenant_id=request.resource_tenant_id,
        requested_scopes=request.requested_scopes,
        required_scopes=required_scopes,
        decision=decision,
        reason=reason,
        approval_required=approval_required,
        receipt=receipt,
        evidence=evidence,
    )
