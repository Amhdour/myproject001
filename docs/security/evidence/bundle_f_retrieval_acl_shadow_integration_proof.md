# Bundle F Retrieval ACL Shadow Integration Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T18:58:00Z |
| Branch name | `bundle-f-retrieval-acl-shadow-integration-proof` |
| Base branch | `main` |
| Starting commit SHA | `309e7c30cfde8eaafbb1e3ace70b068ecbec1dec` |
| Step 41 dependency | `SEARCH_PIPELINE_SEAM_TESTS_PROVEN_BY_CI` |

## Objective

Bundle F accelerates the Phase 3 feature-flag and shadow-integration proof work.

This bundle adds an off-by-default retrieval ACL integration configuration helper, an isolated config-driven shadow integration wrapper, focused tests, CI artifact upload, and evidence documentation.

It does not modify live Onyx `search_pipeline` behavior.

## Accelerated scope

Bundle F combines:

- Step 42 — Retrieval ACL feature flag config;
- Step 43 — Shadow-mode search-pipeline integration proof;
- Step 44 — Shadow-mode integration tests.

## Files added

```text
backend/security_layer/retrieval_acl/integration_config.py
backend/security_layer/retrieval_acl/shadow_integration.py
backend/security_layer/tests/test_retrieval_acl_shadow_integration.py
.github/workflows/retrieval-acl-shadow-integration-tests.yml
docs/security/evidence/bundle_f_retrieval_acl_shadow_integration_proof.md
```

## Feature flag contract

```text
ONYX_SECURITY_RETRIEVAL_ACL_MODE=off|shadow|enforce
```

Default behavior:

```text
off
```

Unsupported, empty, or missing values resolve to:

```text
off
```

## Integration wrapper behavior

The isolated shadow integration wrapper:

- reads the feature flag from an explicit env mapping or process environment;
- defaults to `off` when missing or invalid;
- delegates to the existing isolated search-pipeline gate proof;
- preserves chunks and records no ACL decision in `off` mode;
- preserves chunks and records would-filter evidence in `shadow` mode;
- filters only through the isolated gate in explicit `enforce` mode;
- does not modify live Onyx `search_pipeline` behavior.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_shadow_integration.py -q
```

## Focused tests

The Bundle F tests cover:

- missing env defaults to `off`;
- invalid env defaults to `off`;
- `off` mode preserves chunks and records no ACL decision;
- `shadow` mode preserves chunks and records would-filter evidence;
- explicit config can select shadow mode;
- explicit `enforce` mode filters through the isolated gate only.

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-shadow-integration-tests.yml
```

Artifact name:

```text
retrieval-acl-shadow-integration-test-evidence
```

Artifact contents:

```text
retrieval-acl-shadow-integration-artifacts/environment_metadata.txt
retrieval-acl-shadow-integration-artifacts/test.log
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_SHADOW_INTEGRATION_PROVEN_BY_CI
```

## What this proves

This proves the Phase 3 off-by-default feature flag contract and isolated config-driven retrieval ACL shadow integration behavior.

## What this does not prove

This does **not** prove:

- live Onyx `search_pipeline` integration;
- live Onyx retrieval enforcement;
- production retrieval security;
- enterprise readiness;
- live blocking;
- live filtering;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle F provides off-by-default retrieval ACL integration configuration proof.
- Bundle F provides isolated shadow integration proof.
- `off`, `shadow`, and explicit isolated `enforce` behavior are tested.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx `search_pipeline` integration.
- Do not claim live Onyx retrieval enforcement.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.

## Recommended next bundle

Bundle G should add the explicit enforce-mode test harness and rollback/runbook evidence before any real live-adjacent runtime integration claim is considered.
