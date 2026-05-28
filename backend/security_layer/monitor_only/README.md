# Limited Monitor-Only Integration Bundle

This package contains isolated helper modules for Step 27X limited monitor-only integration work.
It intentionally does **not** add live request hooks, blocking, filtering, enforcement, or shadow-deny runtime behavior.

## Selected candidates

- `LMO-002 shared audit/finding/metric sink consolidation`
- `LMO-004 cache monitor-only dry-run adapter`

## Safety boundary

- Default feature flags are disabled.
- Runtime mode is limited to `disabled` and `monitor_only`.
- Helpers are telemetry-only and fail open by construction.
- The cache adapter exposes a pass-through helper that returns the original value unchanged.
