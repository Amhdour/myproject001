from __future__ import annotations

import pytest
from pydantic import ValidationError

from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.security.policy.policy_schema import SecurityContext
from backend.security.policy.security_policy import SecurityPolicy
from backend.tests.security import factories


def test_policy_schema_validates_required_fields() -> None:
    context = SecurityContext.model_validate(factories.valid_same_tenant_context())
    assert context.user_id == "user-alpha"


def test_policy_schema_rejects_blank_required_fields() -> None:
    context = factories.valid_same_tenant_context()
    context["correlation_id"] = ""
    with pytest.raises(ValidationError):
        SecurityContext.model_validate(context)


def test_default_allow_for_same_tenant_known_action() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.valid_same_tenant_context())
    assert decision.decision == SecurityDecisionValue.ALLOW
    assert decision.policy_version == "portfolio-readiness-mvp-v1"


def test_missing_user_denies() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.missing_user_context())
    assert decision.decision == SecurityDecisionValue.DENY
    assert decision.reason == "missing_user_id_default_deny"


def test_missing_tenant_denies() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.missing_tenant_context())
    assert decision.decision == SecurityDecisionValue.DENY
    assert decision.reason == "missing_tenant_id_default_deny"


def test_cross_tenant_denies() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.cross_tenant_context())
    assert decision.decision == SecurityDecisionValue.DENY
    assert decision.reason == "cross_tenant_access_default_deny"


def test_unknown_action_denies() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.unknown_action_context())
    assert decision.decision == SecurityDecisionValue.DENY
    assert decision.reason == "unknown_action_default_deny"


def test_high_risk_tool_requires_approval() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.high_risk_tool_context())
    assert decision.decision == SecurityDecisionValue.APPROVAL_REQUIRED


def test_monitor_only_decision_does_not_block() -> None:
    decision, _ = SecurityPolicy().evaluate(factories.monitor_only_context())
    assert decision.decision == SecurityDecisionValue.MONITOR_ONLY
    assert not decision.blocks_runtime
