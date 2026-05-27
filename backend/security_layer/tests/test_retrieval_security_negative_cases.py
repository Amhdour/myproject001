from __future__ import annotations

from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig, RetrievalIntegrationMode
from backend.security_layer.retrieval.live_monitor_adapter import monitor_only_live_retrieval_check
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.findings import clear_findings, get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics
from backend.security_layer.tests.retrieval_security_fixtures import build_retrieval_security_fixtures


def _run_monitor_only(candidate_metadata: list[dict[str, object]]) -> list[dict[str, object]]:
    clear_audit_events()
    clear_findings()
    clear_security_metrics()
    monitor_only_live_retrieval_check(
        RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.MONITOR_ONLY),
        request_id="fake_request_negative_cases",
        subject_id="fake_user_allowed",
        tenant_id="fake_tenant_alpha",
        retrieval_scope=("synthetic_scope",),
        candidate_metadata=candidate_metadata,
    )
    return candidate_metadata


def _assert_monitor_only_non_blocking(before: list[dict[str, object]], after: list[dict[str, object]]) -> None:
    assert len(after) == len(before)
    assert [item["candidate_id"] for item in after] == [item["candidate_id"] for item in before]
    assert all(item.get("blocked") is not True for item in after)
    assert all(item.get("denied") is not True for item in after)
    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()


def test_cross_tenant_document_candidate_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_cross_tenant_doc_candidate", "document_id": f["document_cross_tenant"]["id"], "chunk_id": f["chunk_allowed"]["id"], "tenant_id": f["tenant_b"]["id"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_cross_tenant_chunk_candidate_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_cross_tenant_chunk_candidate", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_cross_tenant"]["id"], "tenant_id": f["tenant_b"]["id"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_unauthorized_group_candidate_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_group_denied_candidate", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_denied_group"]["id"], "tenant_id": f["tenant_a"]["id"], "group_id": f["group_denied"]["id"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_unauthorized_role_candidate_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_role_denied_candidate", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_denied_role"]["id"], "tenant_id": f["tenant_a"]["id"], "role_id": f["role_denied"]["id"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_stale_acl_snapshot_candidate_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_stale_acl_candidate", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_allowed"]["id"], "tenant_id": f["tenant_a"]["id"], "acl_snapshot_id": f["stale_acl_snapshot"]["id"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_deleted_document_candidate_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_deleted_document_candidate", "document_id": f["document_deleted"]["id"], "chunk_id": f["chunk_allowed"]["id"], "tenant_id": f["tenant_a"]["id"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_vector_namespace_mismatch_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_vector_ns_denied_candidate", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_allowed"]["id"], "tenant_id": f["tenant_a"]["id"], "vector_namespace": f["vector_namespace_denied"]["namespace"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_vector_metadata_mismatch_detected_monitor_only() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_vector_metadata_denied_candidate", "document_id": f["document_allowed"]["id"], "chunk_id": f["chunk_allowed"]["id"], "tenant_id": f["vector_metadata_denied"]["tenant_id"], "security_scope": f["vector_metadata_denied"]["security_scope"]}]
    before = [m.copy() for m in candidate_metadata]
    _assert_monitor_only_non_blocking(before, _run_monitor_only(candidate_metadata))


def test_cache_cross_tenant_fixture_detected_isolated() -> None:
    f = build_retrieval_security_fixtures()
    cache_entry = f["cache_entry_cross_tenant"]
    assert cache_entry["synthetic_cross_tenant"] is True
    assert cache_entry["tenant_id"] == f["tenant_b"]["id"]


def test_citation_denied_fixture_detected_isolated() -> None:
    f = build_retrieval_security_fixtures()
    assert f["citation_denied"]["unauthorized"] is True
    assert f["citation_denied"]["document_id"] == f["document_cross_tenant"]["id"]


def test_rerank_denied_fixture_detected_isolated() -> None:
    f = build_retrieval_security_fixtures()
    assert f["rerank_candidate_denied"]["unauthorized"] is True
    assert f["rerank_candidate_denied"]["candidate_id"] == "fake_doc_cross_tenant__fake_chunk_cross_tenant"


def test_negative_decisions_do_not_include_raw_text_or_secrets() -> None:
    f = build_retrieval_security_fixtures()
    candidate_metadata = [{"candidate_id": "fake_non_leakage_candidate", "document_id": f["document_cross_tenant"]["id"], "chunk_id": f["chunk_cross_tenant"]["id"], "tenant_id": f["tenant_b"]["id"]}]
    after = _run_monitor_only(candidate_metadata)
    forbidden = {"document_text", "chunk_text", "source_secret", "api_key", "token", "password"}
    assert all(not forbidden.intersection(set(item.keys())) for item in after)
    assert all(not any(str(value).lower().startswith("sk-") for value in item.values()) for item in after)
