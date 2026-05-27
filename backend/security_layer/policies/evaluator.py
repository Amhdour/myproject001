from backend.security_layer.policies.models import Policy
from backend.security_layer.policies.models import PolicyDecision
from backend.security_layer.policies.models import PolicyDecisionContext
from backend.security_layer.policies.models import PolicyEffect


def _rule_matches_action(action: str, rule_actions: list[str]) -> bool:
    return not rule_actions or action in rule_actions


def _rule_matches_context(context: PolicyDecisionContext, required_context: list[str]) -> bool:
    return all(key in context.attributes for key in required_context)


def evaluate_policy(policy: Policy, context: PolicyDecisionContext) -> PolicyDecision:
    matched_deny: list[str] = []
    matched_allow: list[str] = []
    matched_approval: list[str] = []

    for rule in policy.rules:
        if not _rule_matches_action(context.action, rule.actions):
            continue
        if not _rule_matches_context(context, rule.required_context):
            continue

        if rule.effect == PolicyEffect.DENY:
            matched_deny.append(rule.rule_id)
        elif rule.effect == PolicyEffect.ALLOW:
            matched_allow.append(rule.rule_id)
        elif rule.effect == PolicyEffect.APPROVAL_REQUIRED:
            matched_approval.append(rule.rule_id)

    if matched_deny:
        return PolicyDecision(policy.policy_id, policy.version, PolicyEffect.DENY, "deny rule matched", matched_deny)
    if matched_approval:
        return PolicyDecision(policy.policy_id, policy.version, PolicyEffect.APPROVAL_REQUIRED, "approval rule matched", matched_approval)
    if matched_allow:
        return PolicyDecision(policy.policy_id, policy.version, PolicyEffect.ALLOW, "allow rule matched", matched_allow)

    return PolicyDecision(policy.policy_id, policy.version, PolicyEffect.DENY, "no matching rule; default deny", [])


def evaluate_policies(policies: list[Policy], context: PolicyDecisionContext) -> PolicyDecision:
    decisions = [evaluate_policy(policy, context) for policy in policies]

    for decision in decisions:
        if decision.effect == PolicyEffect.DENY:
            return decision
    for decision in decisions:
        if decision.effect == PolicyEffect.APPROVAL_REQUIRED:
            return decision
    for decision in decisions:
        if decision.effect == PolicyEffect.ALLOW:
            return decision

    if decisions:
        return decisions[0]

    return PolicyDecision("none", "none", PolicyEffect.DENY, "no policies provided", [])


def explain_decision(decision: PolicyDecision) -> str:
    matched = ",".join(decision.matched_rule_ids) if decision.matched_rule_ids else "none"
    return (
        f"policy_id={decision.policy_id} version={decision.policy_version} "
        f"effect={decision.effect.value} reason={decision.reason} matched_rules={matched}"
    )
