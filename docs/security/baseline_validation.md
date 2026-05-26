# Baseline Validation Record (Step 1)

## Scope
This document records baseline validation evidence only. No security-layer features were implemented, and no application behavior was intentionally modified.

## Baseline fingerprint
- Branch: `work`
- Commit: `5791e31c91e9b2fc90721fa521f0167f51a34104`
- Timestamp (UTC): see `docs/security/evidence/baseline_repo_snapshot.txt`

## Evidence index
- `docs/security/evidence/baseline_repo_snapshot.txt`
  - repo identity, git metadata, top-level directory snapshot
- `docs/security/evidence/baseline_stack_detection.txt`
  - dependency and stack detection output
- `docs/security/evidence/baseline_env_checks.txt`
  - Python/Node/npm/pytest version checks
- `docs/security/evidence/unit_collect_only.txt`
  - raw pytest unit collection output
- `docs/security/evidence/unit_collect_only.exitcode`
  - exit code of pytest collection attempt

## Validation commands and outcomes
- PASS: repo snapshot and metadata capture commands
- PASS: environment version checks
- FAIL: backend unit test collection
  - command: `source .venv/bin/activate && pytest -xv backend/tests/unit --collect-only`
  - observed error: `ModuleNotFoundError: No module named 'fastapi_users'`
  - exit code: `4`

## Skipped execution
- Full backend unit/external dependency/integration suites — skipped in this phase; baseline task prohibits scope expansion into setup/fixing.
- Frontend Jest/Playwright suites — skipped in this phase; same reason.

## Constraints honored
- No security-layer implementation changes.
- No refactors.
- No behavioral modifications.
- Failures recorded as observed without remediation.

## Remaining blockers
- Python environment appears incomplete for backend test collection (`fastapi_users` missing).
- Until dependency state is resolved, full baseline validation remains blocked.

## Follow-up (next step, not executed here)
- Reproduce environment provisioning used by project maintainers.
- Re-run baseline test matrix and append outputs to `docs/security/evidence/`.

## Step 2A Cleanup Note (Branch/Evidence Chain Repair)
- Original baseline validation execution happened on branch `work`.
- Baseline evidence was moved/replayed onto `security-layer-mvp` so validation artifacts live on the intended branch.
- The expected historical commits `c00de38`, `f647b54`, and `30e516433f17ad42af24d4b02db67a0f1098ca7b` were not present in this repository clone and could not be cherry-picked by object ID.
- As a safe replacement, the baseline documentation/evidence chain was reconstructed with documentation-only updates and raw evidence file placement under `docs/security/evidence/baseline/`.
- `f647b54` ancestry was explicitly checked and is **not verifiable in this clone** because the commit object is missing.
- No application code paths, runtime behavior, or tests were modified in this cleanup.

### Uncommitted local evidence note
The following raw evidence file remains outside `docs/security/evidence/baseline/` and was not replayed into that folder because it includes secret-related placeholder configuration strings and requires sanitization review before duplication:
- `docs/security/evidence/baseline_stack_detection.txt`
