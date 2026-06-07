from __future__ import annotations

from typing import Any

__all__ = ["SecurityDecision", "AuditEvent", "SecurityFinding"]


def __getattr__(name: str) -> Any:
    if name == "SecurityDecision":
        from onyx.security_layer.decisions.models import SecurityDecision

        return SecurityDecision
    if name == "AuditEvent":
        from onyx.security_layer.audit.models import AuditEvent

        return AuditEvent
    if name == "SecurityFinding":
        from onyx.security_layer.findings.models import SecurityFinding

        return SecurityFinding
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
