# Local Validation Results — Security Readiness MVP

## Dependency setup inspection

- Command: `test -d .venv && echo yes || echo no; python - <<'PY' ...`
- Result: blocked for full backend environment.
- Reason: `.venv` exists, but `fastapi_users` was missing; `uv run` on default Python 3.14 was blocked by `onnxruntime` wheel compatibility; `uv run --python 3.11` attempted a GitHub download that failed through the network tunnel.
- Important output excerpt: `ModuleNotFoundError: No module named 'fastapi_users'`; `onnxruntime ... doesn't have a source distribution or wheel for ... CPython 3.14`; `Failed to download ... cpython-3.11.13`.
- Next action: run full backend tests in a correctly provisioned Python 3.11 environment or GitHub Actions runner.

## Backend security tests only

- Command: `PYTHONPATH=. pytest -q --confcutdir=backend/tests/security backend/tests/security`
- Result: passed.
- Reason: MVP tests intentionally avoid parent backend conftest and external services.
- Important output excerpt: `25 passed, 31 warnings in 0.05s`.
- Next action: run the same command in GitHub Actions via `.github/workflows/security-readiness.yml`.

## Demo attack tests

- Command: `PYTHONPATH=. pytest -q --confcutdir=backend/tests/security backend/tests/security/demo_attacks`
- Result: passed.
- Reason: deterministic service-level demo attacks ran locally.
- Important output excerpt: `5 passed, 11 warnings in 0.02s`.
- Next action: add live route demo coverage in the next PR.

## Existing backend tests

- Command: `source .venv/bin/activate 2>/dev/null || true; pytest -q backend/tests/security`
- Result: blocked.
- Reason: parent `backend/tests/conftest.py` imports full backend dependencies that are not installed in `.venv`.
- Important output excerpt: `ModuleNotFoundError: No module named 'fastapi_users'`.
- Next action: install backend dependencies in a Python 3.11 environment and rerun.

## Evidence validation script

- Command: `python scripts/security/validate_security_evidence.py`
- Result: passed.
- Reason: all required evidence files and tests exist and are non-empty.
- Important output excerpt: `Security evidence validation passed for 12 required paths.`
- Next action: keep this script in CI.

## CI-equivalent local command

- Command: `python -m py_compile $(find backend/security scripts/security -name '*.py' -print) && python scripts/security/validate_security_evidence.py`
- Result: passed.
- Reason: MVP implementation and validation script compiled; evidence validation passed.
- Important output excerpt: `Security evidence validation passed for 12 required paths.`
- Next action: wait for GitHub Actions validation after PR creation.
