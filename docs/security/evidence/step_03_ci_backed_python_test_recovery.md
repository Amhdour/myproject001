# Step 03 CI-Backed Python Test Recovery Evidence

## Scope

This evidence records the smallest CI-backed recovery gate added to determine whether backend Python unit-test collection can pass in GitHub Actions when the local Codex environment cannot complete repository dependency installation.

No runtime application code was refactored. No security controls were added.

## Environment

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T11:03:42Z |
| Branch name | `step-03-ci-backed-python-test-recovery` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Current commit SHA at evidence creation | `b11ae490cecd07195b259aebec00ccc16e690b7b` |
| Local checkout remote status | No `origin` remote is configured in this local checkout; fetching the requested base failed locally. |
| Step 03 result marker | `PENDING_CI` |

## CI workflows inspected

| Workflow | Finding |
| --- | --- |
| `.github/workflows/evidence-integrity.yml` | Sets up Python 3.11 and runs evidence-link checks only; it does not install repository Python dependencies and does not collect backend tests. |
| `.github/workflows/portfolio-claim-boundary.yml` | Sets up Python 3.11 and runs portfolio claim-boundary scripts only; it does not install repository Python dependencies and does not collect backend tests. |
| `.github/workflows/runtime-retrieval-acl-security.yml` | Installs only focused pytest dependencies with `pip` for isolated Step 63X security checks; it does not prove repository `.venv` or full backend unit-test collection. |
| `.github/workflows/security-layer-tests.yml` | Installs minimal isolated security-layer test dependencies with `pip`; it intentionally does not stand up Onyx services and does not prove full backend dependency installation or backend unit-test collection. |

## Dependency files inspected

| File | Finding |
| --- | --- |
| `pyproject.toml` | Declares project dependencies, dependency groups, Python `>=3.11`, and pytest/test tooling in the backend/dev dependency set. |
| `uv.lock` | Unified lock file is present and includes resolved pytest packages. |
| `backend/uv.lock` | Secondary backend lock file exists but repository documentation identifies root `uv.lock` with `pyproject.toml` as the dependency source of truth. |
| `backend/requirements/README.md` | Documents `pyproject.toml` as the source of truth, root `uv.lock` as the unified lock file, legacy requirement files for Docker compatibility, and `uv sync` as the development install command. |
| `CONTRIBUTING.md` | Documents Python 3.11, `uv venv .venv --python 3.11`, `source .venv/bin/activate`, and `uv sync` as the backend setup path. |
| `backend/pytest.ini` | Defines backend pytest configuration, Python path entries, markers, warnings, and dotenv support. |

## Dependency install method used

The CI gate uses the repository-supported install path:

```bash
uv sync --frozen
```

The workflow installs `uv` with the official GitHub Action-supported `astral-sh/setup-uv@v8` action, sets up Python 3.11 with `actions/setup-python`, and then runs the collection command through the synced uv environment:

```bash
uv run python -m pytest --collect-only backend/tests/unit -q
```

`--frozen` is used so CI uses the committed lock file rather than updating dependency resolution during the proof run.

## Workflow added

Added:

```text
.github/workflows/python-test-collection.yml
```

The workflow runs on `pull_request` and `workflow_dispatch`, checks out the repository, sets up Python 3.11, installs `uv`, runs `uv sync --frozen`, and then runs backend unit-test collection. The workflow fails honestly if dependency installation or collection fails.

## Local blocker carried forward from Step 02

Step 02 remains the local blocker source:

```text
TEST_EXECUTION_BLOCKED
.venv/bin/python: No module named pytest
```

Step 02 also found that the repository-supported `uv sync` path could not complete in the local Codex environment because external package downloads failed with tunnel errors. A global pyenv pytest shim is not acceptable proof of repository `.venv` recovery.

This Step 03 change does not mark that local blocker resolved.

## Expected CI proof

The expected CI proof is one of the following explicit outcomes from the `Python Backend Test Collection` workflow:

- `TEST_COLLECTION_RECOVERED_BY_CI` if GitHub Actions completes `uv sync --frozen` and `uv run python -m pytest --collect-only backend/tests/unit -q` successfully.
- `TEST_COLLECTION_FAILED_IN_CI` if GitHub Actions fails due to dependency installation, import errors, or pytest collection errors.
- `PENDING_CI` while the workflow has been added but no GitHub Actions result is available in this local environment.

Current recorded status: `PENDING_CI`.

## Safe claims

- A CI-backed backend unit-test collection workflow has been added.
- The workflow uses the repository-supported `uv` dependency installation path.
- The workflow keeps dependency installation and collection failures visible by allowing the job to fail.
- Local repository `.venv` recovery remains unproven in this environment.
- Backend test collection remains pending until GitHub Actions provides a passing or failing result.

## Forbidden claims

This step does not claim:

- production readiness,
- enterprise readiness,
- live security enforcement readiness,
- runtime application behavior changes,
- new or improved security controls,
- repository `.venv` recovery in local Codex,
- backend test collection success before CI reports it, or
- resolution of `TEST_EXECUTION_BLOCKED` without repository `.venv` or CI proof.

## Remaining blockers

- `PENDING_CI`: GitHub Actions has not yet reported whether backend unit-test collection passes with `uv sync --frozen`.
- `LOCAL_UV_SYNC_BLOCKED`: local dependency installation remains blocked by the Step 02 external package download tunnel errors.
- `LOCAL_TEST_EXECUTION_BLOCKED`: local `.venv/bin/python` still cannot be treated as recovered unless repository dependencies are installed and pytest collection is rerun successfully.
- Production readiness remains **NO-GO**.
- Enterprise readiness remains **NO-GO**.

## Local validation commands run

| Command | Exit code | Result |
| --- | ---: | --- |
| `git diff --check` | 0 | Passed with no whitespace errors. |
| `python scripts/portfolio/check_claim_boundary.py` | 0 | Passed; no unsafe positive readiness claims found. |
| `python scripts/portfolio/check_no_fake_claims.py` | 0 | Passed; no unsupported positive evidence claims found. |
| `source .venv/bin/activate && python -m pytest --collect-only backend/tests/unit -q` | 1 | Failed locally because `.venv/bin/python` reports `No module named pytest`. |
| `source .venv/bin/activate && python -m pytest backend/security_layer/tests -q` | 1 | Failed locally for the same environment blocker: `.venv/bin/python` reports `No module named pytest`. |

The local pytest failures are preserved as evidence of the Step 02 local dependency blocker, not hidden or treated as recovered.
