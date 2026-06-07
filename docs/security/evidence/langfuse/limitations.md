# Langfuse Evidence Limitations

- This bundle does not include live validation against a running Langfuse server unless those commands are explicitly run in the target environment.
- This bridge is not a production observability claim and does not provide dashboards, alerting, SIEM integration, retention controls, or operational SLOs.
- The adapter intentionally does not export raw RAG content, raw prompt text, raw retrieved chunk text, full document content, secrets, or auth tokens. Selected metadata is passed through the security-layer redaction helper as defense-in-depth.
- This bundle is not full end-to-end production trace proof; it covers a safe adapter, local smoke checks, and documentation for the OPA Retrieval ACL evidence path.
- Missing Langfuse SDK dependency or missing `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` runtime configuration safe-disables the bridge.
- No Presidio integration, scanners, or red-team tools are added by this change.
