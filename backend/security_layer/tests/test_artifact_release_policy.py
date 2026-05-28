from backend.security_layer.artifacts.release_policy import validate_artifact_release_policy, validate_release_policy_mode


def test_release_policy_validation() -> None:
    assert validate_artifact_release_policy({"release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "inactive"})
    assert validate_artifact_release_policy({"release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "monitor_only"})
    assert not validate_release_policy_mode("enforce")
    assert not validate_release_policy_mode("shadow_deny")


def test_approval_required_not_allowed() -> None:
    assert not validate_artifact_release_policy({"release_policy_id": "artifact-policy-minimal-01", "release_policy_mode": "approval_required"})
