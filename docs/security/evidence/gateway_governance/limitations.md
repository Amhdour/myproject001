# Gateway Governance Limitations

- This is a local, env-gated gateway policy layer and is not a production-readiness claim.
- No live LLM provider routing behavior is changed in this branch; the policy layer is ready to be called by a future gateway integration seam.
- `SECURITY_GATEWAY_GOVERNANCE_ENABLED=true` is required for policy decisions beyond preserve-route allow behavior.
- The layer does not add Ragas, promptfoo, PyRIT, or garak.
- The layer does not alter OPA Retrieval ACL behavior.
- The layer does not alter RAG injection scanner behavior.
- Evidence is metadata-only and excludes raw prompts, retrieved context, secrets, PII, tokens, and full document content.
