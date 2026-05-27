from backend.security_layer.policies.evaluator import evaluate_policies
from backend.security_layer.policies.evaluator import evaluate_policy
from backend.security_layer.policies.evaluator import explain_decision
from backend.security_layer.policies.loader import load_policy_file
from backend.security_layer.policies.models import PolicyDecisionContext
from backend.security_layer.policies.models import PolicyEffect


def test_default_deny_behavior() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_allow_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="write", attributes={"user_id": "u1"}))
    assert decision.effect == PolicyEffect.DENY


def test_allow_decision() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_allow_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="read", attributes={"user_id": "u1"}))
    assert decision.effect == PolicyEffect.ALLOW


def test_deny_decision() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_deny_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="delete", attributes={"user_id": "u1"}))
    assert decision.effect == PolicyEffect.DENY


def test_approval_required_decision() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_approval_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="export", attributes={"ticket_id": "123"}))
    assert decision.effect == PolicyEffect.APPROVAL_REQUIRED


def test_deny_precedence_over_allow() -> None:
    allow_policy = load_policy_file("backend/security_layer/tests/fixtures/valid_allow_policy.json")
    deny_policy = load_policy_file("backend/security_layer/tests/fixtures/valid_deny_policy.json")
    decision = evaluate_policies(
        [allow_policy, deny_policy],
        PolicyDecisionContext(action="delete", attributes={"user_id": "u1"}),
    )
    assert decision.effect == PolicyEffect.DENY


def test_evaluate_policies_with_no_policies_is_default_deny() -> None:
    decision = evaluate_policies([], PolicyDecisionContext(action="read", attributes={"user_id": "u1"}))
    assert decision.effect == PolicyEffect.DENY
    assert decision.reason == "no policies provided"


def test_missing_required_context_denies() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_allow_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="read", attributes={}))
    assert decision.effect == PolicyEffect.DENY
    assert decision.reason == "no matching rule; default deny"


def test_policy_version_is_recorded_on_decision() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_allow_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="read", attributes={"user_id": "u1"}))
    assert decision.policy_version == policy.version


def test_explainable_decision_output() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/valid_allow_policy.json")
    decision = evaluate_policy(policy, PolicyDecisionContext(action="read", attributes={"user_id": "u1"}))
    explanation = explain_decision(decision)
    assert "policy_id=allow-policy" in explanation
    assert f"version={policy.version}" in explanation
    assert "matched_rules=allow-read" in explanation
