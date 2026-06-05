from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from backend.security_layer.retrieval_acl.integration_config import RetrievalACLIntegrationConfig
from backend.security_layer.retrieval_acl.integration_config import get_retrieval_acl_integration_config


ChunkT = TypeVar("ChunkT")


@dataclass(frozen=True)
class RetrievalACLNoopSeamHookResult(Generic[ChunkT]):
    """Result for the Bundle J default-off no-op seam hook.

    The hook is intentionally behavior-preserving. It gives the real Onyx
    `search_pipeline` seam a narrow, testable call point without enabling live
    filtering, live blocking, or live enforcement.
    """

    config: RetrievalACLIntegrationConfig
    returned_chunks: list[ChunkT]
    observed_chunk_count: int
    returned_chunk_count: int
    behavior_changed: bool = False
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_filtering_claimed: bool = False
    live_blocking_claimed: bool = False
    live_enforcement_claimed: bool = False


def apply_retrieval_acl_search_pipeline_noop_hook(
    *,
    chunks: list[ChunkT],
    env: dict[str, str] | None = None,
    config: RetrievalACLIntegrationConfig | None = None,
) -> list[ChunkT]:
    """Return search-pipeline chunks unchanged.

    This is the first real-path no-op hook. It must preserve object identity and
    ordering in default-off mode. It intentionally does not call shadow or enforce
    logic yet.
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
    claim-bounded, but all modes return the original list unchanged in Bundle J.
    """

    resolved_config = config or get_retrieval_acl_integration_config(env=env)
    return RetrievalACLNoopSeamHookResult(
        config=resolved_config,
        returned_chunks=chunks,
        observed_chunk_count=len(chunks),
        returned_chunk_count=len(chunks),
    )
