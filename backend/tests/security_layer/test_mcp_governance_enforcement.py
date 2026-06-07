from __future__ import annotations

from types import SimpleNamespace

from onyx.security_layer.audit.models import AuditEvent
from onyx.security_layer.mcp_governance import MCPGovernanceDecision
from onyx.security_layer.mcp_governance.enforcement import (
    evaluate_mcp_governance_at_invocation_seam,
)
from onyx.security_layer.mcp_governance.enforcement import should_block_mcp_invocation


class RecordingAuditService:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self.events.append(event)
        return event


def _token(scopes: list[str] | None = None) -> SimpleNamespace:
    return SimpleNamespace(
        token="token-value-for-session",
        client_id="user-1",
        scopes=scopes or ["mcp:use", "mcp:search"],
        claims={"tenant_id": "tenant-a", "user_id": "user-1"},
    )


def _evaluate(*, audit: RecordingAuditService, **overrides: object):
    payload = {
        "access_token": _token(),
        "mcp_tool_name": "search_indexed_documents",
        "mcp_resource_id": "indexed_documents",
        "resource_tenant_id": "tenant-a",
        "correlation_id": "corr-mcp-enforcement-test",
        "raw_mcp_payload": {"query": "secret payload should not be exported"},
        "audit_service": audit,
    }
    payload.update(overrides)
    return evaluate_mcp_governance_at_invocation_seam(**payload)


def test_mcp_enforcement_disabled_preserves_behavior(monkeypatch) -> None:
    monkeypatch.delenv("SECURITY_MCP_GOVERNANCE_ENFORCEMENT", raising=False)
    audit = RecordingAuditService()

    result = _evaluate(audit=audit)

    assert result is None
    assert audit.events == []


def test_mcp_same_tenant_required_scope_allowed(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_MCP_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate(audit=audit)

    assert result is not None
    assert result.decision == MCPGovernanceDecision.ALLOW
    assert should_block_mcp_invocation(result) is False
    assert len(audit.events) == 1
    assert audit.events[0].details["decision"] == "allow"


def test_mcp_cross_tenant_resource_blocked_before_execution(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_MCP_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate(audit=audit, resource_tenant_id="tenant-b")

    assert result is not None
    assert result.decision == MCPGovernanceDecision.DENY
    assert should_block_mcp_invocation(result) is True


def test_mcp_missing_scope_blocked_before_execution(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_MCP_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate(audit=audit, access_token=_token(scopes=["mcp:use"]))

    assert result is not None
    assert result.decision == MCPGovernanceDecision.DENY
    assert should_block_mcp_invocation(result) is True


def test_mcp_high_risk_tool_requires_approval(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_MCP_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate(
        audit=audit,
        access_token=_token(scopes=["mcp:use"]),
        mcp_tool_name="delete_document",
        mcp_resource_id="doc-1",
        raw_mcp_payload={"document": "raw secret document"},
    )

    assert result is not None
    assert result.decision == MCPGovernanceDecision.APPROVAL_REQUIRED
    assert should_block_mcp_invocation(result) is True


def test_mcp_raw_payload_excluded_from_enforcement_evidence(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_MCP_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    _evaluate(audit=audit)

    details = audit.events[0].details
    serialized_details = str(details)
    assert "raw_mcp_payload" not in details
    assert "query" not in details
    assert "secret payload" not in serialized_details
