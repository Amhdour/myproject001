# CI Gate Results

## CI gate

`.github/workflows/runtime-retrieval-acl-security.yml`

## Scope

The CI gate is intentionally narrow. It runs:

```bash
python -m pytest backend/tests/security_layer/test_runtime_retrieval_acl_step_63x.py -q
python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## What this proves when green

- The bounded runtime retrieval ACL helper tests pass.
- The cross-tenant retrieval demo attack is blocked.
- The audit and telemetry helpers produce expected in-memory evidence.

## What this does not prove

- Full Onyx test suite success.
- Full staging deployment success.
- Full Onyx-wide runtime enforcement.
- Production readiness.
- Enterprise readiness.

## Current status

`PENDING_GITHUB_ACTIONS_RUN`

Update this file with the real GitHub Actions run URL and conclusion after the workflow runs.
