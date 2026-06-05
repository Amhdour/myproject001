from __future__ import annotations

from backend.security.enforcement.security_enforcer import SecurityEnforcer
from backend.security.policy.policy_decision import SecurityDecisionValue
from backend.tests.security import factories


def test_unsafe_sandbox_action_requires_approval() -> None:
    result = SecurityEnforcer().evaluate(
        factories.unsafe_sandbox_context(),
        enforcement_point="demo_attack.unsafe_sandbox_action",
        demo_attack=True,
    )
    assert result.decision.decision == SecurityDecisionValue.APPROVAL_REQUIRED
    assert result.blocked
