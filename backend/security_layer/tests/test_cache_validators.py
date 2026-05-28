from backend.security_layer.cache.key_contract import REQUIRED_CACHE_KEY_FIELDS
from backend.security_layer.cache.models import (
    CacheACLContext,
    CacheDecisionStatus,
    CacheEntryMetadata,
    CacheKey,
    CacheOperationType,
    CacheProvenance,
    CacheSecurityContext,
    CacheSecurityStage,
    CacheSourceType,
)
from backend.security_layer.cache.validators import (
    build_cache_decision,
    validate_cache_acl_context,
    validate_cache_context,
    validate_cache_entry_metadata,
    validate_cache_entry_ttl,
    validate_cache_hit_authorization,
    validate_cache_invalidation_context,
    validate_cache_key_for_read,
    validate_cache_key_for_write,
    validate_cache_provenance,
    validate_cache_subject_context,
    validate_cache_tenant_context,
)


def _ctx(**kwargs: object) -> CacheSecurityContext:
    return CacheSecurityContext(
        stage=CacheSecurityStage.CACHE_READ_REQUESTED,
        operation=CacheOperationType.READ,
        request_id="req-1",
        tenant_id_hash_or_safe_id=kwargs.get("tenant", "tenant-safe"),
        workspace_id_hash_or_safe_id=kwargs.get("workspace", "workspace-safe"),
        subject_id_hash_or_safe_id=kwargs.get("subject", "subject-safe"),
        acl_context=kwargs.get("acl", CacheACLContext("acl-id", "v1", "2099-01-01T00:00:00Z")),
        provenance=kwargs.get("provenance", CacheProvenance("prov-1", CacheSourceType.SYSTEM)),
    )


def _meta(**kwargs: object) -> CacheEntryMetadata:
    key = {k: "safe" for k in REQUIRED_CACHE_KEY_FIELDS}
    key["cache_key_schema_version"] = "v1"
    key["cache_ttl_seconds"] = 60
    return CacheEntryMetadata(
        cache_key=CacheKey(key),
        cache_ttl_seconds=kwargs.get("ttl", 60),
        acl_snapshot_is_stale=kwargs.get("stale_acl", False),
        is_deleted_or_stale=kwargs.get("deleted_or_stale", False),
        connector_permission_drift=kwargs.get("permission_drift", False),
        cache_poisoning_marker=kwargs.get("cache_poisoning", False),
        prompt_injection_marker=kwargs.get("prompt_injection", False),
    )


def test_missing_tenant_subject_acl_provenance_denied_safely() -> None:
    assert not validate_cache_tenant_context(_ctx(tenant=None))
    assert not validate_cache_subject_context(_ctx(subject=None))
    assert not validate_cache_acl_context(_ctx(acl=None))
    assert not validate_cache_provenance(_ctx(provenance=None))


def test_invalid_cache_key_and_metadata_denied_safely() -> None:
    invalid_key = {k: "safe" for k in REQUIRED_CACHE_KEY_FIELDS if k != "cache_purpose"}
    assert not validate_cache_key_for_read(_ctx(), invalid_key)
    assert not validate_cache_key_for_write(_ctx(), invalid_key)
    assert not validate_cache_entry_metadata(_meta(ttl=0))
    assert not validate_cache_entry_ttl(_meta(ttl=0))


def test_stale_or_deleted_or_drift_or_attack_markers_flaggable() -> None:
    metadata = _meta(
        stale_acl=True,
        deleted_or_stale=True,
        permission_drift=True,
        cache_poisoning=True,
        prompt_injection=True,
    )
    assert metadata.acl_snapshot_is_stale
    assert metadata.is_deleted_or_stale
    assert metadata.connector_permission_drift
    assert metadata.cache_poisoning_marker
    assert metadata.prompt_injection_marker


def test_validate_cache_context_and_hit_authorization_paths() -> None:
    context = _ctx()
    metadata = _meta()
    assert validate_cache_context(context)
    assert validate_cache_invalidation_context(context)
    assert validate_cache_hit_authorization(context, metadata)


def test_decisions_do_not_include_raw_content_or_secrets() -> None:
    decision = build_cache_decision(
        context=_ctx(),
        status=CacheDecisionStatus.DENY,
        reason=(
            "query prompt document chunk token api_key credential "
            "raw_query_text raw_prompt_text raw_document_text raw_chunk_text"
        ),
    )
    lowered_reason = decision.reason.lower()
    assert "query" not in lowered_reason
    assert "prompt" not in lowered_reason
    assert "document" not in lowered_reason
    assert "chunk" not in lowered_reason
