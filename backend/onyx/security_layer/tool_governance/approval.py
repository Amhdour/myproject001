from __future__ import annotations

import hashlib
import json
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

from onyx.security_layer.tool_governance.models import ApprovalRequest


class ApprovalError(ValueError):
    pass


class SelfApprovalError(ApprovalError):
    pass


class ApprovalReplayError(ApprovalError):
    pass


def calculate_action_hash(
    *,
    tenant_id: str,
    tool_name: str,
    action: str,
    safe_action_context: dict[str, Any] | None = None,
) -> str:
    """Hash the approval subject without serializing raw tool payloads."""

    payload = {
        "tenant_id": tenant_id,
        "tool_name": tool_name,
        "action": action,
        "safe_action_context": safe_action_context or {},
    }
    serialized = json.dumps(payload, default=str, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class LocalApprovalStore:
    """In-memory approval store for local governance tests and demos.

    This is intentionally not a production persistence layer. It exists to model
    self-approval prevention and replay protection before UI/storage integration.
    """

    def __init__(self) -> None:
        self._approvals: dict[str, ApprovalRequest] = {}

    def create_pending_approval(
        self,
        *,
        correlation_id: str,
        tenant_id: str,
        user_id: str,
        tool_name: str,
        action: str,
        action_hash: str,
        ttl_seconds: int,
    ) -> ApprovalRequest:
        approval = ApprovalRequest(
            correlation_id=correlation_id,
            tenant_id=tenant_id,
            user_id=user_id,
            tool_name=tool_name,
            action=action,
            action_hash=action_hash,
            requested_by_user_id=user_id,
            expires_at=datetime.now(timezone.utc) + timedelta(seconds=ttl_seconds),
        )
        self._approvals[approval.approval_id] = approval
        return approval

    def approve(self, approval_id: str, *, approved_by_user_id: str) -> ApprovalRequest:
        approval = self._get(approval_id)
        if approval.requested_by_user_id == approved_by_user_id:
            raise SelfApprovalError("Approval requester cannot approve their own action")
        updated = approval.model_copy(update={"approved_by_user_id": approved_by_user_id})
        self._approvals[approval_id] = updated
        return updated

    def consume(self, approval_id: str, *, action_hash: str) -> ApprovalRequest:
        approval = self._get(approval_id)
        now = datetime.now(timezone.utc)
        if approval.used_at is not None:
            raise ApprovalReplayError("Approval was already used")
        if approval.expires_at <= now:
            raise ApprovalReplayError("Approval expired")
        if approval.action_hash != action_hash:
            raise ApprovalReplayError("Approval action hash mismatch")
        if approval.approved_by_user_id is None:
            raise ApprovalReplayError("Approval is not approved")

        used = approval.model_copy(update={"used_at": now})
        self._approvals[approval_id] = used
        return used

    def _get(self, approval_id: str) -> ApprovalRequest:
        approval = self._approvals.get(approval_id)
        if approval is None:
            raise ApprovalReplayError("Approval not found")
        return approval
