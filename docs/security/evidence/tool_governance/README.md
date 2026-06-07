# Tool Governance Evidence

This directory documents the local Authensor-style tool/action governance foundation for selected agent/tool execution decisions.

The foundation is intentionally local-only. It does not add OpenGuardrails, PyRIT, garak, promptfoo, Ragas, or an external Authensor service dependency. It also does not change OPA Retrieval ACL or RAG injection scanner behavior.

## Covered behavior

- Example local risk registry:
  - `search`: low
  - `read_document`: medium
  - `send_email`: high
  - `delete_document`: critical
  - `external_api_call`: high
- Supported decisions: `allow`, `deny`, `approval_required`, `monitor`, and `shadow_deny`.
- High-risk side-effecting actions require approval.
- Critical side-effecting actions are denied by default or can require approval by local configuration.
- Approval records model self-approval prevention and replay protection.
- Receipts include stable audit identifiers and a SHA-256 receipt hash.
- Langfuse-safe evidence is allowlisted and redacted.

## Evidence boundaries

Raw tool payloads, secrets, PII, prompts, and document content are not exported in the evidence metadata. The receipt and Langfuse-safe metadata contain only governance fields needed for traceability.
