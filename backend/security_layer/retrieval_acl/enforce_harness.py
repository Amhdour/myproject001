from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.security_layer.retrieval_acl.adapter import OnyxLikeRetrievalChunk
from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.integration_config import RetrievalACLIntegrationConfig
from backend.security_layer.retrieval_acl.integration_config import get_retrieval_acl_integration_config
from backend.security_layer.retrieval_acl.models import RetrievalACLContext
from backend.security_layer.retrieval_acl.shadow_integration import RetrievalACLShadowIntegrationResult
from backend.security_layer.retrieval_acl.shadow_integration import apply_retrieval_acl_shadow_integration


RollbackVerificationStatus = Literal[
    "not_required",
    "rollback_to_off_available",
    "rollback_verified_off_preserves_chunks",
]


@dataclass(frozen=True)
class RetrievalACLEnforceRollbackPlan:
    """Reviewer-safe rollback plan for isolated enforce-mode proof.

    The plan is intentionally configuration-only: it proves how an operator would
    disable the isolated retrieval ACL integration by restoring the feature flag
    to `off`. It does not claim live Onyx rollback coverage.
    """

    feature_flag: str = INTEGRATION_MODE_ENV_VAR
    rollback_value: str = "off"
    rollback_command: str = f"export {INTEGRATION_MODE_ENV_VAR}=off"
    verification_command: str = (
        "PYTHONPATH=. python -m pytest "
        "backend/security_layer/tests/test_retrieval_acl_enforce_harness.py -q"
    )
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_rollback_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLEnforceHarnessResult:
    """Result for Bundle G isolated enforce-mode harness proof."""

    config: RetrievalACLIntegrationConfig
    integration_result: RetrievalACLShadowIntegrationResult
    rollback_plan: RetrievalACLEnforceRollbackPlan
    rollback_verification_status: RollbackVerificationStatus
    observed_document_ids: tuple[str, ...]
    returned_document_ids: tuple[str, ...]
    denied_document_ids: tuple[str, ...]
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_integration_claimed: bool = False


@dataclass(frozen=True)
class RetrievalACLRollbackVerificationResult:
    """Proof that rollback-to-off preserves retrieved chunks in isolation."""

    rollback_plan: RetrievalACLEnforceRollbackPlan
    before_rollback_result: RetrievalACLEnforceHarnessResult
    after_rollback_result: RetrievalACLShadowIntegrationResult
    rollback_verification_status: RollbackVerificationStatus
    chunks_preserved_after_rollback: bool
    production_readiness: str = "NO-GO"
    enterprise_readiness: str = "NO-GO"
    live_rollback_claimed: bool = False


def run_retrieval_acl_enforce_mode_harness(
    *,
    context: RetrievalACLContext | object | None,
    retrieved_chunks: tuple[OnyxLikeRetrievalChunk, ...] | list[OnyxLikeRetrievalChunk],
    request_id: str = "bundle-g-enforce-mode-harness-proof",
    config: RetrievalACLIntegrationConfig | None = None,
    env: dict[str, str] | None = None,
) -> RetrievalACLEnforceHarnessResult:
    """Run the isolated Bundle G retrieval ACL enforce-mode harness.

    The harness uses the Bundle F shadow integration wrapper and records the
    returned/denied document IDs plus the configuration-only rollback plan. It is
    intentionally unwired from live Onyx retrieval.
    """

    original_chunks = tuple(retrieved_chunks)
    resolved_config = config or get_retrieval_acl_integration_config(env=env)
    integration_result = apply_retrieval_acl_shadow_integration(
        context=context,
        retrieved_chunks=original_chunks,
        request_id=request_id,
        config=resolved_config,
    )
    rollback_plan = RetrievalACLEnforceRollbackPlan()
    denied_document_ids = _denied_document_ids(integration_result)

    return RetrievalACLEnforceHarnessResult(
        config=resolved_config,
        integration_result=integration_result,
        rollback_plan=rollback_plan,
        rollback_verification_status=(
            "rollback_to_off_available" if resolved_config.is_enforce else "not_required"
        ),
        observed_document_ids=tuple(chunk.document_id for chunk in original_chunks),
        returned_document_ids=integration_result.gate_result.downstream_document_ids,
        denied_document_ids=denied_document_ids,
    )


def verify_retrieval_acl_rollback_to_off(
    *,
    context: RetrievalACLContext | object | None,
    retrieved_chunks: tuple[OnyxLikeRetrievalChunk, ...] | list[OnyxLikeRetrievalChunk],
    request_id: str = "bundle-g-rollback-verification-proof",
    enforce_env: dict[str, str] | None = None,
) -> RetrievalACLRollbackVerificationResult:
    """Verify that restoring the feature flag to `off` preserves chunks.

    This is a local proof of rollback behavior for the isolated helper only. It
    does not prove live Onyx operational rollback.
    """

    original_chunks = tuple(retrieved_chunks)
    before_rollback = run_retrieval_acl_enforce_mode_harness(
        context=context,
        retrieved_chunks=original_chunks,
        request_id=f"{request_id}-before",
        env=enforce_env or {INTEGRATION_MODE_ENV_VAR: "enforce"},
    )
    after_rollback = apply_retrieval_acl_shadow_integration(
        context=context,
        retrieved_chunks=original_chunks,
        request_id=f"{request_id}-after",
        env={INTEGRATION_MODE_ENV_VAR: before_rollback.rollback_plan.rollback_value},
    )
    chunks_preserved = after_rollback.returned_chunks == original_chunks

    return RetrievalACLRollbackVerificationResult(
        rollback_plan=before_rollback.rollback_plan,
        before_rollback_result=before_rollback,
        after_rollback_result=after_rollback,
        rollback_verification_status=(
            "rollback_verified_off_preserves_chunks"
            if chunks_preserved
            else "rollback_to_off_available"
        ),
        chunks_preserved_after_rollback=chunks_preserved,
    )


def _denied_document_ids(
    integration_result: RetrievalACLShadowIntegrationResult,
) -> tuple[str, ...]:
    shadow_result = integration_result.gate_result.shadow_result
    if shadow_result is None:
        return ()
    return shadow_result.evidence.denied_document_ids
