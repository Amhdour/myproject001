# Step 03 Summary

Status: PENDING_CI

A GitHub Actions workflow was added at .github/workflows/python-test-collection.yml.

The workflow checks whether backend unit tests can be collected in CI.

Main command:

```bash
uv run python -m pytest --collect-only backend/tests/unit -q
```

Next: open a pull request and wait for the workflow result.
