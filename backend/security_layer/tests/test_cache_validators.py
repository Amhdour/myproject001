from backend.security_layer.cache.key_contract import REQUIRED_CACHE_KEY_FIELDS
from backend.security_layer.cache.models import CacheACLContext, CacheEntryMetadata, CacheKey, CacheOperationType, CacheProvenance, CacheSecurityContext, CacheSecurityStage, CacheSourceType
from backend.security_layer.cache.validators import validate_cache_context, validate_cache_entry_metadata


def _ctx():
    return CacheSecurityContext(stage=CacheSecurityStage.CACHE_READ_REQUESTED, operation=CacheOperationType.READ, request_id="r1", tenant_id_hash_or_safe_id="t", workspace_id_hash_or_safe_id="w", subject_id_hash_or_safe_id="s", acl_context=CacheACLContext("a", "v", "e"), provenance=CacheProvenance("p", CacheSourceType.SYSTEM))


def _meta(**kwargs):
    key = {k: "x" for k in REQUIRED_CACHE_KEY_FIELDS}
    key["cache_key_schema_version"] = "v1"
    key["cache_ttl_seconds"] = 60
    return CacheEntryMetadata(cache_key=CacheKey(key), cache_ttl_seconds=kwargs.get("ttl", 60), acl_snapshot_is_stale=kwargs.get("stale", False), is_deleted_or_stale=kwargs.get("deleted", False), connector_permission_drift=kwargs.get("drift", False), cache_poisoning_marker=kwargs.get("poison", False), prompt_injection_marker=kwargs.get("inject", False))


def test_validator_basics() -> None:
    assert validate_cache_context(_ctx())
    assert validate_cache_entry_metadata(_meta())
