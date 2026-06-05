from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from typing import Any

from backend.security_layer.retrieval_acl.shadow_observation_export import (
    RetrievalACLShadowObservationEvidenceRecord,
)
from backend.security_layer.retrieval_acl.shadow_observation_export import (
    export_retrieval_acl_shadow_observation_evidence,
)


@dataclass(frozen=True)
class RetrievalACLShadowObservationAuditEvent:
    """Correlation-friendly, redacted audit event for shadow observations.

    The event keeps a caller-provided request ID and stage name for correlation,
    but intentionally excludes document content, document IDs, prompts, secrets,
    credentials, metadata, and PII.
    """

    event_type: str
    request_id: str
    pipeline_stage: str
    observed_at_utc: str
    mode: str
    observed_chunk_count: int
    returned_chunk_count: int
    behavior_changed: bool
    redacted: bool
    contains_document_content: bool
    contains_document_ids: bool
    contains_user_prompt: bool
    production_readiness: str
    enterprise_readiness: str
    live_filtering_claimed: bool
    live_blocking_claimed: bool
    live_enforcement_claimed: bool


def build_retrieval_acl_shadow_observation_audit_events(
    *,
    request_id: str,
    pipeline_stage: str = "search_pipeline.post_censoring.return_hook",
    observed_at_utc: str | None = None,
) -> tuple[RetrievalACLShadowObservationAuditEvent, ...]:
    """Build redacted audit events from current shadow observation evidence."""

    evidence_records = export_retrieval_acl_shadow_observation_evidence(
        observed_at_utc=observed_at_utc,
    )
    return tuple(
        _to_audit_event(
            record=record,
            request_id=request_id,
            pipeline_stage=pipeline_stage,
        )
        for record in evidence_records
    )


def build_retrieval_acl_shadow_observation_audit_dicts(
    *,
    request_id: str,
    pipeline_stage: str = "search_pipeline.post_censoring.return_hook",
    observed_at_utc: str | None = None,
) -> tuple[dict[str, Any], ...]:
    """Build dictionary audit events for artifact/export usage."""

    return tuple(
        asdict(event)
        for event in build_retrieval_acl_shadow_observation_audit_events(
            request_id=request_id,
            pipeline_stage=pipeline_stage,
            observed_at_utc=observed_at_utc,
        )
    )


def _to_audit_event(
    *,
    record: RetrievalACLShadowObservationEvidenceRecord,
    request_id: str,
    pipeline_stage: str,
) -> RetrievalACLShadowObservationAuditEvent:
    return RetrievalACLShadowObservationAuditEvent(
        event_type="retrieval_acl.shadow_observation.audit",
        request_id=request_id,
        pipeline_stage=pipeline_stage,
        observed_at_utc=record.observed_at_utc,
        mode=record.mode,
        observed_chunk_count=record.observed_chunk_count,
        returned_chunk_count=record.returned_chunk_count,
        behavior_changed=record.behavior_changed,
        redacted=record.redacted,
        contains_document_content=record.contains_document_content,
        contains_document_ids=record.contains_document_ids,
        contains_user_prompt=record.contains_user_prompt,
        production_readiness=record.production_readiness,
        enterprise_readiness=record.enterprise_readiness,
        live_filtering_claimed=record.live_filtering_claimed,
        live_blocking_claimed=record.live_blocking_claimed,
        live_enforcement_claimed=record.live_enforcement_claimed,
    )
