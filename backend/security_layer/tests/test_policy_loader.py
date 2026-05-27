from pathlib import Path

import pytest

from backend.security_layer.policies.exceptions import PolicyLoadError
from backend.security_layer.policies.loader import compute_policy_hash
from backend.security_layer.policies.loader import load_policy_directory
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


def test_load_policy_directory_with_json_files(tmp_path: Path) -> None:
    (tmp_path / "a.json").write_text((FIXTURES / "valid_allow_policy.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "b.json").write_text((FIXTURES / "valid_deny_policy.json").read_text(encoding="utf-8"), encoding="utf-8")
    (tmp_path / "ignore.txt").write_text("not policy", encoding="utf-8")
    policies = load_policy_directory(tmp_path)
    assert len(policies) == 2
