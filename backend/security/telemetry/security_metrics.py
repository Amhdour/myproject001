from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from backend.security.policy.policy_decision import PolicyDecision
from backend.security.policy.policy_decision import SecurityDecisionValue


@dataclass
class InMemorySecurityMetrics:
    counters: dict[str, int] = field(
        default_factory=lambda: {
            "security_decision_total": 0,
            "security_denied_total": 0,
            "security_approval_required_total": 0,
            "security_monitor_only_total": 0,
            "enforcement_fail_closed_total": 0,
            "demo_attack_blocked_total": 0,
        }
    )
    latencies_ms: list[float] = field(default_factory=list)
    samples: list[dict[str, str | int | float]] = field(default_factory=list)

    def record_decision(
        self,
        decision: PolicyDecision,
        *,
        latency_ms: float,
        fail_closed: bool = False,
        demo_attack: bool = False,
    ) -> None:
        self.counters["security_decision_total"] += 1
        if decision.decision == SecurityDecisionValue.DENY:
            self.counters["security_denied_total"] += 1
        if decision.decision == SecurityDecisionValue.APPROVAL_REQUIRED:
            self.counters["security_approval_required_total"] += 1
        if decision.decision == SecurityDecisionValue.MONITOR_ONLY:
            self.counters["security_monitor_only_total"] += 1
        if fail_closed:
            self.counters["enforcement_fail_closed_total"] += 1
        if demo_attack and decision.blocks_runtime:
            self.counters["demo_attack_blocked_total"] += 1
        self.latencies_ms.append(latency_ms)
        self.samples.append(
            {
                "metric_name": "policy_evaluation_latency_ms",
                "value": round(latency_ms, 4),
                "decision": decision.decision.value,
                "action": decision.action,
                "correlation_id": decision.correlation_id,
            }
        )

    def snapshot(self) -> dict[str, Any]:
        average = sum(self.latencies_ms) / len(self.latencies_ms) if self.latencies_ms else 0
        return {
            **self.counters,
            "policy_evaluation_latency_ms": {
                "count": len(self.latencies_ms),
                "avg": round(average, 4),
                "samples": self.samples,
            },
        }
