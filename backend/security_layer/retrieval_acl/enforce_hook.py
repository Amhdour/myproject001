from __future__ import annotations

from dataclasses import dataclass
from typing import Generic
from typing import TypeVar

from backend.security_layer.retrieval_acl.integration_config import (
    get_retrieval_acl_integration_config,
)
from backend.security_layer.retrieval_acl.integration_config import (
    RetrievalACLIntegrationConfig,
)
from backend.security_layer.retrieval_acl.metadata_adapter import (
    extract_retrieval_acl_metadata,
)
from backend.security_layer.retrieval_acl.noop_seam_hook import (
    apply_retrieval_acl_search_pipeline_noop_hook,
)
from backend.security_layer.retrieval_acl.telemetry_counters import (
    record_retrieval_acl_telemetry_decision,
)

ChunkT = TypeVar("ChunkT")


@dataclass(frozen=True)
class RetrievalACLDecision:
    allowed: bool
    reason: str
    mode: str
    user_tenant_id: str
    chunk_tenant_id: str
    document_ref: str
    metadata_present: bool
    metadata_reason: str | None = None
    policy_version: str = "retrieval-acl-v1"
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"


@dataclass(frozen=True)
class RetrievalACLEnforcementResult(Generic[ChunkT]):
    config: RetrievalACLIntegrationConfig
    returned_chunks: list[ChunkT]
    decisions: tuple[RetrievalACLDecision, ...]
    observed_chunk_count: int
    returned_chunk_count: int
    behavior_changed: bool
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"


def evaluate_retrieval_acl_chunk(
    *,
    chunk: ChunkT,
    user_tenant_id: str | None,
    mode: str,
) -> RetrievalACLDecision:
    metadata = extract_retrieval_acl_metadata(
        chunk=chunk,
        user_tenant_id=user_tenant_id,
    )

    if not metadata.metadata_present:
        return RetrievalACLDecision(
            allowed=False,
            reason="missing_acl_metadata",
            mode=mode,
            user_tenant_id=metadata.user_tenant_id or "missing",
            chunk_tenant_id=metadata.chunk_tenant_id or "missing",
            document_ref=metadata.document_ref,
            metadata_present=False,
            metadata_reason=metadata.reason,
        )

    if metadata.chunk_tenant_id != metadata.user_tenant_id:
        return RetrievalACLDecision(
            allowed=False,
            reason="tenant_mismatch",
            mode=mode,
            user_tenant_id=metadata.user_tenant_id,
            chunk_tenant_id=metadata.chunk_tenant_id,
            document_ref=metadata.document_ref,
            metadata_present=True,
        )

    return RetrievalACLDecision(
        allowed=True,
        reason="allowed",
        mode=mode,
        user_tenant_id=metadata.user_tenant_id,
        chunk_tenant_id=metadata.chunk_tenant_id,
        document_ref=metadata.document_ref,
        metadata_present=True,
    )


def apply_retrieval_acl_enforcement_hook(
    *,
    chunks: list[ChunkT],
    user_tenant_id: str | None,
    env: dict[str, str] | None = None,
    config: RetrievalACLIntegrationConfig | None = None,
) -> RetrievalACLEnforcementResult[ChunkT]:
    resolved_config = config or get_retrieval_acl_integration_config(env=env)

    if resolved_config.is_off or resolved_config.is_shadow:
        return RetrievalACLEnforcementResult(
            config=resolved_config,
            returned_chunks=chunks,
            decisions=tuple(
                evaluate_retrieval_acl_chunk(
                    chunk=chunk,
                    user_tenant_id=user_tenant_id,
                    mode=resolved_config.mode,
                )
                for chunk in chunks
            ),
            observed_chunk_count=len(chunks),
            returned_chunk_count=len(chunks),
            behavior_changed=False,
        )

    returned_chunks: list[ChunkT] = []
    decisions: list[RetrievalACLDecision] = []

    for chunk in chunks:
        decision = evaluate_retrieval_acl_chunk(
            chunk=chunk,
            user_tenant_id=user_tenant_id,
            mode=resolved_config.mode,
        )
        decisions.append(decision)
        record_retrieval_acl_telemetry_decision(
            allowed=decision.allowed,
            reason=decision.reason,
        )

        if decision.allowed:
            returned_chunks.append(chunk)

    return RetrievalACLEnforcementResult(
        config=resolved_config,
        returned_chunks=returned_chunks,
        decisions=tuple(decisions),
        observed_chunk_count=len(chunks),
        returned_chunk_count=len(returned_chunks),
        behavior_changed=len(returned_chunks) != len(chunks),
    )


def apply_retrieval_acl_real_path_enforcement_hook(
    *,
    chunks: list[ChunkT],
    user_tenant_id: str | None,
    env: dict[str, str] | None = None,
    config: RetrievalACLIntegrationConfig | None = None,
) -> list[ChunkT]:
    """Apply the real search-pipeline ACL hook at the post-censoring seam.

    Off and shadow modes deliberately delegate to the existing no-op seam hook so
    prior behavior and reviewer-safe shadow observations are preserved. Enforce
    mode delegates to Retrieval ACL Enforcement v1 and returns only allowed
    chunks. Missing tenant/document metadata remains fail-closed inside the
    enforcement helper.
    """

    resolved_config = config or get_retrieval_acl_integration_config(env=env)

    if not resolved_config.is_enforce:
        return apply_retrieval_acl_search_pipeline_noop_hook(
            chunks=chunks,
            env=env,
            config=resolved_config,
        )

    return apply_retrieval_acl_enforcement_hook(
        chunks=chunks,
        user_tenant_id=user_tenant_id,
        config=resolved_config,
    ).returned_chunks
