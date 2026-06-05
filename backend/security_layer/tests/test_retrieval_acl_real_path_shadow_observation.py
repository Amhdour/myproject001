from __future__ import annotations

from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.noop_seam_hook import apply_retrieval_acl_search_pipeline_noop_hook
from backend.security_layer.retrieval_acl.noop_seam_hook import clear_retrieval_acl_real_path_shadow_observations
from backend.security_layer.retrieval_acl.noop_seam_hook import get_retrieval_acl_real_path_shadow_observations
from backend.security_layer.retrieval_acl.noop_seam_hook import observe_retrieval_acl_search_pipeline_noop_hook


def setup_function() -> None:
    clear_retrieval_acl_real_path_shadow_observations()


def test_real_path_shadow_records_observation_without_changing_chunks() -> None:
    chunks = [object(), object(), object()]

    result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    observations = get_retrieval_acl_real_path_shadow_observations()
    assert result.config.mode == "shadow"
    assert result.returned_chunks is chunks
    assert result.behavior_changed is False
    assert result.shadow_observation_recorded is True
    assert len(observations) == 1
    assert observations[0].mode == "shadow"
    assert observations[0].observed_chunk_count == 3
    assert observations[0].returned_chunk_count == 3
    assert observations[0].behavior_changed is False
    assert observations[0].live_filtering_claimed is False
    assert observations[0].live_blocking_claimed is False
    assert observations[0].live_enforcement_claimed is False


def test_real_path_off_mode_records_no_shadow_observation() -> None:
    chunks = [object(), object()]

    result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "off"},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks is chunks
    assert result.shadow_observation_recorded is False
    assert get_retrieval_acl_real_path_shadow_observations() == ()


def test_real_path_invalid_env_fails_safe_to_off_and_records_no_observation() -> None:
    chunks = [object()]

    result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "invalid"},
    )

    assert result.config.mode == "off"
    assert result.returned_chunks is chunks
    assert result.shadow_observation_recorded is False
    assert get_retrieval_acl_real_path_shadow_observations() == ()


def test_real_path_apply_hook_shadow_mode_still_returns_same_list() -> None:
    chunks = [object(), object()]

    returned = apply_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )

    assert returned is chunks
    observations = get_retrieval_acl_real_path_shadow_observations()
    assert len(observations) == 1
    assert observations[0].observed_chunk_count == 2
    assert observations[0].returned_chunk_count == 2


def test_real_path_enforce_mode_is_still_noop_in_bundle_l() -> None:
    chunks = [object(), object()]

    result = observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env={INTEGRATION_MODE_ENV_VAR: "enforce"},
    )

    assert result.config.mode == "enforce"
    assert result.returned_chunks is chunks
    assert result.behavior_changed is False
    assert result.shadow_observation_recorded is False
    assert result.live_enforcement_claimed is False
    assert get_retrieval_acl_real_path_shadow_observations() == ()
