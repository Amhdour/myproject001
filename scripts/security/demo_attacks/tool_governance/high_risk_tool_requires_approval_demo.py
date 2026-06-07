from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND_PATH = REPO_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from onyx.security_layer.langfuse_evidence import (  # noqa: E402
    safe_tool_governance_langfuse_payload,
)
from onyx.security_layer.tool_governance import evaluate_tool_governance  # noqa: E402
from onyx.security_layer.tool_governance import LocalApprovalStore  # noqa: E402
from onyx.security_layer.tool_governance import ToolActionRequest  # noqa: E402


def main() -> int:
    store = LocalApprovalStore()
    request = ToolActionRequest(
        correlation_id="demo-tool-governance-high-risk",
        user_id="demo-user",
        tenant_id="demo-tenant",
        tool_name="send_email",
        action="execute",
        raw_tool_payload={
            "to": "customer@example.com",
            "subject": "Sensitive update",
            "body": "Do not export this raw payload or api_key=demo-secret-key",
        },
    )
    result = evaluate_tool_governance(request, approval_store=store)
    safe_evidence = safe_tool_governance_langfuse_payload(
        result.evidence.model_dump(mode="json")
    )

    print(
        json.dumps(
            {
                "demo": "high_risk_tool_requires_approval",
                "decision": result.decision.value,
                "risk_level": result.risk_level.value,
                "approval_required": result.approval_required,
                "approval_id_present": result.approval_id is not None,
                "receipt_hash": result.receipt.receipt_hash,
                "safe_evidence": safe_evidence,
                "raw_payload_exported": False,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if result.approval_required and result.approval_id else 1


if __name__ == "__main__":
    raise SystemExit(main())
