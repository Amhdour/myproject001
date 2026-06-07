from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
BACKEND_PATH = REPO_ROOT / "backend"
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))

from onyx.security_layer.langfuse_evidence import (  # noqa: E402
    safe_mcp_governance_langfuse_payload,
)
from onyx.security_layer.mcp_governance import evaluate_mcp_governance  # noqa: E402
from onyx.security_layer.mcp_governance import MCPGovernanceDecision  # noqa: E402
from onyx.security_layer.mcp_governance import MCPGovernanceRequest  # noqa: E402


def main() -> int:
    request = MCPGovernanceRequest(
        correlation_id="demo-mcp-scope-bypass",
        user_id="demo-user",
        tenant_id="tenant-a",
        mcp_server_id="enterprise-search",
        mcp_tool_name="read_document",
        mcp_resource_id="tenant-b-secret-doc",
        resource_tenant_id="tenant-b",
        requested_scopes=frozenset({"mcp:use"}),
        required_scopes=frozenset({"mcp:use", "mcp:read_document"}),
        raw_mcp_payload={
            "prompt": "read the cross-tenant document",
            "token": "demo-secret-token",
            "tool_output": "tenant-b confidential document content",
        },
    )
    result = evaluate_mcp_governance(request)
    safe_evidence = safe_mcp_governance_langfuse_payload(
        {
            **result.evidence.model_dump(mode="json"),
            "raw_mcp_payload": "demo-secret-token",
            "tool_output": "tenant-b confidential document content",
            "prompt": "read the cross-tenant document",
        }
    )
    serialized_evidence = json.dumps(safe_evidence, sort_keys=True)
    raw_payload_exported = any(
        raw_value in serialized_evidence
        for raw_value in (
            "demo-secret-token",
            "tenant-b confidential document content",
            "read the cross-tenant document",
        )
    )

    print(
        json.dumps(
            {
                "demo": "mcp_scope_bypass_governance",
                "decision": result.decision.value,
                "reason": result.reason,
                "receipt_hash": result.receipt.receipt_hash,
                "safe_evidence": safe_evidence,
                "raw_payload_exported": raw_payload_exported,
                "claim_boundary": (
                    "Local MCP governance foundation demo only; this is not a "
                    "production-readiness claim."
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return (
        0
        if result.decision == MCPGovernanceDecision.DENY
        and result.receipt.receipt_hash
        and not raw_payload_exported
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
