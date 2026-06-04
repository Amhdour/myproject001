# Step 04 CI Workflow Setup Recovery Evidence

## Environment

| Field | Value |
| --- | --- |
| UTC timestamp | `2026-06-04T13:06:12Z` |
| Branch name | `codex/fix-github-actions-workflow-setup-failure` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Local starting branch observed | `work` |
| Local commit SHA before Step 05 documentation | `b11ae490cecd07195b259aebec00ccc16e690b7b` |

## Original workflow failure

| Field | Value |
| --- | --- |
| Workflow | `Python Backend Test Collection` |
| Workflow file | `.github/workflows/python-test-collection.yml` |
| Earlier failed step name | `Set up job` |
| Pytest collection reached in earlier run | No |
| Earlier corrected classification | `CI_WORKFLOW_SETUP_FAILED` |

The earlier reported failure happened before checkout, Python setup, uv installation, dependency sync, or pytest collection. Therefore that earlier run was not evidence that backend pytest collection failed.

## Step 05 update: setup recovered, collection blocker remains

| Field | Value |
| --- | --- |
| PR inspected | `#130` |
| Workflow run id | `26948352354` |
| Job id | `79506890682` |
| Current failed step | `Collect backend unit tests` |
| Workflow setup recovered | Yes. The job progressed past setup into normal workflow steps. |
| Dependency sync reached | Yes. The CI state reached the later pytest collection step, so dependency sync completed. |
| Pytest collection reached | Yes. The `Collect backend unit tests` step ran and failed. |
| Remaining blocker | Moved from workflow setup to pytest collection. |
| Current classification | `TEST_COLLECTION_FAILED_IN_CI` |

## Root cause

The root cause of the original workflow setup failure is not confirmed from this local checkout. The root cause of the current pytest collection failure is also not confirmed because the full GitHub Actions pytest traceback was not available without sign-in. The exact available annotation from the public job page is `Collect backend unit tests` / `Process completed with exit code 2.`

## Workflow fix applied

The workflow is present as a minimal GitHub Actions shape:

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
gh pr view 130 --json number,headRefName,baseRefName,headRefOid,url,statusCheckRollup --repo Amhdour/myproject001
python - <<'PY'
import urllib.request
url='https://api.github.com/repos/Amhdour/myproject001/actions/jobs/79506890682/logs'
req=urllib.request.Request(url, headers={'Accept':'application/vnd.github+json'})
with urllib.request.urlopen(req) as r:
    print(r.status, r.geturl(), r.headers.get('content-type'))
PY
rg -n "pytest|testpaths|python_files|asyncio|backend/tests|security_layer|uv sync|dependency-groups|\\[tool.pytest" pyproject.toml uv.lock backend/requirements/README.md CONTRIBUTING.md .github/workflows backend/tests/unit -g '!**/.venv/**'
sed -n '130,230p' pyproject.toml
sed -n '1,130p' backend/requirements/README.md
sed -n '1,80p' .github/workflows/security-layer-tests.yml
sed -n '1,80p' .github/workflows/runtime-retrieval-acl-security.yml
PYENV_VERSION=3.11.15 UV_PYTHON_DOWNLOADS=never uv sync --frozen
PYENV_VERSION=3.11.15 UV_PYTHON_DOWNLOADS=never uv sync --frozen --no-default-groups --group backend --group dev --group ee
source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q
```

## Safe claims

- Workflow setup recovered in the observed PR `#130` run.
- Dependency sync was reached and passed in the observed PR `#130` run.
- Pytest collection was reached in the observed PR `#130` run.
- The current CI blocker is pytest collection, classified as `TEST_COLLECTION_FAILED_IN_CI`.
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

Retrieve the full authenticated GitHub Actions log for run `26948352354`, job `79506890682`, record the first pytest collection traceback, and apply only the smallest fix supported by that traceback.
