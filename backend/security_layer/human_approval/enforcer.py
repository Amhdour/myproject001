from __future__ import annotations

from collections.abc import Mapping

from backend.security_layer.human_approval.models import AgentActionContext
from backend.security_layer.human_approval.models import AgentActionRequest
from backend.security_layer.human_approval.models import HumanApprovalDecision
from backend.security_layer.human_approval.models import HumanApprovalPolicy
from backend.security_layer.human_approval.models import HumanApprovalReason
from backend.security_layer.human_approval.models import HumanApprovalRecord


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_string_frozenset(value: object) -> bool:
    return isinstance(value, frozenset) and all(_is_non_empty_string(item) for item in value)


def _is_well_formed_context(context: object) -> bool:
    if not isinstance(context, AgentActionContext):
        return False
    return (
        _is_non_empty_string(context.tenant_id)
        and _is_non_empty_string(context.subject_id)
        and _is_string_frozenset(context.role_ids)
    )


def _is_well_formed_request(request: object) -> bool:
    if not isinstance(request, AgentActionRequest):
        return False
    return (
        _is_non_empty_string(request.request_id)
        and _is_non_empty_string(request.tenant_id)
        and _is_non_empty_string(request.subject_id)
        and _is_non_empty_string(request.action_name)
        and request.risk_level in {"low", "medium", "high"}
    )


def _is_well_formed_policy(policy: object) -> bool:
    if not isinstance(policy, HumanApprovalPolicy):
        return False
    return _is_string_frozenset(policy.high_risk_actions) and all(
        risk_level in {"low", "medium", "high"}
        for risk_level in policy.approval_required_risk_levels
    )


def _deny(
    *,
    request: AgentActionRequest | object | None,
    reason: HumanApprovalReason,
) -> HumanApprovalDecision:
    return HumanApprovalDecision(
        status="deny",
        request_id=request.request_id if isinstance(request, AgentActionRequest) else None,
        action_name=request.action_name if isinstance(request, AgentActionRequest) else None,
        reason=reason,
    )


def _allow(
    *,
    request: AgentActionRequest,
    reason: HumanApprovalReason,
) -> HumanApprovalDecision:
    return HumanApprovalDecision(
        status="allow",
        request_id=request.request_id,
        action_name=request.action_name,
        reason=reason,
    )


def requires_human_approval(
    *,
    request: AgentActionRequest,
    policy: HumanApprovalPolicy,
) -> bool:
    return (
        request.action_name in policy.high_risk_actions
        or request.risk_level in policy.approval_required_risk_levels
    )


def evaluate_human_approval(
    *,
    context: AgentActionContext | object | None,
    request: AgentActionRequest | object | None,
    policy: HumanApprovalPolicy | object,
    approvals: Mapping[str, HumanApprovalRecord] | object,
) -> HumanApprovalDecision:
    """Evaluate whether an agent action can proceed.

    This helper is intentionally isolated and not wired into live agent runtime.
    It proves a human-in-the-loop approval shape for high-risk actions.
    """

    if context is None:
        return _deny(request=request, reason=HumanApprovalReason.MISSING_CONTEXT)
    if not _is_well_formed_context(context):
        return _deny(request=request, reason=HumanApprovalReason.MALFORMED_CONTEXT)
    if not _is_well_formed_request(request):
        return _deny(request=request, reason=HumanApprovalReason.MALFORMED_CONTEXT)
    if not _is_well_formed_policy(policy):
        return _deny(request=request, reason=HumanApprovalReason.MALFORMED_CONTEXT)

    if request.tenant_id != context.tenant_id or request.subject_id != context.subject_id:
        return _deny(request=request, reason=HumanApprovalReason.MALFORMED_CONTEXT)

    if not requires_human_approval(request=request, policy=policy):
        return _allow(request=request, reason=HumanApprovalReason.ALLOWED_LOW_RISK)

    if not isinstance(approvals, Mapping):
        return _deny(
            request=request,
            reason=HumanApprovalReason.HIGH_RISK_ACTION_REQUIRES_APPROVAL,
        )

    approval = approvals.get(request.request_id)
    if approval is None:
        return _deny(request=request, reason=HumanApprovalReason.APPROVAL_NOT_FOUND)
    if approval.tenant_id != request.tenant_id:
        return _deny(request=request, reason=HumanApprovalReason.APPROVAL_TENANT_MISMATCH)
    if approval.subject_id != request.subject_id:
        return _deny(request=request, reason=HumanApprovalReason.APPROVAL_SUBJECT_MISMATCH)
    if approval.action_name != request.action_name:
        return _deny(request=request, reason=HumanApprovalReason.APPROVAL_ACTION_MISMATCH)
    if approval.status == "rejected":
        return _deny(request=request, reason=HumanApprovalReason.APPROVAL_REJECTED)
    if approval.status == "expired":
        return _deny(request=request, reason=HumanApprovalReason.APPROVAL_EXPIRED)
    if approval.status != "approved":
        return _deny(request=request, reason=HumanApprovalReason.MALFORMED_CONTEXT)

    return _allow(request=request, reason=HumanApprovalReason.APPROVED)
