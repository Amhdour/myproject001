# Cache Key Contract (Step 20A)

Status: planned/design-only.

| Field Name | Purpose | Required/Optional | Allowed Type | Forbidden Content | Validation Rule | Mapped Tests | Implementation Status |
|---|---|---|---|---|---|---|---|
| cache_key_schema_version | schema compatibility | required | string | runtime secrets | semantic version pattern | CACHE-001 | planned |
| tenant_id_hash_or_safe_id | tenant bind | required | string | raw tenant secret/internals | non-empty safe/hash id | CACHE-001,CACHE-005 | planned |
| workspace_id_hash_or_safe_id | workspace bind | optional | string | raw internal topology | safe/hash id only | CACHE-005 | planned |
| subject_id_hash_or_safe_id | subject bind | required | string | PII raw identifier | safe/hash id only | CACHE-002,CACHE-006 | planned |
| subject_group_hashes_or_safe_ids | group authorization bind | optional | array[string] | raw group secrets | normalized unique list | CACHE-007 | planned |
| subject_role_hashes_or_safe_ids | role authorization bind | optional | array[string] | raw role internals | normalized unique list | CACHE-008 | planned |
| acl_snapshot_id | ACL version bind | required | string | raw ACL payload | non-empty opaque id | CACHE-003,CACHE-009 | planned |
| acl_snapshot_version | ACL revision bind | required | integer/string | negative/invalid | monotonic/coercible version | CACHE-009,CACHE-013 | planned |
| acl_snapshot_expires_at | ACL freshness | required | RFC3339 timestamp | no timestamp | must be parseable future/valid | CACHE-009 | planned |
| provenance_id | provenance binding | required | string | raw source secret | non-empty opaque id | CACHE-004 | planned |
| retrieval_scope_hash | retrieval scope bind | optional | string | raw query params | fixed-length hash/safe id | CACHE-013 | planned |
| vector_namespace_hash | vector namespace bind | optional | string | raw namespace secret | fixed-length hash/safe id | CACHE-012 | planned |
| source_type | source classifier | optional | string enum | arbitrary executable payload | allowlist enum | CACHE-019 | planned |
| source_id_hash_or_safe_id | source bind | optional | string | connector secrets | safe/hash id only | CACHE-019 | planned |
| document_id_hash_or_safe_id | document bind | optional | string | raw document path/secret | safe/hash id only | CACHE-010,CACHE-027 | planned |
| chunk_id_hash_or_safe_id | chunk bind | optional | string | raw chunk content | safe/hash id only | CACHE-014,CACHE-027 | planned |
| query_hash | query identity | optional | string | raw query text | fixed-length hash | CACHE-015 | planned |
| prompt_context_hash | prompt context identity | optional | string | raw prompt text | fixed-length hash | CACHE-014,CACHE-015 | planned |
| cache_purpose | cache type purpose | required | string enum | unknown purpose | allowlist: retrieval/vector/prompt_context/answer/tool_result | CACHE-016 | planned |
| cache_ttl_seconds | TTL policy | required | integer | negative/excessive TTL | >0 and <= policy max | CACHE-009,CACHE-010 | planned |
| sensitivity_label_placeholder | safe sensitivity marker | optional | string enum | raw sensitive values | placeholder enum only | CACHE-019,CACHE-027 | planned |

## Step 20B Contract Helper Status
- Isolated cache-key contract helpers implemented (`build_safe_cache_key`, schema validation, forbidden-content validation, sanitization).
