# Bundle L Real-Path Shadow Observation Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-l-real-path-shadow-observation` |
| Base branch | `main` |
| Bundle K dependency | `RETRIEVAL_ACL_REAL_SEARCH_PIPELINE_NOOP_HOOK_PATCH_PROVEN_BY_CI` |

## Objective

Bundle L adds real-path shadow-mode observation behind the existing retrieval ACL feature flag.

This is observation-only and behavior-preserving.

It does not filter, block, or enforce retrieval ACL.

## Patched helper

```text
backend/security_layer/retrieval_acl/noop_seam_hook.py
```

## Existing real path

The real Onyx `search_pipeline` return path already calls:

```python
return apply_retrieval_acl_search_pipeline_noop_hook(chunks=censored_chunks)
```

## Feature flag contract

```text
ONYX_SECURITY_RETRIEVAL_ACL_MODE=off|shadow|enforce
```

## Shadow behavior

When mode is `shadow`, the real-path hook:

- returns the same chunk list object unchanged;
- records observed chunk count;
- records returned chunk count;
- records `behavior_changed=False`;
- records no document content;
- records no sensitive metadata;
- does not filter chunks;
- does not block chunks;
- does not enforce retrieval ACL.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py backend/security_layer/tests/test_retrieval_acl_noop_seam_hook.py backend/security_layer/tests/test_retrieval_acl_real_search_pipeline_noop_hook.py -q
```

## Focused tests

The Bundle L tests cover:

- shadow mode records an observation without changing chunks;
- off mode records no shadow observation;
- invalid env values fail safe to off and record no observation;
- the apply hook still returns the same list in shadow mode;
- enforce mode remains no-op in Bundle L.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_REAL_PATH_SHADOW_OBSERVATION_PROVEN_BY_CI
```

## What this proves

This proves real-path shadow observation exists behind the existing feature flag and preserves returned chunk behavior.

## What this does not prove

This does **not** prove:

- live retrieval ACL enforcement;
- live retrieval filtering;
- live retrieval blocking;
- production retrieval security;
- enterprise readiness;
- enforce-mode behavior in the real path;
- staging validation;
- external validation;
- compliance certification.

## Safe claims

- Bundle L adds real-path shadow observation behind the existing feature flag.
- Bundle L preserves returned chunks in shadow mode.
- Bundle L does not filter, block, or enforce retrieval ACL.
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

Bundle M should add a real-path shadow observation evidence export or audit event adapter that remains redacted and behavior-preserving before any enforce-mode work is attempted.
