from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.runtime.denials import DenialCategory
from backend.security_layer.runtime.denials import build_denial_payload
from backend.security_layer.runtime_enforcement.audit import RuntimeAuditEvent
from backend.security_layer.runtime_enforcement.audit import build_runtime_audit_event
from backend.security_layer.runtime_enforcement.audit import write_runtime_audit_event
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementConfig
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementMode
from backend.security_layer.runtime_enforcement.context import RetrievalChunkLike
from backend.security_layer.runtime_enforcement.context import RuntimeRetrievalContext
from backend.security_layer.runtime_enforcement.decision import authorize_runtime_retrieval
from backend.security_layer.runtime_enforcement.telemetry import record_runtime_retrieval_acl_metric


@dataclass(frozen=True)
class RuntimeRetrievalEnforcementResult:
    allowed_chunks: tuple[RetrievalChunkLike, ...]
    denied_chunk_count: int
    decision: str
    reason_code: str
    enforcement_result: str
    audit_event: RuntimeAuditEvent | None
    safe_denial: dict[str, str] | None = None


def enforce_retrieval_runtime(
    *,
    config: RuntimeEnforcementConfig,
    context: RuntimeRetrievalContext,
    chunks: list[RetrievalChunkLike],
) -> RuntimeRetrievalEnforcementResult:
    if config.mode == RuntimeEnforcementMode.DISABLED:
        return RuntimeRetrievalEnforcementResult(
            allowed_chunks=tuple(chunks),
            denied_chunk_count=0,
            decision="allow",
            reason_code="step_39x_disabled",
            enforcement_result="not_applied",
            audit_event=None,
        )

    decision = authorize_runtime_retrieval(context, chunks)
    is_denied = decision.decision == "deny"
    if config.mode == RuntimeEnforcementMode.ENFORCE:
        enforcement_result = "blocked" if is_denied else "allowed"
    else:
        enforcement_result = "observed"
    audit_event = build_runtime_audit_event(
        request_id=context.request_id,
        mode=config.mode,
        action=context.action,
        resource_type=context.resource_type,
        tenant_id=context.tenant_id,
        subject_id=context.subject_id,
        decision=decision.decision,
        reason_code=decision.reason_code,
        enforcement_result=enforcement_result,
    )
    write_runtime_audit_event(audit_event)
    record_runtime_retrieval_acl_metric(
        mode=config.mode,
        decision=decision.decision,
        enforcement_result=enforcement_result,
        denied_chunk_count=decision.denied_chunk_count,
    )

    if config.mode == RuntimeEnforcementMode.MONITOR_ONLY:
        return RuntimeRetrievalEnforcementResult(
            allowed_chunks=tuple(chunks),
            denied_chunk_count=decision.denied_chunk_count,
            decision=decision.decision,
            reason_code=decision.reason_code,
            enforcement_result=enforcement_result,
            audit_event=audit_event,
        )

    if is_denied:
        return RuntimeRetrievalEnforcementResult(
            allowed_chunks=decision.allowed_chunks,
            denied_chunk_count=decision.denied_chunk_count,
            decision=decision.decision,
            reason_code=decision.reason_code,
            enforcement_result=enforcement_result,
            audit_event=audit_event,
            safe_denial=build_denial_payload(
                DenialCategory.RETRIEVAL_DENIED, decision.reason_code
            ).to_dict(),
        )

    return RuntimeRetrievalEnforcementResult(
        allowed_chunks=decision.allowed_chunks,
        denied_chunk_count=0,
        decision=decision.decision,
        reason_code=decision.reason_code,
        enforcement_result="allowed",
        audit_event=audit_event,
    )
