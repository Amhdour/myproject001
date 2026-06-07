# MCP Governance Evidence

This directory documents the initial local MCP governance foundation for selected MCP server, tool, and resource authorization decisions.

## Scope

- Local in-process governance only; no external MCP gateway dependency is required.
- OpenGuardrails is not included in this foundation.
- OPA Retrieval ACL behavior is unchanged.
- RAG injection scanner behavior is unchanged.
- Existing tool governance behavior is unchanged except for shared evidence/redaction utilities.
- This evidence does not make a production-readiness claim.

## Covered Decisions

The foundation supports `allow`, `deny`, `approval_required`, `monitor`, and `shadow_deny` decisions.

## Evidence Safety

Langfuse-safe metadata is restricted to MCP identifiers, decision, reason, receipt hash, and correlation ID. Raw MCP payloads, secrets, tokens, prompts, tool outputs, and document content are excluded and the remaining payload is passed through the shared redaction helper.
