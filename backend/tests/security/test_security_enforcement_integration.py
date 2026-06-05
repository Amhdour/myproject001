from __future__ import annotations

import pytest

from backend.security.enforcement.security_enforcer import SecurityEnforcementError
from backend.security.enforcement.security_enforcer import SecurityEnforcer
from backend.tests.security import factories


def test_service_level_retrieval_action_succeeds_for_same_tenant() -> None:
    result = SecurityEnforcer().enforce(
        factories.valid_same_tenant_context(),
        enforcement_point="service_level_retrieval_flow",
    )
    assert result.decision.reason == "policy_allow_same_tenant_known_action"
    assert result.audit_event.decision == "allow"


def test_service_level_retrieval_action_denies_cross_tenant_and_records_evidence() -> None:
    enforcer = SecurityEnforcer()
    with pytest.raises(SecurityEnforcementError):
        enforcer.enforce(
            factories.cross_tenant_context(),
            enforcement_point="service_level_retrieval_flow",
            details={"secret_token": "demo-secret"},
        )
    assert enforcer.audit_logger.events[-1].decision == "deny"
    assert enforcer.audit_logger.events[-1].redacted_details["secret_token"] == "[REDACTED]"
    assert enforcer.metrics.snapshot()["security_denied_total"] == 1


def test_service_level_retrieval_action_denies_missing_context() -> None:
    with pytest.raises(SecurityEnforcementError):
        SecurityEnforcer().enforce(
            factories.missing_user_context(),
            enforcement_point="service_level_retrieval_flow",
        )
