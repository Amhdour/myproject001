# Step 07 — Real-Path Enforce Mode With Mapped Metadata Evidence

## Scope

This step adds mapped-metadata real-path enforcement tests for Retrieval ACL Enforcement v1.

This is a production-style portfolio proof only.

It does not claim production readiness, enterprise readiness, staging validation, compliance certification, or full Onyx-wide authorization coverage.

## Files added

- `backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py`
- `docs/security/evidence/step_07_real_path_enforce_mapped_metadata.md`
- `docs/security/evidence/step_07_real_path_enforce_mapped_metadata_summary.md`
- `docs/security/runbooks/retrieval_acl_real_path_mapped_metadata_runbook.md`

## Control behavior covered

- Matching tenant metadata is allowed in enforce mode.
- Cross-tenant mapped metadata is denied in enforce mode.
- Missing chunk tenant metadata fails closed in enforce mode.
- Missing caller tenant metadata fails closed in enforce mode.
- Off mode preserves chunks.
- Shadow mode preserves chunks while recording decision boundaries.
- Decision records do not include chunk text.

## Demo attack

Attack:

- caller tenant: `tenant-a`
- retrieved chunk tenant: `tenant-b`
- mode: `enforce`

Expected result:

- chunk removed
- denial decision recorded
- chunk content absent from decision record
- production readiness remains `NO-GO`
- enterprise readiness remains `NO-GO`

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_retrieval_acl_real_path_mapped_metadata.py -q
```

## Real-path metadata limitation

The current evidence depends on metadata fields that the adapter can read from real retrieval chunk-like objects: `document_id` and a tenant value inside `metadata` such as `tenant_id`.

Repository evidence from Step 06 found that real `InferenceChunk` has `document_id` and `metadata`, but it did not prove that every real `InferenceChunk.metadata` contains tenant metadata. This step therefore treats missing chunk tenant metadata as an enforce-mode fail-closed condition rather than inventing a tenant value from other request state.

## Claim boundary

- Production readiness: `NO-GO`.
- Enterprise readiness: `NO-GO`.
- Staging validation: not claimed.
- Full Onyx-wide authorization: not claimed.
- Enforcement remains limited to Retrieval ACL Enforcement v1 behavior exercised by this test slice.
