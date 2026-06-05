from __future__ import annotations

from backend.security.enforcement.security_enforcer import SecurityEnforcer
from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.tests.security import factories


def test_cross_tenant_retrieval_attack_blocked() -> None:
    result = SecurityEnforcer().evaluate(
        factories.cross_tenant_context(),
        enforcement_point="demo_attack.cross_tenant_retrieval",
        demo_attack=True,
    )
    assert result.decision.decision == SecurityDecisionValue.DENY
    assert result.blocked
    assert result.decision.reason == "cross_tenant_access_default_deny"
