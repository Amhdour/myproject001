# Coolify Staging Evidence Helpers

This package contains isolated Step 29X and Step 32X helper models, checklist logic, and execution-evidence evaluators for Coolify staging evidence bundles.

## Boundary

- No Coolify API calls are made.
- No deployment, network, environment, database, cache, vector, retrieval, tool, MCP, artifact, worker, web, enforce-mode, or shadow-deny state is changed.
- No enforce mode is enabled.
- No shadow-deny runtime mode is enabled.
- No live blocking or live filtering is enabled.
- No application behavior is changed.
- No production-readiness claim is made.
- No enterprise production-readiness claim, external validation claim, or compliance certification claim is made.

## Step 29X Helpers

- `models.py` defines sanitized Coolify staging evidence bundle records.
- `checklist.py` evaluates the Step 29X staging checklist and staging-only go/no-go status.

## Step 32X Helpers

- `execution.py` defines sanitized real Coolify staging execution metadata, checklist items, and outcome helpers.
- Defaults intentionally state that no real Coolify deployment was executed, live staging validation is **PENDING**, partner-demo evidence review is **GO**, production readiness is **NO-GO**, enterprise production readiness is **NO-GO**, external validation is **PENDING**, and compliance certification is **NOT CLAIMED**.

## Test commands

```bash
PYTHONPATH=. python -m pytest backend/security_layer/tests/test_staging_execution.py backend/security_layer/tests/test_staging_models.py backend/security_layer/tests/test_staging_checklist.py -q
PYTHONPATH=. python -m pytest backend/security_layer/tests -q
```
