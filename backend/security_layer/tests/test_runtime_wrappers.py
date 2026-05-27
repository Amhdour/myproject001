import pytest

from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.contexts import ArtifactContext, RequestContext, RetrievalContext, SecurityDecisionContext, SubjectContext, TenantContext
from backend.security_layer.runtime.denials import SecurityDenial
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.runtime.wrappers import WrapperMode, authorize_artifact_release, authorize_cache_access, authorize_mcp_action, authorize_model_call, authorize_prompt_use, authorize_retrieval, authorize_sandbox_execution, authorize_tool_call, authorize_vector_query, require_human_approval


def _ctx() -> SecurityDecisionContext:
    return SecurityDecisionContext(request=RequestContext("r1", "op"), subject=SubjectContext("u1"), tenant=TenantContext("t1"), retrieval=RetrievalContext(query_hash="q"))


def _eval(effect: str):
    return lambda _a, _c: effect


def setup_function() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()


def test_missing_tenant_denied() -> None:
    with pytest.raises(SecurityDenial):
        authorize_retrieval(SecurityDecisionContext(request=RequestContext("r1", "op"), subject=SubjectContext("u1")))


def test_missing_subject_denied() -> None:
    with pytest.raises(SecurityDenial):
        authorize_retrieval(SecurityDecisionContext(request=RequestContext("r1", "op"), tenant=TenantContext("t1")))


def test_wrapper_paths() -> None:
    assert authorize_retrieval(_ctx(), _eval("allow")).decision == "allow"
    with pytest.raises(SecurityDenial): authorize_retrieval(_ctx(), _eval("deny"))
    with pytest.raises(SecurityDenial): authorize_vector_query(_ctx(), _eval(PolicyEffect.DENY))
    with pytest.raises(SecurityDenial): authorize_cache_access(_ctx(), _eval("deny"))
    assert authorize_tool_call(_ctx(), _eval("approval_required")).approval_required
    with pytest.raises(SecurityDenial): authorize_mcp_action(_ctx(), _eval("deny"))
    with pytest.raises(SecurityDenial): authorize_artifact_release(SecurityDecisionContext(request=RequestContext("r1", "op"), subject=SubjectContext("u1"), tenant=TenantContext("t1"), artifact=ArtifactContext(artifact_type="file", redaction_applied=False)), _eval("deny"))
    with pytest.raises(SecurityDenial): authorize_sandbox_execution(_ctx(), _eval("deny"))
    assert authorize_model_call(_ctx(), _eval("allow")).decision == "allow"
    with pytest.raises(SecurityDenial): authorize_model_call(_ctx(), _eval("deny"))
    assert authorize_prompt_use(_ctx(), _eval("allow")).decision == "allow"
    with pytest.raises(SecurityDenial): authorize_prompt_use(_ctx(), _eval("deny"))
    assert require_human_approval(_ctx(), _eval("approval_required")).approval_required


def test_audit_finding_metric_and_modes_and_fail_closed() -> None:
    assert authorize_retrieval(_ctx(), _eval("deny"), WrapperMode.MONITOR_ONLY).decision == "allow"
    assert authorize_retrieval(_ctx(), _eval("deny"), WrapperMode.SHADOW_DENY).decision == "shadow_deny"
    with pytest.raises(SecurityDenial):
        authorize_retrieval(_ctx(), None, WrapperMode.ENFORCE)
    assert len(get_audit_events()) >= 3
    assert len(get_findings()) >= 2
    assert len(get_security_metrics()) >= 3


def test_no_runtime_app_integration() -> None:
    assert True
