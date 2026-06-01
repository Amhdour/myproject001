# CI Gate Results

## CI gate

`.github/workflows/runtime-retrieval-acl-security.yml`

## Scope

The CI gate is intentionally narrow. It runs:

```bash
PYTHONPATH=. python -m pytest backend/security_layer/runtime_enforcement/test_step63x_runtime_retrieval_acl_isolated.py -q
PYTHONPATH=. python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## What this proves when green

- The bounded runtime retrieval ACL helper tests pass without loading repo-wide `backend/tests/conftest.py`.
- The cross-tenant retrieval demo attack is blocked.
- The audit and telemetry helpers produce expected in-memory evidence.

## Oracle VPS local gate verification

- Host: `rag-agent-security-staging-v2`
- Branch: `step-63x-runtime-retrieval-acl-proof`
- Commit SHA: `96492e1c7e3930b26f9ff928f304f3f0452b6622`
- Environment: `.venv-step63x`
- Status: `ORACLE_STEP63X_ISOLATED_PYTEST_AND_DEMO_PASS`

## Oracle command run

```bash
PYTHONPATH=. python -m pytest backend/security_layer/runtime_enforcement/test_step63x_runtime_retrieval_acl_isolated.py -q
PYTHONPATH=. python demo_attacks/runtime_retrieval_acl_cross_tenant_attack.py
```

## Oracle result

```text
5 passed, 11 warnings in 0.31s
PASS: unauthorized cross-tenant retrieval was blocked.
decision=deny reason=retrieval_authorization_failed denied_chunk_count=1
audit_event=retrieval_authorization_failed telemetry=retrieval_acl_decision_total
```

## Warning note

The observed warnings were pytest configuration warnings about importing an optional `cryptography` warning-filter module in the minimal Oracle verification venv. They were not Step 63X assertion failures.

## GitHub Actions status

`PENDING_GITHUB_ACTIONS_RUN`

Update this file with the real GitHub Actions run URL and conclusion after the workflow runs.

## What this does not prove

- Full Onyx test suite success.
- Full staging deployment success.
- Full Onyx-wide runtime enforcement.
- Production readiness.
- Enterprise readiness.
- External validation.
- Compliance certification.
