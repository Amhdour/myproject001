from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from datetime import datetime

from backend.security_layer.tool_authorization.models import ToolAuthorizationDecision


@dataclass(frozen=True)
class ToolAuthorizationAuditEvent:
    request_id: str | None
    status: str
    tool_name: str | None
    action: str | None
    reason: str
    created_at: str
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_enforcement_claimed: bool = False


_TOOL_AUTHORIZATION_AUDIT_EVENTS: list[ToolAuthorizationAuditEvent] = []


def build_tool_authorization_audit_event(
    decision: ToolAuthorizationDecision,
) -> ToolAuthorizationAuditEvent:
    return ToolAuthorizationAuditEvent(
        request_id=decision.request_id,
        status=decision.status,
        tool_name=decision.tool_name,
        action=decision.action,
        reason=decision.reason.value,
        created_at=datetime.now(UTC).isoformat(),
    )


def write_tool_authorization_audit_event(event: ToolAuthorizationAuditEvent) -> None:
    _TOOL_AUTHORIZATION_AUDIT_EVENTS.append(event)


def get_tool_authorization_audit_events() -> list[ToolAuthorizationAuditEvent]:
    return list(_TOOL_AUTHORIZATION_AUDIT_EVENTS)


def clear_tool_authorization_audit_events() -> None:
    _TOOL_AUTHORIZATION_AUDIT_EVENTS.clear()


def audit_tool_authorization_decision(decision: ToolAuthorizationDecision) -> None:
    if decision.status == "allow":
        return
    write_tool_authorization_audit_event(build_tool_authorization_audit_event(decision))
