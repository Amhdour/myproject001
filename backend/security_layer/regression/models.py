"""Dataclass models for isolated regression and synthetic demo-attack evidence.

These models intentionally store only safe identifiers, mapped controls, expected
results, and sanitized evidence references. They do not store raw prompts, raw
documents, raw chunks, secrets, credentials, or tenant internals.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RegressionDemoFamily(str, Enum):
    UNAUTHORIZED_RETRIEVAL = "unauthorized_retrieval"
    CROSS_TENANT_RETRIEVAL = "cross_tenant_retrieval"
    STALE_DELETED_ACL_RETRIEVAL = "stale_deleted_acl_retrieval"
    VECTOR_METADATA_MISMATCH = "vector_metadata_mismatch"
    CACHE_TENANT_ACL_COLLISION = "cache_tenant_acl_collision"
    UNAUTHORIZED_TOOL_CALL = "unauthorized_tool_call"
    PROMPT_TO_TOOL_ABUSE = "prompt_to_tool_abuse"
    MCP_CONFUSED_DEPUTY = "mcp_confused_deputy"
    MCP_CREDENTIAL_MISUSE = "mcp_credential_misuse"
    ARTIFACT_SECRET_LEAKAGE = "artifact_secret_leakage"
    ARTIFACT_DOCUMENT_LEAKAGE = "artifact_document_leakage"
    SHADOW_DENY_SAFETY = "shadow_deny_safety"
    ENFORCE_MODE_GATE_BLOCK = "enforce_mode_gate_block"
    MONITOR_ONLY_NO_BLOCK = "monitor_only_no_block"
    SAFE_DENIAL_NON_LEAKAGE = "safe_denial_non_leakage"
    AUDIT_FINDING_METRIC = "audit_finding_metric"


class RegressionDemoScenarioStatus(str, Enum):
    PLANNED = "planned"
    IMPLEMENTED = "implemented"


class RegressionDemoExpectedResult(str, Enum):
    ALLOWED = "allowed"
    FLAGGED = "flagged"
    BLOCKED_ISOLATED_CONTROL = "blocked_isolated_control"
    APPROVAL_REQUIRED = "approval_required"
    SIMULATED_DENY_NO_BLOCK = "simulated_deny_no_block"
    ENFORCE_ACTIVATION_BLOCKED = "enforce_activation_blocked"
    LIVE_EFFECT_NO_CHANGE = "live_effect_no_change"
    EVIDENCE_EMITTED = "evidence_emitted"


class RegressionDemoOutcome(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    FLAGGED = "flagged"
    BLOCKED_ISOLATED = "blocked_isolated"
    SIMULATED = "simulated"
    APPROVAL_REQUIRED = "approval_required"
    NO_CHANGE = "no_change"


class RegressionDemoSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RegressionDemoFixtureType(str, Enum):
    SYNTHETIC_RETRIEVAL = "synthetic_retrieval"
    SYNTHETIC_VECTOR = "synthetic_vector"
    SYNTHETIC_CACHE = "synthetic_cache"
    SYNTHETIC_TOOL = "synthetic_tool"
    SYNTHETIC_MCP = "synthetic_mcp"
    SYNTHETIC_ARTIFACT = "synthetic_artifact"
    SYNTHETIC_MONITOR_ONLY = "synthetic_monitor_only"
    SYNTHETIC_SHADOW_DENY = "synthetic_shadow_deny"
    SYNTHETIC_ENFORCE_MODE = "synthetic_enforce_mode"
    SYNTHETIC_SAFE_DENIAL = "synthetic_safe_denial"


@dataclass(frozen=True)
class RegressionDemoScenario:
    scenario_id: str
    title: str
    family: RegressionDemoFamily
    status: RegressionDemoScenarioStatus
    expected_result: RegressionDemoExpectedResult
    severity: RegressionDemoSeverity
    fixture_type: RegressionDemoFixtureType
    mapped_controls: tuple[str, ...]
    mapped_risks: tuple[str, ...]
    evidence_ref: str
    tenant_safe_id: str = "tenant_alpha"
    workspace_safe_id: str = "workspace_demo"
    subject_safe_id: str = "subject_demo"
    non_leakage_required: bool = True
    behavior_preserving_required: bool = True


@dataclass(frozen=True)
class RegressionDemoResult:
    scenario_id: str
    outcome: RegressionDemoOutcome
    expected_result: RegressionDemoExpectedResult
    mapped_controls: tuple[str, ...]
    mapped_risks: tuple[str, ...]
    evidence_ref: str
    sanitized_summary: str
    non_leakage_validated: bool
    behavior_preserved: bool
    live_blocking_enabled: bool = False
    live_filtering_enabled: bool = False
    enforce_mode_enabled: bool = False
    shadow_deny_runtime_enabled: bool = False
    tenant_safe_id: str = "tenant_alpha"
    workspace_safe_id: str = "workspace_demo"
    subject_safe_id: str = "subject_demo"


@dataclass(frozen=True)
class RegressionDemoRunSummary:
    total: int
    passed: int
    failed: int
    flagged: int
    blocked_isolated: int
    simulated: int
    approval_required: int
    no_change: int
    non_leakage_validated: bool
    behavior_preserved: bool
    live_blocking_enabled: bool
    live_filtering_enabled: bool
    enforce_mode_enabled: bool
    shadow_deny_runtime_enabled: bool
    evidence_refs: tuple[str, ...]
    sanitized_summary: str
