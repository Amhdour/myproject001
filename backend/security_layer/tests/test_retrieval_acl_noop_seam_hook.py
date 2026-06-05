from __future__ import annotations

from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.noop_seam_hook import apply_retrieval_acl_search_pipeline_noop_hook
from backend.security_layer.retrieval_acl.noop_seam_hook import observe_retrieval_acl_search_pipeline_noop_hook


def test_noop_hook_returns_same_list_object_in_default_off_mode() -> None:
    chunks = [object(), object()]

    returned_chunks = apply_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={},
    )

    assert returned_chunks is chunks
    assert returned_chunks == chunks


def test_noop_hook_observation_preserves_default_off_claim_boundaries() -> None:
    chunks = [object(), object(), object()]

    result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks is chunks
    assert result.observed_chunk_count == 3
    assert result.returned_chunk_count == 3
    assert result.behavior_changed is False
    assert result.production_readiness == "NO-GO"
    assert result.enterprise_readiness == "NO-GO"
    assert result.live_filtering_claimed is False
    assert result.live_blocking_claimed is False
    assert result.live_enforcement_claimed is False


def test_noop_hook_does_not_filter_even_when_env_is_shadow_or_enforce() -> None:
    chunks = [object(), object()]

    shadow_result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )
    enforce_result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "enforce"},
    )

    assert shadow_result.config.mode == "shadow"
    assert shadow_result.returned_chunks is chunks
    assert shadow_result.behavior_changed is False
    assert enforce_result.config.mode == "enforce"
    assert enforce_result.returned_chunks is chunks
    assert enforce_result.behavior_changed is False


def test_noop_hook_invalid_env_fails_safe_to_off() -> None:
    chunks = [object()]

    result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "invalid"},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks is chunks
    assert result.behavior_changed is False
