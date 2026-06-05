# Bundle K Real Search Pipeline No-Op Hook Patch Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-k-real-search-pipeline-noop-hook` |
| Base branch | `main` |
| Bundle J dependency | `RETRIEVAL_ACL_DEFAULT_OFF_NOOP_SEAM_HOOK_PROPOSAL_PROVEN_BY_CI` |

## Objective

Bundle K applies the default-off no-op retrieval ACL hook to the real Onyx `search_pipeline` return path.

This is a behavior-preserving no-op patch only.

It does not prove live retrieval enforcement.

## Patched file

```text
backend/onyx/context/search/pipeline.py
```

## Patch summary

Import added:

```python
from backend.security_layer.retrieval_acl.noop_seam_hook import (
    apply_retrieval_acl_search_pipeline_noop_hook,
)
```

Return path changed from:

```python
return censored_chunks
```

To:

```python
return apply_retrieval_acl_search_pipeline_noop_hook(chunks=censored_chunks)
```

## Why this is safe

The hook is behavior-preserving: it returns the same chunk list object unchanged.

Bundle K creates a real, narrow, testable call point in the Onyx retrieval path while preserving `NO-GO` production and enterprise readiness boundaries.

## Files added or modified

```text
backend/onyx/context/search/pipeline.py
backend/security_layer/tests/test_retrieval_acl_real_search_pipeline_noop_hook.py
.github/workflows/retrieval-acl-real-search-pipeline-noop-hook-tests.yml
docs/security/evidence/bundle_k_real_search_pipeline_noop_hook.md
```

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_search_pipeline_noop_hook.py backend/security_layer/tests/test_retrieval_acl_noop_seam_hook.py -q
```

## Focused tests

The Bundle K tests cover:

- real `search_pipeline` imports the no-op hook;
- real `search_pipeline` return path calls the no-op hook;
- original retrieval and post-query censoring paths remain visible;
- helper tests still prove no filtering, no blocking, and no enforcement;
- evidence preserves claim boundaries.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_REAL_SEARCH_PIPELINE_NOOP_HOOK_PATCH_PROVEN_BY_CI
```

## What this proves

This proves a real Onyx `search_pipeline` no-op hook patch exists and is protected by focused CI tests.

## What this does not prove

This does **not** prove:

- live retrieval ACL enforcement;
- live retrieval filtering;
- live retrieval blocking;
- production retrieval security;
- enterprise readiness;
- shadow-mode behavior in the real path;
- enforce-mode behavior in the real path;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle K adds a behavior-preserving no-op hook to the real Onyx `search_pipeline` return path.
- Bundle K creates a narrow real-path integration point for future shadow-mode work.
- Bundle K does not filter, block, or enforce retrieval ACL.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live retrieval enforcement.
- Do not claim live retrieval blocking.
- Do not claim live retrieval filtering.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim compliance certification.

## Recommended next bundle

Bundle L should add real-path shadow-mode observation behind the existing feature flag, while proving that returned chunks remain unchanged in shadow mode and that production readiness remains NO-GO.
