from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any
from typing import Protocol

from onyx.security_layer.audit.models import AuditEvent
from onyx.security_layer.langfuse_evidence import emit_tool_governance_langfuse_evidence
from onyx.security_layer.langfuse_evidence import safe_tool_governance_langfuse_payload
from onyx.security_layer.tool_governance.decision_mapper import evaluate_tool_governance
from onyx.security_layer.tool_governance.models import ToolActionRequest
from onyx.security_layer.tool_governance.models import ToolGovernanceDecision
from onyx.security_layer.tool_governance.models import ToolGovernanceResult
from onyx.security_layer.tool_governance.risk_registry import get_tool_risk_entry

TOOL_GOVERNANCE_ENFORCEMENT_ENV = "SECURITY_TOOL_GOVERNANCE_ENFORCEMENT"


class ToolGovernanceAuditRecorder(Protocol):
    def record(self, event: AuditEvent) -> AuditEvent:
        pass

# Only these names are connected for the first real execution-seam patch. The
# Onyx internal search implementation is exposed to the LLM as "internal_search";
# it is governed under the requested canonical "search" entry.
_SELECTED_TOOL_NAMES = frozenset(
    {
        "search",
        "internal_search",
        "read_document",
        "send_email",
        "delete_document",
        "external_api_call",
    }
)
_CANONICAL_TOOL_NAMES = {"internal_search": "search"}

_BLOCKING_DECISIONS = {
    ToolGovernanceDecision.DENY,
    ToolGovernanceDecision.APPROVAL_REQUIRED,
}


def is_tool_governance_enforcement_enabled() -> bool:
    return os.getenv(TOOL_GOVERNANCE_ENFORCEMENT_ENV, "false").lower() == "true"


def canonical_tool_governance_name(tool_name: str) -> str:
    normalized = tool_name.lower().strip()
    return _CANONICAL_TOOL_NAMES.get(normalized, normalized)


def is_selected_tool_for_governance(tool_name: str) -> bool:
    return tool_name.lower().strip() in _SELECTED_TOOL_NAMES


def build_tool_governance_request(
    *,
    user_id: str,
    tenant_id: str,
    tool_name: str,
    action: str,
    correlation_id: str,
    raw_tool_payload: Mapping[str, Any],
) -> ToolActionRequest:
    canonical_tool_name = canonical_tool_governance_name(tool_name)
    risk_entry = get_tool_risk_entry(canonical_tool_name)
    return ToolActionRequest(
        user_id=user_id,
        tenant_id=tenant_id,
        tool_name=canonical_tool_name,
        action=action,
        risk_level=risk_entry.risk_level,
        side_effect=risk_entry.side_effecting,
        is_side_effecting=risk_entry.side_effecting,
        correlation_id=correlation_id,
        raw_tool_payload=dict(raw_tool_payload),
    )


def record_tool_governance_evidence(
    *,
    result: ToolGovernanceResult,
    audit_service: ToolGovernanceAuditRecorder,
    session_id: str,
) -> dict[str, str | bool | int | float]:
    safe_evidence = safe_tool_governance_langfuse_payload(
        result.evidence.model_dump(mode="json")
    )
    audit_service.record(
        AuditEvent(
            event_type="tool_governance_decision",
            tenant_id=result.tenant_id,
            user_id=result.user_id,
            session_id=session_id,
            decision_id=result.receipt.receipt_hash,
            resource_type="tool",
            resource_id=result.tool_name,
            action=result.action,
            risk_level=result.risk_level.value,
            details={
                **safe_evidence,
                "governance_enforcement_enabled": True,
            },
        )
    )
    emit_tool_governance_langfuse_evidence(safe_evidence)
    return safe_evidence


def evaluate_tool_governance_at_execution_seam(
    *,
    tool_name: str,
    tool_args: Mapping[str, Any],
    user_id: str,
    tenant_id: str,
    session_id: str,
    correlation_id: str,
    audit_service: ToolGovernanceAuditRecorder,
    action: str = "execute",
) -> ToolGovernanceResult | None:
    if not is_tool_governance_enforcement_enabled():
        return None
    if not is_selected_tool_for_governance(tool_name):
        return None

    request = build_tool_governance_request(
        user_id=user_id,
        tenant_id=tenant_id,
        tool_name=tool_name,
        action=action,
        correlation_id=correlation_id,
        raw_tool_payload=tool_args,
    )
    result = evaluate_tool_governance(request)
    record_tool_governance_evidence(
        result=result,
        audit_service=audit_service,
        session_id=session_id,
    )
    return result


def should_block_tool_execution(result: ToolGovernanceResult | None) -> bool:
    return result is not None and result.decision in _BLOCKING_DECISIONS
