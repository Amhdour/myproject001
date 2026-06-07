from __future__ import annotations

from typing import Any

from onyx.security_layer.opa.decision_mapper import OPA_RETRIEVAL_ACL_PACKAGE
from onyx.security_layer.opa.decision_mapper import OPA_RETRIEVAL_ACL_POLICY_VERSION
from onyx.security_layer.opa.decision_mapper import OPADecision
from onyx.security_layer.opa.decision_mapper import OPADecisionValue


def deny_high_risk_retrieval_fallback(opa_input: dict[str, Any], reason: str) -> OPADecision:
    """Deny context inclusion when OPA is unavailable for a high-risk retrieval decision."""

    subject = opa_input.get("subject", {})
    resource = opa_input.get("resource", {})
    return OPADecision(
        decision=OPADecisionValue.DENY,
        reason=f"OPA unavailable; denied high-risk retrieval decision: {reason}",
        policy_package=OPA_RETRIEVAL_ACL_PACKAGE,
        policy_version=OPA_RETRIEVAL_ACL_POLICY_VERSION,
        fallback_used=True,
        correlation_id=str(opa_input.get("correlation_id", "missing:correlation")),
        subject_user_id=subject.get("user_id") if isinstance(subject, dict) else None,
        subject_tenant_id=subject.get("tenant_id") if isinstance(subject, dict) else None,
        resource_document_id=resource.get("document_id") if isinstance(resource, dict) else None,
        resource_tenant_id=resource.get("tenant_id") if isinstance(resource, dict) else None,
    )
