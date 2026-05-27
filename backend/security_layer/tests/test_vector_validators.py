from datetime import UTC, datetime, timedelta

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.vector.metadata_contract import build_safe_vector_metadata
from backend.security_layer.vector.models import VectorCandidate, VectorDecisionStatus, VectorMetadata, VectorNamespace, VectorOperationType, VectorSecurityContext, VectorSecurityStage
from backend.security_layer.vector.validators import build_vector_decision, filter_authorized_vector_candidates


def _context() -> VectorSecurityContext:
    return VectorSecurityContext(
        request_id="r",
        operation_type=VectorOperationType.QUERY,
        stage=VectorSecurityStage.CANDIDATE_METADATA_CHECKED,
        tenant_id_hash_or_safe_id="t",
        workspace_id_hash_or_safe_id="w",
        subject_id_hash_or_safe_id="s",
        namespace=VectorNamespace(name="ns"),
        authorized_namespaces=("ns",),
    )


def _metadata(**overrides: object) -> VectorMetadata:
    now = datetime.now(UTC)
    base = build_safe_vector_metadata(
        tenant_id_hash_or_safe_id="t", workspace_id_hash_or_safe_id="w", document_id_hash_or_safe_id="d", chunk_id_hash_or_safe_id="c", source_type="connector", source_id_hash_or_safe_id="src", acl_snapshot_id="a", acl_snapshot_version="1", acl_snapshot_created_at=now.isoformat(), acl_snapshot_expires_at=(now + timedelta(hours=1)).isoformat(), document_deleted=False, document_stale=False, provenance_id="p", ingestion_run_id="i", embedding_model_id="m", embedding_created_at=now.isoformat(), content_type="text/plain", sensitivity_label_placeholder="internal", prompt_injection_flag=False, poisoning_flag=False
    )
    base.update(overrides)
    return VectorMetadata(values=base)


def test_filter_and_flags() -> None:
    ctx = _context()
    good = VectorCandidate("1", VectorNamespace("ns"), _metadata())
    deleted = VectorCandidate("2", VectorNamespace("ns"), _metadata(document_deleted=True))
    inj = VectorCandidate("3", VectorNamespace("ns"), _metadata(prompt_injection_flag=True, poisoning_flag=True))
    ns = VectorCandidate("4", VectorNamespace("other"), _metadata())
    allowed, denied, flags = filter_authorized_vector_candidates(ctx, [good, deleted, inj, ns])
    assert [c.candidate_id for c in allowed] == ["1", "3"]
    assert set(denied) == {"2", "4"}
    assert "deleted_or_stale" in flags and "prompt_injection_marker" in flags and "poisoning_marker" in flags


def test_build_decision_uses_safe_denial_category() -> None:
    d = build_vector_decision(context=_context(), status=VectorDecisionStatus.DENY, reason="raw text", denial_category=DenialCategory.VALIDATION_FAILED)
    assert d.denial_category == DenialCategory.VALIDATION_FAILED
    assert "[redacted]" in d.reason
