# Limitations

- This is a local governance foundation only; it does not integrate with an external Authensor service.
- Approval persistence is modeled with an in-memory store for tests and demos, not a production database-backed workflow.
- No approval UI is implemented.
- The policy registry contains example tool names and should be expanded before broader enforcement.
- Critical side-effecting actions are denied by default unless local configuration switches them to approval-required.
- The layer does not add OpenGuardrails, PyRIT, garak, promptfoo, or Ragas.
- OPA Retrieval ACL and RAG injection scanner behavior are unchanged.
- The evidence metadata is intentionally minimal and excludes raw payloads, secrets, PII, and document content.
