from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import UTC
from datetime import datetime
from datetime import timedelta
from typing import Any

from backend.security_layer.retrieval_acl.shadow_observation_audit import (
    RetrievalACLShadowObservationAuditEvent,
)


DEFAULT_SHADOW_OBSERVATION_RETENTION_DAYS = 30


@dataclass(frozen=True)
class RetrievalACLShadowObservationRetentionPolicy:
    """Redacted retention policy for shadow-observation audit events.

    The policy is intentionally small and reviewer-safe. It defines retention for
    redacted audit events only and does not store retrieval content.
    """

    retention_days: int = DEFAULT_SHADOW_OBSERVATION_RETENTION_DAYS
    redacted_required: bool = True
    allow_document_content: bool = False
    allow_document_ids: bool = False
    allow_user_prompt: bool = False
    allow_secrets: bool = False
    allow_pii: bool = False
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_filtering_claimed: bool = False
    live_blocking_claimed: bool = False
    live_enforcement_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLShadowObservationRetentionDecision:
    """Retention decision for one redacted shadow-observation audit event."""

    request_id: str
    retain_until_utc: str
    retention_days: int
    eligible_for_retention: bool
    delete_after_retention: bool
    redaction_policy_passed: bool
    reason: str
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_filtering_claimed: bool = False
    live_blocking_claimed: bool = False
    live_enforcement_claimed: bool = False


def build_shadow_observation_retention_decisions(
    *,
    audit_events: tuple[RetrievalACLShadowObservationAuditEvent, ...],
    policy: RetrievalACLShadowObservationRetentionPolicy | None = None,
    evaluated_at_utc: str | None = None,
) -> tuple[RetrievalACLShadowObservationRetentionDecision, ...]:
    """Apply the redacted retention policy to audit events."""

    resolved_policy = policy or RetrievalACLShadowObservationRetentionPolicy()
    evaluated_at = _parse_or_now(evaluated_at_utc)
    retain_until = evaluated_at + timedelta(days=resolved_policy.retention_days)
    retain_until_utc = retain_until.replace(microsecond=0).isoformat()

    return tuple(
        _decision_for_event(
            event=event,
            policy=resolved_policy,
            retain_until_utc=retain_until_utc,
        )
        for event in audit_events
    )


def build_shadow_observation_retention_decision_dicts(
    *,
    audit_events: tuple[RetrievalACLShadowObservationAuditEvent, ...],
    policy: RetrievalACLShadowObservationRetentionPolicy | None = None,
    evaluated_at_utc: str | None = None,
) -> tuple[dict[str, Any], ...]:
    """Return retention decisions as dictionaries for evidence artifacts."""

    return tuple(
        asdict(decision)
        for decision in build_shadow_observation_retention_decisions(
            audit_events=audit_events,
            policy=policy,
            evaluated_at_utc=evaluated_at_utc,
        )
    )


def _decision_for_event(
    *,
    event: RetrievalACLShadowObservationAuditEvent,
    policy: RetrievalACLShadowObservationRetentionPolicy,
    retain_until_utc: str,
) -> RetrievalACLShadowObservationRetentionDecision:
    redaction_policy_passed = (
        event.redacted is policy.redacted_required
        and event.contains_document_content is policy.allow_document_content
        and event.contains_document_ids is policy.allow_document_ids
        and event.contains_user_prompt is policy.allow_user_prompt
        and event.live_filtering_claimed is False
        and event.live_blocking_claimed is False
        and event.live_enforcement_claimed is False
    )
    reason = (
        "redacted_shadow_observation_audit_event_retained"
        if redaction_policy_passed
        else "redaction_policy_failed_do_not_retain"
    )

    return RetrievalACLShadowObservationRetentionDecision(
        request_id=event.request_id,
        retain_until_utc=retain_until_utc,
        retention_days=policy.retention_days,
        eligible_for_retention=redaction_policy_passed,
        delete_after_retention=redaction_policy_passed,
        redaction_policy_passed=redaction_policy_passed,
        reason=reason,
        production_readiness=policy.production_readiness,
        enterprise_readiness=policy.enterprise_readiness,
        live_filtering_claimed=policy.live_filtering_claimed,
        live_blocking_claimed=policy.live_blocking_claimed,
        live_enforcement_claimed=policy.live_enforcement_claimed,
    )


def _parse_or_now(value: str | None) -> datetime:
    if value is None:
        return datetime.now(UTC)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)
