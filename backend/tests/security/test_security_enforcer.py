from __future__ import annotations

import pytest

from backend.security.enforcement.security_enforcer import SecurityEnforcementError
from backend.security.enforcement.security_enforcer import SecurityEnforcer
from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.tests.security import factories


def test_enforcer_allows_same_tenant_context(enforcer: SecurityEnforcer) -> None:
    result = enforcer.enforce(
        factories.valid_same_tenant_context(), enforcement_point="pytest"
    )
    assert result.decision.decision == SecurityDecisionValue.ALLOW
    assert not result.blocked


def test_enforcer_blocks_denied_context(enforcer: SecurityEnforcer) -> None:
    with pytest.raises(SecurityEnforcementError) as exc:
        enforcer.enforce(factories.cross_tenant_context(), enforcement_point="pytest")
    assert exc.value.decision.reason == "cross_tenant_access_default_deny"


def test_enforcer_blocks_approval_required_without_approval(enforcer: SecurityEnforcer) -> None:
    with pytest.raises(SecurityEnforcementError) as exc:
        enforcer.enforce(factories.high_risk_tool_context(), enforcement_point="pytest")
    assert exc.value.decision.decision == SecurityDecisionValue.APPROVAL_REQUIRED


def test_enforcer_allows_high_risk_tool_with_approval(enforcer: SecurityEnforcer) -> None:
    context = factories.high_risk_tool_context()
    context["approved"] = True
    result = enforcer.enforce(context, enforcement_point="pytest")
    assert result.decision.decision == SecurityDecisionValue.ALLOW


def test_monitor_only_logs_without_blocking(enforcer: SecurityEnforcer) -> None:
    result = enforcer.enforce(factories.monitor_only_context(), enforcement_point="pytest")
    assert result.decision.decision == SecurityDecisionValue.MONITOR_ONLY
    assert not result.blocked


def test_invalid_context_fails_closed(enforcer: SecurityEnforcer) -> None:
    with pytest.raises(SecurityEnforcementError) as exc:
        enforcer.enforce({"tenant_id": "tenant-alpha"}, enforcement_point="pytest")
    assert exc.value.decision.reason.startswith("invalid_security_context")
