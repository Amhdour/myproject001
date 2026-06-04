# Step 41 Search Pipeline Seam Tests

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T18:38:00Z |
| Branch name | `step-41-search-pipeline-seam-tests` |
| Base branch | `main` |
| Starting commit SHA | `1980531cb46ff426b6851b81425b54cdc59cec26` |
| Step 40 dependency | `STEP_40_INTEGRATION_SAFETY_GATE_COMPLETE` |

## Objective

Step 41 adds source-level seam tests for the real Onyx search pipeline target identified in Step 40.

This step proves the seam is still structurally identifiable and ordered correctly without importing, mutating, or wiring live runtime behavior.

## Files added

```text
backend/security_layer/tests/test_retrieval_acl_search_pipeline_seam.py
.github/workflows/search-pipeline-seam-tests.yml
docs/security/evidence/step_41_search_pipeline_seam_tests.md
```

## File inspected by tests

```text
backend/onyx/context/search/pipeline.py
```

## Tested seam

```text
backend/onyx/context/search/pipeline.py::search_pipeline
after retrieved_chunks = search_chunks(...)
before fetch_ee_implementation_or_noop("onyx.external_permissions.post_query_censoring", ...)
before return censored_chunks
```

## Test behavior

The Step 41 tests assert that:

- `backend/onyx/context/search/pipeline.py` exists;
- `search_pipeline(...)` exists;
- `retrieved_chunks = search_chunks(...)` exists;
- post-query censoring hook exists;
- `chunks=retrieved_chunks` is passed to the censoring call;
- `return censored_chunks` exists;
- `search_chunks(...)` occurs before post-query censoring and return;
- `_build_index_filters(...)` still contains ACL and tenant filter construction anchors;
- the tests do not import live `search_pipeline` or require database/LLM/document-index dependencies.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_search_pipeline_seam.py -q
```

## CI artifact

Workflow:

```text
.github/workflows/search-pipeline-seam-tests.yml
```

Artifact name:

```text
search-pipeline-seam-test-evidence
```

Artifact contents:

```text
search-pipeline-seam-artifacts/environment_metadata.txt
search-pipeline-seam-artifacts/test.log
```

## Safe classification after CI passes

```text
SEARCH_PIPELINE_SEAM_TESTS_PROVEN_BY_CI
```

## What this proves

This proves the source-level post-`search_chunks` seam remains identifiable and correctly ordered for future feature-flagged integration work.

## What this does not prove

This does **not** prove:

- live Onyx retrieval enforcement;
- runtime behavior change;
- production retrieval security;
- enterprise readiness;
- live blocking;
- live filtering;
- full backend test success;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Step 41 provides source-level seam tests for the real Onyx search pipeline file.
- The target seam remains identifiable for future feature-flagged work.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx retrieval enforcement.
- Do not claim runtime integration.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim live blocking.
- Do not claim live filtering.

## Recommended next step

Step 42 should add off-by-default feature flag config proof for `ONYX_SECURITY_RETRIEVAL_ACL_MODE=off|shadow|enforce`, without wiring live behavior yet.
