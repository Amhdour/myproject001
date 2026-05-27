import pytest

from backend.security_layer.policies.exceptions import PolicyValidationError
from backend.security_layer.policies.loader import load_policy_file
from backend.security_layer.policies.validator import validate_policy


def test_invalid_missing_required_fields() -> None:
    policy = load_policy_file("backend/security_layer/tests/fixtures/invalid_missing_policy_id.json")
    with pytest.raises(PolicyValidationError):
        validate_policy(policy)


def test_unknown_effect_rejected() -> None:
    with pytest.raises(Exception):
        load_policy_file("backend/security_layer/tests/fixtures/invalid_unknown_effect.json")


def test_unknown_scope_rejected() -> None:
    with pytest.raises(Exception):
        load_policy_file("backend/security_layer/tests/fixtures/invalid_unknown_scope.json")
