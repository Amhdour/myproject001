from __future__ import annotations

from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.enforcer import enforce_retrieval_acl
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLReason
from backend.security_layer.retrieval_acl.models import RetrievalDocumentACL
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
    chunk_id: str = "chunk-allowed",
    document_id: str = "doc-allowed",
    tenant_id: str = "tenant-a",
    allowed_subject_ids: frozenset[str] = frozenset({"user-a"}),
    allowed_group_ids: frozenset[str] = frozenset(),
) -> RetrievalResultChunk:
    return RetrievalResultChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        tenant_id=tenant_id,
        document_acl=RetrievalDocumentACL(
            tenant_id=tenant_id,
            document_id=document_id,
            allowed_subject_ids=allowed_subject_ids,
            allowed_group_ids=allowed_group_ids,
        ),
    )


def setup_function() -> None:
    clear_retrieval_acl_audit_events()


def test_allowed_same_tenant_document_passes() -> None:
    allowed_chunk = _chunk()

    decision = enforce_retrieval_acl(context=_context(), chunks=[allowed_chunk])

    assert decision.status == "allow"
    assert decision.allowed_chunks == (allowed_chunk,)
    assert decision.denials == ()
    assert get_retrieval_acl_audit_events() == []


def test_forbidden_same_tenant_document_denied() -> None:
    forbidden_chunk = _chunk(
        chunk_id="chunk-forbidden",
        document_id="doc-group",
        allowed_subject_ids=frozenset({"user-b"}),
        allowed_group_ids=frozenset({"group-b"}),
    )

    decision = enforce_retrieval_acl(context=_context(), chunks=[forbidden_chunk])

    assert decision.status == "deny"
    assert decision.allowed_chunks == ()
    assert decision.denials[0].reason == RetrievalACLReason.DOCUMENT_ACL_MISMATCH


def test_cross_tenant_document_denied() -> None:
    cross_tenant_chunk = _chunk(
        chunk_id="chunk-cross-tenant",
        document_id="doc-allowed",
        tenant_id="tenant-b",
    )

    decision = enforce_retrieval_acl(context=_context(), chunks=[cross_tenant_chunk])

    assert decision.status == "deny"
    assert decision.allowed_chunks == ()
    assert decision.denials[0].reason == RetrievalACLReason.CROSS_TENANT_RESULT


def test_mixed_retrieval_results_filtered() -> None:
    allowed_chunk = _chunk()
    group_allowed_chunk = _chunk(
        chunk_id="chunk-group",
        document_id="doc-group",
        allowed_subject_ids=frozenset(),
        allowed_group_ids=frozenset({"group-a"}),
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

    decision = enforce_retrieval_acl(
        context=_context(),
        chunks=[allowed_chunk, forbidden_chunk, group_allowed_chunk, cross_tenant_chunk],
    )

    assert decision.status == "filter"
    assert decision.allowed_chunks == (allowed_chunk, group_allowed_chunk)
    assert {denial.reason for denial in decision.denials} == {
        RetrievalACLReason.UNAUTHORIZED_DOCUMENT_ID,
        RetrievalACLReason.CROSS_TENANT_RESULT,
    }


def test_missing_acl_context_denies() -> None:
    decision = enforce_retrieval_acl(context=None, chunks=[_chunk()])

    assert decision.status == "deny"
    assert decision.allowed_chunks == ()
    assert decision.denials[0].reason == RetrievalACLReason.MISSING_ACL_CONTEXT


def test_malformed_acl_context_denies() -> None:
    malformed_context = RetrievalACLContext(
        tenant_id="",
        subject_id="user-a",
        allowed_document_ids=frozenset({"doc-allowed"}),
    )

    decision = enforce_retrieval_acl(context=malformed_context, chunks=[_chunk()])

    assert decision.status == "deny"
    assert decision.allowed_chunks == ()
    assert decision.denials[0].reason == RetrievalACLReason.MALFORMED_ACL_CONTEXT


def test_denial_creates_audit_event() -> None:
    forbidden_chunk = _chunk(
        chunk_id="chunk-forbidden",
        document_id="doc-forbidden",
    )

    decision = enforce_retrieval_acl(
        context=_context(),
        chunks=[forbidden_chunk],
        request_id="request-denied",
    )

    audit_events = get_retrieval_acl_audit_events()
    assert decision.status == "deny"
    assert len(audit_events) == 1
    assert audit_events[0].request_id == "request-denied"
    assert audit_events[0].status == "deny"
    assert audit_events[0].denied_count == 1
    assert audit_events[0].denied_document_ids == ("doc-forbidden",)
    assert audit_events[0].reasons == (RetrievalACLReason.UNAUTHORIZED_DOCUMENT_ID.value,)
