from __future__ import annotations

from typing import Any

from onyx.security_layer.audit.models import AuditEvent


def __getattr__(name: str) -> Any:
    if name == "AuditService":
        from onyx.security_layer.audit.service import AuditService

        return AuditService
    raise AttributeError(name)


__all__ = ["AuditEvent", "AuditService"]
