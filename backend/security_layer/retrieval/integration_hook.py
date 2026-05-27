from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.retrieval.controls import authorize_document_acl_checked
from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig
from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationMode
from backend.security_layer.retrieval.integration_flags import is_enforce_mode
from backend.security_layer.retrieval.integration_flags import is_monitor_only
from backend.security_layer.retrieval.integration_flags import is_shadow_deny
from backend.security_layer.retrieval.models import RetrievalACLContext
from backend.security_layer.retrieval.models import RetrievalACLDecision
from backend.security_layer.retrieval.models import RetrievalCandidate
from backend.security_layer.retrieval.models import RetrievalDecisionStatus
from backend.security_layer.runtime.audit import AuditEvent
from backend.security_layer.runtime.audit import write_audit_event
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.findings import SecurityFinding
from backend.security_layer.runtime.findings import record_finding
from backend.security_layer.runtime.metrics import emit_security_metric


@dataclass(frozen=True)
class RetrievalHookResult:
    candidates: tuple[RetrievalCandidate, ...]
    decision: RetrievalACLDecision


def _evaluate(context: RetrievalACLContext, candidates: list[RetrievalCandidate]) -> RetrievalACLDecision:
    return authorize_document_acl_checked(context, candidates)


def apply_retrieval_acl_monitor_only(config: RetrievalIntegrationConfig, context: RetrievalACLContext, candidates: list[RetrievalCandidate]) -> RetrievalHookResult:
    _ = config
    decision = _evaluate(context, candidates)
    write_audit_event(AuditEvent(action=context.stage.value, decision=decision.status.value, mode="monitor_only", request_id=context.request_id))
    emit_security_metric(context.stage.value, decision.status.value, "monitor_only")
    return RetrievalHookResult(candidates=tuple(candidates), decision=decision)


def apply_retrieval_acl_shadow_deny(config: RetrievalIntegrationConfig, context: RetrievalACLContext, candidates: list[RetrievalCandidate]) -> RetrievalHookResult:
    _ = config
    decision = _evaluate(context, candidates)
    write_audit_event(AuditEvent(action=context.stage.value, decision=decision.status.value, mode="shadow_deny", request_id=context.request_id))
    emit_security_metric(context.stage.value, decision.status.value, "shadow_deny")
    if decision.denied_candidate_ids:
        record_finding(SecurityFinding(action=context.stage.value, reason_code="retrieval_acl_shadow_violation", request_id=context.request_id))
    return RetrievalHookResult(candidates=tuple(candidates), decision=decision)


def apply_retrieval_acl_enforce(config: RetrievalIntegrationConfig, context: RetrievalACLContext, candidates: list[RetrievalCandidate]) -> RetrievalHookResult:
    _ = config
    decision = _evaluate(context, candidates)
    allowed = tuple(decision.allowed_candidates)
    write_audit_event(AuditEvent(action=context.stage.value, decision=decision.status.value, mode="enforce", request_id=context.request_id))
    emit_security_metric(context.stage.value, decision.status.value, "enforce")
    if decision.denied_candidate_ids:
        record_finding(SecurityFinding(action=context.stage.value, reason_code="retrieval_acl_enforce_violation", request_id=context.request_id))
    if not allowed and candidates:
        decision = RetrievalACLDecision(
            stage=decision.stage,
            status=RetrievalDecisionStatus.DENY,
            allowed_candidates=(),
            denied_candidate_ids=decision.denied_candidate_ids,
            flags=decision.flags,
            denial_category=DenialCategory.RETRIEVAL_DENIED,
            reason="all candidates denied",
            metadata=decision.metadata,
        )
    return RetrievalHookResult(candidates=allowed, decision=decision)


def evaluate_retrieval_candidates_with_acl(config: RetrievalIntegrationConfig, context: RetrievalACLContext, candidates: list[RetrievalCandidate]) -> RetrievalHookResult:
    if config.mode == RetrievalIntegrationMode.DISABLED:
        decision = RetrievalACLDecision(
            stage=context.stage,
            status=RetrievalDecisionStatus.ALLOW,
            allowed_candidates=tuple(candidates),
            reason="retrieval acl disabled",
        )
        return RetrievalHookResult(candidates=tuple(candidates), decision=decision)
    if is_monitor_only(config):
        return apply_retrieval_acl_monitor_only(config, context, candidates)
    if is_shadow_deny(config):
        return apply_retrieval_acl_shadow_deny(config, context, candidates)
    if is_enforce_mode(config):
        return apply_retrieval_acl_enforce(config, context, candidates)
    raise ValueError("invalid retrieval integration mode")
