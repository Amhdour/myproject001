from __future__ import annotations

from collections.abc import Iterable

from backend.security_layer.retrieval_acl.audit import build_retrieval_acl_audit_event
from backend.security_layer.retrieval_acl.audit import write_retrieval_acl_audit_event
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLDenial
from backend.security_layer.retrieval_acl.models import RetrievalACLDecision
from backend.security_layer.retrieval_acl.models import RetrievalACLReason
from backend.security_layer.retrieval_acl.models import RetrievalDocumentACL
from backend.security_layer.retrieval_acl.models import RetrievalResultChunk


def _is_non_empty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_string_frozenset(value: object) -> bool:
    return isinstance(value, frozenset) and all(_is_non_empty_string(item) for item in value)


def _is_well_formed_context(context: object) -> bool:
    if not isinstance(context, RetrievalACLContext):
        return False
    return (
        _is_non_empty_string(context.tenant_id)
        and _is_non_empty_string(context.subject_id)
        and _is_string_frozenset(context.allowed_document_ids)
        and _is_string_frozenset(context.group_ids)
    )


def _is_well_formed_acl(document_acl: object) -> bool:
    if not isinstance(document_acl, RetrievalDocumentACL):
        return False
    return (
        _is_non_empty_string(document_acl.tenant_id)
        and _is_non_empty_string(document_acl.document_id)
        and _is_string_frozenset(document_acl.allowed_subject_ids)
        and _is_string_frozenset(document_acl.allowed_group_ids)
    )


def _is_well_formed_chunk(chunk: object) -> bool:
    if not isinstance(chunk, RetrievalResultChunk):
        return False
    return (
        _is_non_empty_string(chunk.chunk_id)
        and _is_non_empty_string(chunk.document_id)
        and _is_non_empty_string(chunk.tenant_id)
        and _is_well_formed_acl(chunk.document_acl)
        and chunk.document_acl.document_id == chunk.document_id
        and chunk.document_acl.tenant_id == chunk.tenant_id
    )


def _deny_all(
    *,
    chunks: tuple[object, ...],
    reason: RetrievalACLReason,
) -> tuple[RetrievalACLDenial, ...]:
    if not chunks:
        return (RetrievalACLDenial(chunk_id=None, document_id=None, reason=reason),)
    return tuple(
        RetrievalACLDenial(
            chunk_id=chunk.chunk_id if isinstance(chunk, RetrievalResultChunk) else None,
            document_id=chunk.document_id if isinstance(chunk, RetrievalResultChunk) else None,
            reason=reason,
        )
        for chunk in chunks
    )


def _authorize_well_formed_chunk(
    context: RetrievalACLContext,
    chunk: RetrievalResultChunk,
) -> RetrievalACLDenial | None:
    if chunk.tenant_id != context.tenant_id or chunk.document_acl.tenant_id != context.tenant_id:
        return RetrievalACLDenial(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            reason=RetrievalACLReason.CROSS_TENANT_RESULT,
        )

    if chunk.document_id not in context.allowed_document_ids:
        return RetrievalACLDenial(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            reason=RetrievalACLReason.UNAUTHORIZED_DOCUMENT_ID,
        )

    subject_is_allowed = context.subject_id in chunk.document_acl.allowed_subject_ids
    group_is_allowed = bool(context.group_ids & chunk.document_acl.allowed_group_ids)
    if not subject_is_allowed and not group_is_allowed:
        return RetrievalACLDenial(
            chunk_id=chunk.chunk_id,
            document_id=chunk.document_id,
            reason=RetrievalACLReason.DOCUMENT_ACL_MISMATCH,
        )

    return None


def enforce_retrieval_acl(
    *,
    context: RetrievalACLContext | object | None,
    chunks: Iterable[RetrievalResultChunk | object],
    request_id: str = "isolated-retrieval-acl-runtime-proof",
) -> RetrievalACLDecision:
    """Filter isolated retrieval chunks by tenant and document ACL, failing closed.

    This helper is intentionally unwired from live Onyx retrieval request paths. It proves
    a runtime authorization shape: malformed or unauthorized candidates are denied before
    the caller receives the filtered result set.
    """

    candidate_chunks = tuple(chunks)
    if context is None:
        decision = RetrievalACLDecision(
            status="deny",
            allowed_chunks=(),
            denials=_deny_all(
                chunks=candidate_chunks,
                reason=RetrievalACLReason.MISSING_ACL_CONTEXT,
            ),
        )
        _audit_if_denied_or_filtered(request_id=request_id, decision=decision)
        return decision

    if not _is_well_formed_context(context):
        decision = RetrievalACLDecision(
            status="deny",
            allowed_chunks=(),
            denials=_deny_all(
                chunks=candidate_chunks,
                reason=RetrievalACLReason.MALFORMED_ACL_CONTEXT,
            ),
        )
        _audit_if_denied_or_filtered(request_id=request_id, decision=decision)
        return decision

    allowed_chunks: list[RetrievalResultChunk] = []
    denials: list[RetrievalACLDenial] = []
    for chunk in candidate_chunks:
        if not _is_well_formed_chunk(chunk):
            denials.append(
                RetrievalACLDenial(
                    chunk_id=chunk.chunk_id if isinstance(chunk, RetrievalResultChunk) else None,
                    document_id=chunk.document_id if isinstance(chunk, RetrievalResultChunk) else None,
                    reason=RetrievalACLReason.MALFORMED_ACL_CONTEXT,
                )
            )
            continue

        denial = _authorize_well_formed_chunk(context, chunk)
        if denial is None:
            allowed_chunks.append(chunk)
        else:
            denials.append(denial)

    status = "allow" if not denials else "filter" if allowed_chunks else "deny"
    decision = RetrievalACLDecision(
        status=status,
        allowed_chunks=tuple(allowed_chunks),
        denials=tuple(denials),
    )
    _audit_if_denied_or_filtered(request_id=request_id, decision=decision)
    return decision


def _audit_if_denied_or_filtered(*, request_id: str, decision: RetrievalACLDecision) -> None:
    if decision.status == "allow":
        return
    write_retrieval_acl_audit_event(
        build_retrieval_acl_audit_event(
            request_id=request_id,
            status=decision.status,
            denials=decision.denials,
        )
    )
