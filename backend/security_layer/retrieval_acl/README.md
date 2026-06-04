# Retrieval ACL Runtime Helper Proof

This package is an isolated Step 21 runtime-security proof helper. It filters
retrieval chunks before return using only a minimal requester ACL context and
per-result document ACL metadata.

## What it proves

- Same-tenant chunks whose document IDs and document ACLs match the requester are allowed.
- Cross-tenant chunks are denied.
- Chunks for document IDs outside the requester context are denied.
- Mixed retrieval result sets are filtered so only authorized chunks remain.
- Missing or malformed ACL context fails closed.
- Denied or filtered decisions emit an in-memory audit event for test evidence.

## Claim boundary

This package does **not** claim production readiness, enterprise readiness, or
full Onyx live retrieval enforcement. It is intentionally not wired into live
Onyx request paths in this step.

## Focused test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_runtime.py -q
```
