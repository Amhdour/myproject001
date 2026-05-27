from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from backend.security_layer.runtime.denials import DenialCategory


class IngestionStage(str, Enum):
    UPLOAD_RECEIVED = "upload_received"
    CONNECTOR_SYNC_STARTED = "connector_sync_started"
    SOURCE_METADATA_VALIDATED = "source_metadata_validated"
    TENANT_BOUNDARY_VALIDATED = "tenant_boundary_validated"
    OWNERSHIP_VALIDATED = "ownership_validated"
    ACL_SNAPSHOT_CAPTURED = "acl_snapshot_captured"
    CONTENT_TYPE_VALIDATED = "content_type_validated"
    FILE_SIZE_VALIDATED = "file_size_validated"
    PARSER_SELECTED = "parser_selected"
    PARSER_COMPLETED = "parser_completed"
    CHUNKS_CREATED = "chunks_created"
    CHUNK_METADATA_ATTACHED = "chunk_metadata_attached"
    EMBEDDING_REQUESTED = "embedding_requested"
    VECTOR_WRITE_AUTHORIZED = "vector_write_authorized"
    PROVENANCE_RECORDED = "provenance_recorded"
    INGESTION_AUDIT_WRITTEN = "ingestion_audit_written"
    INGESTION_FINDING_RECORDED_IF_NEEDED = "ingestion_finding_recorded_if_needed"


class IngestionDecisionStatus(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    FLAG = "flag"


class IngestionSourceType(str, Enum):
    USER_UPLOAD = "user_upload"
    CONNECTOR = "connector"
    API = "api"


@dataclass(frozen=True)
class ContentValidationResult:
    is_valid: bool
    content_type_allowed: bool = True
    file_size_allowed: bool = True
    file_count_allowed: bool = True
    flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class MetadataValidationResult:
    is_valid: bool
    issues: tuple[str, ...] = ()


@dataclass(frozen=True)
class ACLSnapshot:
    captured_at: datetime | None
    acl_entries_count: int
    is_stale: bool = False


@dataclass(frozen=True)
class ProvenanceRecord:
    source_id: str
    source_type: IngestionSourceType
    ingested_at: datetime
    checksum: str


@dataclass(frozen=True)
class IngestionSecurityContext:
    tenant_id: str | None
    subject_id: str | None
    stage: IngestionStage
    source_type: IngestionSourceType
    source_id: str | None
    source_metadata: dict[str, str] = field(default_factory=dict)
    acl_snapshot: ACLSnapshot | None = None
    provenance: ProvenanceRecord | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    file_count: int | None = None
    max_size_bytes: int | None = None
    max_file_count: int | None = None
    text_sample: str | None = None
    request_id: str = ""


@dataclass(frozen=True)
class IngestionSecurityDecision:
    status: IngestionDecisionStatus
    stage: IngestionStage
    reason: str
    denial_category: DenialCategory | None = None
    flags: tuple[str, ...] = ()


@dataclass(frozen=True)
class IngestionFinding:
    stage: IngestionStage
    finding_code: str
    severity: str
    summary: str
