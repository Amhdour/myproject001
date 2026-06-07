# Limitations

- This is a local governance foundation only; it does not integrate with an external Authensor service.
- Enforcement is disabled unless `SECURITY_TOOL_GOVERNANCE_ENFORCEMENT=true` is set.
- The current execution-seam patch applies only to selected tool names: `search` (including the Onyx `internal_search` implementation), `read_document`, `send_email`, `delete_document`, and `external_api_call`.
- Approval persistence is modeled with an in-memory store for tests and demos, not a production database-backed workflow.
- No approval UI is implemented; `approval_required` means the tool is not executed automatically by this seam.
- The policy registry contains example tool names and should be expanded before broader enforcement.
- Critical side-effecting actions are denied by default unless local configuration switches them to approval-required.
- The layer does not add OpenGuardrails, PyRIT, garak, promptfoo, or Ragas.
- OPA Retrieval ACL and RAG injection scanner behavior are unchanged.
- The evidence metadata is intentionally minimal and excludes raw payloads, secrets, PII, prompts, and document content.
- This evidence does not claim production readiness.
