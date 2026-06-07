# Security Evidence Redaction Helper

This evidence bundle documents the small security-layer redaction helper for safer evidence export.

## Scope

- Helper: `backend/onyx/security_layer/redaction.py`
- Langfuse evidence adapter usage: `backend/onyx/security_layer/langfuse_evidence.py`
- Related Langfuse evidence: `docs/security/evidence/langfuse/`
- Related OpenTelemetry evidence: `docs/security/evidence/opentelemetry/`
- Related OPA evidence: `docs/security/evidence/opa/`

The helper supports:

- `redact_text(value: str) -> str`
- `redact_mapping(data: dict) -> dict`
- `safe_metadata(data: dict) -> dict`

## Behavior

The helper dynamically uses Microsoft Presidio when `presidio-analyzer` and `presidio-anonymizer` are installed. Presidio is optional. When those packages are unavailable, the helper uses conservative built-in regex fallback redaction for email addresses, phone-like values, bearer tokens, API-key-like values, and obvious secret-key assignments.

The mapping helpers return redacted copies and do not mutate input mappings in place. Nested dictionaries, lists, tuples, and other non-string scalar values are copied or preserved as appropriate.

## Safe metadata preservation

`safe_metadata` preserves these explicitly allowlisted evidence metadata fields without value redaction:

- `correlation_id`
- `decision`
- `policy_package`
- `fallback_used`
- `enforcement_enabled`

All other fields pass through the redaction path. This keeps stable evidence identifiers available while reducing accidental PII or secret exposure.

## Content boundary

The redaction helper is a defense-in-depth utility for evidence payload safety. It does not authorize exporting new raw prompt text, retrieved chunk text, full document content, or other raw RAG content. The Langfuse evidence adapter remains deny-by-default and raw-content-free.
