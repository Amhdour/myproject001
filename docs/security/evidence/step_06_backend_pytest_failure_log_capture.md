# Step 06 Backend Pytest Failure Log Capture

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T13:12:49Z |
| Branch name | `codex/fix-github-actions-workflow-setup-failure` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `b11ae490cecd07195b259aebec00ccc16e690b7b` |

## Current blocker

`TEST_COLLECTION_FAILED_IN_CI`

GitHub Actions reaches pytest collection for the backend unit-test suite, but collection fails with exit code `2`. The exact collection-time traceback was not available in the local/Codex environment, so the root cause remains unconfirmed.

## Workflow changes

The Python Backend Test Collection workflow now:

- creates `.artifacts/python-test-collection` before collection;
- records environment metadata in `.artifacts/python-test-collection/environment.txt`;
- prints diagnostic versions before pytest collection;
- runs the full backend unit-test collection gate with `tee`;
- preserves pytest failure by using `set -o pipefail`;
- uploads the collection log and environment metadata with `actions/upload-artifact@v4` and `if: always()`.

## Artifact path

Collection log:

```text
.artifacts/python-test-collection/backend-unit-collection.log
```

Environment metadata:

```text
.artifacts/python-test-collection/environment.txt
```

Uploaded artifact name:

```text
python-backend-test-collection-log
```

## Diagnostic commands added

```bash
python --version
which python
python -m pytest --version
python -c "import pytest; print(pytest.__version__)"
uv --version
uv pip list
```

## Collection command

```bash
python -m pytest --collect-only backend/tests/unit -q -ra 2>&1 | tee .artifacts/python-test-collection/backend-unit-collection.log
```

The required collection gate remains:

```bash
python -m pytest --collect-only backend/tests/unit -q
```

## Expected CI result

The workflow is expected to remain red if pytest collection still fails. This change must not make CI pass artificially and must not hide the pytest exit code.

## Safe claims

- The workflow improves observability for backend unit-test collection failures.
- The exact pytest collection output should be visible in the GitHub Actions step log when the collection step runs.
- The collection log should be uploaded as `python-backend-test-collection-log` when the workflow reaches artifact upload.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim backend unit-test collection is recovered unless the collection command passes.
- Do not claim the root cause is confirmed before reviewing the captured traceback.
- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim the PR is safe to merge solely because observability improved.

## Next step

Run GitHub Actions for the updated workflow, download or inspect `python-backend-test-collection-log`, and use `.artifacts/python-test-collection/backend-unit-collection.log` to identify the exact pytest collection failure.
