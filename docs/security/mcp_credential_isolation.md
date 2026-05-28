# MCP Credential Isolation (Planned)

- MCP credential types: user token, service account credential, delegated credential, ephemeral session handle.
- raw credential non-exposure rule: never log/store/emit raw secrets in policy, denial, audit, or finding payloads.
- tenant credential boundary: credentials scoped to single tenant; cross-tenant use denied/flagged.
- user credential boundary: user credentials bound to subject identity and permission set.
- service credential boundary: service credentials constrained to registry-allowed MCP actions only.
- delegated credential boundary: delegated credentials must retain original delegator/delegatee scope chain.
- credential scope validation: validate tenant/workspace/server/tool/resource bounds per registry.
- credential lifetime validation: enforce issued_at/expires_at freshness and revocation status.
- credential rotation assumptions: rotation cadence managed externally; stale credentials flagged.
- credential audit expectations: credential class/handle usage events audited per request.
- credential denial behavior: safe-denial without revealing secret material or internal keys.
- known limitations: design-only, no live credential isolation implementation yet.

## Step 22B Update (2026-05-28)
Implemented minimal isolated MCP hardening helpers/tests only; no live MCP/tool/agent integration and no production enforcement activation.
