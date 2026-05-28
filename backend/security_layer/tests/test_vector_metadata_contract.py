from datetime import UTC, datetime, timedelta

from backend.security_layer.vector.metadata_contract import (
    FORBIDDEN_VECTOR_METADATA_KEYS,
    REQUIRED_VECTOR_METADATA_FIELDS,
    VECTOR_METADATA_SCHEMA_VERSION,
    build_safe_vector_metadata,
    sanitize_vector_metadata,
    validate_metadata_schema_version,
    validate_no_forbidden_metadata_content,
    validate_vector_metadata,
)


def _base() -> dict[str, object]:
    now = datetime.now(UTC)
    return {
        "tenant_id_hash_or_safe_id": "tenant_hash",
        "workspace_id_hash_or_safe_id": "workspace_hash",
        "document_id_hash_or_safe_id": "doc_hash",
        "chunk_id_hash_or_safe_id": "chunk_hash",
        "source_type": "connector",
        "source_id_hash_or_safe_id": "source_hash",
        "acl_snapshot_id": "acl_1",
        "acl_snapshot_version": "v1",
        "acl_snapshot_created_at": now.isoformat(),
        "acl_snapshot_expires_at": (now + timedelta(hours=1)).isoformat(),
        "document_deleted": False,
        "document_stale": False,
        "provenance_id": "prov_1",
        "ingestion_run_id": "ing_1",
        "embedding_model_id": "embed_1",
        "embedding_created_at": now.isoformat(),
        "content_type": "text/plain",
        "sensitivity_label_placeholder": "internal",
        "prompt_injection_flag": False,
        "poisoning_flag": False,
    }


def test_contract_has_all_21_fields() -> None:
    assert len(REQUIRED_VECTOR_METADATA_FIELDS) == 21
    assert "metadata_schema_version" in REQUIRED_VECTOR_METADATA_FIELDS


def test_build_safe_vector_metadata_has_all_required_fields() -> None:
    metadata = build_safe_vector_metadata(**_base())
    assert len(metadata) == 21
    for field in REQUIRED_VECTOR_METADATA_FIELDS:
        assert field in metadata
    assert metadata["metadata_schema_version"] == VECTOR_METADATA_SCHEMA_VERSION


def test_forbidden_metadata_keys_rejected() -> None:
    assert FORBIDDEN_VECTOR_METADATA_KEYS
    for key in FORBIDDEN_VECTOR_METADATA_KEYS:
        metadata = build_safe_vector_metadata(**_base())
        metadata[key] = "x"
        assert not validate_vector_metadata(metadata)


def test_forbidden_content_patterns_rejected() -> None:
    bad_values = [
        "raw document text: should-never-pass",
        "raw chunk text should-never-pass",
        "api_key=abc123",
        "token: abc123",
        "credential=abc123",
        "https://user:pass@example.com/connector",
        "person@example.com",
    ]
    for bad in bad_values:
        metadata = build_safe_vector_metadata(**_base())
        metadata["content_type"] = bad
        assert not validate_no_forbidden_metadata_content(metadata)
        assert not validate_vector_metadata(metadata)

    source_secret = build_safe_vector_metadata(**_base())
    source_secret["source_secret"] = "hidden"
    assert not validate_vector_metadata(source_secret)

    policy_internal = build_safe_vector_metadata(**_base())
    policy_internal["policy_internal"] = "deny if ..."
    assert not validate_vector_metadata(policy_internal)


def test_missing_required_field_rejected() -> None:
    metadata = build_safe_vector_metadata(**_base())
    metadata.pop("tenant_id_hash_or_safe_id")
    assert not validate_vector_metadata(metadata)


def test_schema_version_validated() -> None:
    metadata = build_safe_vector_metadata(**_base())
    assert validate_metadata_schema_version(metadata)
    metadata["metadata_schema_version"] = "0.9"
    assert not validate_metadata_schema_version(metadata)
    assert not validate_vector_metadata(metadata)


def test_sanitization_strips_and_does_not_invent_raw_content_fields() -> None:
    sanitized = sanitize_vector_metadata({" content_type ": " text/plain ", "document_deleted": False, "x": None})
    assert sanitized[" content_type "] == "text/plain"
    assert sanitized["x"] == ""
    assert "raw_document_text" not in sanitized
    assert "raw_chunk_text" not in sanitized
