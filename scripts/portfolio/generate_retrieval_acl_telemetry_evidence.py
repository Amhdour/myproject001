from __future__ import annotations

from pathlib import Path

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.search_pipeline_gate import (
    apply_retrieval_acl_search_pipeline_gate,
)
from backend.security_layer.retrieval_acl.telemetry import (
    render_retrieval_acl_telemetry_evidence,
)
from backend.security_layer.retrieval_acl.telemetry import (
    summarize_retrieval_acl_audit_events,
)


ARTIFACT_DIR = Path("retrieval-acl-telemetry-artifacts")


def _context() -> RetrievalACLContext:
    return RetrievalACLContext(
        tenant_id="tenant-a",
        subject_id="user-a",
        group_ids=frozenset({"group-a"}),
        allowed_document_ids=frozenset({"doc-allowed", "doc-group"}),
    )


def _chunk(
    *,
    chunk_id: str,
    document_id: str,
    tenant_id: str = "tenant-a",
    allowed_subject_ids: list[str] | None = None,
    allowed_group_ids: list[str] | None = None,
) -> OnyxLikeRetrievalChunk:
    metadata: dict[str, object] = {"tenant_id": tenant_id}
    metadata["allowed_subject_ids"] = allowed_subject_ids or ["user-a"]
    if allowed_group_ids is not None:
        metadata["allowed_group_ids"] = allowed_group_ids
    return OnyxLikeRetrievalChunk(
        chunk_id=chunk_id,
        document_id=document_id,
        metadata=metadata,
    )


def main() -> None:
    clear_retrieval_acl_audit_events()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    apply_retrieval_acl_search_pipeline_gate(
        context=_context(),
        retrieved_chunks=[
            _chunk(chunk_id="chunk-allowed", document_id="doc-allowed"),
            _chunk(chunk_id="chunk-forbidden", document_id="doc-forbidden"),
        ],
        request_id="evidence-filter",
        mode="enforce",
    )
    apply_retrieval_acl_search_pipeline_gate(
        context=None,
        retrieved_chunks=[_chunk(chunk_id="chunk-missing-context", document_id="doc-allowed")],
        request_id="evidence-deny",
        mode="enforce",
    )

    summary = summarize_retrieval_acl_audit_events(get_retrieval_acl_audit_events())
    (ARTIFACT_DIR / "telemetry_summary.txt").write_text(
        render_retrieval_acl_telemetry_evidence(summary),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
