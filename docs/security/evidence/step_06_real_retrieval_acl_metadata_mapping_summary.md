# Step 06 — Real Retrieval ACL Metadata Mapping Summary

## What Changed

Step 06 adds a redacted metadata adapter for retrieval ACL enforcement decisions and routes enforce-hook decisions through it.

## Confirmed Behavior

- Off mode preserves returned chunks.
- Shadow mode preserves returned chunks.
- Enforce mode remains opt-in through `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.
- Realistic chunk-like objects with document metadata can be allowed or denied by tenant match.
- Missing tenant metadata fails closed in enforce mode.
- Decision records avoid chunk body, blurb, and context text.

## Known Limitations

- `InferenceChunk` has `document_id` and `metadata`, but no first-class `tenant_id` field was found.
- The inspected retrieval path does not prove tenant metadata is consistently present inside `InferenceChunk.metadata`.
- The adapter intentionally does not invent tenant metadata from request filters or document references.

## Readiness

- Production readiness: NO-GO.
- Enterprise readiness: NO-GO.
- Staging validation: not claimed.
- Safe to merge: only after required tests and claim-boundary checks pass in the target CI environment.
