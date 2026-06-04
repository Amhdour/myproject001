from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.adapter import enforce_retrieval_acl_on_onyx_like_chunks
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.models import RetrievalACLDecision


RetrievalACLShadowMode = Literal["shadow", "enforce"]


@dataclass(frozen=True)
class RetrievalACLShadowDecisionEvidence:
    """Reviewer-safe runtime decision evidence for shadow-mode ACL proof."""

    request_id: str
    mode: RetrievalACLShadowMode
    acl_status: str
    observed_chunk_count: int
    would_return_chunk_count: int
    returned_chunk_count: int
    denied_count: int
    denied_document_ids: tuple[str, ...]
    denied_reasons: tuple[str, ...]
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_enforcement_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLShadowModeResult:
    """Result object for shadow/enforce wrapper proof.

    In `shadow` mode, `returned_chunks` preserves the original input chunks so this
    wrapper cannot silently change live behavior. In `enforce` mode, returned
    chunks are filtered according to the Step 21/23 ACL decision. This module is
    still isolated and not wired into live Onyx retrieval.
    """

    mode: RetrievalACLShadowMode
    decision: RetrievalACLDecision
    returned_chunks: tuple[OnyxLikeRetrievalChunk, ...]
    would_return_chunks: tuple[OnyxLikeRetrievalChunk, ...]
    evidence: RetrievalACLShadowDecisionEvidence


def evaluate_retrieval_acl_shadow_mode(
    *,
    context: RetrievalACLContext | object | None,
    chunks: tuple[OnyxLikeRetrievalChunk, ...] | list[OnyxLikeRetrievalChunk],
    request_id: str = "isolated-retrieval-acl-shadow-mode-proof",
    mode: RetrievalACLShadowMode = "shadow",
) -> RetrievalACLShadowModeResult:
    """Evaluate retrieval ACL decisions without requiring live Onyx wiring.

    Shadow mode observes what would be filtered while returning the original
    chunks unchanged. This is the safe bridge between isolated adapter proof and
    a future feature-flagged `search_pipeline` integration.
    """

    original_chunks = tuple(chunks)
    adapter_result = enforce_retrieval_acl_on_onyx_like_chunks(
        context=context,
        chunks=original_chunks,
        request_id=request_id,
    )
    would_return_chunks = adapter_result.allowed_original_chunks

    if mode == "shadow":
        returned_chunks = original_chunks
    elif mode == "enforce":
        returned_chunks = would_return_chunks
    else:
        raise ValueError(f"Unsupported retrieval ACL shadow mode: {mode}")

    evidence = _build_shadow_evidence(
        request_id=request_id,
        mode=mode,
        decision=adapter_result.decision,
        observed_chunk_count=len(original_chunks),
        would_return_chunk_count=len(would_return_chunks),
        returned_chunk_count=len(returned_chunks),
    )

    return RetrievalACLShadowModeResult(
        mode=mode,
        decision=adapter_result.decision,
        returned_chunks=returned_chunks,
        would_return_chunks=would_return_chunks,
        evidence=evidence,
    )


def _build_shadow_evidence(
    *,
    request_id: str,
    mode: RetrievalACLShadowMode,
    decision: RetrievalACLDecision,
    observed_chunk_count: int,
    would_return_chunk_count: int,
    returned_chunk_count: int,
) -> RetrievalACLShadowDecisionEvidence:
    return RetrievalACLShadowDecisionEvidence(
        request_id=request_id,
        mode=mode,
        acl_status=decision.status,
        observed_chunk_count=observed_chunk_count,
        would_return_chunk_count=would_return_chunk_count,
        returned_chunk_count=returned_chunk_count,
        denied_count=decision.denied_count,
        denied_document_ids=tuple(
            denial.document_id
            for denial in decision.denials
            if denial.document_id is not None
        ),
        denied_reasons=tuple(denial.reason.value for denial in decision.denials),
    )
