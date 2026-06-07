# OPA Retrieval ACL Demo Attack Results

## Scenario

- Tenant A user receives a retrieved chunk belonging to Tenant B.
- The OPA Retrieval ACL policy evaluates the context-inclusion action `rag.context.include`.
- The policy denies the cross-tenant resource.
- The chunk is excluded before final RAG context serialization.
- Decision evidence is written to `docs/security/evidence/opa/decision_log_samples.jsonl`.

## Observed demo result

Generated with:

```bash
python scripts/security/demo_attacks/opa/retrieval_acl_policy_bypass_demo.py
```

```json
{
  "audit_evidence_path": "docs/security/evidence/opa/decision_log_samples.jsonl",
  "chunk_excluded_from_rag_context": true,
  "decision": "deny",
  "fallback_used": false,
  "final_context_contains_tenant_b_chunk": false,
  "opa_denied_cross_tenant_chunk": true,
  "reason": "cross-tenant resource",
  "tenant_a_received_tenant_b_chunk": true
}
```

## Limitation

The demo attack script remains deterministic and in-process so evidence can be reproduced without a running OPA server. The runtime patch point is the final internal-search `InferenceSection` to LLM JSON serialization path; live OPA server availability still depends on deployment configuration.
