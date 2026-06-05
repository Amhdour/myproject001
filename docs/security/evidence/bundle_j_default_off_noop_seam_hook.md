# Bundle J Default-Off No-Op Seam Hook Proposal Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-j-default-off-noop-seam-hook` |
| Base branch | `main` |
| Bundle I dependency | `RETRIEVAL_ACL_REAL_SEAM_IDENTIFIED_AND_STABLE_BY_CI` |

## Objective

Bundle J adds a default-off no-op retrieval ACL seam hook helper and tests proving that the hook preserves chunk behavior.

This is a hook proposal and helper proof only.

It does not modify live Onyx `search_pipeline` behavior.

## Target seam

```text
backend/onyx/context/search/pipeline.py
```

Function:

```text
search_pipeline
```

Current return path:

```text
return censored_chunks
```

Future live-patch proposal:

```python
return apply_retrieval_acl_search_pipeline_noop_hook(chunks=censored_chunks)
```

The future patch must only be attempted in a dedicated PR after the no-op helper and tests pass.

## Files added

```text
backend/security_layer/retrieval_acl/noop_seam_hook.py
backend/security_layer/tests/test_retrieval_acl_noop_seam_hook.py
backend/security_layer/tests/test_retrieval_acl_noop_seam_hook_proposal.py
.github/workflows/retrieval-acl-noop-seam-hook-tests.yml
docs/security/evidence/bundle_j_default_off_noop_seam_hook.md
```

## Hook behavior

The no-op hook:

- accepts a list of chunks;
- returns the exact same list object;
- preserves ordering;
- records observation metadata through the observer helper;
- reads the existing feature flag contract;
- does not filter chunks;
- does not block chunks;
- does not enforce retrieval ACL;
- preserves `NO-GO` production and enterprise readiness boundaries.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_noop_seam_hook.py backend/security_layer/tests/test_retrieval_acl_noop_seam_hook_proposal.py -q
```

## Focused tests

The Bundle J tests cover:

- no-op hook returns the same list object in default-off mode;
- observation preserves default-off claim boundaries;
- shadow and enforce env values still do not filter in Bundle J;
- invalid env values fail safe to off;
- target `search_pipeline` seam remains visible;
- evidence preserves no-live-patch boundaries.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_DEFAULT_OFF_NOOP_SEAM_HOOK_PROPOSAL_PROVEN_BY_CI
```

## What this proves

This proves a default-off no-op hook helper exists and preserves chunk behavior.

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

- Bundle J provides a default-off no-op seam hook helper.
- Bundle J proves the helper preserves chunks without filtering or blocking.
- Bundle J keeps the real `search_pipeline` target seam visible.
- Bundle J does not modify live Onyx behavior.
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

Bundle K should apply the no-op hook to the real `search_pipeline` return path in a tiny patch, with tests proving unchanged behavior and preserving all NO-GO boundaries.
