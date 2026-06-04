from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class ToolAuthorizationReason(str, Enum):
    ALLOWED = "allowed"
    MISSING_CONTEXT = "missing_context"
    MALFORMED_CONTEXT = "malformed_context"
    UNKNOWN_TOOL = "unknown_tool"
    UNAUTHORIZED_TOOL = "unauthorized_tool"
    CROSS_TENANT_TOOL_CALL = "cross_tenant_tool_call"
    MISSING_REQUIRED_APPROVAL = "missing_required_approval"
    DISALLOWED_ACTION = "disallowed_action"


ToolAuthorizationDecisionStatus = Literal["allow", "deny"]


@dataclass(frozen=True)
class ToolRequesterContext:
    """Requester context for isolated agent/tool authorization proof."""

    tenant_id: str
    subject_id: str
    role_ids: frozenset[str]
    approved_request_ids: frozenset[str] = frozenset()


@dataclass(frozen=True)
class ToolCallRequest:
    """Minimal tool call request used by the isolated authorization helper."""

    request_id: str
    tenant_id: str
    tool_name: str
    action: str


@dataclass(frozen=True)
class ToolAuthorizationPolicy:
    """Per-tool authorization policy for isolated runtime proof."""

    tool_name: str
    tenant_id: str
    allowed_subject_ids: frozenset[str]
    allowed_role_ids: frozenset[str]
    allowed_actions: frozenset[str]
    requires_approval: bool = False


@dataclass(frozen=True)
class ToolAuthorizationDecision:
    status: ToolAuthorizationDecisionStatus
    request_id: str | None
    tool_name: str | None
    action: str | None
    reason: ToolAuthorizationReason

    @property
    def denied(self) -> bool:
        return self.status == "deny"
