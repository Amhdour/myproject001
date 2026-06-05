# Retrieval ACL Real-Path Enforcement Runbook

## Purpose

This runbook explains how to exercise the Step 05 real search-pipeline retrieval ACL hook in a claim-bounded way.

The runbook is for portfolio technical-proof validation only. It does not claim production readiness, enterprise readiness, staging validation, or full Onyx-wide authorization coverage.

## Feature flag

Use `ONYX_SECURITY_RETRIEVAL_ACL_MODE` with one of:

- `off`
- `shadow`
- `enforce`

Unset or invalid values fail safe to `off`.

## Expected behavior

| Mode | Expected behavior |
| --- | --- |
| `off` | Return chunks unchanged through the existing no-op seam hook. |
| `shadow` | Return chunks unchanged and preserve the current reviewer-safe shadow observation behavior. |
| `enforce` | Call Retrieval ACL Enforcement v1 after post-query censoring and return only allowed chunks. Missing required metadata fails closed. |

## Exact real-path hook location

`backend/onyx/context/search/pipeline.py` calls `apply_retrieval_acl_real_path_enforcement_hook(...)` after `censored_chunks` and before `search_pipeline` returns.

## Focused validation commands

Run from the repository root:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_hook.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
PYTHONPATH=. python -m py_compile backend/security_layer/retrieval_acl/enforce_hook.py backend/onyx/context/search/pipeline.py
ruff check backend/security_layer/retrieval_acl/enforce_hook.py backend/security_layer/tests/test_retrieval_acl_enforce_hook.py
python scripts/portfolio/check_claim_boundary.py
```

## Known limitation

Real `InferenceChunk` tenant metadata mapping is incomplete in this slice. Do not treat enforce-mode success with fake chunks as full real Onyx enforcement.

## Safe rollback

Set:

```bash
ONYX_SECURITY_RETRIEVAL_ACL_MODE=off
```

`off` mode routes through the existing no-op seam hook and returns chunks unchanged.

## Do not claim

- Production readiness.
- Enterprise readiness.
- Staging validation.
- Full Onyx-wide authorization coverage.
- Full real Onyx enforcement.
- Compliance certification.
