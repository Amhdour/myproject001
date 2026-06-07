# OpenTelemetry Retrieval ACL Limitations

- This change instruments only the OPA Retrieval ACL context-enforcement path; it does not add OpenTelemetry spans for every security decision or every RAG step.
- This change does not add Langfuse-specific wiring, Presidio, new scanners, dashboards, alerting, SIEM integration, compliance certification, or a production-readiness claim.
- If `opentelemetry-api` is unavailable, `backend/onyx/security_layer/tracing.py` returns no-op spans and does not break the RAG flow.
- Trace export still depends on the deployment configuring an OpenTelemetry tracer provider and exporter. The repository change does not configure a collector endpoint.
- Span attributes intentionally omit raw prompt text, raw chunk text, combined context, document bodies, and ACL principal lists.
- The OPA enforcement decision behavior is unchanged; tracing observes decisions and selected metadata only.
- Local tests with fake spans validate the schema and no-raw-chunk-text invariant but do not prove live collector export.
