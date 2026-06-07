# MCP Governance Limitations

- This is an initial local governance foundation, not a production-ready MCP authorization system.
- The execution patch uses a narrow FastMCP tool-handler wrapper because this code path does not expose a central public FastMCP pre-dispatch hook. Future work should move the same wrapper to a central MCP middleware/dispatcher seam if FastMCP exposes one.
- Enforcement remains disabled unless `SECURITY_MCP_GOVERNANCE_ENFORCEMENT=true` is set.
- This change does not alter OPA Retrieval ACL behavior.
- This change does not alter RAG injection scanner behavior.
- This change does not alter tool governance behavior beyond reusing the existing audit/evidence pattern.
- Unknown server monitor mode is an explicit local configuration option; deny remains the default behavior.
- Approval decisions identify high-risk MCP tools, but no end-to-end human approval workflow is introduced here.
- Evidence export is metadata-only and intentionally excludes raw MCP payloads, secrets, tokens, tool outputs, prompts, and document content.
