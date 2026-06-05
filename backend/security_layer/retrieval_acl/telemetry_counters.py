from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RetrievalACLTelemetrySnapshot:
    """In-memory Retrieval ACL decision-counter snapshot.

    The snapshot stores aggregate counters only. It intentionally does not store
    chunk text, prompt text, raw document content, secrets, credentials, or PII.
    This proof-only telemetry is process-local and is not durable monitoring.
    """

    allowed_count: int
    denied_count: int
    fail_closed_count: int
    storage_scope: str = "in_memory_only"
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"


_ALLOWED_COUNT = 0
_DENIED_COUNT = 0
_FAIL_CLOSED_COUNT = 0


def clear_retrieval_acl_telemetry_counters() -> None:
    """Reset the process-local Retrieval ACL telemetry proof counters."""

    global _ALLOWED_COUNT
    global _DENIED_COUNT
    global _FAIL_CLOSED_COUNT

    _ALLOWED_COUNT = 0
    _DENIED_COUNT = 0
    _FAIL_CLOSED_COUNT = 0


def record_retrieval_acl_telemetry_decision(*, allowed: bool, reason: str) -> None:
    """Record one enforce-mode Retrieval ACL decision in memory.

    The caller is responsible for invoking this helper only for enforce-mode
    decisions. The helper receives only the boolean decision and coarse reason,
    so it cannot retain chunk text, prompt text, raw document content, secrets,
    credentials, or PII.
    """

    global _ALLOWED_COUNT
    global _DENIED_COUNT
    global _FAIL_CLOSED_COUNT

    if allowed:
        _ALLOWED_COUNT += 1
        return

    if reason == "missing_acl_metadata":
        _FAIL_CLOSED_COUNT += 1
        return

    _DENIED_COUNT += 1


def get_retrieval_acl_telemetry_snapshot() -> RetrievalACLTelemetrySnapshot:
    """Return immutable aggregate Retrieval ACL telemetry counters."""

    return RetrievalACLTelemetrySnapshot(
        allowed_count=_ALLOWED_COUNT,
        denied_count=_DENIED_COUNT,
        fail_closed_count=_FAIL_CLOSED_COUNT,
    )
