from __future__ import annotations

from datetime import datetime
from datetime import timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel
from pydantic import Field


class MCPGovernanceDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVAL_REQUIRED = "approval_required"
    MONITOR = "monitor"
    SHADOW_DENY = "shadow_deny"


class MCPToolRiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MCPGovernanceConfig(BaseModel):
    """Local policy switches for the initial MCP governance layer."""

    unknown_server_monitor_mode: bool = False
    shadow_mode: bool = False


class MCPGovernanceRequest(BaseModel):
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    tenant_id: str
    mcp_server_id: str
    mcp_tool_name: str | None = None
    mcp_resource_id: str | None = None
    resource_tenant_id: str | None = None
    requested_scopes: frozenset[str] = Field(default_factory=frozenset)
    required_scopes: frozenset[str] = Field(default_factory=frozenset)
    raw_mcp_payload: dict[str, Any] = Field(default_factory=dict, exclude=True)


class MCPServerPolicy(BaseModel):
    mcp_server_id: str
    high_risk_tools: frozenset[str] = Field(default_factory=frozenset)
    default_required_scopes: frozenset[str] = Field(default_factory=frozenset)


class MCPGovernanceReceipt(BaseModel):
    receipt_id: str = Field(default_factory=lambda: str(uuid4()))
    previous_receipt_hash: str | None = None
    receipt_hash: str
    user_id: str
    tenant_id: str
    mcp_server_id: str
    mcp_tool_name: str | None = None
    mcp_resource_id: str | None = None
    decision: MCPGovernanceDecision
    reason: str
    correlation_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class MCPGovernanceEvidence(BaseModel):
    receipt_id: str
    user_id: str
    tenant_id: str
    mcp_server_id: str
    mcp_tool_name: str | None = None
    mcp_resource_id: str | None = None
    decision: MCPGovernanceDecision
    reason: str
    receipt_hash: str
    correlation_id: str


class MCPGovernanceResult(BaseModel):
    correlation_id: str
    user_id: str
    tenant_id: str
    mcp_server_id: str
    mcp_tool_name: str | None = None
    mcp_resource_id: str | None = None
    resource_tenant_id: str | None = None
    requested_scopes: frozenset[str]
    required_scopes: frozenset[str]
    decision: MCPGovernanceDecision
    reason: str
    approval_required: bool = False
    receipt: MCPGovernanceReceipt
    evidence: MCPGovernanceEvidence
