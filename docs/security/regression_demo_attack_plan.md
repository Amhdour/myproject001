# Step 28X Regression + Demo Attack Plan

## Purpose

Create an isolated regression and synthetic demo-attack bundle that consolidates high-value security-layer regression coverage, local fixtures, local runner evidence, and partner-demo-ready summaries.

## Scope

This bundle is scoped to documentation, evidence, synthetic fixtures, isolated scenario definitions, an isolated local runner, and isolated tests. Implementation code is limited to `backend/security_layer/regression/`; tests are limited to `backend/security_layer/tests/`.

## Status

Status: isolated regression/demo bundle.

## Owner

Security engineering / application security evidence owner.

## Non-claim statement

This is not production readiness, not live enforcement, not staging attack execution, and not evidence that production traffic is protected by blocking or filtering. It is regression/demo evidence only.

## Relationship to control areas

- Retrieval security: exercises synthetic same-tenant, cross-tenant, stale ACL, and deleted-document regression cases without changing live retrieval behavior.
- Vector security: maps namespace and ACL metadata mismatch scenarios to existing vector controls without vector DB writes.
- Cache security: maps tenant collision and ACL version mismatch scenarios to isolated cache controls without production cache reads or writes.
- Tool authorization: maps unauthorized tool, approval-required, and prompt-to-tool abuse scenarios to isolated tool controls only.
- MCP hardening: maps unknown server, confused-deputy, and credential-boundary markers to isolated MCP controls only.
- Artifact safety: maps sensitive marker, unauthorized document marker, and prompt-injection marker scenarios to isolated artifact controls only.
- Monitor-only: proves no-block/no-filter behavior remains behavior-preserving in the isolated runner.
- Shadow-deny simulation: keeps simulated-deny evidence simulation-only with live effect `no_change`.
- Enforce-mode readiness: keeps activation blocked by missing gates and does not enable enforce runtime behavior.

## Synthetic fixture policy

All demo fixtures are synthetic. They use safe placeholders such as `tenant_alpha`, `tenant_beta`, `subject_demo`, `workspace_demo`, and `doc_hash_demo`. They store markers only and do not store raw prompt, document, chunk, secret, credential, customer, user, tenant, or source data.

## Forbidden real-data policy

Do not include real tenant IDs, customer names, user emails, document text, chunks, credentials, API keys, tokens, private keys, passwords, source internals, policy internals, or raw prompts in fixtures, scenario results, evidence, or summaries.

## Demo-attack taxonomy

| Family ID | Family | Purpose | Mapped controls | Mapped risks | Synthetic fixture requirement | Expected result | Evidence requirement | Current status |
|---|---|---|---|---|---|---|---|---|
| RDA-FAM-001 | Unauthorized retrieval | Demonstrate retrieval access checks using safe IDs. | retrieval_acl, monitor_only | R-RET-001 | same-tenant synthetic fixture | allowed/no change | scenario and runner summary | Implemented |
| RDA-FAM-002 | Cross-tenant retrieval | Demonstrate cross-tenant marker handling. | retrieval_acl, shadow_deny | R-RET-002, R-SD-001 | tenant_alpha requesting tenant_beta marker | simulated deny/no block | non-leaking result summary | Implemented |
| RDA-FAM-003 | Stale/deleted ACL retrieval | Demonstrate stale ACL and deleted-document markers. | retrieval_acl, safe_denial | R-RET-003, R-RET-004 | stale ACL/deleted marker fixtures | flagged | scenario coverage evidence | Implemented |
| RDA-FAM-004 | Vector metadata mismatch | Demonstrate namespace and ACL metadata mismatch markers. | vector_security | R-VEC-001, R-VEC-002 | vector namespace/ACL marker fixture | flagged | vector scenario evidence | Implemented |
| RDA-FAM-005 | Cache tenant/ACL collision | Demonstrate tenant and ACL cache collision markers. | cache_security, monitor_only | R-CACHE-001, R-CACHE-002 | cache key hash fixture | flagged/no block | cache fixture evidence | Implemented |
| RDA-FAM-006 | Unauthorized tool call | Demonstrate isolated unauthorized tool outcomes. | tool_authorization | R-TOOL-001 | synthetic tool safe name | flagged or isolated deny | tool scenario evidence | Implemented |
| RDA-FAM-007 | Prompt-to-tool abuse | Demonstrate prompt-to-tool injection marker detection. | tool_authorization, prompt_safety | R-TOOL-003 | marker only, no prompt text | flagged | non-leaking result summary | Implemented |
| RDA-FAM-008 | MCP confused-deputy attempt | Demonstrate confused-deputy marker handling. | mcp_hardening | R-MCP-002 | synthetic MCP server safe ID | flagged | MCP scenario evidence | Implemented |
| RDA-FAM-009 | MCP credential misuse | Demonstrate credential boundary marker handling. | mcp_hardening, credential_isolation | R-MCP-003 | redacted credential ref only | flagged | credential-boundary summary | Implemented |
| RDA-FAM-010 | Artifact secret leakage | Demonstrate artifact sensitive marker handling. | artifact_safety | R-ART-001 | sensitive marker only, no secret | flagged | artifact scenario evidence | Implemented |
| RDA-FAM-011 | Artifact unauthorized document leakage | Demonstrate unauthorized document marker handling. | artifact_safety, retrieval_acl | R-ART-002 | doc hash only | flagged | artifact scenario evidence | Implemented |
| RDA-FAM-012 | Shadow-deny simulated deny safety | Demonstrate simulated deny does not block. | shadow_deny, safe_denial | R-SD-001 | simulated marker fixture | simulated/no change | behavior-preservation evidence | Implemented |
| RDA-FAM-013 | Enforce-mode activation blocked by missing gates | Demonstrate readiness gates block activation. | enforce_mode_readiness | R-ENF-001 | missing-gate marker fixture | activation blocked/simulation only | enforce summary | Implemented |
| RDA-FAM-014 | Monitor-only no-block/no-filter behavior | Demonstrate monitor-only preserves behavior. | monitor_only | R-MON-001, R-MON-002 | no-block/no-filter markers | no change | behavior-preservation evidence | Implemented |
| RDA-FAM-015 | Safe denial non-leakage | Demonstrate sanitized denial summaries. | safe_denial, non_leakage | R-SAFE-001, R-SAFE-002 | safe denial marker only | flagged/non-leaking | non-leakage validation | Implemented |
| RDA-FAM-016 | Audit/finding/metric emission | Demonstrate expected evidence references. | audit_finding_metric | R-AUD-001 | audit/finding/metric marker | evidence emitted | runner evidence refs | Implemented |

## Regression test strategy

Focused pytest coverage validates dataclass creation, run summary creation, fixture creation, scenario uniqueness, scenario mappings, runner execution, outcome counts, non-leakage, disabled enforce mode, disabled shadow-deny runtime mode, disabled live blocking/filtering, and behavior preservation.

## Evidence requirements

Evidence must include prerequisite verification, plan summary, matrix summary, evidence standard summary, fixture coverage, scenario coverage, runner coverage, non-leakage validation, behavior-preservation validation, no-live-blocking validation, test output, test exit code, and remote-sync limitation when applicable.

## Partner-demo evidence boundary

Partner demos may present this as isolated regression/demo evidence only. They must not claim production readiness, live enforcement, staging attack execution, or production protection by blocking/filtering.

## Known limitations

The bundle is isolated only, synthetic only, not connected to staging, not tested under production load, and does not validate live traffic or live traces.

## Next recommended staging step

Run a separately approved staging-only demo attack execution plan with synthetic tenants and staging telemetry after explicit go/no-go approval.
