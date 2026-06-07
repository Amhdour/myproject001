from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from uuid import uuid4

from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionContext,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionDecision,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionMode,
)


@dataclass(frozen=True)
class RetrievedContentPromptInjectionDecisionEvent:
    event_type: str
    decision_id: str
    request_id: str
    correlation_id: str | None
    policy_id: str
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
    timestamp: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_RETRIEVED_CONTENT_PROMPT_INJECTION_AUDIT_EVENTS: list[RetrievedContentPromptInjectionDecisionEvent] = []


def build_retrieved_content_prompt_injection_audit_event(
    *,
    context: RetrievedContentPromptInjectionContext,
    mode: RetrievedContentPromptInjectionMode,
    decision: RetrievedContentPromptInjectionDecision,
    reason: str,
    source_types: tuple[str, ...],
    document_ids: tuple[str, ...],
    chunk_ids: tuple[str, ...],
    matched_pattern_names: tuple[str, ...],
    quarantined_chunk_ids: tuple[str, ...],
) -> RetrievedContentPromptInjectionDecisionEvent:
    return RetrievedContentPromptInjectionDecisionEvent(
        event_type="retrieved_content_prompt_injection.decision",
        decision_id=f"rcpi:{uuid4()}",
        request_id=context.request_id,
        correlation_id=context.correlation_id,
        policy_id=context.policy_id,
        mode=mode.value,
        decision=decision.value,
        reason=reason,
        user_id=context.user_id,
        tenant_id=context.tenant_id,
        source_types=source_types,
        document_ids=document_ids,
        chunk_ids=chunk_ids,
        matched_pattern_names=matched_pattern_names,
        quarantined_chunk_ids=quarantined_chunk_ids,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


def write_retrieved_content_prompt_injection_audit_event(
    event: RetrievedContentPromptInjectionDecisionEvent,
) -> None:
    _RETRIEVED_CONTENT_PROMPT_INJECTION_AUDIT_EVENTS.append(event)


def get_retrieved_content_prompt_injection_audit_events() -> list[RetrievedContentPromptInjectionDecisionEvent]:
    return list(_RETRIEVED_CONTENT_PROMPT_INJECTION_AUDIT_EVENTS)


def clear_retrieved_content_prompt_injection_audit_events() -> None:
    _RETRIEVED_CONTENT_PROMPT_INJECTION_AUDIT_EVENTS.clear()
