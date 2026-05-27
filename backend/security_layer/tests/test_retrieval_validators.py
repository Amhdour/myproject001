from datetime import datetime

from backend.security_layer.retrieval.models import ACLSnapshot, RetrievalACLContext, RetrievalCandidate, RetrievalChunk, RetrievalDocument, RetrievalSourceType, RetrievalStage, RetrievalSubject, RetrievalTenant, VectorMetadata, VectorNamespace
from backend.security_layer.retrieval.validators import filter_authorized_candidates


def _ctx() -> RetrievalACLContext:
    return RetrievalACLContext(
        subject=RetrievalSubject(subject_id="u1", group_ids=("g1",), role_ids=("r1",)),
        tenant=RetrievalTenant(tenant_id="t1"),
        stage=RetrievalStage.DOCUMENT_ACL_CHECKED,
        source_type=RetrievalSourceType.VECTOR,
        request_id="req-1",
        retrieval_scope=("kb",),
        acl_snapshot=ACLSnapshot(captured_at=datetime.utcnow(), acl_entries_count=1, is_stale=False),
        expected_vector_namespace="tenant:t1",
    )


def _cand(**kwargs: object) -> RetrievalCandidate:
    base = RetrievalCandidate(
        candidate_id="c1",
        source_type=RetrievalSourceType.VECTOR,
        document=RetrievalDocument("d1", "t1", ("u1",), ("g1",), ("r1",), False),
        chunk=RetrievalChunk("ch1", "d1", "t1", ("u1",), ("g1",), ("r1",)),
        vector_namespace=VectorNamespace("tenant:t1"),
        vector_metadata=VectorMetadata("t1", "d1", "ch1"),
        provenance_id="p1",
    )
    return RetrievalCandidate(**{**base.__dict__, **kwargs})


def test_filter_authorized_candidates() -> None:
    allowed, denied, _ = filter_authorized_candidates(_ctx(), [_cand()])
    assert len(allowed) == 1
    assert denied == []
