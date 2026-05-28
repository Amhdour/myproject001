from __future__ import annotations

ARTIFACT_METADATA_SCHEMA_VERSION = "1.0"

REQUIRED_ARTIFACT_METADATA_FIELDS: tuple[str, ...] = (
    "artifact_id_hash_or_safe_id",
    "artifact_version",
    "tenant_id_hash_or_safe_id",
    "workspace_id_hash_or_safe_id",
    "subject_id_hash_or_safe_id",
    "source_type",
    "source_id_hash_or_safe_id",
    "storage_namespace",
    "storage_bucket_safe_id",
    "storage_object_safe_id",
    "checksum_sha256",
    "checksum_algorithm",
    "size_bytes",
    "content_type",
    "filename_safe",
    "created_at",
    "expires_at",
    "retention_class",
    "classification_label",
    "policy_pack_version",
    "release_policy_id",
    "release_policy_mode",
    "schema_contract_id",
    "schema_contract_version",
    "provenance_id",
    "ingestion_run_id",
    "acl_snapshot_id",
    "acl_snapshot_version",
    "acl_snapshot_created_at",
    "acl_snapshot_expires_at",
    "malware_scan_result",
    "secret_scan_result",
    "metadata_schema_version",
)

FORBIDDEN_ARTIFACT_METADATA_KEYS: tuple[str, ...] = (
    "raw_payload",
    "artifact_bytes",
    "secret",
    "api_key",
    "token",
)


def validate_artifact_metadata(metadata: dict[str, str | bool]) -> bool:
    for field in REQUIRED_ARTIFACT_METADATA_FIELDS:
        if field not in metadata:
            return False
        if metadata[field] == "":
            return False
    if metadata.get("metadata_schema_version") != ARTIFACT_METADATA_SCHEMA_VERSION:
        return False
    lowered = [k.lower() for k in metadata]
    for key in lowered:
        if key in FORBIDDEN_ARTIFACT_METADATA_KEYS:
            return False
    return True
