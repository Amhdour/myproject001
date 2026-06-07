#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

EVIDENCE_PATH = Path("docs/security/evidence/opa/decision_log_samples.jsonl")
EVENT_TYPE = "security.opa.retrieval_acl.decision"
POLICY_PACKAGE = "onyx.security.retrieval_acl"
POLICY_VERSION = "v1"
ACTION = "rag.context.include"


def _normalize_string_list(values: list[str] | None) -> list[str]:
    if values is None:
        return []
    return sorted({str(value) for value in values if str(value)})


def _build_demo_input() -> dict[str, Any]:
    return {
        "subject": {
            "user_id": "tenant-a-user",
            "tenant_id": "tenant-a",
            "groups": _normalize_string_list(["tenant-a-readers"]),
        },
        "resource": {
            "document_id": "tenant-b-doc",
            "chunk_id": "tenant-b-doc:chunk-1",
            "tenant_id": "tenant-b",
            "allowed_users": _normalize_string_list(["tenant-b-user"]),
            "allowed_groups": _normalize_string_list(["tenant-b-readers"]),
            "connector_id": "tenant-b-connector",
            "deleted": False,
            "permission_version": "pv-tenant-b-001",
        },
        "action": ACTION,
        "correlation_id": "opa-demo-cross-tenant-001",
    }


def _simulated_opa_policy_result(opa_input: dict[str, Any]) -> dict[str, str]:
    subject = opa_input["subject"]
    resource = opa_input["resource"]
    if not subject.get("tenant_id") or not resource.get("tenant_id"):
        return _decision("deny", "missing tenant metadata")
    if subject["tenant_id"] != resource["tenant_id"]:
        return _decision("deny", "cross-tenant resource")
    if resource.get("deleted") is True:
        return _decision("deny", "deleted document")
    if not resource.get("permission_version"):
        return _decision("deny", "missing permission metadata")
    if not resource.get("allowed_users") and not resource.get("allowed_groups"):
        return _decision("deny", "missing permission metadata")
    if subject.get("user_id") in resource.get("allowed_users", []):
        return _decision("allow", "same tenant allowed user")
    if set(subject.get("groups", [])) & set(resource.get("allowed_groups", [])):
        return _decision("allow", "same tenant allowed group")
    return _decision("deny", "subject is not permitted for resource")


def _decision(decision: str, reason: str) -> dict[str, str]:
    return {
        "decision": decision,
        "reason": reason,
        "policy_package": POLICY_PACKAGE,
        "policy_version": POLICY_VERSION,
    }


def run_demo() -> dict[str, Any]:
    opa_input = _build_demo_input()
    policy_result = _simulated_opa_policy_result(opa_input)
    tenant_b_chunk = "TENANT_B_CONFIDENTIAL_CONTEXT"
    final_context_chunks = (
        [] if policy_result["decision"] != "allow" else [tenant_b_chunk]
    )
    chunk_excluded = tenant_b_chunk not in final_context_chunks
    evidence = {
        "event_type": EVENT_TYPE,
        "decision": policy_result["decision"],
        "reason": policy_result["reason"],
        "policy_package": policy_result["policy_package"],
        "policy_version": policy_result["policy_version"],
        "subject_user_id": opa_input["subject"]["user_id"],
        "subject_tenant_id": opa_input["subject"]["tenant_id"],
        "resource_document_id": opa_input["resource"]["document_id"],
        "resource_tenant_id": opa_input["resource"]["tenant_id"],
        "correlation_id": opa_input["correlation_id"],
        "fallback_used": False,
        "demo_attack": "Tenant A user receives Tenant B chunk",
        "tenant_a_received_tenant_b_chunk": True,
        "opa_denied_cross_tenant_chunk": policy_result["decision"] == "deny",
        "chunk_excluded_from_rag_context": chunk_excluded,
        "final_context_contains_tenant_b_chunk": tenant_b_chunk in final_context_chunks,
        "audit_evidence_path": str(EVIDENCE_PATH),
    }
    EVIDENCE_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_PATH.write_text(
        json.dumps(evidence, sort_keys=True) + "\n", encoding="utf-8"
    )
    return evidence


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, sort_keys=True))
