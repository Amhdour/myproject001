from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.runtime_enforcement.audit import clear_runtime_audit_events
from backend.security_layer.runtime_enforcement.audit import get_runtime_audit_events
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementConfig
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementMode
from backend.security_layer.runtime_enforcement.context import RuntimeRetrievalContext
from backend.security_layer.runtime_enforcement.retrieval_adapter import enforce_retrieval_runtime
from backend.security_layer.runtime_enforcement.telemetry import clear_runtime_retrieval_acl_metrics
from backend.security_layer.runtime_enforcement.telemetry import get_runtime_retrieval_acl_metrics


@dataclass(frozen=True)
class FakeRetrievedChunk:
    document_id: str
    chunk_id: int
    metadata: dict[str, str | list[str]]


def _context() -> RuntimeRetrievalContext:
    return RuntimeRetrievalContext(
        request_id="step-63x-isolated-pytest-request",
        subject_id="user-a",
        tenant_id="tenant-a",
    )


def setup_function() -> None:
    clear_runtime_audit_events()
    clear_runtime_retrieval_acl_metrics()


def test_disabled_mode_preserves_existing_retrieval_behavior() -> None:
    chunks = [
        FakeRetrievedChunk("doc-a", 1, {"tenant_id": "tenant-a"}),
        FakeRetrievedChunk("doc-b", 2, {"tenant_id": "tenant-b"}),
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.DISABLED),
        context=_context(),
        chunks=chunks,
    )

    assert result.allowed_chunks == tuple(chunks)
    assert result.enforcement_result == "not_applied"
    assert result.audit_event is None
    assert get_runtime_audit_events() == []
    assert get_runtime_retrieval_acl_metrics() == []


def test_monitor_only_records_cross_tenant_violation_without_blocking() -> None:
    chunks = [
        FakeRetrievedChunk("doc-a", 1, {"tenant_id": "tenant-a"}),
        FakeRetrievedChunk("doc-b", 2, {"tenant_id": "tenant-b"}),
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.MONITOR_ONLY),
        context=_context(),
        chunks=chunks,
    )

    assert result.allowed_chunks == tuple(chunks)
    assert result.decision == "deny"
    assert result.denied_chunk_count == 1
    assert result.enforcement_result == "observed"
    assert get_runtime_audit_events()[-1].reason_code == "retrieval_authorization_failed"
    assert get_runtime_retrieval_acl_metrics()[-1].enforcement_result == "observed"


def test_enforce_mode_blocks_cross_tenant_chunk_and_allows_same_tenant_chunk() -> None:
    allowed = FakeRetrievedChunk("doc-a", 1, {"tenant_id": "tenant-a"})
    denied = FakeRetrievedChunk("doc-b", 2, {"tenant_id": "tenant-b"})

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=_context(),
        chunks=[allowed, denied],
    )

    assert result.allowed_chunks == (allowed,)
    assert result.decision == "deny"
    assert result.denied_chunk_count == 1
    assert result.enforcement_result == "blocked"
    assert result.safe_denial is not None
    assert "tenant-b" not in str(result.safe_denial)
    assert "doc-b" not in str(result.safe_denial)


def test_enforce_mode_allows_authorized_same_tenant_subject_scoped_chunk() -> None:
    chunk = FakeRetrievedChunk(
        "doc-a",
        1,
        {"tenant_id": "tenant-a", "allowed_subject_ids": ["user-a", "user-b"]},
    )

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=_context(),
        chunks=[chunk],
    )

    assert result.allowed_chunks == (chunk,)
    assert result.decision == "allow"
    assert result.denied_chunk_count == 0
    assert result.enforcement_result == "allowed"
    assert get_runtime_audit_events()[-1].reason_code == "retrieval_authorized"
    assert get_runtime_retrieval_acl_metrics()[-1].decision == "allow"


def test_enforce_mode_blocks_wrong_subject_even_when_tenant_matches() -> None:
    chunk = FakeRetrievedChunk(
        "doc-a",
        1,
        {"tenant_id": "tenant-a", "allowed_subject_ids": ["user-b"]},
    )

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=_context(),
        chunks=[chunk],
    )

    assert result.allowed_chunks == ()
    assert result.decision == "deny"
    assert result.denied_chunk_count == 1
    assert get_runtime_audit_events()[-1].enforcement_result == "blocked"
    assert get_runtime_retrieval_acl_metrics()[-1].denied_chunk_count == 1
