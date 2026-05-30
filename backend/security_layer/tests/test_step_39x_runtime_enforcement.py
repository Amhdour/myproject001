from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.runtime_enforcement.audit import clear_runtime_audit_events
from backend.security_layer.runtime_enforcement.audit import get_runtime_audit_events
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementConfig
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementMode
from backend.security_layer.runtime_enforcement.config import parse_runtime_enforcement_mode
from backend.security_layer.runtime_enforcement.context import RuntimeRetrievalContext
from backend.security_layer.runtime_enforcement.retrieval_adapter import enforce_retrieval_runtime


@dataclass(frozen=True)
class RuntimeProofChunk:
    document_id: str
    chunk_id: int
    metadata: dict[str, str | list[str]]


def _chunk(
    *,
    document_id: str,
    tenant_id: str,
    allowed_subject_ids: list[str] | None = None,
) -> RuntimeProofChunk:
    metadata: dict[str, str | list[str]] = {"tenant_id": tenant_id}
    if allowed_subject_ids is not None:
        metadata["allowed_subject_ids"] = allowed_subject_ids
    return RuntimeProofChunk(document_id=document_id, chunk_id=1, metadata=metadata)


def _context(
    *,
    subject_id: str | None = "user-1",
    tenant_id: str | None = "tenant-a",
) -> RuntimeRetrievalContext:
    return RuntimeRetrievalContext(
        request_id="req-step-39x",
        subject_id=subject_id,
        tenant_id=tenant_id,
    )


def test_step_39x_invalid_mode_is_rejected_without_enabling_enforce() -> None:
    try:
        parse_runtime_enforcement_mode("enfroce")
    except ValueError as exc:
        message = str(exc)
    else:
        raise AssertionError("invalid Step 39X mode unexpectedly parsed")

    assert "Invalid Step 39X runtime enforcement mode" in message
    assert RuntimeEnforcementMode.ENFORCE.value in message

def test_step_39x_disabled_mode_preserves_chunks_and_does_not_audit() -> None:
    clear_runtime_audit_events()
    chunks = [
        _chunk(
            document_id="doc-a",
            tenant_id="tenant-b",
            allowed_subject_ids=["other-user"],
        )
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.DISABLED),
        context=_context(),
        chunks=chunks,
    )

    assert result.allowed_chunks == tuple(chunks)
    assert result.enforcement_result == "not_applied"
    assert result.audit_event is None
    assert get_runtime_audit_events() == []


def test_step_39x_monitor_only_observes_deny_but_preserves_chunks() -> None:
    clear_runtime_audit_events()
    chunks = [
        _chunk(
            document_id="doc-b",
            tenant_id="tenant-b",
            allowed_subject_ids=["other-user"],
        )
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.MONITOR_ONLY),
        context=_context(),
        chunks=chunks,
    )

    assert result.allowed_chunks == tuple(chunks)
    assert result.decision == "deny"
    assert result.enforcement_result == "observed"
    assert result.safe_denial is None
    assert len(get_runtime_audit_events()) == 1


def test_step_39x_enforce_allows_same_tenant_authorized_retrieval() -> None:
    clear_runtime_audit_events()
    chunks = [
        _chunk(
            document_id="doc-allowed",
            tenant_id="tenant-a",
            allowed_subject_ids=["user-1"],
        )
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=_context(),
        chunks=chunks,
    )

    assert result.allowed_chunks == tuple(chunks)
    assert result.decision == "allow"
    assert result.reason_code == "retrieval_authorized"
    assert result.enforcement_result == "allowed"
    assert result.safe_denial is None

    audit_events = get_runtime_audit_events()
    assert len(audit_events) == 1
    event = audit_events[0].to_dict()
    assert event["event_type"] == "step_39x_runtime_retrieval_authorization"
    assert event["decision_id"].startswith("step39x:")
    assert event["request_id"] == "req-step-39x"
    assert event["mode"] == "enforce"
    assert event["action"] == "retrieve"
    assert event["resource_type"] == "chunk"
    assert event["tenant_id"] == "tenant-a"
    assert event["subject_id"] == "user-1"
    assert event["decision"] == "allow"
    assert event["reason_code"] == "retrieval_authorized"
    assert event["timestamp"]
    assert event["enforcement_result"] == "allowed"


def test_step_39x_enforce_blocks_cross_tenant_retrieval_with_safe_denial() -> None:
    clear_runtime_audit_events()
    chunks = [
        _chunk(
            document_id="sensitive-doc-id",
            tenant_id="tenant-b",
            allowed_subject_ids=["user-2"],
        )
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=_context(),
        chunks=chunks,
    )

    assert result.allowed_chunks == ()
    assert result.denied_chunk_count == 1
    assert result.decision == "deny"
    assert result.reason_code == "retrieval_authorization_failed"
    assert result.enforcement_result == "blocked"
    assert result.safe_denial == {
        "category": "retrieval_denied",
        "error_code": "security_retrieval_denied",
        "message": "Request blocked by security policy.",
        "admin_summary": "safe_denial:retrieval_denied; reason=[redacted]",
    }
    denial_text = str(result.safe_denial)
    assert "sensitive-doc-id" not in denial_text
    assert "tenant-b" not in denial_text
    assert "user-2" not in denial_text
    assert "allowed_subject_ids" not in denial_text
    assert "source" not in denial_text
    assert "chunk content" not in denial_text
    assert "policy_engine_rule_42" not in denial_text
    assert "Traceback" not in denial_text
    assert "secret" not in denial_text

    audit_events = get_runtime_audit_events()
    assert len(audit_events) == 1
    event = audit_events[0].to_dict()
    assert event["decision"] == "deny"
    assert event["reason_code"] == "retrieval_authorization_failed"
    assert event["enforcement_result"] == "blocked"


def test_step_39x_enforce_blocks_missing_subject_context() -> None:
    clear_runtime_audit_events()
    chunks = [
        _chunk(
            document_id="doc-no-subject",
            tenant_id="tenant-a",
            allowed_subject_ids=["user-1"],
        )
    ]

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=_context(subject_id=None),
        chunks=chunks,
    )

    assert result.allowed_chunks == ()
    assert result.decision == "deny"
    assert result.reason_code == "missing_subject_context"
    assert result.enforcement_result == "blocked"
    assert result.safe_denial is not None
    assert result.safe_denial["message"] == "Request blocked by security policy."
