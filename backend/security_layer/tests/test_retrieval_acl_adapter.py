from __future__ import annotations

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.adapter import (
    adapt_onyx_like_chunk_to_retrieval_acl_chunk,
)
from backend.security_layer.retrieval_acl.adapter import (
    enforce_retrieval_acl_on_onyx_like_chunks,
)
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLReason
from backend.security_layer.retrieval_acl.models import RetrievalResultChunk


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


def test_adapter_maps_onyx_like_chunk_to_retrieval_acl_chunk() -> None:
    adapted = adapt_onyx_like_chunk_to_retrieval_acl_chunk(
        _chunk(chunk_id=123, allowed_subject_ids=["user-a", "user-b"])
    )

    assert isinstance(adapted, RetrievalResultChunk)
    assert adapted.chunk_id == "123"
    assert adapted.document_id == "doc-allowed"
    assert adapted.tenant_id == "tenant-a"
    assert adapted.document_acl.allowed_subject_ids == frozenset({"user-a", "user-b"})


def test_adapter_allows_and_returns_original_chunk() -> None:
    original_chunk = _chunk()

    result = enforce_retrieval_acl_on_onyx_like_chunks(
        context=_context(),
        chunks=[original_chunk],
    )

    assert result.decision.status == "allow"
    assert result.allowed_original_chunks == (original_chunk,)
    assert get_retrieval_acl_audit_events() == []


def test_adapter_filters_mixed_onyx_like_chunks() -> None:
    allowed_chunk = _chunk()
    group_allowed_chunk = _chunk(
        chunk_id="chunk-group",
        document_id="doc-group",
        allowed_subject_ids=[],
        allowed_group_ids=["group-a"],
    )
    forbidden_chunk = _chunk(
        chunk_id="chunk-forbidden",
        document_id="doc-forbidden",
    )
    cross_tenant_chunk = _chunk(
        chunk_id="chunk-cross-tenant",
        document_id="doc-allowed",
        tenant_id="tenant-b",
    )

    result = enforce_retrieval_acl_on_onyx_like_chunks(
        context=_context(),
        chunks=[allowed_chunk, forbidden_chunk, group_allowed_chunk, cross_tenant_chunk],
        request_id="request-filtered",
    )

    assert result.decision.status == "filter"
    assert result.allowed_original_chunks == (allowed_chunk, group_allowed_chunk)
    assert {denial.reason for denial in result.decision.denials} == {
        RetrievalACLReason.UNAUTHORIZED_DOCUMENT_ID,
        RetrievalACLReason.CROSS_TENANT_RESULT,
    }
    audit_events = get_retrieval_acl_audit_events()
    assert len(audit_events) == 1
    assert audit_events[0].request_id == "request-filtered"
    assert audit_events[0].status == "filter"
    assert audit_events[0].denied_count == 2


def test_adapter_fails_closed_for_missing_acl_metadata() -> None:
    missing_metadata_chunk = _chunk(allowed_subject_ids=None)

    result = enforce_retrieval_acl_on_onyx_like_chunks(
        context=_context(),
        chunks=[missing_metadata_chunk],
    )

    assert result.decision.status == "deny"
    assert result.allowed_original_chunks == ()
    assert result.decision.denials[0].reason == RetrievalACLReason.MALFORMED_ACL_CONTEXT


def test_adapter_fails_closed_for_missing_request_context() -> None:
    result = enforce_retrieval_acl_on_onyx_like_chunks(
        context=None,
        chunks=[_chunk()],
    )

    assert result.decision.status == "deny"
    assert result.allowed_original_chunks == ()
    assert result.decision.denials[0].reason == RetrievalACLReason.MISSING_ACL_CONTEXT


def test_adapter_denies_document_acl_subject_group_mismatch() -> None:
    forbidden_chunk = _chunk(
        chunk_id="chunk-forbidden",
        document_id="doc-group",
        allowed_subject_ids=["user-b"],
        allowed_group_ids=["group-b"],
    )

    result = enforce_retrieval_acl_on_onyx_like_chunks(
        context=_context(),
        chunks=[forbidden_chunk],
    )

    assert result.decision.status == "deny"
    assert result.allowed_original_chunks == ()
    assert result.decision.denials[0].reason == RetrievalACLReason.DOCUMENT_ACL_MISMATCH
