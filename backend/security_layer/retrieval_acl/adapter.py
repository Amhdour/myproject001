from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from backend.security_layer.retrieval_acl.enforcer import enforce_retrieval_acl
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLDecision
from backend.security_layer.retrieval_acl.models import RetrievalDocumentACL
from backend.security_layer.retrieval_acl.models import RetrievalResultChunk


@dataclass(frozen=True)
class OnyxLikeRetrievalChunk:
    """Small test double for the Onyx `InferenceChunk` shape.

    This adapter proof intentionally avoids importing the full Onyx model so the
    security proof remains isolated, fast, and CI-friendly. The fields mirror the
    subset of data needed to prove how real retrieved chunks could be translated
    into the Step 21 Retrieval ACL helper model.
    """

    chunk_id: str | int
    document_id: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class RetrievalACLAdapterResult:
    """Adapter output preserving both the ACL decision and original chunks."""

    decision: RetrievalACLDecision
    allowed_original_chunks: tuple[OnyxLikeRetrievalChunk, ...]


def _metadata_string(metadata: dict[str, Any], key: str) -> str | None:
    value = metadata.get(key)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _metadata_string_set(metadata: dict[str, Any], key: str) -> frozenset[str]:
    value = metadata.get(key)
    if value is None:
        return frozenset()
    if isinstance(value, str):
        cleaned = value.strip()
        return frozenset({cleaned}) if cleaned else frozenset()
    if isinstance(value, (list, tuple, set, frozenset)):
        cleaned_values = {
            item.strip()
            for item in value
            if isinstance(item, str) and item.strip()
        }
        return frozenset(cleaned_values)
    return frozenset()


def adapt_onyx_like_chunk_to_retrieval_acl_chunk(
    chunk: OnyxLikeRetrievalChunk | object,
) -> RetrievalResultChunk | object:
    """Translate an Onyx-like retrieved chunk into Step 21 helper input.

    Required metadata keys:
    - `tenant_id`
    - `allowed_subject_ids`

    Optional metadata key:
    - `allowed_group_ids`

    Missing or malformed metadata intentionally produces a malformed object for
    the Step 21 enforcer, which then fails closed instead of silently allowing.
    """

    if not isinstance(chunk, OnyxLikeRetrievalChunk):
        return chunk

    tenant_id = _metadata_string(chunk.metadata, "tenant_id")
    allowed_subject_ids = _metadata_string_set(chunk.metadata, "allowed_subject_ids")
    allowed_group_ids = _metadata_string_set(chunk.metadata, "allowed_group_ids")

    if tenant_id is None or not allowed_subject_ids:
        return object()

    chunk_id = str(chunk.chunk_id)
    return RetrievalResultChunk(
        chunk_id=chunk_id,
        document_id=chunk.document_id,
        tenant_id=tenant_id,
        document_acl=RetrievalDocumentACL(
            tenant_id=tenant_id,
            document_id=chunk.document_id,
            allowed_subject_ids=allowed_subject_ids,
            allowed_group_ids=allowed_group_ids,
        ),
    )


def enforce_retrieval_acl_on_onyx_like_chunks(
    *,
    context: RetrievalACLContext | object | None,
    chunks: Iterable[OnyxLikeRetrievalChunk | object],
    request_id: str = "isolated-onyx-like-retrieval-acl-adapter-proof",
) -> RetrievalACLAdapterResult:
    """Adapt Onyx-like chunks, call the Step 21 helper, and map allowed chunks back.

    This function is intentionally unwired from live Onyx retrieval. It proves an
    adapter shape only: retrieved chunk metadata can be converted to the Step 21
    ACL helper model, filtered, and mapped back to original retrieved chunks.
    """

    original_chunks = tuple(chunks)
    adapted_chunks = tuple(
        adapt_onyx_like_chunk_to_retrieval_acl_chunk(chunk)
        for chunk in original_chunks
    )
    decision = enforce_retrieval_acl(
        context=context,
        chunks=adapted_chunks,
        request_id=request_id,
    )

    allowed_ids = {
        (chunk.document_id, chunk.chunk_id)
        for chunk in decision.allowed_chunks
    }
    allowed_original_chunks = tuple(
        chunk
        for chunk, adapted_chunk in zip(original_chunks, adapted_chunks, strict=True)
        if isinstance(chunk, OnyxLikeRetrievalChunk)
        and isinstance(adapted_chunk, RetrievalResultChunk)
        and (adapted_chunk.document_id, adapted_chunk.chunk_id) in allowed_ids
    )

    return RetrievalACLAdapterResult(
        decision=decision,
        allowed_original_chunks=allowed_original_chunks,
    )
