from __future__ import annotations

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.audit import clear_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.audit import get_retrieval_acl_audit_events
from backend.security_layer.retrieval_acl.enforce_harness import run_retrieval_acl_enforce_mode_harness
from backend.security_layer.retrieval_acl.enforce_harness import verify_retrieval_acl_rollback_to_off
from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
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


def test_enforce_harness_filters_unauthorized_chunks_in_isolation() -> None:
    result = run_retrieval_acl_enforce_mode_harness(
        context=_context(),
        retrieved_chunks=_mixed_chunks(),
        request_id="bundle-g-enforce-harness-test",
        env={INTEGRATION_MODE_ENV_VAR: "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.observed_document_ids == ("doc-allowed", "doc-forbidden", "doc-group")
    assert result.returned_document_ids == ("doc-allowed", "doc-group")
    assert result.denied_document_ids == ("doc-forbidden",)
    assert result.rollback_verification_status == "rollback_to_off_available"
    assert result.rollback_plan.rollback_value == "off"
    assert result.production_readiness == "NO-GO"
    assert result.enterprise_readiness == "NO-GO"
    assert result.live_integration_claimed is False
    assert len(get_retrieval_acl_audit_events()) == 1


def test_enforce_harness_off_mode_preserves_chunks_and_needs_no_rollback() -> None:
    chunks = _mixed_chunks()

    result = run_retrieval_acl_enforce_mode_harness(
        context=_context(),
        retrieved_chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "off"},
    )

    assert result.config.mode == "off"
    assert result.integration_result.returned_chunks == chunks
    assert result.returned_document_ids == ("doc-allowed", "doc-forbidden", "doc-group")
    assert result.denied_document_ids == ()
    assert result.rollback_verification_status == "not_required"
    assert get_retrieval_acl_audit_events() == []


def test_rollback_to_off_preserves_chunks_after_isolated_enforce_mode() -> None:
    chunks = _mixed_chunks()

    result = verify_retrieval_acl_rollback_to_off(
        context=_context(),
        retrieved_chunks=chunks,
        request_id="bundle-g-rollback-test",
    )

    assert result.before_rollback_result.config.mode == "enforce"
    assert result.before_rollback_result.returned_document_ids == ("doc-allowed", "doc-group")
    assert result.after_rollback_result.config.mode == "off"
    assert result.after_rollback_result.returned_chunks == chunks
    assert result.chunks_preserved_after_rollback is True
    assert result.rollback_verification_status == "rollback_verified_off_preserves_chunks"
    assert result.rollback_plan.rollback_command == "export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off"
    assert result.rollback_plan.live_rollback_claimed is False


def test_invalid_enforce_env_rolls_safe_to_off() -> None:
    chunks = _mixed_chunks()

    result = run_retrieval_acl_enforce_mode_harness(
        context=_context(),
        retrieved_chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "unexpected"},
    )

    assert result.config.mode == "off"
    assert result.integration_result.returned_chunks == chunks
    assert result.returned_document_ids == ("doc-allowed", "doc-forbidden", "doc-group")
    assert result.rollback_verification_status == "not_required"
    assert get_retrieval_acl_audit_events() == []
