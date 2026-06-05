from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class SecurityDecisionValue(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVAL_REQUIRED = "approval_required"
    MONITOR_ONLY = "monitor_only"


class SecurityRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PolicyDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: str(uuid4()))
    decision: SecurityDecisionValue
    reason: str
    policy_version: str
    risk_level: SecurityRiskLevel
    correlation_id: str
    enforcement_point: str
    action: str
    resource_type: str
    resource_id: str
    user_id: str | None
    tenant_id: str | None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @property
    def blocks_runtime(self) -> bool:
        return self.decision in {
            SecurityDecisionValue.DENY,
            SecurityDecisionValue.APPROVAL_REQUIRED,
        }
