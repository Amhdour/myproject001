from __future__ import annotations

from backend.security_layer.retrieval.models import RetrievalACLContext
from backend.security_layer.retrieval.models import RetrievalCandidate
from backend.security_layer.retrieval.models import RetrievalDecisionStatus
from backend.security_layer.runtime.audit import AuditEvent
from backend.security_layer.runtime.audit import write_audit_event
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import SecurityFinding
from backend.security_layer.runtime.findings import record_finding
from backend.security_layer.runtime.metrics import emit_security_metric

from .validators import build_retrieval_decision
from .validators import filter_authorized_candidates
from .validators import validate_retrieval_scope
from .validators import validate_subject_context
from .validators import validate_tenant_context


def _basic_context_gate(context: RetrievalACLContext):
    if not validate_tenant_context(context):
        return build_retrieval_decision(
            context=context,
            status=RetrievalDecisionStatus.DENY,
            reason="tenant context missing",
            denial_category=DenialCategory.TENANT_CONTEXT_MISSING,
        )
    if not validate_subject_context(context):
        return build_retrieval_decision(
            context=context,
            status=RetrievalDecisionStatus.DENY,
            reason="subject context missing",
            denial_category=DenialCategory.SUBJECT_CONTEXT_MISSING,
        )
    return None


def _authorize_candidates(context: RetrievalACLContext, candidates: list[RetrievalCandidate]):
    basic = _basic_context_gate(context)
    if basic:
        return basic
    if not validate_retrieval_scope(context):
        return build_retrieval_decision(
            context=context,
            status=RetrievalDecisionStatus.DENY,
            reason="retrieval scope missing",
            denial_category=DenialCategory.VALIDATION_FAILED,
        )
    allowed, denied, categories = filter_authorized_candidates(context, candidates)
    status = RetrievalDecisionStatus.ALLOW if not denied else RetrievalDecisionStatus.FILTER
    denial = categories[0] if categories else None
    decision = build_retrieval_decision(
        context=context,
        status=status,
        reason="candidate acl evaluated",
        denial_category=denial,
        allowed_candidates=allowed,
        denied_candidate_ids=denied,
        flags=["unauthorized_candidates_filtered"] if denied else [],
    )
    emit_security_metric(context.stage.value, decision.status.value, "isolated")
    if denied:
        record_finding(
            SecurityFinding(action=context.stage.value, reason_code="retrieval_acl_violation", request_id=context.request_id)
        )
    return decision


def authorize_query_received(context: RetrievalACLContext): return _basic_context_gate(context) or build_retrieval_decision(context=context, status=RetrievalDecisionStatus.ALLOW, reason="query received")
def authorize_subject_context_validated(context: RetrievalACLContext): return authorize_query_received(context)
def authorize_tenant_context_validated(context: RetrievalACLContext): return authorize_query_received(context)
def authorize_retrieval_scope_resolved(context: RetrievalACLContext):
    basic = _basic_context_gate(context)
    if basic: return basic
    if not validate_retrieval_scope(context):
        return build_retrieval_decision(context=context, status=RetrievalDecisionStatus.DENY, reason="retrieval scope missing", denial_category=DenialCategory.VALIDATION_FAILED)
    return build_retrieval_decision(context=context, status=RetrievalDecisionStatus.ALLOW, reason="scope resolved")
def authorize_candidate_sources_resolved(context: RetrievalACLContext): return authorize_retrieval_scope_resolved(context)
def authorize_document_acl_checked(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_chunk_acl_checked(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_vector_namespace_checked(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_vector_metadata_checked(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_hybrid_search_filtered(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_rerank_candidates_filtered(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_citation_sources_filtered(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_context_chunks_authorized(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_prompt_context_authorized(context: RetrievalACLContext, candidates: list[RetrievalCandidate]): return _authorize_candidates(context, candidates)
def authorize_cache_read_authorized(context: RetrievalACLContext):
    basic = _basic_context_gate(context)
    if basic: return basic
    if not context.cache_acl_context_key or context.cache_acl_context_key != f"{context.tenant.tenant_id}:{context.subject.subject_id}":
        return build_retrieval_decision(context=context, status=RetrievalDecisionStatus.DENY, reason="cache acl mismatch", denial_category=DenialCategory.RETRIEVAL_DENIED)
    return build_retrieval_decision(context=context, status=RetrievalDecisionStatus.ALLOW, reason="cache acl valid")
def authorize_retrieval_audit_written(context: RetrievalACLContext):
    write_audit_event(AuditEvent(action=context.stage.value, decision="allow", mode="isolated", request_id=context.request_id))
    return build_retrieval_decision(context=context, status=RetrievalDecisionStatus.ALLOW, reason="audit written")
def authorize_retrieval_finding_recorded_if_needed(context: RetrievalACLContext):
    emit_security_metric(context.stage.value, "allow", "isolated")
    return build_retrieval_decision(context=context, status=RetrievalDecisionStatus.ALLOW, reason="finding stage evaluated")
