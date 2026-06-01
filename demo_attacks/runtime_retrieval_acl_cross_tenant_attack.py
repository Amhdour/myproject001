from __future__ import annotations

from dataclasses import dataclass

from backend.security_layer.runtime_enforcement.audit import clear_runtime_audit_events
from backend.security_layer.runtime_enforcement.audit import get_runtime_audit_events
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementConfig
from backend.security_layer.runtime_enforcement.config import RuntimeEnforcementMode
from backend.security_layer.runtime_enforcement.context import RuntimeRetrievalContext
from backend.security_layer.runtime_enforcement.retrieval_adapter import enforce_retrieval_runtime
from backend.security_layer.runtime_enforcement.telemetry import clear_runtime_retrieval_acl_metrics
from backend.security_layer.runtime_enforcement.telemetry import get_runtime_retrieval_acl_metrics


@dataclass(frozen=True)
class DemoRetrievedChunk:
    document_id: str
    chunk_id: int
    metadata: dict[str, str | list[str]]


def run_attack() -> int:
    clear_runtime_audit_events()
    clear_runtime_retrieval_acl_metrics()

    authorized_chunk = DemoRetrievedChunk(
        document_id="tenant-a-roadmap",
        chunk_id=1,
        metadata={"tenant_id": "tenant-a", "allowed_subject_ids": ["user-a"]},
    )
    leaked_chunk = DemoRetrievedChunk(
        document_id="tenant-b-secret-plan",
        chunk_id=2,
        metadata={"tenant_id": "tenant-b", "allowed_subject_ids": ["user-b"]},
    )

    result = enforce_retrieval_runtime(
        config=RuntimeEnforcementConfig(mode=RuntimeEnforcementMode.ENFORCE),
        context=RuntimeRetrievalContext(
            request_id="step-63x-cross-tenant-demo-attack",
            subject_id="user-a",
            tenant_id="tenant-a",
        ),
        chunks=[authorized_chunk, leaked_chunk],
    )

    allowed_document_ids = {chunk.document_id for chunk in result.allowed_chunks}
    audit_events = get_runtime_audit_events()
    metrics = get_runtime_retrieval_acl_metrics()

    attack_blocked = (
        "tenant-b-secret-plan" not in allowed_document_ids
        and "tenant-a-roadmap" in allowed_document_ids
        and result.enforcement_result == "blocked"
        and result.denied_chunk_count == 1
        and bool(audit_events)
        and audit_events[-1].reason_code == "retrieval_authorization_failed"
        and bool(metrics)
        and metrics[-1].enforcement_result == "blocked"
    )

    if attack_blocked:
        print("PASS: unauthorized cross-tenant retrieval was blocked.")
        print("decision=deny reason=retrieval_authorization_failed denied_chunk_count=1")
        print("audit_event=retrieval_authorization_failed telemetry=retrieval_acl_decision_total")
        return 0

    print("FAIL: unauthorized cross-tenant retrieval reached context or evidence was missing.")
    print(f"allowed_document_ids={sorted(allowed_document_ids)}")
    print(f"result={result}")
    print(f"audit_events={audit_events}")
    print(f"metrics={metrics}")
    return 1


if __name__ == "__main__":
    raise SystemExit(run_attack())
