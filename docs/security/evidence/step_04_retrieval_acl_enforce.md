# Step 04 Retrieval ACL Enforcement Evidence

## Objective

Implement the first minimal Retrieval ACL Enforcement v1 vertical slice as a portfolio technical proof.

This evidence does not claim production readiness.
This evidence does not claim enterprise readiness.
This evidence does not claim compliance certification.

## Implemented slice

The slice adds an isolated enforcement hook for retrieved chunks. The hook is controlled by `ONYX_SECURITY_RETRIEVAL_ACL_MODE` and supports three modes:

- `off`: preserve existing off-mode behavior by returning chunks unchanged.
- `shadow`: preserve existing shadow-mode behavior by recording decisions while returning chunks unchanged.
- `enforce`: remove chunks that are unauthorized for the caller tenant.

## Enforcement rule

A chunk is allowed only when all required ACL metadata is present and the chunk tenant matches the caller tenant.

Required metadata:

- caller `user_tenant_id`;
- chunk `tenant_id`;
- chunk `document_id`.

Missing metadata fails closed with `missing_acl_metadata`.
Cross-tenant metadata fails closed with `tenant_mismatch`.

## Decision record redaction

Decision records include only the redacted document reference returned by the enforcement hook. They must not include retrieved content or unredacted document identifiers.

## Test evidence

Focused tests cover:

- off mode returns chunks unchanged;
- shadow mode records decisions and returns chunks unchanged;
- enforce mode removes cross-tenant chunks;
- enforce mode fails closed when ACL metadata is missing;
- a demo cross-tenant retrieval attack is blocked without leaking chunk content in the decision record.

## Boundary

This is a minimal portfolio proof slice only. It is not wired as an Onyx-wide authorization control, and it is not a complete retrieval security program.
