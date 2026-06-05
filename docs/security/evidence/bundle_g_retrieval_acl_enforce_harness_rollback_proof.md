# Bundle G Retrieval ACL Enforce Harness and Rollback Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-g-enforce-harness-rollback-proof` |
| Base branch | `main` |
| Bundle F dependency | `RETRIEVAL_ACL_SHADOW_INTEGRATION_PROVEN_BY_CI` |

## Objective

Bundle G adds an isolated enforce-mode test harness and rollback-to-off verification proof for the retrieval ACL helper path.

It does not modify live Onyx `search_pipeline` behavior.

## Scope

Bundle G includes:

- isolated enforce-mode harness;
- rollback-to-off plan;
- rollback verification helper;
- focused tests;
- focused CI workflow;
- rollback runbook;
- evidence documentation.

## Files added

```text
backend/security_layer/retrieval_acl/enforce_harness.py
backend/security_layer/tests/test_retrieval_acl_enforce_harness.py
.github/workflows/retrieval-acl-enforce-harness-tests.yml
docs/security/runbooks/retrieval_acl_enforce_mode_rollback.md
docs/security/evidence/bundle_g_retrieval_acl_enforce_harness_rollback_proof.md
```

## Enforce harness behavior

The isolated enforce harness:

- reads the existing `ONYX_SECURITY_RETRIEVAL_ACL_MODE` feature flag contract;
- runs through the Bundle F isolated shadow integration wrapper;
- records observed document IDs;
- records returned document IDs;
- records denied document IDs;
- exposes a rollback-to-off plan when enforce mode is selected;
- preserves `NO-GO` production and enterprise readiness boundaries;
- does not claim live Onyx retrieval enforcement.

## Rollback behavior

Rollback is configuration-only:

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off
```

Rollback verification proves that, in the isolated helper path, restoring mode to `off` preserves the original retrieved chunks.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_harness.py -q
```

## Focused tests

The Bundle G tests cover:

- isolated enforce mode filters unauthorized chunks;
- off mode preserves chunks and requires no rollback;
- rollback-to-off preserves chunks after isolated enforce mode;
- invalid enforce env values fail safe to off.

## CI artifact

Workflow:

```text
.github/workflows/retrieval-acl-enforce-harness-tests.yml
```

Artifact name:

```text
retrieval-acl-enforce-harness-test-evidence
```

Artifact contents:

```text
retrieval-acl-enforce-harness-artifacts/environment_metadata.txt
retrieval-acl-enforce-harness-artifacts/test.log
```

## Safe classification after CI passes

```text
RETRIEVAL_ACL_ENFORCE_HARNESS_ROLLBACK_PROVEN_BY_CI
```

## What this proves

This proves an isolated enforce-mode harness and rollback-to-off verification path for the retrieval ACL helper.

## What this does not prove

This does **not** prove:

- live Onyx `search_pipeline` integration;
- live Onyx retrieval enforcement;
- live Onyx rollback;
- production retrieval security;
- enterprise readiness;
- live blocking;
- live filtering;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle G provides isolated retrieval ACL enforce-mode harness proof.
- Bundle G provides rollback-to-off verification proof.
- Invalid config values safely default to off.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx `search_pipeline` integration.
- Do not claim live Onyx retrieval enforcement.
- Do not claim live Onyx rollback.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.

## Recommended next bundle

Bundle H should add live-adjacent seam instrumentation in default-off mode, proving that the real retrieval path can be located and observed without changing live behavior.
