# Coolify Staging Evidence Helpers

This package contains isolated Step 29X helper models and checklist logic for a
Coolify staging evidence bundle.

## Boundary

- No Coolify API calls are made.
- No deployment, network, environment, database, cache, vector, retrieval, tool,
  MCP, artifact, worker, web, enforce-mode, or shadow-deny state is changed.
- No enforce mode is enabled.
- No shadow-deny runtime mode is enabled.
- No live blocking or live filtering is enabled.
- No application behavior is changed.
- No production-readiness claim is made.

## Test command

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_staging_models.py backend/security_layer/tests/test_staging_checklist.py -q
```
