from __future__ import annotations

import re

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
    "raw_artifact_content",
    "raw_query_text",
    "raw_prompt_text",
    "raw_document_text",
    "raw_chunk_text",
    "source_secret",
    "api_key",
    "token",
    "credential",
    "private_key",
    "password",
    "connector_url",
    "email",
    "tenant_internal_id",
    "source_internal_config",
    "policy_internal_rules",
)

_FORBIDDEN_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)api[_-]?key"),
    re.compile(r"(?i)token"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)password|credential"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"(?i)raw_(?:artifact|query|prompt|document|chunk)_text|raw_artifact_content"),
    re.compile(r"(?i)tenant_internal|source_internal|policy_internal|source_secret"),
)


def sanitize_metadata_for_decision(metadata: dict[str, str | bool]) -> dict[str, str]:
    safe: dict[str, str] = {}
    allowlist = {
        "artifact_id_hash_or_safe_id",
        "tenant_id_hash_or_safe_id",
        "workspace_id_hash_or_safe_id",
        "subject_id_hash_or_safe_id",
        "source_type",
        "release_policy_id",
        "release_policy_mode",
        "retention_class",
        "classification_label",
        "metadata_schema_version",
    }
    for key in allowlist:
        value = metadata.get(key)
        safe[key] = "" if value is None else str(value)
    return safe


def validate_artifact_metadata(metadata: dict[str, str | bool]) -> bool:
    for field in REQUIRED_ARTIFACT_METADATA_FIELDS:
        if field not in metadata or metadata[field] == "":
            return False

    if metadata.get("metadata_schema_version") != ARTIFACT_METADATA_SCHEMA_VERSION:
        return False

    lowered = {k.lower(): k for k in metadata}
    if any(key in lowered for key in FORBIDDEN_ARTIFACT_METADATA_KEYS):
        return False

    for value in metadata.values():
        text = str(value)
        if any(pattern.search(text) for pattern in _FORBIDDEN_PATTERNS):
            return False

    return True
