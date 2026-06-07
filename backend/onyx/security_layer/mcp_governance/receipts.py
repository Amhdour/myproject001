from __future__ import annotations

import hashlib
import json
from typing import Any

from onyx.security_layer.mcp_governance.models import MCPGovernanceDecision
from onyx.security_layer.mcp_governance.models import MCPGovernanceReceipt


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, default=str, separators=(",", ":"), sort_keys=True)


def generate_mcp_governance_receipt_hash(receipt_fields: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(receipt_fields).encode("utf-8")).hexdigest()


def create_mcp_governance_receipt(
    *,
    correlation_id: str,
    user_id: str,
    tenant_id: str,
    mcp_server_id: str,
    mcp_tool_name: str | None,
    mcp_resource_id: str | None,
    decision: MCPGovernanceDecision,
    reason: str,
    previous_receipt_hash: str | None = None,
) -> MCPGovernanceReceipt:
    unsigned_receipt = MCPGovernanceReceipt(
        receipt_hash="pending",
        previous_receipt_hash=previous_receipt_hash,
        correlation_id=correlation_id,
        user_id=user_id,
        tenant_id=tenant_id,
        mcp_server_id=mcp_server_id,
        mcp_tool_name=mcp_tool_name,
        mcp_resource_id=mcp_resource_id,
        decision=decision,
        reason=reason,
    )
    receipt_dict = unsigned_receipt.model_dump(mode="json")
    receipt_dict.pop("receipt_hash", None)
    return unsigned_receipt.model_copy(
        update={"receipt_hash": generate_mcp_governance_receipt_hash(receipt_dict)}
    )
