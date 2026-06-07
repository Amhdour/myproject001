# OpenTelemetry Retrieval ACL Trace Schema

## Span: `security.opa.retrieval_context_filter`

Emitted around the final RAG context-filtering operation for OPA Retrieval ACL enforcement.

| Attribute | Meaning | Content restriction |
| --- | --- | --- |
| `correlation_id` | Request or RAG-context correlation identifier passed into the filter. | Identifier only; no prompt or chunk text. |
| `subject_user_id` | Acting subject user identifier when available. | Identifier only. |
| `subject_tenant_id` | Acting subject tenant identifier when available. | Identifier only. |
| `enforcement_enabled` | Boolean result of `SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT=true`. | Boolean only. |
| `decision_count` | Number of per-chunk OPA decisions evaluated by the filter. | Count only. |
| `allowed_section_count` | Number of sections left after denied chunks and empty sections are removed. | Count only. |

## Span: `security.opa.retrieval_acl.decision`

Emitted around each per-chunk Retrieval ACL OPA decision.

| Attribute | Meaning | Content restriction |
| --- | --- | --- |
| `correlation_id` | Per-chunk decision correlation identifier. | Identifier only; no prompt or chunk text. |
| `subject_user_id` | Acting subject user identifier when available. | Identifier only. |
| `subject_tenant_id` | Acting subject tenant identifier when available. | Identifier only. |
| `resource_document_id` | Retrieved resource document identifier. | Identifier only. |
| `resource_chunk_id` | Retrieved resource chunk identifier. | Identifier only. |
| `resource_tenant_id` | Retrieved resource tenant identifier when available. | Identifier only. |
| `policy_package` | OPA policy package that produced the decision. | Policy metadata only. |
| `decision` | OPA decision value such as `allow`, `deny`, `monitor`, or `shadow_deny`. | Decision enum only. |
| `reason` | Policy reason string returned or mapped for the decision. | Policy reason only; must not include raw chunk text. |
| `fallback_used` | Whether the OPA unavailable fallback produced the decision. | Boolean only. |
| `enforcement_enabled` | Boolean result of `SECURITY_OPA_RETRIEVAL_ACL_CONTEXT_ENFORCEMENT=true`. | Boolean only. |

## Non-exported fields

The instrumentation does not record:

- raw retrieved chunk content;
- `InferenceSection.combined_content`;
- prompts or LLM messages;
- document bodies;
- allowed user/group lists from ACL metadata.
