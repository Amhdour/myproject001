# Staging Helper Coverage

Covered helper files:

- `backend/security_layer/staging/models.py`
- `backend/security_layer/staging/checklist.py`
- `backend/security_layer/staging/__init__.py`
- `backend/security_layer/staging/README.md`

Covered tests:

- `backend/security_layer/tests/test_staging_models.py`
- `backend/security_layer/tests/test_staging_checklist.py`

The helpers are isolated in-memory models/checklist evaluation only and do not
call Coolify, mutate runtime flags, change application behavior, or perform any
network activity.
