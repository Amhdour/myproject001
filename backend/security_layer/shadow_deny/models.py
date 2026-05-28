from dataclasses import dataclass, field
from enum import Enum


class ShadowDenyControlFamily(str, Enum):
    RETRIEVAL = "retrieval"
    VECTOR = "vector"
    CACHE = "cache"
    TOOL = "tool"
    MCP = "mcp"
    ARTIFACT = "artifact"
    INGESTION = "ingestion"
    SAFE_DENIAL = "safe_denial"
    AUDIT_METRIC = "audit_metric"


class ShadowDenyStage(str, Enum):
    PRECHECK = "precheck"
    DECISION = "decision"
    POSTCHECK = "postcheck"


class ShadowDenyDecisionStatus(str, Enum):
    NOOP = "noop"
    SIMULATED_DENY = "simulated_deny"
    SIMULATED_FLAG = "simulated_flag"
    SIMULATED_APPROVAL_REQUIRED = "simulated_approval_required"


class ShadowDenySimulatedEffect(str, Enum):
    NO_CHANGE = "no_change"
    DENY = "deny"
    FLAG = "flag"
    APPROVAL_REQUIRED = "approval_required"


class ShadowDenyLiveEffect(str, Enum):
    ALLOWED = "allowed"
    NO_CHANGE = "no_change"


class ShadowDenyFeatureFlagState(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"


class ShadowDenyRollbackState(str, Enum):
    DISABLED = "disabled"
    ENABLED = "enabled"


class ShadowDenyMode(str, Enum):
    MONITOR_ONLY = "monitor_only"
    SHADOW_SIMULATION_ONLY = "shadow_simulation_only"


@dataclass(frozen=True)
class ShadowDenyDecisionRecord:
    schema_version: str
    decision_id: str
    timestamp: str
    control_family: str
    stage: str
    tenant_id_hash_or_safe_id: str
    workspace_id_hash_or_safe_id: str
    subject_id_hash_or_safe_id: str
    decision_status: str
    simulated_effect: str
    live_effect: str
    monitor_only_decision_id: str
    deny_reason_code: str
    safe_denial_category: str
    finding_ids: list[str]
    metric_names: list[str]
    audit_event_id: str
    evidence_ref: str
    rollback_flag_state: str
    feature_flag_state: str
    non_leakage_validated: bool
    created_at: str


@dataclass(frozen=True)
class ShadowDenyComparisonResult:
    monitor_only_decision_id: str
    shadow_decision_id: str
    decision_status_match: bool
    simulated_effect_match: bool


@dataclass
class ShadowDenySimulationContext:
    decision_id: str
    timestamp: str
    control_family: ShadowDenyControlFamily
    stage: ShadowDenyStage
    tenant_id_hash_or_safe_id: str
    workspace_id_hash_or_safe_id: str
    subject_id_hash_or_safe_id: str
    deny_reason_code: str
    safe_denial_category: str
    flags: dict[str, bool]
    monitor_only_decision_id: str = ""
    feature_flag_state: ShadowDenyFeatureFlagState = ShadowDenyFeatureFlagState.DISABLED
    rollback_flag_state: ShadowDenyRollbackState = ShadowDenyRollbackState.DISABLED
    mode: ShadowDenyMode = ShadowDenyMode.SHADOW_SIMULATION_ONLY
    schema_version: str = "v1"


@dataclass
class ShadowDenySimulationDecision:
    decision_record: ShadowDenyDecisionRecord
    comparison: ShadowDenyComparisonResult | None = None
    recorded: bool = False
    audit_events: list[str] = field(default_factory=list)
    finding_ids: list[str] = field(default_factory=list)
    metric_names: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ShadowDenyFinding:
    finding_id: str
    category: str
    detail: str
