from backend.security_layer.artifacts.metadata_contract import (
    FORBIDDEN_ARTIFACT_METADATA_KEYS,
    REQUIRED_ARTIFACT_METADATA_FIELDS,
    sanitize_metadata_for_decision,
    validate_artifact_metadata,
)


def _valid_metadata() -> dict[str, str | bool]:
    return {k: "safe_value" for k in REQUIRED_ARTIFACT_METADATA_FIELDS} | {
        "metadata_schema_version": "1.0",
        "release_policy_id": "artifact-policy-minimal-01",
        "release_policy_mode": "inactive",
    }


def test_required_metadata_field_count_is_33() -> None:
    assert len(REQUIRED_ARTIFACT_METADATA_FIELDS) == 33


def test_validate_artifact_metadata_accepts_complete_payload() -> None:
    assert validate_artifact_metadata(_valid_metadata())


def test_forbidden_metadata_keys_rejected() -> None:
    for key in FORBIDDEN_ARTIFACT_METADATA_KEYS:
        metadata = _valid_metadata() | {key: "blocked"}
        assert not validate_artifact_metadata(metadata)


def test_forbidden_patterns_rejected() -> None:
    samples = [
        "raw_artifact_content", "raw_query_text", "raw_prompt_text", "raw_document_text", "raw_chunk_text",
        "source_secret=abc", "api_key=abc", "token=abc", "credential=abc", "-----BEGIN PRIVATE KEY-----",
        "password=hunter2", "https://x.y/path?token=abc", "john.doe@example.com",
        "tenant_internal_config", "source_internal_rules", "policy_internal_rules",
    ]
    for sample in samples:
        metadata = _valid_metadata() | {"classification_label": sample}
        assert not validate_artifact_metadata(metadata)


def test_sanitizer_only_returns_safe_fields() -> None:
    sanitized = sanitize_metadata_for_decision(_valid_metadata() | {"raw_payload": "secret"})
    assert "raw_payload" not in sanitized
    assert sanitized["metadata_schema_version"] == "1.0"
