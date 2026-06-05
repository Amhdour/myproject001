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


def test_real_path_off_mode_still_returns_same_chunks() -> None:
    from backend.security_layer.retrieval_acl.enforce_hook import (
        apply_retrieval_acl_real_path_enforcement_hook,
    )

    chunks = [
        FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
        FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
    ]

    returned = apply_retrieval_acl_real_path_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "off"},
    )

    assert returned is chunks


def test_real_path_shadow_mode_still_returns_same_chunks() -> None:
    from backend.security_layer.retrieval_acl.enforce_hook import (
        apply_retrieval_acl_real_path_enforcement_hook,
    )
    from backend.security_layer.retrieval_acl.noop_seam_hook import (
        clear_retrieval_acl_real_path_shadow_observations,
    )
    from backend.security_layer.retrieval_acl.noop_seam_hook import (
        get_retrieval_acl_real_path_shadow_observations,
    )

    clear_retrieval_acl_real_path_shadow_observations()
    chunks = [
        FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
        FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
    ]

    returned = apply_retrieval_acl_real_path_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "shadow"},
    )

    assert returned is chunks
    observations = get_retrieval_acl_real_path_shadow_observations()
    assert len(observations) == 1
    assert observations[0].observed_chunk_count == 2
    assert observations[0].returned_chunk_count == 2
    assert observations[0].behavior_changed is False


def test_real_path_enforce_mode_uses_enforcement_hook_when_metadata_available() -> None:
    from backend.security_layer.retrieval_acl.enforce_hook import (
        apply_retrieval_acl_real_path_enforcement_hook,
    )

    allowed_chunk = FakeChunk(document_id="doc-a", tenant_id="tenant-a")
    denied_chunk = FakeChunk(document_id="doc-b", tenant_id="tenant-b")
    chunks = [allowed_chunk, denied_chunk]

    returned = apply_retrieval_acl_real_path_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert returned == [allowed_chunk]


def test_real_path_enforce_mode_fails_closed_when_required_metadata_missing() -> None:
    from backend.security_layer.retrieval_acl.enforce_hook import (
        apply_retrieval_acl_real_path_enforcement_hook,
    )

    chunks = [
        FakeChunk(document_id=None, tenant_id="tenant-a"),
        FakeChunk(document_id="doc-b", tenant_id=None),
    ]

    returned = apply_retrieval_acl_real_path_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert returned == []


def test_real_path_does_not_claim_production_or_enterprise_readiness() -> None:
    result = apply_retrieval_acl_enforcement_hook(
        chunks=[FakeChunk(document_id="doc-a", tenant_id="tenant-a")],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.production_readiness == "NO-GO"
    assert result.enterprise_readiness == "NO-GO"
    assert result.decisions[0].production_readiness == "NO-GO"
    assert result.decisions[0].enterprise_readiness == "NO-GO"


@dataclass
class RealisticInferenceChunkLike:
    document_id: str | None
    metadata: dict[str, str | list[str]]
    content: str = "secret chunk body must not enter decision records"
    blurb: str = "secret chunk blurb must not enter decision records"
    chunk_context: str = "secret chunk context must not enter decision records"


def test_metadata_adapter_extracts_document_id_from_realistic_chunk() -> None:
    from backend.security_layer.retrieval_acl.metadata_adapter import (
        extract_retrieval_acl_metadata,
    )

    metadata = extract_retrieval_acl_metadata(
        chunk=RealisticInferenceChunkLike(
            document_id="customer-private-document-12345",
            metadata={"tenant_id": "tenant-a"},
        ),
        user_tenant_id="tenant-a",
    )

    assert metadata.document_ref == "redacted:cust...2345"
    assert metadata.metadata_present is True


def test_metadata_adapter_extracts_tenant_id_when_available() -> None:
    from backend.security_layer.retrieval_acl.metadata_adapter import (
        extract_retrieval_acl_metadata,
    )

    metadata = extract_retrieval_acl_metadata(
        chunk=RealisticInferenceChunkLike(
            document_id="doc-a",
            metadata={"tenant_id": "tenant-a"},
        ),
        user_tenant_id="tenant-a",
    )

    assert metadata.chunk_tenant_id == "tenant-a"
    assert metadata.user_tenant_id == "tenant-a"
    assert metadata.reason is None


def test_metadata_adapter_marks_missing_tenant_metadata() -> None:
    from backend.security_layer.retrieval_acl.metadata_adapter import (
        extract_retrieval_acl_metadata,
    )

    metadata = extract_retrieval_acl_metadata(
        chunk=RealisticInferenceChunkLike(
            document_id="doc-a",
            metadata={},
        ),
        user_tenant_id="tenant-a",
    )

    assert metadata.metadata_present is False
    assert metadata.reason == "missing_chunk_tenant_id"
    assert metadata.document_ref == "redacted"


def test_enforce_mode_fails_closed_for_realistic_chunk_without_tenant_metadata() -> None:
    chunks = [
        RealisticInferenceChunkLike(
            document_id="doc-a",
            metadata={},
        )
    ]

    result = apply_retrieval_acl_enforcement_hook(
        chunks=chunks,
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.returned_chunks == []
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason == "missing_acl_metadata"
    assert result.decisions[0].metadata_present is False
    assert result.decisions[0].metadata_reason == "missing_chunk_tenant_id"


def test_enforce_mode_allows_realistic_chunk_with_matching_tenant_metadata() -> None:
    chunk = RealisticInferenceChunkLike(
        document_id="doc-a",
        metadata={"tenant_id": "tenant-a"},
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.returned_chunks == [chunk]
    assert result.decisions[0].allowed is True
    assert result.decisions[0].reason == "allowed"
    assert result.decisions[0].metadata_present is True


def test_enforce_mode_denies_realistic_chunk_with_cross_tenant_metadata() -> None:
    chunk = RealisticInferenceChunkLike(
        document_id="doc-b",
        metadata={"tenant_id": "tenant-b"},
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.returned_chunks == []
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason == "tenant_mismatch"
    assert result.decisions[0].metadata_present is True


def test_decision_records_do_not_include_chunk_text() -> None:
    secret_text = "secret chunk body must not enter decision records"
    chunk = RealisticInferenceChunkLike(
        document_id="customer-private-document-12345",
        metadata={"tenant_id": "tenant-b"},
        content=secret_text,
        blurb="secret chunk blurb must not enter decision records",
        chunk_context="secret chunk context must not enter decision records",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    decision_text = str(result.decisions[0])
    assert secret_text not in decision_text
    assert "secret chunk blurb" not in decision_text
    assert "secret chunk context" not in decision_text
    assert "customer-private-document-12345" not in decision_text
    assert result.decisions[0].document_ref == "redacted:cust...2345"
