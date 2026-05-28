from backend.security_layer.cache import controls
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
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics


def _ctx(stage: CacheSecurityStage = CacheSecurityStage.CACHE_READ_REQUESTED, **kwargs: object) -> CacheSecurityContext:
    return CacheSecurityContext(
        stage=stage,
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


def test_all_19_stage_controls_have_isolated_authorizers() -> None:
    stage_to_fn = {
        CacheSecurityStage.CACHE_KEY_BUILD_REQUESTED: controls.authorize_cache_key_build_requested,
        CacheSecurityStage.CACHE_KEY_CONTEXT_VALIDATED: controls.authorize_cache_key_context_validated,
        CacheSecurityStage.CACHE_KEY_TENANT_BOUND: controls.authorize_cache_key_tenant_bound,
        CacheSecurityStage.CACHE_KEY_SUBJECT_BOUND: controls.authorize_cache_key_subject_bound,
        CacheSecurityStage.CACHE_KEY_ACL_BOUND: controls.authorize_cache_key_acl_bound,
        CacheSecurityStage.CACHE_KEY_PROVENANCE_BOUND: controls.authorize_cache_key_provenance_bound,
        CacheSecurityStage.CACHE_READ_REQUESTED: controls.authorize_cache_read_requested,
        CacheSecurityStage.CACHE_READ_AUTHORIZED: controls.authorize_cache_read_authorized,
        CacheSecurityStage.CACHE_HIT_VALIDATED: controls.authorize_cache_hit_validated,
        CacheSecurityStage.CACHE_MISS_RECORDED: controls.authorize_cache_miss_recorded,
        CacheSecurityStage.CACHE_WRITE_REQUESTED: controls.authorize_cache_write_requested,
        CacheSecurityStage.CACHE_WRITE_AUTHORIZED: controls.authorize_cache_write_authorized,
        CacheSecurityStage.CACHE_ENTRY_METADATA_VALIDATED: controls.authorize_cache_entry_metadata_validated,
        CacheSecurityStage.CACHE_ENTRY_TTL_VALIDATED: controls.authorize_cache_entry_ttl_validated,
        CacheSecurityStage.CACHE_INVALIDATION_REQUESTED: controls.authorize_cache_invalidation_requested,
        CacheSecurityStage.CACHE_ACL_SNAPSHOT_INVALIDATED: controls.authorize_cache_acl_snapshot_invalidated,
        CacheSecurityStage.CACHE_DELETED_OR_STALE_INVALIDATED: controls.authorize_cache_deleted_or_stale_invalidated,
        CacheSecurityStage.CACHE_AUDIT_WRITTEN: controls.authorize_cache_audit_written,
        CacheSecurityStage.CACHE_FINDING_RECORDED_IF_NEEDED: controls.authorize_cache_finding_recorded_if_needed,
    }
    assert len(stage_to_fn) == 19


def test_denials_and_marker_flags_and_in_memory_helpers() -> None:
    assert controls.authorize_cache_key_tenant_bound(_ctx(tenant=None)).status == CacheDecisionStatus.DENY
    assert controls.authorize_cache_key_subject_bound(_ctx(subject=None)).status == CacheDecisionStatus.DENY
    assert controls.authorize_cache_key_acl_bound(_ctx(acl=None)).status == CacheDecisionStatus.DENY
    assert controls.authorize_cache_key_provenance_bound(_ctx(provenance=None)).status == CacheDecisionStatus.DENY
    assert controls.authorize_cache_entry_metadata_validated(_ctx(), _meta(ttl=-1)).status == CacheDecisionStatus.DENY

    flags = controls.authorize_cache_deleted_or_stale_invalidated(
        _ctx(), _meta(deleted_or_stale=True, permission_drift=True, cache_poisoning=True, prompt_injection=True)
    ).flags
    assert set(flags) >= {
        "deleted_or_stale_cache_entry",
        "connector_permission_drift",
        "cache_poisoning_marker",
        "prompt_injection_marker",
    }

    assert "stale_acl_snapshot" in controls.authorize_cache_acl_snapshot_invalidated(_ctx(), _meta(stale_acl=True)).flags

    clear_audit_events()
    clear_findings()
    clear_security_metrics()
    controls.authorize_cache_audit_written(_ctx(CacheSecurityStage.CACHE_AUDIT_WRITTEN))
    controls.authorize_cache_finding_recorded_if_needed(_ctx(CacheSecurityStage.CACHE_FINDING_RECORDED_IF_NEEDED), "reason")
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()
