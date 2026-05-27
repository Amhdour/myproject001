from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from backend.security_layer.runtime.denials import DenialCategory


class VectorSecurityStage(str, Enum):
    WRITE_REQUESTED = "write_requested"
    WRITE_CONTEXT_VALIDATED = "write_context_validated"
    NAMESPACE_RESOLVED = "namespace_resolved"
    NAMESPACE_AUTHORIZED = "namespace_authorized"
    METADATA_VALIDATED = "metadata_validated"
    ACL_SNAPSHOT_ATTACHED = "acl_snapshot_attached"
    PROVENANCE_ATTACHED = "provenance_attached"
    EMBEDDING_METADATA_ATTACHED = "embedding_metadata_attached"
    WRITE_COMMITTED = "write_committed"
    QUERY_REQUESTED = "query_requested"
    QUERY_CONTEXT_VALIDATED = "query_context_validated"
    SEARCH_FILTER_BUILT = "search_filter_built"
    CANDIDATES_RETURNED = "candidates_returned"
    CANDIDATE_METADATA_CHECKED = "candidate_metadata_checked"
    DELETED_OR_STALE_FILTERED = "deleted_or_stale_filtered"
    CACHE_CHECKED = "cache_checked"
    AUDIT_WRITTEN = "audit_written"
    FINDING_RECORDED_IF_NEEDED = "finding_recorded_if_needed"


class VectorDecisionStatus(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    FILTER = "filter"
    FLAG = "flag"


class VectorOperationType(str, Enum):
    WRITE = "write"
    READ = "read"
    DELETE = "delete"
    QUERY = "query"


class VectorSourceType(str, Enum):
    CONNECTOR = "connector"
    USER_UPLOAD = "user_upload"
    API = "api"
    SYSTEM = "system"


@dataclass(frozen=True)
class VectorNamespace:
    name: str


@dataclass(frozen=True)
class VectorMetadata:
    values: dict[str, str | bool]


@dataclass(frozen=True)
class VectorACLSnapshot:
    snapshot_id: str
    version: str
    created_at: datetime
    expires_at: datetime


@dataclass(frozen=True)
class VectorProvenance:
    provenance_id: str
    ingestion_run_id: str
    source_type: VectorSourceType
    source_id_hash_or_safe_id: str


@dataclass(frozen=True)
class VectorEmbeddingMetadata:
    embedding_model_id: str
    embedding_created_at: datetime
    content_type: str
    sensitivity_label_placeholder: str


@dataclass(frozen=True)
class VectorSecurityContext:
    request_id: str
    operation_type: VectorOperationType
    stage: VectorSecurityStage
    tenant_id_hash_or_safe_id: str | None
    workspace_id_hash_or_safe_id: str | None
    subject_id_hash_or_safe_id: str | None
    namespace: VectorNamespace
    authorized_namespaces: tuple[str, ...] = ()
    metadata: VectorMetadata | None = None
    acl_snapshot: VectorACLSnapshot | None = None
    provenance: VectorProvenance | None = None
    embedding_metadata: VectorEmbeddingMetadata | None = None


@dataclass(frozen=True)
class VectorCandidate:
    candidate_id: str
    namespace: VectorNamespace
    metadata: VectorMetadata


@dataclass(frozen=True)
class VectorSecurityDecision:
    stage: VectorSecurityStage
    status: VectorDecisionStatus
    reason: str
    denial_category: DenialCategory | None = None
    allowed_candidate_ids: tuple[str, ...] = ()
    denied_candidate_ids: tuple[str, ...] = ()
    flags: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class VectorFinding:
    request_id: str
    stage: VectorSecurityStage
    reason_code: str
    candidate_id: str | None = None
