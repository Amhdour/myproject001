from __future__ import annotations

from datetime import datetime, timezone

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.vector.metadata_contract import validate_vector_metadata
from backend.security_layer.vector.models import VectorCandidate
from backend.security_layer.vector.models import VectorDecisionStatus
from backend.security_layer.vector.models import VectorSecurityContext
from backend.security_layer.vector.models import VectorSecurityDecision


def validate_vector_tenant_context(context: VectorSecurityContext) -> bool:
    return bool(context.tenant_id_hash_or_safe_id)


def validate_vector_subject_context(context: VectorSecurityContext) -> bool:
    return bool(context.subject_id_hash_or_safe_id)


def validate_vector_namespace(context: VectorSecurityContext) -> bool:
    return bool(context.namespace.name)


def validate_vector_namespace_authorization(context: VectorSecurityContext, namespace: str) -> bool:
    return namespace in context.authorized_namespaces


def validate_vector_context(context: VectorSecurityContext) -> bool:
    return validate_vector_tenant_context(context) and validate_vector_subject_context(context) and validate_vector_namespace(context)


def validate_vector_write_metadata(context: VectorSecurityContext, metadata: dict[str, str | bool]) -> bool:
    _ = context
    return validate_vector_metadata(metadata)


def validate_vector_read_metadata(context: VectorSecurityContext, metadata: dict[str, str | bool]) -> bool:
    _ = context
    return validate_vector_metadata(metadata)


def validate_vector_acl_snapshot(metadata: dict[str, str | bool]) -> bool:
    if not metadata.get("acl_snapshot_id") or not metadata.get("acl_snapshot_version"):
        return False
    expires_at = metadata.get("acl_snapshot_expires_at")
    if not isinstance(expires_at, str):
        return False
    return datetime.fromisoformat(expires_at) > datetime.now(timezone.utc)


def validate_vector_provenance(metadata: dict[str, str | bool]) -> bool:
    return bool(metadata.get("provenance_id") and metadata.get("ingestion_run_id"))


def validate_deleted_or_stale_vector(metadata: dict[str, str | bool]) -> bool:
    return not (bool(metadata.get("document_deleted")) or bool(metadata.get("document_stale")))


def validate_vector_candidate(context: VectorSecurityContext, candidate: VectorCandidate) -> bool:
    if candidate.namespace.name != context.namespace.name:
        return False
    if not validate_vector_read_metadata(context, candidate.metadata.values):
        return False
    return validate_vector_acl_snapshot(candidate.metadata.values) and validate_vector_provenance(candidate.metadata.values)


def filter_authorized_vector_candidates(
    context: VectorSecurityContext, candidates: list[VectorCandidate]
) -> tuple[list[VectorCandidate], list[str], list[str]]:
    allowed: list[VectorCandidate] = []
    denied_ids: list[str] = []
    flags: list[str] = []
    for candidate in candidates:
        if not validate_vector_candidate(context, candidate):
            denied_ids.append(candidate.candidate_id)
            continue
        if not validate_deleted_or_stale_vector(candidate.metadata.values):
            denied_ids.append(candidate.candidate_id)
            flags.append("deleted_or_stale")
            continue
        if bool(candidate.metadata.values.get("prompt_injection_flag")):
            flags.append("prompt_injection_marker")
        if bool(candidate.metadata.values.get("poisoning_flag")):
            flags.append("poisoning_marker")
        allowed.append(candidate)
    return allowed, denied_ids, flags


def build_vector_decision(*, context: VectorSecurityContext, status: VectorDecisionStatus, reason: str, denial_category: DenialCategory | None = None, allowed_candidate_ids: list[str] | None = None, denied_candidate_ids: list[str] | None = None, flags: list[str] | None = None) -> VectorSecurityDecision:
    return VectorSecurityDecision(
        stage=context.stage,
        status=status,
        reason=reason.replace("text", "[redacted]"),
        denial_category=denial_category,
        allowed_candidate_ids=tuple(allowed_candidate_ids or []),
        denied_candidate_ids=tuple(denied_candidate_ids or []),
        flags=tuple(flags or []),
    )
