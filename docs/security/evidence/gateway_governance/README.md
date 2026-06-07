# Gateway Governance Evidence

This directory captures evidence for an env-gated, OpenGuardrails-style gateway policy layer. The layer evaluates sanitized route metadata before an application could route a request to a private or external model provider.

Supported local decisions are `allow`, `deny`, `mask`, `route_private`, `route_external`, `approval_required`, `monitor`, and `shadow_deny`.

Evidence is metadata-only and excludes raw prompts, retrieved context, secrets, PII, tokens, and full document content.
