import pytest

from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.runtime.audit import clear_audit_events
from backend.security_layer.runtime.audit import get_audit_events
from backend.security_layer.runtime.contexts import ArtifactContext
from backend.security_layer.runtime.contexts import RequestContext
from backend.security_layer.runtime.contexts import RetrievalContext
from backend.security_layer.runtime.contexts import SecurityDecisionContext
from backend.security_layer.runtime.contexts import SubjectContext
from backend.security_layer.runtime.contexts import TenantContext
from backend.security_layer.runtime.denials import SecurityDenial
from backend.security_layer.runtime.findings import clear_findings
from backend.security_layer.runtime.findings import get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics
from backend.security_layer.runtime.metrics import get_security_metrics
from backend.security_layer.runtime.wrappers import WrapperMode
from backend.security_layer.runtime.wrappers import authorize_artifact_release
from backend.security_layer.runtime.wrappers import authorize_cache_access
from backend.security_layer.runtime.wrappers import authorize_ingestion
from backend.security_layer.runtime.wrappers import authorize_mcp_action
from backend.security_layer.runtime.wrappers import authorize_model_call
from backend.security_layer.runtime.wrappers import authorize_prompt_use
from backend.security_layer.runtime.wrappers import authorize_retrieval
from backend.security_layer.runtime.wrappers import authorize_sandbox_execution
from backend.security_layer.runtime.wrappers import authorize_tool_call
from backend.security_layer.runtime.wrappers import authorize_vector_query
from backend.security_layer.runtime.wrappers import require_human_approval


def _ctx() -> SecurityDecisionContext:
    return SecurityDecisionContext(
        request=RequestContext("r1", "op"),
        subject=SubjectContext("u1"),
        tenant=TenantContext("t1"),
        retrieval=RetrievalContext(query_hash="q"),
    )


def _eval(effect: str):
    return lambda _a, _c: effect


def setup_function() -> None:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()


def test_missing_tenant_denied() -> None:
    with pytest.raises(SecurityDenial):
        authorize_retrieval(
            SecurityDecisionContext(
                request=RequestContext("r1", "op"),
                subject=SubjectContext("u1"),
            )
        )


def test_missing_subject_denied() -> None:
    with pytest.raises(SecurityDenial):
        authorize_retrieval(
            SecurityDecisionContext(
                request=RequestContext("r1", "op"),
                tenant=TenantContext("t1"),
            )
        )


def test_wrapper_functions_covered() -> None:
    assert authorize_ingestion(_ctx(), _eval("allow")).decision == "allow"
    assert authorize_retrieval(_ctx(), _eval("allow")).decision == "allow"

    with pytest.raises(SecurityDenial):
        authorize_vector_query(_ctx(), _eval(PolicyEffect.DENY))
    with pytest.raises(SecurityDenial):
        authorize_cache_access(_ctx(), _eval("deny"))

    assert authorize_tool_call(_ctx(), _eval("approval_required")).approval_required

    with pytest.raises(SecurityDenial):
        authorize_mcp_action(_ctx(), _eval("deny"))
    with pytest.raises(SecurityDenial):
        authorize_artifact_release(
            SecurityDecisionContext(
                request=RequestContext("r1", "op"),
                subject=SubjectContext("u1"),
                tenant=TenantContext("t1"),
                artifact=ArtifactContext(artifact_type="file", redaction_applied=False),
            ),
            _eval("deny"),
        )
    with pytest.raises(SecurityDenial):
        authorize_sandbox_execution(_ctx(), _eval("deny"))

    assert authorize_model_call(_ctx(), _eval("allow")).decision == "allow"
    assert authorize_prompt_use(_ctx(), _eval("allow")).decision == "allow"
    assert require_human_approval(_ctx(), _eval("approval_required")).approval_required


def test_fail_closed_and_modes() -> None:
    assert (
        authorize_retrieval(_ctx(), _eval("deny"), WrapperMode.MONITOR_ONLY).decision
        == "allow"
    )
    assert (
        authorize_retrieval(_ctx(), _eval("deny"), WrapperMode.SHADOW_DENY).decision
        == "shadow_deny"
    )

    with pytest.raises(SecurityDenial):
        authorize_retrieval(_ctx(), None, WrapperMode.ENFORCE)

    def _boom(_a, _c):
        raise RuntimeError("down")

    with pytest.raises(SecurityDenial):
        authorize_retrieval(_ctx(), _boom, WrapperMode.ENFORCE)


def test_audit_finding_metric_recording() -> None:
    assert authorize_retrieval(_ctx(), _eval("allow")).decision == "allow"

    with pytest.raises(SecurityDenial):
        authorize_retrieval(_ctx(), _eval("deny"))

    events = get_audit_events()
    findings = get_findings()
    metrics = get_security_metrics()
    assert len(events) == 2
    assert len(findings) == 1
    assert len(metrics) == 2


def test_monitor_only_denied_action_does_not_raise() -> None:
    decision = authorize_tool_call(_ctx(), _eval("deny"), WrapperMode.MONITOR_ONLY)
    assert decision.decision == "allow"


def test_shadow_deny_records_and_returns_structured_result() -> None:
    decision = authorize_tool_call(_ctx(), _eval("deny"), WrapperMode.SHADOW_DENY)
    assert decision.decision == "shadow_deny"
    assert get_findings()[-1].reason_code == "shadow_denied"
