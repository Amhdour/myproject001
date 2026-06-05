from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.integration_config import RetrievalACLIntegrationConfig
from backend.security_layer.retrieval_acl.integration_config import get_retrieval_acl_integration_config
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.shadow_integration import RetrievalACLShadowIntegrationResult
from backend.security_layer.retrieval_acl.shadow_integration import apply_retrieval_acl_shadow_integration


SeamInstrumentationStatus = Literal[
    "observed_off_no_behavior_change",
    "observed_shadow_no_behavior_change",
    "observed_isolated_enforce_behavior",
]


@dataclass(frozen=True)
class RetrievalACLLiveAdjacentSeamObservation:
    """Observation record for a live-adjacent retrieval seam.

    This object records what a retrieval ACL wrapper would observe near a real
    retrieval seam while preserving strict claim boundaries. It is not wired into
    live Onyx `search_pipeline` behavior and does not claim live enforcement.
    """

    seam_name: str
    request_id: str
    mode: str
    observed_chunk_count: int
    returned_chunk_count: int
    observed_document_ids: tuple[str, ...]
    returned_document_ids: tuple[str, ...]
    behavior_changed: bool
    status: SeamInstrumentationStatus
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_integration_claimed: bool = False
    live_enforcement_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLLiveAdjacentSeamResult:
    """Result for Bundle H default-off live-adjacent seam instrumentation."""

    config: RetrievalACLIntegrationConfig
    observation: RetrievalACLLiveAdjacentSeamObservation
    integration_result: RetrievalACLShadowIntegrationResult

    @property
    def returned_chunks(self) -> tuple[OnyxLikeRetrievalChunk, ...]:
        return self.integration_result.returned_chunks


def observe_retrieval_acl_live_adjacent_seam(
    *,
    seam_name: str,
    context: RetrievalACLContext | object | None,
    retrieved_chunks: tuple[OnyxLikeRetrievalChunk, ...] | list[OnyxLikeRetrievalChunk],
    request_id: str = "bundle-h-live-adjacent-seam-observation-proof",
    config: RetrievalACLIntegrationConfig | None = None,
    env: dict[str, str] | None = None,
) -> RetrievalACLLiveAdjacentSeamResult:
    """Observe a live-adjacent retrieval seam with default-off behavior.

    This helper proves the seam can be observed and measured without requiring a
    live Onyx patch. `off` and `shadow` modes must preserve returned chunks. The
    explicit `enforce` mode remains isolated and must not be described as live
    production enforcement.
    """

    original_chunks = tuple(retrieved_chunks)
    resolved_config = config or get_retrieval_acl_integration_config(env=env)
    integration_result = apply_retrieval_acl_shadow_integration(
        context=context,
        retrieved_chunks=original_chunks,
        request_id=request_id,
        config=resolved_config,
    )
    returned_chunks = integration_result.returned_chunks
    behavior_changed = returned_chunks != original_chunks

    observation = RetrievalACLLiveAdjacentSeamObservation(
        seam_name=seam_name,
        request_id=request_id,
        mode=resolved_config.mode,
        observed_chunk_count=len(original_chunks),
        returned_chunk_count=len(returned_chunks),
        observed_document_ids=tuple(chunk.document_id for chunk in original_chunks),
        returned_document_ids=tuple(chunk.document_id for chunk in returned_chunks),
        behavior_changed=behavior_changed,
        status=_status_for_mode(
            mode=resolved_config.mode,
            behavior_changed=behavior_changed,
        ),
    )

    return RetrievalACLLiveAdjacentSeamResult(
        config=resolved_config,
        observation=observation,
        integration_result=integration_result,
    )


def _status_for_mode(
    *,
    mode: str,
    behavior_changed: bool,
) -> SeamInstrumentationStatus:
    if mode == "off":
        return "observed_off_no_behavior_change"
    if mode == "shadow":
        return "observed_shadow_no_behavior_change"
    if mode == "enforce" and behavior_changed:
        return "observed_isolated_enforce_behavior"
    if mode == "enforce":
        return "observed_isolated_enforce_behavior"
    return "observed_off_no_behavior_change"
