# Feature Flag Helper Summary

`integration_flags.py` provides:
- `RetrievalIntegrationMode` with: disabled, monitor_only, shadow_deny, enforce
- `RetrievalIntegrationConfig`
- `default_retrieval_integration_config()` defaulting to `disabled`
- mode helpers and validation

Validation rejects invalid modes. No environment-variable integration or live app config wiring is included.
