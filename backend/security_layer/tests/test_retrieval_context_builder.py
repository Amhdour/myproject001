import pytest

from backend.security_layer.retrieval.context_builder import RetrievalContextBuildInput, RetrievalContextBuildResult, build_candidate_from_metadata, build_candidates_from_metadata_list, build_retrieval_acl_context, build_subject_context, build_tenant_context, validate_context_build_result
from backend.security_layer.retrieval.models import RetrievalSourceType, RetrievalStage


def test_subject_and_tenant_context_builders_and_missing_safe() -> None:
    inp = RetrievalContextBuildInput(request_id='r1', source_type=RetrievalSourceType.VECTOR, stage=RetrievalStage.DOCUMENT_ACL_CHECKED, subject_id='u1', tenant_id='t1')
    assert build_subject_context(inp).subject_id == 'u1'
    assert build_tenant_context(inp).tenant_id == 't1'
    missing = RetrievalContextBuildInput(request_id='r2', source_type=RetrievalSourceType.VECTOR, stage=RetrievalStage.DOCUMENT_ACL_CHECKED)
    assert build_subject_context(missing).subject_id is None
    assert build_tenant_context(missing).tenant_id is None


def test_build_candidate_safe_and_reject_unsafe_text_secret() -> None:
    md = {'candidate_id':'c1','tenant_id':'t1','document_id':'d1','chunk_id':'ch1','vector_namespace':'tenant:t1','source_type':'vector','document_allowed_subject_ids':['u1'],'chunk_allowed_subject_ids':['u1']}
    cand = build_candidate_from_metadata(md)
    assert cand.document.document_id == 'd1'
    assert cand.chunk.chunk_id == 'ch1'
    assert build_candidates_from_metadata_list([md])[0].candidate_id == 'c1'
    for key in ['document_text', 'chunk_text', 'source_secret']:
        bad = dict(md); bad[key] = 'sensitive'
        with pytest.raises(ValueError):
            build_candidate_from_metadata(bad)


def test_build_context_and_validate_result() -> None:
    inp = RetrievalContextBuildInput(request_id='r3', source_type=RetrievalSourceType.VECTOR, stage=RetrievalStage.DOCUMENT_ACL_CHECKED, subject_id='u1', tenant_id='t1')
    ctx = build_retrieval_acl_context(inp)
    result = RetrievalContextBuildResult(context=ctx, candidates=(build_candidate_from_metadata({'candidate_id':'c1','tenant_id':'t1','document_id':'d1','chunk_id':'ch1','vector_namespace':'tenant:t1','source_type':'vector'}),))
    assert validate_context_build_result(result)
