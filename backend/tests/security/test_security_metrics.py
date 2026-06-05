from __future__ import annotations

from backend.security.policy.security_policy import SecurityPolicy
from backend.security.telemetry.security_metrics import InMemorySecurityMetrics
from backend.tests.security import factories


def test_security_metric_creation() -> None:
    decision, latency_ms = SecurityPolicy().evaluate(factories.high_risk_tool_context())
    metrics = InMemorySecurityMetrics()
    metrics.record_decision(decision, latency_ms=latency_ms, demo_attack=True)
    snapshot = metrics.snapshot()
    assert snapshot["security_decision_total"] == 1
    assert snapshot["security_approval_required_total"] == 1
    assert snapshot["demo_attack_blocked_total"] == 1
    assert snapshot["policy_evaluation_latency_ms"]["count"] == 1
