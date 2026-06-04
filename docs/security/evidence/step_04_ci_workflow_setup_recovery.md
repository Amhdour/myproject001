# Step 04 CI Workflow Setup Recovery Evidence

## Environment

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T11:11:13Z |
| Branch name | `codex/add-ci-backed-python-test-collection-workflow` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Local starting branch observed | `work` |
| Current commit SHA before this correction | `b11ae490cecd07195b259aebec00ccc16e690b7b` |

## Original workflow failure

| Field | Value |
| --- | --- |
| Workflow | `Python Backend Test Collection` |
| Workflow file | `.github/workflows/python-test-collection.yml` |
| PR | `#129` |
| Failed job name | `Python Backend Test Collection` |
| Failed step name | `Set up job` |
| Pytest collection reached | No |
| Corrected classification | `CI_WORKFLOW_SETUP_FAILED` |

The reported failure happened before checkout, Python setup, uv installation, dependency sync, or pytest collection. Therefore the run is not evidence that backend pytest collection failed.

## Root cause

The root cause is not confirmed from this local checkout. The requested PR logs and repository settings were not visible locally because:

- the checkout initially had no `origin` remote configured;
- adding `https://github.com/Amhdour/myproject001.git` and fetching failed with a CONNECT tunnel 403;
- `gh` is not installed in the environment, so PR #129 logs could not be queried with the GitHub CLI.

The confirmed local fact is the required target workflow file was not present in the starting checkout, while other workflows use a minimal `ubuntu-latest`, `actions/checkout@v4`, and `actions/setup-python@v5` pattern successfully.

## Workflow fix applied

The workflow was created/reduced to a minimal GitHub Actions shape:

```yaml
name: Python Backend Test Collection

on:
  pull_request:
  workflow_dispatch:

jobs:
  python-backend-test-collection:
    name: Python Backend Test Collection
    runs-on: ubuntu-latest
    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install uv
        run: |
          python -m pip install --upgrade pip uv

      - name: Sync dependencies
        env:
          UV_PYTHON_DOWNLOADS: never
        run: |
          uv sync --frozen

      - name: Collect backend unit tests
        run: |
          source .venv/bin/activate
          python -m pytest --collect-only backend/tests/unit -q
```

This avoids nonessential workflow options and avoids a separate setup-uv action while preserving the repository-supported `uv` dependency path and the collect-only backend pytest gate.

## Commands run locally

```bash
git remote -v
git branch -vv
git fetch origin codex/add-ci-backed-python-test-collection-workflow step-63x-runtime-retrieval-acl-proof
sed -n '1,220p' .github/workflows/python-test-collection.yml
find .github/workflows -maxdepth 1 -type f -print
sed -n '1,180p' .github/workflows/evidence-integrity.yml
sed -n '1,180p' .github/workflows/portfolio-claim-boundary.yml
sed -n '1,180p' .github/workflows/runtime-retrieval-acl-security.yml
sed -n '1,180p' .github/workflows/security-layer-tests.yml
gh auth status
gh pr view 129 --repo Amhdour/myproject001 --json headRefName,baseRefName,headRefOid,statusCheckRollup,url
date -u +%Y-%m-%dT%H:%M:%SZ
git rev-parse HEAD
```

## Expected GitHub Actions outcome

The corrected workflow is expected to get past GitHub Actions job setup and reach normal workflow steps: checkout, Python setup, uv installation, dependency sync, and then backend pytest collection if dependency sync succeeds.

If dependency sync or pytest collection fails, that later failure must be recorded with the exact failed step and logs. It must not be inferred from the earlier setup failure.

## Safe claims

- The prior PR #129 run is classified as `CI_WORKFLOW_SETUP_FAILED`.
- Pytest collection was not reached in that failed run.
- The workflow has been reduced to a minimal repository-consistent shape.
- `TEST_EXECUTION_BLOCKED` remains unresolved until a corrected workflow reaches and passes pytest collection.
- Production readiness remains NO-GO.
- Enterprise readiness remains NO-GO.

## Forbidden claims

Do not claim:

- backend pytest collection recovered;
- backend tests passed;
- production readiness;
- enterprise readiness;
- live enforcement;
- external validation; or
- compliance certification.

## Next step

Push this correction to PR #129 and rerun `Python Backend Test Collection`. Update Step 03/Step 04 evidence only with the actual GitHub Actions result after the workflow reaches a concrete step beyond setup.
