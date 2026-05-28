"""Models for isolated enforce-mode readiness simulations.

The schema intentionally stores safe identifiers and sanitized summaries only.
It must not store raw query, prompt, document, chunk, or secret values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

SCHEMA_VERSION = "enforce-mode-readiness.v1"


class EnforceControlFamily(StrEnum):
    RETRIEVAL_ACL = "retrieval_acl"
    VECTOR_DB_SECURITY = "vector_db_security"
    CACHE_SECURITY = "cache_security"
    TOOL_AUTHORIZATION = "tool_authorization"
    MCP_HARDENING = "mcp_hardening"
    ARTIFACT_SAFETY = "artifact_safety"
    SECURE_INGESTION = "secure_ingestion"
    SAFE_DENIAL = "safe_denial_shared_runtime"
    AUDIT_FINDING_METRIC = "audit_finding_metric_shared_sink"


class EnforceReadinessStage(StrEnum):
    PLANNED = "planned"
    SIMULATED = "simulated"
    BLOCKED = "blocked"
    APPROVED_LIMITED_PILOT = "approved_limited_pilot"


class EnforceGateStatus(StrEnum):
    PASSED = "passed"
    BLOCKED = "blocked"
    NOT_EVALUATED = "not_evaluated"


class EnforceActivationDecisionStatus(StrEnum):
    APPROVED_SIMULATION_ONLY = "approved_simulation_only"
    BLOCKED = "blocked"


class EnforceSimulatedEffect(StrEnum):
    NO_CHANGE = "no_change"
    WOULD_BLOCK = "would_block"
    WOULD_DENY = "would_deny"


class EnforceLiveEffect(StrEnum):
    NO_CHANGE = "no_change"


class EnforceFeatureFlagState(StrEnum):
    ENABLED = "enabled"
    DISABLED = "disabled"


class EnforceRollbackState(StrEnum):
    AVAILABLE = "available"
    ENABLED = "enabled"
    DISABLED = "disabled"
    MISSING = "missing"


class EnforceKillSwitchState(StrEnum):
    AVAILABLE = "available"
    ENABLED = "enabled"
    DISABLED = "disabled"
    MISSING = "missing"


class EnforceBlastRadiusStatus(StrEnum):
    NONE_ALLOWED = "none_allowed"
    LIMITED = "limited"
    TOO_BROAD = "too_broad"
    THRESHOLD_BREACHED = "threshold_breached"


class EnforceApprovalStatus(StrEnum):
    NOT_APPROVED = "not_approved"
    GLOBALLY_APPROVED = "globally_approved"
    FAMILY_APPROVED = "family_approved"
    FULLY_APPROVED = "fully_approved"


@dataclass(frozen=True)
class EnforceReadinessContext:
    control_family: EnforceControlFamily
    stage: EnforceReadinessStage = EnforceReadinessStage.PLANNED
    tenant_safe_id: str = "tenant-placeholder"
    workspace_safe_id: str = "workspace-placeholder"
    subject_safe_id: str = "subject-placeholder"
    feature_flags: dict[str, EnforceFeatureFlagState] = field(default_factory=dict)
    approval_status: EnforceApprovalStatus = EnforceApprovalStatus.NOT_APPROVED
    rollback_state: EnforceRollbackState = EnforceRollbackState.DISABLED
    kill_switch_state: EnforceKillSwitchState = EnforceKillSwitchState.DISABLED
    blast_radius_status: EnforceBlastRadiusStatus = (
        EnforceBlastRadiusStatus.NONE_ALLOWED
    )
    monitor_only_evidence_present: bool = False
    shadow_deny_evidence_present: bool = False
    ci_evidence_present: bool = False
    staging_dry_run_evidence_present: bool = False
    false_positive_review_complete: bool = False
    incident_response_plan_present: bool = False
    non_leakage_validation_passed: bool = False
    safe_denial_validation_passed: bool = False
    audit_event_evidence_present: bool = False
    finding_evidence_present: bool = False
    metric_evidence_present: bool = False
    rollback_evidence_present: bool = False
    kill_switch_evidence_present: bool = False
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class EnforceGateResult:
    gate_id: str
    status: EnforceGateStatus
    reason: str
    required_evidence: tuple[str, ...]
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class EnforceFinding:
    finding_id: str
    control_family: EnforceControlFamily
    severity: str
    sanitized_summary: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class EnforceSimulationRecord:
    record_id: str
    control_family: EnforceControlFamily
    simulated_effect: EnforceSimulatedEffect
    live_effect: EnforceLiveEffect
    sanitized_summary: str
    schema_version: str = SCHEMA_VERSION


@dataclass(frozen=True)
class EnforceActivationDecision:
    status: EnforceActivationDecisionStatus
    control_family: EnforceControlFamily
    simulated_effect: EnforceSimulatedEffect
    live_effect: EnforceLiveEffect
    approval_status: EnforceApprovalStatus
    rollback_state: EnforceRollbackState
    kill_switch_state: EnforceKillSwitchState
    blast_radius_status: EnforceBlastRadiusStatus
    non_leakage_validation_passed: bool
    safe_denial_validation_passed: bool
    gate_results: tuple[EnforceGateResult, ...]
    findings: tuple[EnforceFinding, ...] = ()
    simulation_records: tuple[EnforceSimulationRecord, ...] = ()
    reason: str = "simulation only"
    schema_version: str = SCHEMA_VERSION
