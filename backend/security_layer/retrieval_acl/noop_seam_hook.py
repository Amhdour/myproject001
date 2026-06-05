from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from backend.security_layer.retrieval_acl.integration_config import RetrievalACLIntegrationConfig
from backend.security_layer.retrieval_acl.integration_config import get_retrieval_acl_integration_config


ChunkT = TypeVar("ChunkT")


@dataclass(frozen=True)
class RetrievalACLNoopSeamHookResult(Generic[ChunkT]):
    """Result for the default-off real search-pipeline hook.

    The hook is intentionally behavior-preserving. It gives the real Onyx
    `search_pipeline` seam a narrow, testable call point without enabling live
    filtering, live blocking, or live enforcement.
    """

    config: RetrievalACLIntegrationConfig
    returned_chunks: list[ChunkT]
    observed_chunk_count: int
    returned_chunk_count: int
    behavior_changed: bool = False
    shadow_observation_recorded: bool = False
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_filtering_claimed: bool = False
    live_blocking_claimed: bool = False
    live_enforcement_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLRealPathShadowObservation:
    """Reviewer-safe observation emitted by the real search-pipeline hook.

    This observation records counts and mode only. It intentionally avoids
    recording document content or sensitive metadata and does not filter chunks.
    """

    mode: str
    observed_chunk_count: int
    returned_chunk_count: int
    behavior_changed: bool
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_filtering_claimed: bool = False
    live_blocking_claimed: bool = False
    live_enforcement_claimed: bool = False


_SHADOW_OBSERVATIONS: list[RetrievalACLRealPathShadowObservation] = []


def clear_retrieval_acl_real_path_shadow_observations() -> None:
    _SHADOW_OBSERVATIONS.clear()


def get_retrieval_acl_real_path_shadow_observations() -> tuple[
    RetrievalACLRealPathShadowObservation, ...
]:
    return tuple(_SHADOW_OBSERVATIONS)


def apply_retrieval_acl_search_pipeline_noop_hook(
    *,
    chunks: list[ChunkT],
    env: dict[str, str] | None = None,
    config: RetrievalACLIntegrationConfig | None = None,
) -> list[ChunkT]:
    """Return search-pipeline chunks unchanged.

    In Bundle L, `shadow` mode records a reviewer-safe observation while still
    returning the exact same chunk list. No filtering, blocking, or enforcement is
    performed.
    """

    return observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=chunks,
        env=env,
        config=config,
    ).returned_chunks


def observe_retrieval_acl_search_pipeline_noop_hook(
    *,
    chunks: list[ChunkT],
    env: dict[str, str] | None = None,
    config: RetrievalACLIntegrationConfig | None = None,
) -> RetrievalACLNoopSeamHookResult[ChunkT]:
    """Observe the no-op hook while preserving behavior.

    The config is read so tests can prove the hook remains default-off and
    claim-bounded. Shadow mode records an observation, but all modes return the
    original list unchanged in Bundle L.
    """

    resolved_config = config or get_retrieval_acl_integration_config(env=env)
    shadow_observation_recorded = resolved_config.is_shadow
    if shadow_observation_recorded:
        _SHADOW_OBSERVATIONS.append(
            RetrievalACLRealPathShadowObservation(
                mode=resolved_config.mode,
                observed_chunk_count=len(chunks),
                returned_chunk_count=len(chunks),
                behavior_changed=False,
            )
        )

    return RetrievalACLNoopSeamHookResult(
        config=resolved_config,
        returned_chunks=chunks,
        observed_chunk_count=len(chunks),
        returned_chunk_count=len(chunks),
        shadow_observation_recorded=shadow_observation_recorded,
    )
