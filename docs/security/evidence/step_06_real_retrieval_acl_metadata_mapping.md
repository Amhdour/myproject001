# Step 06 — Real Retrieval ACL Metadata Mapping Evidence

## Scope

This step maps real retrieval chunk-like metadata into the Retrieval ACL Enforcement v1 decision input. It does not claim full Onyx-wide authorization. It does not claim staging validation.

## Implementation Evidence

- Added `backend/security_layer/retrieval_acl/metadata_adapter.py` as the small adapter for redacted metadata extraction.
- Updated `backend/security_layer/retrieval_acl/enforce_hook.py` so decisions are built from adapter output instead of test-only direct field reads.
- Preserved off mode behavior: returned chunk lists are not filtered.
- Preserved shadow mode behavior: returned chunk lists are not filtered.
- Enforce mode remains gated behind `ONYX_SECURITY_RETRIEVAL_ACL_MODE=enforce`.

## Metadata Fields Discovered

From repository inspection:

- `InferenceChunk.document_id` exists and is available on real retrieval chunks.
- `InferenceChunk.metadata` exists as a document metadata mapping.
- `InferenceChunk.file_id` exists after a post-retrieval lookup, but it is not tenant metadata.
- `IndexFilters.tenant_id` exists on retrieval filters and is populated from current tenant context in multitenant mode.
- `TenantState.tenant_id` exists for document index instances.
- `DocMetadataAwareIndexChunk.tenant_id` exists during indexing.

## Metadata Fields Missing

- `InferenceChunk` does not define a first-class `tenant_id` field.
- The inspected real retrieval path does not prove that `InferenceChunk.metadata` always contains a tenant key.
- The adapter does not invent tenant metadata. If chunk tenant metadata is absent, the adapter reports `missing_chunk_tenant_id`.
- In non-multitenant mode, `user_tenant_id` can be absent because the pipeline passes `None`; enforce mode therefore fails closed for tenant-boundary decisions without a user tenant.

## Enforcement Boundary

- Metadata present and tenant matches: allow.
- Metadata present and tenant mismatches: deny.
- Metadata missing in enforce mode: fail closed.
- Metadata missing in off or shadow mode: preserve returned chunks while decision records mark the missing metadata boundary.
- Decision records use redacted document references and do not include chunk text fields.

## Readiness Boundary

- Production readiness: NO-GO.
- Enterprise readiness: NO-GO.
- Staging validation: not claimed.
- Full Onyx-wide authorization: not claimed.
