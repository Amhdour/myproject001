from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backend.security_layer.retrieval_acl.enforce_hook import (
    apply_retrieval_acl_enforcement_hook,
)


@dataclass
class RealisticInferenceChunk:
    document_id: str
    metadata: dict[str, Any]
    content: str = "chunk text must never appear in ACL decisions"


def test_real_path_enforce_allows_matching_tenant_metadata() -> None:
    chunk = RealisticInferenceChunk(
        document_id="doc-tenant-a-001",
        metadata={"tenant_id": "tenant-a"},
        content="PRIVATE SAME TENANT CONTENT",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == [chunk]
    assert result.returned_chunk_count == 1
    assert result.behavior_changed is False
    assert len(result.decisions) == 1
    assert result.decisions[0].allowed is True
    assert result.decisions[0].reason == "allowed"
    assert "PRIVATE SAME TENANT CONTENT" not in str(result.decisions[0])


def test_real_path_enforce_blocks_cross_tenant_mapped_metadata() -> None:
    unauthorized_chunk = RealisticInferenceChunk(
        document_id="doc-tenant-b-002",
        metadata={"tenant_id": "tenant-b"},
        content="PRIVATE TENANT B CONTENT",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[unauthorized_chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == []
    assert result.returned_chunk_count == 0
    assert result.behavior_changed is True
    assert len(result.decisions) == 1
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason in {
        "tenant_mismatch",
        "unauthorized_tenant",
    }
    assert "PRIVATE TENANT B CONTENT" not in str(result.decisions[0])


def test_real_path_enforce_fails_closed_when_chunk_tenant_metadata_missing() -> None:
    chunk_without_tenant = RealisticInferenceChunk(
        document_id="doc-without-tenant",
        metadata={},
        content="CONTENT WITHOUT TENANT METADATA",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk_without_tenant],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == []
    assert result.returned_chunk_count == 0
    assert result.behavior_changed is True
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason in {
        "missing_acl_metadata",
        "missing_chunk_tenant_id",
    }
    assert "CONTENT WITHOUT TENANT METADATA" not in str(result.decisions[0])


def test_real_path_enforce_fails_closed_when_user_tenant_missing() -> None:
    chunk = RealisticInferenceChunk(
        document_id="doc-tenant-a-003",
        metadata={"tenant_id": "tenant-a"},
        content="CONTENT WITH MISSING CALLER TENANT",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id=None,
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks == []
    assert result.returned_chunk_count == 0
    assert result.behavior_changed is True
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason in {
        "missing_acl_metadata",
        "missing_user_tenant_id",
    }
    assert "CONTENT WITH MISSING CALLER TENANT" not in str(result.decisions[0])


def test_real_path_off_mode_preserves_chunks_even_with_cross_tenant_metadata() -> None:
    chunk = RealisticInferenceChunk(
        document_id="doc-tenant-b-off",
        metadata={"tenant_id": "tenant-b"},
        content="OFF MODE CONTENT",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "off"},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks == [chunk]
    assert result.returned_chunk_count == 1
    assert result.behavior_changed is False
    assert "OFF MODE CONTENT" not in str(result.decisions)


def test_real_path_shadow_mode_preserves_chunks_but_records_denial_decision() -> None:
    chunk = RealisticInferenceChunk(
        document_id="doc-tenant-b-shadow",
        metadata={"tenant_id": "tenant-b"},
        content="SHADOW MODE CONTENT",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[chunk],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "shadow"},
    )

    assert result.config.mode == "shadow"
    assert result.returned_chunks == [chunk]
    assert result.returned_chunk_count == 1
    assert result.behavior_changed is False
    assert result.decisions[0].allowed is False
    assert result.decisions[0].reason in {
        "tenant_mismatch",
        "unauthorized_tenant",
    }
    assert "SHADOW MODE CONTENT" not in str(result.decisions[0])


def test_demo_attack_realistic_cross_tenant_metadata_is_blocked() -> None:
    attacker_tenant = "tenant-a"
    victim_chunk = RealisticInferenceChunk(
        document_id="customer-private-doc-tenant-b",
        metadata={
            "tenant_id": "tenant-b",
            "source": "realistic-retrieval-metadata",
        },
        content="CUSTOMER SECRET FROM TENANT B",
    )

    result = apply_retrieval_acl_enforcement_hook(
        chunks=[victim_chunk],
        user_tenant_id=attacker_tenant,
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    assert result.returned_chunks == []
    assert result.observed_chunk_count == 1
    assert result.returned_chunk_count == 0
    assert result.behavior_changed is True
    assert result.decisions[0].allowed is False
    assert result.decisions[0].production_readiness == "NO-GO"
    assert result.decisions[0].enterprise_readiness == "NO-GO"
    assert "CUSTOMER SECRET FROM TENANT B" not in str(result.decisions[0])
