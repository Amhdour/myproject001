from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class RetrievalChunkLike(Protocol):
    document_id: str
    chunk_id: int
    metadata: dict[str, str | list[str]]


@dataclass(frozen=True)
class RuntimeRetrievalContext:
    request_id: str
    subject_id: str | None
    tenant_id: str | None
    action: str = "retrieve"
    resource_type: str = "chunk"


def _metadata_values(chunk: RetrievalChunkLike, key: str) -> tuple[str, ...]:
    raw_value = chunk.metadata.get(key)
    if raw_value is None:
        return ()
    if isinstance(raw_value, list):
        return tuple(str(value) for value in raw_value)
    return (str(raw_value),)


def chunk_tenant_id(chunk: RetrievalChunkLike, fallback_tenant_id: str | None) -> str | None:
    values = _metadata_values(chunk, "tenant_id")
    if values:
        return values[0]
    return fallback_tenant_id


def chunk_allowed_subject_ids(chunk: RetrievalChunkLike) -> tuple[str, ...]:
    return _metadata_values(chunk, "allowed_subject_ids")
