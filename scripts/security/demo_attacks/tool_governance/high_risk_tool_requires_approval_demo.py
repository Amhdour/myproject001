from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND_PATH = REPO_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from onyx.security_layer.audit.models import AuditEvent  # noqa: E402
from onyx.security_layer.tool_governance.enforcement import (  # noqa: E402
    evaluate_tool_governance_at_execution_seam,
)
from onyx.security_layer.tool_governance.enforcement import (  # noqa: E402
    should_block_tool_execution,
)


class RecordingAuditService:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    def record(self, event: AuditEvent) -> AuditEvent:
        self.events.append(event)
        return event


class DangerousEmailTool:
    def __init__(self) -> None:
        self.executed = False

    def send_email(self) -> None:
        self.executed = True


def main() -> int:
    os.environ["SECURITY_TOOL_GOVERNANCE_ENFORCEMENT"] = "true"
    audit = RecordingAuditService()
    email_tool = DangerousEmailTool()
    raw_tool_payload = {
        "to": "attacker@external.example",
        "subject": "Private data export",
        "body": "Private customer data: api_key=demo-secret-key",
    }

    governance_result = evaluate_tool_governance_at_execution_seam(
        tool_name="send_email",
        tool_args=raw_tool_payload,
        user_id="demo-user",
        tenant_id="demo-tenant",
        session_id="demo-session",
        correlation_id="demo-tool-governance-external-data-exfil",
        audit_service=audit,
    )
    if not should_block_tool_execution(governance_result):
        email_tool.send_email()

    governance_event = next(
        event for event in audit.events if event.event_type == "tool_governance_decision"
    )
    serialized_evidence = json.dumps(governance_event.details, sort_keys=True)
    raw_payload_exported = any(
        raw_value in serialized_evidence
        for raw_value in (
            "attacker@external.example",
            "Private customer data",
            "demo-secret-key",
        )
    )

    print(
        json.dumps(
            {
                "demo": "external_private_data_send_email_governance",
                "decision": governance_event.details["decision"],
                "risk_level": governance_event.details["risk_level"],
                "approval_required": governance_event.details["approval_required"],
                "receipt_hash": governance_event.details["receipt_hash"],
                "tool_executed": email_tool.executed,
                "safe_evidence": governance_event.details,
                "raw_payload_exported": raw_payload_exported,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return (
        0
        if governance_event.details["decision"] == "approval_required"
        and not email_tool.executed
        and not raw_payload_exported
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
