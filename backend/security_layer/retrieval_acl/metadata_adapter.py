from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RetrievalACLMetadata:
    """Redacted Retrieval ACL metadata extracted from a retrieval chunk.

    This adapter intentionally avoids storing chunk text fields such as
    ``content``, ``blurb``, highlights, summaries, or context. Decision records
    should only receive the redacted document reference and tenant boundary
    values needed for Retrieval ACL Enforcement v1.
    """

    document_ref: str
    chunk_tenant_id: str | None
    user_tenant_id: str | None
    metadata_present: bool
    reason: str | None


def redact_document_ref(document_id: Any) -> str:
    if not document_id:
        return "missing"
    text = str(document_id)
    if len(text) <= 8:
        return "redacted"
    return f"redacted:{text[:4]}...{text[-4:]}"


def _read_attr_or_key(value: Any, name: str) -> Any:
    if isinstance(value, dict):
        return value.get(name)
    return getattr(value, name, None)


def _read_nested_mapping_value(value: Any, mapping_name: str, key: str) -> Any:
    mapping = _read_attr_or_key(value, mapping_name)
    if isinstance(mapping, dict):
        return mapping.get(key)
    return None


def _extract_document_id(chunk: Any) -> Any:
    for field_name in ("document_id", "doc_id"):
        document_id = _read_attr_or_key(chunk, field_name)
        if document_id:
            return document_id
    return None


def _extract_chunk_tenant_id(chunk: Any) -> Any:
    direct_tenant_id = _read_attr_or_key(chunk, "tenant_id")
    if direct_tenant_id:
        return direct_tenant_id

    for mapping_name in ("metadata", "retrieval_metadata", "acl_metadata"):
        for tenant_key in ("tenant_id", "onyx_tenant_id", "tenant"):
            tenant_id = _read_nested_mapping_value(chunk, mapping_name, tenant_key)
            if tenant_id:
                return tenant_id

    source_document = _read_attr_or_key(chunk, "source_document")
    if source_document is not None:
        source_document_tenant_id = _read_attr_or_key(source_document, "tenant_id")
        if source_document_tenant_id:
            return source_document_tenant_id

    return None


def extract_retrieval_acl_metadata(
    *,
    chunk: Any,
    user_tenant_id: str | None,
) -> RetrievalACLMetadata:
    """Extract redacted ACL metadata from a real retrieval chunk-like object."""

    document_id = _extract_document_id(chunk)
    chunk_tenant_id = _extract_chunk_tenant_id(chunk)

    missing_reasons: list[str] = []
    if not document_id:
        missing_reasons.append("missing_document_id")
    if not chunk_tenant_id:
        missing_reasons.append("missing_chunk_tenant_id")
    if not user_tenant_id:
        missing_reasons.append("missing_user_tenant_id")

    return RetrievalACLMetadata(
        document_ref=redact_document_ref(document_id),
        chunk_tenant_id=str(chunk_tenant_id) if chunk_tenant_id else None,
        user_tenant_id=str(user_tenant_id) if user_tenant_id else None,
        metadata_present=not missing_reasons,
        reason=",".join(missing_reasons) if missing_reasons else None,
    )
