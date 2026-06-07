from __future__ import annotations

from onyx.security_layer.opa.decision_mapper import OPADecisionValue
from onyx.security_layer.opa.decision_mapper import map_opa_result
from onyx.security_layer.opa.fallback import deny_high_risk_retrieval_fallback
from onyx.security_layer.opa.input_builder import build_retrieval_acl_input


def _opa_input() -> dict[str, object]:
    return build_retrieval_acl_input(
        subject_user_id="user-a",
        subject_tenant_id="tenant-a",
        subject_groups=["group-b", "group-a", "group-a"],
        resource_document_id="doc-a",
        resource_chunk_id=1,
        resource_tenant_id="tenant-a",
        resource_allowed_users=["user-a"],
        resource_allowed_groups=["group-a"],
        resource_connector_id="connector-a",
        resource_deleted=False,
        resource_permission_version="pv-1",
        correlation_id="corr-1",
    )


def test_build_retrieval_acl_input_normalizes_required_fields() -> None:
    opa_input = _opa_input()
    assert opa_input["action"] == "rag.context.include"
    assert opa_input["correlation_id"] == "corr-1"
    assert opa_input["subject"] == {
        "user_id": "user-a",
        "tenant_id": "tenant-a",
        "groups": ["group-a", "group-b"],
    }
    assert opa_input["resource"] == {
        "document_id": "doc-a",
        "chunk_id": "1",
        "tenant_id": "tenant-a",
        "allowed_users": ["user-a"],
        "allowed_groups": ["group-a"],
        "connector_id": "connector-a",
        "deleted": False,
        "permission_version": "pv-1",
    }


def test_map_opa_result_supports_decision_values_and_audit_details() -> None:
    opa_input = _opa_input()
    decision = map_opa_result(
        {
            "decision": "shadow_deny",
            "reason": "would deny in enforcement",
            "policy_package": "onyx.security.retrieval_acl",
            "policy_version": "v1",
        },
        opa_input,
    )
    assert decision.decision == OPADecisionValue.SHADOW_DENY
    assert decision.audit_details["event_type"] == "security.opa.retrieval_acl.decision"
    assert decision.audit_details["subject_user_id"] == "user-a"
    assert decision.audit_details["resource_document_id"] == "doc-a"


def test_fallback_denies_high_risk_retrieval_decision() -> None:
    decision = deny_high_risk_retrieval_fallback(_opa_input(), "connection refused")
    assert decision.decision == OPADecisionValue.DENY
    assert decision.fallback_used is True
    assert "OPA unavailable" in decision.reason
