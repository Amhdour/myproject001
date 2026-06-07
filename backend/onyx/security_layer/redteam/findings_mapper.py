from __future__ import annotations

from onyx.security_layer.redteam.models import RedteamControlMapping
from onyx.security_layer.redteam.models import RedteamFinding
from onyx.security_layer.redteam.models import RedteamFindingCategory

_CONTROL_MAPPINGS: dict[RedteamFindingCategory, RedteamControlMapping] = {
    RedteamFindingCategory.PROMPT_INJECTION: RedteamControlMapping(
        category=RedteamFindingCategory.PROMPT_INJECTION,
        control_name="RAG injection scanner",
        control_summary="Retrieved-content prompt injection signals are handled by the RAG injection scanner evidence path.",
        evidence_boundary="Maps red-team finding category to the existing scanner control; it does not change scanner behavior.",
        implementation_reference="backend/onyx/security_layer/artifact_scanner/scanner.py",
    ),
    RedteamFindingCategory.CROSS_TENANT_LEAKAGE: RedteamControlMapping(
        category=RedteamFindingCategory.CROSS_TENANT_LEAKAGE,
        control_name="OPA Retrieval ACL",
        control_summary="Cross-tenant retrieval leakage findings map to the OPA retrieval ACL control evidence.",
        evidence_boundary="Maps red-team finding category to existing retrieval ACL governance; it does not change OPA policy behavior.",
        implementation_reference="backend/onyx/security_layer/policy/opa/retrieval_acl.rego",
    ),
    RedteamFindingCategory.TOOL_ABUSE: RedteamControlMapping(
        category=RedteamFindingCategory.TOOL_ABUSE,
        control_name="tool governance",
        control_summary="Tool-abuse attempts map to existing tool governance approval and policy controls.",
        evidence_boundary="Maps red-team finding category to tool governance; it does not change tool authorization behavior.",
        implementation_reference="backend/onyx/security_layer/policies/tools.yaml",
    ),
    RedteamFindingCategory.MCP_SCOPE_BYPASS: RedteamControlMapping(
        category=RedteamFindingCategory.MCP_SCOPE_BYPASS,
        control_name="MCP governance",
        control_summary="MCP scope bypass attempts map to MCP governance scope and receipt evidence.",
        evidence_boundary="Maps red-team finding category to MCP governance; it does not change MCP enforcement behavior.",
        implementation_reference="backend/onyx/security_layer/mcp_governance/enforcement.py",
    ),
    RedteamFindingCategory.SECRET_EXTERNAL_ROUTING: RedteamControlMapping(
        category=RedteamFindingCategory.SECRET_EXTERNAL_ROUTING,
        control_name="gateway governance",
        control_summary="Secret external routing attempts map to gateway route governance controls.",
        evidence_boundary="Maps red-team finding category to gateway governance; it does not change gateway routing behavior.",
        implementation_reference="backend/onyx/security_layer/gateway_governance/route_policy.py",
    ),
    RedteamFindingCategory.RAW_EVIDENCE_LEAKAGE: RedteamControlMapping(
        category=RedteamFindingCategory.RAW_EVIDENCE_LEAKAGE,
        control_name="redaction/Langfuse-safe evidence",
        control_summary="Raw prompt, context, and secret evidence leakage maps to redaction and Langfuse-safe evidence handling.",
        evidence_boundary="Maps red-team finding category to evidence redaction controls; it does not export raw prompts, raw context, or secrets.",
        implementation_reference="backend/onyx/security_layer/langfuse_evidence.py",
    ),
}


def get_control_mapping(category: RedteamFindingCategory) -> RedteamControlMapping:
    return _CONTROL_MAPPINGS[category]


def map_findings_to_controls(findings: list[RedteamFinding]) -> list[RedteamFinding]:
    return [
        finding.model_copy(update={"control_mapping": get_control_mapping(finding.category)})
        for finding in findings
    ]


def render_findings_to_controls_markdown(findings: list[RedteamFinding]) -> str:
    mapped_findings = map_findings_to_controls(findings)
    lines = [
        "# Red-team Findings to Controls",
        "",
        "This document maps fixture-based PyRIT and garak-style findings to existing Onyx controls.",
        "It is an evidence mapping only and does not change OPA, scanner, tool governance, MCP governance, gateway governance, or evaluation behavior.",
        "",
        "| Finding | Category | Control | Evidence boundary | Implementation reference |",
        "| --- | --- | --- | --- | --- |",
    ]
    for finding in mapped_findings:
        assert finding.control_mapping is not None
        mapping = finding.control_mapping
        lines.append(
            f"| {finding.finding_id} | {finding.category.value} | {mapping.control_name} | "
            f"{mapping.evidence_boundary} | `{mapping.implementation_reference}` |"
        )
    return "\n".join(lines) + "\n"
