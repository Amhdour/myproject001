from backend.security_layer.policies.exceptions import PolicyValidationError
from backend.security_layer.policies.models import EnforcementMode
from backend.security_layer.policies.models import Policy
from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.policies.models import PolicyScope


def validate_required_fields(policy: Policy) -> None:
    if not policy.policy_id:
        raise PolicyValidationError("missing policy_id")
    if not policy.version:
        raise PolicyValidationError("missing version")
    if not policy.scope:
        raise PolicyValidationError("missing scope")


def validate_effects(policy: Policy) -> None:
    if policy.default_effect not in set(PolicyEffect):
        raise PolicyValidationError("unknown default_effect")
    for rule in policy.rules:
        if rule.effect not in set(PolicyEffect):
            raise PolicyValidationError(f"unknown rule effect: {rule.rule_id}")


def validate_scopes(policy: Policy) -> None:
    if policy.scope not in set(PolicyScope):
        raise PolicyValidationError("unknown scope")


def validate_rules(policy: Policy) -> None:
    if policy.enforcement_mode not in set(EnforcementMode):
        raise PolicyValidationError("unknown enforcement mode")

    for rule in policy.rules:
        if rule.actions and not rule.required_context:
            raise PolicyValidationError(
                f"empty required_context for rule requiring context: {rule.rule_id}"
            )


def validate_policy(policy: Policy) -> None:
    validate_required_fields(policy)
    validate_effects(policy)
    validate_scopes(policy)
    validate_rules(policy)
