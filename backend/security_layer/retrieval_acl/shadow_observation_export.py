from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from typing import Any

from backend.security_layer.retrieval_acl.noop_seam_hook import (
    RetrievalACLRealPathShadowObservation,
)
from backend.security_layer.retrieval_acl.noop_seam_hook import (
    get_retrieval_acl_real_path_shadow_observations,
)


@dataclass(frozen=True)
class RetrievalACLShadowObservationEvidenceRecord:
    """Redacted evidence/audit-style record for real-path shadow observations.

    The record intentionally contains counts, mode, readiness boundaries, and a
    generated timestamp only. It does not include chunk text, document IDs,
    metadata, user prompts, credentials, secrets, or PII.
    """

    event_type: str
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


def export_retrieval_acl_shadow_observation_evidence(
    observations: tuple[RetrievalACLRealPathShadowObservation, ...] | None = None,
    *,
    observed_at_utc: str | None = None,
) -> tuple[RetrievalACLShadowObservationEvidenceRecord, ...]:
    """Export redacted shadow observations as reviewer-safe evidence records."""

    source = observations or get_retrieval_acl_real_path_shadow_observations()
    timestamp = observed_at_utc or datetime.now(UTC).replace(microsecond=0).isoformat()
    return tuple(_to_evidence_record(observation, timestamp) for observation in source)


def export_retrieval_acl_shadow_observation_evidence_dicts(
    observations: tuple[RetrievalACLRealPathShadowObservation, ...] | None = None,
    *,
    observed_at_utc: str | None = None,
) -> tuple[dict[str, Any], ...]:
    """Export redacted shadow observations as dictionaries for evidence artifacts."""

    return tuple(
        asdict(record)
        for record in export_retrieval_acl_shadow_observation_evidence(
            observations=observations,
            observed_at_utc=observed_at_utc,
        )
    )


def _to_evidence_record(
    observation: RetrievalACLRealPathShadowObservation,
    observed_at_utc: str,
) -> RetrievalACLShadowObservationEvidenceRecord:
    return RetrievalACLShadowObservationEvidenceRecord(
        event_type="retrieval_acl.real_path_shadow_observation",
        observed_at_utc=observed_at_utc,
        mode=observation.mode,
        observed_chunk_count=observation.observed_chunk_count,
        returned_chunk_count=observation.returned_chunk_count,
        behavior_changed=observation.behavior_changed,
        redacted=True,
        contains_document_content=False,
        contains_document_ids=False,
        contains_user_prompt=False,
        production_readiness=observation.production_readiness,
        enterprise_readiness=observation.enterprise_readiness,
        live_filtering_claimed=observation.live_filtering_claimed,
        live_blocking_claimed=observation.live_blocking_claimed,
        live_enforcement_claimed=observation.live_enforcement_claimed,
    )
