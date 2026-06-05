# Retrieval ACL Enforcement v1 Runbook

## Scope

This runbook covers the first minimal Retrieval ACL Enforcement v1 portfolio proof.

It is not production readiness.
It is not enterprise readiness.
It is not compliance certification.
It is not full Onyx-wide authorization coverage.

## Modes

- `off`: return chunks unchanged.
- `shadow`: evaluate decisions but return chunks unchanged.
- `enforce`: remove unauthorized chunks.

## Enable enforce mode

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce
```

## Disable enforce mode

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off
```

## Expected enforce behavior

When enforce mode is enabled, the hook evaluates each retrieved chunk against the caller tenant context.

- Matching `tenant_id` and `user_tenant_id`: the chunk is returned.
- Cross-tenant `tenant_id`: the chunk is removed.
- Missing `user_tenant_id`, chunk `tenant_id`, or chunk `document_id`: the chunk is removed fail-closed.

## Audit-ready decision records

Each evaluated chunk produces a decision record with:

- allow or deny outcome;
- reason code such as `allowed`, `tenant_mismatch`, or `missing_acl_metadata`;
- mode;
- tenant identifiers needed to review the decision;
- redacted document reference only.

Decision records must not include document content or unredacted document identifiers.

## Validation

Run the focused unit test:

```bash
source .venv/bin/activate && PYTHONPATH=. pytest -q backend/security_layer/tests/test_retrieval_acl_enforce_hook.py
```

The validation is a technical-proof slice only. Passing this test does not establish production readiness, enterprise readiness, or compliance certification.
