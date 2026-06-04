# Step 05 Backend Pytest Collection Failure Diagnosis

## Status

`TEST_COLLECTION_FAILED_IN_CI`

The backend Python workflow setup reached the full backend unit-test collection gate, but pytest collection failed in GitHub Actions with exit code `2`. The root cause is not confirmed because the local/Codex environment did not expose the full CI traceback.

## Collection gate preserved

The workflow must continue to run the full backend unit-test collection gate:

```bash
python -m pytest --collect-only backend/tests/unit -q
```

The collection scope is not narrowed to make CI pass.

## Step 06 observability update

### Reason full traceback was needed

The previous CI signal only established that pytest collection failed with exit code `2`. That was not enough to identify the failing import, fixture, plugin, configuration file, or collection-time exception. The Step 06 workflow update captures the full pytest collection stream so the exact traceback can be reviewed from GitHub Actions logs and artifacts.

### Artifact name

`python-backend-test-collection-log`

### Log path

`.artifacts/python-test-collection/backend-unit-collection.log`

The same artifact upload also includes environment metadata at:

`.artifacts/python-test-collection/environment.txt`

### Workflow behavior

The workflow still executes the full backend unit-test collection command. The collection step uses `set -o pipefail` and `tee`, so the pytest output is written to the GitHub Actions log and to the artifact file while preserving pytest's non-zero exit status.

### Whether failure is still expected

Yes. Until CI proves otherwise, backend unit-test collection is still expected to fail with `TEST_COLLECTION_FAILED_IN_CI`. The update improves observability only; it does not recover or hide the failing collection result.

### Safe claim

It is safe to claim that the workflow now captures backend unit-test collection diagnostics and uploads the collection log artifact when the workflow reaches the collection step.

### Forbidden claim

Do not claim backend test collection is recovered, production readiness is achieved, enterprise readiness is achieved, or the repository is safe to merge because of this observability-only update.

## Readiness classification

| Area | Status |
| --- | --- |
| Backend unit-test collection | `TEST_COLLECTION_FAILED_IN_CI` |
| Production readiness | `NO-GO` |
| Enterprise readiness | `NO-GO` |
