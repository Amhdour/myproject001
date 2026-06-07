from __future__ import annotations

import hashlib
import json
from typing import Any

from onyx.security_layer.tool_governance.models import ToolGovernanceDecision
from onyx.security_layer.tool_governance.models import ToolGovernanceReceipt


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, default=str, separators=(",", ":"), sort_keys=True)


def generate_receipt_hash(receipt_fields: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(receipt_fields).encode("utf-8")).hexdigest()


def create_tool_governance_receipt(
    *,
    correlation_id: str,
    user_id: str,
    tenant_id: str,
    tool_name: str,
    action: str,
    decision: ToolGovernanceDecision,
    reason: str,
    previous_receipt_hash: str | None = None,
) -> ToolGovernanceReceipt:
    unsigned_receipt = ToolGovernanceReceipt(
        receipt_hash="pending",
        previous_receipt_hash=previous_receipt_hash,
        correlation_id=correlation_id,
        user_id=user_id,
        tenant_id=tenant_id,
        tool_name=tool_name,
        action=action,
        decision=decision,
        reason=reason,
    )
    receipt_dict = unsigned_receipt.model_dump(mode="json")
    receipt_dict.pop("receipt_hash", None)
    return unsigned_receipt.model_copy(
        update={"receipt_hash": generate_receipt_hash(receipt_dict)}
    )
