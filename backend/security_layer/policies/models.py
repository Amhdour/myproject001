from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PolicyEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    APPROVAL_REQUIRED = "approval_required"


class PolicyScope(str, Enum):
    RETRIEVAL = "retrieval"
    TOOLS = "tools"
    GLOBAL = "global"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EnforcementMode(str, Enum):
    DISABLED = "disabled"
    SHADOW = "shadow"
    ACTIVE = "active"


@dataclass(frozen=True)
class PolicyRule:
    rule_id: str
    effect: PolicyEffect
    actions: list[str] = field(default_factory=list)
    required_context: list[str] = field(default_factory=list)
    reason: str = ""
    risk_level: RiskLevel = RiskLevel.LOW


@dataclass(frozen=True)
class Policy:
    policy_id: str
    version: str
    scope: PolicyScope
    default_effect: PolicyEffect = PolicyEffect.DENY
    enforcement_mode: EnforcementMode = EnforcementMode.DISABLED
    rules: list[PolicyRule] = field(default_factory=list)


@dataclass(frozen=True)
class PolicyDecisionContext:
    action: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PolicyDecision:
    policy_id: str
    policy_version: str
    effect: PolicyEffect
    reason: str
    matched_rule_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PolicyException:
    exception_id: str
    policy_id: str
    justification: str
