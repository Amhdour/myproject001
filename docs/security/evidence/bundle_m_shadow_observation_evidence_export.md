# Bundle M Shadow Observation Evidence Export Proof

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-05T00:00:00Z |
| Branch name | `bundle-m-shadow-observation-evidence-export` |
| Base branch | `main` |
| Bundle L dependency | `RETRIEVAL_ACL_REAL_PATH_SHADOW_OBSERVATION_PROVEN_BY_CI` |

## Objective

Bundle M adds redacted evidence/audit-style export for real-path retrieval ACL shadow observations.

This is evidence export only.

It does not filter, block, or enforce retrieval ACL.

## Files added

```text
backend/security_layer/retrieval_acl/shadow_observation_export.py
backend/security_layer/tests/test_retrieval_acl_shadow_observation_export.py
.github/workflows/retrieval-acl-shadow-observation-export-tests.yml
docs/security/evidence/bundle_m_shadow_observation_evidence_export.md
```

## Export behavior

The export helper emits reviewer-safe evidence records containing:

- event type;
- UTC timestamp;
- mode;
- observed chunk count;
- returned chunk count;
- behavior-changed flag;
- redaction flags;
- readiness boundaries;
- live-claim booleans.

The export intentionally does **not** include:

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
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_shadow_observation_export.py backend/security_layer/tests/test_retrieval_acl_real_path_shadow_observation.py -q
```

## Focused tests

The Bundle M tests cover:

- shadow observation export is redacted and claim-bounded;
- exported dicts contain no sensitive field names;
- export is empty when no shadow observation exists;
- off mode produces no exported shadow observation.

## Safe classification after CI passes

```text
RETRIEVAL_ACL_SHADOW_OBSERVATION_EVIDENCE_EXPORT_PROVEN_BY_CI
```

## What this proves

This proves real-path retrieval ACL shadow observations can be exported as redacted evidence records.

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

- Bundle M exports redacted shadow-observation evidence records.
- Bundle M does not export document content, document IDs, user prompts, secrets, or PII.
- Bundle M remains behavior-preserving.
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

Bundle N should add a redacted audit event adapter for shadow observations and prove that audit records remain correlation-friendly without exposing sensitive retrieval data.
