from __future__ import annotations

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.live_adjacent_seam import observe_retrieval_acl_live_adjacent_seam
from backend.security_layer.retrieval_acl.models import RetrievalACLContext


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
    )


def setup_function() -> None:
    clear_retrieval_acl_audit_events()


def test_live_adjacent_seam_defaults_off_and_preserves_chunks() -> None:
    chunks = _mixed_chunks()

    result = observe_retrieval_acl_live_adjacent_seam(
        seam_name="post_search_chunks_pre_llm_context",
        context=_context(),
        retrieved_chunks=chunks,
        env={},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks == chunks
    assert result.observation.behavior_changed is False
    assert result.observation.status == "observed_off_no_behavior_change"
    assert result.observation.observed_document_ids == (
        "doc-allowed",
        "doc-forbidden",
        "doc-group",
    )
    assert result.observation.returned_document_ids == (
        "doc-allowed",
        "doc-forbidden",
        "doc-group",
    )
    assert result.observation.live_integration_claimed is False
    assert result.observation.live_enforcement_claimed is False
    assert get_retrieval_acl_audit_events() == []


def test_live_adjacent_shadow_observes_would_filter_without_behavior_change() -> None:
    chunks = _mixed_chunks()

    result = observe_retrieval_acl_live_adjacent_seam(
        seam_name="post_search_chunks_pre_llm_context",
        context=_context(),
        retrieved_chunks=chunks,
        request_id="bundle-h-shadow-observation-test",
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    assert result.config.mode == "shadow"
    assert result.returned_chunks == chunks
    assert result.observation.behavior_changed is False
    assert result.observation.status == "observed_shadow_no_behavior_change"
    assert result.integration_result.gate_result.shadow_result is not None
    assert result.integration_result.gate_result.shadow_result.would_return_chunks == (
        chunks[0],
        chunks[2],
    )
    assert len(get_retrieval_acl_audit_events()) == 1


def test_live_adjacent_explicit_enforce_remains_isolated_and_records_change() -> None:
    chunks = _mixed_chunks()

    result = observe_retrieval_acl_live_adjacent_seam(
        seam_name="post_search_chunks_pre_llm_context",
        context=_context(),
        retrieved_chunks=chunks,
        request_id="bundle-h-enforce-observation-test",
        env={INTEGRATION_MODE_ENV_VAR: "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == (chunks[0], chunks[2])
    assert result.observation.behavior_changed is True
    assert result.observation.status == "observed_isolated_enforce_behavior"
    assert result.observation.returned_document_ids == ("doc-allowed", "doc-group")
    assert result.observation.production_readiness == "NO-GO"
    assert result.observation.enterprise_readiness == "NO-GO"
    assert result.observation.live_integration_claimed is False
    assert result.observation.live_enforcement_claimed is False


def test_live_adjacent_invalid_env_fails_safe_to_off() -> None:
    chunks = _mixed_chunks()

    result = observe_retrieval_acl_live_adjacent_seam(
        seam_name="post_search_chunks_pre_llm_context",
        context=_context(),
        retrieved_chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "invalid"},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks == chunks
    assert result.observation.behavior_changed is False
    assert result.observation.status == "observed_off_no_behavior_change"
    assert get_retrieval_acl_audit_events() == []
