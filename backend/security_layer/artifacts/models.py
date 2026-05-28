from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from backend.security_layer.runtime.denials import DenialCategory


class ArtifactSafetyStage(str, Enum):
    UPLOAD_REQUESTED = "upload_requested"
    REQUEST_CONTEXT_VALIDATED = "request_context_validated"
    TENANT_BOUNDARY_VALIDATED = "tenant_boundary_validated"
    WORKSPACE_BOUNDARY_VALIDATED = "workspace_boundary_validated"
    SUBJECT_BOUNDARY_VALIDATED = "subject_boundary_validated"
    STORAGE_NAMESPACE_RESOLVED = "storage_namespace_resolved"
    STORAGE_NAMESPACE_AUTHORIZED = "storage_namespace_authorized"
    METADATA_SCHEMA_VALIDATED = "metadata_schema_validated"
    METADATA_REQUIRED_FIELDS_VALIDATED = "metadata_required_fields_validated"
    METADATA_FORBIDDEN_FIELDS_VALIDATED = "metadata_forbidden_fields_validated"
    CONTENT_TYPE_VALIDATED = "content_type_validated"
    CONTENT_SIZE_VALIDATED = "content_size_validated"
    CONTENT_MALWARE_SCANNED = "content_malware_scanned"
    CONTENT_SECRET_SCANNED = "content_secret_scanned"
    CONTENT_POLICY_MARKER_SCANNED = "content_policy_marker_scanned"
    HASH_COMPUTED = "hash_computed"
    INTEGRITY_BOUND = "integrity_bound"
    PROVENANCE_ATTACHED = "provenance_attached"
    RETENTION_POLICY_VALIDATED = "retention_policy_validated"
    RELEASE_POLICY_VALIDATED = "release_policy_validated"
    AUDIT_WRITTEN = "audit_written"
    FINDING_RECORDED_IF_NEEDED = "finding_recorded_if_needed"
    SAFE_REFERENCE_PUBLISHED = "safe_reference_published"
    CONTROL_FLOW_COMPLETED = "control_flow_completed"


class ArtifactDecisionStatus(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    FILTER = "filter"
    FLAG = "flag"


@dataclass(frozen=True)
class ArtifactMetadata:
    values: dict[str, str | bool]


@dataclass(frozen=True)
class ArtifactSecurityContext:
    request_id: str
    stage: ArtifactSafetyStage
    tenant_id_hash_or_safe_id: str | None
    workspace_id_hash_or_safe_id: str | None
    subject_id_hash_or_safe_id: str | None
    storage_namespace: str
    authorized_storage_namespaces: tuple[str, ...] = ()
    metadata: ArtifactMetadata | None = None


@dataclass(frozen=True)
class ArtifactSecurityDecision:
    stage: ArtifactSafetyStage
    status: ArtifactDecisionStatus
    reason: str
    denial_category: DenialCategory | None = None
    flags: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ArtifactFinding:
    request_id: str
    stage: ArtifactSafetyStage
    reason_code: str


@dataclass(frozen=True)
class ArtifactProvenance:
    provenance_id: str
    ingestion_run_id: str
    created_at: datetime
