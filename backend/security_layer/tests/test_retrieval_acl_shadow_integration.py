from __future__ import annotations

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.integration_config import RetrievalACLIntegrationConfig
from backend.security_layer.retrieval_acl.integration_config import get_retrieval_acl_integration_config
from backend.security_layer.retrieval_acl.integration_config import parse_retrieval_acl_integration_mode
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.shadow_integration import apply_retrieval_acl_shadow_integration


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


def test_missing_env_defaults_to_off() -> None:
    config = get_retrieval_acl_integration_config(env={})

    assert config.mode == "off"
    assert config.production_readiness == "NO-GO"
    assert config.enterprise_readiness == "NO-GO"
    assert config.live_enforcement_claimed is False


def test_invalid_env_defaults_to_off() -> None:
    assert parse_retrieval_acl_integration_mode("invalid") == "off"
    assert parse_retrieval_acl_integration_mode("") == "off"
    assert parse_retrieval_acl_integration_mode(None) == "off"


def test_off_mode_preserves_chunks_and_records_no_acl_decision() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_shadow_integration(
        context=_context(),
        retrieved_chunks=chunks,
        env={},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks == chunks
    assert result.gate_result.shadow_result is None
    assert result.gate_result.downstream_document_ids == (
        "doc-allowed",
        "doc-forbidden",
        "doc-group",
    )
    assert get_retrieval_acl_audit_events() == []


def test_shadow_mode_preserves_chunks_and_records_would_filter_evidence() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_shadow_integration(
        context=_context(),
        retrieved_chunks=chunks,
        request_id="request-shadow-integration",
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    assert result.config.mode == "shadow"
    assert result.returned_chunks == chunks
    assert result.gate_result.shadow_result is not None
    assert result.gate_result.shadow_result.decision.status == "filter"
    assert result.gate_result.shadow_result.would_return_chunks == (chunks[0], chunks[2])
    assert result.gate_result.shadow_result.evidence.returned_chunk_count == 3
    assert result.gate_result.shadow_result.evidence.would_return_chunk_count == 2
    assert len(get_retrieval_acl_audit_events()) == 1


def test_explicit_config_can_select_shadow_mode() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_shadow_integration(
        context=_context(),
        retrieved_chunks=chunks,
        config=RetrievalACLIntegrationConfig(mode="shadow"),
    )

    assert result.config.mode == "shadow"
    assert result.returned_chunks == chunks
    assert result.gate_result.shadow_result is not None
    assert result.gate_result.shadow_result.would_return_chunks == (chunks[0], chunks[2])


def test_explicit_enforce_mode_filters_with_isolated_gate_only() -> None:
    chunks = _mixed_chunks()

    result = apply_retrieval_acl_shadow_integration(
        context=_context(),
        retrieved_chunks=chunks,
        request_id="request-enforce-integration",
        env={INTEGRATION_MODE_ENV_VAR: "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == (chunks[0], chunks[2])
    assert result.gate_result.downstream_document_ids == ("doc-allowed", "doc-group")
    assert result.gate_result.shadow_result is not None
    assert result.gate_result.shadow_result.decision.status == "filter"
