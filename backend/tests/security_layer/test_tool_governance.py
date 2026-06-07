from __future__ import annotations

import pytest

from onyx.security_layer.audit.models import AuditEvent
from onyx.security_layer.langfuse_evidence import safe_tool_governance_langfuse_payload
from onyx.security_layer.tool_governance import evaluate_tool_governance
from onyx.security_layer.tool_governance import LocalApprovalStore
from onyx.security_layer.tool_governance import SelfApprovalError
from onyx.security_layer.tool_governance import ToolActionRequest
from onyx.security_layer.tool_governance import ToolGovernanceConfig
from onyx.security_layer.tool_governance import ToolGovernanceDecision
from onyx.security_layer.tool_governance import ToolRiskLevel
from onyx.security_layer.tool_governance.enforcement import (
    evaluate_tool_governance_at_execution_seam,
)


def _request(tool_name: str, **overrides: object) -> ToolActionRequest:
    payload = {
        "correlation_id": "corr-tool-governance-test",
        "user_id": "user-requester",
        "tenant_id": "tenant-a",
        "tool_name": tool_name,
        "action": "execute",
    }
    payload.update(overrides)
    return ToolActionRequest(**payload)


def test_low_risk_tool_allowed() -> None:
    result = evaluate_tool_governance(_request("search"))

    assert result.risk_level == ToolRiskLevel.LOW
    assert result.decision == ToolGovernanceDecision.ALLOW
    assert result.approval_required is False


def test_high_risk_side_effecting_tool_requires_approval() -> None:
    store = LocalApprovalStore()

    result = evaluate_tool_governance(_request("send_email"), approval_store=store)

    assert result.risk_level == ToolRiskLevel.HIGH
    assert result.decision == ToolGovernanceDecision.APPROVAL_REQUIRED
    assert result.approval_required is True
    assert result.approval_id is not None


def test_critical_action_denied_or_approval_required_based_config() -> None:
    denied = evaluate_tool_governance(_request("delete_document"))
    approval_required = evaluate_tool_governance(
        _request("delete_document"),
        config=ToolGovernanceConfig(critical_side_effect_requires_approval=True),
    )

    assert denied.risk_level == ToolRiskLevel.CRITICAL
    assert denied.decision == ToolGovernanceDecision.DENY
    assert denied.approval_required is False
    assert approval_required.risk_level == ToolRiskLevel.CRITICAL
    assert approval_required.decision == ToolGovernanceDecision.APPROVAL_REQUIRED
    assert approval_required.approval_required is True


def test_self_approval_blocked() -> None:
    store = LocalApprovalStore()
    result = evaluate_tool_governance(_request("send_email"), approval_store=store)

    assert result.approval_id is not None
    with pytest.raises(SelfApprovalError):
        store.approve(result.approval_id, approved_by_user_id="user-requester")


def test_approval_replay_blocked() -> None:
    store = LocalApprovalStore()
    pending = evaluate_tool_governance(_request("send_email"), approval_store=store)
    assert pending.approval_id is not None
    store.approve(pending.approval_id, approved_by_user_id="user-approver")

    approved_request = _request("send_email", approval_id=pending.approval_id)
    first_use = evaluate_tool_governance(approved_request, approval_store=store)
    replay = evaluate_tool_governance(approved_request, approval_store=store)

    assert first_use.decision == ToolGovernanceDecision.ALLOW
    assert replay.decision == ToolGovernanceDecision.DENY
    assert "Approval replay protection blocked action" in replay.reason


def test_receipt_hash_generated() -> None:
    result = evaluate_tool_governance(_request("read_document"))

    assert result.receipt.receipt_hash
    assert result.receipt.receipt_hash != "pending"
    assert len(result.receipt.receipt_hash) == 64
    assert result.evidence.receipt_hash == result.receipt.receipt_hash


