# Limited Monitor-Only Feature Flags

## Implemented Flags

| Flag | Default | Purpose |
|---|---:|---|
| `runtime_mode` | `disabled` | Limits helpers to disabled or monitor-only runtime state. |
| `shared_sink_enabled` | `false` | Enables shared audit/finding/metric telemetry helper when runtime is monitor-only. |
| `cache_adapter_enabled` | `false` | Enables cache dry-run observations when runtime is monitor-only. |

## Environment Variables

| Variable | Default | Effect |
|---|---:|---|
| `SECURITY_LAYER_MONITOR_ONLY_ENABLED` | unset/false | Enables `monitor_only` runtime when truthy. |
| `SECURITY_LAYER_MONITOR_ONLY_SHARED_SINK_ENABLED` | unset/false | Enables shared sink only when monitor-only runtime is enabled. |
| `SECURITY_LAYER_MONITOR_ONLY_CACHE_ADAPTER_ENABLED` | unset/false | Enables cache adapter only when monitor-only runtime is enabled. |

## Guardrails

- Helper flags are invalid when runtime mode is disabled.
- No `enforce` mode is present in this feature-flag module.
- No `shadow_deny` runtime mode is present in this feature-flag module.
- The cache adapter is telemetry-only and preserves original return values.
