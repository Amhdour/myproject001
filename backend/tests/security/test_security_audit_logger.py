from __future__ import annotations

from backend.security.audit.security_audit_logger import InMemorySecurityAuditLogger
from backend.security.policy.security_policy import SecurityPolicy
from backend.tests.security import factories


def test_audit_event_creation_and_redaction() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.cross_tenant_context())
    audit = InMemorySecurityAuditLogger()
    event = audit.emit(decision, details={"api_key": "sk-demo", "safe": "value"})
    assert event.decision == "deny"
    assert event.redacted_details["api_key"] == "[REDACTED]"
    assert event.redacted_details["safe"] == "value"
    assert len(audit.events) == 1
