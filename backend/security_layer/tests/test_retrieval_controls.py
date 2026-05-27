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


def test_all_17_stages_have_isolated_authorizers() -> None:
    context_by_stage = {
        RetrievalStage.QUERY_RECEIVED: lambda: controls.authorize_query_received(_ctx(RetrievalStage.QUERY_RECEIVED)),
        RetrievalStage.SUBJECT_CONTEXT_VALIDATED: lambda: controls.authorize_subject_context_validated(_ctx(RetrievalStage.SUBJECT_CONTEXT_VALIDATED)),
        RetrievalStage.TENANT_CONTEXT_VALIDATED: lambda: controls.authorize_tenant_context_validated(_ctx(RetrievalStage.TENANT_CONTEXT_VALIDATED)),
        RetrievalStage.RETRIEVAL_SCOPE_RESOLVED: lambda: controls.authorize_retrieval_scope_resolved(_ctx(RetrievalStage.RETRIEVAL_SCOPE_RESOLVED)),
        RetrievalStage.CANDIDATE_SOURCES_RESOLVED: lambda: controls.authorize_candidate_sources_resolved(_ctx(RetrievalStage.CANDIDATE_SOURCES_RESOLVED)),
        RetrievalStage.DOCUMENT_ACL_CHECKED: lambda: controls.authorize_document_acl_checked(_ctx(RetrievalStage.DOCUMENT_ACL_CHECKED), [_cand()]),
        RetrievalStage.CHUNK_ACL_CHECKED: lambda: controls.authorize_chunk_acl_checked(_ctx(RetrievalStage.CHUNK_ACL_CHECKED), [_cand()]),
        RetrievalStage.VECTOR_NAMESPACE_CHECKED: lambda: controls.authorize_vector_namespace_checked(_ctx(RetrievalStage.VECTOR_NAMESPACE_CHECKED), [_cand()]),
        RetrievalStage.VECTOR_METADATA_CHECKED: lambda: controls.authorize_vector_metadata_checked(_ctx(RetrievalStage.VECTOR_METADATA_CHECKED), [_cand()]),
        RetrievalStage.HYBRID_SEARCH_FILTERED: lambda: controls.authorize_hybrid_search_filtered(_ctx(RetrievalStage.HYBRID_SEARCH_FILTERED), [_cand()]),
        RetrievalStage.RERANK_CANDIDATES_FILTERED: lambda: controls.authorize_rerank_candidates_filtered(_ctx(RetrievalStage.RERANK_CANDIDATES_FILTERED), [_cand()]),
        RetrievalStage.CITATION_SOURCES_FILTERED: lambda: controls.authorize_citation_sources_filtered(_ctx(RetrievalStage.CITATION_SOURCES_FILTERED), [_cand()]),
        RetrievalStage.CONTEXT_CHUNKS_AUTHORIZED: lambda: controls.authorize_context_chunks_authorized(_ctx(RetrievalStage.CONTEXT_CHUNKS_AUTHORIZED), [_cand()]),
        RetrievalStage.PROMPT_CONTEXT_AUTHORIZED: lambda: controls.authorize_prompt_context_authorized(_ctx(RetrievalStage.PROMPT_CONTEXT_AUTHORIZED), [_cand()]),
        RetrievalStage.CACHE_READ_AUTHORIZED: lambda: controls.authorize_cache_read_authorized(_ctx(RetrievalStage.CACHE_READ_AUTHORIZED)),
        RetrievalStage.RETRIEVAL_AUDIT_WRITTEN: lambda: controls.authorize_retrieval_audit_written(_ctx(RetrievalStage.RETRIEVAL_AUDIT_WRITTEN)),
        RetrievalStage.RETRIEVAL_FINDING_RECORDED_IF_NEEDED: lambda: controls.authorize_retrieval_finding_recorded_if_needed(_ctx(RetrievalStage.RETRIEVAL_FINDING_RECORDED_IF_NEEDED)),
    }
    for stage, invoker in context_by_stage.items():
        decision = invoker()
        assert decision.stage == stage
        assert decision.reason


def test_decisions_do_not_expose_sensitive_content_or_source_names() -> None:
    unauthorized = RetrievalCandidate(
        candidate_id="secret-candidate",
        source_type=RetrievalSourceType.VECTOR,
        document=RetrievalDocument("doc-secret", "t2", (), ("unauthorized-group",), ("unauthorized-role",), False),
        chunk=RetrievalChunk("chunk-secret", "doc-secret", "t2", (), ("unauthorized-group",), ("unauthorized-role",)),
        vector_namespace=VectorNamespace("tenant:t2"),
        vector_metadata=VectorMetadata("t2", "doc-secret", "chunk-secret"),
        provenance_id="Finance-Q4-Projections",
    )
    decision = controls.authorize_document_acl_checked(_ctx(), [unauthorized])
    assert decision.status in {RetrievalDecisionStatus.DENY, RetrievalDecisionStatus.FILTER}
    assert decision.denial_category is not None
    assert "finance" not in decision.reason.lower()
    assert "q4" not in decision.reason.lower()
    assert "doc-secret" not in decision.reason
    assert "chunk-secret" not in decision.reason


def test_no_live_app_integration_imports_present() -> None:
    assert "onyx" not in controls.__dict__
