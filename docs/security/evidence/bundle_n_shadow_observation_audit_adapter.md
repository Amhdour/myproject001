# Bundle N Shadow Observation Audit Adapter Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-n-shadow-observation-audit-adapter` |
| Base branch | `main` |
| Bundle M dependency | `RETRIEVAL_ACL_SHADOW_OBSERVATION_EVIDENCE_EXPORT_PROVEN_BY_CI` |

## Objective

Bundle N adds a redacted audit-event adapter for real-path retrieval ACL shadow observations.

This is audit-event adaptation only.

It does not filter, block, or enforce retrieval ACL.

## Files added

```text
backend/security_layer/retrieval_acl/shadow_observation_audit.py
backend/security_layer/tests/test_retrieval_acl_shadow_observation_audit.py
.github/workflows/retrieval-acl-shadow-observation-audit-tests.yml
docs/security/evidence/bundle_n_shadow_observation_audit_adapter.md
```

## Audit behavior

The audit adapter emits correlation-friendly redacted audit events containing:

- event type;
- request ID;
- pipeline stage;
- UTC timestamp;
- mode;
- observed chunk count;
- returned chunk count;
- behavior-changed flag;
- redaction flags;
- readiness boundaries;
- live-claim booleans.

The audit event intentionally does **not** include:

- chunk text;
- document IDs;
- document content;
- document metadata;
- user prompts;
- credentials;
- secrets;
- PII.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_shadow_observation_audit.py backend/security_layer/tests/test_retrieval_acl_shadow_observation_export.py -q
```

## Focused tests

The Bundle N tests cover:

- audit events are redacted and correlation-friendly;
- audit dictionaries contain no sensitive field names;
- audit export is empty when no shadow observation exists;
- off mode produces no shadow audit event.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_SHADOW_OBSERVATION_AUDIT_ADAPTER_PROVEN_BY_CI
```

## What this proves

This proves real-path retrieval ACL shadow observations can be adapted into redacted audit-style events.

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

- Bundle N exports redacted audit events from shadow observations.
- Bundle N supports request-level correlation without exposing retrieval content.
- Bundle N does not export document content, document IDs, user prompts, secrets, credentials, or PII.
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

Bundle O should add a bounded retention and redaction policy test for shadow-observation audit events before any enforce-mode implementation is attempted.
