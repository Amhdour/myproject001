from __future__ import annotations

import pytest

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLReason
from backend.security_layer.retrieval_acl.shadow_mode import evaluate_retrieval_acl_shadow_mode


def _context() -> RetrievalACLContext:
    return RetrievalACLContext(
        tenant_id="tenant-a",
        subject_id="user-a",
        group_ids=frozenset({"group-a"}),
        allowed_document_ids=frozenset({"doc-allowed", "doc-group"}),
    )


def _chunk(
    *,
    chunk_id: str | int = "chunk-allowed",
    document_id: str = "doc-allowed",
    tenant_id: str = "tenant-a",
    allowed_subject_ids: list[str] | str | None = "user-a",
    allowed_group_ids: list[str] | str | None = None,
) -> OnyxLikeRetrievalChunk:
    metadata: dict[str, object] = {"tenant_id": tenant_id}
    if allowed_subject_ids is not None:
        metadata["allowed_subject_ids"] = allowed_subject_ids
    if allowed_group_ids is not None:
        metadata["allowed_group_ids"] = allowed_group_ids
    return OnyxLikeRetrievalChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        metadata=metadata,
    )


def setup_function() -> None:
    clear_retrieval_acl_audit_events()


def test_shadow_mode_preserves_original_chunks_while_recording_filter_decision() -> None:
    allowed_chunk = _chunk()
    forbidden_chunk = _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden")
    cross_tenant_chunk = _chunk(
        chunk_id="chunk-cross-tenant",
        document_id="doc-allowed",
        tenant_id="tenant-b",
    )
    original_chunks = (allowed_chunk, forbidden_chunk, cross_tenant_chunk)

    result = evaluate_retrieval_acl_shadow_mode(
        context=_context(),
        chunks=original_chunks,
        request_id="request-shadow-filter",
        mode="shadow",
    )

    assert result.mode == "shadow"
    assert result.decision.status == "filter"
    assert result.returned_chunks == original_chunks
    assert result.would_return_chunks == (allowed_chunk,)
    assert result.evidence.mode == "shadow"
    assert result.evidence.observed_chunk_count == 3
    assert result.evidence.would_return_chunk_count == 1
    assert result.evidence.returned_chunk_count == 3
    assert result.evidence.denied_count == 2
    assert result.evidence.denied_document_ids == ("doc-forbidden", "doc-allowed")
    assert result.evidence.denied_reasons == (
        RetrievalACLReason.UNAUTHORIZED_DOCUMENT_ID.value,
        RetrievalACLReason.CROSS_TENANT_RESULT.value,
    )
    assert result.evidence.production_readiness == "NO-GO"
    assert result.evidence.enterprise_readiness == "NO-GO"
    assert result.evidence.live_enforcement_claimed is False

    audit_events = get_retrieval_acl_audit_events()
    assert len(audit_events) == 1
    assert audit_events[0].request_id == "request-shadow-filter"
    assert audit_events[0].status == "filter"


def test_shadow_mode_allows_all_when_acl_decision_allows() -> None:
    allowed_chunk = _chunk()

    result = evaluate_retrieval_acl_shadow_mode(
        context=_context(),
        chunks=[allowed_chunk],
        request_id="request-shadow-allow",
        mode="shadow",
    )

    assert result.decision.status == "allow"
    assert result.returned_chunks == (allowed_chunk,)
    assert result.would_return_chunks == (allowed_chunk,)
    assert result.evidence.denied_count == 0
    assert get_retrieval_acl_audit_events() == []


def test_shadow_mode_records_deny_without_changing_returned_chunks() -> None:
    forbidden_chunk = _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden")

    result = evaluate_retrieval_acl_shadow_mode(
        context=_context(),
        chunks=[forbidden_chunk],
        request_id="request-shadow-deny",
        mode="shadow",
    )

    assert result.decision.status == "deny"
    assert result.returned_chunks == (forbidden_chunk,)
    assert result.would_return_chunks == ()
    assert result.evidence.denied_count == 1
    assert result.evidence.returned_chunk_count == 1


def test_explicit_enforce_mode_filters_returned_chunks() -> None:
    allowed_chunk = _chunk()
    forbidden_chunk = _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden")

    result = evaluate_retrieval_acl_shadow_mode(
        context=_context(),
        chunks=[allowed_chunk, forbidden_chunk],
        request_id="request-enforce-filter",
        mode="enforce",
    )

    assert result.mode == "enforce"
    assert result.decision.status == "filter"
    assert result.returned_chunks == (allowed_chunk,)
    assert result.would_return_chunks == (allowed_chunk,)
    assert result.evidence.returned_chunk_count == 1
    assert result.evidence.live_enforcement_claimed is False


def test_shadow_mode_fails_closed_for_missing_context_but_preserves_shadow_return() -> None:
    chunk = _chunk()

    result = evaluate_retrieval_acl_shadow_mode(
        context=None,
        chunks=[chunk],
        request_id="request-shadow-missing-context",
        mode="shadow",
    )

    assert result.decision.status == "deny"
    assert result.returned_chunks == (chunk,)
    assert result.would_return_chunks == ()
    assert result.evidence.denied_reasons == (
        RetrievalACLReason.MISSING_ACL_CONTEXT.value,
    )


def test_invalid_mode_rejected() -> None:
    with pytest.raises(ValueError):
        evaluate_retrieval_acl_shadow_mode(
            context=_context(),
            chunks=[_chunk()],
            mode="invalid",
        )
