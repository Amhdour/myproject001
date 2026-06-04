from __future__ import annotations

from collections.abc import Mapping

from backend.security_layer.tool_authorization.models import ToolAuthorizationDecision
from backend.security_layer.tool_authorization.models import ToolAuthorizationPolicy
from backend.security_layer.tool_authorization.models import ToolAuthorizationReason
from backend.security_layer.tool_authorization.models import ToolCallRequest
from backend.security_layer.tool_authorization.models import ToolRequesterContext


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_string_frozenset(value: object) -> bool:
    return isinstance(value, frozenset) and all(_is_non_empty_string(item) for item in value)


def _is_well_formed_context(context: object) -> bool:
    if not isinstance(context, ToolRequesterContext):
        return False
    return (
        _is_non_empty_string(context.tenant_id)
        and _is_non_empty_string(context.subject_id)
        and _is_string_frozenset(context.role_ids)
        and _is_string_frozenset(context.approved_request_ids)
    )


def _is_well_formed_request(request: object) -> bool:
    if not isinstance(request, ToolCallRequest):
        return False
    return (
        _is_non_empty_string(request.request_id)
        and _is_non_empty_string(request.tenant_id)
        and _is_non_empty_string(request.tool_name)
        and _is_non_empty_string(request.action)
    )


def _is_well_formed_policy(policy: object) -> bool:
    if not isinstance(policy, ToolAuthorizationPolicy):
        return False
    return (
        _is_non_empty_string(policy.tool_name)
        and _is_non_empty_string(policy.tenant_id)
        and _is_string_frozenset(policy.allowed_subject_ids)
        and _is_string_frozenset(policy.allowed_role_ids)
        and _is_string_frozenset(policy.allowed_actions)
    )


def deny_tool_call(
    *,
    request: ToolCallRequest | object | None,
    reason: ToolAuthorizationReason,
) -> ToolAuthorizationDecision:
    return ToolAuthorizationDecision(
        status="deny",
        request_id=request.request_id if isinstance(request, ToolCallRequest) else None,
        tool_name=request.tool_name if isinstance(request, ToolCallRequest) else None,
        action=request.action if isinstance(request, ToolCallRequest) else None,
        reason=reason,
    )


def authorize_tool_call(
    *,
    context: ToolRequesterContext | object | None,
    request: ToolCallRequest | object | None,
    policies: Mapping[str, ToolAuthorizationPolicy] | object,
) -> ToolAuthorizationDecision:
    """Authorize an isolated tool call, failing closed on malformed inputs.

    This helper is intentionally not wired into live agent/tool runtime paths. It
    proves a runtime authorization shape for tool calls before execution.
    """

    if context is None:
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.MISSING_CONTEXT)
    if not _is_well_formed_context(context):
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.MALFORMED_CONTEXT)
    if not _is_well_formed_request(request):
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.MALFORMED_CONTEXT)
    if not isinstance(policies, Mapping):
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.UNKNOWN_TOOL)

    policy = policies.get(request.tool_name)
    if policy is None:
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.UNKNOWN_TOOL)
    if not _is_well_formed_policy(policy):
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.UNKNOWN_TOOL)

    if request.tenant_id != context.tenant_id or policy.tenant_id != context.tenant_id:
        return deny_tool_call(
            request=request,
            reason=ToolAuthorizationReason.CROSS_TENANT_TOOL_CALL,
        )

    subject_is_allowed = context.subject_id in policy.allowed_subject_ids
    role_is_allowed = bool(context.role_ids & policy.allowed_role_ids)
    if not subject_is_allowed and not role_is_allowed:
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.UNAUTHORIZED_TOOL)

    if request.action not in policy.allowed_actions:
        return deny_tool_call(request=request, reason=ToolAuthorizationReason.DISALLOWED_ACTION)

    if policy.requires_approval and request.request_id not in context.approved_request_ids:
        return deny_tool_call(
            request=request,
            reason=ToolAuthorizationReason.MISSING_REQUIRED_APPROVAL,
        )

    return ToolAuthorizationDecision(
        status="allow",
        request_id=request.request_id,
        tool_name=request.tool_name,
        action=request.action,
        reason=ToolAuthorizationReason.ALLOWED,
    )
