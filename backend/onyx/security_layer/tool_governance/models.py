from __future__ import annotations

from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field


class ToolGovernanceDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVAL_REQUIRED = "approval_required"
    MONITOR = "monitor"
    SHADOW_DENY = "shadow_deny"


class ToolRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolGovernanceConfig(BaseModel):
    """Local policy switches for the first tool governance foundation."""

    critical_side_effect_requires_approval: bool = False
    shadow_mode: bool = False
    approval_ttl_seconds: int = 900


class ToolActionRequest(BaseModel):
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    tenant_id: str
    tool_name: str
    action: str = "execute"
    is_side_effecting: bool | None = None
    raw_tool_payload: dict[str, Any] = Field(default_factory=dict, exclude=True)
    approval_id: str | None = None


class ApprovalRequest(BaseModel):
    approval_id: str = Field(default_factory=lambda: str(uuid4()))
    correlation_id: str
    tenant_id: str
    user_id: str
    tool_name: str
    action: str
    action_hash: str
    requested_by_user_id: str
    approved_by_user_id: str | None = None
    expires_at: datetime
    used_at: datetime | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ToolGovernanceReceipt(BaseModel):
    receipt_id: str = Field(default_factory=lambda: str(uuid4()))
    previous_receipt_hash: str | None = None
    receipt_hash: str
    correlation_id: str
    user_id: str
    tenant_id: str
    tool_name: str
    action: str
    decision: ToolGovernanceDecision
    reason: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ToolGovernanceEvidence(BaseModel):
    tool_name: str
    action: str
    risk_level: ToolRiskLevel
    decision: ToolGovernanceDecision
    approval_required: bool
    receipt_hash: str
    correlation_id: str


class ToolGovernanceResult(BaseModel):
    correlation_id: str
    user_id: str
    tenant_id: str
    tool_name: str
    action: str
    risk_level: ToolRiskLevel
    decision: ToolGovernanceDecision
    reason: str
    approval_required: bool = False
    approval_id: str | None = None
    action_hash: str
    receipt: ToolGovernanceReceipt
    evidence: ToolGovernanceEvidence
