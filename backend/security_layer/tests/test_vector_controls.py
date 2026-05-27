from datetime import UTC, datetime, timedelta

from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.vector.controls import (
    authorize_vector_acl_snapshot_attached,
    authorize_vector_audit_written,
    authorize_vector_candidate_metadata_checked,
    authorize_vector_finding_recorded_if_needed,
    authorize_vector_namespace_authorized,
    authorize_vector_provenance_attached,
    authorize_vector_query_context_validated,
    authorize_vector_write_context_validated,
)
from backend.security_layer.vector.metadata_contract import build_safe_vector_metadata
from backend.security_layer.vector.models import VectorCandidate, VectorDecisionStatus, VectorMetadata, VectorNamespace, VectorOperationType, VectorSecurityContext, VectorSecurityStage


def _ctx() -> VectorSecurityContext:
    return VectorSecurityContext("r", VectorOperationType.WRITE, VectorSecurityStage.WRITE_CONTEXT_VALIDATED, "t", "w", "s", VectorNamespace("ns"), ("ns",))


def _md(**kw: object) -> VectorMetadata:
    now = datetime.now(UTC)
    base = build_safe_vector_metadata(
        tenant_id_hash_or_safe_id="t", workspace_id_hash_or_safe_id="w", document_id_hash_or_safe_id="d", chunk_id_hash_or_safe_id="c", source_type="connector", source_id_hash_or_safe_id="src", acl_snapshot_id="a", acl_snapshot_version="1", acl_snapshot_created_at=now.isoformat(), acl_snapshot_expires_at=(now + timedelta(hours=1)).isoformat(), document_deleted=False, document_stale=False, provenance_id="p", ingestion_run_id="i", embedding_model_id="m", embedding_created_at=now.isoformat(), content_type="text/plain", sensitivity_label_placeholder="internal", prompt_injection_flag=False, poisoning_flag=False
    )
    base.update(kw)
    return VectorMetadata(base)


def test_denials_and_isolated_emissions() -> None:
    deny_tenant = authorize_vector_write_context_validated(VectorSecurityContext("r", VectorOperationType.WRITE, VectorSecurityStage.WRITE_CONTEXT_VALIDATED, None, "w", "s", VectorNamespace("ns"), ("ns",)))
    assert deny_tenant.status == VectorDecisionStatus.DENY
    deny_subject = authorize_vector_query_context_validated(VectorSecurityContext("r", VectorOperationType.QUERY, VectorSecurityStage.QUERY_CONTEXT_VALIDATED, "t", "w", None, VectorNamespace("ns"), ("ns",)))
    assert deny_subject.status == VectorDecisionStatus.DENY
    deny_ns = authorize_vector_namespace_authorized(VectorSecurityContext("r", VectorOperationType.WRITE, VectorSecurityStage.NAMESPACE_AUTHORIZED, "t", "w", "s", VectorNamespace("bad"), ("ns",)))
    assert deny_ns.status == VectorDecisionStatus.DENY


def test_acl_provenance_candidate_audit_finding_metric() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    ctx = _ctx()
    bad_acl_ctx = VectorSecurityContext(**(ctx.__dict__ | {"metadata": _md(acl_snapshot_expires_at=(datetime.now(UTC)-timedelta(hours=1)).isoformat())}))
    assert authorize_vector_acl_snapshot_attached(bad_acl_ctx).status == VectorDecisionStatus.DENY
    bad_prov_ctx = VectorSecurityContext(**(ctx.__dict__ | {"metadata": _md(provenance_id="")}))
    assert authorize_vector_provenance_attached(bad_prov_ctx).status == VectorDecisionStatus.DENY
    candidates = [VectorCandidate("c1", VectorNamespace("ns"), _md(document_stale=True))]
    dec = authorize_vector_candidate_metadata_checked(VectorSecurityContext(**(ctx.__dict__ | {"stage": VectorSecurityStage.CANDIDATE_METADATA_CHECKED})), candidates)
    assert dec.status == VectorDecisionStatus.FILTER
    assert "deleted_or_stale" in dec.flags
    assert authorize_vector_audit_written(VectorSecurityContext(**(ctx.__dict__ | {"stage": VectorSecurityStage.AUDIT_WRITTEN}))).status == VectorDecisionStatus.ALLOW
    assert authorize_vector_finding_recorded_if_needed(VectorSecurityContext(**(ctx.__dict__ | {"stage": VectorSecurityStage.FINDING_RECORDED_IF_NEEDED}))).status == VectorDecisionStatus.FLAG
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()
