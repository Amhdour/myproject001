from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class MonitorOnlyCandidate(str, Enum):
    RETRIEVAL_LIVE_ACL_CHECK = "LMO-001 retrieval live ACL check"
    SHARED_SINK_CONSOLIDATION = "LMO-002 shared audit/finding/metric sink consolidation"
    POLICY_DECISION_SUMMARY = "LMO-003 policy decision summary"
    CACHE_DRY_RUN_ADAPTER = "LMO-004 cache monitor-only dry-run adapter"
    TOOL_INVOCATION_SUMMARY = "LMO-005 tool invocation summary"
    ARTIFACT_RELEASE_SUMMARY = "LMO-006 artifact release summary"
    INGESTION_METADATA_SUMMARY = "LMO-007 ingestion metadata summary"
    MCP_REQUEST_SUMMARY = "LMO-008 MCP request summary"


SELECTED_MONITOR_ONLY_CANDIDATES: tuple[MonitorOnlyCandidate, ...] = (
    MonitorOnlyCandidate.SHARED_SINK_CONSOLIDATION,
    MonitorOnlyCandidate.CACHE_DRY_RUN_ADAPTER,
)


class MonitorOnlySignalType(str, Enum):
    AUDIT = "audit"
    FINDING = "finding"
    METRIC = "metric"


class MonitorOnlyDecision(str, Enum):
    OBSERVED = "observed"
    SKIPPED_DISABLED = "skipped_disabled"


@dataclass(frozen=True)
class MonitorOnlySignal:
    signal_type: MonitorOnlySignalType
    action: str
    decision: str
    mode: str
    request_id: str
    reason_code: str | None = None
    details: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class MonitorOnlyObservation:
    candidate: MonitorOnlyCandidate
    decision: MonitorOnlyDecision
    request_id: str
    signals: tuple[MonitorOnlySignal, ...] = ()
    notes: tuple[str, ...] = ()


def reviewed_candidate_count() -> int:
    return len(MonitorOnlyCandidate)


def selected_candidate_count() -> int:
    return len(SELECTED_MONITOR_ONLY_CANDIDATES)
