from __future__ import annotations

from backend.security_layer.cache.key_contract import validate_cache_key
from backend.security_layer.cache.models import CacheDecisionStatus, CacheEntryMetadata, CacheSecurityContext, CacheSecurityDecision
from backend.security_layer.runtime.denials import DenialCategory


def validate_cache_tenant_context(context: CacheSecurityContext) -> bool:
    return bool(context.tenant_id_hash_or_safe_id and context.workspace_id_hash_or_safe_id)

def validate_cache_subject_context(context: CacheSecurityContext) -> bool:
    return bool(context.subject_id_hash_or_safe_id)

def validate_cache_acl_context(context: CacheSecurityContext) -> bool:
    return bool(context.acl_context and context.acl_context.acl_snapshot_id)

def validate_cache_provenance(context: CacheSecurityContext) -> bool:
    return bool(context.provenance and context.provenance.provenance_id)

def validate_cache_context(context: CacheSecurityContext) -> bool:
    return all((validate_cache_tenant_context(context), validate_cache_subject_context(context), validate_cache_acl_context(context), validate_cache_provenance(context)))

def validate_cache_key_for_read(context: CacheSecurityContext, cache_key: dict[str, object]) -> bool:
    _ = context
    return validate_cache_key(cache_key)

def validate_cache_key_for_write(context: CacheSecurityContext, cache_key: dict[str, object]) -> bool:
    _ = context
    return validate_cache_key(cache_key)

def validate_cache_entry_metadata(metadata: CacheEntryMetadata) -> bool:
    return validate_cache_key(metadata.cache_key.fields) and metadata.cache_ttl_seconds > 0

def validate_cache_entry_ttl(metadata: CacheEntryMetadata) -> bool:
    return metadata.cache_ttl_seconds > 0

def validate_cache_hit_authorization(context: CacheSecurityContext, metadata: CacheEntryMetadata) -> bool:
    return validate_cache_context(context) and validate_cache_entry_metadata(metadata)

def validate_cache_invalidation_context(context: CacheSecurityContext) -> bool:
    return validate_cache_context(context)

def validate_deleted_or_stale_cache_entry(metadata: CacheEntryMetadata) -> bool:
    return metadata.is_deleted_or_stale

def validate_connector_permission_drift(metadata: CacheEntryMetadata) -> bool:
    return metadata.connector_permission_drift

def build_cache_decision(*, context: CacheSecurityContext, status: CacheDecisionStatus, reason: str, denial_category: DenialCategory | None = None, flags: list[str] | None = None, metadata: dict[str, str] | None = None) -> CacheSecurityDecision:
    safe_reason = reason.replace("query", "[redacted]").replace("prompt", "[redacted]").replace("document", "[redacted]").replace("chunk", "[redacted]")
    return CacheSecurityDecision(stage=context.stage, status=status, reason=safe_reason, denial_category=denial_category, flags=tuple(flags or []), metadata=metadata or {})
