# Bundle O Shadow Observation Retention Policy Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-o-shadow-observation-retention-policy` |
| Base branch | `main` |
| Bundle N dependency | `RETRIEVAL_ACL_SHADOW_OBSERVATION_AUDIT_ADAPTER_PROVEN_BY_CI` |

## Objective

Bundle O adds bounded retention and redaction policy decisions for redacted retrieval ACL shadow-observation audit events.

This is retention-policy proof only.

It does not filter, block, or enforce retrieval ACL.

## Files added

```text
backend/security_layer/retrieval_acl/shadow_observation_retention.py
backend/security_layer/tests/test_retrieval_acl_shadow_observation_retention.py
.github/workflows/retrieval-acl-shadow-observation-retention-tests.yml
docs/security/evidence/bundle_o_shadow_observation_retention_policy.md
```

## Policy behavior

The retention policy:

- defaults to 30 days;
- requires redacted audit events;
- rejects events containing document content;
- rejects events containing document IDs;
- rejects events containing user prompts;
- preserves production and enterprise `NO-GO` boundaries;
- preserves no-filtering, no-blocking, and no-enforcement claim boundaries.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_shadow_observation_retention.py backend/security_layer/tests/test_retrieval_acl_shadow_observation_audit.py -q
```

## Focused tests

The Bundle O tests cover:

- redacted shadow audit events are eligible for bounded retention;
- unredacted audit events are rejected;
- events with document content or document IDs are rejected;
- retention decision dictionaries contain no sensitive field names;
- empty audit event inputs produce empty decisions.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_SHADOW_OBSERVATION_RETENTION_POLICY_PROVEN_BY_CI
```

## What this proves

This proves redacted shadow-observation audit events can receive bounded retention decisions without storing retrieval content.

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

- Bundle O adds bounded retention policy decisions for redacted shadow-observation audit events.
- Bundle O rejects unredacted or sensitive audit events.
- Bundle O does not export document content, document IDs, user prompts, secrets, credentials, or PII.
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

Bundle P should add a reviewer-facing evidence summary that links real-path shadow observation, export, audit, and retention proofs into one claim-bounded evidence chain.
