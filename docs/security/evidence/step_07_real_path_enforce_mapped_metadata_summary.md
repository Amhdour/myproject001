# Step 07 — Real-Path Enforce Mode With Mapped Metadata Summary

## What changed

Step 07 adds a mapped-metadata real-path test slice for Retrieval ACL Enforcement v1. The tests use a realistic chunk shape with `document_id`, `metadata`, and `content`, then verify that enforcement decisions are made from mapped metadata without leaking chunk text into decision records.

## Behavior proven by tests

- Enforce mode allows a chunk when caller tenant metadata matches chunk tenant metadata.
- Enforce mode denies a chunk when mapped chunk tenant metadata belongs to a different tenant.
- Enforce mode fails closed when chunk tenant metadata is missing.
- Enforce mode fails closed when caller tenant metadata is missing.
- Off mode preserves returned chunks, including cross-tenant-looking metadata.
- Shadow mode preserves returned chunks while recording the denial boundary.
- Decision records do not include chunk content strings.

## Demo attack result

A caller from `tenant-a` receives a realistic retrieval chunk mapped to `tenant-b`. With `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`, the hook removes the chunk, records a denial decision, and keeps the tenant B chunk text out of the decision record.

## Known limitation

Real `InferenceChunk` tenant metadata remains incomplete as a guarantee. Step 06 found `InferenceChunk.document_id` and `InferenceChunk.metadata`, but did not prove that tenant metadata is always present inside `InferenceChunk.metadata`. This step does not invent that metadata. Missing tenant metadata remains a fail-closed condition in enforce mode.

## Claim boundary

- Production readiness: `NO-GO`.
- Enterprise readiness: `NO-GO`.
- Staging validation: not claimed.
- Full Onyx-wide authorization: not claimed.
- This is evidence for the Retrieval ACL Enforcement v1 test slice only.
