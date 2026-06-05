# Retrieval ACL Shadow Observation Non-Production Runbook

## Scope

This runbook explains how an operator can enable retrieval ACL shadow observation in a non-production environment and collect redacted evidence artifacts.

This runbook does not enable production enforcement.

This runbook does not claim production readiness, enterprise readiness, live blocking, live filtering, or compliance certification.

## Preconditions

- Use a non-production environment only.
- Confirm the current code includes the real `search_pipeline` no-op hook.
- Confirm the shadow observation, evidence export, audit adapter, retention policy, and evidence-chain tests pass in CI.
- Confirm no secrets, credentials, document content, document IDs, or user prompts are copied into evidence artifacts.

## Feature flag

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=shadow
```

## Safe rollback

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off
```

## Verification commands

```bash
PYTHONPATH=. python -m pytest \
  backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py \
  backend/security_layer/tests/test_retrieval_acl_shadow_observation_export.py \
  backend/security_layer/tests/test_retrieval_acl_shadow_observation_audit.py \
  backend/security_layer/tests/test_retrieval_acl_shadow_observation_retention.py \
  -q
```

## Evidence to collect

Collect only redacted artifacts:

- CI workflow status for shadow observation tests.
- CI workflow status for evidence export tests.
- CI workflow status for audit adapter tests.
- CI workflow status for retention policy tests.
- Redacted event counts.
- Redacted returned-count versus observed-count comparison.
- Claim-boundary confirmation.

## Evidence not allowed

Do not collect:

- document content;
- document IDs;
- chunk text;
- user prompts;
- credentials;
- secrets;
- API keys;
- PII;
- customer data;
- production data.

## Go/no-go rules

### Go for non-production shadow observation only

All must be true:

- Mode is `shadow`.
- Returned chunks remain unchanged.
- Redacted audit/evidence records are produced.
- Retention policy accepts only redacted audit events.
- CI is green.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

### No-go

Any of the following means no-go:

- Mode is `enforce`.
- Returned chunks change.
- Any document content appears in evidence.
- Any document ID appears in evidence.
- Any user prompt appears in evidence.
- Any secret, credential, API key, or PII appears in evidence.
- Any production-readiness or enterprise-readiness claim appears.

## Safe claims

- Non-production shadow observation can be enabled with a feature flag.
- Returned chunks remain unchanged in the tested shadow-observation path.
- Redacted evidence, audit, and retention records can be generated.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim live retrieval enforcement.
- Do not claim live retrieval filtering.
- Do not claim live retrieval blocking.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim compliance certification.

## Rollback confirmation

After rollback to `off`, confirm that no shadow observations are produced in the focused tests.

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
```
