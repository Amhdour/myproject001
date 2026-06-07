from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.retrieval.prompt_injection.audit import (
    build_retrieved_content_prompt_injection_audit_event,
)
from backend.security_layer.retrieval.prompt_injection.audit import (
    write_retrieved_content_prompt_injection_audit_event,
)
from backend.security_layer.retrieval.prompt_injection.config import (
    get_retrieved_content_prompt_injection_config,
)
from backend.security_layer.retrieval.prompt_injection.config import (
    RetrievedContentPromptInjectionConfig,
)
from backend.security_layer.retrieval.prompt_injection.detector import (
    detect_retrieved_content_prompt_injection_signals,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentChunkLike,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionContext,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionDecision,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionHookResult,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionMode,
)
from backend.security_layer.retrieval.prompt_injection.models import (
    RetrievedContentPromptInjectionTelemetrySnapshot,
)
from backend.security_layer.retrieval.prompt_injection.telemetry import (
    record_retrieved_content_prompt_injection_metric,
)


@dataclass(frozen=True)
class RetrievedContentPromptInjectionChunkDecision:
    chunk: RetrievedContentChunkLike
    matched_pattern_names: tuple[str, ...]


def _chunk_source_type(chunk: RetrievedContentChunkLike) -> str:
    source_type = getattr(chunk, "source_type", None)
    if source_type is None:
        return "unknown"
    value = getattr(source_type, "value", None)
    if value is not None:
        return str(value)
    return str(source_type)


def _chunk_id(chunk: RetrievedContentChunkLike) -> str:
    return str(getattr(chunk, "chunk_id", "unknown"))


def _document_id(chunk: RetrievedContentChunkLike) -> str:
    return str(getattr(chunk, "document_id", "unknown"))


def apply_retrieved_content_prompt_injection_hook(
    *,
    chunks: list[RetrievedContentChunkLike],
    request_id: str,
    user_id: str | None,
    tenant_id: str | None,
    correlation_id: str | None = None,
    config: RetrievedContentPromptInjectionConfig | None = None,
) -> RetrievedContentPromptInjectionHookResult[RetrievedContentChunkLike]:
    resolved_config = config or get_retrieved_content_prompt_injection_config()
    if resolved_config.mode == RetrievedContentPromptInjectionMode.DISABLED:
        return RetrievedContentPromptInjectionHookResult(
            returned_chunks=tuple(chunks),
            quarantined_chunk_ids=(),
            decision=RetrievedContentPromptInjectionDecision.ALLOW,
            reason="retrieved-content prompt injection hook disabled",
            matched_pattern_names=(),
            audit_event=None,
            telemetry_snapshot=RetrievedContentPromptInjectionTelemetrySnapshot(
                checked_count=len(chunks),
                detected_count=0,
                allow_count=len(chunks),
                monitor_count=0,
                quarantine_count=0,
                deny_count=0,
            ),
        )

    matched_chunks: list[RetrievedContentPromptInjectionChunkDecision] = []
    safe_chunks: list[RetrievedContentChunkLike] = []
    quarantined_chunk_ids: list[str] = []
    source_types: list[str] = []
    document_ids: list[str] = []
    chunk_ids: list[str] = []
    matched_pattern_names: list[str] = []

    for chunk in chunks:
        source_types.append(_chunk_source_type(chunk))
        document_ids.append(_document_id(chunk))
        chunk_ids.append(_chunk_id(chunk))
        matches = detect_retrieved_content_prompt_injection_signals(chunk)
        if not matches:
            safe_chunks.append(chunk)
            continue
        matched_chunks.append(RetrievedContentPromptInjectionChunkDecision(chunk=chunk, matched_pattern_names=matches))
        matched_pattern_names.extend(matches)
        quarantined_chunk_ids.append(_chunk_id(chunk))
        if resolved_config.mode == RetrievedContentPromptInjectionMode.MONITOR:
            safe_chunks.append(chunk)

    detected_count = len(matched_chunks)
    if detected_count == 0:
        decision = RetrievedContentPromptInjectionDecision.ALLOW
        reason = "no retrieved-content prompt injection signals detected"
        returned_chunks = tuple(chunks)
        quarantined_chunk_ids = []
    elif resolved_config.mode == RetrievedContentPromptInjectionMode.MONITOR:
        decision = RetrievedContentPromptInjectionDecision.MONITOR
        reason = "retrieved-content prompt injection signals detected in monitor mode"
        returned_chunks = tuple(chunks)
    elif resolved_config.mode == RetrievedContentPromptInjectionMode.SHADOW_DENY:
        decision = RetrievedContentPromptInjectionDecision.QUARANTINE
        reason = "retrieved-content prompt injection signals quarantined in shadow-deny mode"
        returned_chunks = tuple(safe_chunks)
    else:
        if safe_chunks:
            decision = RetrievedContentPromptInjectionDecision.QUARANTINE
            reason = "retrieved-content prompt injection signals quarantined in enforce mode"
            returned_chunks = tuple(safe_chunks)
        else:
            decision = RetrievedContentPromptInjectionDecision.DENY
            reason = "retrieved-content prompt injection signals denied in enforce mode"
            returned_chunks = ()

    telemetry_snapshot = RetrievedContentPromptInjectionTelemetrySnapshot(
        checked_count=len(chunks),
        detected_count=detected_count,
        allow_count=len(returned_chunks) if decision == RetrievedContentPromptInjectionDecision.ALLOW else len(safe_chunks),
        monitor_count=1 if decision == RetrievedContentPromptInjectionDecision.MONITOR else 0,
        quarantine_count=1 if decision == RetrievedContentPromptInjectionDecision.QUARANTINE else 0,
        deny_count=1 if decision == RetrievedContentPromptInjectionDecision.DENY else 0,
    )
    record_retrieved_content_prompt_injection_metric(
        mode=resolved_config.mode,
        decision=decision,
        checked_count=telemetry_snapshot.checked_count,
        detected_count=telemetry_snapshot.detected_count,
        quarantined_count=len(quarantined_chunk_ids),
    )

    context = RetrievedContentPromptInjectionContext(
        request_id=request_id,
        user_id=user_id,
        tenant_id=tenant_id,
        correlation_id=correlation_id,
    )
    audit_event = build_retrieved_content_prompt_injection_audit_event(
        context=context,
        mode=resolved_config.mode,
        decision=decision,
        reason=reason,
        source_types=tuple(sorted(set(source_types))),
        document_ids=tuple(sorted(set(document_ids))),
        chunk_ids=tuple(sorted(set(chunk_ids))),
        matched_pattern_names=tuple(sorted(set(matched_pattern_names))),
        quarantined_chunk_ids=tuple(sorted(set(quarantined_chunk_ids))),
    )
    write_retrieved_content_prompt_injection_audit_event(audit_event)
    return RetrievedContentPromptInjectionHookResult(
        returned_chunks=returned_chunks,
        quarantined_chunk_ids=tuple(sorted(set(quarantined_chunk_ids))),
        decision=decision,
        reason=reason,
        matched_pattern_names=tuple(sorted(set(matched_pattern_names))),
        audit_event=audit_event,
        telemetry_snapshot=telemetry_snapshot,
    )
