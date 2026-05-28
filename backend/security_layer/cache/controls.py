from __future__ import annotations

from backend.security_layer.cache.key_contract import validate_cache_key
from backend.security_layer.cache.models import CacheDecisionStatus, CacheEntryMetadata, CacheSecurityContext
from backend.security_layer.cache.validators import build_cache_decision, validate_cache_acl_context, validate_cache_context, validate_cache_entry_metadata, validate_cache_entry_ttl, validate_cache_provenance, validate_cache_subject_context, validate_cache_tenant_context
from backend.security_layer.runtime.audit import AuditEvent, write_audit_event
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import SecurityFinding, record_finding
from backend.security_layer.runtime.metrics import emit_security_metric


def _deny(context: CacheSecurityContext, category: DenialCategory, reason: str):
    emit_security_metric(context.stage.value, "deny", "isolated")
    return build_cache_decision(context=context, status=CacheDecisionStatus.DENY, reason=reason, denial_category=category)

def _allow(context: CacheSecurityContext, flags: list[str] | None = None):
    emit_security_metric(context.stage.value, "allow", "isolated")
    return build_cache_decision(context=context, status=CacheDecisionStatus.ALLOW, reason="safe_allow", flags=flags or [])

def authorize_cache_key_build_requested(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_key_context_validated(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_key_tenant_bound(context: CacheSecurityContext):
    return _allow(context) if validate_cache_tenant_context(context) else _deny(context, DenialCategory.TENANT_CONTEXT_MISSING, "missing_tenant")
def authorize_cache_key_subject_bound(context: CacheSecurityContext):
    return _allow(context) if validate_cache_subject_context(context) else _deny(context, DenialCategory.SUBJECT_CONTEXT_MISSING, "missing_subject")
def authorize_cache_key_acl_bound(context: CacheSecurityContext):
    return _allow(context) if validate_cache_acl_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "missing_acl")
def authorize_cache_key_provenance_bound(context: CacheSecurityContext):
    return _allow(context) if validate_cache_provenance(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "missing_provenance")
def authorize_cache_read_requested(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_read_authorized(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_hit_validated(context: CacheSecurityContext):
    return _allow(context)
def authorize_cache_miss_recorded(context: CacheSecurityContext):
    return _allow(context)
def authorize_cache_write_requested(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_write_authorized(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_entry_metadata_validated(context: CacheSecurityContext, metadata: CacheEntryMetadata | None = None):
    return _allow(context) if (metadata and validate_cache_entry_metadata(metadata)) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_cache_metadata")
def authorize_cache_entry_ttl_validated(context: CacheSecurityContext, metadata: CacheEntryMetadata | None = None):
    return _allow(context) if (metadata and validate_cache_entry_ttl(metadata)) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_ttl")
def authorize_cache_invalidation_requested(context: CacheSecurityContext):
    return _allow(context) if validate_cache_context(context) else _deny(context, DenialCategory.VALIDATION_FAILED, "invalid_context")
def authorize_cache_acl_snapshot_invalidated(context: CacheSecurityContext, metadata: CacheEntryMetadata | None = None):
    return _allow(context, ["stale_acl_snapshot"]) if (metadata and metadata.acl_snapshot_is_stale) else _allow(context)
def authorize_cache_deleted_or_stale_invalidated(context: CacheSecurityContext, metadata: CacheEntryMetadata | None = None):
    flags = []
    if metadata:
        if metadata.is_deleted_or_stale: flags.append("deleted_or_stale_cache_entry")
        if metadata.connector_permission_drift: flags.append("connector_permission_drift")
        if metadata.cache_poisoning_marker: flags.append("cache_poisoning_marker")
        if metadata.prompt_injection_marker: flags.append("prompt_injection_marker")
    return _allow(context, flags)
def authorize_cache_audit_written(context: CacheSecurityContext):
    write_audit_event(AuditEvent(action=context.stage.value, decision="allow", mode="isolated", request_id=context.request_id, details={"operation": context.operation.value}))
    return _allow(context)
def authorize_cache_finding_recorded_if_needed(context: CacheSecurityContext, reason_code: str | None = None):
    if reason_code:
        record_finding(SecurityFinding(action=context.stage.value, reason_code=reason_code, request_id=context.request_id))
    return _allow(context)
