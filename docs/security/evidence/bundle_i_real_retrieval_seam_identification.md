# Bundle I Real Retrieval Seam Identification Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-i-real-retrieval-seam-identification` |
| Base branch | `main` |
| Bundle H dependency | `RETRIEVAL_ACL_LIVE_ADJACENT_SEAM_OBSERVATION_PROVEN_BY_CI` |

## Objective

Bundle I identifies the real Onyx retrieval seam that must remain stable before any live retrieval ACL patch is attempted.

This is seam identification and stability proof only.

It does not modify live Onyx behavior.

## Real candidate seam

```text
backend/onyx/context/search/pipeline.py
```

Function:

```text
search_pipeline
```

Primary retrieval call:

```text
retrieved_chunks = search_chunks(
```

Post-retrieval censoring path:

```text
fetch_ee_implementation_or_noop(
    "onyx.external_permissions.post_query_censoring",
    "_post_query_chunk_censoring",
    retrieved_chunks,
)
```

Return path:

```text
return censored_chunks
```

## Why this seam matters

The retrieval ACL runtime patch point should be considered after `search_chunks(...)` returns retrieved chunks and before downstream chunks can be returned to caller surfaces.

However, this bundle does not add that patch.

## Files added

```text
backend/security_layer/tests/test_retrieval_acl_real_seam_identification.py
.github/workflows/retrieval-acl-real-seam-identification-tests.yml
docs/security/evidence/bundle_i_real_retrieval_seam_identification.md
```

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_seam_identification.py -q
```

## Focused tests

The Bundle I tests cover:

- real Onyx search pipeline file exists;
- `search_pipeline` function exists;
- `retrieved_chunks = search_chunks(` call remains visible;
- post-query censoring path remains visible;
- `return censored_chunks` remains visible;
- evidence file preserves observation-only, no-live-patch boundaries.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_REAL_SEAM_IDENTIFIED_AND_STABLE_BY_CI
```

## What this proves

This proves the real candidate retrieval seam file/function/call/return path is visible and protected by a focused stability test.

## What this does not prove

This does **not** prove:

- live Onyx `search_pipeline` integration;
- live Onyx retrieval ACL enforcement;
- live runtime instrumentation;
- production retrieval security;
- enterprise readiness;
- live blocking;
- live filtering;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle I identifies the real candidate Onyx retrieval seam.
- Bundle I protects the seam location with focused CI tests.
- Bundle I is observation-only and does not modify live Onyx behavior.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live Onyx `search_pipeline` integration.
- Do not claim live retrieval enforcement.
- Do not claim live runtime instrumentation.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.

## Recommended next bundle

Bundle J should add a default-off no-op seam hook proposal around the identified `search_pipeline` area, with tests proving unchanged behavior in off mode before any shadow or enforce behavior is attempted in the real path.
