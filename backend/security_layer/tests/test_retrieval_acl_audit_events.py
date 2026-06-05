from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass

from backend.security_layer.retrieval_acl.audit_events import (
    build_retrieval_acl_audit_event,
)
from backend.security_layer.retrieval_acl.audit_events import (
    clear_retrieval_acl_audit_events,
)
from backend.security_layer.retrieval_acl.audit_events import (
    get_retrieval_acl_audit_events,
)
from backend.security_layer.retrieval_acl.audit_events import (
    record_retrieval_acl_audit_event,
)
from backend.security_layer.retrieval_acl.audit_events import (
    RETRIEVAL_ACL_AUDIT_EVENT_TYPE,
)
from backend.security_layer.retrieval_acl.audit_events import RETRIEVAL_ACL_CONTROL_ID
from backend.security_layer.retrieval_acl.enforce_hook import (
    apply_retrieval_acl_enforcement_hook,
)
from backend.security_layer.retrieval_acl.enforce_hook import RetrievalACLDecision


@dataclass(frozen=True)
class FakeChunk:
    document_id: str
    tenant_id: str
    content: str
    user_prompt: str = "user prompt must never appear in audit events"
    raw_document_body: str = "raw document body must never appear in audit events"
    credentials: str = "credential must never appear in audit events"
    secret: str = "secret must never appear in audit events"
    email: str = "person@example.com"


def _decision_for_chunk(*, chunk: FakeChunk, user_tenant_id: str) -> RetrievalACLDecision:
    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id=user_tenant_id,
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.config.mode == "enforce"
    assert len(result.decisions) == 1
    return result.decisions[0]


def test_build_audit_event_from_allowed_decision() -> None:
    decision = _decision_for_chunk(
        chunk=FakeChunk(
            document_id="tenant-a-allowed-document",
            tenant_id="tenant-a",
            content="ALLOWED CHUNK TEXT",
        ),
        user_tenant_id="tenant-a",
    )

    event = build_retrieval_acl_audit_event(decision)

    assert event.event_type == RETRIEVAL_ACL_AUDIT_EVENT_TYPE
    assert event.control_id == RETRIEVAL_ACL_CONTROL_ID
    assert event.policy_version == "retrieval-acl-v1"
    assert event.mode == "enforce"
    assert event.decision == "allowed"
    assert event.reason == "allowed"
    assert event.user_tenant_id == "tenant-a"
    assert event.chunk_tenant_id == "tenant-a"
    assert event.document_ref.startswith("redacted:")
    assert event.production_readiness == "NO-GO"
    assert event.enterprise_readiness == "NO-GO"


def test_build_audit_event_from_denied_decision() -> None:
    decision = _decision_for_chunk(
        chunk=FakeChunk(
            document_id="tenant-b-denied-document",
            tenant_id="tenant-b",
            content="DENIED CHUNK TEXT",
        ),
        user_tenant_id="tenant-a",
    )

    event = build_retrieval_acl_audit_event(decision)

    assert event.event_type == "retrieval_acl.decision"
    assert event.control_id == "retrieval-acl-enforcement-v1"
    assert event.mode == "enforce"
    assert event.decision == "denied"
    assert event.reason == "tenant_mismatch"
    assert event.user_tenant_id == "tenant-a"
    assert event.chunk_tenant_id == "tenant-b"
    assert event.production_readiness == "NO-GO"
    assert event.enterprise_readiness == "NO-GO"


def test_audit_event_records_no_chunk_content() -> None:
    chunk = FakeChunk(
        document_id="tenant-b-redaction-document",
        tenant_id="tenant-b",
        content="PRIVATE CHUNK TEXT MUST NOT BE STORED",
    )
    decision = _decision_for_chunk(chunk=chunk, user_tenant_id="tenant-a")

    event = build_retrieval_acl_audit_event(decision)
    serialized_event = str(asdict(event))

    assert "PRIVATE CHUNK TEXT MUST NOT BE STORED" not in serialized_event
    assert chunk.user_prompt not in serialized_event
    assert chunk.raw_document_body not in serialized_event
    assert chunk.credentials not in serialized_event
    assert chunk.secret not in serialized_event
    assert chunk.email not in serialized_event


def test_audit_sink_records_and_returns_events() -> None:
    clear_retrieval_acl_audit_events()
    decision = _decision_for_chunk(
        chunk=FakeChunk(
            document_id="tenant-a-record-document",
            tenant_id="tenant-a",
            content="RECORDED CHUNK TEXT",
        ),
        user_tenant_id="tenant-a",
    )
    clear_retrieval_acl_audit_events()
    event = build_retrieval_acl_audit_event(decision)

    record_retrieval_acl_audit_event(event)

    assert get_retrieval_acl_audit_events() == (event,)


def test_audit_sink_clear_removes_events() -> None:
    clear_retrieval_acl_audit_events()
    decision = _decision_for_chunk(
        chunk=FakeChunk(
            document_id="tenant-a-clear-document",
            tenant_id="tenant-a",
            content="CLEAR CHUNK TEXT",
        ),
        user_tenant_id="tenant-a",
    )
    record_retrieval_acl_audit_event(build_retrieval_acl_audit_event(decision))

    clear_retrieval_acl_audit_events()

    assert get_retrieval_acl_audit_events() == ()


def test_demo_attack_denial_produces_redacted_audit_event() -> None:
    clear_retrieval_acl_audit_events()
    victim_chunk = FakeChunk(
        document_id="customer-private-doc-tenant-b",
        tenant_id="tenant-b",
        content="CUSTOMER SECRET FROM TENANT B",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[victim_chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )
    assert result.returned_chunks == []
    assert result.decisions[0].allowed is False

    event = get_retrieval_acl_audit_events()[0]
    serialized_event = str(asdict(event))
    assert event.event_type == "retrieval_acl.decision"
    assert event.decision == "denied"
    assert event.mode == "enforce"
    assert event.user_tenant_id == "tenant-a"
    assert event.chunk_tenant_id == "tenant-b"
    assert event.production_readiness == "NO-GO"
    assert event.enterprise_readiness == "NO-GO"
    assert "CUSTOMER SECRET FROM TENANT B" not in serialized_event
    assert get_retrieval_acl_audit_events() == (event,)


def test_audit_event_preserves_no_go_readiness_boundaries() -> None:
    decision = _decision_for_chunk(
        chunk=FakeChunk(
            document_id="tenant-b-readiness-document",
            tenant_id="tenant-b",
            content="READINESS CHUNK TEXT",
        ),
        user_tenant_id="tenant-a",
    )

    event = build_retrieval_acl_audit_event(decision)

    assert event.production_readiness == "NO-GO"
    assert event.enterprise_readiness == "NO-GO"
    assert "production_ready" not in str(asdict(event)).lower()
    assert "enterprise_ready" not in str(asdict(event)).lower()
