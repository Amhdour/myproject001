from __future__ import annotations

import re
from datetime import datetime
from urllib.parse import urlparse

VECTOR_METADATA_SCHEMA_VERSION = "1.0"
REQUIRED_VECTOR_METADATA_FIELDS: tuple[str, ...] = (
    "tenant_id_hash_or_safe_id",
    "workspace_id_hash_or_safe_id",
    "document_id_hash_or_safe_id",
    "chunk_id_hash_or_safe_id",
    "source_type",
    "source_id_hash_or_safe_id",
    "acl_snapshot_id",
    "acl_snapshot_version",
    "acl_snapshot_created_at",
    "acl_snapshot_expires_at",
    "document_deleted",
    "document_stale",
    "provenance_id",
    "ingestion_run_id",
    "embedding_model_id",
    "embedding_created_at",
    "content_type",
    "sensitivity_label_placeholder",
    "prompt_injection_flag",
    "poisoning_flag",
    "metadata_schema_version",
)
OPTIONAL_VECTOR_METADATA_FIELDS: tuple[str, ...] = ()
FORBIDDEN_VECTOR_METADATA_KEYS: tuple[str, ...] = (
    "raw_document_text",
    "raw_chunk_text",
    "document_text",
    "chunk_text",
    "policy_internal",
    "policy_debug",
    "secret",
    "api_key",
    "token",
    "credential",
)
_FORBIDDEN_VALUE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-[A-Za-z0-9]{8,}"),
    re.compile(r"(?i)api[_-]?key\s*[:=]"),
    re.compile(r"(?i)token\s*[:=]"),
    re.compile(r"(?i)credential\s*[:=]"),
    re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"(?i)raw\s*(document|chunk)\s*text"),
)


def sanitize_vector_metadata(metadata: dict[str, object]) -> dict[str, str | bool]:
    clean: dict[str, str | bool] = {}
    for k, v in metadata.items():
        if isinstance(v, bool):
            clean[k] = v
        elif v is None:
            clean[k] = ""
        else:
            clean[k] = str(v).strip()
    return clean


def build_safe_vector_metadata(**kwargs: object) -> dict[str, str | bool]:
    sanitized = sanitize_vector_metadata(kwargs)
    sanitized.setdefault("metadata_schema_version", VECTOR_METADATA_SCHEMA_VERSION)
    validate_vector_metadata(sanitized)
    return sanitized


def validate_metadata_schema_version(metadata: dict[str, str | bool]) -> bool:
    return metadata.get("metadata_schema_version") == VECTOR_METADATA_SCHEMA_VERSION


def validate_no_forbidden_metadata_content(metadata: dict[str, str | bool]) -> bool:
    for key, value in metadata.items():
        lowered = key.lower()
        if any(forbidden in lowered for forbidden in FORBIDDEN_VECTOR_METADATA_KEYS):
            return False
        if isinstance(value, bool):
            continue
        value_text = str(value)
        if _looks_like_secret_url(value_text):
            return False
        for pattern in _FORBIDDEN_VALUE_PATTERNS:
            if pattern.search(value_text):
                return False
    return True


def _looks_like_secret_url(value_text: str) -> bool:
    if "://" not in value_text:
        return False
    parsed = urlparse(value_text)
    return bool(parsed.username or parsed.password or parsed.query)


def validate_vector_metadata(metadata: dict[str, str | bool]) -> bool:
    for field in REQUIRED_VECTOR_METADATA_FIELDS:
        if field not in metadata:
            return False
        if field not in {"document_deleted", "document_stale", "prompt_injection_flag", "poisoning_flag"} and metadata[field] == "":
            return False
    return validate_metadata_schema_version(metadata) and validate_no_forbidden_metadata_content(metadata)
