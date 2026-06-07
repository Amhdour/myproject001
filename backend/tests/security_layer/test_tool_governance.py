from __future__ import annotations

import pytest

from onyx.security_layer.langfuse_evidence import safe_tool_governance_langfuse_payload
from onyx.security_layer.tool_governance import evaluate_tool_governance
from onyx.security_layer.tool_governance import LocalApprovalStore
from onyx.security_layer.tool_governance import SelfApprovalError
from onyx.security_layer.tool_governance import ToolActionRequest
from onyx.security_layer.tool_governance import ToolGovernanceConfig
from onyx.security_layer.tool_governance import ToolGovernanceDecision
from onyx.security_layer.tool_governance import ToolRiskLevel


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
