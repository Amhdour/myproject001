import pytest

from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.runtime.contexts import RequestContext
from backend.security_layer.runtime.contexts import RetrievalContext
from backend.security_layer.runtime.contexts import SecurityDecisionContext
from backend.security_layer.runtime.contexts import SubjectContext
from backend.security_layer.runtime.contexts import TenantContext
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.denials import SecurityDenial
from backend.security_layer.runtime.wrappers import WrapperMode
from backend.security_layer.runtime.wrappers import authorize_retrieval
from backend.security_layer.runtime.wrappers import authorize_tool_call


def _ctx() -> SecurityDecisionContext:
    return SecurityDecisionContext(
        request=RequestContext("r1", "op"),
        subject=SubjectContext("u1"),
        tenant=TenantContext("t1"),
        retrieval=RetrievalContext(query_hash="q"),
    )


def _eval(effect: str):
    return lambda _a, _c: effect


def test_wrapper_deny_path_uses_safe_denial() -> None:
    with pytest.raises(SecurityDenial) as ex:
        authorize_retrieval(_ctx(), _eval(PolicyEffect.DENY))
    assert ex.value.payload.category == DenialCategory.POLICY_DENIED
    assert "policy" in ex.value.message.lower()


def test_wrapper_fail_closed_path_uses_safe_denial() -> None:
    with pytest.raises(SecurityDenial) as ex:
        authorize_retrieval(_ctx(), None, WrapperMode.ENFORCE)
    assert ex.value.payload.category == DenialCategory.POLICY_ENGINE_UNAVAILABLE


def test_wrapper_approval_required_path_safe_structured_response() -> None:
    decision = authorize_tool_call(_ctx(), _eval(PolicyEffect.APPROVAL_REQUIRED))
    assert decision.approval_required is True
    assert decision.denial_payload is not None
    assert decision.denial_payload["approval_required"] is True
    assert decision.denial_payload["error_code"].startswith("security_")


def test_monitor_only_and_shadow_deny_do_not_leak_policy_internals() -> None:
    monitor_decision = authorize_tool_call(_ctx(), _eval("deny_internal_rule_44"), WrapperMode.MONITOR_ONLY)
    shadow_decision = authorize_tool_call(_ctx(), _eval("deny_internal_rule_44"), WrapperMode.SHADOW_DENY)
    monitor_text = str(monitor_decision)
    shadow_text = str(shadow_decision)
    assert "internal_rule_44" not in monitor_text
    assert "internal_rule_44" not in shadow_text
