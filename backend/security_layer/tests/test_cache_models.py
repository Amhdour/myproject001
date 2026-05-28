from backend.security_layer.cache.models import (
    CacheACLContext,
    CacheOperationType,
    CacheProvenance,
    CachePurpose,
    CacheSecurityContext,
    CacheSecurityStage,
    CacheSourceType,
)


def test_cache_security_stage_has_19_isolated_stages() -> None:
    assert len(CacheSecurityStage) == 19


def test_cache_security_context_explicit_security_fields_present() -> None:
    ctx = CacheSecurityContext(
        stage=CacheSecurityStage.CACHE_READ_REQUESTED,
        operation=CacheOperationType.READ,
        request_id="r1",
        tenant_id_hash_or_safe_id="tenant-safe",
        workspace_id_hash_or_safe_id="workspace-safe",
        subject_id_hash_or_safe_id="subject-safe",
        subject_group_hashes_or_safe_ids=("group-a", "group-b"),
        subject_role_hashes_or_safe_ids=("role-reader",),
        acl_context=CacheACLContext("acl-id", "v1", "2099-01-01T00:00:00Z"),
        provenance=CacheProvenance("prov-1", CacheSourceType.SYSTEM),
        cache_purpose=CachePurpose.RETRIEVAL_RESULT,
    )
    assert ctx.tenant_id_hash_or_safe_id == "tenant-safe"
    assert ctx.workspace_id_hash_or_safe_id == "workspace-safe"
    assert ctx.subject_group_hashes_or_safe_ids == ("group-a", "group-b")
    assert ctx.subject_role_hashes_or_safe_ids == ("role-reader",)
    assert ctx.cache_purpose == CachePurpose.RETRIEVAL_RESULT
