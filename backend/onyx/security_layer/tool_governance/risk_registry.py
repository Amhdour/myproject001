from __future__ import annotations

from dataclasses import dataclass

from onyx.security_layer.tool_governance.models import ToolRiskLevel


@dataclass(frozen=True)
class ToolRiskEntry:
    tool_name: str
    risk_level: ToolRiskLevel
    side_effecting: bool
    reason: str


DEFAULT_TOOL_RISK_REGISTRY: dict[str, ToolRiskEntry] = {
    "search": ToolRiskEntry("search", ToolRiskLevel.LOW, False, "Read-only search action"),
    "read_document": ToolRiskEntry(
        "read_document", ToolRiskLevel.MEDIUM, False, "Document read action"
    ),
    "send_email": ToolRiskEntry(
        "send_email", ToolRiskLevel.HIGH, True, "Outbound email side effect"
    ),
    "delete_document": ToolRiskEntry(
        "delete_document", ToolRiskLevel.CRITICAL, True, "Destructive document deletion"
    ),
    "external_api_call": ToolRiskEntry(
        "external_api_call", ToolRiskLevel.HIGH, True, "External side-effect capable call"
    ),
}


def get_tool_risk_entry(
    tool_name: str,
    registry: dict[str, ToolRiskEntry] | None = None,
) -> ToolRiskEntry:
    resolved_registry = registry or DEFAULT_TOOL_RISK_REGISTRY
    normalized_name = tool_name.lower().strip()
    return resolved_registry.get(
        normalized_name,
        ToolRiskEntry(
            normalized_name,
            ToolRiskLevel.CRITICAL,
            True,
            "Unknown tool defaults to critical side-effect governance",
        ),
    )
