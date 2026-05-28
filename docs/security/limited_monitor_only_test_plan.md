# Limited Monitor-Only Test Plan

## Scope

Validate Step 27X isolated monitor-only helpers only:

- candidate inventory and selected-candidate count
- default-disabled feature flags
- shared audit/finding/metric sink consolidation
- cache dry-run adapter behavior preservation

## Focused Test Command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_monitor_only_models.py backend/security_layer/tests/test_monitor_only_feature_flags.py backend/security_layer/tests/test_monitor_only_shared_sink.py backend/security_layer/tests/test_monitor_only_cache_adapter.py -q
```

## Full Security-Layer Test Command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```

## Acceptance Criteria

- Focused monitor-only tests pass.
- Full security-layer tests pass.
- Disabled flags do not emit telemetry.
- Cache adapter returns the original result object unchanged.
- No enforce mode, shadow-deny runtime mode, live blocking, or live filtering is enabled.

## Non-Leakage Checks

- Shared sink test data uses safe synthetic request IDs and details.
- Cache adapter telemetry captures operation and purpose only.
- No raw document contents, user secrets, credentials, or API keys are emitted.
