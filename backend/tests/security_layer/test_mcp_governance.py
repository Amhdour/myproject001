from __future__ import annotations

import onyx.security_layer.mcp_governance.decision_mapper as decision_mapper
from onyx.security_layer.langfuse_evidence import safe_mcp_governance_langfuse_payload
from onyx.security_layer.mcp_governance import evaluate_mcp_governance
from onyx.security_layer.mcp_governance import MCPGovernanceConfig
from onyx.security_layer.mcp_governance import MCPGovernanceDecision
from onyx.security_layer.mcp_governance import MCPGovernanceRequest


class RecordingSpan:
    def __init__(self) -> None:
        self.attributes: dict[str, str | bool | int | float] = {}

    def set_attribute(self, key: str, value: str | bool | int | float) -> None:
        self.attributes[key] = value


class RecordingSecuritySpan:
    def __init__(self) -> None:
        self.name: str | None = None
        self.attributes: dict[str, object | None] = {}
        self.span = RecordingSpan()

    def __call__(self, name: str, attributes: dict[str, object | None]):
        self.name = name
        self.attributes = attributes
        return self

    def __enter__(self) -> RecordingSpan:
        return self.span

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None


def _request(**overrides: object) -> MCPGovernanceRequest:
    payload = {
        "correlation_id": "corr-mcp-governance-test",
        "user_id": "user-1",
        "tenant_id": "tenant-a",
        "mcp_server_id": "enterprise-search",
        "mcp_tool_name": "read_document",
        "mcp_resource_id": "doc-1",
        "resource_tenant_id": "tenant-a",
        "requested_scopes": frozenset({"mcp:use", "mcp:read_document"}),
        "required_scopes": frozenset({"mcp:use", "mcp:read_document"}),
    }
    payload.update(overrides)
    return MCPGovernanceRequest(**payload)


def test_same_tenant_required_scope_allowed(monkeypatch) -> None:
    recording_security_span = RecordingSecuritySpan()
    monkeypatch.setattr(decision_mapper, "security_span", recording_security_span)

    result = evaluate_mcp_governance(_request())

    assert result.decision == MCPGovernanceDecision.ALLOW
    assert result.approval_required is False
    assert result.reason == "Same-tenant MCP resource access allowed with required scopes"
    assert recording_security_span.name == "security.mcp_governance.decision"
    assert recording_security_span.attributes["security.decision"] == "allow"
    assert recording_security_span.span.attributes["security.receipt_hash"] == (
        result.receipt.receipt_hash
    )


def test_cross_tenant_resource_denied() -> None:
    result = evaluate_mcp_governance(
        _request(resource_tenant_id="tenant-b", mcp_resource_id="doc-cross-tenant")
    )

    assert result.decision == MCPGovernanceDecision.DENY
    assert result.reason == "Cross-tenant MCP resource access denied"


def test_missing_scope_denied() -> None:
    result = evaluate_mcp_governance(
        _request(requested_scopes=frozenset({"mcp:use"}))
    )

    assert result.decision == MCPGovernanceDecision.DENY
    assert result.reason == "Missing required MCP scope: mcp:read_document"


def test_high_risk_mcp_tool_requires_approval() -> None:
    result = evaluate_mcp_governance(
        _request(
            mcp_tool_name="delete_document",
            requested_scopes=frozenset({"mcp:use", "mcp:delete_document"}),
            required_scopes=frozenset({"mcp:use", "mcp:delete_document"}),
        )
    )

    assert result.decision == MCPGovernanceDecision.APPROVAL_REQUIRED
    assert result.approval_required is True
    assert result.reason == "High-risk MCP tool requires approval"


def test_unknown_server_deny_or_monitor_behavior() -> None:
    denied = evaluate_mcp_governance(_request(mcp_server_id="unknown-server"))
    monitored = evaluate_mcp_governance(
        _request(mcp_server_id="unknown-server"),
        config=MCPGovernanceConfig(unknown_server_monitor_mode=True),
    )

    assert denied.decision == MCPGovernanceDecision.DENY
    assert denied.reason == "Unknown MCP server denied"
    assert monitored.decision == MCPGovernanceDecision.MONITOR
    assert monitored.reason == (
        "Unknown MCP server monitored by local MCP governance configuration"
    )


def test_receipt_hash_generated() -> None:
    result = evaluate_mcp_governance(_request())

    assert result.receipt.receipt_id
    assert result.receipt.receipt_hash
    assert result.receipt.receipt_hash != "pending"
    assert len(result.receipt.receipt_hash) == 64
    assert result.evidence.receipt_id == result.receipt.receipt_id
    assert result.evidence.receipt_hash == result.receipt.receipt_hash
    assert result.evidence.user_id == result.receipt.user_id
    assert result.evidence.tenant_id == result.receipt.tenant_id


def test_raw_payload_excluded_from_evidence() -> None:
    result = evaluate_mcp_governance(
        _request(
            raw_mcp_payload={
                "prompt": "summarize document content",
                "token": "secret-token-value",
                "tool_output": "confidential tool output",
            }
        )
    )
    payload = safe_mcp_governance_langfuse_payload(
        {
            **result.evidence.model_dump(mode="json"),
            "raw_mcp_payload": "secret-token-value",
            "token": "secret-token-value",
            "tool_output": "confidential tool output",
            "prompt": "summarize document content",
            "document_content": "private document content",
        }
    )
    serialized_payload = str(payload)

    assert payload == {
        "correlation_id": result.evidence.correlation_id,
        "decision": result.evidence.decision.value,
        "mcp_resource_id": result.evidence.mcp_resource_id,
        "mcp_server_id": result.evidence.mcp_server_id,
        "mcp_tool_name": result.evidence.mcp_tool_name,
        "reason": result.evidence.reason,
        "receipt_hash": result.evidence.receipt_hash,
    }
    assert "raw_mcp_payload" not in payload
    assert "token" not in payload
    assert "tool_output" not in payload
    assert "prompt" not in payload
    assert "document_content" not in payload
    assert "secret-token-value" not in serialized_payload
    assert "confidential tool output" not in serialized_payload
    assert "private document content" not in serialized_payload
