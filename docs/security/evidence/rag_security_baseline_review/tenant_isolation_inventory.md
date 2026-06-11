# Tenant Isolation Inventory

## Purpose
Assess repository evidence for preventing cross-tenant retrieval.

## Commands or search methods used
- `rg -n -i "tenant|cross_tenant|tenant_id" backend docs .github`
- Direct inspection of contextvars, DB tenant mapping models, search filters, Vespa filter builders, retrieval guard, and demo attack tests.

## Files found
- `backend/onyx/db/models.py`
- `backend/onyx/db/engine/tenant_utils.py`
- `backend/onyx/db/engine/sql_engine.py`
- `backend/onyx/context/search/pipeline.py`
- `backend/onyx/document_index/vespa/shared_utils/vespa_request_builders.py`
- `backend/onyx/document_index/vespa/chunk_retrieval.py`
- `backend/onyx/security_layer/retrieval_guard/guard.py`
- `backend/tests/security/demo_attacks/test_cross_tenant_retrieval_attack.py`
- `.github/workflows/security-readiness.yml`

## Relevant code paths found
- `UserTenantMapping` maps user emails to tenant IDs.
- `search_pipeline` sets `IndexFilters.tenant_id` from current tenant when multi-tenant mode is enabled.
- Vespa filter construction adds tenant filtering when `MULTI_TENANT` and `filters.tenant_id` are set.
- Vespa visit API retrieval rejects missing tenant ID in multi-tenant mode and skips documents whose stored tenant differs.
- Retrieval guard classifies tenant mismatches as `ACLState.CROSS_TENANT`.

## Findings
- Code evidence exists for tenant-scoped search filters and post-retrieval cross-tenant checks.
- A demo attack test exists for cross-tenant retrieval in the separate `backend/tests/security` security-enforcer path.

## Gaps
- This review did not execute a multi-tenant live retrieval against Vespa/Postgres.
- CI workflow presence was found, but local repository evidence did not include CI pass results.
- Tenant isolation is not proven for every code path, connector, federated source, or deployment mode.

## Claim boundary
Tenant-isolation controls are partially evidenced by code and isolated tests; full cross-tenant prevention is not proven.
