Added tests for monitor-only live adapter behavior:
- disabled mode emits no retrieval ACL telemetry events.
- monitor-only mode emits audit + metrics.
- monitor-only payload uses safe metadata fields only.
- full backend/security_layer tests pass under PYTHONPATH=.
