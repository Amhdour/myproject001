from __future__ import annotations

from pathlib import Path

import pytest

from backend.security_layer.retrieval.context_builder import build_candidates_from_metadata_list
from backend.security_layer.retrieval.integration_flags import (
    RetrievalIntegrationConfig,
    RetrievalIntegrationMode,
    default_retrieval_integration_config,
)
from backend.security_layer.retrieval.live_monitor_adapter import monitor_only_live_retrieval_check
from backend.security_layer.runtime.audit import clear_audit_events, get_audit_events
from backend.security_layer.runtime.metrics import clear_security_metrics, get_security_metrics


def _metadata() -> list[dict[str, object]]:
    return [
        {
            "candidate_id": "d1__1",
            "document_id": "d1",
            "chunk_id": "1",
            "tenant_id": "t1",
            "vector_namespace": "tenant:t1",
            "source_type": "hybrid",
            "provenance_id": "d1__1",
        },
        {
            "candidate_id": "d2__2",
            "document_id": "d2",
            "chunk_id": "2",
            "tenant_id": "t2",
            "vector_namespace": "tenant:t2",
            "source_type": "hybrid",
            "provenance_id": "d2__2",
        },
    ]


def test_disabled_mode_preserves_behavior_without_events() -> None:
    clear_audit_events(); clear_security_metrics()
    monitor_only_live_retrieval_check(RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.DISABLED), request_id="r-disabled", subject_id="u1", tenant_id="t1", retrieval_scope=("ds",), candidate_metadata=_metadata())
    assert get_audit_events() == []
    assert get_security_metrics() == []


def test_monitor_only_records_audit_and_metric_without_filtering() -> None:
    clear_audit_events(); clear_security_metrics()
    input_metadata = _metadata()
    monitor_only_live_retrieval_check(RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.MONITOR_ONLY), request_id="r-monitor", subject_id="u1", tenant_id="t1", retrieval_scope=("ds",), candidate_metadata=input_metadata)
    assert get_audit_events()
    assert get_security_metrics()
    assert [m["candidate_id"] for m in input_metadata] == ["d1__1", "d2__2"]


@pytest.mark.parametrize("forbidden_key", ["document_text", "chunk_text", "source_secret", "secret", "raw_text", "content"])
def test_safe_metadata_blocks_raw_text_and_secrets(forbidden_key: str) -> None:
    metadata = _metadata()
    metadata[0][forbidden_key] = "should-not-pass"
    with pytest.raises(ValueError):
        build_candidates_from_metadata_list(metadata)


def test_enforce_mode_is_disabled_by_default() -> None:
    assert default_retrieval_integration_config().mode == RetrievalIntegrationMode.DISABLED


def test_live_search_runner_path_is_monitor_only_and_fail_open() -> None:
    content = Path("backend/onyx/context/search/retrieval/search_runner.py").read_text()
    assert "return chunks" in content
    assert "except Exception" in content
    assert "monitor_only_live_retrieval_check" in content
    assert "apply_retrieval_acl_guard" in content
    assert "is_monitor_only(config)" in content


def test_live_patch_imports_are_isolated() -> None:
    content = Path("backend/onyx/context/search/retrieval/search_runner.py").read_text()
    assert "from backend.security_layer.retrieval.integration_flags import default_retrieval_integration_config" in content
    assert "from backend.security_layer.retrieval.integration_flags import is_monitor_only" in content
    assert "from backend.security_layer.retrieval.live_monitor_adapter import (" in content
