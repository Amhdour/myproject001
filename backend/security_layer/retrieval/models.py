from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from backend.security_layer.runtime.denials import DenialCategory


class RetrievalStage(str, Enum):
    QUERY_RECEIVED = "query_received"
    SUBJECT_CONTEXT_VALIDATED = "subject_context_validated"
    TENANT_CONTEXT_VALIDATED = "tenant_context_validated"
    RETRIEVAL_SCOPE_RESOLVED = "retrieval_scope_resolved"
    CANDIDATE_SOURCES_RESOLVED = "candidate_sources_resolved"
    DOCUMENT_ACL_CHECKED = "document_acl_checked"
    CHUNK_ACL_CHECKED = "chunk_acl_checked"
    VECTOR_NAMESPACE_CHECKED = "vector_namespace_checked"
    VECTOR_METADATA_CHECKED = "vector_metadata_checked"
    HYBRID_SEARCH_FILTERED = "hybrid_search_filtered"
    RERANK_CANDIDATES_FILTERED = "rerank_candidates_filtered"
    CITATION_SOURCES_FILTERED = "citation_sources_filtered"
    CONTEXT_CHUNKS_AUTHORIZED = "context_chunks_authorized"
    PROMPT_CONTEXT_AUTHORIZED = "prompt_context_authorized"
    CACHE_READ_AUTHORIZED = "cache_read_authorized"
    RETRIEVAL_AUDIT_WRITTEN = "retrieval_audit_written"
    RETRIEVAL_FINDING_RECORDED_IF_NEEDED = "retrieval_finding_recorded_if_needed"


class RetrievalDecisionStatus(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    FILTER = "filter"
    FLAG = "flag"


class RetrievalSourceType(str, Enum):
    VECTOR = "vector"
    KEYWORD = "keyword"
    HYBRID = "hybrid"
    CACHE = "cache"


@dataclass(frozen=True)
class ACLDecision:
    is_allowed: bool
    reason: str


@dataclass(frozen=True)
class ACLSnapshot:
    captured_at: datetime
    acl_entries_count: int
    is_stale: bool = False


@dataclass(frozen=True)
class RetrievalSubject:
    subject_id: str | None
    group_ids: tuple[str, ...] = ()
    role_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievalTenant:
    tenant_id: str | None


@dataclass(frozen=True)
class RetrievalDocument:
    document_id: str
    tenant_id: str
    allowed_subject_ids: tuple[str, ...] = ()
    allowed_group_ids: tuple[str, ...] = ()
    allowed_role_ids: tuple[str, ...] = ()
    is_deleted: bool = False


@dataclass(frozen=True)
class RetrievalChunk:
    chunk_id: str
    document_id: str
    tenant_id: str
    allowed_subject_ids: tuple[str, ...] = ()
    allowed_group_ids: tuple[str, ...] = ()
    allowed_role_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class VectorNamespace:
    namespace: str


@dataclass(frozen=True)
class VectorMetadata:
    tenant_id: str
    document_id: str
    chunk_id: str


@dataclass(frozen=True)
class RetrievalCandidate:
    candidate_id: str
    source_type: RetrievalSourceType
    document: RetrievalDocument
    chunk: RetrievalChunk
    vector_namespace: VectorNamespace
    vector_metadata: VectorMetadata
    provenance_id: str


@dataclass(frozen=True)
class RetrievalACLContext:
    subject: RetrievalSubject
    tenant: RetrievalTenant
    stage: RetrievalStage
    source_type: RetrievalSourceType
    request_id: str
    retrieval_scope: tuple[str, ...] = ()
    acl_snapshot: ACLSnapshot | None = None
    expected_vector_namespace: str | None = None
    cache_acl_context_key: str | None = None


@dataclass(frozen=True)
class RetrievalACLDecision:
    stage: RetrievalStage
    status: RetrievalDecisionStatus
    allowed_candidates: tuple[RetrievalCandidate, ...] = ()
    denied_candidate_ids: tuple[str, ...] = ()
    flags: tuple[str, ...] = ()
    denial_category: DenialCategory | None = None
    reason: str = ""
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class RetrievalFinding:
    request_id: str
    stage: RetrievalStage
    reason_code: str
    candidate_id: str | None = None
