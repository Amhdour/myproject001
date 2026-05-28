from backend.security_layer.cache.controls import authorize_cache_acl_snapshot_invalidated, authorize_cache_audit_written, authorize_cache_deleted_or_stale_invalidated, authorize_cache_entry_metadata_validated, authorize_cache_finding_recorded_if_needed, authorize_cache_key_subject_bound, authorize_cache_key_tenant_bound, authorize_cache_key_acl_bound, authorize_cache_key_provenance_bound
from backend.security_layer.cache.key_contract import REQUIRED_CACHE_KEY_FIELDS
from backend.security_layer.cache.models import CacheACLContext, CacheDecisionStatus, CacheEntryMetadata, CacheKey, CacheOperationType, CacheProvenance, CacheSecurityContext, CacheSecurityStage, CacheSourceType
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics


def _ctx(**kw):
    return CacheSecurityContext(stage=CacheSecurityStage.CACHE_AUDIT_WRITTEN, operation=CacheOperationType.READ, request_id="r1", tenant_id_hash_or_safe_id=kw.get("tenant", "t"), workspace_id_hash_or_safe_id=kw.get("ws", "w"), subject_id_hash_or_safe_id=kw.get("subject", "s"), acl_context=kw.get("acl", CacheACLContext("a", "v", "e")), provenance=kw.get("prov", CacheProvenance("p", CacheSourceType.SYSTEM)))


def _meta(**kwargs):
    key = {k: "x" for k in REQUIRED_CACHE_KEY_FIELDS}
    key["cache_key_schema_version"] = "v1"
    key["cache_ttl_seconds"] = 60
    return CacheEntryMetadata(cache_key=CacheKey(key), cache_ttl_seconds=kwargs.get("ttl", 60), acl_snapshot_is_stale=kwargs.get("stale", False), is_deleted_or_stale=kwargs.get("deleted", False), connector_permission_drift=kwargs.get("drift", False), cache_poisoning_marker=kwargs.get("poison", False), prompt_injection_marker=kwargs.get("inject", False))


def test_denials_and_flags_and_events() -> None:
    assert authorize_cache_key_tenant_bound(_ctx(tenant=None)).status == CacheDecisionStatus.DENY
    assert authorize_cache_key_subject_bound(_ctx(subject=None)).status == CacheDecisionStatus.DENY
    assert authorize_cache_key_acl_bound(_ctx(acl=None)).status == CacheDecisionStatus.DENY
    assert authorize_cache_key_provenance_bound(_ctx(prov=None)).status == CacheDecisionStatus.DENY
    assert authorize_cache_entry_metadata_validated(_ctx(), _meta(ttl=-1)).status == CacheDecisionStatus.DENY
    assert "stale_acl_snapshot" in authorize_cache_acl_snapshot_invalidated(_ctx(), _meta(stale=True)).flags
    flags = authorize_cache_deleted_or_stale_invalidated(_ctx(), _meta(deleted=True, drift=True, poison=True, inject=True)).flags
    assert set(flags) >= {"deleted_or_stale_cache_entry", "connector_permission_drift", "cache_poisoning_marker", "prompt_injection_marker"}

    clear_audit_events(); clear_findings(); clear_security_metrics()
    authorize_cache_audit_written(_ctx())
    authorize_cache_finding_recorded_if_needed(_ctx(), "x")
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()
