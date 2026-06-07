# MCP Governance Limitations

- This is an initial local governance foundation, not a production-ready MCP authorization system.
- The implementation does not add OpenGuardrails.
- The implementation does not alter OPA Retrieval ACL behavior.
- The implementation does not alter RAG injection scanner behavior.
- Unknown server monitor mode is an explicit local configuration option; deny remains the default behavior.
- Approval decisions identify high-risk MCP tools, but no end-to-end human approval workflow is introduced here.
- Evidence export is metadata-only and intentionally excludes raw MCP payloads, secrets, tokens, tool outputs, prompts, and document content.