def test_evidence_excludes_raw_payload() -> None:
    result = evaluate_tool_governance(
        _request(
            "send_email",
            raw_tool_payload={
                "to": "recipient@example.com",
                "body": "document content and api_key=supersecretvalue",
            },
        )
    )
    payload = safe_tool_governance_langfuse_payload(
        {
            **result.evidence.model_dump(mode="json"),
            "raw_tool_payload": "recipient@example.com api_key=supersecretvalue",
            "document_content": "raw document content",
            "secret": "secret-value",
        }
    )
    serialized = str(payload)

    assert payload == result.evidence.model_dump(mode="json")
    assert "raw_tool_payload" not in payload
    assert "document_content" not in payload
    assert "secret" not in payload
    assert "recipient@example.com" not in serialized
    assert "supersecretvalue" not in serialized
    assert "raw document content" not in serialized



class RecordingAuditService:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self.events.append(event)
        return event


def _evaluate_at_execution_seam(
    *,
    tool_name: str,
    audit: RecordingAuditService,
):
    return evaluate_tool_governance_at_execution_seam(
        tool_name=tool_name,
        tool_args={
            "recipient": "external@example.com",
            "body": "private data api_key=should-not-export",
        },
        user_id="user-1",
        tenant_id="tenant-1",
        session_id="session-1",
        correlation_id="corr-execution-seam-test",
        audit_service=audit,
    )


def test_execution_seam_governance_disabled_preserves_behavior(monkeypatch) -> None:
    monkeypatch.delenv("SECURITY_TOOL_GOVERNANCE_ENFORCEMENT", raising=False)
    audit = RecordingAuditService()

    result = _evaluate_at_execution_seam(tool_name="send_email", audit=audit)

    assert result is None
    assert not any(event.event_type == "tool_governance_decision" for event in audit.events)


def test_execution_seam_low_risk_tool_allowed(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_TOOL_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate_at_execution_seam(tool_name="search", audit=audit)

    assert result is not None
    assert result.decision == ToolGovernanceDecision.ALLOW
    governance_events = [
        event for event in audit.events if event.event_type == "tool_governance_decision"
    ]
    assert len(governance_events) == 1
    assert governance_events[0].details["decision"] == "allow"
    assert governance_events[0].details["risk_level"] == "low"


def test_execution_seam_high_risk_side_effect_tool_blocked_pending_approval(
    monkeypatch,
) -> None:
    monkeypatch.setenv("SECURITY_TOOL_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate_at_execution_seam(tool_name="send_email", audit=audit)

    assert result is not None
    assert result.decision == ToolGovernanceDecision.APPROVAL_REQUIRED
    governance_event = next(
        event for event in audit.events if event.event_type == "tool_governance_decision"
    )
    assert governance_event.details["decision"] == "approval_required"
    assert governance_event.details["approval_required"] is True
    assert governance_event.details["receipt_hash"]


def test_execution_seam_critical_action_blocked_by_config(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_TOOL_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    result = _evaluate_at_execution_seam(tool_name="delete_document", audit=audit)

    assert result is not None
    assert result.decision in {
        ToolGovernanceDecision.DENY,
        ToolGovernanceDecision.APPROVAL_REQUIRED,
    }
    governance_event = next(
        event for event in audit.events if event.event_type == "tool_governance_decision"
    )
    assert governance_event.details["decision"] in {"deny", "approval_required"}
    assert governance_event.details["risk_level"] == "critical"


def test_execution_seam_evidence_excludes_raw_payload(monkeypatch) -> None:
    monkeypatch.setenv("SECURITY_TOOL_GOVERNANCE_ENFORCEMENT", "true")
    audit = RecordingAuditService()

    _evaluate_at_execution_seam(tool_name="send_email", audit=audit)

    governance_event = next(
        event for event in audit.events if event.event_type == "tool_governance_decision"
    )
    serialized_details = str(governance_event.details)
    assert "recipient" not in governance_event.details
    assert "body" not in governance_event.details
    assert "raw_tool_payload" not in governance_event.details
    assert "external@example.com" not in serialized_details
    assert "should-not-export" not in serialized_details
