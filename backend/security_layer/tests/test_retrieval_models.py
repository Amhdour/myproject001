from datetime import datetime

from backend.security_layer.retrieval.models import ACLSnapshot, RetrievalACLContext, RetrievalSourceType, RetrievalStage, RetrievalSubject, RetrievalTenant


def test_retrieval_context_creation() -> None:
    ctx = RetrievalACLContext(
        subject=RetrievalSubject(subject_id="user-1", group_ids=("g1",), role_ids=("r1",)),
        tenant=RetrievalTenant(tenant_id="t1"),
        stage=RetrievalStage.QUERY_RECEIVED,
        source_type=RetrievalSourceType.HYBRID,
        request_id="req-1",
        retrieval_scope=("docs",),
        acl_snapshot=ACLSnapshot(captured_at=datetime.utcnow(), acl_entries_count=2, is_stale=False),
        expected_vector_namespace="tenant:t1",
    )
    assert ctx.tenant.tenant_id == "t1"
    assert ctx.subject.subject_id == "user-1"
