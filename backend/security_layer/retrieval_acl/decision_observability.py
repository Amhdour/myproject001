from __future__ import annotations

from typing import TYPE_CHECKING

from backend.security_layer.retrieval_acl.audit_events import (
    build_retrieval_acl_audit_event,
)
from backend.security_layer.retrieval_acl.audit_events import (
    record_retrieval_acl_audit_event,
)
from backend.security_layer.retrieval_acl.audit_events import RetrievalACLAuditEvent
from backend.security_layer.retrieval_acl.telemetry_counters import (
    record_retrieval_acl_telemetry_decision,
)

if TYPE_CHECKING:
    from backend.security_layer.retrieval_acl.enforce_hook import RetrievalACLDecision


def observe_retrieval_acl_decision(
    decision: RetrievalACLDecision,
) -> RetrievalACLAuditEvent:
    """Record in-memory audit and telemetry proof signals for one ACL decision.

    This combined observability helper is intentionally limited to redacted
    decision metadata and aggregate counters. It does not receive or store chunk
    text, user prompts, raw document content, secrets, credentials, or PII.
    Production and enterprise readiness remain explicit NO-GO proof boundaries.
    """

    audit_event = build_retrieval_acl_audit_event(decision)
    record_retrieval_acl_audit_event(audit_event)
    record_retrieval_acl_telemetry_decision(
        allowed=decision.allowed,
        reason=decision.reason,
    )
    return audit_event
