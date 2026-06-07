from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from enum import Enum
from typing import Generic
from typing import Protocol
from typing import TypeVar


class RetrievedContentPromptInjectionMode(str, Enum):
    DISABLED = "disabled"
    MONITOR = "monitor"
    SHADOW_DENY = "shadow_deny"
    ENFORCE = "enforce"


class RetrievedContentPromptInjectionDecision(str, Enum):
    ALLOW = "allow"
    MONITOR = "monitor"
    QUARANTINE = "quarantine"
    DENY = "deny"


class RetrievedContentChunkLike(Protocol):
    document_id: str
    chunk_id: int | str
    metadata: dict[str, str | list[str]]
    source_type: object
    blurb: str | None
    doc_summary: str | None
    chunk_context: str | None
    match_highlights: list[str]


@dataclass(frozen=True)
class RetrievedContentPromptInjectionContext:
    request_id: str
    user_id: str | None
    tenant_id: str | None
    correlation_id: str | None = None
    policy_id: str = "retrieved_content_prompt_injection_v1"


@dataclass(frozen=True)
class RetrievedContentPromptInjectionAuditEvent:
    event_type: str
    policy_id: str
    request_id: str
    correlation_id: str | None
    mode: str
    decision: str
    reason: str
    user_id: str | None
    tenant_id: str | None
    source_types: tuple[str, ...]
    document_ids: tuple[str, ...]
    chunk_ids: tuple[str, ...]
    matched_pattern_names: tuple[str, ...]
    quarantined_chunk_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RetrievedContentPromptInjectionTelemetrySnapshot:
    checked_count: int
    detected_count: int
    allow_count: int
    monitor_count: int
    quarantine_count: int
    deny_count: int
    storage_scope: str = "in_memory_only"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


ChunkT = TypeVar("ChunkT", bound=RetrievedContentChunkLike)


@dataclass(frozen=True)
class RetrievedContentPromptInjectionHookResult(Generic[ChunkT]):
    returned_chunks: tuple[ChunkT, ...]
    quarantined_chunk_ids: tuple[str, ...]
    decision: RetrievedContentPromptInjectionDecision
    reason: str
    matched_pattern_names: tuple[str, ...]
    audit_event: RetrievedContentPromptInjectionAuditEvent | None
    telemetry_snapshot: RetrievedContentPromptInjectionTelemetrySnapshot
