from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from backend.security.policy.policy_decision import PolicyDecision

_SENSITIVE_TOKENS = ("secret", "token", "password", "api_key", "credential", "authorization")


@dataclass(frozen=True)
class SecurityAuditEvent:
    timestamp: str
    correlation_id: str
    user_id: str | None
    tenant_id: str | None
    action: str
    resource_type: str
    resource_id: str
    decision: str
    reason: str
    policy_version: str
    enforcement_point: str
    risk_level: str
    redacted_details: dict[str, str | int | float | bool | None] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class InMemorySecurityAuditLogger:
    def __init__(self) -> None:
        self.events: list[SecurityAuditEvent] = []

    def emit(
        self,
        decision: PolicyDecision,
        *,
        details: dict[str, object] | None = None,
    ) -> SecurityAuditEvent:
        event = SecurityAuditEvent(
            timestamp=datetime.now(UTC).isoformat(),
            correlation_id=decision.correlation_id,
            user_id=decision.user_id,
            tenant_id=decision.tenant_id,
            action=decision.action,
            resource_type=decision.resource_type,
            resource_id=decision.resource_id,
            decision=decision.decision.value,
            reason=decision.reason,
            policy_version=decision.policy_version,
            enforcement_point=decision.enforcement_point,
            risk_level=decision.risk_level.value,
            redacted_details=redact_details(details or {}),
        )
        self.events.append(event)
        return event

    def write_jsonl(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "\n".join(json.dumps(event.to_dict(), sort_keys=True) for event in self.events)
            + ("\n" if self.events else ""),
            encoding="utf-8",
        )


def redact_details(details: dict[str, object]) -> dict[str, str | int | float | bool | None]:
    redacted: dict[str, str | int | float | bool | None] = {}
    for key, value in details.items():
        if any(token in key.lower() for token in _SENSITIVE_TOKENS):
            redacted[key] = "[REDACTED]"
        elif isinstance(value, str | int | float | bool) or value is None:
            redacted[key] = value
        else:
            redacted[key] = str(value)
    return redacted
