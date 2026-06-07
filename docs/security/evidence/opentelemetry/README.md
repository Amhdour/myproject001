# OpenTelemetry Evidence for OPA Retrieval ACL Context Enforcement

This evidence bundle documents the OpenTelemetry span instrumentation added for the OPA Retrieval ACL context-enforcement path. The instrumentation is intentionally limited to retrieval-context filtering and per-chunk OPA decisions.

## Scope

- Helper module: `backend/onyx/security_layer/tracing.py`
- Instrumented runtime path: `backend/onyx/security_layer/opa/retrieval_context_filter.py`
- Decision metadata source: `backend/onyx/security_layer/opa/decision_mapper.py`
- OPA evidence linkage: `docs/security/evidence/opa/`

This bundle does not add Langfuse-specific tracing, Presidio, new scanners, alerting, dashboards, SIEM integration, or a production-readiness claim.

## Spans

The Retrieval ACL path emits these span names when OpenTelemetry is available and a tracer provider/exporter is configured by the runtime environment:

- `security.opa.retrieval_context_filter`
- `security.opa.retrieval_acl.decision`

If the OpenTelemetry API dependency is unavailable, the helper degrades to a no-op so RAG retrieval and OPA enforcement behavior continue without trace export.

## Data handling invariant

Span attributes use identifiers and decision metadata only. Raw prompt text, chunk text, combined retrieved context, and document content are not recorded by this instrumentation.
