# Telemetry Sample

## Expected metric

```json
{
  "metric_name": "retrieval_acl_decision_total",
  "mode": "enforce",
  "decision": "deny",
  "enforcement_result": "blocked",
  "denied_chunk_count": 1
}
```

## Purpose

This metric supports reviewer inspection of the bounded retrieval ACL decision path. It is an in-memory test/demo metric and not a production monitoring backend.

## Current status

`EXPECTED_SAMPLE_ONLY_PENDING_EXECUTION`

Update this file with real redacted output from local, CI, or staging execution.
