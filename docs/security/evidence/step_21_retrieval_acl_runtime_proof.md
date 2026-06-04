# Step 21 — Retrieval ACL Runtime Proof

## What was added

- `backend/security_layer/retrieval_acl/models.py` defines minimal isolated ACL context, document ACL, retrieval chunk, denial, and decision models.
- `backend/security_layer/retrieval_acl/enforcer.py` filters retrieval chunks by tenant, authorized document ID, and document ACL subject/group match before returning allowed chunks.
- `backend/security_layer/retrieval_acl/audit.py` records in-memory audit events for denied or filtered runtime decisions.
- `backend/security_layer/retrieval_acl/README.md` documents the helper scope and claim boundary.
- `backend/security_layer/tests/test_retrieval_acl_runtime.py` proves same-tenant allow, same-tenant forbidden denial, cross-tenant denial, mixed-result filtering, missing-context denial, malformed-context denial, and audit emission.
- `.github/workflows/retrieval-acl-runtime-tests.yml` runs only the focused Step 21 retrieval ACL runtime tests and uploads test logs plus environment metadata.

## Exact test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_runtime.py -q
```

## Safe claims

- This step proves an isolated runtime retrieval ACL helper can deny or filter unauthorized retrieval chunks before returning them to its caller.
- This step proves cross-tenant chunks, unauthorized document IDs, and malformed/missing ACL context fail closed in focused tests.
- This step proves denied or filtered helper decisions create audit events in the isolated in-memory audit sink.
- After the focused CI workflow passes, the classification may be: `RETRIEVAL_ACL_RUNTIME_HELPER_PROVEN_BY_CI`.

## Forbidden claims

- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim full Onyx live retrieval enforcement.
- Do not claim all Onyx request paths use this helper.
- Do not claim this helper replaces existing production authorization controls.

## Readiness decision

- Production readiness: **NO-GO**.
- Enterprise readiness: **NO-GO**.

This step is intentionally isolated and unwired from live Onyx retrieval request paths.
