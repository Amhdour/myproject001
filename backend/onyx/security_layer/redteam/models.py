from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel
from pydantic import Field


class RedteamToolName(str, Enum):
    PYRIT = "pyrit"
    GARAK = "garak"


class RedteamFindingCategory(str, Enum):
    PROMPT_INJECTION = "prompt_injection"
    CROSS_TENANT_LEAKAGE = "cross_tenant_leakage"
    TOOL_ABUSE = "tool_abuse"
    MCP_SCOPE_BYPASS = "mcp_scope_bypass"
    SECRET_EXTERNAL_ROUTING = "secret_external_routing"
    RAW_EVIDENCE_LEAKAGE = "raw_evidence_leakage"


class RedteamSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RedteamControlMapping(BaseModel):
    category: RedteamFindingCategory
    control_name: str
    control_summary: str
    evidence_boundary: str
    implementation_reference: str


class RedteamFinding(BaseModel):
    finding_id: str
    category: RedteamFindingCategory
    severity: RedteamSeverity
    title: str
    sanitized_evidence: str
    control_mapping: RedteamControlMapping | None = None
    source_tool: RedteamToolName
    source_fixture: str
    raw_evidence_exported: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class RedteamAdapterStatus(BaseModel):
    tool_name: RedteamToolName
    dependency_available: bool
    fixture_mode: bool
    limitation: str


class RedteamEvidenceBundle(BaseModel):
    generated_by: str
    claim_boundary: str
    adapter_status: RedteamAdapterStatus
    findings: list[RedteamFinding]


class RedteamSummary(BaseModel):
    claim_boundary: str
    pyrit_status: RedteamAdapterStatus
    garak_status: RedteamAdapterStatus
    findings: list[RedteamFinding]
    finding_counts_by_category: dict[str, int]
    raw_evidence_exported: bool
