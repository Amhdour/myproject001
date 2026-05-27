from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig, RetrievalIntegrationMode
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
    monitor_only_live_retrieval_check(
        RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.DISABLED),
        request_id="r-disabled",
        subject_id="u1",
        tenant_id="t1",
        retrieval_scope=("ds",),
        candidate_metadata=_metadata(),
    )
    assert get_audit_events() == []
    assert get_security_metrics() == []


def test_monitor_only_records_audit_and_metric_without_filtering() -> None:
    clear_audit_events(); clear_security_metrics()
    monitor_only_live_retrieval_check(
        RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.MONITOR_ONLY),
        request_id="r-monitor",
        subject_id="u1",
        tenant_id="t1",
        retrieval_scope=("ds",),
        candidate_metadata=_metadata(),
    )
    assert get_audit_events()
    assert get_security_metrics()


def test_monitor_only_no_raw_text_or_secret_in_context_metadata() -> None:
    clear_audit_events(); clear_security_metrics()
    monitor_only_live_retrieval_check(
        RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.MONITOR_ONLY),
        request_id="r-safe",
        subject_id="u1",
        tenant_id="t1",
        retrieval_scope=("ds",),
        candidate_metadata=_metadata(),
    )
    events = get_audit_events()
    assert events[-1].request_id == "r-safe"
