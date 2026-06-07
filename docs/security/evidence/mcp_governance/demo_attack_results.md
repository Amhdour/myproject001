# MCP Governance Demo Attack Results

The MCP governance demo attack constructs an MCP request for a resource owned by `tenant-b` while the requester belongs to `tenant-a`. The local MCP governance layer denies the cross-tenant resource access and emits a receipt hash plus Langfuse-safe metadata.

Expected result summary:

- `decision`: `deny`
- `reason`: `Cross-tenant MCP resource access denied`
- `raw_payload_exported`: `false`
- `receipt_hash`: present SHA-256 hash

Additional enforcement-seam tests cover the env-gated near-real FastMCP tool wrapper now called before selected MCP tool handlers execute. With `SECURITY_MCP_GOVERNANCE_ENFORCEMENT=true`, cross-tenant resource requests, missing-scope requests, and high-risk MCP tools are blocked before automatic execution. `monitor` and `shadow_deny` decisions still allow execution while recording metadata-only evidence.

The demo and tests are intentionally local and do not claim production readiness.
