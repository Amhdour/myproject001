from __future__ import annotations

from backend.security.enforcement.security_enforcer import SecurityEnforcer
from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.tests.security import factories


def test_high_risk_tool_without_approval_blocked() -> None:
    result = SecurityEnforcer().evaluate(
        factories.high_risk_tool_context(),
        enforcement_point="demo_attack.high_risk_tool_without_approval",
        demo_attack=True,
    )
    assert result.decision.decision == SecurityDecisionValue.APPROVAL_REQUIRED
    assert result.blocked
    assert result.decision.reason == "high_risk_action_requires_approval"
