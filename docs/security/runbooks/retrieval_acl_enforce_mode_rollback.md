# Retrieval ACL Enforce-Mode Rollback Runbook

## Scope

This runbook covers Bundle G isolated retrieval ACL enforce-mode harness rollback behavior.

It does not cover live Onyx operational rollback, production rollback, enterprise rollback, or compliance rollback.

## Feature flag

```text
ONYX_SECURITY_RETRIEVAL_ACL_MODE=off|shadow|enforce
```

## Safe default

```text
off
```

Missing, empty, or invalid values resolve to `off`.

## Rollback command

```bash
export ONYX_SECURITY_RETRIEVAL_ACL_MODE=off
```

## Verification command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_enforce_harness.py -q
```

## Expected rollback behavior

1. Enforce-mode harness filters unauthorized chunks in isolation.
2. Rollback restores mode to `off`.
3. Off mode preserves the original retrieved chunks.
4. No live Onyx retrieval behavior is claimed as changed.
5. No live Onyx rollback behavior is claimed as proven.

## Required evidence before any stronger claim

- CI run for `Retrieval ACL Enforce Harness Tests` passes.
- Artifact `retrieval-acl-enforce-harness-test-evidence` exists.
- Test log shows Bundle G tests passed.
- Evidence file preserves production and enterprise NO-GO boundaries.

## Safe claims

- Isolated enforce-mode harness exists.
- Isolated rollback-to-off verification exists.
- Invalid config safely defaults to off.
- Production readiness remains NO-GO.
- Enterprise readiness remains NO-GO.

## Forbidden claims

- Do not claim live Onyx retrieval enforcement.
- Do not claim live Onyx rollback.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim production retrieval security.
- Do not claim enterprise readiness.
- Do not claim compliance certification.
