from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Final

if TYPE_CHECKING:
    from backend.security_layer.retrieval_acl.enforce_hook import RetrievalACLDecision

RETRIEVAL_ACL_AUDIT_EVENT_TYPE: Final[str] = "retrieval_acl.decision"
RETRIEVAL_ACL_CONTROL_ID: Final[str] = "retrieval-acl-enforcement-v1"

_RETRIEVAL_ACL_AUDIT_EVENTS: list[RetrievalACLAuditEvent] = []


@dataclass(frozen=True)
class RetrievalACLAuditEvent:
    """Reviewer-safe Retrieval ACL decision audit event.

    The schema intentionally stores only decision metadata. It does not include
    retrieved chunk text, user prompts, raw document bodies, secrets,
    credentials, or PII. The sink below is an in-memory proof-only sink and is
    not database-backed persistence.
    """

    event_type: str
    control_id: str
    policy_version: str
    mode: str
    decision: str
    reason: str
    user_tenant_id: str
    chunk_tenant_id: str
    document_ref: str
    production_readiness: str
    enterprise_readiness: str


def build_retrieval_acl_audit_event(
    decision: RetrievalACLDecision,
) -> RetrievalACLAuditEvent:
    """Convert a Retrieval ACL decision into a redacted audit event."""

    return RetrievalACLAuditEvent(
        event_type=RETRIEVAL_ACL_AUDIT_EVENT_TYPE,
        control_id=RETRIEVAL_ACL_CONTROL_ID,
        policy_version=decision.policy_version,
        mode=decision.mode,
        decision="allowed" if decision.allowed else "denied",
        reason=decision.reason,
        user_tenant_id=decision.user_tenant_id,
        chunk_tenant_id=decision.chunk_tenant_id,
        document_ref=decision.document_ref,
        production_readiness=decision.production_readiness,
        enterprise_readiness=decision.enterprise_readiness,
    )


def record_retrieval_acl_audit_event(event: RetrievalACLAuditEvent) -> None:
    """Record an event in the focused in-memory proof sink."""

    _RETRIEVAL_ACL_AUDIT_EVENTS.append(event)


def get_retrieval_acl_audit_events() -> tuple[RetrievalACLAuditEvent, ...]:
    """Return recorded in-memory events without exposing mutable sink state."""

    return tuple(_RETRIEVAL_ACL_AUDIT_EVENTS)


def clear_retrieval_acl_audit_events() -> None:
    """Clear the focused in-memory proof sink."""

    _RETRIEVAL_ACL_AUDIT_EVENTS.clear()
