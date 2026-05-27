from __future__ import annotations

from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig, RetrievalIntegrationMode
from backend.security_layer.retrieval.live_monitor_adapter import monitor_only_live_retrieval_check
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.tests.retrieval_security_fixtures import build_retrieval_security_fixtures


def _candidate_metadata() -> list[dict[str, object]]:
    f = build_retrieval_security_fixtures()
    return [
        {"candidate_id": "fake_allowed__1", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_allowed"]["id"], "tenant_id": f["tenant_a"]["id"], "vector_namespace": f["vector_namespace_allowed"]["namespace"], "source_type": "hybrid", "provenance_id": "fake_allowed__1"},
        {"candidate_id": "fake_cross_tenant__1", "document_id": f["document_cross_tenant"]["id"], "chunk_id": f["chunk_cross_tenant"]["id"], "tenant_id": f["tenant_b"]["id"], "vector_namespace": f["vector_namespace_denied"]["namespace"], "source_type": "hybrid", "provenance_id": "fake_cross_tenant__1"},
    ]


def test_monitor_only_skeleton_behaviors() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    metadata = _candidate_metadata()
    before = [m.copy() for m in metadata]
    monitor_only_live_retrieval_check(
        RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.MONITOR_ONLY),
        request_id="fake_request_monitor_only",
        subject_id="fake_user_allowed",
        tenant_id="fake_tenant_alpha",
        retrieval_scope=("synthetic_scope",),
        candidate_metadata=metadata,
    )

    assert len(metadata) == len(before)
    assert [m["candidate_id"] for m in metadata] == [m["candidate_id"] for m in before]
    assert any(m["tenant_id"] == "fake_tenant_beta" for m in metadata)
    assert all(m.get("blocked") is not True for m in metadata)
    assert all(m.get("denied") is not True for m in metadata)
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()

    forbidden_keys = {"document_text", "chunk_text", "source_secret"}
    assert all(not forbidden_keys.intersection(m.keys()) for m in metadata)
