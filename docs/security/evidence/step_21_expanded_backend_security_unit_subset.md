# Step 21 Expanded Backend Security Unit Subset

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T15:55:00Z |
| Branch name | `step-21-expanded-backend-security-unit-subset` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `f34f6578bbb45c64fa5cf4616eb21bde12e92480` |

## Objective

Step 21 starts the next engineering-proof phase after the reviewer-evidence sequence completed in Step 20.

It expands the existing backend unit subset CI gate from one backend LLM secret-scrubbing test file to a small security-relevant backend unit subset covering:

- LLM credential / secret scrubbing;
- sensitive value masking and safe-access behavior;
- permission implication and authorization denial logic.

This is a stronger backend test-execution proof than the previous single-file subset, but it is still not full backend test success, production readiness, or enterprise readiness.

## Workflow updated

```text
.github/workflows/backend-unit-subset-tests.yml
```

## Previous subset

```text
backend/tests/unit/onyx/llm/test_llm_utils_scrub.py
```

## Expanded subset

```text
backend/tests/unit/onyx/llm/test_llm_utils_scrub.py
backend/tests/unit/onyx/utils/test_sensitive.py
backend/tests/unit/onyx/auth/test_permissions.py
```

## Why these tests

### LLM secret scrubbing

`backend/tests/unit/onyx/llm/test_llm_utils_scrub.py` verifies that LLM credential and secret values are not leaked through validation/error-message handling paths.

### SensitiveValue safe access and masking

`backend/tests/unit/onyx/utils/test_sensitive.py` verifies masking, safe repr behavior, blocked string/iteration/subscript access, JSON masking, and decryption caching for sensitive values.

### Permission implication and denial logic

`backend/tests/unit/onyx/auth/test_permissions.py` verifies permission expansion, admin behavior, implied permissions, missing-permission denial, and empty-permission denial.

## Command executed by CI

```bash
python -m pytest \
  backend/tests/unit/onyx/llm/test_llm_utils_scrub.py \
  backend/tests/unit/onyx/utils/test_sensitive.py \
  backend/tests/unit/onyx/auth/test_permissions.py \
  -q -ra
```

## Artifact paths

Backend security unit subset log:

```text
.artifacts/backend-unit-subset-tests/backend-security-unit-subset-tests.log
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
EXPANDED_BACKEND_SECURITY_UNIT_SUBSET_PROVEN_BY_CI
```

If the workflow reaches pytest and fails:

```text
EXPANDED_BACKEND_SECURITY_UNIT_SUBSET_FAILED_IN_CI
```

If the workflow fails before pytest execution:

```text
EXPANDED_BACKEND_SECURITY_UNIT_SUBSET_SETUP_FAILED
```

## Safe claims

- Step 21 expands backend unit-test execution evidence to a broader security-relevant subset.
- Passing this workflow proves only the selected backend unit subset.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim full backend test success.
- Do not claim production readiness.
- Do not claim enterprise readiness.
- Do not claim live enforcement.
- Do not claim live blocking.
- Do not claim live filtering.
- Do not claim full Onyx staging.
- Do not claim external validation.
- Do not claim compliance certification.

## Acceptance criteria

- `Backend Unit Subset Tests` workflow runs in GitHub Actions.
- All three selected backend unit-test files execute.
- Artifact `backend-unit-subset-test-evidence` is uploaded.
- If the workflow passes, classify as `EXPANDED_BACKEND_SECURITY_UNIT_SUBSET_PROVEN_BY_CI`.
- Claim boundaries remain visible.

## Next step

If Step 21 passes, Step 22 should add an explicit CI artifact index/update documenting the expanded backend subset result in the final reviewer status snapshot or completion checkpoint.
