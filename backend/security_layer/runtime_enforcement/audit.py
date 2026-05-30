from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from typing import Literal
from uuid import uuid4

from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementMode


DecisionValue = Literal["allow", "deny"]


@dataclass(frozen=True)
class RuntimeAuditEvent:
    event_type: str
    decision_id: str
    request_id: str
    mode: str
    action: str
    resource_type: str
    tenant_id: str | None
    subject_id: str | None
    decision: DecisionValue
    reason_code: str
    timestamp: str
    enforcement_result: str

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


_RUNTIME_AUDIT_EVENTS: list[RuntimeAuditEvent] = []


def build_runtime_audit_event(
    *,
    request_id: str,
    mode: RuntimeEnforcementMode,
    action: str,
    resource_type: str,
    tenant_id: str | None,
    subject_id: str | None,
    decision: DecisionValue,
    reason_code: str,
    enforcement_result: str,
) -> RuntimeAuditEvent:
    return RuntimeAuditEvent(
        event_type="step_39x_runtime_retrieval_authorization",
        decision_id=f"step39x:{uuid4()}",
        request_id=request_id,
        mode=mode.value,
        action=action,
        resource_type=resource_type,
        tenant_id=tenant_id,
        subject_id=subject_id,
        decision=decision,
        reason_code=reason_code,
        timestamp=datetime.now(timezone.utc).isoformat(),
        enforcement_result=enforcement_result,
    )


def write_runtime_audit_event(event: RuntimeAuditEvent) -> None:
    _RUNTIME_AUDIT_EVENTS.append(event)


def get_runtime_audit_events() -> list[RuntimeAuditEvent]:
    return list(_RUNTIME_AUDIT_EVENTS)


def clear_runtime_audit_events() -> None:
    _RUNTIME_AUDIT_EVENTS.clear()
