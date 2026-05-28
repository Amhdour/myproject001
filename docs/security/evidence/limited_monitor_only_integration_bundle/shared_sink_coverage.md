# Shared Sink Coverage

## Covered Behavior

- Disabled state emits no audit, finding, or metric records.
- Enabled monitor-only state emits audit and metric records.
- Optional reason codes emit findings.
- Emitted runtime mode is `monitor_only`.

## Safety Notes

The sink writes only to existing in-memory security-layer runtime helpers in tests. It does not block or filter live application behavior.
