# Baseline Validation (Clean Rebuild)

## Lineage note
- Branch: `security-layer-mvp`
- Rebuilt from source commit: `502239d50c41172ae14759fe3cc31780ace71b98`
- Intent: create a clean, documentation/evidence-only baseline package and supersede prior baseline attempts on `work`.

## Command matrix
| Area | Command | Outcome |
|---|---|---|
| Branch confirmation | `git branch --show-current` | PASS (`security-layer-mvp`) |
| Source commit pin | `git rev-parse HEAD` (post-reset) | PASS (`502239d50c41172ae14759fe3cc31780ace71b98`) |
| Env checks | see `docs/security/evidence/baseline/baseline_env_checks.txt` | PASS |
| Repo snapshot | see `docs/security/evidence/baseline/baseline_repo_snapshot.txt` | PASS |
| Stack detection | see `docs/security/evidence/baseline/baseline_stack_detection.txt` | PASS |
| Unit collect-only | `source .venv/bin/activate && pytest -xv backend/tests/unit --collect-only` | FAIL (exit code captured) |

## Passing checks
- Branch rebuild and verification completed.
- Environment/version snapshot captured.
- Repository snapshot captured.
- Stack/tooling detection snapshot captured.

## Failing checks
- Unit-test collection failed in baseline mode; raw output captured in evidence.
- Exit code recorded in `unit_collect_only.exitcode`.

## Skipped checks
- Full backend unit execution.
- External dependency unit tests.
- Integration tests.
- Frontend tests/lint/typecheck.
- Playwright E2E.

## Known blockers
- Baseline unit collection failure (see captured output).
- Per task constraints, no dependency changes or remediation were performed.

## Evidence file list
- `docs/security/evidence/README.md`
- `docs/security/evidence/baseline/baseline_env_checks.txt`
- `docs/security/evidence/baseline/baseline_repo_snapshot.txt`
- `docs/security/evidence/baseline/baseline_stack_detection.txt`
- `docs/security/evidence/baseline/unit_collect_only.txt`
- `docs/security/evidence/baseline/unit_collect_only.exitcode`
