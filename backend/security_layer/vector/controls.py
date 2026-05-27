from __future__ import annotations

from backend.security_layer.runtime.audit import AuditEvent, write_audit_event
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import SecurityFinding, record_finding
from backend.security_layer.runtime.metrics import emit_security_metric
from backend.security_layer.vector.models import VectorCandidate, VectorDecisionStatus, VectorSecurityContext
from backend.security_layer.vector.validators import (
    build_vector_decision,
    filter_authorized_vector_candidates,
    validate_vector_acl_snapshot,
    validate_vector_context,
    validate_vector_namespace_authorization,
    validate_vector_provenance,
    validate_vector_write_metadata,
)


def _deny(context: VectorSecurityContext, reason: str, category: DenialCategory):
    emit_security_metric(context.stage.value, VectorDecisionStatus.DENY.value, "inactive")
    return build_vector_decision(context=context, status=VectorDecisionStatus.DENY, reason=reason, denial_category=category)


def authorize_vector_write_requested(context: VectorSecurityContext):
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="write request accepted")


def authorize_vector_write_context_validated(context: VectorSecurityContext):
    if not context.tenant_id_hash_or_safe_id:
        return _deny(context, "missing tenant", DenialCategory.TENANT_CONTEXT_MISSING)
    if not context.subject_id_hash_or_safe_id:
        return _deny(context, "missing subject", DenialCategory.SUBJECT_CONTEXT_MISSING)
    if not validate_vector_context(context):
        return _deny(context, "invalid context", DenialCategory.VALIDATION_FAILED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="context validated")


def authorize_vector_namespace_resolved(context: VectorSecurityContext):
    if not context.namespace.name:
        return _deny(context, "namespace missing", DenialCategory.VALIDATION_FAILED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="namespace resolved")


def authorize_vector_namespace_authorized(context: VectorSecurityContext):
    if not validate_vector_namespace_authorization(context, context.namespace.name):
        return _deny(context, "namespace mismatch", DenialCategory.ACCESS_DENIED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="namespace authorized")


def authorize_vector_metadata_validated(context: VectorSecurityContext):
    if context.metadata is None or not validate_vector_write_metadata(context, context.metadata.values):
        return _deny(context, "invalid metadata", DenialCategory.VALIDATION_FAILED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="metadata validated")


def authorize_vector_acl_snapshot_attached(context: VectorSecurityContext):
    if context.metadata is None or not validate_vector_acl_snapshot(context.metadata.values):
        return _deny(context, "missing or stale acl snapshot", DenialCategory.VALIDATION_FAILED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="acl snapshot attached")


def authorize_vector_provenance_attached(context: VectorSecurityContext):
    if context.metadata is None or not validate_vector_provenance(context.metadata.values):
        return _deny(context, "missing provenance", DenialCategory.VALIDATION_FAILED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="provenance attached")


def authorize_vector_embedding_metadata_attached(context: VectorSecurityContext):
    if context.embedding_metadata is None:
        return _deny(context, "missing embedding metadata", DenialCategory.VALIDATION_FAILED)
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="embedding metadata attached")


def authorize_vector_write_committed(context: VectorSecurityContext):
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="isolated write control completed")


def authorize_vector_query_requested(context: VectorSecurityContext):
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="query request accepted")


def authorize_vector_query_context_validated(context: VectorSecurityContext):
    return authorize_vector_write_context_validated(context)


def authorize_vector_search_filter_built(context: VectorSecurityContext):
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="isolated search filter built")


def authorize_vector_candidates_returned(context: VectorSecurityContext, candidates: list[VectorCandidate]):
    _ = candidates
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="candidates handled")


def authorize_vector_candidate_metadata_checked(context: VectorSecurityContext, candidates: list[VectorCandidate]):
    allowed, denied, flags = filter_authorized_vector_candidates(context, candidates)
    status = VectorDecisionStatus.ALLOW if not denied else VectorDecisionStatus.FILTER
    return build_vector_decision(
        context=context,
        status=status,
        reason="candidate metadata checked",
        allowed_candidate_ids=[c.candidate_id for c in allowed],
        denied_candidate_ids=denied,
        flags=flags,
    )


def authorize_vector_deleted_or_stale_filtered(context: VectorSecurityContext, candidates: list[VectorCandidate]):
    return authorize_vector_candidate_metadata_checked(context, candidates)


def authorize_vector_cache_checked(context: VectorSecurityContext):
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="cache check isolated")


def authorize_vector_audit_written(context: VectorSecurityContext):
    write_audit_event(AuditEvent(action=context.stage.value, decision="allow", mode="inactive", request_id=context.request_id))
    emit_security_metric(context.stage.value, "allow", "inactive")
    return build_vector_decision(context=context, status=VectorDecisionStatus.ALLOW, reason="audit emitted")


def authorize_vector_finding_recorded_if_needed(context: VectorSecurityContext):
    record_finding(SecurityFinding(action=context.stage.value, reason_code="vector_security_flag", request_id=context.request_id))
    emit_security_metric(context.stage.value, "flag", "inactive")
    return build_vector_decision(context=context, status=VectorDecisionStatus.FLAG, reason="finding emitted")
