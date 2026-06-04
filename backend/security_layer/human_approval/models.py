from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class HumanApprovalReason(str, Enum):
    ALLOWED_LOW_RISK = "allowed_low_risk"
    APPROVED = "approved"
    MISSING_CONTEXT = "missing_context"
    MALFORMED_CONTEXT = "malformed_context"
    HIGH_RISK_ACTION_REQUIRES_APPROVAL = "high_risk_action_requires_approval"
    APPROVAL_NOT_FOUND = "approval_not_found"
    APPROVAL_REJECTED = "approval_rejected"
    APPROVAL_EXPIRED = "approval_expired"
    APPROVAL_SUBJECT_MISMATCH = "approval_subject_mismatch"
    APPROVAL_TENANT_MISMATCH = "approval_tenant_mismatch"
    APPROVAL_ACTION_MISMATCH = "approval_action_mismatch"


HumanApprovalDecisionStatus = Literal["allow", "deny"]
HumanApprovalRiskLevel = Literal["low", "medium", "high"]
HumanApprovalRecordStatus = Literal["approved", "rejected", "expired"]


@dataclass(frozen=True)
class AgentActionContext:
    """Requester context for isolated human approval workflow proof."""

    tenant_id: str
    subject_id: str
    role_ids: frozenset[str]


@dataclass(frozen=True)
class AgentActionRequest:
    """Minimal high-risk agent action request used by the isolated helper."""

    request_id: str
    tenant_id: str
    subject_id: str
    action_name: str
    risk_level: HumanApprovalRiskLevel


@dataclass(frozen=True)
class HumanApprovalPolicy:
    """Policy deciding which action/risk combinations need human approval."""

    high_risk_actions: frozenset[str]
    approval_required_risk_levels: frozenset[HumanApprovalRiskLevel]


@dataclass(frozen=True)
class HumanApprovalRecord:
    """Human approval decision captured before agent action execution."""

    approval_id: str
    request_id: str
    tenant_id: str
    subject_id: str
    action_name: str
    status: HumanApprovalRecordStatus


@dataclass(frozen=True)
class HumanApprovalDecision:
    status: HumanApprovalDecisionStatus
    request_id: str | None
    action_name: str | None
    reason: HumanApprovalReason

    @property
    def denied(self) -> bool:
        return self.status == "deny"
