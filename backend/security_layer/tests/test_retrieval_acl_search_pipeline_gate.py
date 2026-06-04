from __future__ import annotations

import pytest

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLReason
from backend.security_layer.retrieval_acl.search_pipeline_gate import (
    apply_retrieval_acl_search_pipeline_gate,
)


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


def _mixed_chunks() -> tuple[OnyxLikeRetrievalChunk, ...]:
    return (
        _chunk(),
        _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden"),
        _chunk(
            chunk_id="chunk-group",
            document_id="doc-group",
            allowed_subject_ids=[],
            allowed_group_ids=["group-a"],
        ),
        _chunk(
            chunk_id="chunk-cross-tenant",
            document_id="doc-allowed",
            tenant_id="tenant-b",
        ),
    )


def setup_function() -> None:
    clear_retrieval_acl_audit_events()


def test_gate_off_returns_all_chunks_and_records_no_acl_decision() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=chunks,
        mode="off",
    )

    assert result.mode == "off"
    assert result.returned_chunks == chunks
    assert result.shadow_result is None
    assert result.downstream_document_ids == (
        "doc-allowed",
        "doc-forbidden",
        "doc-group",
        "doc-allowed",
    )
    assert get_retrieval_acl_audit_events() == []


def test_gate_shadow_records_would_filter_but_preserves_downstream_chunks() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=chunks,
        request_id="request-gate-shadow",
        mode="shadow",
    )

    assert result.mode == "shadow"
    assert result.returned_chunks == chunks
    assert result.downstream_document_ids == (
        "doc-allowed",
        "doc-forbidden",
        "doc-group",
        "doc-allowed",
    )
    assert result.shadow_result is not None
    assert result.shadow_result.decision.status == "filter"
    assert result.shadow_result.would_return_chunks == (chunks[0], chunks[2])
    assert result.shadow_result.evidence.returned_chunk_count == 4
    assert result.shadow_result.evidence.would_return_chunk_count == 2
    assert result.production_readiness == "NO-GO"
    assert result.enterprise_readiness == "NO-GO"
    assert result.live_integration_claimed is False

    audit_events = get_retrieval_acl_audit_events()
    assert len(audit_events) == 1
    assert audit_events[0].request_id == "request-gate-shadow"
    assert audit_events[0].status == "filter"


def test_gate_enforce_filters_before_simulated_downstream_surfaces() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=chunks,
        request_id="request-gate-enforce",
        mode="enforce",
    )

    assert result.mode == "enforce"
    assert result.returned_chunks == (chunks[0], chunks[2])
    assert result.downstream_document_ids == ("doc-allowed", "doc-group")
    assert "doc-forbidden" not in result.downstream_document_ids
    assert result.shadow_result is not None
    assert result.shadow_result.decision.status == "filter"
    assert {denial.reason for denial in result.shadow_result.decision.denials} == {
        RetrievalACLReason.UNAUTHORIZED_DOCUMENT_ID,
        RetrievalACLReason.CROSS_TENANT_RESULT,
    }


def test_gate_enforce_denies_all_when_context_missing() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_search_pipeline_gate(
        context=None,
        retrieved_chunks=chunks,
        request_id="request-gate-missing-context",
        mode="enforce",
    )

    assert result.mode == "enforce"
    assert result.returned_chunks == ()
    assert result.downstream_document_ids == ()
    assert result.shadow_result is not None
    assert result.shadow_result.decision.status == "deny"
    assert result.shadow_result.evidence.denied_count == len(chunks)
    assert set(result.shadow_result.evidence.denied_reasons) == {
        RetrievalACLReason.MISSING_ACL_CONTEXT.value,
    }


def test_gate_rejects_invalid_mode() -> None:
    with pytest.raises(ValueError):
        apply_retrieval_acl_search_pipeline_gate(
            context=_context(),
            retrieved_chunks=[_chunk()],
            mode="invalid",
        )
