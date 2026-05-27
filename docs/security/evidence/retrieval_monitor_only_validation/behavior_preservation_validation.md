# Behavior Preservation Validation
- Disabled mode test confirms no audit/metrics emitted and no retrieval mutation.
- Monitor-only mode test confirms audit/metric emission without candidate filtering.
- Live path test confirms `_apply_monitor_only_live_acl_hook` preserves `return chunks` behavior shape.
- Exception handling test confirms fail-open preservation.
