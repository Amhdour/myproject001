from __future__ import annotations

from onyx.security_layer.tool_governance.approval import ApprovalReplayError
from onyx.security_layer.tool_governance.approval import calculate_action_hash
from onyx.security_layer.tool_governance.approval import LocalApprovalStore
from onyx.security_layer.tool_governance.models import ToolActionRequest
from onyx.security_layer.tool_governance.models import ToolGovernanceConfig
from onyx.security_layer.tool_governance.models import ToolGovernanceDecision
from onyx.security_layer.tool_governance.models import ToolGovernanceEvidence
from onyx.security_layer.tool_governance.models import ToolGovernanceResult
from onyx.security_layer.tool_governance.models import ToolRiskLevel
from onyx.security_layer.tool_governance.receipts import create_tool_governance_receipt
from onyx.security_layer.tool_governance.risk_registry import get_tool_risk_entry
from onyx.security_layer.tool_governance.risk_registry import ToolRiskEntry
from onyx.security_layer.tracing import security_span
from onyx.security_layer.tracing import set_security_span_attributes


def _base_decision(
    risk_level: ToolRiskLevel,
    *,
    side_effecting: bool,
    config: ToolGovernanceConfig,
) -> tuple[ToolGovernanceDecision, str, bool]:
    if risk_level == ToolRiskLevel.LOW:
        return ToolGovernanceDecision.ALLOW, "Low-risk tool action allowed", False
    if risk_level == ToolRiskLevel.MEDIUM and not side_effecting:
        return ToolGovernanceDecision.MONITOR, "Medium-risk read action monitored", False
    if risk_level == ToolRiskLevel.HIGH and side_effecting:
        return (
            ToolGovernanceDecision.APPROVAL_REQUIRED,
            "High-risk side-effecting action requires approval",
            True,
        )
    if risk_level == ToolRiskLevel.CRITICAL and side_effecting:
        if config.critical_side_effect_requires_approval:
            return (
                ToolGovernanceDecision.APPROVAL_REQUIRED,
                "Critical side-effecting action requires approval by configuration",
                True,
            )
        return ToolGovernanceDecision.DENY, "Critical side-effecting action denied", False
    if risk_level in {ToolRiskLevel.HIGH, ToolRiskLevel.CRITICAL}:
        return ToolGovernanceDecision.MONITOR, "Elevated non-side-effect action monitored", False
    return ToolGovernanceDecision.MONITOR, "Tool action monitored", False


def evaluate_tool_governance(
    request: ToolActionRequest,
    *,
    config: ToolGovernanceConfig | None = None,
    registry: dict[str, ToolRiskEntry] | None = None,
    approval_store: LocalApprovalStore | None = None,
    previous_receipt_hash: str | None = None,
) -> ToolGovernanceResult:
    resolved_config = config or ToolGovernanceConfig()
    risk_entry = get_tool_risk_entry(request.tool_name, registry)
    side_effecting = (
        risk_entry.side_effecting
        if request.is_side_effecting is None
        else request.is_side_effecting
    )
    action_hash = calculate_action_hash(
        tenant_id=request.tenant_id,
        tool_name=risk_entry.tool_name,
        action=request.action,
    )

    decision, reason, approval_required = _base_decision(
        risk_entry.risk_level,
        side_effecting=side_effecting,
        config=resolved_config,
    )

    if decision == ToolGovernanceDecision.APPROVAL_REQUIRED and request.approval_id:
        try:
            store = approval_store or LocalApprovalStore()
            store.consume(request.approval_id, action_hash=action_hash)
            decision = ToolGovernanceDecision.ALLOW
            reason = "Approved high-risk tool action allowed"
            approval_required = False
        except ApprovalReplayError as e:
            decision = ToolGovernanceDecision.DENY
            reason = f"Approval replay protection blocked action: {e}"
            approval_required = False

    approval_id = None
    if decision == ToolGovernanceDecision.APPROVAL_REQUIRED:
        store = approval_store or LocalApprovalStore()
        approval = store.create_pending_approval(
            correlation_id=request.correlation_id,
            tenant_id=request.tenant_id,
            user_id=request.user_id,
            tool_name=risk_entry.tool_name,
            action=request.action,
            action_hash=action_hash,
            ttl_seconds=resolved_config.approval_ttl_seconds,
        )
        approval_id = approval.approval_id

    if resolved_config.shadow_mode and decision in {
        ToolGovernanceDecision.DENY,
        ToolGovernanceDecision.APPROVAL_REQUIRED,
    }:
        decision = ToolGovernanceDecision.SHADOW_DENY
        reason = f"Shadow mode would block: {reason}"
        approval_required = False

    receipt = create_tool_governance_receipt(
        correlation_id=request.correlation_id,
        user_id=request.user_id,
        tenant_id=request.tenant_id,
        tool_name=risk_entry.tool_name,
        action=request.action,
        decision=decision,
        reason=reason,
        previous_receipt_hash=previous_receipt_hash,
    )
    evidence = ToolGovernanceEvidence(
        tool_name=risk_entry.tool_name,
        action=request.action,
        risk_level=risk_entry.risk_level,
        decision=decision,
        approval_required=approval_required,
        receipt_hash=receipt.receipt_hash,
        correlation_id=request.correlation_id,
    )

    with security_span(
        "security.tool_governance.decision",
        {
            "security.correlation_id": request.correlation_id,
            "security.tool_name": risk_entry.tool_name,
            "security.action": request.action,
            "security.risk_level": risk_entry.risk_level.value,
            "security.decision": decision.value,
            "security.approval_required": approval_required,
        },
    ) as span:
        set_security_span_attributes(
            span,
            {"security.receipt_hash": receipt.receipt_hash},
        )

    return ToolGovernanceResult(
        correlation_id=request.correlation_id,
        user_id=request.user_id,
        tenant_id=request.tenant_id,
        tool_name=risk_entry.tool_name,
        action=request.action,
        risk_level=risk_entry.risk_level,
        decision=decision,
        reason=reason,
        approval_required=approval_required,
        approval_id=approval_id,
        action_hash=action_hash,
        receipt=receipt,
        evidence=evidence,
    )
