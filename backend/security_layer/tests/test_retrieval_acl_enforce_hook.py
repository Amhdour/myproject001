from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.retrieval_acl.enforce_hook import (
    apply_retrieval_acl_enforcement_hook,
)


@dataclass
class FakeChunk:
    document_id: str | None
    tenant_id: str | None
    content: str = "secret content must not appear in decisions"


def test_off_mode_returns_chunks_unchanged() -> None:
    chunks = [
        FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
        FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
    ]

    result = apply_retrieval_acl_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "off"},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks is chunks
    assert result.behavior_changed is False
    assert result.observed_chunk_count == 2
    assert result.returned_chunk_count == 2


def test_shadow_mode_records_decisions_but_returns_chunks_unchanged() -> None:
    chunks = [
        FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
        FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
    ]

    result = apply_retrieval_acl_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "shadow"},
    )

    assert result.config.mode == "shadow"
    assert result.returned_chunks is chunks
    assert result.behavior_changed is False
    assert len(result.decisions) == 2
    assert result.decisions[0].allowed is True
    assert result.decisions[1].allowed is False
    assert result.decisions[1].reason == "tenant_mismatch"


def test_enforce_mode_removes_cross_tenant_chunks() -> None:
    allowed_chunk = FakeChunk(document_id="doc-a", tenant_id="tenant-a")
    denied_chunk = FakeChunk(document_id="doc-b", tenant_id="tenant-b")
    chunks = [allowed_chunk, denied_chunk]

    result = apply_retrieval_acl_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == [allowed_chunk]
    assert result.behavior_changed is True
    assert result.observed_chunk_count == 2
    assert result.returned_chunk_count == 1
    assert result.decisions[0].allowed is True
    assert result.decisions[1].allowed is False
    assert result.decisions[1].reason == "tenant_mismatch"


def test_enforce_mode_fails_closed_when_acl_metadata_missing() -> None:
    chunks = [
        FakeChunk(document_id=None, tenant_id="tenant-a"),
        FakeChunk(document_id="doc-b", tenant_id=None),
    ]

    result = apply_retrieval_acl_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.returned_chunks == []
    assert result.behavior_changed is True
    assert all(decision.allowed is False for decision in result.decisions)
    assert all(
        decision.reason == "missing_acl_metadata" for decision in result.decisions
    )


def test_demo_attack_cross_tenant_retrieval_is_blocked_in_enforce_mode() -> None:
    attacker_tenant = "tenant-a"
    unauthorized_chunk = FakeChunk(
        document_id="customer-private-doc-tenant-b",
        tenant_id="tenant-b",
        content="PRIVATE TENANT B DATA",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[unauthorized_chunk],
        user_tenant_id=attacker_tenant,
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.returned_chunks == []
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason == "tenant_mismatch"
    assert "PRIVATE TENANT B DATA" not in str(result.decisions[0])
    assert result.decisions[0].production_readiness == "NO-GO"
    assert result.decisions[0].enterprise_readiness == "NO-GO"
