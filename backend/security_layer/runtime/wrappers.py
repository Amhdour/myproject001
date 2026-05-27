from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable

from backend.security_layer.policies.models import PolicyEffect
from backend.security_layer.runtime.audit import AuditEvent
from backend.security_layer.runtime.audit import write_audit_event
from backend.security_layer.runtime.contexts import RuntimeAction
from backend.security_layer.runtime.contexts import SecurityDecisionContext
from backend.security_layer.runtime.contexts import has_required_identity
from backend.security_layer.runtime.contexts import has_required_tenant
from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.denials import approval_required_payload
from backend.security_layer.runtime.denials import raise_security_denial
from backend.security_layer.runtime.findings import SecurityFinding
from backend.security_layer.runtime.findings import record_finding
from backend.security_layer.runtime.metrics import emit_security_metric


class WrapperMode(str, Enum):
    ENFORCE = "enforce"
    MONITOR_ONLY = "monitor_only"
    SHADOW_DENY = "shadow_deny"


@dataclass(frozen=True)
class WrapperDecision:
    action: str
    decision: str
    mode: str
    approval_required: bool = False
    denial_payload: dict[str, str] | None = None


def _normalize_mode(mode: WrapperMode | str) -> WrapperMode:
    return mode if isinstance(mode, WrapperMode) else WrapperMode(mode)


def _evaluate(
    action: RuntimeAction,
    context: SecurityDecisionContext,
    policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None,
    mode: WrapperMode | str,
) -> WrapperDecision:
    normalized_mode = _normalize_mode(mode)
    if not has_required_identity(context):
        _record(action, "deny", normalized_mode, context, "missing_subject")
        raise_security_denial(DenialCategory.SUBJECT_CONTEXT_MISSING)
    if not has_required_tenant(context):
        _record(action, "deny", normalized_mode, context, "missing_tenant")
        raise_security_denial(DenialCategory.TENANT_CONTEXT_MISSING)

    if policy_evaluator is None:
        if normalized_mode == WrapperMode.ENFORCE:
            _record(action, "deny", normalized_mode, context, "evaluator_unavailable")
            raise_security_denial(DenialCategory.POLICY_ENGINE_UNAVAILABLE)
        _record(action, "allow", normalized_mode, context)
        return WrapperDecision(action.value, "allow", normalized_mode.value)

    try:
        result = policy_evaluator(action, context)
    except Exception:
        if normalized_mode == WrapperMode.ENFORCE:
            _record(action, "deny", normalized_mode, context, "evaluation_error")
            raise_security_denial(DenialCategory.POLICY_DENIED)
        _record(action, "allow", normalized_mode, context)
        return WrapperDecision(action.value, "allow", normalized_mode.value)

    effect = result if isinstance(result, str) else getattr(result, "effect", "deny")
    effect_value = effect.value if isinstance(effect, PolicyEffect) else str(effect)

    if effect_value == PolicyEffect.DENY.value:
        if normalized_mode == WrapperMode.MONITOR_ONLY:
            _record(action, "allow", normalized_mode, context)
            return WrapperDecision(action.value, "allow", normalized_mode.value)
        if normalized_mode == WrapperMode.SHADOW_DENY:
            _record(action, "shadow_deny", normalized_mode, context, "shadow_denied")
            return WrapperDecision(action.value, "shadow_deny", normalized_mode.value)
        _record(action, "deny", normalized_mode, context, "denied")
        raise_security_denial(DenialCategory.POLICY_DENIED)

    if effect_value == PolicyEffect.APPROVAL_REQUIRED.value:
        _record(action, "approval_required", normalized_mode, context)
        return WrapperDecision(action.value, "approval_required", normalized_mode.value, approval_required=True, denial_payload=approval_required_payload())

    _record(action, "allow", normalized_mode, context)
    return WrapperDecision(action.value, "allow", normalized_mode.value)


def _record(action: RuntimeAction, decision: str, mode: WrapperMode, context: SecurityDecisionContext, reason: str | None = None) -> None:
    write_audit_event(AuditEvent(action=action.value, decision=decision, mode=mode.value, request_id=context.request.request_id))
    emit_security_metric(action.value, decision, mode.value)
    if decision in {"deny", "shadow_deny"}:
        record_finding(SecurityFinding(action=action.value, reason_code=reason or "security_denied", request_id=context.request.request_id))


def authorize_ingestion(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.INGESTION, context, policy_evaluator, mode)

def authorize_retrieval(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.RETRIEVAL, context, policy_evaluator, mode)

def authorize_vector_query(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.VECTOR_QUERY, context, policy_evaluator, mode)

def authorize_cache_access(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.CACHE_ACCESS, context, policy_evaluator, mode)

def authorize_tool_call(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.TOOL_CALL, context, policy_evaluator, mode)

def authorize_mcp_action(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.MCP_ACTION, context, policy_evaluator, mode)

def authorize_artifact_release(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.ARTIFACT_RELEASE, context, policy_evaluator, mode)

def authorize_sandbox_execution(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.SANDBOX_EXECUTION, context, policy_evaluator, mode)

def authorize_model_call(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.MODEL_CALL, context, policy_evaluator, mode)

def authorize_prompt_use(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.PROMPT_USE, context, policy_evaluator, mode)

def require_human_approval(context: SecurityDecisionContext, policy_evaluator: Callable[[RuntimeAction, SecurityDecisionContext], Any] | None = None, mode: WrapperMode | str = WrapperMode.ENFORCE) -> WrapperDecision:
    return _evaluate(RuntimeAction.HUMAN_APPROVAL, context, policy_evaluator, mode)
