from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone

from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementMode


@dataclass(frozen=True)
class RuntimeRetrievalAclMetric:
    metric_name: str
    mode: str
    decision: str
    enforcement_result: str
    denied_chunk_count: int
    timestamp: str

    def to_dict(self) -> dict[str, str | int]:
        return asdict(self)


_RUNTIME_RETRIEVAL_ACL_METRICS: list[RuntimeRetrievalAclMetric] = []


def record_runtime_retrieval_acl_metric(
    *,
    mode: RuntimeEnforcementMode,
    decision: str,
    enforcement_result: str,
    denied_chunk_count: int,
) -> RuntimeRetrievalAclMetric:
    metric = RuntimeRetrievalAclMetric(
        metric_name="retrieval_acl_decision_total",
        mode=mode.value,
        decision=decision,
        enforcement_result=enforcement_result,
        denied_chunk_count=denied_chunk_count,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
    _RUNTIME_RETRIEVAL_ACL_METRICS.append(metric)
    return metric


def get_runtime_retrieval_acl_metrics() -> list[RuntimeRetrievalAclMetric]:
    return list(_RUNTIME_RETRIEVAL_ACL_METRICS)


def clear_runtime_retrieval_acl_metrics() -> None:
    _RUNTIME_RETRIEVAL_ACL_METRICS.clear()
