from __future__ import annotations

from dataclasses import replace

from backend.security_layer.retrieval_acl.integration_config import INTEGRATION_MODE_ENV_VAR
from backend.security_layer.retrieval_acl.noop_seam_hook import clear_retrieval_acl_real_path_shadow_observations
from backend.security_layer.retrieval_acl.noop_seam_hook import observe_retrieval_acl_search_pipeline_noop_hook
from backend.security_layer.retrieval_acl.shadow_observation_audit import build_retrieval_acl_shadow_observation_audit_events
from backend.security_layer.retrieval_acl.shadow_observation_retention import DEFAULT_SHADOW_OBSERVATION_RETENTION_DAYS
from backend.security_layer.retrieval_acl.shadow_observation_retention import RetrievalACLShadowObservationRetentionPolicy
from backend.security_layer.retrieval_acl.shadow_observation_retention import build_shadow_observation_retention_decision_dicts
from backend.security_layer.retrieval_acl.shadow_observation_retention import build_shadow_observation_retention_decisions


def setup_function() -> None:
    clear_retrieval_acl_real_path_shadow_observations()


def _audit_events():
    observe_retrieval_acl_search_pipeline_noop_hook(
        chunks=[object(), object()],
        env={INTEGRATION_MODE_ENV_VAR: "shadow"},
    )
    return build_retrieval_acl_shadow_observation_audit_events(
        request_id="request-retention-1",
        observed_at_utc="2026-06-05T00:00:00+00:00",
    )


def test_retention_policy_marks_redacted_shadow_audit_event_eligible() -> None:
    decisions = build_shadow_observation_retention_decisions(
        audit_events=_audit_events(),
        evaluated_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(decisions) == 1
    decision = decisions[0]
    assert decision.request_id == "request-retention-1"
    assert decision.retention_days == DEFAULT_SHADOW_OBSERVATION_RETENTION_DAYS
    assert decision.retain_until_utc == "2026-07-05T00:00:00+00:00"
    assert decision.eligible_for_retention is True
    assert decision.delete_after_retention is True
    assert decision.redaction_policy_passed is True
    assert decision.reason == "redacted_shadow_observation_audit_event_retained"
    assert decision.production_readiness == "NO-GO"
    assert decision.enterprise_readiness == "NO-GO"
    assert decision.live_filtering_claimed is False
    assert decision.live_blocking_claimed is False
    assert decision.live_enforcement_claimed is False


def test_retention_policy_rejects_unredacted_audit_event() -> None:
    events = _audit_events()
    unredacted_event = replace(events[0], redacted=False)

    decisions = build_shadow_observation_retention_decisions(
        audit_events=(unredacted_event,),
        evaluated_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(decisions) == 1
    assert decisions[0].eligible_for_retention is False
    assert decisions[0].delete_after_retention is False
    assert decisions[0].redaction_policy_passed is False
    assert decisions[0].reason == "redaction_policy_failed_do_not_retain"


def test_retention_policy_rejects_events_with_document_content_or_ids() -> None:
    events = _audit_events()
    event_with_content = replace(events[0], contains_document_content=True)
    event_with_doc_ids = replace(events[0], contains_document_ids=True)

    decisions = build_shadow_observation_retention_decisions(
        audit_events=(event_with_content, event_with_doc_ids),
        evaluated_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(decisions) == 2
    assert all(decision.eligible_for_retention is False for decision in decisions)
    assert all(decision.redaction_policy_passed is False for decision in decisions)


def test_retention_policy_dicts_are_redacted_and_claim_bounded() -> None:
    decisions = build_shadow_observation_retention_decision_dicts(
        audit_events=_audit_events(),
        policy=RetrievalACLShadowObservationRetentionPolicy(retention_days=7),
        evaluated_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert len(decisions) == 1
    decision = decisions[0]
    forbidden_keys = {
        "document_id",
        "document_ids",
        "chunk_text",
        "content",
        "metadata",
        "user_prompt",
        "secret",
        "credential",
        "pii",
    }
    assert forbidden_keys.isdisjoint(decision.keys())
    assert decision["retention_days"] == 7
    assert decision["retain_until_utc"] == "2026-06-12T00:00:00+00:00"
    assert decision["production_readiness"] == "NO-GO"
    assert decision["enterprise_readiness"] == "NO-GO"
    assert decision["live_enforcement_claimed"] is False


def test_retention_policy_empty_when_no_audit_events_exist() -> None:
    decisions = build_shadow_observation_retention_decisions(
        audit_events=(),
        evaluated_at_utc="2026-06-05T00:00:00+00:00",
    )

    assert decisions == ()
