from __future__ import annotations

import re

from backend.security_layer.retrieval.context_builder import RetrievalContextBuildInput
from backend.security_layer.retrieval.context_builder import build_candidates_from_metadata_list
from backend.security_layer.retrieval.context_builder import build_retrieval_acl_context
from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationConfig
from backend.security_layer.retrieval.integration_flags import RetrievalIntegrationMode
from backend.security_layer.retrieval.integration_hook import evaluate_retrieval_candidates_with_acl
from backend.security_layer.retrieval.models import ACLSnapshot
from backend.security_layer.retrieval.models import RetrievalDecisionStatus
from backend.security_layer.retrieval.models import RetrievalSourceType
from backend.security_layer.retrieval.models import RetrievalStage
from backend.security_layer.runtime.audit import clear_audit_events
from backend.security_layer.runtime.audit import get_audit_events
from backend.security_layer.runtime.findings import clear_findings
from backend.security_layer.runtime.findings import get_findings
from backend.security_layer.runtime.metrics import clear_security_metrics
from backend.security_layer.runtime.metrics import get_security_metrics
from backend.security_layer.tests.retrieval_security_fixtures import build_retrieval_security_fixtures


def _base_context_input() -> RetrievalContextBuildInput:
    f = build_retrieval_security_fixtures()
    return RetrievalContextBuildInput(
        request_id="fake_request_negative_coverage",
        source_type=RetrievalSourceType.HYBRID,
        stage=RetrievalStage.DOCUMENT_ACL_CHECKED,
        subject_id=str(f["user_allowed"]["id"]),
        group_ids=(str(f["group_allowed"]["id"]),),
        role_ids=(str(f["role_allowed"]["id"]),),
        tenant_id=str(f["tenant_a"]["id"]),
        retrieval_scope=("synthetic_scope",),
        expected_vector_namespace=str(f["vector_namespace_allowed"]["namespace"]),
        acl_snapshot=ACLSnapshot(captured_at=__import__("datetime").datetime(2026, 1, 1), acl_entries_count=2, is_stale=False),
    )


def _allowed_candidate_metadata() -> dict[str, object]:
    f = build_retrieval_security_fixtures()
    return {
        "candidate_id": "fake_candidate_allowed",
        "document_id": str(f["document_allowed"]["id"]),
        "chunk_id": str(f["chunk_allowed"]["id"]),
        "tenant_id": str(f["tenant_a"]["id"]),
        "vector_namespace": str(f["vector_namespace_allowed"]["namespace"]),
        "source_type": "hybrid",
        "provenance_id": "fake_candidate_allowed",
        "document_allowed_subject_ids": (str(f["user_allowed"]["id"]),),
        "chunk_allowed_subject_ids": (str(f["user_allowed"]["id"]),),
        "document_allowed_group_ids": (str(f["group_allowed"]["id"]),),
        "chunk_allowed_group_ids": (str(f["group_allowed"]["id"]),),
        "document_allowed_role_ids": (str(f["role_allowed"]["id"]),),
        "chunk_allowed_role_ids": (str(f["role_allowed"]["id"]),),
        "document_is_deleted": False,
    }


def _evaluate(metadata: list[dict[str, object]], *, stale_acl: bool = False):
    context_input = _base_context_input()
    if stale_acl:
        context_input = RetrievalContextBuildInput(
            **{**context_input.__dict__, "acl_snapshot": ACLSnapshot(captured_at=__import__("datetime").datetime(2026, 1, 1), acl_entries_count=2, is_stale=True)}
        )
    context = build_retrieval_acl_context(context_input)
    candidates = build_candidates_from_metadata_list(metadata)
    return evaluate_retrieval_candidates_with_acl(
        RetrievalIntegrationConfig(mode=RetrievalIntegrationMode.MONITOR_ONLY),
        context,
        candidates,
    )


