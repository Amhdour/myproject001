from __future__ import annotations

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.search_pipeline_gate import (
    apply_retrieval_acl_search_pipeline_gate,
)
from backend.security_layer.retrieval_acl.telemetry import (
    build_retrieval_acl_decision_telemetry_record,
)
from backend.security_layer.retrieval_acl.telemetry import (
    render_retrieval_acl_telemetry_evidence,
)
from backend.security_layer.retrieval_acl.telemetry import (
    summarize_retrieval_acl_audit_events,
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


def setup_function() -> None:
    clear_retrieval_acl_audit_events()


def test_decision_telemetry_record_includes_denied_counts_and_boundaries() -> None:
    result = apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=[
            _chunk(),
            _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden"),
        ],
        request_id="request-record",
        mode="enforce",
    )
    assert result.shadow_result is not None

    record = build_retrieval_acl_decision_telemetry_record(
        request_id="request-record",
        decision=result.shadow_result.decision,
    )

    assert record.request_id == "request-record"
    assert record.status == "filter"
    assert record.allowed_count == 1
    assert record.denied_count == 1
    assert record.denied_document_ids == ("doc-forbidden",)
    assert record.denied_reasons == ("unauthorized_document_id",)
    assert record.production_readiness == "NO-GO"
    assert record.enterprise_readiness == "NO-GO"
    assert record.live_enforcement_claimed is False


def test_audit_event_summary_counts_filter_and_deny_decisions() -> None:
    apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=[
            _chunk(),
            _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden"),
        ],
        request_id="request-filter",
        mode="enforce",
    )
    apply_retrieval_acl_search_pipeline_gate(
        context=None,
        retrieved_chunks=[_chunk(chunk_id="chunk-missing-context")],
        request_id="request-deny",
        mode="enforce",
    )

    summary = summarize_retrieval_acl_audit_events(get_retrieval_acl_audit_events())

    assert summary.total_decisions == 2
    assert summary.allow_count == 0
    assert summary.filter_count == 1
    assert summary.deny_count == 1
    assert summary.denied_chunk_count == 2
    assert summary.denied_document_ids == ("doc-forbidden", "doc-allowed")
    assert summary.denial_reason_counts == {
        "missing_acl_context": 1,
        "unauthorized_document_id": 1,
    }
    assert summary.request_ids == ("request-filter", "request-deny")
    assert summary.production_readiness == "NO-GO"
    assert summary.enterprise_readiness == "NO-GO"
    assert summary.live_enforcement_claimed is False


def test_telemetry_evidence_rendering_is_deterministic_and_claim_bounded() -> None:
    apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=[
            _chunk(),
            _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden"),
        ],
        request_id="request-filter",
        mode="enforce",
    )

    summary = summarize_retrieval_acl_audit_events(get_retrieval_acl_audit_events())
    rendered = render_retrieval_acl_telemetry_evidence(summary)

    assert "retrieval_acl_telemetry_summary" in rendered
    assert "total_decisions=1" in rendered
    assert "filter_count=1" in rendered
    assert "denied_chunk_count=1" in rendered
    assert "denied_document_ids=doc-forbidden" in rendered
    assert "denial_reason_counts=unauthorized_document_id:1" in rendered
    assert "request_ids=request-filter" in rendered
    assert "production_readiness=NO-GO" in rendered
    assert "enterprise_readiness=NO-GO" in rendered
    assert "live_enforcement_claimed=false" in rendered


def test_empty_audit_summary_is_safe_and_bounded() -> None:
    summary = summarize_retrieval_acl_audit_events([])

    assert summary.total_decisions == 0
    assert summary.allow_count == 0
    assert summary.deny_count == 0
    assert summary.filter_count == 0
    assert summary.denied_chunk_count == 0
    assert summary.denied_document_ids == ()
    assert summary.denial_reason_counts == {}
    assert summary.request_ids == ()
    assert render_retrieval_acl_telemetry_evidence(summary).endswith(
        "live_enforcement_claimed=false\n"
    )
