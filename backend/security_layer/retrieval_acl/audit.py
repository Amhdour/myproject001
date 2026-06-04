from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from uuid import uuid4

from backend.security_layer.retrieval_acl.models import RetrievalACLDenial
from backend.security_layer.retrieval_acl.models import RetrievalACLDecisionStatus


@dataclass(frozen=True)
class RetrievalACLAuditEvent:
    event_type: str
    event_id: str
    request_id: str
    status: RetrievalACLDecisionStatus
    denied_count: int
    denied_document_ids: tuple[str, ...]
    reasons: tuple[str, ...]
    timestamp: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_RETRIEVAL_ACL_AUDIT_EVENTS: list[RetrievalACLAuditEvent] = []


def build_retrieval_acl_audit_event(
    *,
    request_id: str,
    status: RetrievalACLDecisionStatus,
    denials: tuple[RetrievalACLDenial, ...],
) -> RetrievalACLAuditEvent:
    denied_document_ids = tuple(
        sorted({denial.document_id for denial in denials if denial.document_id is not None})
    )
    reasons = tuple(sorted({denial.reason.value for denial in denials}))
    return RetrievalACLAuditEvent(
        event_type="step_21_retrieval_acl_runtime_helper_denial",
        event_id=f"step21:{uuid4()}",
        request_id=request_id,
        status=status,
        denied_count=len(denials),
        denied_document_ids=denied_document_ids,
        reasons=reasons,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def write_retrieval_acl_audit_event(event: RetrievalACLAuditEvent) -> None:
    _RETRIEVAL_ACL_AUDIT_EVENTS.append(event)


def get_retrieval_acl_audit_events() -> list[RetrievalACLAuditEvent]:
    return list(_RETRIEVAL_ACL_AUDIT_EVENTS)


def clear_retrieval_acl_audit_events() -> None:
    _RETRIEVAL_ACL_AUDIT_EVENTS.clear()
