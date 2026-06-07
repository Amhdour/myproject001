from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone

from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionDecision,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionMode,
)


@dataclass(frozen=True)
class RetrievedContentPromptInjectionTelemetryMetric:
    metric_name: str
    mode: str
    decision: str
    checked_count: int
    detected_count: int
    quarantined_count: int
    timestamp: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_PROMPT_INJECTION_TELEMETRY_METRICS: list[RetrievedContentPromptInjectionTelemetryMetric] = []


def record_retrieved_content_prompt_injection_metric(
    *,
    mode: RetrievedContentPromptInjectionMode,
    decision: RetrievedContentPromptInjectionDecision,
    checked_count: int,
    detected_count: int,
    quarantined_count: int,
) -> RetrievedContentPromptInjectionTelemetryMetric:
    metric = RetrievedContentPromptInjectionTelemetryMetric(
        metric_name="retrieved_content_prompt_injection_decision_total",
        mode=mode.value,
        decision=decision.value,
        checked_count=checked_count,
        detected_count=detected_count,
        quarantined_count=quarantined_count,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    _PROMPT_INJECTION_TELEMETRY_METRICS.append(metric)
    return metric


def get_retrieved_content_prompt_injection_telemetry_metrics() -> list[RetrievedContentPromptInjectionTelemetryMetric]:
    return list(_PROMPT_INJECTION_TELEMETRY_METRICS)


def clear_retrieved_content_prompt_injection_telemetry_metrics() -> None:
    _PROMPT_INJECTION_TELEMETRY_METRICS.clear()
