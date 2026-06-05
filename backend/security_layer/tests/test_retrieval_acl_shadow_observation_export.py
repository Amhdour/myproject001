from __future__ import annotations

from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.noop_seam_hook import clear_retrieval_acl_real_path_shadow_observations
from backend.security_layer.retrieval_acl.noop_seam_hook import observe_retrieval_acl_search_pipeline_noop_hook
from backend.security_layer.retrieval_acl.shadow_observation_export import export_retrieval_acl_shadow_observation_evidence
from backend.security_layer.retrieval_acl.shadow_observation_export import export_retrieval_acl_shadow_observation_evidence_dicts


def setup_function() -> None:
    clear_retrieval_acl_real_path_shadow_observations()


def test_shadow_observation_export_is_redacted_and_claim_bounded() -> None:
    chunks = [object(), object(), object()]
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    records = export_retrieval_acl_shadow_observation_evidence(
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(records) == 1
    record = records[0]
    assert record.event_type == "retrieval_acl.real_path_shadow_observation"
    assert record.observed_at_utc == "2026-06-05T00:00:00+00:00"
    assert record.mode == "shadow"
    assert record.observed_chunk_count == 3
    assert record.returned_chunk_count == 3
    assert record.behavior_changed is False
    assert record.redacted is True
    assert record.contains_document_content is False
    assert record.contains_document_ids is False
    assert record.contains_user_prompt is False
    assert record.production_readiness == "NO-GO"
    assert record.enterprise_readiness == "NO-GO"
    assert record.live_filtering_claimed is False
    assert record.live_blocking_claimed is False
    assert record.live_enforcement_claimed is False


def test_shadow_observation_export_dicts_contain_no_sensitive_fields() -> None:
    chunks = [object()]
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    records = export_retrieval_acl_shadow_observation_evidence_dicts(
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(records) == 1
    record = records[0]
    forbidden_keys = {
        "document_id",
        "document_ids",
        "chunk_text",
        "content",
        "metadata",
        "user_prompt",
        "secret",
        "pii",
    }
    assert forbidden_keys.isdisjoint(record.keys())
    assert record["redacted"] is True
    assert record["contains_document_content"] is False
    assert record["contains_document_ids"] is False
    assert record["contains_user_prompt"] is False


def test_shadow_observation_export_empty_when_no_shadow_observation_exists() -> None:
    records = export_retrieval_acl_shadow_observation_evidence(
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert records == ()


def test_off_mode_produces_no_exported_shadow_observation() -> None:
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=[object()],
        env={INTEGRATION_MODE_ENV_VAR: "off"},
    )

    records = export_retrieval_acl_shadow_observation_evidence(
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert records == ()
