# Red-team Findings to Controls

This document maps fixture-based PyRIT and garak-style findings to existing Onyx controls.
It is an evidence mapping only and does not change OPA, scanner, tool governance, MCP governance, gateway governance, or evaluation behavior.

| Finding | Category | Control | Evidence boundary | Implementation reference |
| --- | --- | --- | --- | --- |
| pyrit-pi-001 | prompt_injection | RAG injection scanner | Maps red-team finding category to the existing scanner control; it does not change scanner behavior. | `backend/onyx/security_layer/artifact_scanner/scanner.py` |
| pyrit-evidence-001 | raw_evidence_leakage | redaction/Langfuse-safe evidence | Maps red-team finding category to evidence redaction controls; it does not export raw prompts, raw context, or secrets. | `backend/onyx/security_layer/langfuse_evidence.py` |
| pyrit-tool-001 | tool_abuse | tool governance | Maps red-team finding category to tool governance; it does not change tool authorization behavior. | `backend/onyx/security_layer/policies/tools.yaml` |
| pyrit-mcp-001 | mcp_scope_bypass | MCP governance | Maps red-team finding category to MCP governance; it does not change MCP enforcement behavior. | `backend/onyx/security_layer/mcp_governance/enforcement.py` |
| garak-pi-001 | prompt_injection | RAG injection scanner | Maps red-team finding category to the existing scanner control; it does not change scanner behavior. | `backend/onyx/security_layer/artifact_scanner/scanner.py` |
| garak-route-001 | secret_external_routing | gateway governance | Maps red-team finding category to gateway governance; it does not change gateway routing behavior. | `backend/onyx/security_layer/gateway_governance/route_policy.py` |
| garak-x-tenant-001 | cross_tenant_leakage | OPA Retrieval ACL | Maps red-team finding category to existing retrieval ACL governance; it does not change OPA policy behavior. | `backend/onyx/security_layer/policy/opa/retrieval_acl.rego` |
| garak-evidence-001 | raw_evidence_leakage | redaction/Langfuse-safe evidence | Maps red-team finding category to evidence redaction controls; it does not export raw prompts, raw context, or secrets. | `backend/onyx/security_layer/langfuse_evidence.py` |
