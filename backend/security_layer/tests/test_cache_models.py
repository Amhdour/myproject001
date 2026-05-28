from backend.security_layer.cache.models import CacheACLContext, CacheOperationType, CacheProvenance, CachePurpose, CacheSecurityContext, CacheSecurityStage, CacheSourceType


def test_cache_security_context_creation() -> None:
    ctx = CacheSecurityContext(stage=CacheSecurityStage.CACHE_READ_REQUESTED, operation=CacheOperationType.READ, request_id="r1", tenant_id_hash_or_safe_id="t", workspace_id_hash_or_safe_id="w", subject_id_hash_or_safe_id="s", acl_context=CacheACLContext("a", "v", "e"), provenance=CacheProvenance("p", CacheSourceType.SYSTEM), cache_purpose=CachePurpose.RETRIEVAL_RESULT)
    assert ctx.tenant_id_hash_or_safe_id == "t"
