from pathlib import Path

import pytest

from backend.security_layer.policies.exceptions import PolicyLoadError
from backend.security_layer.policies.loader import compute_policy_hash
from backend.security_layer.policies.loader import load_policy_file


FIXTURES = Path(__file__).parent / "fixtures"


def test_policy_hash_generated() -> None:
    value = compute_policy_hash('{"a":1}')
    assert len(value) == 64


def test_unsupported_file_extension_rejected(tmp_path: Path) -> None:
    path = tmp_path / "policy.txt"
    path.write_text("test", encoding="utf-8")
    with pytest.raises(PolicyLoadError):
        load_policy_file(path)


def test_load_valid_json_policy() -> None:
    policy = load_policy_file(FIXTURES / "valid_allow_policy.json")
    assert policy.policy_id == "allow-policy"
