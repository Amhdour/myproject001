from __future__ import annotations

import pytest

from backend.security.audit.security_audit_logger import InMemorySecurityAuditLogger
from backend.security.enforcement.security_enforcer import SecurityEnforcer
from backend.security.telemetry.security_metrics import InMemorySecurityMetrics
from backend.tests.security import factories


@pytest.fixture
def audit_logger() -> InMemorySecurityAuditLogger:
    return InMemorySecurityAuditLogger()


@pytest.fixture
def metrics() -> InMemorySecurityMetrics:
    return InMemorySecurityMetrics()


@pytest.fixture
def enforcer(
    audit_logger: InMemorySecurityAuditLogger, metrics: InMemorySecurityMetrics
) -> SecurityEnforcer:
    return SecurityEnforcer(audit_logger=audit_logger, metrics=metrics)


@pytest.fixture
def valid_same_tenant_context() -> dict[str, object]:
    return factories.valid_same_tenant_context()


@pytest.fixture
def missing_user_context() -> dict[str, object]:
    return factories.missing_user_context()


@pytest.fixture
def missing_tenant_context() -> dict[str, object]:
    return factories.missing_tenant_context()


@pytest.fixture
def cross_tenant_context() -> dict[str, object]:
    return factories.cross_tenant_context()


@pytest.fixture
def high_risk_tool_context() -> dict[str, object]:
    return factories.high_risk_tool_context()
