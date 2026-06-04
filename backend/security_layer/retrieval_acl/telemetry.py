from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from backend.security_layer.retrieval_acl.audit import RetrievalACLAuditEvent
from backend.security_layer.retrieval_acl.models import RetrievalACLDecision


@dataclass(frozen=True)
class RetrievalACLTelemetrySummary:
    """Structured reviewer-safe telemetry summary for retrieval ACL decisions."""

    total_decisions: int
    allow_count: int
    deny_count: int
    filter_count: int
    denied_chunk_count: int
    denied_document_ids: tuple[str, ...]
    denial_reason_counts: dict[str, int]
    request_ids: tuple[str, ...]
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_enforcement_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLDecisionTelemetryRecord:
    """Single-decision telemetry record safe for evidence artifacts."""

    request_id: str
    status: str
    allowed_count: int
    denied_count: int
    denied_document_ids: tuple[str, ...]
    denied_reasons: tuple[str, ...]
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_enforcement_claimed: bool = False


def build_retrieval_acl_decision_telemetry_record(
    *,
    request_id: str,
    decision: RetrievalACLDecision,
) -> RetrievalACLDecisionTelemetryRecord:
    """Build a structured telemetry record from one ACL decision."""

    return RetrievalACLDecisionTelemetryRecord(
        request_id=request_id,
        status=decision.status,
        allowed_count=len(decision.allowed_chunks),
        denied_count=decision.denied_count,
        denied_document_ids=tuple(
            denial.document_id
            for denial in decision.denials
            if denial.document_id is not None
        ),
        denied_reasons=tuple(denial.reason.value for denial in decision.denials),
    )


def summarize_retrieval_acl_audit_events(
    events: tuple[RetrievalACLAuditEvent, ...] | list[RetrievalACLAuditEvent],
) -> RetrievalACLTelemetrySummary:
    """Summarize retrieval ACL audit events into reviewer-safe telemetry counts."""

    event_tuple = tuple(events)
    status_counts = Counter(event.status for event in event_tuple)
    reason_counts: Counter[str] = Counter()
    denied_document_ids: list[str] = []

    for event in event_tuple:
        reason_counts.update(event.reasons)
        denied_document_ids.extend(event.denied_document_ids)

    return RetrievalACLTelemetrySummary(
        total_decisions=len(event_tuple),
        allow_count=status_counts.get("allow", 0),
        deny_count=status_counts.get("deny", 0),
        filter_count=status_counts.get("filter", 0),
        denied_chunk_count=sum(event.denied_count for event in event_tuple),
        denied_document_ids=tuple(denied_document_ids),
        denial_reason_counts=dict(sorted(reason_counts.items())),
        request_ids=tuple(event.request_id for event in event_tuple),
    )


def render_retrieval_acl_telemetry_evidence(
    summary: RetrievalACLTelemetrySummary,
) -> str:
    """Render deterministic evidence text for CI artifacts and reviewer docs."""

    lines = [
        "retrieval_acl_telemetry_summary",
        f"total_decisions={summary.total_decisions}",
        f"allow_count={summary.allow_count}",
        f"deny_count={summary.deny_count}",
        f"filter_count={summary.filter_count}",
        f"denied_chunk_count={summary.denied_chunk_count}",
        f"denied_document_ids={','.join(summary.denied_document_ids)}",
        "denial_reason_counts="
        + ",".join(
            f"{reason}:{count}"
            for reason, count in summary.denial_reason_counts.items()
        ),
        f"request_ids={','.join(summary.request_ids)}",
        f"production_readiness={summary.production_readiness}",
        f"enterprise_readiness={summary.enterprise_readiness}",
        f"live_enforcement_claimed={str(summary.live_enforcement_claimed).lower()}",
    ]
    return "\n".join(lines) + "\n"
