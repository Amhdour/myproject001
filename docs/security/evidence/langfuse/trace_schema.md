# Langfuse OPA Retrieval ACL Trace Schema

## Observation

- Name: `security.opa.retrieval_acl.decision`
- Type: Langfuse span
- Metadata source: OPA Retrieval ACL decision metadata after a chunk-level decision is evaluated.

## Allowed metadata fields

| Field | Meaning | Data handling note |
| --- | --- | --- |
| `correlation_id` | Request/decision correlation identifier. | Identifier only. |
| `subject_user_id` | User identifier from the OPA subject. | Identifier only; no profile or user content. |
| `subject_tenant_id` | Tenant identifier from the OPA subject. | Identifier only. |
| `resource_document_id` | Document identifier for the evaluated resource. | Identifier only; no document body. |
| `resource_chunk_id` | Chunk identifier for the evaluated resource. | Identifier only; no chunk text. |
| `resource_tenant_id` | Tenant identifier on the evaluated resource. | Identifier only. |
| `policy_package` | OPA policy package that made the decision. | Policy metadata only. |
| `decision` | OPA decision value such as `allow`, `deny`, `monitor`, or `shadow_deny`. | Decision metadata only. |
| `reason` | OPA reason string. | Reason metadata only; must not contain raw RAG content. |
| `fallback_used` | Whether fallback handling was used for the decision. | Boolean only. |
| `enforcement_enabled` | Whether retrieval-context enforcement is enabled by runtime config. | Boolean only. |

## Deny-by-default fields

Any metadata key outside the allowed list is ignored by the adapter. This excludes raw retrieved chunk text, raw prompt text, full document content, secrets, auth tokens, and ad-hoc PII fields.
