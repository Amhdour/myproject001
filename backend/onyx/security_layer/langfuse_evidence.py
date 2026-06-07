from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from typing import Any
from typing import Protocol

from onyx.security_layer.redaction import safe_metadata

logger = logging.getLogger(__name__)

OPA_RETRIEVAL_ACL_LANGFUSE_OBSERVATION_NAME = "security.opa.retrieval_acl.decision"
RAG_INJECTION_LANGFUSE_OBSERVATION_NAME = "security.rag_injection.scan"
LANGFUSE_PUBLIC_KEY_ENV = "LANGFUSE_PUBLIC_KEY"
LANGFUSE_SECRET_KEY_ENV = "LANGFUSE_SECRET_KEY"

_SAFE_OPA_RETRIEVAL_ACL_FIELDS = frozenset(
    {
        "correlation_id",
        "subject_user_id",
        "subject_tenant_id",
        "resource_document_id",
        "resource_chunk_id",
        "resource_tenant_id",
        "policy_package",
        "decision",
        "reason",
        "fallback_used",
        "enforcement_enabled",
    }
)

_SAFE_RAG_INJECTION_FIELDS = frozenset(
    {
        "scanner_name",
        "scanner_provider",
        "scanner_backend_available",
        "scanner_backend_version",
        "scanner_decision",
        "risk_type",
        "risk_score",
        "sanitized",
        "resource_chunk_id",
        "correlation_id",
        "fallback_used",
    }
)

_SAFE_SCALAR_TYPES = (str, bool, int, float)


class LangfuseObservation(Protocol):
    def end(self) -> None:
        pass


class LangfuseEvidenceClient(Protocol):
    def start_observation(self, **kwargs: Any) -> LangfuseObservation:
        pass


def _langfuse_configured() -> bool:
    return bool(
        os.getenv(LANGFUSE_PUBLIC_KEY_ENV) and os.getenv(LANGFUSE_SECRET_KEY_ENV)
    )


def _get_langfuse_client() -> LangfuseEvidenceClient | None:
    if not _langfuse_configured():
        return None

    try:
        from langfuse import get_client
    except Exception:
        logger.debug("Langfuse SDK unavailable; OPA Retrieval ACL evidence disabled")
        return None

    try:
        return get_client()
    except Exception as e:
        logger.debug(
            "Langfuse client unavailable; OPA Retrieval ACL evidence disabled: %s", e
        )
        return None


def safe_opa_retrieval_acl_langfuse_payload(
    metadata: Mapping[str, object | None],
) -> dict[str, str | bool | int | float]:
    """Return only safe OPA Retrieval ACL evidence fields for Langfuse metadata.

    This adapter is deny-by-default: any field outside the explicit allowlist is
    ignored so raw RAG content, prompts, full documents, tokens, secrets, or PII
    fields cannot be forwarded by accident.
    """

    payload: dict[str, str | bool | int | float] = {}
    for key in _SAFE_OPA_RETRIEVAL_ACL_FIELDS:
        value = metadata.get(key)
        if value is None:
            continue
        if isinstance(value, _SAFE_SCALAR_TYPES):
            payload[key] = value
    redacted_payload = safe_metadata(payload)
    return {
        key: value
        for key, value in redacted_payload.items()
        if isinstance(value, _SAFE_SCALAR_TYPES)
    }


def emit_opa_retrieval_acl_langfuse_evidence(
    metadata: Mapping[str, object | None],
    *,
    client: LangfuseEvidenceClient | None = None,
) -> bool:
    """Emit safe OPA Retrieval ACL metadata to Langfuse when available.

    Returns True only when an observation was created. Missing Langfuse runtime
    configuration, missing SDK dependency, client construction errors, and emit
    errors are all safe no-ops.
    """

    payload = safe_opa_retrieval_acl_langfuse_payload(metadata)
    resolved_client = client or _get_langfuse_client()
    if resolved_client is None:
        return False

    try:
        observation = resolved_client.start_observation(
            name=OPA_RETRIEVAL_ACL_LANGFUSE_OBSERVATION_NAME,
            as_type="span",
            metadata=payload,
        )
        observation.end()
        return True
    except Exception as e:
        logger.debug("Failed to emit OPA Retrieval ACL Langfuse evidence: %s", e)
        return False


def safe_rag_injection_langfuse_payload(
    metadata: Mapping[str, object | None],
) -> dict[str, str | bool | int | float]:
    """Return only safe RAG injection scanner evidence fields for Langfuse.

    The allowlist intentionally excludes raw retrieved chunk text, prompts, full
    document text, and scanner debug payloads. Values still pass through
    ``safe_metadata`` as defense in depth.
    """

    payload: dict[str, str | bool | int | float] = {}
    for key in _SAFE_RAG_INJECTION_FIELDS:
        value = metadata.get(key)
        if value is None:
            continue
        if isinstance(value, _SAFE_SCALAR_TYPES):
            payload[key] = value
    redacted_payload = safe_metadata(payload)
    return {
        key: value
        for key, value in redacted_payload.items()
        if isinstance(value, _SAFE_SCALAR_TYPES)
    }


def emit_rag_injection_langfuse_evidence(
    metadata: Mapping[str, object | None],
    *,
    client: LangfuseEvidenceClient | None = None,
) -> bool:
    """Emit safe RAG injection scanner metadata to Langfuse when available."""

    payload = safe_rag_injection_langfuse_payload(metadata)
    resolved_client = client or _get_langfuse_client()
    if resolved_client is None:
        return False

    try:
        observation = resolved_client.start_observation(
            name=RAG_INJECTION_LANGFUSE_OBSERVATION_NAME,
            as_type="span",
            metadata=payload,
        )
        observation.end()
        return True
    except Exception as e:
        logger.debug("Failed to emit RAG injection Langfuse evidence: %s", e)
        return False
