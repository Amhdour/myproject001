# Cache Adapter Coverage

## Covered Behavior

- Disabled state returns a skipped observation.
- Enabled monitor-only state records observations through the shared sink.
- Invalid cache context/metadata/TTL conditions produce monitor-only finding reason codes.
- Pass-through helper returns the original result object unchanged.

## Safety Notes

The adapter is not wired into live cache paths. It performs dry-run validation and telemetry only.
