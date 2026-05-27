from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SecurityMetric:
    action: str
    decision: str
    mode: str


_METRICS: list[SecurityMetric] = []


def emit_security_metric(action: str, decision: str, mode: str) -> None:
    _METRICS.append(SecurityMetric(action=action, decision=decision, mode=mode))


def get_security_metrics() -> list[SecurityMetric]:
    return list(_METRICS)


def clear_security_metrics() -> None:
    _METRICS.clear()
