from __future__ import annotations

from typing import Any

from onyx.security_layer.langfuse_evidence import (
    OPA_RETRIEVAL_ACL_LANGFUSE_OBSERVATION_NAME,
)
from onyx.security_layer.langfuse_evidence import emit_opa_retrieval_acl_langfuse_evidence
from onyx.security_layer.langfuse_evidence import safe_opa_retrieval_acl_langfuse_payload


class RecordingObservation:
    def __init__(self) -> None:
        self.ended = False

    def end(self) -> None:
        self.ended = True


class RecordingLangfuseClient:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.observation = RecordingObservation()

    def start_observation(self, **kwargs: Any) -> RecordingObservation:
        self.calls.append(kwargs)
        return self.observation


def _safe_metadata() -> dict[str, object | None]:
    return {
        "correlation_id": "corr-1",
        "subject_user_id": "user-1",
        "subject_tenant_id": "tenant-a",
        "resource_document_id": "doc-1",
        "resource_chunk_id": "chunk-1",
        "resource_tenant_id": "tenant-a",
        "policy_package": "onyx.security.retrieval_acl",
        "decision": "allow",
        "reason": "same tenant allowed user",
        "fallback_used": False,
        "enforcement_enabled": True,
    }


def test_langfuse_evidence_adapter_accepts_safe_payload() -> None:
    payload = safe_opa_retrieval_acl_langfuse_payload(_safe_metadata())

    assert payload == _safe_metadata()


def test_langfuse_evidence_adapter_ignores_unsafe_raw_content_fields() -> None:
    metadata = {
        **_safe_metadata(),
        "chunk_text": "raw secret chunk text",
        "raw_prompt": "raw prompt text",
        "full_document_content": "full document content",
        "auth_token": "token",
        "secret": "secret",
        "reason": {"raw_content": "nested content is not scalar"},
    }

    payload = safe_opa_retrieval_acl_langfuse_payload(metadata)
    serialized_payload = str(payload)

    assert "chunk_text" not in payload
    assert "raw_prompt" not in payload
    assert "full_document_content" not in payload
    assert "auth_token" not in payload
    assert "secret" not in payload
    assert "reason" not in payload
    assert "raw secret chunk text" not in serialized_payload
    assert "raw prompt text" not in serialized_payload
    assert "full document content" not in serialized_payload
    assert "token" not in serialized_payload


def test_langfuse_evidence_adapter_redacts_selected_metadata_defense_in_depth() -> None:
    payload = safe_opa_retrieval_acl_langfuse_payload(
        {
            **_safe_metadata(),
            "reason": "upstream note included admin@example.com",
        }
    )

    assert payload["reason"] == "upstream note included [REDACTED]"
    assert payload["correlation_id"] == "corr-1"
    assert payload["decision"] == "allow"
    assert payload["policy_package"] == "onyx.security.retrieval_acl"
    assert payload["fallback_used"] is False
    assert payload["enforcement_enabled"] is True


def test_langfuse_evidence_adapter_noops_without_runtime_config(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_PUBLIC_KEY", raising=False)
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)

    emitted = emit_opa_retrieval_acl_langfuse_evidence(_safe_metadata())

    assert emitted is False


def test_langfuse_evidence_adapter_emits_metadata_with_injected_client() -> None:
    client = RecordingLangfuseClient()

    emitted = emit_opa_retrieval_acl_langfuse_evidence(
        {
            **_safe_metadata(),
            "chunk_text": "raw secret chunk text",
        },
        client=client,
    )

    assert emitted is True
    assert client.observation.ended is True
    assert client.calls == [
        {
            "name": OPA_RETRIEVAL_ACL_LANGFUSE_OBSERVATION_NAME,
            "as_type": "span",
            "metadata": _safe_metadata(),
        }
    ]
