from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.integration_config import RetrievalACLIntegrationConfig
from backend.security_layer.retrieval_acl.integration_config import get_retrieval_acl_integration_config
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.search_pipeline_gate import SearchPipelineGateResult
from backend.security_layer.retrieval_acl.search_pipeline_gate import apply_retrieval_acl_search_pipeline_gate


@dataclass(frozen=True)
class RetrievalACLShadowIntegrationResult:
    config: RetrievalACLIntegrationConfig
    gate_result: SearchPipelineGateResult

    @property
    def returned_chunks(self) -> tuple[OnyxLikeRetrievalChunk, ...]:
        return self.gate_result.returned_chunks


def apply_retrieval_acl_shadow_integration(
    *,
    context: RetrievalACLContext | object | None,
    retrieved_chunks: tuple[OnyxLikeRetrievalChunk, ...] | list[OnyxLikeRetrievalChunk],
    request_id: str = "phase-3-shadow-integration-proof",
    config: RetrievalACLIntegrationConfig | None = None,
    env: dict[str, str] | None = None,
) -> RetrievalACLShadowIntegrationResult:
    """Apply config-driven retrieval ACL gate behavior in an isolated helper."""

    resolved_config = config or get_retrieval_acl_integration_config(env=env)
    gate_result = apply_retrieval_acl_search_pipeline_gate(
        context=context,
        retrieved_chunks=retrieved_chunks,
        request_id=request_id,
        mode=resolved_config.mode,
    )
    return RetrievalACLShadowIntegrationResult(
        config=resolved_config,
        gate_result=gate_result,
    )
