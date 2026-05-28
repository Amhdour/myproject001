from datetime import UTC, datetime, timedelta

from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.vector import controls
from backend.security_layer.vector.metadata_contract import build_safe_vector_metadata
from backend.security_layer.vector.models import (
    VectorCandidate,
    VectorDecisionStatus,
    VectorEmbeddingMetadata,
    VectorMetadata,
    VectorNamespace,
    VectorOperationType,
    VectorSecurityContext,
    VectorSecurityStage,
)


def _ctx(stage: VectorSecurityStage, *, tenant: str | None = "t", subject: str | None = "s") -> VectorSecurityContext:
    return VectorSecurityContext("r", VectorOperationType.WRITE, stage, tenant, "w", subject, VectorNamespace("ns"), ("ns",))


def _md(**kw: object) -> VectorMetadata:
    now = datetime.now(UTC)
    base = build_safe_vector_metadata(
        tenant_id_hash_or_safe_id="t",
        workspace_id_hash_or_safe_id="w",
        document_id_hash_or_safe_id="d",
        chunk_id_hash_or_safe_id="c",
        source_type="connector",
        source_id_hash_or_safe_id="src",
        acl_snapshot_id="a",
        acl_snapshot_version="1",
        acl_snapshot_created_at=now.isoformat(),
        acl_snapshot_expires_at=(now + timedelta(hours=1)).isoformat(),
        document_deleted=False,
        document_stale=False,
        provenance_id="p",
        ingestion_run_id="i",
        embedding_model_id="m",
        embedding_created_at=now.isoformat(),
        content_type="text/plain",
        sensitivity_label_placeholder="internal",
        prompt_injection_flag=False,
        poisoning_flag=False,
    )
    base.update(kw)
    return VectorMetadata(base)


def test_all_18_stage_controls_exist_and_return_decisions() -> None:
    ctx_base = _ctx(VectorSecurityStage.WRITE_REQUESTED)
    candidates = [VectorCandidate("c1", VectorNamespace("ns"), _md())]

    stages_and_calls = [
        controls.authorize_vector_write_requested(ctx_base),
        controls.authorize_vector_write_context_validated(_ctx(VectorSecurityStage.WRITE_CONTEXT_VALIDATED)),
        controls.authorize_vector_namespace_resolved(_ctx(VectorSecurityStage.NAMESPACE_RESOLVED)),
        controls.authorize_vector_namespace_authorized(_ctx(VectorSecurityStage.NAMESPACE_AUTHORIZED)),
        controls.authorize_vector_metadata_validated(VectorSecurityContext(**(_ctx(VectorSecurityStage.METADATA_VALIDATED).__dict__ | {"metadata": _md()}))),
        controls.authorize_vector_acl_snapshot_attached(VectorSecurityContext(**(_ctx(VectorSecurityStage.ACL_SNAPSHOT_ATTACHED).__dict__ | {"metadata": _md()}))),
        controls.authorize_vector_provenance_attached(VectorSecurityContext(**(_ctx(VectorSecurityStage.PROVENANCE_ATTACHED).__dict__ | {"metadata": _md()}))),
        controls.authorize_vector_embedding_metadata_attached(VectorSecurityContext(**(_ctx(VectorSecurityStage.EMBEDDING_METADATA_ATTACHED).__dict__ | {"embedding_metadata": VectorEmbeddingMetadata("m", datetime.now(UTC), "text/plain", "internal")}))),
        controls.authorize_vector_write_committed(_ctx(VectorSecurityStage.WRITE_COMMITTED)),
        controls.authorize_vector_query_requested(_ctx(VectorSecurityStage.QUERY_REQUESTED)),
        controls.authorize_vector_query_context_validated(_ctx(VectorSecurityStage.QUERY_CONTEXT_VALIDATED)),
        controls.authorize_vector_search_filter_built(_ctx(VectorSecurityStage.SEARCH_FILTER_BUILT)),
        controls.authorize_vector_candidates_returned(_ctx(VectorSecurityStage.CANDIDATES_RETURNED), candidates),
        controls.authorize_vector_candidate_metadata_checked(_ctx(VectorSecurityStage.CANDIDATE_METADATA_CHECKED), candidates),
        controls.authorize_vector_deleted_or_stale_filtered(_ctx(VectorSecurityStage.DELETED_OR_STALE_FILTERED), candidates),
        controls.authorize_vector_cache_checked(_ctx(VectorSecurityStage.CACHE_CHECKED)),
        controls.authorize_vector_audit_written(_ctx(VectorSecurityStage.AUDIT_WRITTEN)),
        controls.authorize_vector_finding_recorded_if_needed(_ctx(VectorSecurityStage.FINDING_RECORDED_IF_NEEDED)),
    ]
    assert len(stages_and_calls) == 18
    assert all(call.stage for call in stages_and_calls)


def test_denials_for_missing_tenant_subject_namespace_acl_provenance() -> None:
    assert controls.authorize_vector_write_context_validated(_ctx(VectorSecurityStage.WRITE_CONTEXT_VALIDATED, tenant=None)).status == VectorDecisionStatus.DENY
    assert controls.authorize_vector_query_context_validated(_ctx(VectorSecurityStage.QUERY_CONTEXT_VALIDATED, subject=None)).status == VectorDecisionStatus.DENY
    bad_ns_ctx = VectorSecurityContext(**(_ctx(VectorSecurityStage.NAMESPACE_AUTHORIZED).__dict__ | {"namespace": VectorNamespace("bad")}))
    assert controls.authorize_vector_namespace_authorized(bad_ns_ctx).status == VectorDecisionStatus.DENY
    bad_acl_ctx = VectorSecurityContext(**(_ctx(VectorSecurityStage.ACL_SNAPSHOT_ATTACHED).__dict__ | {"metadata": _md(acl_snapshot_expires_at=(datetime.now(UTC)-timedelta(hours=1)).isoformat())}))
    assert controls.authorize_vector_acl_snapshot_attached(bad_acl_ctx).status == VectorDecisionStatus.DENY
    bad_prov_ctx = VectorSecurityContext(**(_ctx(VectorSecurityStage.PROVENANCE_ATTACHED).__dict__ | {"metadata": _md(provenance_id="")}))
    assert controls.authorize_vector_provenance_attached(bad_prov_ctx).status == VectorDecisionStatus.DENY


def test_candidate_filtering_and_in_memory_audit_finding_metric_only() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    candidates = [
        VectorCandidate("ok", VectorNamespace("ns"), _md()),
        VectorCandidate("deleted", VectorNamespace("ns"), _md(document_deleted=True)),
        VectorCandidate("stale", VectorNamespace("ns"), _md(document_stale=True)),
        VectorCandidate("inj", VectorNamespace("ns"), _md(prompt_injection_flag=True)),
        VectorCandidate("poison", VectorNamespace("ns"), _md(poisoning_flag=True)),
    ]
    decision = controls.authorize_vector_candidate_metadata_checked(_ctx(VectorSecurityStage.CANDIDATE_METADATA_CHECKED), candidates)
    assert decision.status == VectorDecisionStatus.FILTER
    assert set(decision.denied_candidate_ids) == {"deleted", "stale"}
    assert "prompt_injection_marker" in decision.flags
    assert "poisoning_marker" in decision.flags

    assert controls.authorize_vector_audit_written(_ctx(VectorSecurityStage.AUDIT_WRITTEN)).status == VectorDecisionStatus.ALLOW
    assert controls.authorize_vector_finding_recorded_if_needed(_ctx(VectorSecurityStage.FINDING_RECORDED_IF_NEEDED)).status == VectorDecisionStatus.FLAG
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()
