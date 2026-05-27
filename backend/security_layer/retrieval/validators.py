from __future__ import annotations

from backend.security_layer.retrieval.models import RetrievalACLContext
from backend.security_layer.retrieval.models import RetrievalACLDecision
from backend.security_layer.retrieval.models import RetrievalCandidate
from backend.security_layer.retrieval.models import RetrievalDecisionStatus
from backend.security_layer.retrieval.models import RetrievalStage
from backend.security_layer.runtime.denials import DenialCategory


def validate_subject_context(context: RetrievalACLContext) -> bool:
    return bool(context.subject.subject_id)


def validate_tenant_context(context: RetrievalACLContext) -> bool:
    return bool(context.tenant.tenant_id)


def validate_retrieval_scope(context: RetrievalACLContext) -> bool:
    return bool(context.retrieval_scope)


def validate_document_acl(context: RetrievalACLContext, candidate: RetrievalCandidate) -> bool:
    subject_id = context.subject.subject_id
    if candidate.document.is_deleted or subject_id is None:
        return False
    if context.tenant.tenant_id != candidate.document.tenant_id:
        return False
    if subject_id in candidate.document.allowed_subject_ids:
        return True
    if set(context.subject.group_ids).intersection(candidate.document.allowed_group_ids):
        return True
    return bool(set(context.subject.role_ids).intersection(candidate.document.allowed_role_ids))


def validate_chunk_acl(context: RetrievalACLContext, candidate: RetrievalCandidate) -> bool:
    subject_id = context.subject.subject_id
    if subject_id is None or context.tenant.tenant_id != candidate.chunk.tenant_id:
        return False
    if subject_id in candidate.chunk.allowed_subject_ids:
        return True
    if set(context.subject.group_ids).intersection(candidate.chunk.allowed_group_ids):
        return True
    return bool(set(context.subject.role_ids).intersection(candidate.chunk.allowed_role_ids))


def validate_vector_namespace(context: RetrievalACLContext, candidate: RetrievalCandidate) -> bool:
    return context.expected_vector_namespace is None or context.expected_vector_namespace == candidate.vector_namespace.namespace


def validate_vector_metadata(context: RetrievalACLContext, candidate: RetrievalCandidate) -> bool:
    tenant_id = context.tenant.tenant_id
    return (
        tenant_id == candidate.vector_metadata.tenant_id
        and candidate.document.document_id == candidate.vector_metadata.document_id
        and candidate.chunk.chunk_id == candidate.vector_metadata.chunk_id
    )


def validate_acl_snapshot_freshness(context: RetrievalACLContext, candidate: RetrievalCandidate) -> bool:
    _ = candidate
    return context.acl_snapshot is not None and not context.acl_snapshot.is_stale


def validate_deleted_document_state(candidate: RetrievalCandidate) -> bool:
    return not candidate.document.is_deleted


def filter_authorized_candidates(
    context: RetrievalACLContext, candidates: list[RetrievalCandidate]
) -> tuple[list[RetrievalCandidate], list[str], list[DenialCategory]]:
    allowed: list[RetrievalCandidate] = []
    denied: list[str] = []
    categories: list[DenialCategory] = []
    for candidate in candidates:
        checks = (
            (validate_deleted_document_state(candidate), DenialCategory.RETRIEVAL_DENIED),
            (validate_acl_snapshot_freshness(context, candidate), DenialCategory.VALIDATION_FAILED),
            (validate_document_acl(context, candidate), DenialCategory.RETRIEVAL_DENIED),
            (validate_chunk_acl(context, candidate), DenialCategory.RETRIEVAL_DENIED),
            (validate_vector_namespace(context, candidate), DenialCategory.RETRIEVAL_DENIED),
            (validate_vector_metadata(context, candidate), DenialCategory.RETRIEVAL_DENIED),
        )
        if all(ok for ok, _ in checks):
            allowed.append(candidate)
        else:
            denied.append(candidate.candidate_id)
            categories.extend(category for ok, category in checks if not ok)
    return allowed, denied, categories


def build_retrieval_decision(
    *,
    context: RetrievalACLContext,
    status: RetrievalDecisionStatus,
    reason: str,
    denial_category: DenialCategory | None = None,
    allowed_candidates: list[RetrievalCandidate] | None = None,
    denied_candidate_ids: list[str] | None = None,
    flags: list[str] | None = None,
    metadata: dict[str, str] | None = None,
) -> RetrievalACLDecision:
    safe_reason = reason.replace("text", "[redacted]")
    return RetrievalACLDecision(
        stage=context.stage,
        status=status,
        reason=safe_reason,
        denial_category=denial_category,
        allowed_candidates=tuple(allowed_candidates or []),
        denied_candidate_ids=tuple(denied_candidate_ids or []),
        flags=tuple(flags or []),
        metadata=metadata or {},
    )
