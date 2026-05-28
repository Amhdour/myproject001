from __future__ import annotations

import re

CACHE_KEY_SCHEMA_VERSION = "v1"
REQUIRED_CACHE_KEY_FIELDS = (
    "cache_key_schema_version",
    "tenant_id_hash_or_safe_id",
    "workspace_id_hash_or_safe_id",
    "subject_id_hash_or_safe_id",
    "subject_group_hashes_or_safe_ids",
    "subject_role_hashes_or_safe_ids",
    "acl_snapshot_id",
    "acl_snapshot_version",
    "acl_snapshot_expires_at",
    "provenance_id",
    "retrieval_scope_hash",
    "vector_namespace_hash",
    "source_type",
    "source_id_hash_or_safe_id",
    "document_id_hash_or_safe_id",
    "chunk_id_hash_or_safe_id",
    "query_hash",
    "prompt_context_hash",
    "cache_purpose",
    "cache_ttl_seconds",
    "sensitivity_label_placeholder",
)
OPTIONAL_CACHE_KEY_FIELDS = ("notes",)
FORBIDDEN_CACHE_KEY_FIELDS = (
    "raw_query_text", "raw_prompt_text", "raw_document_text", "raw_chunk_text", "source_secret",
    "api_key", "token", "credential", "connector_url", "email", "raw_policy", "raw_cache_backend",
)
_FORBIDDEN_PATTERNS = [r"sk-[A-Za-z0-9]{10,}", r"api[_-]?key", r"token", r"credential", r"password", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r"://[^\s]+:[^\s]+@"]

def build_safe_cache_key(**kwargs: object) -> dict[str, object]:
    key = {field: kwargs.get(field) for field in REQUIRED_CACHE_KEY_FIELDS}
    key["cache_key_schema_version"] = CACHE_KEY_SCHEMA_VERSION
    return sanitize_cache_key(key)

def validate_cache_key(cache_key: dict[str, object]) -> bool:
    return validate_cache_key_schema_version(cache_key) and all(f in cache_key for f in REQUIRED_CACHE_KEY_FIELDS) and validate_no_forbidden_cache_key_content(cache_key)

def validate_cache_key_schema_version(cache_key: dict[str, object]) -> bool:
    return cache_key.get("cache_key_schema_version") == CACHE_KEY_SCHEMA_VERSION

def validate_no_forbidden_cache_key_content(cache_key: dict[str, object]) -> bool:
    lowered_keys = {k.lower() for k in cache_key}
    if any(bad in lowered_keys for bad in FORBIDDEN_CACHE_KEY_FIELDS):
        return False
    serialized = str(cache_key).lower()
    return not any(re.search(pattern, serialized, re.IGNORECASE) for pattern in _FORBIDDEN_PATTERNS)

def sanitize_cache_key(cache_key: dict[str, object]) -> dict[str, object]:
    clean: dict[str, object] = {}
    for k, v in cache_key.items():
        if k in FORBIDDEN_CACHE_KEY_FIELDS:
            continue
        if isinstance(v, str):
            clean[k] = v.strip()
        else:
            clean[k] = v
    return clean
