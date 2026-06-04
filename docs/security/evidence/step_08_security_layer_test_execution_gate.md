# Step 08 Security-Layer Test Execution Gate

## Metadata

| Field | Value |
| --- | --- |
| UTC timestamp | 2026-06-04T13:40:00Z |
| Branch name | `step-08-security-layer-test-execution-gate` |
| Base branch | `step-63x-runtime-retrieval-acl-proof` |
| Starting commit SHA | `d21a3e0af98edf96bb06d7976cf6f9eb1f027c6b` |

## Objective

Step 08 turns the already existing isolated security-layer test workflow into a stronger evidence-producing test execution gate.

This step does not add new security controls. It improves the proof trail for the existing isolated security-layer helper tests by preserving test output and environment metadata as GitHub Actions artifacts.

## Precondition from Step 07

Step 07 recovered backend unit-test collection in CI after fixing the `SearchSettings` runtime annotation failure.

Safe classification after Step 07 CI success:

```text
TEST_COLLECTION_RECOVERED_BY_CI
```

This does not prove full backend test success. It proves only that backend unit-test collection can complete in CI after the annotation fix.

## Workflow updated

```text
.github/workflows/security-layer-tests.yml
```

## Test command preserved

```bash
python -m pytest backend/security_layer/tests -q -ra
```

The workflow still runs the isolated security-layer helper tests. It does not stand up the full Onyx application, does not validate production deployment, and does not prove live enforcement.

## Artifact paths

Security-layer test log:

```text
.artifacts/security-layer-tests/security-layer-tests.log
```

Environment metadata:

```text
.artifacts/security-layer-tests/environment.txt
```

Uploaded artifact name:

```text
isolated-security-layer-test-evidence
```

## Workflow evidence improvements

The workflow now:

- creates `.artifacts/security-layer-tests`;
- records Python, pytest, working-directory, commit, ref, and command metadata;
- runs the isolated security-layer tests with `tee`;
- preserves pytest exit behavior with `set -o pipefail`;
- uploads test output and environment metadata with `actions/upload-artifact@v4` and `if: always()`.

## Expected CI result

If the existing isolated security-layer tests continue passing, classify the result as:

```text
SECURITY_LAYER_TEST_EXECUTION_PROVEN_BY_CI
```

If the workflow fails, classify the result as:

```text
SECURITY_LAYER_TEST_EXECUTION_FAILED_IN_CI
```

## Safe claims

- The isolated security-layer test workflow now produces reviewer-visible CI artifacts.
- Passing isolated security-layer tests prove only isolated helper behavior covered by those tests.
- Step 08 improves test evidence and reproducibility.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Forbidden claims

- Do not claim production security.
- Do not claim enterprise readiness.
- Do not claim live Onyx-wide enforcement.
- Do not claim full backend test success.
- Do not claim full deployment readiness.
- Do not claim compliance certification.

## Commands expected from CI

```bash
python -m pip install --upgrade pip
python -m pip install pytest "pydantic==2.11.7"
python -m pytest backend/security_layer/tests -q -ra
```

## Acceptance criteria

- `Security Layer Tests` workflow passes in GitHub Actions.
- Artifact `isolated-security-layer-test-evidence` is uploaded.
- The artifact includes `security-layer-tests.log` and `environment.txt`.
- Claim boundary checks pass.
- Production readiness remains `NO-GO`.
- Enterprise readiness remains `NO-GO`.

## Next step

After Step 08 passes, proceed to Step 09: add an actual backend test execution gate for a narrow, safe backend unit-test subset, separate from full backend unit-test collection.
