from __future__ import annotations

from backend.security_layer.retrieval.context_builder import RetrievalContextBuildInput
from backend.security_layer.retrieval.context_builder import build_candidates_from_metadata_list
from backend.security_layer.retrieval.context_builder import build_retrieval_acl_context
from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig
from backend.security_layer.retrieval.integration_flags import is_monitor_only
from backend.security_layer.retrieval.integration_hook import evaluate_retrieval_candidates_with_acl
from backend.security_layer.retrieval.models import RetrievalSourceType
from backend.security_layer.retrieval.models import RetrievalStage


def monitor_only_live_retrieval_check(
    config: RetrievalIntegrationConfig,
    *,
    request_id: str,
    subject_id: str | None,
    tenant_id: str | None,
    retrieval_scope: tuple[str, ...],
    candidate_metadata: list[dict[str, object]],
) -> None:
    if not is_monitor_only(config):
        return
    context = build_retrieval_acl_context(
        RetrievalContextBuildInput(
            request_id=request_id,
            source_type=RetrievalSourceType.HYBRID,
            stage=RetrievalStage.DOCUMENT_ACL_CHECKED,
            subject_id=subject_id,
            tenant_id=tenant_id,
            retrieval_scope=retrieval_scope,
        )
    )
    candidates = build_candidates_from_metadata_list(candidate_metadata)
    evaluate_retrieval_candidates_with_acl(config, context, candidates)
