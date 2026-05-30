from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.security_layer.runtime_enforcement.context import RetrievalChunkLike
from backend.security_layer.runtime_enforcement.context import RuntimeRetrievalContext
from backend.security_layer.runtime_enforcement.context import chunk_allowed_subject_ids
from backend.security_layer.runtime_enforcement.context import chunk_tenant_id


RuntimeDecision = Literal["allow", "deny"]


@dataclass(frozen=True)
class RuntimeRetrievalDecision:
    decision: RuntimeDecision
    reason_code: str
    allowed_chunks: tuple[RetrievalChunkLike, ...]
    denied_chunk_count: int


def authorize_runtime_retrieval(
    context: RuntimeRetrievalContext,
    chunks: list[RetrievalChunkLike],
) -> RuntimeRetrievalDecision:
    if context.subject_id is None or context.subject_id == "":
        return RuntimeRetrievalDecision(
            decision="deny",
            reason_code="missing_subject_context",
            allowed_chunks=(),
            denied_chunk_count=len(chunks),
        )
    if context.tenant_id is None or context.tenant_id == "":
        return RuntimeRetrievalDecision(
            decision="deny",
            reason_code="missing_tenant_context",
            allowed_chunks=(),
            denied_chunk_count=len(chunks),
        )

    allowed_chunks: list[RetrievalChunkLike] = []
    denied_count = 0
    for chunk in chunks:
        candidate_tenant_id = chunk_tenant_id(chunk, context.tenant_id)
        allowed_subject_ids = chunk_allowed_subject_ids(chunk)
        tenant_allowed = candidate_tenant_id == context.tenant_id
        subject_allowed = (
            not allowed_subject_ids or context.subject_id in allowed_subject_ids
        )
        if tenant_allowed and subject_allowed:
            allowed_chunks.append(chunk)
        else:
            denied_count += 1

    if denied_count:
        return RuntimeRetrievalDecision(
            decision="deny",
            reason_code="retrieval_authorization_failed",
            allowed_chunks=tuple(allowed_chunks),
            denied_chunk_count=denied_count,
        )

    return RuntimeRetrievalDecision(
        decision="allow",
        reason_code="retrieval_authorized",
        allowed_chunks=tuple(allowed_chunks),
        denied_chunk_count=0,
    )
