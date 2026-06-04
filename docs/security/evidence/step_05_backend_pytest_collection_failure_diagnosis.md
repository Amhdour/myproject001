# Step 05 Backend Pytest Collection Failure Diagnosis

## Environment

| Field | Value |
| --- | --- |
| UTC timestamp | `2026-06-04T13:06:12Z` |
| Branch name | `codex/fix-github-actions-workflow-setup-failure` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Local branch observed | `work` |
| Commit SHA inspected locally before this update | `b11ae490cecd07195b259aebec00ccc16e690b7b` |
| Current PR | `#130` |

## CI run inspected

| Field | Value |
| --- | --- |
| Repository | `Amhdour/myproject001` |
| Workflow | `Python Backend Test Collection` |
| Workflow run id | `26948352354` |
| Job id | `79506890682` |
| Job name | `Python Backend Test Collection` |
| Failed step | `Collect backend unit tests` |
| Public job URL | `https://github.com/Amhdour/myproject001/actions/runs/26948352354/job/79506890682?pr=130` |

## Exact failure available from GitHub Actions

The full pytest traceback was not available from this environment. The public GitHub job page displayed `Sign in to view logs`, local `gh` was not installed, and a direct GitHub API request for job logs failed with `Tunnel connection failed: 403 Forbidden`.

The exact available GitHub Actions annotation was:

```text
Collect backend unit tests
Process completed with exit code 2.
```

## Failure classification

| Category | Status |
| --- | --- |
| missing module | Not confirmed from available CI annotation. |
| import error | Not confirmed from available CI annotation. |
| config error | Not confirmed from available CI annotation. |
| database/env error | Not confirmed from available CI annotation. |
| fixture error | Not confirmed from available CI annotation. |
| path error | Not confirmed from available CI annotation. |
| dependency lock error | Not indicated by the verified CI state because `Sync dependencies` passed before pytest collection. |
| other | Confirmed at the annotation level only: pytest collect-only step exited with code `2`. |

Current classification: `TEST_COLLECTION_FAILED_IN_CI`.

## Root cause if confirmed

No concrete root cause is confirmed because the first pytest traceback line is hidden behind authenticated GitHub Actions logs.

## Root cause if not confirmed

The blocker is preserved as an unresolved pytest collection failure. The verified CI state proves that workflow setup and dependency sync are no longer the blockers, but it does not prove whether the collection failure is caused by a missing dependency, optional dependency, wrong test path, missing environment variable, import side effect, service requirement, fixture issue, or upstream Onyx dependency complexity.

## Files inspected

- `pyproject.toml`
- `uv.lock`
- `backend/requirements/README.md`
- `CONTRIBUTING.md`
- `.github/workflows/security-layer-tests.yml`
- `.github/workflows/runtime-retrieval-acl-security.yml`
- `.github/workflows/evidence-integrity.yml`
- `.github/workflows/portfolio-claim-boundary.yml`
- `backend/tests/conftest.py`
- `backend/tests/unit`
- `backend/tests/unit/model_server/test_embedding.py`

## Fix applied or blocker preserved

No dependency or runtime code fix was applied because the exact pytest traceback was not available. The safe action in this update is documentation and classification correction only:

- preserve the `Python Backend Test Collection` workflow;
- keep the backend unit-test collect-only command intact;
- document that dependency sync passed and pytest collection was reached;
- reclassify the current blocker as `TEST_COLLECTION_FAILED_IN_CI`;
- avoid narrowing tests, hiding failures, or adding speculative dependencies.

If the full traceback later confirms an optional dependency is missing, adding it is safe only when it belongs in the correct `pyproject.toml` dependency group and `uv.lock` is refreshed. If the missing component is not needed for backend unit collection, a narrower test scope can be considered only with explicit documentation that full backend collection remains blocked.

## Commands run

```bash
pwd && find .. -name AGENTS.md -print && git status --short --branch
gh pr view 130 --json number,headRefName,baseRefName,headRefOid,url,statusCheckRollup --repo Amhdour/myproject001
git remote -v && git branch --show-current && git rev-parse HEAD && git log --oneline -5
git status --short --branch && git remote get-url origin || true && git remote
python - <<'PY'
import urllib.request
url='https://api.github.com/repos/Amhdour/myproject001/actions/jobs/79506890682/logs'
req=urllib.request.Request(url, headers={'Accept':'application/vnd.github+json'})
try:
    with urllib.request.urlopen(req) as r:
        print(r.status, r.geturl(), r.headers.get('content-type'))
        print(r.read(20000).decode('utf-8','replace')[:20000])
except Exception as e:
    print(type(e).__name__, e)
    if hasattr(e,'read'):
        print(e.read().decode('utf-8','replace'))
PY
find .github/workflows -maxdepth 1 -type f -print 2>/dev/null | sort
find docs/security/evidence -maxdepth 1 -type f -print | sort | tail -30
sed -n '1,220p' pyproject.toml
sed -n '1,220p' backend/requirements/README.md
sed -n '1,220p' CONTRIBUTING.md
rg -n "pytest|testpaths|python_files|asyncio|backend/tests|security_layer|uv sync|dependency-groups|\\[tool.pytest" pyproject.toml uv.lock backend/requirements/README.md CONTRIBUTING.md .github/workflows backend/tests/unit -g '!**/.venv/**'
test -x .venv/bin/python && .venv/bin/python -V && .venv/bin/python -m pytest --version || true
uv --version || python -m pip show uv || true
python3.11 --version || true && UV_PYTHON_DOWNLOADS=never uv sync --frozen
PYENV_VERSION=3.11.15 python --version && PYENV_VERSION=3.11.15 UV_PYTHON_DOWNLOADS=never uv sync --frozen
rm -rf .venv && PYENV_VERSION=3.11.15 UV_PYTHON_DOWNLOADS=never uv sync --frozen
source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q
rm -rf .venv && PYENV_VERSION=3.11.15 UV_PYTHON_DOWNLOADS=never uv sync --frozen --no-default-groups --group backend --group dev --group ee
find backend/tests -path '*/conftest.py' -print | sort | head -20
sed -n '1,240p' backend/tests/conftest.py
sed -n '1,140p' backend/tests/unit/model_server/test_embedding.py
date -u +%Y-%m-%dT%H:%M:%SZ && git rev-parse HEAD
```

## Safe claims

- CI workflow setup recovered for PR `#130`.
- Dependency sync passed in the observed CI run.
- Pytest collection was reached in the observed CI run.
- Pytest collection failed in CI with exit code `2`.
- The correct current classification is `TEST_COLLECTION_FAILED_IN_CI`.
- Production readiness remains NO-GO.
- Enterprise readiness remains NO-GO.

## Forbidden claims

Do not claim:

- full backend pytest collection passes;
- backend test recovery is complete;
- backend tests pass;
- production readiness;
- enterprise readiness;
- live security enforcement;
- external validation; or
- compliance certification.

## Next step

Use an authenticated GitHub Actions log source to retrieve the full `Collect backend unit tests` output for run `26948352354`, job `79506890682`. Record the first pytest collection traceback line, then apply the smallest justified fix without deleting the workflow, hiding tests, weakening the gate, or refactoring runtime application code.