def test_negative_cases_are_flagged_in_monitor_only_without_blocking_or_filtering() -> None:
    clear_audit_events(); clear_findings(); clear_security_metrics()
    f = build_retrieval_security_fixtures()
    allowed = _allowed_candidate_metadata()
    cross_tenant_doc = {**allowed, "candidate_id": "fake_cross_tenant_document", "document_id": str(f["document_cross_tenant"]["id"]), "tenant_id": str(f["tenant_b"]["id"]) }
    cross_tenant_chunk = {**allowed, "candidate_id": "fake_cross_tenant_chunk", "chunk_id": str(f["chunk_cross_tenant"]["id"]), "tenant_id": str(f["tenant_b"]["id"]) }
    unauthorized_group = {**allowed, "candidate_id": "fake_unauthorized_group", "document_allowed_group_ids": (str(f["group_denied"]["id"]),), "chunk_allowed_group_ids": (str(f["group_denied"]["id"]),), "document_allowed_subject_ids": (), "chunk_allowed_subject_ids": (), "document_allowed_role_ids": (), "chunk_allowed_role_ids": ()}
    unauthorized_role = {**allowed, "candidate_id": "fake_unauthorized_role", "document_allowed_role_ids": (str(f["role_denied"]["id"]),), "chunk_allowed_role_ids": (str(f["role_denied"]["id"]),), "document_allowed_subject_ids": (), "chunk_allowed_subject_ids": (), "document_allowed_group_ids": (), "chunk_allowed_group_ids": ()}
    deleted_document = {**allowed, "candidate_id": "fake_deleted_document", "document_id": str(f["document_deleted"]["id"]), "document_is_deleted": True}
    vector_namespace_mismatch = {**allowed, "candidate_id": "fake_namespace_mismatch", "vector_namespace": str(f["vector_namespace_denied"]["namespace"])}
    metadata = [allowed, cross_tenant_doc, cross_tenant_chunk, unauthorized_group, unauthorized_role, deleted_document, vector_namespace_mismatch]
    result = _evaluate(metadata)

    assert len(result.candidates) == len(metadata)
    assert len(result.decision.allowed_candidates) < len(metadata)
    assert result.decision.status is RetrievalDecisionStatus.FILTER
    denied = set(result.decision.denied_candidate_ids)
    assert {"fake_cross_tenant_document", "fake_cross_tenant_chunk", "fake_unauthorized_group", "fake_unauthorized_role", "fake_deleted_document", "fake_namespace_mismatch"}.issubset(denied)

    assert get_audit_events()
    assert get_findings()
    assert get_security_metrics()


def test_stale_acl_snapshot_and_isolated_negative_controls() -> None:
    f = build_retrieval_security_fixtures()
    allowed = _allowed_candidate_metadata()
    result = _evaluate([allowed], stale_acl=True)
    assert result.decision.status is RetrievalDecisionStatus.FILTER
    assert "fake_candidate_allowed" in result.decision.denied_candidate_ids

    cache_cross_tenant_context = build_retrieval_acl_context(
        RetrievalContextBuildInput(
            request_id="fake_request_cache_denied",
            source_type=RetrievalSourceType.CACHE,
            stage=RetrievalStage.CACHE_READ_AUTHORIZED,
            subject_id=str(f["user_allowed"]["id"]),
            tenant_id=str(f["tenant_a"]["id"]),
            retrieval_scope=("synthetic_scope",),
        )
    )
    cache_cross_tenant_context = __import__("dataclasses").replace(
        cache_cross_tenant_context,
        cache_acl_context_key=f"{f['tenant_b']['id']}:{f['user_allowed']['id']}",
    )
    from backend.security_layer.retrieval.controls import authorize_cache_read_authorized
    cache_decision = authorize_cache_read_authorized(cache_cross_tenant_context)
    assert cache_decision.status is RetrievalDecisionStatus.DENY

    citation_denied = _evaluate([{**allowed, "candidate_id": str(f["citation_denied"]["id"]), "tenant_id": str(f["tenant_b"]["id"])}])
    rerank_denied = _evaluate([{**allowed, "candidate_id": str(f["rerank_candidate_denied"]["id"]), "tenant_id": str(f["tenant_b"]["id"])}])
    assert citation_denied.decision.status is RetrievalDecisionStatus.FILTER
    assert rerank_denied.decision.status is RetrievalDecisionStatus.FILTER


def test_non_leakage_negative_decisions_and_safe_unauthorized_representation() -> None:
    suspicious_patterns = re.compile(r"(api[_-]?key|token|credential|secret|bearer\s)", re.IGNORECASE)
    metadata = [{**_allowed_candidate_metadata(), "candidate_id": "fake_prompt_context_unauthorized", "tenant_id": "fake_tenant_beta"}]
    result = _evaluate(metadata)
    decision_blob = {
        "reason": result.decision.reason,
        "flags": list(result.decision.flags),
        "metadata": result.decision.metadata,
        "denied": list(result.decision.denied_candidate_ids),
    }
    serialized = str(decision_blob).lower()
    assert "document_text" not in serialized
    assert "chunk_text" not in serialized
    assert "source_secret" not in serialized
    assert suspicious_patterns.search(serialized) is None


def test_vector_metadata_mismatch_is_detected_in_isolated_validation() -> None:
    from dataclasses import replace
    from backend.security_layer.retrieval.models import VectorMetadata
    from backend.security_layer.retrieval.validators import validate_vector_metadata

    context = build_retrieval_acl_context(_base_context_input())
    candidate = build_candidates_from_metadata_list([_allowed_candidate_metadata()])[0]
    mismatched = replace(candidate, vector_metadata=VectorMetadata(tenant_id="fake_tenant_beta", document_id=candidate.document.document_id, chunk_id=candidate.chunk.chunk_id))
    assert validate_vector_metadata(context, mismatched) is False
