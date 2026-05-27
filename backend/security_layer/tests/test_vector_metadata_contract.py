from datetime import UTC, datetime, timedelta

from backend.security_layer.vector.metadata_contract import build_safe_vector_metadata, validate_vector_metadata


def _base() -> dict[str, object]:
    now = datetime.now(UTC)
    return {
        "tenant_id_hash_or_safe_id": "t",
        "workspace_id_hash_or_safe_id": "w",
        "document_id_hash_or_safe_id": "d",
        "chunk_id_hash_or_safe_id": "c",
        "source_type": "connector",
        "source_id_hash_or_safe_id": "s",
        "acl_snapshot_id": "acl1",
        "acl_snapshot_version": "1",
        "acl_snapshot_created_at": now.isoformat(),
        "acl_snapshot_expires_at": (now + timedelta(hours=1)).isoformat(),
        "document_deleted": False,
        "document_stale": False,
        "provenance_id": "p",
        "ingestion_run_id": "ing",
        "embedding_model_id": "e",
        "embedding_created_at": now.isoformat(),
        "content_type": "text/plain",
        "sensitivity_label_placeholder": "internal",
        "prompt_injection_flag": True,
        "poisoning_flag": True,
    }


def test_safe_vector_metadata_creation_and_fields() -> None:
    metadata = build_safe_vector_metadata(**_base())
    assert len(metadata.keys()) == 21
    assert validate_vector_metadata(metadata)


def test_forbidden_key_and_content_rejected() -> None:
    bad = _base()
    bad["raw_document_text"] = "secret"
    assert not validate_vector_metadata(build_safe_vector_metadata(**_base()) | {"raw_document_text": "secret"})
    for v in ["raw chunk text", "password credential=abc", "api_key=xyz", "x@y.com"]:
        bad2 = build_safe_vector_metadata(**_base())
        bad2["content_type"] = v
        assert not validate_vector_metadata(bad2)
