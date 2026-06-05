from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass

import pytest

from backend.security_layer.retrieval_acl.enforce_hook import (
    apply_retrieval_acl_enforcement_hook,
)
from backend.security_layer.retrieval_acl.telemetry_counters import (
    clear_retrieval_acl_telemetry_counters,
)
from backend.security_layer.retrieval_acl.telemetry_counters import (
    get_retrieval_acl_telemetry_snapshot,
)


@dataclass
class FakeChunk:
    document_id: str | None
    tenant_id: str | None
    content: str = "secret chunk body must not enter telemetry counters"


@pytest.fixture(autouse=True)
def clear_counters() -> None:
    clear_retrieval_acl_telemetry_counters()


def test_allowed_enforce_decision_increments_allowed_count() -> None:
    apply_retrieval_acl_enforcement_hook(
        chunks=[FakeChunk(document_id="doc-a", tenant_id="tenant-a")],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    snapshot = get_retrieval_acl_telemetry_snapshot()

    assert snapshot.allowed_count == 1
    assert snapshot.denied_count == 0
    assert snapshot.fail_closed_count == 0


def test_cross_tenant_enforce_denial_increments_denied_count() -> None:
    apply_retrieval_acl_enforcement_hook(
        chunks=[FakeChunk(document_id="doc-b", tenant_id="tenant-b")],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    snapshot = get_retrieval_acl_telemetry_snapshot()

    assert snapshot.allowed_count == 0
    assert snapshot.denied_count == 1
    assert snapshot.fail_closed_count == 0


def test_missing_metadata_increments_fail_closed_count() -> None:
    apply_retrieval_acl_enforcement_hook(
        chunks=[FakeChunk(document_id=None, tenant_id="tenant-a")],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    snapshot = get_retrieval_acl_telemetry_snapshot()

    assert snapshot.allowed_count == 0
    assert snapshot.denied_count == 0
    assert snapshot.fail_closed_count == 1


def test_off_mode_does_not_increment_counters() -> None:
    apply_retrieval_acl_enforcement_hook(
        chunks=[
            FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
            FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
            FakeChunk(document_id=None, tenant_id="tenant-a"),
        ],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "off"},
    )

    snapshot = get_retrieval_acl_telemetry_snapshot()

    assert snapshot.allowed_count == 0
    assert snapshot.denied_count == 0
    assert snapshot.fail_closed_count == 0


def test_shadow_mode_does_not_increment_counters() -> None:
    apply_retrieval_acl_enforcement_hook(
        chunks=[
            FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
            FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
            FakeChunk(document_id=None, tenant_id="tenant-a"),
        ],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "shadow"},
    )

    snapshot = get_retrieval_acl_telemetry_snapshot()

    assert snapshot.allowed_count == 0
    assert snapshot.denied_count == 0
    assert snapshot.fail_closed_count == 0


def test_clear_resets_counters() -> None:
    apply_retrieval_acl_enforcement_hook(
        chunks=[
            FakeChunk(document_id="doc-a", tenant_id="tenant-a"),
            FakeChunk(document_id="doc-b", tenant_id="tenant-b"),
            FakeChunk(document_id=None, tenant_id="tenant-a"),
        ],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    before_clear = get_retrieval_acl_telemetry_snapshot()
    assert before_clear.allowed_count == 1
    assert before_clear.denied_count == 1
    assert before_clear.fail_closed_count == 1

    clear_retrieval_acl_telemetry_counters()
    after_clear = get_retrieval_acl_telemetry_snapshot()

    assert after_clear.allowed_count == 0
    assert after_clear.denied_count == 0
    assert after_clear.fail_closed_count == 0


def test_demo_attack_denial_increments_denied_count_without_chunk_content() -> None:
    demo_chunk_text = "PRIVATE TENANT B DATA AND PROMPT BAIT"

    apply_retrieval_acl_enforcement_hook(
        chunks=[
            FakeChunk(
                document_id="customer-private-doc-tenant-b",
                tenant_id="tenant-b",
                content=demo_chunk_text,
            )
        ],
        user_tenant_id="tenant-a",
        env={"ONYX_SECURITY_RETRIEVAL_ACL_MODE": "enforce"},
    )

    snapshot = get_retrieval_acl_telemetry_snapshot()
    serialized_snapshot = str(asdict(snapshot))

    assert snapshot.allowed_count == 0
    assert snapshot.denied_count == 1
    assert snapshot.fail_closed_count == 0
    assert demo_chunk_text not in serialized_snapshot
    assert "tenant-b" not in serialized_snapshot
    assert "customer-private-doc-tenant-b" not in serialized_snapshot


def test_snapshot_preserves_no_go_production_enterprise_boundaries() -> None:
    snapshot = get_retrieval_acl_telemetry_snapshot()

    assert snapshot.production_readiness == "NO-GO"
    assert snapshot.enterprise_readiness == "NO-GO"
    assert snapshot.storage_scope == "in_memory_only"
    assert "production_ready" not in asdict(snapshot)
    assert "enterprise_ready" not in asdict(snapshot)
