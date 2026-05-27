from datetime import UTC, datetime, timedelta

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.vector.metadata_contract import build_safe_vector_metadata
from backend.security_layer.vector.models import (
    VectorCandidate,
    VectorDecisionStatus,
    VectorMetadata,
    VectorNamespace,
    VectorOperationType,
    VectorSecurityContext,
    VectorSecurityStage,
)
from backend.security_layer.vector.validators import (
    build_vector_decision,
    filter_authorized_vector_candidates,
    validate_vector_acl_snapshot,
    validate_vector_candidate,
    validate_vector_context,
    validate_vector_namespace_authorization,
)


def _context() -> VectorSecurityContext:
    return VectorSecurityContext(
        request_id="r",
        operation_type=VectorOperationType.QUERY,
        stage=VectorSecurityStage.CANDIDATE_METADATA_CHECKED,
        tenant_id_hash_or_safe_id="tenant",
        workspace_id_hash_or_safe_id="workspace",
        subject_id_hash_or_safe_id="subject",
        namespace=VectorNamespace(name="ns"),
        authorized_namespaces=("ns",),
    )


def _metadata(**overrides: object) -> VectorMetadata:
    now = datetime.now(UTC)
    base = build_safe_vector_metadata(
        tenant_id_hash_or_safe_id="tenant",
        workspace_id_hash_or_safe_id="workspace",
        document_id_hash_or_safe_id="doc",
        chunk_id_hash_or_safe_id="chunk",
        source_type="connector",
        source_id_hash_or_safe_id="source",
        acl_snapshot_id="acl",
        acl_snapshot_version="1",
        acl_snapshot_created_at=now.isoformat(),
        acl_snapshot_expires_at=(now + timedelta(hours=1)).isoformat(),
        document_deleted=False,
        document_stale=False,
        provenance_id="prov",
        ingestion_run_id="ing",
        embedding_model_id="model",
        embedding_created_at=now.isoformat(),
        content_type="text/plain",
        sensitivity_label_placeholder="internal",
        prompt_injection_flag=False,
        poisoning_flag=False,
    )
    base.update(overrides)
    return VectorMetadata(values=base)


def test_context_and_namespace_authorization_validation() -> None:
    assert validate_vector_context(_context())
    no_tenant = VectorSecurityContext(**(_context().__dict__ | {"tenant_id_hash_or_safe_id": None}))
    no_subject = VectorSecurityContext(**(_context().__dict__ | {"subject_id_hash_or_safe_id": None}))
    assert not validate_vector_context(no_tenant)
    assert not validate_vector_context(no_subject)
    assert validate_vector_namespace_authorization(_context(), "ns")
    assert not validate_vector_namespace_authorization(_context(), "other")


def test_acl_snapshot_missing_or_stale_denied() -> None:
    assert validate_vector_acl_snapshot(_metadata().values)
    missing = _metadata(acl_snapshot_id="")
    assert not validate_vector_acl_snapshot(missing.values)
    stale = _metadata(acl_snapshot_expires_at=(datetime.now(UTC) - timedelta(minutes=5)).isoformat())
    assert not validate_vector_acl_snapshot(stale.values)


def test_candidate_validation_for_namespace_metadata_acl_provenance() -> None:
    ctx = _context()
    valid = VectorCandidate("ok", VectorNamespace("ns"), _metadata())
    wrong_namespace = VectorCandidate("bad_ns", VectorNamespace("other"), _metadata())
    missing_provenance = VectorCandidate("bad_prov", VectorNamespace("ns"), _metadata(provenance_id=""))
    assert validate_vector_candidate(ctx, valid)
    assert not validate_vector_candidate(ctx, wrong_namespace)
    assert not validate_vector_candidate(ctx, missing_provenance)


def test_filter_authorized_candidates_and_all_required_flags() -> None:
    ctx = _context()
    good = VectorCandidate("good", VectorNamespace("ns"), _metadata())
    deleted = VectorCandidate("deleted", VectorNamespace("ns"), _metadata(document_deleted=True))
    stale = VectorCandidate("stale", VectorNamespace("ns"), _metadata(document_stale=True))
    prompt_inj = VectorCandidate("inj", VectorNamespace("ns"), _metadata(prompt_injection_flag=True))
    poisoned = VectorCandidate("poison", VectorNamespace("ns"), _metadata(poisoning_flag=True))
    ns_mismatch = VectorCandidate("ns", VectorNamespace("other"), _metadata())
    missing_acl = VectorCandidate("acl", VectorNamespace("ns"), _metadata(acl_snapshot_id=""))
    missing_prov = VectorCandidate("prov", VectorNamespace("ns"), _metadata(provenance_id=""))

    allowed, denied, flags = filter_authorized_vector_candidates(
        ctx, [good, deleted, stale, prompt_inj, poisoned, ns_mismatch, missing_acl, missing_prov]
    )
    assert {c.candidate_id for c in allowed} == {"good", "inj", "poison"}
    assert set(denied) == {"deleted", "stale", "ns", "acl", "prov"}
    assert "deleted_or_stale" in flags
    assert "prompt_injection_marker" in flags
    assert "poisoning_marker" in flags


def test_decisions_redact_raw_text_and_secrets() -> None:
    decision = build_vector_decision(
        context=_context(),
        status=VectorDecisionStatus.DENY,
        reason="raw text token=abc api_key=xyz credential=bad",
        denial_category=DenialCategory.VALIDATION_FAILED,
    )
    assert decision.denial_category == DenialCategory.VALIDATION_FAILED
    assert "raw" not in decision.reason.lower() or "[redacted]" in decision.reason
