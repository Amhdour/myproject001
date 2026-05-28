from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from backend.security_layer.runtime.denials import DenialCategory


class CacheSecurityStage(str, Enum):
    CACHE_KEY_BUILD_REQUESTED = "cache_key_build_requested"
    CACHE_KEY_CONTEXT_VALIDATED = "cache_key_context_validated"
    CACHE_KEY_TENANT_BOUND = "cache_key_tenant_bound"
    CACHE_KEY_SUBJECT_BOUND = "cache_key_subject_bound"
    CACHE_KEY_ACL_BOUND = "cache_key_acl_bound"
    CACHE_KEY_PROVENANCE_BOUND = "cache_key_provenance_bound"
    CACHE_READ_REQUESTED = "cache_read_requested"
    CACHE_READ_AUTHORIZED = "cache_read_authorized"
    CACHE_HIT_VALIDATED = "cache_hit_validated"
    CACHE_MISS_RECORDED = "cache_miss_recorded"
    CACHE_WRITE_REQUESTED = "cache_write_requested"
    CACHE_WRITE_AUTHORIZED = "cache_write_authorized"
    CACHE_ENTRY_METADATA_VALIDATED = "cache_entry_metadata_validated"
    CACHE_ENTRY_TTL_VALIDATED = "cache_entry_ttl_validated"
    CACHE_INVALIDATION_REQUESTED = "cache_invalidation_requested"
    CACHE_ACL_SNAPSHOT_INVALIDATED = "cache_acl_snapshot_invalidated"
    CACHE_DELETED_OR_STALE_INVALIDATED = "cache_deleted_or_stale_invalidated"
    CACHE_AUDIT_WRITTEN = "cache_audit_written"
    CACHE_FINDING_RECORDED_IF_NEEDED = "cache_finding_recorded_if_needed"


class CacheDecisionStatus(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    FLAG = "flag"


class CacheOperationType(str, Enum):
    READ = "read"
    WRITE = "write"
    INVALIDATE = "invalidate"


class CachePurpose(str, Enum):
    RETRIEVAL_RESULT = "retrieval_result"
    PROMPT_CONTEXT = "prompt_context"


class CacheSourceType(str, Enum):
    CONNECTOR = "connector"
    USER_UPLOAD = "user_upload"
    SYSTEM = "system"


@dataclass(frozen=True)
class CacheKey:
    fields: dict[str, object]


@dataclass(frozen=True)
class CacheEntryMetadata:
    cache_key: CacheKey
    cache_ttl_seconds: int
    acl_snapshot_is_stale: bool = False
    is_deleted_or_stale: bool = False
    connector_permission_drift: bool = False
    cache_poisoning_marker: bool = False
    prompt_injection_marker: bool = False


@dataclass(frozen=True)
class CacheACLContext:
    acl_snapshot_id: str | None
    acl_snapshot_version: str | None
    acl_snapshot_expires_at: str | None


@dataclass(frozen=True)
class CacheProvenance:
    provenance_id: str | None
    source_type: CacheSourceType


@dataclass(frozen=True)
class CacheSecurityContext:
    stage: CacheSecurityStage
    operation: CacheOperationType
    request_id: str
    tenant_id_hash_or_safe_id: str | None
    workspace_id_hash_or_safe_id: str | None
    subject_id_hash_or_safe_id: str | None
    subject_group_hashes_or_safe_ids: tuple[str, ...] = ()
    subject_role_hashes_or_safe_ids: tuple[str, ...] = ()
    acl_context: CacheACLContext | None = None
    provenance: CacheProvenance | None = None
    cache_purpose: CachePurpose = CachePurpose.RETRIEVAL_RESULT


@dataclass(frozen=True)
class CacheSecurityDecision:
    stage: CacheSecurityStage
    status: CacheDecisionStatus
    reason: str
    denial_category: DenialCategory | None = None
    flags: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CacheFinding:
    request_id: str
    stage: CacheSecurityStage
    reason_code: str
