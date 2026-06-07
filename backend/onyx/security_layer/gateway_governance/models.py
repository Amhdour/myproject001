from __future__ import annotations

from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field


class GatewayGovernanceDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    MASK = "mask"
    ROUTE_PRIVATE = "route_private"
    ROUTE_EXTERNAL = "route_external"
    APPROVAL_REQUIRED = "approval_required"
    MONITOR = "monitor"
    SHADOW_DENY = "shadow_deny"


class GatewayDataClassification(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    RESTRICTED = "restricted"


class GatewayRouteTarget(str, Enum):
    EXTERNAL = "external"
    PRIVATE = "private"
    BLOCKED = "blocked"
    PENDING_APPROVAL = "pending_approval"
    MONITOR = "monitor"


class GatewayPolicyMode(str, Enum):
    DENY = "deny"
    ROUTE_PRIVATE = "route_private"
    MONITOR = "monitor"
    MASK = "mask"


class GatewayGovernanceConfig(BaseModel):
    enabled: bool = False
    restricted_external_mode: GatewayPolicyMode = GatewayPolicyMode.DENY
    pii_external_mode: GatewayPolicyMode = GatewayPolicyMode.MASK
    high_risk_mode: GatewayGovernanceDecision = GatewayGovernanceDecision.APPROVAL_REQUIRED


class GatewayGovernanceRequest(BaseModel):
    user_id: str
    tenant_id: str
    model_provider: str
    requested_model: str
    data_classification: GatewayDataClassification = GatewayDataClassification.LOW
    contains_pii: bool = False
    contains_secret: bool = False
    contains_restricted_tenant_data: bool = False
    external_provider: bool = False
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    raw_prompt: str | None = Field(default=None, exclude=True)
    raw_context: str | None = Field(default=None, exclude=True)
    raw_payload: dict[str, Any] = Field(default_factory=dict, exclude=True)


class GatewayGovernanceEvidence(BaseModel):
    model_provider: str
    requested_model: str
    data_classification: GatewayDataClassification
    decision: GatewayGovernanceDecision
    route_target: GatewayRouteTarget
    contains_pii: bool
    contains_secret: bool
    restricted_data: bool
    correlation_id: str


class GatewayGovernanceResult(BaseModel):
    request: GatewayGovernanceRequest
    decision: GatewayGovernanceDecision
    route_target: GatewayRouteTarget
    reason: str
    evidence: GatewayGovernanceEvidence
