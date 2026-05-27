from datetime import datetime

from backend.security_layer.retrieval import controls
from backend.security_layer.retrieval.models import ACLSnapshot, RetrievalACLContext, RetrievalCandidate, RetrievalChunk, RetrievalDecisionStatus, RetrievalDocument, RetrievalSourceType, RetrievalStage, RetrievalSubject, RetrievalTenant, VectorMetadata, VectorNamespace
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics


def _ctx(stage: RetrievalStage = RetrievalStage.DOCUMENT_ACL_CHECKED) -> RetrievalACLContext:
    return RetrievalACLContext(
        subject=RetrievalSubject(subject_id="u1", group_ids=("g1",), role_ids=("r1",)),
        tenant=RetrievalTenant(tenant_id="t1"),
        stage=stage,
        source_type=RetrievalSourceType.HYBRID,
        request_id="req-1",
        retrieval_scope=("kb",),
        acl_snapshot=ACLSnapshot(captured_at=datetime.utcnow(), acl_entries_count=1, is_stale=False),
        expected_vector_namespace="tenant:t1",
        cache_acl_context_key="t1:u1",
    )


def _cand() -> RetrievalCandidate:
    return RetrievalCandidate(
        candidate_id="c1", source_type=RetrievalSourceType.VECTOR,
        document=RetrievalDocument("d1", "t1", ("u1",), ("g1",), ("r1",), False),
        chunk=RetrievalChunk("ch1", "d1", "t1", ("u1",), ("g1",), ("r1",)),
        vector_namespace=VectorNamespace("tenant:t1"), vector_metadata=VectorMetadata("t1", "d1", "ch1"), provenance_id="p1",
    )


def test_denials_and_filters_and_placeholders() -> None:
    cand = _cand()
    assert controls.authorize_query_received(RetrievalACLContext(**{**_ctx().__dict__, "tenant": RetrievalTenant(None)})).denial_category == DenialCategory.TENANT_CONTEXT_MISSING
    assert controls.authorize_query_received(RetrievalACLContext(**{**_ctx().__dict__, "subject": RetrievalSubject(None)})).denial_category == DenialCategory.SUBJECT_CONTEXT_MISSING
    assert controls.authorize_retrieval_scope_resolved(RetrievalACLContext(**{**_ctx(RetrievalStage.RETRIEVAL_SCOPE_RESOLVED).__dict__, "retrieval_scope": ()})).status == RetrievalDecisionStatus.DENY

    cross_tenant_doc = RetrievalCandidate(**{**cand.__dict__, "candidate_id": "c2", "document": RetrievalDocument("d1", "t2", ("u1",), (), (), False)})
    cross_tenant_chunk = RetrievalCandidate(**{**cand.__dict__, "chunk": RetrievalChunk("ch1", "d1", "t2", ("u1",), (), ())})
    unauthorized_group = RetrievalCandidate(**{**cand.__dict__, "document": RetrievalDocument("d1", "t1", (), ("other",), (), False)})
    unauthorized_role = RetrievalCandidate(**{**cand.__dict__, "document": RetrievalDocument("d1", "t1", (), (), ("other",), False)})
    stale = controls.authorize_document_acl_checked(RetrievalACLContext(**{**_ctx().__dict__, "acl_snapshot": ACLSnapshot(datetime.utcnow(), 1, True)}), [cand])
    deleted = controls.authorize_document_acl_checked(_ctx(), [RetrievalCandidate(**{**cand.__dict__, "document": RetrievalDocument("d1", "t1", ("u1",), (), (), True)})])
    ns_bad = controls.authorize_vector_namespace_checked(_ctx(), [RetrievalCandidate(**{**cand.__dict__, "vector_namespace": VectorNamespace("tenant:t2")})])
    md_bad = controls.authorize_vector_metadata_checked(_ctx(), [RetrievalCandidate(**{**cand.__dict__, "vector_metadata": VectorMetadata("t2", "d1", "ch1")})])

    for d in [
        controls.authorize_document_acl_checked(_ctx(), [cross_tenant_doc]),
        controls.authorize_chunk_acl_checked(_ctx(), [cross_tenant_chunk]),
        controls.authorize_document_acl_checked(_ctx(), [unauthorized_group]),
        controls.authorize_document_acl_checked(_ctx(), [unauthorized_role]),
        stale, deleted, ns_bad, md_bad,
    ]:
        assert d.status in {RetrievalDecisionStatus.DENY, RetrievalDecisionStatus.FILTER}
        assert d.denial_category is not None

    filtered = controls.authorize_hybrid_search_filtered(_ctx(RetrievalStage.HYBRID_SEARCH_FILTERED), [cand, cross_tenant_doc])
    assert filtered.allowed_candidates == (cand,)
    assert "c2" in filtered.denied_candidate_ids
    assert controls.authorize_rerank_candidates_filtered(_ctx(RetrievalStage.RERANK_CANDIDATES_FILTERED), [cross_tenant_doc]).allowed_candidates == ()
    assert controls.authorize_citation_sources_filtered(_ctx(RetrievalStage.CITATION_SOURCES_FILTERED), [cross_tenant_doc]).allowed_candidates == ()
    assert controls.authorize_context_chunks_authorized(_ctx(RetrievalStage.CONTEXT_CHUNKS_AUTHORIZED), [cand]).allowed_candidates == (cand,)
    assert controls.authorize_prompt_context_authorized(_ctx(RetrievalStage.PROMPT_CONTEXT_AUTHORIZED), [cand]).allowed_candidates == (cand,)

    cache_deny = controls.authorize_cache_read_authorized(RetrievalACLContext(**{**_ctx(RetrievalStage.CACHE_READ_AUTHORIZED).__dict__, "cache_acl_context_key": "bad"}))
    assert cache_deny.status == RetrievalDecisionStatus.DENY
    assert controls.authorize_cache_read_authorized(_ctx(RetrievalStage.CACHE_READ_AUTHORIZED)).status == RetrievalDecisionStatus.ALLOW


def test_audit_finding_metric_and_safety() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    cand = _cand()
    controls.authorize_retrieval_audit_written(_ctx(RetrievalStage.RETRIEVAL_AUDIT_WRITTEN))
    controls.authorize_document_acl_checked(_ctx(), [RetrievalCandidate(**{**cand.__dict__, "document": RetrievalDocument("d1", "t2", (), (), (), False)})])
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()
    d = controls.authorize_prompt_context_authorized(_ctx(RetrievalStage.PROMPT_CONTEXT_AUTHORIZED), [cand])
    assert "text" not in d.reason
    assert "fastapi" not in controls.__dict__ and "celery" not in controls.__dict__
