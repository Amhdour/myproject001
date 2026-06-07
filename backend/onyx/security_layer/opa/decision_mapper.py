from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

OPA_RETRIEVAL_ACL_EVENT_TYPE = "security.opa.retrieval_acl.decision"
OPA_RETRIEVAL_ACL_PACKAGE = "onyx.security.retrieval_acl"
OPA_RETRIEVAL_ACL_POLICY_VERSION = "v1"


class OPADecisionValue(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    MONITOR = "monitor"
    SHADOW_DENY = "shadow_deny"


@dataclass(frozen=True)
class OPADecision:
    decision: OPADecisionValue
    reason: str
    correlation_id: str
    policy_package: str = OPA_RETRIEVAL_ACL_PACKAGE
    policy_version: str = OPA_RETRIEVAL_ACL_POLICY_VERSION
    fallback_used: bool = False
    subject_user_id: str | None = None
    subject_tenant_id: str | None = None
    resource_document_id: str | None = None
    resource_tenant_id: str | None = None
    raw_result: dict[str, Any] = field(default_factory=dict)

    @property
    def audit_details(self) -> dict[str, str | bool | None]:
        return {
            "event_type": OPA_RETRIEVAL_ACL_EVENT_TYPE,
            "decision": self.decision.value,
            "reason": self.reason,
            "policy_package": self.policy_package,
            "policy_version": self.policy_version,
            "subject_user_id": self.subject_user_id,
            "subject_tenant_id": self.subject_tenant_id,
            "resource_document_id": self.resource_document_id,
            "resource_tenant_id": self.resource_tenant_id,
            "correlation_id": self.correlation_id,
            "fallback_used": self.fallback_used,
        }


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    return str(value)


def map_opa_result(result: dict[str, Any], opa_input: dict[str, Any]) -> OPADecision:
    raw_decision = result.get("decision", OPADecisionValue.DENY.value)
    try:
        decision = OPADecisionValue(str(raw_decision))
    except ValueError:
        decision = OPADecisionValue.DENY

    subject = opa_input.get("subject", {})
    resource = opa_input.get("resource", {})
    return OPADecision(
        decision=decision,
        reason=str(result.get("reason", "OPA policy returned no reason")),
        policy_package=str(result.get("policy_package", OPA_RETRIEVAL_ACL_PACKAGE)),
        policy_version=str(result.get("policy_version", OPA_RETRIEVAL_ACL_POLICY_VERSION)),
        fallback_used=bool(result.get("fallback_used", False)),
        correlation_id=str(opa_input.get("correlation_id", "missing:correlation")),
        subject_user_id=_optional_string(subject.get("user_id")) if isinstance(subject, dict) else None,
        subject_tenant_id=_optional_string(subject.get("tenant_id")) if isinstance(subject, dict) else None,
        resource_document_id=_optional_string(resource.get("document_id")) if isinstance(resource, dict) else None,
        resource_tenant_id=_optional_string(resource.get("tenant_id")) if isinstance(resource, dict) else None,
        raw_result=result,
    )
