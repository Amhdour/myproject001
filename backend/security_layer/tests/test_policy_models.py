from backend.security_layer.policies.models import EnforcementMode
from backend.security_layer.policies.models import Policy
from backend.security_layer.policies.models import PolicyDecisionContext
from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.policies.models import PolicyRule
from backend.security_layer.policies.models import PolicyScope


def test_valid_policy_object() -> None:
    policy = Policy(
        policy_id="p1",
        version="1",
        scope=PolicyScope.RETRIEVAL,
        default_effect=PolicyEffect.DENY,
        enforcement_mode=EnforcementMode.DISABLED,
        rules=[
            PolicyRule(
                rule_id="r1",
                effect=PolicyEffect.ALLOW,
                actions=["read"],
                required_context=["user_id"],
            )
        ],
    )
    context = PolicyDecisionContext(action="read", attributes={"user_id": "u1"})
    assert policy.policy_id == "p1"
    assert context.action == "read"
