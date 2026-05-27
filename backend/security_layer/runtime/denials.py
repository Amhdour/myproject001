from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityDenial(Exception):
    message: str
    reason_code: str = "security_denied"

    def __str__(self) -> str:
        return self.message


def safe_denial_message(reason: str | None = None) -> str:
    if reason in {"missing_subject", "missing_tenant", "evaluation_error", "evaluator_unavailable"}:
        return "Request blocked by security policy."
    return "Request blocked by security controls."


def raise_security_denial(reason: str | None = None) -> None:
    raise SecurityDenial(message=safe_denial_message(reason), reason_code=reason or "security_denied")
