from __future__ import annotations


def validate_release_policy_mode(mode: str) -> bool:
    return mode in {"inactive", "monitor_only"}


def validate_release_policy_id(policy_id: str) -> bool:
    return policy_id.startswith("artifact-policy-") and len(policy_id) > 16


def validate_artifact_release_policy(metadata: dict[str, str | bool]) -> bool:
    policy_id = str(metadata.get("release_policy_id", ""))
    mode = str(metadata.get("release_policy_mode", ""))
    return validate_release_policy_id(policy_id) and validate_release_policy_mode(mode)
