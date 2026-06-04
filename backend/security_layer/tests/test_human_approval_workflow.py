from __future__ import annotations

from backend.security_layer.human_approval.audit import audit_human_approval_decision
from backend.security_layer.human_approval.audit import clear_human_approval_audit_events
from backend.security_layer.human_approval.audit import get_human_approval_audit_events
from backend.security_layer.human_approval.enforcer import evaluate_human_approval
from backend.security_layer.human_approval.models import AgentActionContext
from backend.security_layer.human_approval.models import AgentActionRequest
from backend.security_layer.human_approval.models import HumanApprovalPolicy
from backend.security_layer.human_approval.models import HumanApprovalReason
from backend.security_layer.human_approval.models import HumanApprovalRecord


def _context() -> AgentActionContext:
    return AgentActionContext(
        tenant_id="tenant-a",
        subject_id="user-a",
        role_ids=frozenset({"operator"}),
    )


def _policy() -> HumanApprovalPolicy:
    return HumanApprovalPolicy(
        high_risk_actions=frozenset({"send_email", "delete_document", "external_api_call"}),
        approval_required_risk_levels=frozenset({"high"}),
    )


def _request(
    *,
    request_id: str = "request-1",
    tenant_id: str = "tenant-a",
    subject_id: str = "user-a",
    action_name: str = "read_document",
    risk_level: str = "low",
) -> AgentActionRequest:
    return AgentActionRequest(
        request_id=request_id,
        tenant_id=tenant_id,
        subject_id=subject_id,
        action_name=action_name,
        risk_level=risk_level,
    )


def _approval(
    *,
    approval_id: str = "approval-1",
    request_id: str = "request-1",
    tenant_id: str = "tenant-a",
    subject_id: str = "user-a",
    action_name: str = "send_email",
    status: str = "approved",
) -> HumanApprovalRecord:
    return HumanApprovalRecord(
        approval_id=approval_id,
        request_id=request_id,
        tenant_id=tenant_id,
        subject_id=subject_id,
        action_name=action_name,
        status=status,
    )


def setup_function() -> None:
    clear_human_approval_audit_events()


def test_low_risk_action_allowed_without_approval() -> None:
    decision = evaluate_human_approval(
        context=_context(),
        request=_request(action_name="read_document", risk_level="low"),
        policy=_policy(),
        approvals={},
    )

    assert decision.status == "allow"
    assert decision.reason == HumanApprovalReason.ALLOWED_LOW_RISK
    audit_human_approval_decision(decision)
    assert get_human_approval_audit_events() == []


def test_high_risk_action_denied_without_approval_and_audited() -> None:
    request = _request(request_id="email-1", action_name="send_email", risk_level="high")
    decision = evaluate_human_approval(
        context=_context(),
        request=request,
        policy=_policy(),
        approvals={},
    )
    audit_human_approval_decision(decision)

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.APPROVAL_NOT_FOUND
    events = get_human_approval_audit_events()
    assert len(events) == 1
    assert events[0].request_id == "email-1"
    assert events[0].action_name == "send_email"
    assert events[0].reason == "approval_not_found"
    assert events[0].production_readiness == "NO-GO"
    assert events[0].enterprise_readiness == "NO-GO"
    assert events[0].live_enforcement_claimed is False


def test_high_risk_action_allowed_with_matching_approval() -> None:
    request = _request(request_id="email-1", action_name="send_email", risk_level="high")
    decision = evaluate_human_approval(
        context=_context(),
        request=request,
        policy=_policy(),
        approvals={"email-1": _approval(request_id="email-1", action_name="send_email")},
    )

    assert decision.status == "allow"
    assert decision.reason == HumanApprovalReason.APPROVED


def test_rejected_approval_denied() -> None:
    request = _request(request_id="email-1", action_name="send_email", risk_level="high")
    decision = evaluate_human_approval(
        context=_context(),
        request=request,
        policy=_policy(),
        approvals={
            "email-1": _approval(
                request_id="email-1",
                action_name="send_email",
                status="rejected",
            )
        },
    )

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.APPROVAL_REJECTED


def test_expired_approval_denied() -> None:
    request = _request(request_id="email-1", action_name="send_email", risk_level="high")
    decision = evaluate_human_approval(
        context=_context(),
        request=request,
        policy=_policy(),
        approvals={
            "email-1": _approval(
                request_id="email-1",
                action_name="send_email",
                status="expired",
            )
        },
    )

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.APPROVAL_EXPIRED


def test_mismatched_approval_tenant_denied() -> None:
    request = _request(request_id="email-1", action_name="send_email", risk_level="high")
    decision = evaluate_human_approval(
        context=_context(),
        request=request,
        policy=_policy(),
        approvals={
            "email-1": _approval(
                request_id="email-1",
                tenant_id="tenant-b",
                action_name="send_email",
            )
        },
    )

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.APPROVAL_TENANT_MISMATCH


def test_mismatched_approval_action_denied() -> None:
    request = _request(request_id="email-1", action_name="send_email", risk_level="high")
    decision = evaluate_human_approval(
        context=_context(),
        request=request,
        policy=_policy(),
        approvals={
            "email-1": _approval(
                request_id="email-1",
                action_name="delete_document",
            )
        },
    )

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.APPROVAL_ACTION_MISMATCH


def test_missing_context_denied() -> None:
    decision = evaluate_human_approval(
        context=None,
        request=_request(action_name="send_email", risk_level="high"),
        policy=_policy(),
        approvals={},
    )

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.MISSING_CONTEXT


def test_malformed_context_denied() -> None:
    decision = evaluate_human_approval(
        context=AgentActionContext(
            tenant_id="",
            subject_id="user-a",
            role_ids=frozenset({"operator"}),
        ),
        request=_request(action_name="send_email", risk_level="high"),
        policy=_policy(),
        approvals={},
    )

    assert decision.status == "deny"
    assert decision.reason == HumanApprovalReason.MALFORMED_CONTEXT
