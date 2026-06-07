# OPA Retrieval ACL Demo Attack Results

## Scenario

- Tenant A user receives a retrieved chunk belonging to Tenant B.
- The OPA Retrieval ACL policy evaluates the context-inclusion action `rag.context.include`.
- The policy denies the cross-tenant resource.
- The chunk is excluded from final RAG context.
- Decision evidence is written to `docs/security/evidence/opa/decision_log_samples.jsonl`.

## Observed demo result

```json
{
  "decision": "deny",
  "reason": "cross-tenant resource",
  "chunk_excluded_from_rag_context": true,
  "fallback_used": false
}
```
