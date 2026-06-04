from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC
from datetime import datetime

from backend.security_layer.human_approval.models import HumanApprovalDecision


@dataclass(frozen=True)
class HumanApprovalAuditEvent:
    request_id: str | None
    status: str
    action_name: str | None
    reason: str
    created_at: str
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_enforcement_claimed: bool = False


_HUMAN_APPROVAL_AUDIT_EVENTS: list[HumanApprovalAuditEvent] = []


def build_human_approval_audit_event(
    decision: HumanApprovalDecision,
) -> HumanApprovalAuditEvent:
    return HumanApprovalAuditEvent(
        request_id=decision.request_id,
        status=decision.status,
        action_name=decision.action_name,
        reason=decision.reason.value,
        created_at=datetime.now(UTC).isoformat(),
    )


def write_human_approval_audit_event(event: HumanApprovalAuditEvent) -> None:
    _HUMAN_APPROVAL_AUDIT_EVENTS.append(event)


def get_human_approval_audit_events() -> list[HumanApprovalAuditEvent]:
    return list(_HUMAN_APPROVAL_AUDIT_EVENTS)


def clear_human_approval_audit_events() -> None:
    _HUMAN_APPROVAL_AUDIT_EVENTS.clear()


def audit_human_approval_decision(decision: HumanApprovalDecision) -> None:
    if decision.status == "allow":
        return
    write_human_approval_audit_event(build_human_approval_audit_event(decision))
