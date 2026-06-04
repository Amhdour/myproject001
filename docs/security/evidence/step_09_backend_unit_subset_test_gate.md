# Step 09 Backend Unit Subset Test Gate

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T13:55:00Z |
| Branch name | `step-09-backend-unit-subset-test-gate` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `857605ff9d45917658522d0513558c7003007af0` |

## Objective

Step 09 adds a narrow backend unit-test execution gate, separate from:

- full backend unit-test collection;
- isolated `backend/security_layer/tests` execution;
- production or staging validation.

This step executes one real backend unit-test file that is security-relevant and bounded enough for CI evidence.

## Selected backend unit-test subset

```text
backend/tests/unit/onyx/llm/test_llm_utils_scrub.py
```

## Why this subset

This file tests LLM credential and secret-scrubbing behavior around error messages and API-key handling. It is security-relevant because it checks that sensitive values are not echoed back through LLM validation and error-handling paths.

The test file is narrow compared with the full backend test suite and does not intentionally stand up the full Onyx application, external services, staging deployment, or live enforcement.

## Workflow added

```text
.github/workflows/backend-unit-subset-tests.yml
```

## Test command

```bash
python -m pytest backend/tests/unit/onyx/llm/test_llm_utils_scrub.py -q -ra
```

## Dependency setup

The workflow uses the repository dependency path already proven by the Python Backend Test Collection workflow:

```bash
uv sync --frozen
```

## Artifact paths

Backend unit subset test log:

```text
.artifacts/backend-unit-subset-tests/backend-llm-secret-scrub-tests.log
```

Environment metadata:

```text
.artifacts/backend-unit-subset-tests/environment.txt
```

Uploaded artifact name:

```text
backend-unit-subset-test-evidence
```

## Expected CI classifications

If the workflow passes and uploads the artifact:

```text
BACKEND_UNIT_SUBSET_TEST_EXECUTION_PROVEN_BY_CI
```

If the workflow reaches pytest and fails:

```text
BACKEND_UNIT_SUBSET_TEST_EXECUTION_FAILED_IN_CI
```

If the workflow fails before pytest execution:

```text
BACKEND_UNIT_SUBSET_WORKFLOW_SETUP_FAILED
```

## Safe claims

- Step 09 adds a CI-backed backend unit-test subset execution gate.
- The selected subset covers LLM credential/secret-scrubbing behavior in backend unit tests.
- Passing this workflow proves only that this specific backend unit-test subset passed in CI.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim full backend unit-test success.
- Do not claim full application security.
- Do not claim live enforcement.
- Do not claim full Onyx staging.
- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim compliance certification.

## Acceptance criteria

- `Backend Unit Subset Tests` workflow runs in GitHub Actions.
- The selected backend unit-test file executes.
- Artifact `backend-unit-subset-test-evidence` is uploaded.
- If the workflow passes, classify as `BACKEND_UNIT_SUBSET_TEST_EXECUTION_PROVEN_BY_CI`.
- Claim boundaries remain visible.

## Next step

After Step 09 passes, proceed to Step 10: add a demo attack execution gate that produces a reviewer-safe attack/result artifact without claiming production security.
