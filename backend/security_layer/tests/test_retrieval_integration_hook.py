from datetime import datetime

from backend.security_layer.retrieval.context_builder import RetrievalContextBuildInput, build_candidate_from_metadata, build_retrieval_acl_context
from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig, RetrievalIntegrationMode
from backend.security_layer.retrieval.integration_hook import evaluate_retrieval_candidates_with_acl
from backend.security_layer.retrieval.models import ACLSnapshot, RetrievalSourceType, RetrievalStage
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics


def _ctx() :
    i = RetrievalContextBuildInput(request_id='r1', source_type=RetrievalSourceType.VECTOR, stage=RetrievalStage.DOCUMENT_ACL_CHECKED, subject_id='u1', tenant_id='t1', retrieval_scope=('kb',), expected_vector_namespace='tenant:t1', acl_snapshot=ACLSnapshot(datetime.utcnow(),1,False))
    return build_retrieval_acl_context(i)


def _cands():
    ok = build_candidate_from_metadata({'candidate_id':'c1','tenant_id':'t1','document_id':'d1','chunk_id':'ch1','vector_namespace':'tenant:t1','source_type':'vector','document_allowed_subject_ids':['u1'],'chunk_allowed_subject_ids':['u1']})
    cross = build_candidate_from_metadata({'candidate_id':'c2','tenant_id':'t2','document_id':'d2','chunk_id':'ch2','vector_namespace':'tenant:t2','source_type':'vector','document_allowed_subject_ids':['u1'],'chunk_allowed_subject_ids':['u1']})
    unauth_chunk = build_candidate_from_metadata({'candidate_id':'c3','tenant_id':'t1','document_id':'d3','chunk_id':'ch3','vector_namespace':'tenant:t1','source_type':'vector','document_allowed_subject_ids':['u1'],'chunk_allowed_subject_ids':['u2']})
    return [ok,cross,unauth_chunk]


def test_modes_behavior_and_events() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    ctx = _ctx(); cands = _cands()
    disabled = evaluate_retrieval_candidates_with_acl(RetrievalIntegrationConfig(RetrievalIntegrationMode.DISABLED), ctx, cands)
    assert len(disabled.candidates) == 3
    monitor = evaluate_retrieval_candidates_with_acl(RetrievalIntegrationConfig(RetrievalIntegrationMode.MONITOR_ONLY), ctx, cands)
    assert len(monitor.candidates) == 3
    shadow = evaluate_retrieval_candidates_with_acl(RetrievalIntegrationConfig(RetrievalIntegrationMode.SHADOW_DENY), ctx, cands)
    assert len(shadow.candidates) == 3
    enforce = evaluate_retrieval_candidates_with_acl(RetrievalIntegrationConfig(RetrievalIntegrationMode.ENFORCE), ctx, cands)
    assert [c.candidate_id for c in enforce.candidates] == ['c1']
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()


def test_no_live_imports_reference() -> None:
    import backend.security_layer.retrieval.integration_hook as hook
    assert 'onyx' not in hook.__dict__
