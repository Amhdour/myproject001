from backend.security_layer.artifacts.release_policy import validate_artifact_release_policy


def test_release_policy_validation() -> None:
    assert validate_artifact_release_policy({"release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "inactive"})
    assert not validate_artifact_release_policy({"release_policy_id": "bad", "release_policy_mode": "enforce"})
