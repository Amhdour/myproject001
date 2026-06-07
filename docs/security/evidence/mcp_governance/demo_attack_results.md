# MCP Scope Bypass Demo Attack Results

The demo attack constructs an MCP request for a resource owned by `tenant-b` while the requester belongs to `tenant-a`. The local MCP governance layer denies the cross-tenant resource access and emits a receipt hash plus Langfuse-safe metadata.

Expected result summary:

- `decision`: `deny`
- `reason`: `Cross-tenant MCP resource access denied`
- `raw_payload_exported`: `false`
- `receipt_hash`: present SHA-256 hash

The demo is intentionally local and does not claim production readiness.
