from __future__ import annotations

from backend.security_layer.tool_authorization.audit import audit_tool_authorization_decision
from backend.security_layer.tool_authorization.audit import clear_tool_authorization_audit_events
from backend.security_layer.tool_authorization.audit import get_tool_authorization_audit_events
from backend.security_layer.tool_authorization.enforcer import authorize_tool_call
from backend.security_layer.tool_authorization.models import ToolAuthorizationPolicy
from backend.security_layer.tool_authorization.models import ToolAuthorizationReason
from backend.security_layer.tool_authorization.models import ToolCallRequest
from backend.security_layer.tool_authorization.models import ToolRequesterContext


def _context(*, approved_request_ids: frozenset[str] = frozenset()) -> ToolRequesterContext:
    return ToolRequesterContext(
        tenant_id="tenant-a",
        subject_id="user-a",
        role_ids=frozenset({"analyst"}),
        approved_request_ids=approved_request_ids,
    )


def _request(
    *,
    request_id: str = "request-1",
    tenant_id: str = "tenant-a",
    tool_name: str = "internal_search",
    action: str = "read",
) -> ToolCallRequest:
    return ToolCallRequest(
        request_id=request_id,
        tenant_id=tenant_id,
        tool_name=tool_name,
        action=action,
    )


def _policies() -> dict[str, ToolAuthorizationPolicy]:
    return {
        "internal_search": ToolAuthorizationPolicy(
            tool_name="internal_search",
            tenant_id="tenant-a",
            allowed_subject_ids=frozenset({"user-a"}),
            allowed_role_ids=frozenset({"analyst"}),
            allowed_actions=frozenset({"read"}),
        ),
        "send_email": ToolAuthorizationPolicy(
            tool_name="send_email",
            tenant_id="tenant-a",
            allowed_subject_ids=frozenset({"user-a"}),
            allowed_role_ids=frozenset({"operator"}),
            allowed_actions=frozenset({"send"}),
            requires_approval=True,
        ),
    }


def setup_function() -> None:
    clear_tool_authorization_audit_events()


def test_allowed_tool_call_passes() -> None:
    decision = authorize_tool_call(
        context=_context(),
        request=_request(),
        policies=_policies(),
    )

    assert decision.status == "allow"
    assert decision.reason == ToolAuthorizationReason.ALLOWED
    audit_tool_authorization_decision(decision)
    assert get_tool_authorization_audit_events() == []


def test_unknown_tool_denied_and_audited() -> None:
    decision = authorize_tool_call(
        context=_context(),
        request=_request(tool_name="unknown_tool"),
        policies=_policies(),
    )
    audit_tool_authorization_decision(decision)

    assert decision.status == "deny"
    assert decision.reason == ToolAuthorizationReason.UNKNOWN_TOOL
    events = get_tool_authorization_audit_events()
    assert len(events) == 1
    assert events[0].tool_name == "unknown_tool"
    assert events[0].reason == "unknown_tool"
    assert events[0].production_readiness == "NO-GO"
    assert events[0].enterprise_readiness == "NO-GO"
    assert events[0].live_enforcement_claimed is False


def test_cross_tenant_tool_call_denied() -> None:
    decision = authorize_tool_call(
        context=_context(),
        request=_request(tenant_id="tenant-b"),
        policies=_policies(),
    )

    assert decision.status == "deny"
    assert decision.reason == ToolAuthorizationReason.CROSS_TENANT_TOOL_CALL


def test_disallowed_action_denied() -> None:
    decision = authorize_tool_call(
        context=_context(),
        request=_request(action="write"),
        policies=_policies(),
    )

    assert decision.status == "deny"
    assert decision.reason == ToolAuthorizationReason.DISALLOWED_ACTION


def test_required_approval_denied_when_missing() -> None:
    decision = authorize_tool_call(
        context=_context(),
        request=_request(request_id="email-1", tool_name="send_email", action="send"),
        policies=_policies(),
    )

    assert decision.status == "deny"
    assert decision.reason == ToolAuthorizationReason.MISSING_REQUIRED_APPROVAL


def test_required_approval_allowed_when_present() -> None:
    decision = authorize_tool_call(
        context=_context(approved_request_ids=frozenset({"email-1"})),
        request=_request(request_id="email-1", tool_name="send_email", action="send"),
        policies=_policies(),
    )

    assert decision.status == "allow"
    assert decision.reason == ToolAuthorizationReason.ALLOWED


def test_missing_context_denied() -> None:
    decision = authorize_tool_call(
        context=None,
        request=_request(),
        policies=_policies(),
    )

    assert decision.status == "deny"
    assert decision.reason == ToolAuthorizationReason.MISSING_CONTEXT


def test_malformed_context_denied() -> None:
    decision = authorize_tool_call(
        context=ToolRequesterContext(
            tenant_id="",
            subject_id="user-a",
            role_ids=frozenset({"analyst"}),
        ),
        request=_request(),
        policies=_policies(),
    )

    assert decision.status == "deny"
    assert decision.reason == ToolAuthorizationReason.MALFORMED_CONTEXT
