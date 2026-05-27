from __future__ import annotations

from backend.security_layer.ingestion.models import IngestionDecisionStatus
from backend.security_layer.ingestion.models import IngestionSecurityContext
from backend.security_layer.ingestion.models import IngestionStage
from backend.security_layer.runtime.audit import AuditEvent
from backend.security_layer.runtime.audit import write_audit_event
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import SecurityFinding
from backend.security_layer.runtime.findings import record_finding
from backend.security_layer.runtime.metrics import emit_security_metric
from backend.security_layer.ingestion.validators import build_ingestion_decision
from backend.security_layer.ingestion.validators import detect_poisoning_markers
from backend.security_layer.ingestion.validators import detect_prompt_injection_markers
from backend.security_layer.ingestion.validators import validate_acl_snapshot
from backend.security_layer.ingestion.validators import validate_content_type
from backend.security_layer.ingestion.validators import validate_file_count
from backend.security_layer.ingestion.validators import validate_file_size
from backend.security_layer.ingestion.validators import validate_provenance
from backend.security_layer.ingestion.validators import validate_source_metadata
from backend.security_layer.ingestion.validators import validate_subject_context
from backend.security_layer.ingestion.validators import validate_tenant_context


def _decision(context: IngestionSecurityContext, status: IngestionDecisionStatus, reason: str, denial: DenialCategory | None = None, flags: tuple[str, ...] = ()):
    emit_security_metric(action=context.stage.value, decision=status.value, mode="isolated")
    write_audit_event(AuditEvent(action=context.stage.value, decision=status.value, mode="isolated", request_id=context.request_id))
    if flags:
        for flag in flags:
            record_finding(SecurityFinding(action=context.stage.value, reason_code=flag, request_id=context.request_id))
    return build_ingestion_decision(stage=context.stage, status=status, reason=reason, denial_category=denial, flags=flags)


def _base_authorize(context: IngestionSecurityContext):
    if not validate_tenant_context(context):
        return _decision(context, IngestionDecisionStatus.DENY, "Tenant context missing.", DenialCategory.TENANT_CONTEXT_MISSING)
    if not validate_subject_context(context):
        return _decision(context, IngestionDecisionStatus.DENY, "Subject context missing.", DenialCategory.SUBJECT_CONTEXT_MISSING)
    if not validate_source_metadata(context):
        return _decision(context, IngestionDecisionStatus.DENY, "Source metadata validation failed.", DenialCategory.VALIDATION_FAILED)
    flags: list[str] = []
    if detect_prompt_injection_markers(context.text_sample):
        flags.append("prompt_injection_marker")
    if detect_poisoning_markers(context.text_sample):
        flags.append("poisoning_marker")
    status = IngestionDecisionStatus.FLAG if flags else IngestionDecisionStatus.ALLOW
    return _decision(context, status, "Stage authorized in isolated mode.", flags=tuple(flags))


def authorize_upload_received(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_connector_sync_started(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_source_metadata_validated(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_tenant_boundary_validated(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_ownership_validated(context: IngestionSecurityContext): return _base_authorize(context)

def authorize_acl_snapshot_captured(context: IngestionSecurityContext):
    base = _base_authorize(context)
    if base.status == IngestionDecisionStatus.DENY:
        return base
    if not validate_acl_snapshot(context):
        return _decision(context, IngestionDecisionStatus.DENY, "ACL snapshot missing or stale.", DenialCategory.VALIDATION_FAILED)
    return base


def authorize_content_type_validated(context: IngestionSecurityContext):
    base = _base_authorize(context)
    if base.status == IngestionDecisionStatus.DENY:
        return base
    if not validate_content_type(context.content_type):
        return _decision(context, IngestionDecisionStatus.DENY, "Content type rejected.", DenialCategory.VALIDATION_FAILED)
    return base


def authorize_file_size_validated(context: IngestionSecurityContext):
    base = _base_authorize(context)
    if base.status == IngestionDecisionStatus.DENY:
        return base
    if not validate_file_size(context.size_bytes, context.max_size_bytes):
        return _decision(context, IngestionDecisionStatus.DENY, "File size exceeds policy.", DenialCategory.VALIDATION_FAILED)
    if not validate_file_count(context.file_count, context.max_file_count):
        return _decision(context, IngestionDecisionStatus.DENY, "File count exceeds policy.", DenialCategory.VALIDATION_FAILED)
    return base


def authorize_parser_selected(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_parser_completed(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_chunks_created(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_chunk_metadata_attached(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_embedding_requested(context: IngestionSecurityContext): return _base_authorize(context)

def authorize_vector_write_authorized(context: IngestionSecurityContext):
    base = _base_authorize(context)
    if base.status == IngestionDecisionStatus.DENY:
        return base
    if not validate_provenance(context.provenance):
        return _decision(context, IngestionDecisionStatus.DENY, "Provenance missing.", DenialCategory.VALIDATION_FAILED)
    return base

def authorize_provenance_recorded(context: IngestionSecurityContext): return authorize_vector_write_authorized(context)
def authorize_ingestion_audit_written(context: IngestionSecurityContext): return _base_authorize(context)
def authorize_ingestion_finding_recorded_if_needed(context: IngestionSecurityContext): return _base_authorize(context)
