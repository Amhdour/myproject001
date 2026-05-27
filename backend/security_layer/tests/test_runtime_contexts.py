from backend.security_layer.runtime.contexts import RequestContext, SecurityDecisionContext, SubjectContext, TenantContext


def test_request_context_creation() -> None:
    request = RequestContext(request_id="r1", operation="retrieval")
    assert request.request_id == "r1"


def test_subject_context_creation() -> None:
    subject = SubjectContext(subject_id="u1")
    assert subject.subject_id == "u1"


def test_tenant_context_creation() -> None:
    tenant = TenantContext(tenant_id="t1")
    context = SecurityDecisionContext(request=RequestContext("r1", "retrieval"), subject=SubjectContext("u1"), tenant=tenant)
    assert context.tenant is not None
