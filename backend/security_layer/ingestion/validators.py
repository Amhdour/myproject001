from __future__ import annotations

from backend.security_layer.ingestion.models import ACLSnapshot
from backend.security_layer.ingestion.models import IngestionDecisionStatus
from backend.security_layer.ingestion.models import IngestionSecurityContext
from backend.security_layer.ingestion.models import IngestionSecurityDecision
from backend.security_layer.ingestion.models import IngestionStage
from backend.security_layer.ingestion.models import ProvenanceRecord
from backend.security_layer.runtime.denials import DenialCategory

_ALLOWED_CONTENT_TYPES = {
    "text/plain",
    "text/markdown",
    "application/pdf",
    "application/json",
}
_PROMPT_MARKERS = ("ignore previous instructions", "system prompt", "developer instructions")
_POISONING_MARKERS = ("hidden instruction", "model backdoor", "poison")


def validate_tenant_context(context: IngestionSecurityContext) -> bool:
    return bool(context.tenant_id and context.tenant_id.strip())


def validate_subject_context(context: IngestionSecurityContext) -> bool:
    return bool(context.subject_id and context.subject_id.strip())


def validate_source_metadata(context: IngestionSecurityContext) -> bool:
    if not context.source_id:
        return False
    for key, value in context.source_metadata.items():
        if any(token in key.lower() for token in ("secret", "token", "password", "key")):
            return False
        if any(token in value.lower() for token in ("secret", "token", "password", "sk-")):
            return False
    return True


def validate_acl_snapshot(context: IngestionSecurityContext) -> bool:
    snapshot = context.acl_snapshot
    if snapshot is None:
        return False
    return snapshot.captured_at is not None and snapshot.acl_entries_count >= 0 and not snapshot.is_stale


def validate_content_type(content_type: str | None) -> bool:
    return bool(content_type and content_type in _ALLOWED_CONTENT_TYPES)


def validate_file_size(size_bytes: int | None, max_size_bytes: int | None) -> bool:
    if size_bytes is None or max_size_bytes is None:
        return False
    return 0 <= size_bytes <= max_size_bytes


def validate_file_count(file_count: int | None, max_file_count: int | None) -> bool:
    if file_count is None or max_file_count is None:
        return False
    return 0 <= file_count <= max_file_count


def validate_provenance(provenance: ProvenanceRecord | None) -> bool:
    if provenance is None:
        return False
    return bool(provenance.source_id and provenance.checksum)


def detect_prompt_injection_markers(text_sample: str | None) -> bool:
    if not text_sample:
        return False
    scanned = text_sample[:500].lower()
    return any(marker in scanned for marker in _PROMPT_MARKERS)


def detect_poisoning_markers(text_sample: str | None) -> bool:
    if not text_sample:
        return False
    scanned = text_sample[:500].lower()
    return any(marker in scanned for marker in _POISONING_MARKERS)


def build_ingestion_decision(
    *,
    stage: IngestionStage,
    status: IngestionDecisionStatus,
    reason: str,
    denial_category: DenialCategory | None = None,
    flags: tuple[str, ...] = (),
) -> IngestionSecurityDecision:
    sanitized_reason = reason.replace("\n", " ")[:240]
    return IngestionSecurityDecision(
        status=status,
        stage=stage,
        reason=sanitized_reason,
        denial_category=denial_category,
        flags=flags,
    )


def _placeholder_noop_scanner(_: str | None) -> bool:
    return False


def placeholder_malware_scan(text_sample: str | None) -> bool:
    return _placeholder_noop_scanner(text_sample)


def placeholder_dlp_scan(text_sample: str | None) -> bool:
    return _placeholder_noop_scanner(text_sample)
