# Vector DB Metadata Contract (Step 19A)

Status: planned/design only.

| Field Name | Purpose | Required/Optional | Allowed Type | Forbidden Content | Validation Rule | Mapped Tests | Implementation Status |
|---|---|---|---|---|---|---|---|
| tenant_id_hash_or_safe_id | tenant scope without raw secret id leakage | required | string | raw tenant secret, email, token | non-empty safe/hash format | VEC-TST-003, VEC-TST-012 | planned |
| workspace_id_hash_or_safe_id | workspace scope binding | required | string | raw secrets/PII | non-empty safe/hash format | VEC-TST-003, VEC-TST-012 | planned |
| document_id_hash_or_safe_id | document lineage binding | required | string | full document path/secret ids | non-empty safe/hash format | VEC-TST-013, VEC-TST-026 | planned |
| chunk_id_hash_or_safe_id | chunk lineage binding | required | string | raw content fragments | non-empty safe/hash format | VEC-TST-013, VEC-TST-026 | planned |
| source_type | source classifier for policy and drift logic | required | enum/string | executable payloads, freeform secrets | value in approved source-type allowlist | VEC-TST-006 | planned |
| source_id_hash_or_safe_id | source-safe identifier | required | string | raw connector secrets | non-empty safe/hash format | VEC-TST-006, VEC-TST-026 | planned |
| acl_snapshot_id | ACL snapshot linkage | required | string | raw ACL payload | UUID/safe id format | VEC-TST-004, VEC-TST-019 | planned |
| acl_snapshot_version | ACL snapshot versioning | required | integer/string | negative values, freeform blobs | parseable numeric or semver-safe | VEC-TST-004, VEC-TST-005 | planned |
| acl_snapshot_created_at | ACL snapshot issuance time | required | datetime string | non-date arbitrary text | RFC3339 timestamp parse | VEC-TST-005 | planned |
| acl_snapshot_expires_at | ACL snapshot expiry time | required | datetime string | non-date arbitrary text | RFC3339 timestamp parse and not expired at write | VEC-TST-005 | planned |
| document_deleted | deleted marker for candidate handling | required | boolean | non-boolean values | strict boolean | VEC-TST-015 | planned |
| document_stale | stale marker for candidate handling | required | boolean | non-boolean values | strict boolean | VEC-TST-016 | planned |
| provenance_id | provenance chain id | required | string | raw secret URLs/tokens | non-empty safe id format | VEC-TST-006, VEC-TST-019 | planned |
| ingestion_run_id | ingestion run lineage | required | string | shell command fragments/secrets | non-empty safe id format | VEC-TST-006 | planned |
| embedding_model_id | embedding model traceability | required | string | API keys/provider secrets | allowlisted model identifier format | VEC-TST-019 | planned |
| embedding_created_at | embedding creation timestamp | required | datetime string | non-date arbitrary text | RFC3339 timestamp parse | VEC-TST-019 | planned |
| content_type | content class for policy branching | optional | enum/string | executable code blobs as identifier | optional allowlisted content type | VEC-TST-007 | planned |
| sensitivity_label_placeholder | future sensitivity classification slot | optional | string | raw classified payload | optional label allowlist | VEC-TST-007 | planned |
| prompt_injection_flag | marker propagated from ingestion checks | required | boolean | non-boolean values | strict boolean; true must be preserved | VEC-TST-009 | planned |
| poisoning_flag | poisoning/anomaly marker | required | boolean | non-boolean values | strict boolean; true must be preserved | VEC-TST-008 | planned |
| metadata_schema_version | contract versioning | required | string | invalid/empty version | semver-style string required | VEC-TST-007 | planned |

## Step 19B Implementation Update (2026-05-27)
- Implemented isolated metadata contract helpers in `backend/security_layer/vector/metadata_contract.py`.
- Added required 21-field schema validation, schema version validation, forbidden key/value pattern checks, and metadata sanitization/build helper.

## Step 19C Metadata Validation Status (2026-05-27)
- Required metadata field coverage validated end-to-end in isolated tests.
- Forbidden metadata keys and forbidden value content patterns validated as reject paths.
- Schema version enforcement validated.
- Sanitization behavior validated to keep metadata safe/non-raw.
