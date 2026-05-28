# Staging Execution Helper Coverage

Covered helper files:

- `backend/security_layer/staging/execution.py`
- `backend/security_layer/staging/README.md`
- `backend/security_layer/staging/__init__.py`

Covered tests:

- `backend/security_layer/tests/test_staging_execution.py`
- `backend/security_layer/tests/test_staging_models.py`
- `backend/security_layer/tests/test_staging_checklist.py`

The helper is isolated in-memory metadata/checklist/outcome evaluation only. It does not call Coolify, mutate runtime flags, change application behavior, or perform network activity.
