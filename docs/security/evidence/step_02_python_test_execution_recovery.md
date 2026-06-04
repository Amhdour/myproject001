# Step 02 Python Test Execution Recovery Evidence

## Scope

This evidence records the attempt to recover backend Python test execution after the Step 01 blocker:

```text
TEST_EXECUTION_BLOCKED
.venv/bin/python: No module named pytest
```

No runtime application behavior was modified in this step.

## Environment

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T10:55:51Z |
| Branch name | `step-02-python-test-execution-recovery` |
| Requested base branch | `step-63x-runtime-retrieval-acl-proof` |
| Local starting branch observed | `work` |
| Starting commit SHA | `181a1bd0212b7bc1ed5ee04e193285be76ea0795` |
| Default `python --version` before repair | `Python 3.14.4` |
| Initial `.venv/bin/python --version` | `Python 3.14.4` |
| Recreated `.venv/bin/python --version` | `Python 3.11.15` |
| Package manager detected | `uv 0.7.22` |

## Branch/base evidence

Command:

```bash
git fetch origin step-63x-runtime-retrieval-acl-proof
```

Exit code: `128`

Output:

```text
fatal: 'origin' does not appear to be a git repository
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

Command:

```bash
git branch -a --no-color
```

Exit code: `0`

Output:

```text
* work
```

Command:

```bash
git switch -c step-02-python-test-execution-recovery
```

Exit code: `0`

Output:

```text
Switched to a new branch 'step-02-python-test-execution-recovery'
```

Result: the requested branch was created locally from the only available local branch/commit. The requested base branch could not be fetched because no `origin` remote is configured in this checkout.

## Dependency and test configuration files inspected

| File/path | Evidence found |
| --- | --- |
| `pyproject.toml` | Defines project `onyx`, requires Python `>=3.11`, lists dependency groups, and includes `pytest==9.0.3` plus pytest plugins in the `dev` group. |
| `uv.lock` | Lock file is present and contains resolved pytest packages including `pytest`, `pytest-asyncio`, `pytest-dotenv`, `pytest-mock`, `pytest-playwright`, `pytest-repeat`, and `pytest-xdist`. |
| `backend/uv.lock` | Secondary backend lock file is present. |
| `backend/requirements/README.md` | States `pyproject.toml` is the dependency source of truth, `uv.lock` is the unified lock file, legacy `.txt` requirements are for Docker compatibility, and development install is `uv sync`. |
| `backend/requirements/default.txt` | Legacy exported backend requirements file is present. |
| `backend/requirements/dev.txt` | Legacy exported dev requirements file is present. |
| `backend/requirements/ee.txt` | Legacy exported EE requirements file is present. |
| `backend/requirements/model_server.txt` | Legacy exported model-server requirements file is present. |
| `backend/requirements/combined.txt` | Legacy combined requirements file is present. |
| `backend/pytest.ini` | Backend pytest configuration is present. |
| `backend/tests/conftest.py` | Backend shared pytest fixture/conftest file is present and imports application modules during collection. |
| `backend/tests/README.md` | Documents unit-test command `pytest -xv backend/tests/unit` and broader backend test commands. |
| `.github/workflows/security-layer-tests.yml` | Documents minimal isolated security-layer CI dependency install, not full backend dependency installation. |
| `.github/workflows/runtime-retrieval-acl-security.yml` | Documents focused isolated Step 63X CI dependency install, not full backend dependency installation. |
| `CONTRIBUTING.md` | Documents backend Python setup: `uv venv .venv --python 3.11`, `source .venv/bin/activate`, then `uv sync`. |
| `README.md` | Security-layer command references are present, but full backend dependency setup is documented in `CONTRIBUTING.md` and `backend/requirements/README.md`. |
| Makefile/task runner files | No repository-level `Makefile`, `Taskfile`, or `justfile` was found within the inspected max-depth search. |

## Official repository-supported Python dependency installation path

The repository-supported path is `uv`:

1. Create/use a Python 3.11 virtual environment:

   ```bash
   uv venv .venv --python 3.11
   source .venv/bin/activate
   ```

2. Install required dependencies:

   ```bash
   uv sync
   ```

Evidence:

- `CONTRIBUTING.md` says the backend uses `uv`, recommends a `.venv`, and documents `uv venv .venv --python 3.11`, `source .venv/bin/activate`, and `uv sync`.
- `backend/requirements/README.md` says `pyproject.toml` is the source of truth, `uv.lock` is the unified lock file, legacy `backend/requirements/*.txt` files are for Docker compatibility, and development installation is `uv sync`.
- `pyproject.toml` defines dependency groups and includes `pytest==9.0.3` in the `dev` group; `[tool.uv]` has default groups including `dev`.

## Commands attempted

### Pre-repair environment check

Command:

```bash
.venv/bin/python -m pytest --version
```

Exit code: `1`

Output:

```text
/workspace/myproject001/.venv/bin/python: No module named pytest
```

### Official documented virtualenv creation command

Command:

```bash
uv venv .venv --python 3.11
```

Exit code: `1`

Output:

```text
  × Failed to download
  │ https://github.com/astral-sh/python-build-standalone/releases/download/20250712/cpython-3.11.13%2B20250712-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz
  ├─▶ Request failed after 3 retries
  ├─▶ error sending request for url
  │   (https://github.com/astral-sh/python-build-standalone/releases/download/20250712/cpython-3.11.13%2B20250712-x86_64-unknown-linux-gnu-install_only_stripped.tar.gz)
  ├─▶ client error (Connect)
  ╰─▶ tunnel error: unsuccessful
EXIT_CODE=1
Python 3.14.4
```

### Local Python 3.11 interpreter discovery

Command:

```bash
python3.11 --version
```

Exit code: `127`

Output:

```text
pyenv: python3.11: command not found

The `python3.11' command exists in these Python versions:
  3.11.15

Note: See 'pyenv help global' for tips on allowing multiple
      Python versions to be found at the same time.
```

Command:

```bash
PYENV_VERSION=3.11.15 python --version
```

Exit code: `0`

Output:

```text
Python 3.11.15
```

### Repo-supported virtualenv creation using available local Python 3.11

Command:

```bash
PYENV_VERSION=3.11.15 uv venv .venv --python 3.11
```

Exit code: `0`

Output:

```text
Using CPython 3.11.15 interpreter at: /root/.pyenv/versions/3.11.15/bin/python3.11
Creating virtual environment at: .venv
EXIT_CODE=0
Python 3.11.15
```

### Repo-supported dependency sync

Command:

```bash
PYENV_VERSION=3.11.15 uv sync
```

Exit code: `1`

Output:

```text
Resolved 445 packages in 8ms
   Building onyx @ file:///workspace/myproject001
  × Failed to download `google-cloud-aiplatform==1.133.0`
  ├─▶ Failed to fetch:
  │   `https://files.pythonhosted.org/packages/01/5b/ef74ff65aebb74eaba51078e33ddd897247ba0d1197fd5a7953126205519/google_cloud_aiplatform-1.133.0-py2.py3-none-any.whl`
  ├─▶ Request failed after 3 retries
  ├─▶ error sending request for url
  │   (https://files.pythonhosted.org/packages/01/5b/ef74ff65aebb74eaba51078e33ddd897247ba0d1197fd5a7953126205519/google_cloud_aiplatform-1.133.0-py2.py3-none-any.whl)
  ├─▶ client error (Connect)
  ╰─▶ tunnel error: unsuccessful
  help: `google-cloud-aiplatform` (v1.133.0) was included because `onyx`
        (v0.0.0) depends on `litellm[google]` (v1.83.14) which depends on
        `google-cloud-aiplatform`
EXIT_CODE=1
/workspace/myproject001/.venv/bin/python: No module named pytest
PYTEST_EXIT=1
```

### Required backend unit test collection command

Command:

```bash
source .venv/bin/activate
python -m pytest --collect-only backend/tests/unit -q
```

Exit code: `1`

Output:

```text
/workspace/myproject001/.venv/bin/python: No module named pytest
EXIT_CODE=1
```

### Closest repo-supported backend unit test command from docs

Command:

```bash
source .venv/bin/activate
pytest -xv backend/tests/unit
```

Exit code: `4`

Output:

```text
ImportError while loading conftest '/workspace/myproject001/backend/tests/conftest.py'.
backend/tests/conftest.py:7: in <module>
    from onyx.utils.variable_functionality import fetch_versioned_implementation
backend/onyx/utils/variable_functionality.py:8: in <module>
    from onyx.configs.app_configs import API_SERVER_HOST
backend/onyx/configs/app_configs.py:8: in <module>
    from onyx.auth.schemas import AuthBackend
backend/onyx/auth/schemas.py:5: in <module>
    from fastapi_users import schemas
E   ModuleNotFoundError: No module named 'fastapi_users'
EXIT_CODE=4
```

Important boundary: this `pytest` executable came from `/root/.pyenv/shims/pytest`, not from `.venv/bin/python`. The active virtualenv Python still could not import pytest:

Command:

```bash
source .venv/bin/activate
which python
python --version
which pytest
pytest --version
python -c 'import sys; print(sys.executable); import pytest; print(pytest.__version__)'
```

Exit code: `1` for the Python import check

Output:

```text
/workspace/myproject001/.venv/bin/python
Python 3.11.15
/root/.pyenv/shims/pytest
pytest 9.0.3
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'pytest'
/workspace/myproject001/.venv/bin/python
PY_IMPORT_EXIT:1
```

### `uv run` collection attempt

Command:

```bash
PYENV_VERSION=3.11.15 uv run pytest --collect-only backend/tests/unit -q
```

Exit code: `1`

Output:

```text
   Building onyx @ file:///workspace/myproject001
  × Failed to download `onnxruntime==1.20.1`
  ├─▶ Failed to fetch:
  │   `https://files.pythonhosted.org/packages/11/ac/4120dfb74c8e45cce1c664fc7f7ce010edd587ba67ac41489f7432eb9381/onnxruntime-1.20.1-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl`
  ├─▶ Request failed after 3 retries
  ├─▶ error sending request for url
  │   (https://files.pythonhosted.org/packages/11/ac/4120dfb74c8e45cce1c664fc7f7ce010edd587ba67ac41489f7432eb9381/onnxruntime-1.20.1-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl)
  ├─▶ client error (Connect)
  ╰─▶ tunnel error: unsuccessful
  help: `onnxruntime` (v1.20.1) was included because `onyx:backend` (v0.0.0)
        depends on `markitdown` (v0.1.2) which depends on `magika` (v0.6.3)
        which depends on `onnxruntime`
EXIT_CODE=1
```

Note: the failed URL in the command output is recorded exactly as emitted for this run.

## Result classification

`TEST_EXECUTION_BLOCKED`

Reason: pytest could not be installed into the repository virtualenv using the repository-supported `uv sync` path because package downloads from external package hosts failed with tunnel connection errors. The required command `python -m pytest --collect-only backend/tests/unit -q` therefore still fails with `No module named pytest` under `.venv/bin/python`.

## Remaining blockers

1. The checkout has no configured `origin` remote, so the requested base branch could not be fetched or verified from GitHub in this environment.
2. The default Python was initially `3.14.4`; the documented backend setup expects Python 3.11. This was partially repaired by creating `.venv` with local pyenv Python `3.11.15`.
3. `uv sync` cannot complete because package downloads from external hosts failed with tunnel connection errors.
4. `.venv/bin/python -m pytest` remains unavailable after the failed sync.
5. A global pyenv `pytest` shim exists, but it is not proof that the repository `.venv` is correctly installed. It also reaches an application dependency import failure (`fastapi_users`) when running the documented unit test command.

## Safe claims

- The repository-supported dependency installation method is documented as `uv venv .venv --python 3.11`, virtualenv activation, and `uv sync`.
- A Python 3.11 virtualenv was recreated locally using `PYENV_VERSION=3.11.15 uv venv .venv --python 3.11`.
- Backend unit test collection was attempted with `python -m pytest --collect-only backend/tests/unit -q`.
- Test execution remains blocked in the repository virtualenv because `pytest` is not installed there.
- The blocker is documented with exact commands, exit codes, and observed errors.

## Forbidden claims

- Do not claim backend tests passed.
- Do not claim test collection recovered.
- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim runtime security enforcement was improved.
- Do not treat the global pyenv `pytest` shim as a valid repository virtualenv install.

## Next recommended step

Run the same documented setup in an environment where the configured package indexes are reachable, or provide a repository-supported offline dependency cache/wheelhouse. Then rerun:

```bash
source .venv/bin/activate
python -m pytest --collect-only backend/tests/unit -q
```
