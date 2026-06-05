from __future__ import annotations

from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.noop_seam_hook import clear_retrieval_acl_real_path_shadow_observations
from backend.security_layer.retrieval_acl.noop_seam_hook import observe_retrieval_acl_search_pipeline_noop_hook
from backend.security_layer.retrieval_acl.shadow_observation_audit import build_retrieval_acl_shadow_observation_audit_dicts
from backend.security_layer.retrieval_acl.shadow_observation_audit import build_retrieval_acl_shadow_observation_audit_events


def setup_function() -> None:
    clear_retrieval_acl_real_path_shadow_observations()


def test_shadow_observation_audit_event_is_redacted_and_correlation_friendly() -> None:
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=[object(), object()],
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    events = build_retrieval_acl_shadow_observation_audit_events(
        request_id="request-123",
        pipeline_stage="search_pipeline.post_censoring.return_hook",
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(events) == 1
    event = events[0]
    assert event.event_type == "retrieval_acl.shadow_observation.audit"
    assert event.request_id == "request-123"
    assert event.pipeline_stage == "search_pipeline.post_censoring.return_hook"
    assert event.mode == "shadow"
    assert event.observed_chunk_count == 2
    assert event.returned_chunk_count == 2
    assert event.behavior_changed is False
    assert event.redacted is True
    assert event.contains_document_content is False
    assert event.contains_document_ids is False
    assert event.contains_user_prompt is False
    assert event.production_readiness == "NO-GO"
    assert event.enterprise_readiness == "NO-GO"
    assert event.live_filtering_claimed is False
    assert event.live_blocking_claimed is False
    assert event.live_enforcement_claimed is False


def test_shadow_observation_audit_dicts_contain_no_sensitive_fields() -> None:
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=[object()],
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    events = build_retrieval_acl_shadow_observation_audit_dicts(
        request_id="request-abc",
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(events) == 1
    event = events[0]
    forbidden_keys = {
        "document_id",
        "document_ids",
        "chunk_text",
        "content",
        "metadata",
        "user_prompt",
        "secret",
        "credential",
        "pii",
    }
    assert forbidden_keys.isdisjoint(event.keys())
    assert event["request_id"] == "request-abc"
    assert event["redacted"] is True
    assert event["contains_document_content"] is False
    assert event["contains_document_ids"] is False
    assert event["contains_user_prompt"] is False


def test_shadow_observation_audit_empty_when_no_shadow_observation_exists() -> None:
    events = build_retrieval_acl_shadow_observation_audit_events(
        request_id="request-empty",
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert events == ()


def test_off_mode_produces_no_shadow_audit_event() -> None:
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=[object()],
        env={INTEGRATION_MODE_ENV_VAR: "off"},
    )

    events = build_retrieval_acl_shadow_observation_audit_events(
        request_id="request-off",
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert events == ()
