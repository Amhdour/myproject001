# Threat Model (Step 6 Initial)

## Scope and Status
This is an initial documentation-only threat model derived from architecture discovery and patch-point mapping artifacts. No production-readiness claim is made.

## Assets
- Tenant documents and metadata
- Retrieval results and citations
- Vector index namespaces and filters
- Connector credentials and sync state
- Tool execution capabilities and outputs
- MCP server trust channels and capabilities
- Sandbox execution environment and artifacts
- Approval decisions and audit logs
- Security evidence and readiness records

## Actors
- End users (authorized)
- Tenant admins
- Platform operators
- AI agent runtime
- External connector systems
- MCP servers/tools
- Potential malicious users/insiders

## Trust Boundaries
- User session boundary (identity and role)
- Tenant data isolation boundary
- Retrieval and vector boundary
- Connector ingestion boundary
- Tool invocation boundary
- MCP integration boundary
- Sandbox/runtime execution boundary
- Audit/evidence governance boundary

## Abuse Cases
- Cross-tenant data retrieval through ACL/filter bypass
- Unauthorized tool execution for privileged actions
- MCP confused deputy via delegated over-privilege
- Prompt injection from untrusted retrieved documents
- Poisoned ingestion content that manipulates downstream output
- Artifact generation that leaks secrets
- Sandbox command misuse or escape attempts
- Approval bypass for high-risk operations
- Admin privilege misuse without adequate oversight
- Missing audit events that prevent forensic validation

## Threat Categories
- Authorization and isolation failures
- Integrity compromise (ingestion/prompt/context)
- Confidentiality leakage (artifact/provider/cache)
- Execution safety failures (tool/sandbox/MCP)
- Governance and evidence failures (audit/approval/readiness)

## Mapping Basis
Primary mappings are aligned to Step 4 patch points and Step 6 risk/requirements catalogs for traceability.
