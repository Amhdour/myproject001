from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AuditEvent:
    action: str
    decision: str
    mode: str
    request_id: str
    details: dict[str, Any] = field(default_factory=dict)


_AUDIT_EVENTS: list[AuditEvent] = []


def write_audit_event(event: AuditEvent) -> None:
    _AUDIT_EVENTS.append(event)


def get_audit_events() -> list[AuditEvent]:
    return list(_AUDIT_EVENTS)


def clear_audit_events() -> None:
    _AUDIT_EVENTS.clear()
