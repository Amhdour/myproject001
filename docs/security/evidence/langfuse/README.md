# Langfuse Evidence Bridge for OPA Retrieval ACL

This evidence bundle documents the safe Langfuse bridge for OPA Retrieval ACL security trace metadata.

## Scope

- Adapter: `backend/onyx/security_layer/langfuse_evidence.py`
- Runtime call site: `backend/onyx/security_layer/opa/retrieval_context_filter.py`
- Decision metadata source: `backend/onyx/security_layer/opa/decision_mapper.py`
- Related OpenTelemetry evidence: `docs/security/evidence/opentelemetry/`
- Related OPA evidence: `docs/security/evidence/opa/`
- Related redaction evidence: `docs/security/evidence/redaction/`

The bridge emits a Langfuse span named `security.opa.retrieval_acl.decision` only when the Langfuse SDK and runtime configuration are available. If Langfuse is not configured or the dependency is unavailable, the adapter is safe-disabled and retrieval/OPA enforcement continues unchanged.

## Data handling invariant

The adapter is deny-by-default and forwards only the allowlisted OPA Retrieval ACL metadata fields documented in `trace_schema.md`. It then passes that selected payload through the security-layer `safe_metadata` helper as defense-in-depth. It does not export raw retrieved chunk text, raw prompt text, full document content, secrets, auth tokens, or additional PII fields.

## Claim boundary

This is an evidence bridge and documentation bundle. It optionally uses the security-layer redaction helper when preparing selected metadata, but does not require Presidio and does not add scanners, red-team tools, dashboards, alerting, SIEM integration, or a production-readiness claim.
