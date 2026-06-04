from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.shadow_mode import RetrievalACLShadowModeResult
from backend.security_layer.retrieval_acl.shadow_mode import evaluate_retrieval_acl_shadow_mode


RetrievalACLGateMode = Literal["off", "shadow", "enforce"]


@dataclass(frozen=True)
class SearchPipelineGateResult:
    """Result for the isolated post-search_chunks gate proof.

    This module models the Step 22 integration point without importing or mutating
    live Onyx `search_pipeline`. It proves the behavior a feature-flagged guard
    should have around retrieved chunks before downstream recombination, UI
    emission, selection, or LLM context construction.
    """

    mode: RetrievalACLGateMode
    returned_chunks: tuple[OnyxLikeRetrievalChunk, ...]
    shadow_result: RetrievalACLShadowModeResult | None
    downstream_document_ids: tuple[str, ...]
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_integration_claimed: bool = False


def apply_retrieval_acl_search_pipeline_gate(
    *,
    context: RetrievalACLContext | object | None,
    retrieved_chunks: tuple[OnyxLikeRetrievalChunk, ...] | list[OnyxLikeRetrievalChunk],
    request_id: str = "isolated-search-pipeline-gate-proof",
    mode: RetrievalACLGateMode = "off",
) -> SearchPipelineGateResult:
    """Apply the isolated retrieval ACL gate at the post-search_chunks boundary.

    Modes:
    - `off`: returns retrieved chunks unchanged and records no ACL decision.
    - `shadow`: returns retrieved chunks unchanged, but records what ACL would filter.
    - `enforce`: returns only ACL-allowed chunks using the Step 21/23/Bundle A path.

    This proof is intentionally isolated. It does not modify live Onyx
    `search_pipeline` behavior and does not claim production retrieval security.
    """

    original_chunks = tuple(retrieved_chunks)

    if mode == "off":
        returned_chunks = original_chunks
        shadow_result = None
    elif mode == "shadow":
        shadow_result = evaluate_retrieval_acl_shadow_mode(
            context=context,
            chunks=original_chunks,
            request_id=request_id,
            mode="shadow",
        )
        returned_chunks = shadow_result.returned_chunks
    elif mode == "enforce":
        shadow_result = evaluate_retrieval_acl_shadow_mode(
            context=context,
            chunks=original_chunks,
            request_id=request_id,
            mode="enforce",
        )
        returned_chunks = shadow_result.returned_chunks
    else:
        raise ValueError(f"Unsupported retrieval ACL gate mode: {mode}")

    return SearchPipelineGateResult(
        mode=mode,
        returned_chunks=returned_chunks,
        shadow_result=shadow_result,
        downstream_document_ids=_simulate_downstream_document_ids(returned_chunks),
    )


def _simulate_downstream_document_ids(
    chunks: tuple[OnyxLikeRetrievalChunk, ...],
) -> tuple[str, ...]:
    """Simulate the document IDs visible to downstream UI/LLM surfaces."""

    return tuple(chunk.document_id for chunk in chunks)
