from __future__ import annotations

from collections.abc import Mapping

from onyx.security_layer.mcp_governance.models import MCPServerPolicy

DEFAULT_MCP_SERVER_REGISTRY: dict[str, MCPServerPolicy] = {
    "enterprise-search": MCPServerPolicy(
        mcp_server_id="enterprise-search",
        default_required_scopes=frozenset({"mcp:use"}),
        high_risk_tools=frozenset({"delete_document", "export_documents"}),
    ),
    "local-filesystem": MCPServerPolicy(
        mcp_server_id="local-filesystem",
        default_required_scopes=frozenset({"mcp:use"}),
        high_risk_tools=frozenset({"file_write", "code_execute"}),
    ),
}


def get_mcp_server_policy(
    mcp_server_id: str,
    registry: Mapping[str, MCPServerPolicy] | None = None,
) -> MCPServerPolicy | None:
    resolved_registry = registry or DEFAULT_MCP_SERVER_REGISTRY
    return resolved_registry.get(mcp_server_id)
