# Audit Log Sample

## Expected audit event

```json
{
  "event_type": "step_39x_runtime_retrieval_authorization",
  "request_id": "step-63x-cross-tenant-demo-attack",
  "mode": "enforce",
  "action": "retrieve",
  "resource_type": "chunk",
  "tenant_id": "tenant-a",
  "subject_id": "user-a",
  "decision": "deny",
  "reason_code": "retrieval_authorization_failed",
  "enforcement_result": "blocked"
}
```

## Redaction note

The sample intentionally excludes retrieved content and unauthorized document content.

## Current status

`EXPECTED_SAMPLE_ONLY_PENDING_EXECUTION`

Update this file with real redacted output from local, CI, or staging execution.
